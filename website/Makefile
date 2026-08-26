MAKEFLAGS += -s --no-print-directory
LATEX = latexmk -pdflua

.PHONY: build deps serve clean help latex

help:
	@echo "deps        Install dependencies"
	@echo "latex       Build PDF from LaTeX"
	@echo "build       Build website (and compile LaTeX PDFs)"
	@echo "serve       Run dev server"
	@echo "clean       Clean build artifacts and cache files"

deps:
	pip install -r requirements.txt

latex: docs/cv.pdf docs/certificates.pdf

docs/cv.pdf: ../latex/cv.tex ../latex/shared.tex
	$(LATEX) ../latex/cv.tex -cd -output-directory="../website/docs"
	$(LATEX) -c ../latex/cv.tex -cd -output-directory="../website/docs"

docs/certificates.pdf: ../latex/certificates.tex ../latex/shared.tex
	$(LATEX) ../latex/certificates.tex -cd -output-directory="../website/docs"
	$(LATEX) -c ../latex/certificates.tex -cd -output-directory="../website/docs"

build: latex
	zensical build

serve:
	zensical serve

clean:
	$(LATEX) -C ../latex/cv.tex -cd -output-directory="../website/docs"
	$(LATEX) -C ../latex/certificates.tex -cd -output-directory="../website/docs"
	rm -rf site
	rm -rf .cache
