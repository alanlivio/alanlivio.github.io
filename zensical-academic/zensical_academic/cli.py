import argparse
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

__all__ = ["cli", "main", "build_parser", "generate_academic_tex"]


def generate_academic_tex(toml_path: Path, output_path: Path | None = None) -> str:
    toml_path = Path(toml_path)
    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    project = data.get("project", data)
    academic = project.get("extra", {}).get("academic", {})

    full_name = academic.get("name", "Alan Guedes").strip()
    parts = full_name.split(None, 1)
    first_name = parts[0] if parts else full_name
    last_name = parts[1] if len(parts) > 1 else ""

    lines = [
        f"% Auto-generated from {toml_path.name}. Do not edit manually.",
        f"\\name{{{first_name}}}{{{last_name}}}",
    ]

    if email := academic.get("email"):
        lines.append(f"\\email{{{email}}}")
    if homepage := academic.get("homepage"):
        lines.append(f"\\homepage{{{homepage}}}")

    lines.append("")
    lines.append("\\newcommand{\\renderEducation}{%")
    for edu in academic.get("education", []):
        period = (edu.get("period") or "").replace("-", "--")
        course = edu.get("course") or ""
        inst = edu.get("institution_full") or edu.get("institution") or ""
        lines.append(f"    \\cventry{{{period}}}{{{course}}}{{{inst}}}{{}}{{}}{{}}%")
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
    if Path("src").is_dir():
        return Path("src/generated_academic.tex")
    return Path("latex/generated_academic.tex")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zensical-academic",
        description="CLI utilities for the zensical-academic theme.",
    )
    subparsers = parser.add_subparsers(dest="command")

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
        help="Path to output .tex file (defaults to src/generated_academic.tex or latex/generated_academic.tex)",
    )
    return parser


def cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

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
