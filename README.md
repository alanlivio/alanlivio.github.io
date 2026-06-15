# researcher-cv-website

This [Alan Guedes](https://github.com/alanlivio) website hosted at [https://alanlivio.github.io](https://alanlivio.github.io).

It is also a github template useful to create a research website which include CV, research projects and blog. It using [https://zensical.org/](https://zensical.org/) and [moderncv-latex](https://github.com/moderncv/moderncv).

## setup

```bash
make setup-latex
make setup-pip
```

## run

To run website locally, do:

```bash
make cv
make serve
```

## deploy

GitHub Pages publishing is handled by [ci.yml](.github/workflows/ci.yml).
