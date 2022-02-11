import os
import sys
from jinja2 import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf
from mkdocs.__main__ import cli
import yaml


def build_latex():
    # load reseacher data from mkdcos.yml
    with open('mkdocs.yml', 'r') as file:
        data = yaml.full_load(file)
        reseacher = data['extra']['reseacher']

    # fill latex with data using latex.jinja2 pkg
    latex_dir = os.path.abspath(os.path.dirname(__file__) + "/latex")
    env = make_env(loader=FileSystemLoader(latex_dir))
    tpl = env.get_template('cv.tex')
    latex_cv = tpl.render(**reseacher)
    pdf = build_pdf(latex_cv, texinputs=[latex_dir])

    # save
    pdf.save_to('src/cv.pdf')


def build_mkdocs():
    sys.argv.append("build")
    cli()


if __name__ == '__main__':
    build_latex()
    build_mkdocs()
