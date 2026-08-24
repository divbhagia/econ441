-- Fix-ups for the tagged-PDF notes build (Makefile target `notes`).
--
-- Pandoc's LaTeX writer drops fig-alt, so \includegraphics goes out with no
-- alt= key and LaTeX's tagging code falls back to tagging each figure with its
-- filename ("assets/venn2.pdf"). Rebuilding the command here keeps the same
-- descriptions the HTML slides use.
--
-- Also rewrites the image path: sources are .svg under assets/, while the notes
-- build wants the converted .pdf at a path relative to the build directory.

if not FORMAT:match('latex') then return {} end

local function tex_escape(s)
  return (s:gsub('\\', '\\textbackslash{}'):gsub('([{}%%&#_%$])', '\\%1'))
end

-- Quarto's widths are bare pixel counts (width=280); LaTeX needs a unit.
local function to_length(v)
  local n = v:match('^(%d+%.?%d*)$')
  if n then return string.format('%.4fin', tonumber(n) / 96) end
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
