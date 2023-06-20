import logging

from devtools.config import REPO_CONFIG
from devtools.targets import util
from devtools.targets.target import Target

from wrappers.pytest_wrapper import pytest

logger = logging.getLogger()


class Tool(Target):
    """Python command line application."""

    def __init__(
        self,
        target_name: str,
    ) -> None:
        Target.__init__(self, target_name)

    @classmethod
    def create(cls, target_name: str) -> None:
        target_dir = REPO_CONFIG.app_dir / target_name
        target_dir.mkdir(parents=True)
        (target_dir / "requirements.txt").touch()
        target_src_dir = target_dir / "src"
        target_src_dir.mkdir(parents=True)
        (target_src_dir / "__init__.py").touch()
        target_tests_dir = target_dir / "tests"
        target_tests_dir.mkdir(parents=True)
        util.extend_pythonpath(target_src_dir)
        logger.info(
            "Your target %s was set up, please register it in registered_targets.py.",
            target_name,
        )

    def validate(self) -> bool:
        return True

    def build(self, clean: bool) -> None:
        raise NotImplementedError

    def test(self, coverage: bool) -> bool:
        coverage_dir = REPO_CONFIG.metrics_dir / "pytest-coverage" / self.target_name
        return pytest.test_directory(
            REPO_CONFIG.project_root, out_dir=coverage_dir, coverage=coverage, vis=False
        )

    def deploy(self) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError

    def debug(self) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError
