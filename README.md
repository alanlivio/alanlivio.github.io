# researcher website-cv

Template website for researchers using centralized markdown to generate both a `github-pages` using [hugo](https://gohugo.io/documentation/) and `cv.pdf` using [moderncv-latex](https://github.com/moderncv/moderncv).

## requirements

The project requires `hugo` and `texlive-extra`, which contains moderncv.

On Ubuntu, you can install as below.

  ```bash
  sudo apt-get install texlive-latex-extra texlive-fonts-extra
  sudo snap install hugo
  sudo snap install --classic node
  ```

On Windows, you can install them by [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) as below.

  ```bash
  winget install Hugo.Hugo ChristianSchenk.MiKTeX
  winget install StrawberryPerl.StrawberryPerl # optional,required only if you runing from gitbatsh
  ```

## serve locally

  ```bash
  cp latex/cv.pdf latex/certificates.pdf static/files/
  sh scripts/update_publication.sh # run once
  hugo server
  ```

## deploy to gh-pages

The deploy is done by a GitHub action when push.
