import re
from pathlib import Path
import yaml
import pytest
import zensical_academic

try:
    import tomllib
except ImportError:
    import tomli as tomllib


@pytest.fixture(scope="module")
def pkg_dir():
    return Path(zensical_academic.__file__).resolve().parent


@pytest.fixture(scope="module")
def root_dir(pkg_dir):
    return pkg_dir.parent


def test_version_defined():
    assert hasattr(zensical_academic, "__version__")
    assert isinstance(zensical_academic.__version__, str)
    assert re.match(r"^\d+\.\d+\.\d+", zensical_academic.__version__) is not None


def test_package_directory_exists(pkg_dir):
    assert pkg_dir.is_dir()


def test_templates_exist(pkg_dir):
    expected_files = [
        "mkdocs_theme.yml",
        "css/academic.css",
        "js/academic.js",
        "home.html",
        "cv.html",
        "opensource.html",
        "projects.html",
        "partials/render_cards.html",
        "partials/render_github_stars_forks.html",
    ]
    for rel_path in expected_files:
        file_path = pkg_dir / rel_path
        assert file_path.is_file(), f"Missing template file: {rel_path}"


def test_mkdocs_theme_config(pkg_dir):
    theme_config_path = pkg_dir / "mkdocs_theme.yml"
    with open(theme_config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data.get("extends") == "material"
    assert "css/academic.css" in data.get("extra_css", [])
    assert "js/academic.js" in data.get("extra_javascript", [])


def test_pyproject_toml_configuration(root_dir):
    pyproject_path = root_dir / "pyproject.toml"
    assert pyproject_path.is_file()
    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    assert config["project"]["name"] == "zensical-academic"
    theme_entry = config["project"]["entry-points"]["mkdocs.themes"]
    assert "academic" in theme_entry
    assert theme_entry["academic"] == "zensical_academic"
    assert "zensical-academic" in theme_entry
    assert theme_entry["zensical-academic"] == "zensical_academic"
    assert (
        config["project"]["scripts"]["zensical-academic"] == "zensical_academic.cli:cli"
    )
    pkg_data = config["tool"]["setuptools"]["package-data"]["zensical_academic"]
    assert "css/*.css" in pkg_data
    assert "js/*.js" in pkg_data


def test_generate_academic_tex(tmp_path):
    from zensical_academic.cli import generate_academic_tex

    sample_toml = tmp_path / "zensical.toml"
    sample_toml.write_text(
        """
[project.extra.academic]
name = "Jane Doe"
email = "jane@example.com"
homepage = "jane.example.com"

[[project.extra.academic.education]]
period = "2020-2024"
course = "BSc Computer Science"
institution_full = "Example University"
""",
        encoding="utf-8",
    )
    out_file = tmp_path / "generated.tex"
    output = generate_academic_tex(sample_toml, out_file)
    assert "\\name{Jane}{Doe}" in output
    assert "\\email{jane@example.com}" in output
    assert "\\homepage{jane.example.com}" in output
    assert (
        "\\cventry{2020--2024}{BSc Computer Science}{Example University}{}{}{}"
        in output
    )
    assert out_file.read_text(encoding="utf-8") == output


def test_generate_academic_tex_with_socials(tmp_path):
    from zensical_academic.cli import generate_academic_tex

    sample_toml = tmp_path / "zensical.toml"
    sample_toml.write_text(
        """
[project.extra.academic]
name = "Jane Doe"

[[project.extra.social]]
title = "github"
link = "https://github.com/janedoe"

[[project.extra.social]]
title = "scholar"
link = "https://scholar.google.com/citations?user=123"
""",
        encoding="utf-8",
    )
    out_file = tmp_path / "generated.tex"
    output = generate_academic_tex(sample_toml, out_file)
    assert (
        r"\collectionadd[github]{socials}{\protect\httpslink[github]{github.com/janedoe}}"
        in output
    )
    assert (
        r"\collectionadd[googlescholar]{socials}{\protect\httpslink[scholar]{scholar.google.com/citations?user=123}}"
        in output
    )


def test_cli_latex_command(tmp_path):
    from zensical_academic.cli import cli

    toml_file = tmp_path / "zensical.toml"
    toml_file.write_text(
        """
[project.extra.academic]
name = "Jane Doe"
email = "jane@example.com"
""",
        encoding="utf-8",
    )
    out_file = tmp_path / "out" / "generated.tex"
    ret = cli(["latex", str(toml_file), str(out_file)])
    assert ret == 0
    assert out_file.is_file()
    content = out_file.read_text(encoding="utf-8")
    assert "\\name{Jane}{Doe}" in content
    assert "\\email{jane@example.com}" in content


def test_cli_default_command(tmp_path, monkeypatch):
    from zensical_academic.cli import cli, main

    assert main is cli
    monkeypatch.chdir(tmp_path)
    toml_file = tmp_path / "zensical.toml"
    toml_file.write_text(
        """
[project.extra.academic]
name = "Alan Turing"
""",
        encoding="utf-8",
    )
    ret = cli([])
    assert ret == 0
    expected_out = tmp_path / "latex" / "generated_academic.tex"
    assert expected_out.is_file()
    assert "\\name{Alan}{Turing}" in expected_out.read_text(encoding="utf-8")
