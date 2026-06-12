serve:
	zensical serve

setup:
	pip install -r requirements.txt

build:
	zensical build

test: build

cv:
	latexmk -pdflua latex/cv.tex -cd -output-directory="../docs"

certificates:
	latexmk -pdflua latex/certificates -cd -output-directory="../docs"
