.DEFAULT_GOAL := serve

RM = python -c "import os, shutil, glob; [shutil.rmtree(f) if os.path.isdir(f) else os.remove(f) for mask in '$(1)'.split() for f in glob.glob(mask)]"

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

clean:
	@$(call RM,site)
	@$(call RM,.cache)
	@$(call RM,docs/cv.aux docs/cv.log docs/cv.toc docs/cv.out docs/cv.fdb_latexmk docs/cv.fls docs/cv.dvi docs/cv.pdf)
	@$(call RM,docs/certificates.aux docs/certificates.log docs/certificates.toc docs/certificates.out docs/certificates.fdb_latexmk docs/certificates.fls docs/certificates.pdf)
	@$(call RM,latex/*.aux latex/*.log latex/*.toc latex/*.out latex/*.fdb_latexmk latex/*.fls latex/*.synctex.gz latex/cv.pdf latex/certificates.pdf)

.PHONY: setup-latex setup-pip setup test serve build cv clean
