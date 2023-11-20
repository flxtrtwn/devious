"""Build project."""

import logging

import click

from devious import registration

logger = logging.getLogger()


@click.command()
@click.option("--clean", is_flag=True, default=False)
@click.option("--target", type=str, required=True)
def build(clean: bool, target: str) -> None:
    """Build software."""
    registration.find_target(target).build(clean)
    # logger.error("Not built anything.")
