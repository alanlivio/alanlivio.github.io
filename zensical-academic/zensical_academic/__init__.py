"""Zensical Academic Theme and Page Templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from markdown import Extension, Markdown
from markdown.postprocessors import Postprocessor

__version__ = "0.1.0"
__all__ = ["AcademicExtension", "__version__", "makeExtension"]


class AcademicSectionsPostprocessor(Postprocessor):
    def run(self, text: str) -> str:
        context = None
        for processor in self.md.preprocessors:
            if getattr(processor, "name", None) == "rendering_context":
                context = processor
                break
        if context is None or not hasattr(context, "page"):
            return text
        meta = getattr(context.page, "meta", None)
        if not isinstance(meta, dict):
            return text
        sections = meta.get("sections")
        if not isinstance(sections, list):
            return text
        anchors: list[str] = []
        for sec in sections:
            if not isinstance(sec, dict):
                continue
            sec_id = sec.get("id")
            if not sec_id and sec.get("title"):
                sec_id = str(sec["title"]).lower().replace(" ", "-")
            if sec_id and f'id="{sec_id}"' not in text:
                anchors.append(f'<div id="{sec_id}"></div>')
        if not anchors:
            return text
        return text + "\n" + "\n".join(anchors)


class AcademicExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.postprocessors.register(
            AcademicSectionsPostprocessor(md),
            "zensical_academic_sections",
            0,
        )


def makeExtension(**kwargs: Any) -> AcademicExtension:
    return AcademicExtension(**kwargs)


def _register_zensical_hook() -> None:
    try:
        import zensical.config as zc
    except ImportError:
        return
    if getattr(zc, "_academic_hooked", False):
        return
    orig_apply_defaults = zc._apply_defaults

    def _apply_defaults_with_theme_extensions(
        config: dict[str, Any], path: str
    ) -> dict[str, Any]:
        theme_cfg_path = Path(__file__).resolve().parent / "mkdocs_theme.yml"
        if theme_cfg_path.is_file():
            with theme_cfg_path.open(encoding="utf-8") as f:
                theme_data = yaml.safe_load(f) or {}
            theme_font = theme_data.get("font")
            if isinstance(theme_font, dict):
                theme_section = config.get("theme")
                if isinstance(theme_section, dict) and "font" not in theme_section:
                    theme_section["font"] = dict(theme_font)
            theme_exts = theme_data.get("markdown_extensions")
            if isinstance(theme_exts, dict):
                user_exts = config.get("markdown_extensions")
                if user_exts is None:
                    merged = dict(theme_exts)
                elif isinstance(user_exts, dict):
                    merged = {**theme_exts, **user_exts}
                elif isinstance(user_exts, list):
                    merged = list(user_exts) + [
                        {k: v} if v else k for k, v in theme_exts.items()
                    ]
                else:
                    merged = user_exts
                config["markdown_extensions"] = merged
        result = orig_apply_defaults(config, path)
        if isinstance(result.get("theme"), dict):
            result["theme"].pop("markdown_extensions", None)
        return result

    zc._apply_defaults = _apply_defaults_with_theme_extensions
    zc._academic_hooked = True


_register_zensical_hook()
