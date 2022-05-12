#!/bin/env python
import os
from jinja2 import FileSystemLoader
from latex import jinja2
import yaml


def build_tex_partials_from_mkdocs_yml():
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


if __name__ == '__main__':
    build_tex_partials_from_mkdocs_yml()
