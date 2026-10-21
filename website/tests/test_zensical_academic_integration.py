from pathlib import Path
import jinja2
import yaml
import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class MockTemplateLoader(jinja2.BaseLoader):
    def __init__(self, template_dir):
        self.template_dir = Path(template_dir)
        self.fs_loader = jinja2.FileSystemLoader(str(self.template_dir))

    def get_source(self, environment, template):
        if template == "main.html":
            return "{% block content %}{% endblock %}", "main.html", lambda: True
        if template.startswith(".icons/"):
            return '<svg class="mock-icon"></svg>', template, lambda: True
        return self.fs_loader.get_source(environment, template)


class DummyPage:
    def __init__(
        self, template="opensource.html", url="", title="", content="", meta=None
    ):
        self.url = url
        self.title = title
        self.content = content
        self.meta = meta if meta is not None else {"template": template}


@pytest.fixture(scope="module")
def website_dir():
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def config(website_dir):
    config_path = website_dir / "zensical.toml"
    with open(config_path, "rb") as f:
        return tomllib.load(f)


@pytest.fixture(scope="module")
def theme_dir(website_dir, config):
    theme_custom_dir = config["project"]["theme"]["custom_dir"]
    return (website_dir / theme_custom_dir).resolve()


@pytest.fixture(scope="module")
def jinja_env(theme_dir):
    env = jinja2.Environment(
        loader=MockTemplateLoader(theme_dir),
        autoescape=False,
    )
    env.filters["url"] = lambda x: x
    env.globals["page"] = DummyPage()
    return env


def parse_frontmatter(website_dir, doc_rel_path):
    doc_path = website_dir / doc_rel_path
    assert doc_path.is_file()
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    parts = content.split("---", 2)
    assert len(parts) >= 3, f"Missing YAML frontmatter in {doc_rel_path}"
    meta = yaml.safe_load(parts[1])
    body = parts[2]
    return meta, body


def test_zensical_toml_points_to_zensical_academic(config, theme_dir, website_dir):
    assert theme_dir.is_dir()
    required_templates = [
        "home.html",
        "cv.html",
        "opensource.html",
        "projects.html",
        "partials/render_cards.html",
        "partials/render_github_stars_forks.html",
    ]
    for template_name in required_templates:
        template_path = theme_dir / template_name
        assert template_path.is_file(), f"Missing template: {template_name}"

    assert (theme_dir / "js" / "academic.js").is_file()

    markdown_extensions = config["project"].get("markdown_extensions", {})
    assert "zensical.extensions.macros" not in markdown_extensions

    plugins = config["project"].get("plugins", {})
    assert "zensical_academic" in plugins
    plugin_path = (website_dir / plugins["zensical_academic"]["path"]).resolve()
    assert plugin_path.is_dir()


def test_zensical_toml_academic_metadata(config, website_dir):
    extra = config["project"]["extra"]
    assert "academic" in extra
    academic = extra["academic"]

    required_fields = [
        "name",
        "role",
        "email",
        "homepage",
        "cv_file",
        "shortbio",
        "photo",
        "interests",
        "applications",
        "experience",
        "education",
        "accomplishments",
    ]
    for field in required_fields:
        assert field in academic, f"Missing required academic field: {field}"

    photo_path = website_dir / "docs" / academic["photo"]
    assert photo_path.is_file(), f"Missing academic photo asset: {photo_path}"
    assert academic["cv_file"] == "cv.pdf"

    assert isinstance(academic["interests"], list)
    assert isinstance(academic["applications"], list)
    assert isinstance(academic["experience"], list)
    assert isinstance(academic["education"], list)
    assert isinstance(academic["accomplishments"], list)

    for xp in academic["experience"]:
        assert "role" in xp
        assert "place" in xp
        assert "period" in xp

    for edu in academic["education"]:
        assert "course" in edu
        assert "institution" in edu
        assert "institution_full" in edu
        assert "period" in edu
        if "MSc" in edu["course"]:
            assert edu["institution"] == "UFPB"

    for acc in academic["accomplishments"]:
        assert "title" in acc
        assert "organization" in acc
        assert "year" in acc

    assert "social" in extra
    assert isinstance(extra["social"], list)
    for s in extra["social"]:
        assert "title" in s
        assert "link" in s
        assert "icon" in s


