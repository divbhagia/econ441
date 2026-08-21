# ECON 441 build.
#
#   make syllabus   regenerate the schedule, rebuild the syllabus PDF
#   make pdfs       recompile handouts, practice problems, module notes
#   make site       rebuild the website into docs/
#   make            all of the above
#
# The site renders in a temp copy outside Dropbox. Dropbox reverts in-place
# overwrites of individual files, which silently drops pages from docs/.

SHELL := /bin/bash
TMP   := $(TMPDIR)econ441-build
NOTES := content/notes/{Linear-Algebra,Calculus,Log-and-Exponential-Functions,Optimization}
AUX   := aux,log,out,fls,fdb_latexmk,xdv,toc,synctex.gz

.PHONY: all syllabus pdfs site

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
	@for f in content/handouts/*.tex content/practice/*.tex $(NOTES).tex; do \
	  [ -e "$$f" ] || continue; \
	  d=$$(dirname "$$f"); b=$$(basename "$$f" .tex); \
	  (cd "$$d"; lualatex -interaction=nonstopmode "$$b.tex" >/dev/null 2>&1; \
	             lualatex -interaction=nonstopmode "$$b.tex" >/dev/null 2>&1; \
	   rm -f "$$b".{$(AUX)}); \
	done
	@echo "    $$(ls content/handouts/*.pdf content/practice/*.pdf $(NOTES).pdf 2>/dev/null | wc -l | tr -d ' ') PDFs"

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
	@rm -rf docs; sleep 8; mkdir -p docs
	@(cd $(TMP)/docs && tar cf - .) | (cd docs && tar xf -)
	@sleep 15
	@find docs -name "*conflicted copy*" -exec rm -rf {} + 2>/dev/null || true
	@echo "    pages: $$(find docs -name '*.html' ! -path '*site_libs*' | wc -l | tr -d ' ')"
