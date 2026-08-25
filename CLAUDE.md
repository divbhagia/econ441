# ECON 441 course site

Quarto website (output in `docs/`, served via GitHub Pages) plus LaTeX-built
PDFs (handouts, notes, syllabus). `make site` renders in a temp copy outside
Dropbox and replaces `docs/` — never render into `docs/` directly.

## Accessibility is a hard requirement

Everything published on this site must meet **WCAG 2.1 Level AA** (DOJ Title II
rule, 28 CFR 35.200; CSUF's compliance deadline is 2027-04-26). The site has an
[accessibility statement](accessibility.qmd) promising this. Non-negotiable for
any new or edited material:

- **Every figure gets `fig-alt`** (markdown) or `alt` (raw HTML) describing
  what it shows. Decorative icons get `aria-hidden="true"` instead.
- **Math is authored as TeX** (rendered to MathML) — never as an image of an
  equation.
- **Text contrast ≥ 4.5:1** on white. Safe theme colors: `#912040` (8.5:1),
  `#393A3B` (11.4:1), `#747576` (4.6:1), `#6b6b6b` (5.3:1), `#595a5b` (6.9:1).
  Anything lighter fails at normal text size.
- **Raw HTML blocks need real semantics**: header cells with `scope`, valid
  list nesting (no `<ul>` directly inside `<ul>`), `aria-label` on icon-only
  links, `tabindex="0"` on scrollable regions.
- **PDFs are tagged AND validated**: every `.tex` starts with
  `\DocumentMetadata{pdfstandard=UA-2,pdfversion=2.0,lang=en-US,tagging=on}`,
  compiles with lualatex, and must pass `verapdf --flavour ua2` (part of
  `make audit`). Figures in LaTeX get `alt={...}` on `\includegraphics`.
- **LaTeX constructs that break tagging** (all found the hard way; veraPDF
  catches them): TeX-primitive `$$...$$` display math unbalances tagpdf's
  paragraph hooks -- use `\[...\]`; the `tasks` package emits invalid
  structure -- use enumerate inside `multicols`; argument-taking commands like
  `\textit` in sectsty's `\sectionfont`/`\subsectionfont` swallow the heading
  closure so everything nests inside the Hn -- use switches (`\itshape`);
  boxed constructs that create paragraphs-in-paragraphs need
  `\tagpdfparaOff`/`\tagpdfparaOn` (see `\myheader` in latex/handout.cls);
  newtx's txexs/txexas fonts need the `\pdfglyphtounicode` lines in
  handout.cls for extensible-symbol pieces.
- Don't convey meaning by color alone; keep pages usable at 320px width
  (wide content scrolls in its own container, never the page).

## Audit

`make audit` checks every built page and PDF: axe-core (WCAG 2.1 A/AA), a
reflow check at 320px, and veraPDF PDF/UA-2 validation of every PDF in docs/.
It is a separate target (it takes several minutes) and exits nonzero on any
failure — **run `make audit` after `make site` and before pushing; nothing
is published until it passes.** The audit script is
`scripts/audit_a11y.py` (axe vendored at `scripts/axe.min.js`; verapdf via
Homebrew).

## Slide decks as tagged PDF

`make slides-pdf` builds a tagged-PDF version of each published deck from the
SAME `.qmd` source, via pandoc's beamer writer compiled under `ltx-talk` (the
LaTeX team's tagging-aware talk class -- beamer itself refuses tagging).
Script: `scripts/build_slides_pdf.py`; fig-alt survives via
`assets/beamer-deck.lua`; overlays are stripped (the PDF is the complete-slides
study artifact); each deck is veraPDF-gated at build time. `LECTURES` in the
Makefile lists what gets built -- keep it in step with PUBLISHED in
syllabus/create_schedule.py, and rerun `make slides-pdf` before `make site`
when a deck changes. ltx-talk is experimental: after `tlmgr update`, rebuild
and re-audit before publishing.

Known gotchas that caused real failures before:

- reveal.js emits `user-scalable=no` and unlabeled menu chrome; fixed at
  runtime by `assets/slides-a11y.html` (included via `content/slides/_metadata.yml`).
  Don't remove that include.
- Quarto ships `.reveal .slide ul li` margin rules that silently outrank
  simpler selectors in `assets/slides.scss` — match that specificity when
  styling slide lists. Quarto's SCSS compiler also drops `:has()` rules.
- Long inline equations overflow narrow viewports; `assets/site-a11y.html`
  (included site-wide via `_quarto.yml`) makes actual offenders scrollable and
  keyboard-reachable. Don't remove that include either.

## Schedule table

`schedule.qmd` is generated — edit `syllabus/create_schedule.py`, not the qmd.
The same script emits `syllabus/schedule.tex` for the syllabus PDF.

## Practice problems

HTML practice pages are per lecture (`content/practice/practiceN.qmd`). PDFs
are per **module**: `content/practice/practice-<module>.tex` stitches the
per-lecture bodies (`practiceN-body.tex`, `practiceN_solutions-body.tex`)
under one header; `make pdfs` builds only those. When a new lecture's practice
set is published, add its body to the module file (and split its wrapper the
same way if it still has the content inline).
