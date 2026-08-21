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
- **The site renders in a temp copy outside Dropbox.** Dropbox reverts in-place
  overwrites of individual files, which silently drops pages from `docs/`.

`syllabus/create_schedule.py` is the single source of truth for the schedule —
it writes both `syllabus/schedule.tex` (print) and `schedule.qmd` (web). Edit
the schedule there, never in either output.

## Publishing a new module

Material is gated so only vetted modules appear. To release one:

1. Add its lecture numbers to `PUBLISHED` in `syllabus/create_schedule.py`.
2. Drop the matching `"!content/practice/practiceN.qmd"` and
   `"!content/slides/slidesN.qmd"` lines from `_quarto.yml`.
3. Add the practice pages to the sidebar `contents` in `_quarto.yml` — a page
   that isn't listed there renders without the theme.

## Local-only

These exist on the machine but are gitignored and never reach GitHub, which is
a **public** repo:

| | |
|---|---|
| `grades/` | student grade data and the Canvas API token |
| `exams/` | exams and sample exams |
| `quizzes/` | quizzes |
| `references/`, `rtp-material/` | reference material |
| `lectures-old/` | archived once-a-week format, superseded by `content/` |
| `canvas-upload.py` | creates Canvas assignments; reads the token |

A `.gitignore` rule only applies to files git isn't already tracking. To drop
something already committed, `git rm --cached <path>` — and note it stays
readable in the repo's history.

The once-a-week version of this course is preserved on the `weekly-format`
branch.
