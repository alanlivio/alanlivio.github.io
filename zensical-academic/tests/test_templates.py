from pathlib import Path
import jinja2
import pytest
import zensical_academic


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
    def __init__(self, url="projects/", title="Projects", content="", meta=None):
        self.url = url
        self.title = title
        self.content = content
        self.meta = meta or {}


class DummyNav:
    def __init__(self, items):
        self.items = items


class DummyItem:
    def __init__(self, title, url, description="", image="", tags=None, children=None):
        self.title = title
        self.url = url
        self.meta = {"description": description, "image": image, "tags": tags or []}
        self.children = children or []


@pytest.fixture(scope="module")
def template_dir():
    return Path(zensical_academic.__file__).resolve().parent


@pytest.fixture(scope="module")
def env(template_dir):
    environment = jinja2.Environment(
        loader=MockTemplateLoader(template_dir),
        autoescape=False,
    )
    environment.filters["url"] = lambda x: x
    environment.globals["page"] = DummyPage()
    return environment


def test_all_templates_syntax(env, template_dir):
    for html_file in template_dir.glob("**/*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            source = f.read()
        env.parse(source)


def test_render_github_stars_forks(env):
    template = env.get_template("partials/render_github_stars_forks.html")
    render_fn = getattr(template.module, "render_github_stars_forks")

    repos = [
        {
            "name": "octocat/Hello-World",
            "title": "Hello-World",
            "description": "My first repository",
            "lang": "Python",
            "stars": 120,
            "forks": 35,
        },
        {
            "name": "octocat/Spoon-Knife",
            "title": "Spoon-Knife",
            "description": "Fork this repo",
            "lang": "HTML",
            "stars": 5,
            "forks": 2,
        },
    ]
    lang_colors = {"Python": "#3572A5", "HTML": "#e34c26"}

    output = render_fn(repos, lang_colors)
    assert "octocat/Hello-World" in output
    assert "My first repository" in output
    assert "120" in output
    assert "35" in output
    assert "#3572A5" in output
    assert "repo-stars-Hello-World" in output
    assert "repo-forks-Hello-World" in output
    assert "octocat/Spoon-Knife" in output


def test_render_github_stars_forks_empty(env):
    template = env.get_template("partials/render_github_stars_forks.html")
    render_fn = getattr(template.module, "render_github_stars_forks")
    output = render_fn([])
    assert 'class="repo-grid-new"' in output


def test_render_cards(env):
    template = env.get_template("partials/render_cards.html")
    render_fn = getattr(template.module, "render_cards")

    items = [
        DummyItem(
            title="Active PhD Project",
            url="projects/phd_active/topic-a/",
            description="Study on AI",
            image="assets/cover.png",
            tags=["Computer Vision", "Deep Learning"],
        ),
        DummyItem(
            title="Ignored Project",
            url="projects/other/topic-b/",
            description="Another topic",
        ),
        DummyItem(
            title="Category Group",
            url="",
            children=[
                DummyItem(
                    title="Nested Available PhD",
                    url="projects/phd_available/topic-c/",
                    description="Self funded opportunity",
                    image="https://example.com/ext.jpg",
                    tags=["Generative AI"],
                )
            ],
        ),
    ]

    output_active = render_fn(items, "phd_active")
    assert "Active PhD Project" in output_active
    assert "Study on AI" in output_active
    assert "project-card-tag" in output_active
    assert "Computer Vision" in output_active
    assert "Deep Learning" in output_active
    assert "Ignored Project" not in output_active
    assert "Nested Available PhD" not in output_active

    output_available = render_fn(items, "phd_available")
    assert "Nested Available PhD" in output_available
    assert "https://example.com/ext.jpg" in output_available
    assert "Generative AI" in output_available
    assert "Active PhD Project" not in output_available


def test_home_template_render(env):
    template = env.get_template("home.html")
    context = {
        "config": {
            "extra": {
                "academic": {
                    "name": "Dr. Jane Doe",
                    "role": "Senior Lecturer",
                    "shortbio": "Bio paragraph for researcher.",
                    "photo": "assets/photo.jpg",
                    "interests": ["Robotics", "NLP"],
                    "applications": ["Healthcare", "Space"],
                },
                "social": [
                    {
                        "title": "github",
                        "link": "https://github.com/janedoe",
                        "icon": "fontawesome/brands/github",
                    }
                ],
            }
        },
        "page": DummyPage(
            content="<p>Intro</p><!-- ABOUT_ME_CONTENT --><!-- RESEARCH_INTERESTS_CONTENT -->"
        ),
    }
    output = template.render(context)
    assert "Dr. Jane Doe" in output
    assert "Senior Lecturer" in output
    assert "Bio paragraph for researcher." in output
    assert "Robotics" in output
    assert "Healthcare" in output
    assert "https://github.com/janedoe" in output
    assert "<!-- ABOUT_ME_CONTENT -->" not in output
    assert "<!-- RESEARCH_INTERESTS_CONTENT -->" not in output


def test_cv_template_render(env):
    template = env.get_template("cv.html")
    context = {
        "config": {
            "extra": {
                "academic": {
                    "experience": [
                        {
                            "role": "Associate Professor",
                            "place": "Sample University",
                            "url": "https://sample.edu",
                            "location": "London",
                            "period": "2020-present",
                            "description": ["Taught courses", "Led grants"],
                        }
                    ],
                    "education": [
                        {
                            "course": "PhD in Computer Science",
                            "institution": "Tech Institute",
                            "url": "https://tech.edu",
                            "period": "2015-2019",
                        }
                    ],
                    "accomplishments": [
                        {
                            "title": "Distinguished Paper Award",
                            "organization": "ACM Conference",
                            "certificate_url": "https://acm.org/cert",
                            "year": 2021,
                        }
                    ],
                }
            }
        },
        "page": DummyPage(
            content=(
                '<h2 id="experience">Experience</h2>\n<!-- EXPERIENCE_CONTENT -->\n'
                '<h2 id="education">Education</h2>\n<!-- EDUCATION_CONTENT -->\n'
                '<h2 id="honors-awards">Honors & Awards</h2>\n<!-- HONORS_CONTENT -->\n'
                "<!-- DOWNLOADS_CONTENT -->"
            )
        ),
    }
    output = template.render(context)
    assert "Associate Professor" in output
    assert "Sample University" in output
    assert "Taught courses" in output
    assert "PhD in Computer Science" in output
    assert "Tech Institute" in output
    assert "Distinguished Paper Award" in output
    assert "ACM Conference" in output
    assert "cv.pdf" in output
    assert "certificates.pdf" in output
    assert "<!-- EXPERIENCE_CONTENT -->" not in output
    assert "<!-- EDUCATION_CONTENT -->" not in output
    assert "<!-- HONORS_CONTENT -->" not in output
    assert "<!-- DOWNLOADS_CONTENT -->" not in output


def test_opensource_template_render(env):
    template = env.get_template("opensource.html")
    meta = {
        "total_repos": 10,
        "total_stars": 250,
        "total_forks": 45,
        "sections": [
            {
                "title": "Academic Tools",
                "repositories": [
                    {
                        "name": "org/repo-a",
                        "title": "Repo A",
                        "description": "Academic tool A",
                        "lang": "Python",
                        "stars": 100,
                        "forks": 20,
                    }
                ],
            },
            {
                "title": "Multimedia Systems",
                "repositories": [
                    {
                        "name": "org/repo-b",
                        "title": "Repo B",
                        "description": "Multimedia tool B",
                        "lang": "C++",
                        "stars": 150,
                        "forks": 25,
                    }
                ],
            },
        ],
    }
    context = {
        "page": DummyPage(
            title="Open Source Repositories",
            meta=meta,
            content="<!-- ACADEMIC_TOOLS_GRID --><!-- MULTIMEDIA_SYSTEMS_GRID -->",
        )
    }
    output = template.render(context)
    assert 'id="github-repos-count">10<' in output
    assert 'id="github-stars-count">250<' in output
    assert 'id="github-forks-count">45<' in output
    assert "org/repo-a" in output
    assert "org/repo-b" in output
    assert "<!-- ACADEMIC_TOOLS_GRID -->" not in output
    assert "<!-- MULTIMEDIA_SYSTEMS_GRID -->" not in output


def test_projects_template_render(env):
    template = env.get_template("projects.html")
    projects = [
        DummyItem("PhD Topic 1", "projects/phd_active/topic1/"),
        DummyItem("PhD Topic 2", "projects/phd_available/topic2/"),
        DummyItem("UG Project 1", "projects/ug/project1/"),
        DummyItem("MSc Project 1", "projects/msc/project1/"),
    ]
    context = {
        "page": DummyPage(
            title="Projects",
            url="projects/",
            content="<!-- ACTIVE_PROJECTS_GRID --><!-- AVAILABLE_PROJECTS_GRID --><!-- UG_PROJECTS_GRID --><!-- MSC_PROJECTS_GRID -->",
        ),
        "nav": DummyNav(projects),
    }
    output = template.render(context)
    assert "PhD Topic 1" in output
    assert "PhD Topic 2" in output
    assert "UG Project 1" in output
    assert "MSc Project 1" in output
    assert "<!-- ACTIVE_PROJECTS_GRID -->" not in output
    assert "<!-- AVAILABLE_PROJECTS_GRID -->" not in output
    assert "<!-- UG_PROJECTS_GRID -->" not in output
    assert "<!-- MSC_PROJECTS_GRID -->" not in output
