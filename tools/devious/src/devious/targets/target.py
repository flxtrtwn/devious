"""Application abstractions."""

from abc import ABC, abstractmethod
from pathlib import Path

import regex as re

from devious.config import REPO_CONFIG


class Target(ABC):
    """Generic software target."""

    @abstractmethod
    def __init__(self, target_name: str, base_target_dir: Path, base_build_dir: Path) -> None:
        self.target_name = target_name
        self.target_dir: Path = base_target_dir / target_name
        self.target_src_dir: Path = self.target_dir / "src" / target_name
        self.target_tests_dir: Path = self.target_dir / "tests"
        self.target_build_dir: Path = base_build_dir / self.target_name

    @classmethod
    @abstractmethod
    def create(cls, target_name: str) -> None:
        """Create directory structure for target and register it where necessary."""

    @abstractmethod
    def test(self, coverage: bool) -> bool:
        """Run tests for target. Returning non-zero indicates failure."""

    @abstractmethod
    def build(self, clean: bool) -> None:
        """Build target, optionally clean."""

    @abstractmethod
    def deploy(self, test: bool) -> None:
        """Deploy target in production or test environment."""

    @abstractmethod
    def run(self) -> None:
        """Run (deployed) target."""

    @abstractmethod
    def debug(self, full: bool) -> None:
        """Debug target, include the full system if needed."""

    @abstractmethod
    def stop(self) -> None:
        """Stop (deployed) target."""

    def verify(self) -> bool:
        """Check if target is consistent with model, return True (non-zero) if not.
        If implementing additional checks in subclasses, call super first."""
        return self.target_src_dir != self.target_dir / "src" or self.target_tests_dir != self.target_dir / "tests"


def extend_pythonpath(path: Path) -> None:
    envrc = REPO_CONFIG.project_root / ".envrc"
    content = envrc.read_text()
    envrc.write_text(
        re.sub(
            r"(pythonpath_add .+)\n(?!.*pythonpath_add.*)",
            rf"\g<1>\npythonpath_add {path.relative_to(REPO_CONFIG.project_root)}\n",
            content,
            flags=re.MULTILINE,
        )
    )
