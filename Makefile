# ECON 441 build.
#
#   make syllabus   regenerate the schedule, rebuild the syllabus PDF
#   make pdfs       recompile handouts, practice problems, module notes
#   make site       rebuild the website into docs/
#   make audit      WCAG 2.1 AA check of docs/ (axe-core + reflow + veraPDF); run before publishing
#   make slides-pdf tagged-PDF decks (ltx-talk) from the same slide sources
#   make            all of the above
#
# The site renders in a temp copy outside Dropbox. Dropbox reverts in-place
# overwrites of individual files, which silently drops pages from docs/.

SHELL := /bin/bash
# Published lectures; keep in step with PUBLISHED in syllabus/create_schedule.py.
LECTURES := 1 2 3
TMP   := $(TMPDIR)econ441-build
NOTES := content/notes/{Linear-Algebra,Calculus,Log-and-Exponential-Functions,Optimization}
AUX   := aux,log,out,fls,fdb_latexmk,xdv,toc,synctex.gz

.PHONY: all syllabus pdfs site audit slides-pdf

all: syllabus pdfs site

syllabus:
	@echo "==> schedule (feeds both the syllabus PDF and the website)"
	@python3 syllabus/create_schedule.py
	@echo "==> syllabus PDF"
	@(cd syllabus && lualatex -interaction=nonstopmode Econ441-Syllabus.tex >/dev/null 2>&1; \
	                lualatex -interaction=nonstopmode Econ441-Syllabus.tex >/dev/null 2>&1; \
	  rm -f Econ441-Syllabus.{$(AUX)})
	@pdfinfo syllabus/Econ441-Syllabus.pdf | awk '/^Pages/{print "    pages: " $$2}'

# Compiled in place; the PDFs sit next to the pages that link them, so Quarto
# copies them into docs/ on its own.
pdfs:
	@echo "==> handouts, practice problems, notes"
	@for f in content/handouts/*.tex content/practice/practice-*.tex $(NOTES).tex; do \
	  [ -e "$$f" ] || continue; \
	  d=$$(dirname "$$f"); b=$$(basename "$$f" .tex); \
	  (cd "$$d"; lualatex -interaction=nonstopmode "$$b.tex" >/dev/null 2>&1; \
	             lualatex -interaction=nonstopmode "$$b.tex" >/dev/null 2>&1; \
	   rm -f "$$b".{$(AUX)}); \
	done
	@echo "    $$(ls content/handouts/*.pdf content/practice/practice-*.pdf $(NOTES).pdf 2>/dev/null | wc -l | tr -d ' ') PDFs"

site:
	@echo "==> schedule table (feeds the web page)"
	@python3 syllabus/create_schedule.py >/dev/null
	@echo "==> website"
	@rm -rf $(TMP)
	@rsync -a --exclude .git --exclude grades --exclude docs --exclude .quarto \
	          --exclude _freeze --exclude lectures-old --exclude rtp-material \
	          --exclude references --exclude exams ./ $(TMP)/
	@cd $(TMP) && quarto render
	@mkdir -p $(TMP)/docs/syllabus && cp syllabus/Econ441-Syllabus.pdf $(TMP)/docs/syllabus/
	@mkdir -p docs
	@python3 scripts/sync_docs.py $(TMP)/docs
	@find docs -name "*conflicted copy*" -exec rm -rf {} + 2>/dev/null || true
	@echo "    pages: $$(find docs -name '*.html' ! -path '*site_libs*' | wc -l | tr -d ' ')"

# Every page and PDF must meet WCAG 2.1 AA / PDF/UA-2 (DOJ Title II rule,
# 28 CFR 35.200; CSUF deadline 2027-04-26). Separate from `site` because it
# takes several minutes (Chromium over every page, a JVM over every PDF):
# run it before pushing, and after any new material.
audit:
	@echo "==> accessibility audit (WCAG 2.1 AA + PDF/UA-2)"
	@python3 scripts/audit_a11y.py

# Tagged-PDF slide decks from the same .qmd sources as the web decks, compiled
# under ltx-talk (beamer refuses tagging). Each build veraPDF-gates its output.
slides-pdf:
	@echo "==> slide decks as tagged PDF (ltx-talk)"
	@python3 scripts/build_slides_pdf.py $(LECTURES)
