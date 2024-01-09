# Compile all LaTeX files into PDFs
TEX_FILES := $(wildcard *.tex)
PDF_FILES := $(TEX_FILES:.tex=.pdf)

all: $(PDF_FILES)

%.pdf: %.tex
	pdflatex $<
	rm -f $*.log $*.aux $*.out $*.bbl $*.blg $*.toc

clean:
	rm -f $(PDF_FILES)