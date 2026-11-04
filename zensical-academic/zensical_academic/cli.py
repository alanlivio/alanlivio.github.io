import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from pylatex import Document, Package
from pylatex.utils import NoEscape

try:
    import tomllib
except ImportError:
    import tomli as tomllib

__all__ = [
    "cli",
    "main",
    "build_parser",
    "generate_academic_tex",
    "resolve_default_pdf_output",
    "build_cv_pdf",
]


def _format_period(period: str) -> str:
    return (period or "").replace("--", "-").replace("-", "--")


def _extract_cvitems(entry: dict) -> list[tuple[str, str]]:
    if "items" in entry and isinstance(entry["items"], list):
        result = []
        for item in entry["items"]:
            if isinstance(item, dict):
                result.append((item.get("label") or "", item.get("text") or ""))
            elif isinstance(item, str):
                result.append(("", item))
        return result
    result = []
    for desc in entry.get("description", []):
        if isinstance(desc, str):
            result.append(("", desc))
    return result


def _append_cventry_with_cvitems(
    lines: list[str],
    period: str,
    role: str,
    place: str,
    items: list[tuple[str, str]],
) -> None:
    if not items:
        lines.append(f"    \\cventry{{{period}}}{{{role}}}{{{place}}}{{}}{{}}{{}}%")
        return
    lines.append(f"    \\cventry{{{period}}}{{{role}}}{{{place}}}{{}}{{}}{{%")
    for label, text in items:
        lines.append(f"      \\cvitem[0pt]{{{label}}}{{{text}}}%")
    lines.append("    }%")


