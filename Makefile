# ECON 441 build.
#
#   make syllabus   regenerate the schedule, rebuild the syllabus PDF
#   make pdfs       recompile handouts, practice problems, module notes
#   make site       rebuild the website into docs/
#   make notes      tagged-PDF lecture notes from the slide decks
#   make            all of the above (notes are built separately)
#
# The site renders in a temp copy outside Dropbox. Dropbox reverts in-place
# overwrites of individual files, which silently drops pages from docs/.

SHELL := /bin/bash
TMP   := $(TMPDIR)econ441-build
NOTES := content/notes/{Linear-Algebra,Calculus,Log-and-Exponential-Functions,Optimization}
# Lectures whose slides are published; keep in step with PUBLISHED in
# syllabus/create_schedule.py.
LECTURES := 1 2
NBUILD   := $(TMPDIR)econ441-notes
AUX   := aux,log,out,fls,fdb_latexmk,xdv,toc,synctex.gz

.PHONY: all syllabus pdfs site notes

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

# Linear, tagged-PDF version of each lecture deck.
#
# Deliberately article-class, not beamer: beamer refuses \DocumentMetadata
# outright ("not compatible"), and a browser export of the reveal deck is
# untagged, drops every fig-alt and mangles the maths. Going through LaTeX gives
# the same PDF/UA-2 output as the handouts, with the maths tagged as formulas.
#
# Built outside docs/ because the figures resolve relative to the .tex, and the
# .svg sources have to become .pdf first.
notes:
	@echo "==> lecture notes (tagged PDF from the slide decks)"
	@rm -rf $(NBUILD); mkdir -p $(NBUILD)/assets
	@cd assets && find . -name '*.svg' | while read f; do \
	   mkdir -p "$(NBUILD)/assets/$$(dirname $$f)"; \
	   rsvg-convert -f pdf -o "$(NBUILD)/assets/$${f%.svg}.pdf" "$$f"; \
	 done
	@cd assets && find . \( -name '*.png' -o -name '*.jpg' \) | while read f; do \
	   mkdir -p "$(NBUILD)/assets/$$(dirname $$f)"; cp "$$f" "$(NBUILD)/assets/$$f"; \
	 done
	@for n in $(LECTURES); do \
	   quarto render content/slides/slides$$n.qmd --to latex \
	     --metadata-file=assets/notes-format.yml >/dev/null 2>&1; \
	   cp docs/content/slides/slides$$n.tex $(NBUILD)/; \
	   (cd $(NBUILD); \
	    lualatex -interaction=nonstopmode slides$$n.tex >/dev/null 2>&1; \
	    lualatex -interaction=nonstopmode slides$$n.tex >/dev/null 2>&1); \
	   cp $(NBUILD)/slides$$n.pdf content/slides/slides$$n-notes.pdf; \
	   rm -f docs/content/slides/slides$$n.tex; \
	 done
	@rm -rf $(NBUILD)
	@for n in $(LECTURES); do \
	   printf "    lecture %s: " "$$n"; \
	   pdfinfo content/slides/slides$$n-notes.pdf | \
	     awk '/^Pages/{p=$$2}/^Tagged/{t=$$2}END{printf "%s pages, tagged=%s\n",p,t}'; \
	 done
