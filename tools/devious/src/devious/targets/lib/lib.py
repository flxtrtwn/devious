import logging
from pathlib import Path

from devious.config import REPO_CONFIG
from devious.targets import target
from devious.targets.target import Target
from devious.wrappers import pytest

logger = logging.getLogger()


class Lib(Target):
    """Python library."""

    def __init__(self, target_name: str, base_target_dir: Path, base_build_dir: Path) -> None:
        Target.__init__(self, target_name, base_target_dir, base_build_dir)

    @classmethod
    def create(cls, target_name: str) -> None:
        target_dir = REPO_CONFIG.lib_dir / target_name
        target_dir.mkdir(parents=True)
        (target_dir / "requirements.txt").touch()
        target_src_dir = target_dir / "src"
        (target_src_dir / target_name).mkdir(parents=True)
        (target_src_dir / "__init__.py").touch()
        target_tests_dir = target_dir / "tests"
        target_tests_dir.mkdir(parents=True)
        target.extend_pythonpath(target_src_dir)
        logger.info("Your target %s was set up, please register it in registered_targets.py.", target_name)

    def verify(self) -> bool:
        return False

    def build(self, clean: bool) -> None:
        raise NotImplementedError

    def test(self, coverage: bool) -> bool:
        coverage_dir = REPO_CONFIG.metrics_dir / "pytest-coverage" / self.target_name
        return pytest.test_directory(self.target_tests_dir, out_dir=coverage_dir, coverage=coverage, vis=False)

    def deploy(self) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError

    def debug(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError
