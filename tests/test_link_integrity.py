import re
import urllib.parse
from pathlib import Path
import yaml
import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib


@pytest.fixture(scope="module")
def website_dir():
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def docs_dir(website_dir):
    return website_dir / "docs"


@pytest.fixture(scope="module")
def config(website_dir):
    config_path = website_dir / "zensical.toml"
    with open(config_path, "rb") as f:
        return tomllib.load(f)


def test_no_spaces_in_directory_or_file_names(docs_dir):
    for path in docs_dir.rglob("*"):
        rel_path = path.relative_to(docs_dir)
        assert " " not in str(rel_path), f"Path contains spaces: {rel_path}"


def test_markdown_links_and_images_integrity(docs_dir, website_dir):
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    img_pattern = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']")

    md_files = list(docs_dir.rglob("*.md"))
    assert len(md_files) > 0

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        raw_targets = link_pattern.findall(content) + img_pattern.findall(content)

        for raw_target in raw_targets:
            target = raw_target.strip()
            if target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue

            assert (
                " " not in target
            ), f"Link contains unencoded space in {md_file}: {target}"
            assert (
                "%20" not in target
            ), f"Link contains encoded space (%20) in {md_file}: {target}"

            clean_target = target.split("#")[0].split("?")[0]
            if not clean_target:
                continue

            decoded_target = urllib.parse.unquote(clean_target)
            if decoded_target.startswith("/"):
                resolved = (docs_dir / decoded_target.lstrip("/")).resolve()
            else:
                resolved = (md_file.parent / decoded_target).resolve()

            assert (
                resolved.exists()
            ), f"Broken link in {md_file.relative_to(website_dir)}: '{target}' resolved to '{resolved}' which does not exist"


def test_external_urls_syntax(docs_dir, website_dir):
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    img_pattern = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']")

    for md_file in docs_dir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        raw_targets = link_pattern.findall(content) + img_pattern.findall(content)
        for raw_target in raw_targets:
            target = raw_target.strip()
            if target.startswith(("http://", "https://")):
                assert (
                    " " not in target
                ), f"Whitespace in external URL in {md_file.relative_to(website_dir)}: {target}"
                parsed = urllib.parse.urlparse(target)
                assert parsed.scheme in ("http", "https")
                assert bool(
                    parsed.netloc
                ), f"Missing netloc in external URL in {md_file.relative_to(website_dir)}: {target}"


def test_markdown_headings_surrounded_by_single_blank_line(docs_dir, website_dir):
    for md_file in docs_dir.rglob("*.md"):
        lines = md_file.read_text(encoding="utf-8").splitlines()
        start_idx = 0
        if lines and lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    start_idx = i + 1
                    break
        in_fence = False
        for i in range(start_idx, len(lines)):
            stripped = lines[i].strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if re.match(r"^#{1,6}\s+", stripped):
                if i > start_idx:
                    assert (
                        lines[i - 1].strip() == ""
                    ), f"Missing blank line before heading in {md_file.relative_to(website_dir)}:{i + 1}"
                    if i - 1 > start_idx:
                        assert (
                            lines[i - 2].strip() != ""
                        ), f"Multiple blank lines before heading in {md_file.relative_to(website_dir)}:{i + 1}"
                if i + 1 < len(lines):
                    assert (
                        lines[i + 1].strip() == ""
                    ), f"Missing blank line after heading in {md_file.relative_to(website_dir)}:{i + 1}"
                    if i + 2 < len(lines):
                        assert (
                            lines[i + 2].strip() != ""
                        ), f"Multiple blank lines after heading in {md_file.relative_to(website_dir)}:{i + 1}"


def test_project_frontmatter_and_images(docs_dir, website_dir):
    projects_dir = docs_dir / "projects"
    subdirs = ["phd_active", "phd_available", "ug", "msc"]
    project_files = []
    for sub in subdirs:
        project_files.extend((projects_dir / sub).rglob("*.md"))
    assert len(project_files) == 16

    for pfile in project_files:
        content = pfile.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        assert (
            len(parts) >= 3
        ), f"Missing frontmatter in {pfile.relative_to(website_dir)}"
        meta = yaml.safe_load(parts[1])
        assert isinstance(meta, dict)
        assert (
            "title" in meta and isinstance(meta["title"], str) and meta["title"].strip()
        )
        assert (
            "description" not in meta
        ), f"Unexpected 'description' in {pfile.relative_to(website_dir)}"
        assert (
            "tags" in meta and isinstance(meta["tags"], list) and len(meta["tags"]) > 0
        )
        for tag in meta["tags"]:
            assert isinstance(tag, str) and tag.strip()
        assert (
            "image" in meta and isinstance(meta["image"], str) and meta["image"].strip()
        )
        img = meta["image"].strip()
        if img.startswith(("http://", "https://")):
            parsed = urllib.parse.urlparse(img)
            assert bool(
                parsed.netloc
            ), f"Invalid remote image URL in {pfile.relative_to(website_dir)}: {img}"
        else:
            img_path = (pfile.parent / img.lstrip("/")).resolve()
            assert (
                img_path.is_file()
            ), f"Missing local project image in {pfile.relative_to(website_dir)}: {img}"


def test_zensical_favicon_configuration(config, docs_dir):
    theme = config.get("project", {}).get("theme", {})
    favicon = theme.get("favicon")
    assert favicon is not None, "Favicon is not configured in zensical.toml"
    assert not favicon.startswith(
        "fontawesome/"
    ), f"Favicon cannot be a raw icon path: {favicon}"

    favicon_file = docs_dir / favicon
    assert (
        favicon_file.is_file()
    ), f"Configured favicon file does not exist: {favicon_file}"


def test_site_url_is_https(config):
    site_url = config.get("project", {}).get("site_url", "")
    assert site_url.startswith("https://"), f"site_url should use HTTPS: {site_url}"


def test_redirect_maps_integrity(config, docs_dir):
    redirects = (
        config.get("project", {})
        .get("plugins", {})
        .get("redirects", {})
        .get("redirect_maps", {})
    )
    for source, target in redirects.items():
        clean_target = target.split("#")[0].split("?")[0]
        target_path = (docs_dir / clean_target).resolve()
        assert (
            target_path.exists()
        ), f"Redirect target does not exist: {source} -> {target}"
