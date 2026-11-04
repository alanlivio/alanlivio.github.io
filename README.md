# researcher-cv-website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is the personal website of [Alan Guedes](https://github.com/alanlivio) hosted at [https://alanlivio.github.io](https://alanlivio.github.io). It is built using [Zensical](https://zensical.org/) and [moderncv-latex](https://github.com/moderncv/moderncv), with Markdown pages under `docs/` and a reusable theme under `zensical-academic/` (which will be shared as a `pip` package in the future).

This is also a GitHub template useful easy replicate ([click here](https://github.com/new?template_name=alanlivio.github.io)).

## Usage

The zensical_academic creates a cv.pdf using `moderncv` distributed with TeX Live; install it on Linux (`sudo apt-get install -y latexmk texlive-latex-extra texlive-fonts-extra texlive-luatex`) or Windows (`winget install MiKTeX`).

Run `make help` to see all available commands and `make serve` to run locally.

The deploy to GitHub Pages is handled by [deploy.yml](.github/workflows/deploy.yml).
