.DEFAULT_GOAL := serve

ifeq ($(OS),Windows_NT)
setup-latex:
	-winget install MiKTeX.MiKTeX
	-winget install StrawberryPerl.StrawberryPerl
else
setup-latex:
	sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra
endif

setup-pip:
	pip install -r requirements.txt

setup: setup-pip setup-latex

test: build

serve: cv
	zensical serve

build:
	zensical build

cv: docs/cv.pdf docs/certificates.pdf

docs/cv.pdf: latex/cv.tex latex/shared.tex
	latexmk -pdflua latex/cv.tex -cd -output-directory="../docs"

docs/certificates.pdf: latex/certificates.tex latex/shared.tex
	latexmk -pdflua latex/certificates.tex -cd -output-directory="../docs"

.PHONY: setup-latex setup-pip setup test serve build cv
