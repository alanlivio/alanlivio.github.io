# researcher website-cv

Researcher website using [Hugo](https://gohugo.io/documentation/) and [MkDocs Material](https://github.com/mkdocs/mkdocs) for `github-pages` and using [moderncv-latex](https://github.com/moderncv/moderncv) for `cv.pdf`.

### deps

To install moderncv on ubuntu, run:

```bash
sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra
```

while on windows, run:

```bash
winget install Python ChristianSchenk.MiKTeX StrawberryPerl.StrawberryPerl
```

### build

To build latex and run locally, run:

```bash
pip install -r requirements.txt
python build_tex_partials_from_mkdocs_yml.py
latexmk -pdflua latex/cv.tex -cd -output-directory="../mkdocs"
latexmk -pdflua latex/certificates -cd -output-directory="../mkdocs"
mkdocs serve
```

To deploy to github pages, run:

```bash
mkdocs gh-deploy --force
```
