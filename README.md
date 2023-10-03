# researcher website-cv

Template website for researchers using centralized markdown to generate both a `github-pages` using [hugo](https://gohugo.io/documentation/) and `cv.pdf` using [moderncv-latex](https://github.com/moderncv/moderncv).

## requirements

The project requires `hugo` and `texlive`.

On Ubuntu, you can install them by apt. To get the latest node version, setup first the [nodesource distribution](https://github.com/nodesource/distributions).

  ```bash
  sudo apt-get install texlive-latex-extra texlive-fonts-extra
  sudo snap install hugo
  ```

On Windows, you can install them by [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/). You may also need to install Perl if running from PowerShell (GitBash already has it).

  ```bash
  winget install Hugo.Hugo ChristianSchenk.MiKTeX
  winget install StrawberryPerl.StrawberryPerl # optional
  ```

## serve locally

  ```bash
  sh scripts/update_publication.sh # run once
  hugo server
  ```

## deploy to gh-pages

The deploy is done by a GitHub action when push.
