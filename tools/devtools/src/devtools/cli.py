"""Devtools CLI."""

import logging

import click
from devtools.build import build
from devtools.create import create
from devtools.debug import debug
from devtools.deploy import deploy
from devtools.inspect import inspect
from devtools.install import install
from devtools.run import run
from devtools.stop import stop
from devtools.test import test
from devtools.update import update

logger = logging.getLogger()


@click.group()
@click.option(
    "--verbose", is_flag=True, default=False, help="Set logging level to DEBUG."
)
def cli(verbose: bool) -> None:
    """Devtools CLI top level command."""
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


cli.add_command(build)
cli.add_command(create)
cli.add_command(debug)
cli.add_command(deploy)
cli.add_command(inspect)
cli.add_command(install)
cli.add_command(run)
cli.add_command(stop)
cli.add_command(test)
cli.add_command(update)
