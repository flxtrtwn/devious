"""Verify targets."""

import logging
import sys

import click
from devtools import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str)
def verify(target: str) -> None:
    """Run tests for a target. Without specifying target, all tests are run."""
    if target:
        sys.exit(registration.find_target(target).verify())
    sys.exit(any(target.verify() for target in registration.REGISTERED_TARGETS))
