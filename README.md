# researcher-cv-website

This is the personal website of [Alan Guedes](https://github.com/alanlivio) hosted at [https://alanlivio.github.io](https://alanlivio.github.io). It is built using [Zensical](https://zensical.org/) and [moderncv-latex](https://github.com/moderncv/moderncv).

This is also a GitHub template useful easy replicate ([click here](https://github.com/new?template_name=alanlivio.github.io)).

## Structure

- `latex/` — LaTeX source
- `web/` — static webpage using Zensical

## Usage

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

The deploy to GitHub Pages is handled by [deploy.yml](.github/workflows/deploy.yml).
