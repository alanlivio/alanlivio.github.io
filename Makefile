MAKEFLAGS += -s --no-print-directory
.DEFAULT_GOAL := help
$(if $(filter Windows_NT,$(OS)),$(if $(shell where printf 2>nul),,$(error coreutils is not installed. Please run: winget install coreutils)))

LATEX := latexmk -pdflua

.PHONY: help deps test latex build serve format clean

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
		"  format   Format Python code with black" \
		"  clean    Clean build artifacts and cache files"

deps:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

latex: website/docs/cv.pdf website/docs/certificates.pdf

website/docs/cv.pdf: latex/cv.tex latex/shared.tex website/zensical.toml
	$(LATEX) latex/cv.tex -cd -output-directory="../website/docs"
	$(LATEX) -c latex/cv.tex -cd -output-directory="../website/docs"

website/docs/certificates.pdf: latex/certificates.tex latex/shared.tex website/zensical.toml
	$(LATEX) latex/certificates.tex -cd -output-directory="../website/docs"
	$(LATEX) -c latex/certificates.tex -cd -output-directory="../website/docs"

build: latex
	cd website && python -m zensical build

serve:
	cd website && python -m zensical serve

format:
	python -m black .

clean:
	$(LATEX) -C latex/cv.tex -cd -output-directory="../website/docs"
	$(LATEX) -C latex/certificates.tex -cd -output-directory="../website/docs"
	rm -f latex/*.aux latex/*.log latex/*.out latex/*.synctex.gz latex/*.toc latex/*.fls latex/*.fdb_latexmk latex/*.pdf
	rm -f website/docs/*.aux website/docs/*.log website/docs/*.out website/docs/*.synctex.gz website/docs/*.toc website/docs/*.fls website/docs/*.fdb_latexmk website/docs/cv.pdf website/docs/certificates.pdf
	rm -rf website/site
	rm -rf website/.cache
	rm -rf .cache
	rm -rf dist build ./*.egg-info zensical-academic/*.egg-info
