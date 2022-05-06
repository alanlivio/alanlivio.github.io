#!/bin/env python
import os
import sys
from jinja2 import FileSystemLoader
from latex import jinja2, build_pdf
from mkdocs.__main__ import build_command
import yaml
import argparse


def build_latex():
    # load reseacher data from mkdcos.yml
    with open('mkdocs.yml', 'r') as file:
        # ignore mkdocs.yml related emoji using !
        yaml.add_multi_constructor(
            'tag:', lambda loader, suffix, node: None, Loader=yaml.SafeLoader)
        data = yaml.safe_load(file)
        reseacher = data['extra']['reseacher']

    # fill .jinja2.tex files with mkdcos.yml:researcher data and build cv.pdf
    # https://pythonhosted.org/latex/
    latex_dir = os.path.abspath(os.path.dirname(__file__) + "/latex")
    env = jinja2.make_env(loader=FileSystemLoader(latex_dir))
    shortbio = env.get_template('partials/shortbio.tex.jinja').render(**reseacher)
    with open("latex/partials/shortbio.tex", "w") as file:
        file.write(shortbio)
    cv = build_pdf(open('latex/cv.tex'), texinputs=[latex_dir])
    cv.save_to('mkdocs/cv.pdf')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--latex', help='build latex cv', action="store_true")
    group.add_argument('--mkdocs', help='build mkdocs site', action="store_true")
    args = parser.parse_args()
    if args.latex:
        build_latex()
    elif args.mkdocs:
        build_command({})