def generate_academic_tex(toml_path: Path, output_path: Path | None = None) -> str:
    toml_path = Path(toml_path)
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    project = data.get("project", data)
    extra = project.get("extra", {})
    academic = extra.get("academic", {})

    full_name = academic.get("name", "Alan Guedes").strip()
    parts = full_name.split(None, 1)
    first_name = parts[0] if parts else full_name
    last_name = parts[1] if len(parts) > 1 else ""

    lines = [
        f"\\name{{{first_name}}}{{{last_name}}}",
    ]

    if email := academic.get("email"):
        lines.append(f"\\email{{{email}}}")
    if homepage := academic.get("homepage"):
        lines.append(f"\\homepage{{{homepage}}}")

    socials = extra.get("social", []) or academic.get("social", [])
    scholar_url = "https://scholar.google.com/citations?user=1bEOmkUAAAAJ"
    for s in socials:
        title = (s.get("title") or "").lower()
        raw_link = s.get("link") or ""
        clean_link = raw_link.replace("https://", "").replace("http://", "")
        if title == "github" or "github.com" in raw_link:
            lines.append(
                f"\\collectionadd[github]{{socials}}{{\\protect\\httpslink[github]{{{clean_link}}}}}"
            )
        elif title in ("scholar", "googlescholar") or "scholar.google" in raw_link:
            lines.append(
                f"\\collectionadd[googlescholar]{{socials}}{{\\protect\\httpslink[scholar]{{{clean_link}}}}}"
            )

    site_url = (
        project.get("site_url")
        or (f"https://{academic['homepage']}" if academic.get("homepage") else "")
        or "https://alanlivio.github.io"
    ).rstrip("/")
    cert_url = f"{site_url}/cv/"

    lines.append("")
    lines.append("\\newcommand{\\renderCertificatesFootnote}{%")
    lines.append(f"    \\footnotetext[1]{{See certificates at \\url{{{cert_url}}}}}%")
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderHighlights}{%")
    for hl in academic.get("highlights", []):
        label = hl.get("label") or ""
        text = hl.get("text") or ""
        lines.append(f"    \\cvitem{{{label}}}{{{text}}}%")
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderExperience}{%")
    for xp in academic.get("experience", []):
        period = _format_period(xp.get("cv_period") or xp.get("period") or "")
        role = xp.get("cv_role") or xp.get("role") or ""
        place = xp.get("cv_place") or xp.get("place") or ""
        items = _extract_cvitems(xp)
        _append_cventry_with_cvitems(lines, period, role, place, items)
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderEducation}{%")
    for edu in academic.get("education", []):
        period = _format_period(edu.get("period") or "")
        course = edu.get("course") or ""
        inst = edu.get("institution_full") or edu.get("institution") or ""
        lines.append(f"    \\cventry{{{period}}}{{{course}}}{{{inst}}}{{}}{{}}{{}}%")
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderFundingAwards}{%")
    funding_list = academic.get("funding_awards") or academic.get("accomplishments", [])
    for fa in funding_list:
        period = _format_period(str(fa.get("period") or fa.get("year") or ""))
        title = fa.get("title") or ""
        org = fa.get("organization") or ""
        items = _extract_cvitems(fa)
        _append_cventry_with_cvitems(lines, period, title, org, items)
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderSelectedPublications}{%")
    pub_summary = academic.get(
        "publications_summary",
        f"\\href{{{scholar_url}}}{{Google Scholar}} shows 50+ published papers, 160+ citations, h-index 7. See below recent and selected publications.",
    )
    lines.append(f"    \\cvitem{{}}{{{pub_summary}}}%")
    for pub in academic.get("publications", []):
        venue = pub.get("venue") or ""
        links = pub.get("links", [])
        formatted_links = ", ".join(
            f"\\href{{{lnk.get('url', '')}}}{{{lnk.get('year', '')}}}" for lnk in links
        )
        lines.append(f"    \\cvitem{{{venue}}}{{{formatted_links}}}%")
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderResearchCommittees}{%")
    for rc in academic.get("research_committees", []):
        period = _format_period(rc.get("period") or "")
        role = rc.get("role") or ""
        org = rc.get("organization") or ""
        items = _extract_cvitems(rc)
        _append_cventry_with_cvitems(lines, period, role, org, items)
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderIndustryCommittees}{%")
    for ic in academic.get("industry_committees", []):
        period = _format_period(ic.get("period") or "")
        role = ic.get("role") or ""
        org = ic.get("organization") or ""
        items = _extract_cvitems(ic)
        _append_cventry_with_cvitems(lines, period, role, org, items)
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderTraining}{%")
    for tr in academic.get("training", []):
        inst = tr.get("institution") or tr.get("label") or ""
        courses = tr.get("courses") or tr.get("text") or ""
        lines.append(f"    \\cvitem{{{inst}}}{{{courses}}}%")
    lines.append("}")

    lines.append("")
    lines.append("\\newcommand{\\renderReferences}{%")
    for ref in academic.get("references", []):
        name = ref.get("name") or ""
        email_addr = ref.get("email") or ""
        relation = ref.get("relation") or ""
        details = f"{email_addr}. {relation}".strip(". ") + "."
        lines.append(f"    \\cvitem{{{name}}}{{{details}}}%")
    lines.append("}")
    lines.append("")

    content = "\n".join(lines)
    if output_path:
        Path(output_path).write_text(content, encoding="utf-8")
    return content


def find_default_toml() -> Path:
    for candidate in [Path("zensical.toml"), Path("website/zensical.toml")]:
        if candidate.is_file():
            return candidate
    return Path("zensical.toml")


def find_default_output() -> Path:
    for d in ["cv", "paper", "src", "latex"]:
        if Path(d).is_dir():
            return Path(d) / "generated_academic.tex"
    return Path("cv/generated_academic.tex")


def resolve_default_pdf_output(toml_path: Path) -> Path:
    toml_path = Path(toml_path)
    docs_dir = "docs"
    cv_file = "cv.pdf"
    if toml_path.is_file():
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        project = data.get("project", data)
        docs_dir = project.get("docs_dir", "docs")
        academic = project.get("extra", {}).get("academic", {})
        cv_file = academic.get("cv_file", "cv.pdf")
    base_dir = toml_path.parent
    return base_dir / docs_dir / "assets" / "pdfs" / cv_file


def build_cv_pdf(toml_path: Path, output_pdf_path: Path | None = None) -> Path:
    if not shutil.which("latexmk") or not shutil.which("lualatex"):
        raise RuntimeError(
            "TeX Live (latexmk and lualatex) is not installed. Please install TeX Live."
        )
    toml_path = Path(toml_path)
    target_pdf = (
        Path(output_pdf_path)
        if output_pdf_path is not None
        else resolve_default_pdf_output(toml_path)
    )
    template_tex = Path(__file__).resolve().parent / "cv.tex"
    raw_tex = template_tex.read_text(encoding="utf-8")
    _, body_part = raw_tex.split("\\begin{document}", 1)
    body_tex, _ = body_part.rsplit("\\end{document}", 1)

    with tempfile.TemporaryDirectory() as tmp_str:
        tmp_dir = Path(tmp_str)
        generate_academic_tex(toml_path, tmp_dir / "generated_academic.tex")
        doc = Document(
            default_filepath=str(tmp_dir / "cv"),
            documentclass="moderncv",
            document_options=["10pt", "a4paper", "sans", "colorlinks"],
            fontenc=None,
            inputenc=None,
            lmodern=False,
            textcomp=False,
            page_numbers=True,
        )
        doc.packages.append(Package("url"))
        doc.packages.append(Package("footmisc"))
        doc.packages.append(Package("textcomp"))
        doc.packages.append(
            Package("geometry", options=["a4paper", "left=20mm", "top=20mm"])
        )
        doc.preamble.append(NoEscape(r"\linespread{1}"))
        doc.preamble.append(NoEscape(r"\setlength{\parskip}{0pt}"))
        doc.preamble.append(NoEscape(r"\setlength{\parsep}{0pt}"))
        doc.preamble.append(
            NoEscape(
                "\\newcommand\\setHyperrefBlueLinks{\n"
                "  \\definecolor{links}{HTML}{2A1B81}\n"
                "  \\hypersetup{urlcolor=links,linkcolor=links,citecolor=links}\n"
                "}"
            )
        )
        doc.preamble.append(NoEscape(r"\moderncvstyle{banking}"))
        doc.preamble.append(NoEscape(r"\moderncvcolor{blue}"))
        doc.preamble.append(NoEscape(r"\input{generated_academic.tex}"))
        doc.preamble.append(NoEscape(r"\title{C.V.}"))
        doc.append(NoEscape(body_tex.strip()))
        doc.generate_pdf(
            str(tmp_dir / "cv"),
            clean=True,
            clean_tex=True,
            compiler="latexmk",
            compiler_args=["-cd", "-pdflua"],
        )
        compiled_pdf = tmp_dir / "cv.pdf"
        target_pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(compiled_pdf, target_pdf)

    return target_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zensical-academic",
        description="CLI utilities for the zensical-academic theme.",
    )
    subparsers = parser.add_subparsers(dest="command")

    for cmd_name in ("cv.pdf", "pdf"):
        pdf_parser = subparsers.add_parser(
            cmd_name,
            help="Compile the LaTeX CV PDF directly from zensical.toml",
        )
        pdf_parser.add_argument(
            "toml",
            nargs="?",
            default=None,
            help="Path to zensical.toml (defaults to zensical.toml or website/zensical.toml)",
        )
        pdf_parser.add_argument(
            "output",
            nargs="?",
            default=None,
            help="Path to output PDF file (defaults to docs/assets/pdfs/cv.pdf)",
        )

    latex_parser = subparsers.add_parser(
        "latex",
        help="Generate LaTeX academic macros from zensical.toml",
    )
    latex_parser.add_argument(
        "toml",
        nargs="?",
        default=None,
        help="Path to zensical.toml (defaults to zensical.toml or website/zensical.toml)",
    )
    latex_parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Path to output .tex file (defaults to cv/generated_academic.tex)",
    )
    return parser


def cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in ("cv.pdf", "pdf"):
        toml_path = (
            Path(args.toml) if getattr(args, "toml", None) else find_default_toml()
        )
        output_path = (
            Path(args.output)
            if getattr(args, "output", None)
            else resolve_default_pdf_output(toml_path)
        )
        build_cv_pdf(toml_path, output_path)
        return 0

    if args.command == "latex" or args.command is None:
        toml_path = (
            Path(args.toml) if getattr(args, "toml", None) else find_default_toml()
        )
        output_path = (
            Path(args.output)
            if getattr(args, "output", None)
            else find_default_output()
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        generate_academic_tex(toml_path, output_path)
        return 0

    parser.print_help()
    return 1


main = cli

if __name__ == "__main__":
    sys.exit(cli())
