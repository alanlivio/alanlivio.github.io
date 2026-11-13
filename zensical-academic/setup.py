from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.editable_wheel import _TopLevelFinder, editable_wheel

PTH_FILENAME = "zensical_academic_autoload.pth"
PTH_CONTENT = "import zensical_academic\n"

_orig_get_implementation = _TopLevelFinder.get_implementation


def _get_implementation_with_autoload(self):
    yield from _orig_get_implementation(self)
    yield (PTH_FILENAME, PTH_CONTENT.encode("utf-8"))


_TopLevelFinder.get_implementation = _get_implementation_with_autoload


class BuildPy(build_py):
    def run(self):
        super().run()
        target = Path(self.build_lib) / PTH_FILENAME
        target.write_text(PTH_CONTENT, encoding="utf-8")


setup(cmdclass={"build_py": BuildPy, "editable_wheel": editable_wheel})
