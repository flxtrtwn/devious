"""Debug project."""

import logging

import click

from devious import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str, required=True)
@click.option("--full", type=bool, is_flag=True)
def debug(target: str, full: bool) -> None:
    """Debug target."""
    registration.find_target(target).debug(full)
