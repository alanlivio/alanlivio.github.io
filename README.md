# Reseacher website

Researcher website using centralized data for both static HTML and a [moderncv-latex](https://github.com/moderncv/moderncv) pdf.

### deps

on ubuntu:

  ```bash
  sudo apt-get install npm texlive texlive-latex-extra texlive-fonts-extra
  ```

on windows:

  ```bash
  winget install ChristianSchenk.MiKTeX OpenJS.NodeJS
  ```
The latexmk requires Perl, so if are you not runing from GitBash (already has perl) you can install it by:

  ```bash
  winget install  StrawberryPerl.StrawberryPerl
  ```

### build locally

  ```bash
  latexmk -shell-escape -cd -pdf ./latex/cv.tex
  cp latex/cv.pdf static/
  npm start
  ```

### deploy to gh-pages

  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm run deploy
  ```
