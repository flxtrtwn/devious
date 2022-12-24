"""Create project."""

import logging

import click
from devtools import registration

logger = logging.getLogger()


@click.command()
@click.option("--target-name", type=str, required=True)
@click.option(
    "--target-type",
    type=click.Choice(list(registration.KNOWN_TARGETS.keys())),
    required=True,
)
def create(target_name: str, target_type: str) -> None:
    registration.register_target(target_name, registration.from_string(target_type))
