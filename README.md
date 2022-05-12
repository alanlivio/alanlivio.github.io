# cv-site

Personal researcher website which uses [mkdocs](https://github.com/mkdocs/mkdocs) to generate static HTML and [moderncv latex class](https://github.com/moderncv/moderncv) for pdfs, both integrated through the `build.py` script using centralized data from `mkdocs.yaml`. 

### deps
To install moderncv on ubuntu, run: 
  ```bash
  sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra
  ```
while on windows, run:
  ```bash
  winget install ChristianSchenk.MiKTeX
  ```
To install mkdcos, run:
  ```bash
  pip install -r requirements.txt
  ```
  
### build

To build latex pdf to mkdocs/ folder, run:
  ```bash
  python build_latex.py
  ```

To test locally, run: 
  ```bash
  mkdocs serve
  ```

### deploy

To deploy into github pages, run: 
  ```bash
  mkdocs gh-deploy --force
  ```