"""Stop apps."""

import click
from devtools import registration


@click.command
@click.option("--target", type=str, required=True)
@click.option("--ip-address", required=True, type=str)
def stop(target: str, ip_address: str) -> None:
    registration.find_target(target).stop(ip_address=ip_address)
