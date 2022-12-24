"""Deploy project."""

import logging

import click
from devtools import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str, required=True)
@click.option("--ip-address", type=str, required=True, help="IP address of VM.")
@click.option("--build", is_flag=True, help="(Clean) build before deploying.")
@click.option("--run", is_flag=True, help="Run after deploying.")
def deploy(
    target: str, ip_address: str, build: bool = False, run: bool = False
) -> None:
    found_target = registration.find_target(target)
    if build:
        found_target.build(clean=True)
    found_target.deploy(ip_address)
    if run:
        found_target.run(ip_address)
