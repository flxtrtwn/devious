"""Coverage calculation."""

import logging
import sys

import click
from devtools import registration
from devtools.config import REPO_CONFIG

from wrappers.pytest_wrapper import pytest

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str)
@click.option("--coverage", is_flag=True, help="Calculate coverage during testing.")
@click.option("--vis", is_flag=True, help="Show visual test/coverage representation.")
def test(target: str, coverage: bool, vis: bool) -> None:
    """Run Python unit tests."""
    if target:
        registration.find_target(target).test()
    coverage_dir = REPO_CONFIG.metrics_dir / "pytest-coverage"
    if not pytest.test_directory(
        REPO_CONFIG.project_root, out_dir=coverage_dir, coverage=coverage, vis=vis
    ):
        sys.exit(1)
