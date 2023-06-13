"""Update utilities."""

import logging
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import click

from wrappers.git_wrapper import git

logger = logging.getLogger()


@click.command()
def update() -> None:
    """Update dev environment"""
    devcontainer_repository = "https://github.com/flxtrtwn/devcontainer.git"
    devcontainer_repository_folder = Path("/tmp/devcontainer")
    development_repo_remote = git.query_remote()
    with switch_dir(devcontainer_repository_folder):
        git.clone(devcontainer_repository, bare=True)
        git.push(mirror=True, remote=development_repo_remote)
    shutil.rmtree(devcontainer_repository_folder)
    git.remote_add(name="upstream", target_repo=devcontainer_repository)
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
