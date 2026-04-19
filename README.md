# researcher website-cv

Researcher website using [Hugo](https://gohugo.io/) with the [Hextra](https://github.com/imfing/hextra) theme, and [moderncv-latex](https://github.com/moderncv/moderncv) for `cv.pdf`.

### deps

To install dependencies on ubuntu, run:

```bash
sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra hugo
```

while on windows, run:

```bash
winget install Hugo.Hugo.Extended ChristianSchenk.MiKTeX StrawberryPerl.StrawberryPerl
```

### build

To build latex and run locally, run:

```bash
latexmk -pdflua latex/cv.tex -cd -output-directory="../static"
latexmk -pdflua latex/certificates -cd -output-directory="../static"
hugo server
```

To deploy to github pages, run:

```bash
hugo
```

GitHub Pages publishing is handled by [ci.yml](.github/workflows/ci.yml).
