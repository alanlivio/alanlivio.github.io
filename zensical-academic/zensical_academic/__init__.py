"""Zensical Academic Theme and Page Templates."""

from __future__ import annotations

from typing import Any

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
