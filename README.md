# researcher-cv-website

This is the personal website of [Alan Guedes](https://github.com/alanlivio) hosted at [https://alanlivio.github.io](https://alanlivio.github.io).

It is also a GitHub template useful for creating a research website that includes a CV, research projects, and a blog. It is built using [Zensical](https://zensical.org/) and [moderncv-latex](https://github.com/moderncv/moderncv).

## Run Locally

To see all available commands, run:

```bash
make help
```

Output:

```text
pip          Install python dependencies
latex        Build PDF from LaTeX
clean        Clean build artifacts and cache files
web          Build website
serve        Run dev server
```

For local development:

```bash
make serve
```

## Deploy

GitHub Pages publishing is handled by [deploy.yml](.github/workflows/deploy.yml).
