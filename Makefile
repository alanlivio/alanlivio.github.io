MAKEFLAGS += -s --no-print-directory
.DEFAULT_GOAL := help
$(if $(filter Windows_NT,$(OS)),$(if $(shell where printf 2>nul),,$(error coreutils is not installed. Please run: winget install coreutils)))

LATEX := latexmk -cd -pdflua -interaction=nonstopmode

.PHONY: help deps test all latex site serve build format clean

help:
	@printf "%s\n" \
		"Usage: make [target]" \
		"" \
		"Targets:" \
		"  all      Compile LaTeX PDFs, run tests, and build website" \
		"  deps     Install dependencies" \
		"  test     Run tests" \
		"  latex    Compile LaTeX documents" \
		"  site     Build website" \
		"  serve    Run dev server" \
		"  build    Build website and compile LaTeX PDFs" \
		"  format   Format Python code with black" \
		"  clean    Clean build artifacts and cache files"

deps:
	python -m pip install -e ".[dev]" -e ./zensical-academic

test:
	python -m pytest

src/generated_academic.tex: zensical.toml
	python -m zensical_academic latex $< $@

latex: src/generated_academic.tex
	mkdir -p docs/assets/pdfs
	$(LATEX) src/cv.tex
	$(LATEX) src/certificates.tex
	cp src/cv.pdf src/certificates.pdf docs/assets/pdfs/

site:
	python -m zensical build

serve:
	python -m zensical serve

all: latex test site

build: all

format:
	python -m black .

clean:
	$(LATEX) -C src/cv.tex src/certificates.tex
	rm -rf src/.build
	rm -f docs/assets/pdfs/*
	rm -rf site
	rm -f src/generated_academic.tex
	rm -f src/*.aux src/*.log src/*.out src/*.synctex.gz src/*.toc src/*.fls src/*.fdb_latexmk src/*.pdf
	rm -rf .cache
	rm -rf dist build ./*.egg-info zensical-academic/*.egg-info
