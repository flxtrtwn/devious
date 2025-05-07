"""Deploy project."""

import logging

import click

from devious import registration

logger = logging.getLogger()


@click.command()
@click.option("--target", type=str, required=True)
@click.option("--build", is_flag=True, help="(Clean) build before deploying.")
@click.option("--run", is_flag=True, help="Run after deploying.")
@click.option("--test", is_flag=True, help="Test environment.")
def deploy(target: str, build: bool = False, run: bool = False, test: bool = False) -> None:
    """Deploy application at target destination."""
    found_target = registration.find_target(target)
    if build:
        found_target.build(clean=True)
    found_target.deploy(test)
    if run:
        found_target.run()
