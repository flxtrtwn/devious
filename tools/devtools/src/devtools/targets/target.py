"""Application abstractions."""
from abc import ABC, abstractmethod

from devtools.config import REPO_CONFIG


class Target(ABC):
    @abstractmethod
    def __init__(self, target_name: str) -> None:
        self.target_name = target_name
        self.target_dir = REPO_CONFIG.app_dir / self.target_name
        self.target_src_dir = self.target_dir / "src"
        self.target_tests_dir = self.target_dir / "tests"
        self.target_build_dir = REPO_CONFIG.build_dir / self.target_name

    @classmethod
    @abstractmethod
    def create(cls, target_name: str) -> None:
        """Create directory structure for target and register it where necessary."""

    @abstractmethod
    def validate(self) -> bool:
        """Check if target is consistent with model."""

    @abstractmethod
    def test(self, coverage: bool) -> bool:
        """Run tests for target. Returning non-zero indicates failure."""

    @abstractmethod
    def build(self, clean: bool) -> None:
        """Build target."""

    @abstractmethod
    def deploy(self) -> None:
        """Deploy target in production."""

    @abstractmethod
    def run(self) -> None:
        """Run (deployed) target."""

    @abstractmethod
    def debug(self) -> None:
        """Debug target."""

    @abstractmethod
    def stop(self) -> None:
        """Stop (deployed) target."""
