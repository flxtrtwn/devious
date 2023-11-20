"""devious CLI."""

import logging

import click

from devious.build import build
from devious.create import create
from devious.debug import debug
from devious.deploy import deploy
from devious.inspect import inspect
from devious.install import install
from devious.run import run
from devious.stop import stop
from devious.test import test
from devious.update import update
from devious.verify import verify

logger = logging.getLogger()


@click.group()
@click.option("--verbose", is_flag=True, default=False, help="Set logging level to DEBUG.")
def cli(verbose: bool) -> None:
    """devious CLI top level command."""
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
cli.add_command(verify)
