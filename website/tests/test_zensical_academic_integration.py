from pathlib import Path
import jinja2
import yaml
import pytest
import macros

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
    def __init__(self, template="opensource.html", url="", title="", content="", meta=None):
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

    plugins = config["project"].get("plugins", {})
    assert "zensical_academic" in plugins
    plugin_path = (website_dir / plugins["zensical_academic"]["path"]).resolve()
    assert plugin_path.is_dir()


def test_zensical_toml_researcher_metadata(config):
    extra = config["project"]["extra"]
    assert "researcher" in extra
    researcher = extra["researcher"]

    required_fields = [
        "name",
        "role",
        "shortbio",
        "photo",
        "interests",
        "applications",
        "experience",
        "education",
        "accomplishments",
    ]
    for field in required_fields:
        assert field in researcher, f"Missing required researcher field: {field}"

    assert isinstance(researcher["interests"], list)
    assert isinstance(researcher["applications"], list)
    assert isinstance(researcher["experience"], list)
    assert isinstance(researcher["education"], list)
    assert isinstance(researcher["accomplishments"], list)

    for xp in researcher["experience"]:
        assert "role" in xp
        assert "place" in xp
        assert "period" in xp

    for edu in researcher["education"]:
        assert "course" in edu
        assert "institution" in edu
        assert "period" in edu

    for acc in researcher["accomplishments"]:
        assert "title" in acc
        assert "organization" in acc
        assert "year" in acc

    assert "social" in extra
    assert isinstance(extra["social"], list)
    for s in extra["social"]:
        assert "title" in s
        assert "link" in s
        assert "icon" in s


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


def test_macros_populates_metadata_for_academic_template(website_dir):
    class DummyEnv:
        def __init__(self):
            self.variables = {}

    env = DummyEnv()
    macros.define_env(env)

    meta, _ = parse_frontmatter(website_dir, "docs/opensource.md")
    page = DummyPage(template="opensource.html", meta=meta)

    macros.define_env(env)
    assert "github_total_repos" in env.variables
    assert "github_total_stars" in env.variables
    assert "github_total_forks" in env.variables


def test_home_template_renders_website_researcher_config(config, jinja_env, website_dir):
    template = jinja_env.get_template("home.html")
    meta, body = parse_frontmatter(website_dir, "docs/index.md")
    context = {
        "config": config["project"],
        "page": DummyPage(url="index.html", title=meta.get("title", ""), content=body, meta=meta),
    }
    output = template.render(context)
    researcher = config["project"]["extra"]["researcher"]
    assert researcher["name"] in output
    assert researcher["role"] in output
    assert "Interests" in output
    assert "Applications" in output


def test_cv_template_renders_website_researcher_config(config, jinja_env, website_dir):
    template = jinja_env.get_template("cv.html")
    meta, body = parse_frontmatter(website_dir, "docs/cv.md")
    context = {
        "config": config["project"],
        "page": DummyPage(url="cv/index.html", title=meta.get("title", ""), content=body, meta=meta),
    }
    output = template.render(context)
    assert "University of Reading" in output
    assert "PUC-Rio" in output
    assert "cv.pdf" in output
    assert "certificates.pdf" in output
