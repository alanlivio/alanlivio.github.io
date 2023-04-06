# Reseacher website

Researcher website using centralized markdown for: 1) both `github-pages` using [docusaurus](https://docusaurus.io/) and 2) `cv.pdf` using [moderncv-latex](https://github.com/moderncv/moderncv).

### requirements

The system requirements are the nodejs and texlive.

On ubuntu, use [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) to installl node, and apt to install latex packages.

  ```bash
  nvm install node
  sudo apt-get install texlive texlive-latex-extra texlive-fonts-extra 
  ```

On windows, you can use [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) to install node and latex packages. You may also need install Perl if running from powershell (GitBash already has it).

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
