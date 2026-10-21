# zensical-academic

Reusable page templates and theme components for academic and researcher CV websites using the [Zensical](https://zensical.org/) static site generator.

## Overview

`zensical-academic` provides structured, clean page templates and layout components for academic profiles:

- **Home Page** (`home.html`): Profile hero with biographical summary, photo, social links, research interests, and applications.
- **Curriculum Vitae** (`cv.html`): Structured timeline entries for academic appointments, education, accomplishments, and CV downloads.
- **Projects Showcase** (`projects.html`): Filterable card grid for PhD, MSc, and undergraduate projects.
- **Open Source Repositories** (`opensource.html`): Grid view for highlighted repositories with live GitHub stars and forks counters.
- **Partials**: Reusable card layout components (`partials/render_cards.html`, `partials/render_github_stars_forks.html`).

## Usage

### Local Subfolder Plugin Mode

In your `zensical.toml`, configure the custom theme directory to point to this directory:

```toml
[project.theme]
name = "material"
custom_dir = "../zensical-academic/zensical_academic"
```

### Python Package Installation

Install via pip in editable mode or as a package:

```bash
pip install -e ./zensical-academic
```

And in `zensical.toml`:

```toml
[project.theme]
name = "academic"
```

## LaTeX CV Integration

`zensical-academic` provides a CLI command and module to generate LaTeX academic macros directly from `zensical.toml`:

```bash
zensical-academic latex [path/to/zensical.toml] [path/to/output.tex]
```

Or via Python:

```bash
python -m zensical_academic latex
```

In your project `Makefile`, you can define:

```makefile
latex/generated_academic.tex: zensical.toml
	python -m zensical_academic latex $< $@
```

## Testing

Run tests with pytest:

```bash
pytest zensical-academic/tests
```
