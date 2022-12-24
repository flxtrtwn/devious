"""Run apps."""

import click
from devtools import registration


@click.command
@click.option("--target", type=str, required=True)
@click.option("--ip-address", type=str, required=True)
def run(target: str, ip_address: str) -> None:
    registration.find_target(target).run(ip_address=ip_address)
