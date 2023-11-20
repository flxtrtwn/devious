"""Verify targets."""

import logging
import sys

import click

from devious import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str)
def verify(target: str) -> None:
    """Verify consistency of a target and of global config. Without specifying target, all targets are verified."""
    registration.verify_registration()
    if target:
        sys.exit(registration.find_target(target).verify())
    sys.exit(any(target.verify() for target in registration.REGISTERED_TARGETS))
