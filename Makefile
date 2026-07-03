LATEX = latexmk -pdflua

.PHONY: latex web clean help

help:
	@echo "latex        Build PDF from LaTeX"
	@echo "clean        Clean build artifacts and cache files"
	@echo "web          Build website"
	@echo "serve        Run dev server"

latex: web/docs/cv.pdf web/docs/certificates.pdf

web/docs/cv.pdf: latex/cv.tex latex/shared.tex
	$(LATEX) latex/cv.tex -cd -output-directory="../web/docs"

web/docs/certificates.pdf: latex/certificates.tex latex/shared.tex
	$(LATEX) latex/certificates.tex -cd -output-directory="../web/docs"

clean:
	$(LATEX) -C latex/cv.tex -cd -output-directory="../web/docs"
	$(LATEX) -C latex/certificates.tex -cd -output-directory="../web/docs"
	rm -rf web/site
	rm -rf web/.cache

web:
	cd web && zensical build

serve:
	cd web && zensical serve
