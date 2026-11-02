MAKEFLAGS += -s --no-print-directory
.DEFAULT_GOAL := help
$(if $(filter Windows_NT,$(OS)),$(if $(shell where printf 2>nul),,$(error coreutils is not installed. Please run: winget install coreutils)))

LATEX := latexmk -cd -pdflua -interaction=nonstopmode

.PHONY: help deps test latex site serve format clean

help:
	@printf "%s\n" \
		"Usage: make [target]" \
		"" \
		"Targets:" \
		"  deps     Install dependencies" \
		"  test     Run tests" \
		"  latex    Compile LaTeX documents" \
		"  site     Build website (compiles LaTeX PDFs first)" \
		"  serve    Run dev server" \
		"  format   Format Python code with black and LaTeX with latexindent" \
		"  clean    Clean build artifacts and cache files"

deps:
	python -m pip install -e ".[dev]" -e ./zensical-academic

test:
	python -m pytest

cv/generated_academic.tex: zensical.toml
	python -m zensical_academic latex $< $@

latex: cv/generated_academic.tex
	$(LATEX) cv/cv.tex
	cp cv/cv.pdf docs/assets/pdfs/

site: latex
	python -m zensical build

serve:
	python -m zensical serve

format:
	latexindent -w -s -m -c=/tmp/ -y="defaultIndent: '  '" cv/cv.tex
	python -m black -q .

clean:
	$(LATEX) -C cv/cv.tex
	rm -rf cv/.build
	rm -f docs/assets/pdfs/*
	rm -rf site
	rm -f cv/generated_academic.tex
	rm -f cv/*.aux cv/*.log cv/*.out cv/*.synctex.gz cv/*.toc cv/*.fls cv/*.fdb_latexmk cv/*.pdf
	rm -rf .cache
	rm -rf dist build ./*.egg-info zensical-academic/*.egg-info
