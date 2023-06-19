"""Stop apps."""

import click
from devtools import registration


@click.command
@click.option("--target", type=str, required=True)
def stop(target: str) -> None:
    registration.find_target(target).stop()
