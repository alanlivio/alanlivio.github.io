# Script: update content/publication using hugo academic cli
# Author: Alan Guedes <alanlivio@outlook.com>

# install hugo academic cli
if ! type academic; then
    pip3 install -U academic
fi
# fetch bib from dbpl
test -f /tmp/alan_publication.bib && rm -r /tmp/alan_publication.bib
curl "https://dblp.org/pid/141/9540.bib?param=1" -o /tmp/alan_publication.bib
# import to content/publication
test -d content/publication && rm -r content/publication
academic import --bibtex /tmp/alan_publication.bib --publication-dir content/publications --overwrite