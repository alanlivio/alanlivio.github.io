# Reseacher website

Researcher website using centralized data for both static HTML and a [moderncv-latex](https://github.com/moderncv/moderncv) pdf.

### deps

on ubuntu, run: 
  ```bash
  sudo apt-get install npm texlive texlive-latex-extra texlive-fonts-extra
  ```
  
on windows, run:
  ```bash
  winget install ChristianSchenk.MiKTeX OpenJS.NodeJS
  ```
  
### build locally 

Run:
  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm start
  ```

### deploy to gh-pages 

Run:
  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm run deploy
  ```
