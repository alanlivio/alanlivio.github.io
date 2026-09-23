MAKEFLAGS += -s --no-print-directory
.DEFAULT_GOAL := help

LATEX := latexmk -pdflua

.PHONY: help deps test latex build serve clean

help:
	@printf "%s\n" \
		"Usage: make [target]" \
		"" \
		"Targets:" \
		"  deps     Install dependencies" \
		"  test     Run tests" \
		"  latex    Build PDF from LaTeX" \
		"  build    Build website (and compile LaTeX PDFs)" \
		"  serve    Run dev server" \
		"  clean    Clean build artifacts and cache files"

deps:
	pip install -r website/requirements.txt

test:
	pytest website/tests

latex: website/docs/cv.pdf website/docs/certificates.pdf

website/docs/cv.pdf: latex/cv.tex latex/shared.tex
	$(LATEX) latex/cv.tex -cd -output-directory="../website/docs"
	$(LATEX) -c latex/cv.tex -cd -output-directory="../website/docs"

website/docs/certificates.pdf: latex/certificates.tex latex/shared.tex
	$(LATEX) latex/certificates.tex -cd -output-directory="../website/docs"
	$(LATEX) -c latex/certificates.tex -cd -output-directory="../website/docs"

build: latex
	cd website && zensical build

serve:
	cd website && zensical serve

clean:
	$(LATEX) -C latex/cv.tex -cd -output-directory="../website/docs"
	$(LATEX) -C latex/certificates.tex -cd -output-directory="../website/docs"
	rm -rf website/site
	rm -rf website/.cache
	rm -rf .cache