def test_opensource_languages_have_color_mappings(website_dir, theme_dir):
    meta, _ = parse_frontmatter(website_dir, "docs/opensource.md")
    template_content = (theme_dir / "opensource.html").read_text(encoding="utf-8")
    for section in meta.get("sections", []):
        for repo in section.get("repositories", []):
            lang = repo.get("lang")
            assert lang, f"Missing lang for repo {repo.get('name')}"
            assert (
                f'"{lang}"' in template_content
            ), f"Language '{lang}' missing from lang_colors in opensource.html"


def test_latex_cv_shares_zensical_toml(website_dir, config):
    repo_root = website_dir.parent
    shared_tex = (repo_root / "latex" / "shared.tex").read_text(encoding="utf-8")
    cv_tex = (repo_root / "latex" / "cv.tex").read_text(encoding="utf-8")
    generated_file = repo_root / "latex" / "generated_academic.tex"
    if not generated_file.exists():
        from zensical_academic.cli import generate_academic_tex

        generate_academic_tex(website_dir / "zensical.toml", generated_file)
    generated_tex = generated_file.read_text(encoding="utf-8")
    assert "../website/zensical.toml" in shared_tex
    assert "\\input{generated_academic.tex}" in shared_tex
    assert "\\renderEducation" in cv_tex
    assert "luacode" not in shared_tex
    academic = config["project"]["extra"]["academic"]
    assert academic["email"] in generated_tex


def test_docs_home_uses_academic_template(website_dir):
    meta, body = parse_frontmatter(website_dir, "docs/index.md")
    assert meta.get("template") == "home.html"
    assert "<!-- ABOUT_ME_CONTENT -->" in body
    assert "<!-- RESEARCH_INTERESTS_CONTENT -->" in body


def test_docs_cv_uses_academic_template(website_dir):
    meta, body = parse_frontmatter(website_dir, "docs/cv.md")
    assert meta.get("template") == "cv.html"
    assert "<!-- EXPERIENCE_CONTENT -->" in body
    assert "<!-- EDUCATION_CONTENT -->" in body
    assert "<!-- HONORS_CONTENT -->" in body
    assert "<!-- DOWNLOADS_CONTENT -->" in body


def test_docs_opensource_uses_academic_template(website_dir):
    meta, body = parse_frontmatter(website_dir, "docs/opensource.md")
    assert meta.get("template") == "opensource.html"
    assert "sections" in meta
    assert len(meta["sections"]) > 0
    assert "<!-- ACADEMIC_TOOLS_GRID -->" in body
    assert "<!-- MULTIMEDIA_SYSTEMS_GRID -->" in body


def test_docs_projects_uses_academic_template(website_dir):
    meta, body = parse_frontmatter(website_dir, "docs/projects/index.md")
    assert meta.get("template") == "projects.html"
    assert "<!-- ACTIVE_PROJECTS_GRID -->" in body
    assert "<!-- AVAILABLE_PROJECTS_GRID -->" in body
    assert "<!-- UG_PROJECTS_GRID -->" in body
    assert "<!-- MSC_PROJECTS_GRID -->" in body


def test_opensource_template_renders_without_macros(config, jinja_env, website_dir):
    template = jinja_env.get_template("opensource.html")
    meta, body = parse_frontmatter(website_dir, "docs/opensource.md")
    context = {
        "config": config["project"],
        "page": DummyPage(
            url="opensource/index.html",
            title=meta.get("title", ""),
            content=body,
            meta=meta,
        ),
    }
    output = template.render(context)
    assert 'id="github-repos-count">8<' in output
    assert "academic.js" in output
    assert "data-repo=" in output


def test_home_template_renders_website_academic_config(config, jinja_env, website_dir):
    template = jinja_env.get_template("home.html")
    meta, body = parse_frontmatter(website_dir, "docs/index.md")
    context = {
        "config": config["project"],
        "page": DummyPage(
            url="index.html", title=meta.get("title", ""), content=body, meta=meta
        ),
    }
    output = template.render(context)
    academic = config["project"]["extra"]["academic"]
    assert academic["name"] in output
    assert academic["role"] in output
    assert "Interests" in output
    assert "Applications" in output


def test_cv_template_renders_website_researcher_config(config, jinja_env, website_dir):
    template = jinja_env.get_template("cv.html")
    meta, body = parse_frontmatter(website_dir, "docs/cv.md")
    context = {
        "config": config["project"],
        "page": DummyPage(
            url="cv/index.html", title=meta.get("title", ""), content=body, meta=meta
        ),
    }
    output = template.render(context)
    assert "University of Reading" in output
    assert "PUC-Rio" in output
    assert "UFPB" in output
    assert "cv.pdf" in output
    assert "certificates.pdf" in output
