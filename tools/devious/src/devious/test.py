"""Coverage calculation."""

import logging
import sys

import click

from devious import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str)
@click.option("--coverage", is_flag=True, default=False, help="Calculate coverage during testing.")
def test(target: str, coverage: bool) -> None:
    """Run tests for a target. Without specifying target, all tests are run."""
    if target:
        sys.exit(registration.find_target(target).test(coverage))
    sys.exit(any(target.test(coverage) for target in registration.REGISTERED_TARGETS))
