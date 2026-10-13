# zensical-academic

Reusable page templates and theme components for academic and researcher CV websites using the [Zensical](https://zensical.org/) static site generator.

## Overview

`zensical-academic` provides structured, clean page templates and macros for academic profiles:

- **Home Page** (`home.html`): Profile hero with biographical summary, photo, social links, research interests, and applications.
- **Curriculum Vitae** (`cv.html`): Structured timeline entries for academic appointments, education, accomplishments, and CV downloads.
- **Projects Showcase** (`projects.html`): Filterable card grid for PhD, MSc, and undergraduate projects.
- **Open Source Repositories** (`opensource.html`): Grid view for highlighted repositories with live GitHub stars and forks counters.
- **Partials**: Reusable card layout macros (`partials/render_cards.html`, `partials/render_github_stars_forks.html`).

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

## Testing

Run tests with pytest:

```bash
pytest zensical-academic/tests
```
