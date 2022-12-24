"""Debug project."""

import logging

import click
from devtools import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str, required=True)
def debug(target: str) -> None:
    registration.find_target(target).debug()
