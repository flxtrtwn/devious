"""Update utilities."""

import logging
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import click

from wrappers.git_wrapper import git

logger = logging.getLogger()


@click.command()
@click.option("--private_remote", type=str, required=True)
def update(private_remote: str) -> None:
    """Update dev environment if in a detached private repository."""
    devcontainer_repo_remote = "https://github.com/flxtrtwn/devcontainer.git"
    devcontainer_repo_folder = Path("/tmp/devcontainer")
    current_remote = git.query_remote()
    if current_remote == devcontainer_repo_remote:
        if not click.confirm(
            "Updating your environment will detach it from the upstream remote (flxtrtwn/devcontainer) "
            "and should only be used for private repositories where forking is not possible. Continue?"
        ):
            sys.exit(0)
        else:
            git.remote_rename("origin", "upstream")
            git.remote_add("origin", private_remote)
            with switch_dir(devcontainer_repo_folder):
                git.clone(devcontainer_repo_remote, bare=True)
                git.push(mirror=True, remote=private_remote)
            shutil.rmtree(devcontainer_repo_folder)
            git.remote_add(name="upstream", target_repo=devcontainer_repo_remote)
    git.pull(remote="upstream")
    git.push()


@contextmanager
def switch_dir(dir: Path) -> Generator[None, Any, None]:
    current_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(current_dir)
