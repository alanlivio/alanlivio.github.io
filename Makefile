LATEX = latexmk -pdflua

.PHONY: latex web clean help

help:
	@echo "latex        Build PDF from LaTeX"
	@echo "clean        Clean build artifacts and cache files"
	@echo "web          Build website"
	@echo "serve        Run dev server"

latex: docs/cv.pdf docs/certificates.pdf

docs/cv.pdf: latex/cv.tex latex/shared.tex
	$(LATEX) latex/cv.tex -cd -output-directory="../docs"

docs/certificates.pdf: latex/certificates.tex latex/shared.tex
	$(LATEX) latex/certificates.tex -cd -output-directory="../docs"

clean:
	$(LATEX) -C latex/cv.tex -cd -output-directory="../docs"
	$(LATEX) -C latex/certificates.tex -cd -output-directory="../docs"
	rm -rf site
	rm -rf .cache
	rm -rf web

web:
	zensical build

serve:
	zensical serve
