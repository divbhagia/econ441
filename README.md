ECON 441: Introduction to Mathematical Economics — course website, built with Quarto.
Live at <https://dbhagia.com/econ441/>.

## Layout

```
index.qmd  syllabus.qmd  schedule.qmd   top-level pages
content/                                everything student-facing
  preliminaries.qmd  linear-algebra.qmd
  calculus.qmd       optimization.qmd   module pages
  slides/                               reveal.js decks (.qmd)
  practice/                             practice pages + their .tex/.pdf
  handouts/                             in-class worksheets (.tex/.pdf)
  notes/                                module notes (.tex/.pdf)
syllabus/                               syllabus .tex + create_schedule.py
latex/                                  .cls files used by the .tex sources
assets/                                 css, scss, figures
_extensions/                            Quarto extension — required to render
docs/                                   generated site; never edit by hand
Makefile
```

LaTeX sources live next to the pages that link them. Quarto copies a PDF into
`docs/` only when a rendered page references it, so nothing else gets published.

## Building

```
make syllabus   regenerate the schedule, rebuild the syllabus PDF
make pdfs       recompile handouts, practice problems, module notes
make site       rebuild the website into docs/
make            all of the above
```

Two things the Makefile handles that are easy to get wrong by hand:

- **Compile with LuaLaTeX, not XeLaTeX.** Every source declares
  `\DocumentMetadata{... tagging=on}` for PDF/UA output. Under XeLaTeX the
  tagging silently no-ops and you get an untagged, inaccessible PDF that still
  claims to be UA-2.
