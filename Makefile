

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

serve:
	zensical serve

build:
	zensical build

cv:
	latexmk -pdflua latex/cv.tex -cd -output-directory="../docs"
	latexmk -pdflua latex/certificates -cd -output-directory="../docs"
