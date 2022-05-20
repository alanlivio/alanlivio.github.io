# Reseacher website

Researcher website using centralized [mkdocs.yaml](https://github.com/mkdocs/mkdocs) data for both static HTML and a [moderncv-latex](https://github.com/moderncv/moderncv) pdf.

### latex deps

on ubuntu, run: 
  ```bash
  sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra
  ```
  
on windows, run:
  ```bash
  winget install ChristianSchenk.MiKTeX
  ```
  
### build

to build latex and serve locally, run:
  ```bash
  pip install -r requirements.txt
  python build_tex_partials_from_mkdocs_yml.py
  latexmk -pdf latex/cv.tex -cd -output-directory="../mkdocs"
  mkdocs serve
  ```

to deploy on GitHub pages, run: 
  ```bash
  mkdocs gh-deploy --force
  ```
