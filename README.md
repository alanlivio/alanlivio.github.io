# researcher website-cv

Reseacher website using [Hugo](https://gohugo.io/documentation/) and [HugoBlox Academic Group Theme](https://github.com/HugoBlox/theme-research-group) for `github-pages` and using [moderncv-latex](https://github.com/moderncv/moderncv) for `cv.pdf`.

## Dependencies

The project requires `hugo` and `texlive-extra`, which contains moderncv.

On Ubuntu, you can install as below.

  ```bash
  sudo snap install hugo
  sudo snap install --classic node
  sudo apt-get install texlive-latex-extra texlive-fonts-extra
  ```

On Windows, it is better use [WSL](https://learn.microsoft.com/en-us/windows/wsl/): (1) run the VSCode action `"WSL: Open Folder in WSL"` and install the depedencies; (2) open the `.devcontainer.json` file and run the suggested action `Reopen in Container`.

## serve locally

  ```bash
  cp latex/cv.pdf latex/certificates.pdf static/files/
  sh scripts/update_publication.sh # run once
  hugo server
  ```

## deploy to gh-pages

The deploy is done by a GitHub action when push.
