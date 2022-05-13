# cv-site

Researcher website which uses [mkdocs](https://github.com/mkdocs/mkdocs) to generate static HTML and [moderncv latex class](https://github.com/moderncv/moderncv) latex pdf using centralized data from mkdocs.yaml.

### latex deps
To install moderncv on ubuntu, run: 
  ```bash
  sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra
  ```
while on windows, run:
  ```bash
  winget install ChristianSchenk.MiKTeX
  ```
  
### build

To build latex and run locally, run:
  ```bash
  pip install -r requirements.txt
  python build_tex_partials_from_mkdocs_yml.py
  latexmk -pdf latex/cv.tex -cd -output-directory="../mkdocs"
  mkdocs serve
  ```

To deploy to github pages, run: 
  ```bash
  mkdocs gh-deploy --force
  ```
