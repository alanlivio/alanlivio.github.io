# Script: update content/publication using hugo academic cli
# Author: Alan L. V. Guedes <alanlivio@outlook.com>

# install hugo academic cli
if ! type academic; then
    pip3 install -U academic==0.11.2
fi
# fetch bib from dbpl
test -f /tmp/alan_publications.bib && rm -r /tmp/alan_publications.bib
curl "https://dblp.org/pid/141/9540.bib?param=1" -o /tmp/alan_publications.bib
# import to content/publication
test -d content/publications && rm -r content/publications
academic import --bibtex /tmp/alan_publications.bib --publication-dir content/publications --overwrite

