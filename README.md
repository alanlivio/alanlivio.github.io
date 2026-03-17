# researcher website-cv

Researcher website using [Zensical](https://github.com/zensical/zensical), a  static webside generator, and [moderncv-latex](https://github.com/moderncv/moderncv) for `cv.pdf`.

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
latexmk -pdflua latex/cv.tex -cd -output-directory="../mkdocs"
latexmk -pdflua latex/certificates -cd -output-directory="../mkdocs"
zensical serve
```

To deploy to github pages, run:

```bash
zensical build
```

GitHub Pages publishing is handled by [ci.yml](.github/workflows/ci.yml).
