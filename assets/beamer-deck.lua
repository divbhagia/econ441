-- Fix-ups for the tagged-PDF slide deck build (Makefile target `slides-pdf`).
-- Runs on pandoc's *beamer* writer output; the .tex is then compiled under
-- ltx-talk (see scripts/build_slides_pdf.py).
--
-- Pandoc's LaTeX writer drops fig-alt, so \includegraphics goes out with no
-- alt= key and LaTeX's tagging code falls back to tagging each figure with its
-- filename ("assets/venn2.pdf"). Rebuilding the command here keeps the same
-- descriptions the HTML slides use.
--
-- Also rewrites the image path: sources are .svg under assets/, while the notes
-- build wants the converted .pdf at a path relative to the build directory.

if not (FORMAT:match('latex') or FORMAT:match('beamer')) then return {} end

local function tex_escape(s)
  return (s:gsub('\\', '\\textbackslash{}'):gsub('([{}%%&#_%$])', '\\%1'))
end

-- Quarto's widths are bare pixel counts relative to reveal's 1080px canvas;
-- map them to the same fraction of the frame's text width. (\paperwidth: a reveal pixel width is a fraction of the full 1080px canvas, and
-- \paperwidth is the only unit ltx-talk keeps stable inside columns.)
local function to_length(v)
  local n = v:match('^(%d+%.?%d*)$')
  if n then return string.format('%.3f\\paperwidth', tonumber(n) / 1080) end
  return v
end

local function build_path(src)
  local tail = src:match('assets/(.*)$')          -- keep any sub-directory
  if not tail then return (src:gsub('%.svg$', '.pdf')) end
  return 'assets/' .. tail:gsub('%.svg$', '.pdf')
end

function Image(el)
  local alt = el.attributes['fig-alt']
  if not alt or alt == '' then return nil end

  local opts = {}
  if el.attributes.width  then opts[#opts+1] = 'width='  .. to_length(el.attributes.width)  end
  if el.attributes.height then opts[#opts+1] = 'height=' .. to_length(el.attributes.height) end
  opts[#opts+1] = 'keepaspectratio'
  opts[#opts+1] = 'alt={' .. tex_escape(alt) .. '}'

  return pandoc.RawInline('latex',
    '\\includegraphics[' .. table.concat(opts, ',') .. ']{' .. build_path(el.src) .. '}')
end

-- The decks put the course name above the lecture number with an HTML <br>,
-- which the LaTeX writer drops -- leaving "...Mathematical EconomicsLecture 1".
function RawInline(el)
  if el.format:match('html') and el.text:match('^<br%s*/?>$') then
    return pandoc.RawInline('latex', '\\\\')
  end
end

-- A paragraph that is only an image is centred, as on the old beamer decks.
-- (By the time Para runs, Image above has already turned the image into a
-- RawInline, so that is what to look for.)
function Para(el)
  if #el.content == 1 then
    local x = el.content[1]
    local tex
    if x.t == 'RawInline' and x.text:match('^\\includegraphics') then tex = x.text
    elseif x.t == 'Image' then local i = Image(x); tex = i and i.text end
    if tex then
      return pandoc.RawBlock('latex', '\\begin{center}' .. tex .. '\\end{center}')
    end
  end
end

-- witemize: air between top-level list items (sub-points stay tight). Done
-- here because the class-level knobs (\@listi, the block templates'
-- item-vspace) are both overridden by ltx-talk's own inter-item code.
local function space_lists(blocks, depth)
  for _, b in ipairs(blocks) do
    if b.t == 'BulletList' or b.t == 'OrderedList' then
      for i, item in ipairs(b.content) do
        space_lists(item, depth + 1)
      end
      -- ltx-talk adds \itemsep between items but groups each item's body,
      -- so a local assignment is lost; a global one set in the first item
      -- survives to every later gap on this level. Nested lists set their
      -- own (local) \itemsep, so sub-points stay tight.
      if depth == 0 and #b.content > 0 then
        b.content[1]:insert(1, pandoc.RawBlock('latex', '\\global\\itemsep=0.7em'))
      end
    elseif b.t == 'Div' or b.t == 'BlockQuote' then
      space_lists(b.content, depth)
    end
  end
end
-- On these decks each reveal fragment is its own one-item list, so most of the
-- "gaps between bullets" are gaps between consecutive lists. Add the same air
-- after every top-level block that ends in a list and is followed by more.
local function ends_in_list(b)
  if b.t == 'BulletList' or b.t == 'OrderedList' then return true end
  if b.t == 'Div' and #b.content > 0 then return ends_in_list(b.content[#b.content]) end
  return false
end
local function space_between_lists(blocks)
  local out = pandoc.List()
  for i, b in ipairs(blocks) do
    if b.t == 'Div' then b.content = space_between_lists(b.content) end
    out:insert(b)
    local nxt = blocks[i + 1]
    if nxt and ends_in_list(b) and nxt.t ~= 'Header' then
      out:insert(pandoc.RawBlock('latex', '\\vspace{0.7em}'))
    end
  end
  return out
end
function Pandoc(doc)
  space_lists(doc.blocks, 0)
  doc.blocks = space_between_lists(doc.blocks)
  return doc
end
