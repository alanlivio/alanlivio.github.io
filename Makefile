MAKEFLAGS += -s --no-print-directory
.DEFAULT_GOAL := help
$(if $(filter Windows_NT,$(OS)),$(if $(shell where printf 2>nul),,$(error coreutils is not installed. Please run: winget install coreutils)))

.PHONY: help deps test site serve format clean

help:
	@printf "%s\n" \
		"Usage: make [target]" \
		"" \
		"Targets:" \
		"  deps     Install dependencies" \
		"  test     Run tests" \
		"  site     Build website (compiles LaTeX CV PDF first)" \
		"  serve    Run dev server" \
		"  format   Format Python code with black" \
		"  clean    Clean build artifacts and cache files"

deps:
	python -m pip install -e ".[dev]" -e ./zensical-academic
	python -c "import shutil, sys; shutil.which('latexmk') or sys.exit('TeX Live is not installed. Please install TeX Live.')"

test:
	python -m pytest

docs/assets/pdfs/cv.pdf: zensical.toml
	python -m zensical_academic cv.pdf

site: docs/assets/pdfs/cv.pdf
	python -m zensical build

serve: docs/assets/pdfs/cv.pdf
	python -m zensical serve

format:
	python -m black -q .

clean:
	rm -f docs/assets/pdfs/*
	rm -rf site
	rm -rf .cache
	rm -rf dist build ./*.egg-info zensical-academic/*.egg-info
