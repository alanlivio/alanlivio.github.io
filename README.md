# Reseacher website

Researcher website using centralized markdown for both github pages using [docusaurus](https://docusaurus.io/) and cv pdf using [moderncv-latex](https://github.com/moderncv/moderncv).

### requirements

The system requirements are the nodejs and texlive.

On ubuntu, use [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) to installl node, and apt to install latemk, moderncv.cls, and fonts:

  ```bash
  nvm install node
  sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra 
  ```

On windows, you can do the following. But you need install Perl if not runing from GitBash (which already has it):

  ```bash
  winget install OpenJS.NodeJS ChristianSchenk.MiKTeX
  winget install StrawberryPerl.StrawberryPerl # optional
  ```

Then install npm requirements:

```bash
  npm install
```

### serve locally

  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm serve
  ```

### deploy to gh-pages

  ```bash
  latexmk -pdf latex/cv.tex -cd -output-directory="../static"
  npm run deploy
  ```
