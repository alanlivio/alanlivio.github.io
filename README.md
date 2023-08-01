# researcher website-cv

Template website for researchers using centralized markdown to generate both a `github-pages` using [docusaurus](https://docusaurus.io/) and `cv.pdf` using [moderncv-latex](https://github.com/moderncv/moderncv).

## requirements

The project requires `nodejs` and `texlive`. 

On Ubuntu, you can install them by apt. To get the latest node version, setup first the [nodesource distribution](https://github.com/nodesource/distributions).

  ```bash
  sudo apt-get install nodejs texlive texlive-latex-extra texlive-fonts-extra 
  ```

On Windows, you can install them by [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/). You may also need to install Perl if running from PowerShell (GitBash already has it).

  ```bash
  winget install OpenJS.NodeJS ChristianSchenk.MiKTeX
  winget install StrawberryPerl.StrawberryPerl # optional
  ```

Then install npm requirements:

```bash
  npm install
```

## serve locally

  ```bash
  latexmk -pdf -quiet latex/cv.tex -cd -output-directory="../static"
  latexmk -pdf -quiet latex/certificates.tex -cd -output-directory="../static"
  npm serve
  ```

## deploy to gh-pages

  ```bash
  npm run deploy
  ```
