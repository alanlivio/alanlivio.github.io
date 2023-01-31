# Reseacher website

Researcher website using centralized data for both github pages (using [docusaurus](https://docusaurus.io/) and cv pdf using [moderncv-latex](https://github.com/moderncv/moderncv).

### requeriments

on ubuntu:

  ```bash
  sudo apt-get install npm texlive texlive-latex-extra texlive-fonts-extra
  ```

on windows:

  ```bash
  winget install ChristianSchenk.MiKTeX OpenJS.NodeJS
  ```

The latexmk requires Perl, so if are you not runing from GitBash (which already has perl) you can install it by:

  ```bash
  winget install StrawberryPerl.StrawberryPerl
  ```

### build locally

  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm start
  ```

### deploy to gh-pages

  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm run deploy
  ```
