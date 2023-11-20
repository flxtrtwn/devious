"""Install tools (on remote machines)."""

import logging

import click

from devious.wrappers import docker as docker_wrapper, ssh

logger = logging.getLogger()


@click.group()
@click.pass_context
@click.option("--ip-address", type=str, help="IP address to deploy application to.")
def install(ctx: click.Context, ip_address: str) -> None:
    """Install applications on remote machines."""
    ctx.ensure_object(dict)
    ctx.obj["ip_address"] = ip_address


@install.command()
@click.pass_context
def docker(ctx: click.Context) -> None:
    """Install docker if not installed yet."""
    ip_address = ctx.obj["ip_address"]
    with ssh.SSHSession(ip_address) as session:
        if session.run(["command", "-v", "docker", ">/dev/null 2>&1"]):
            session.run(docker_wrapper.install_docker())
