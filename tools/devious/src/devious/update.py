"""Update utilities."""

import logging
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import click
import regex as re

from devious.config import REPO_CONFIG
from devious.wrappers import git

logger = logging.getLogger()


@click.command()
@click.option("--private-remote", type=str, help="Link to your initialized (private) repository (with .git ending).")
@click.option(
    "--strategy",
    type=click.Choice(["squash", "merge", "rebase"]),
    default="squash",
    help="Set merge strategy for upstream commits.",
)
def update(private_remote: str, strategy: str) -> None:
    """Update dev environment with latest changes from devcontainer repository.
    Needs to be used initially to decouple the devcontainer upstream.
    strategy: The way the update is applied, defaults to having a single squash commit."""

    devcontainer_repo_remote = "https://github.com/flxtrtwn/devcontainer.git"
    current_remote = git.query_remote()
    if current_remote == devcontainer_repo_remote:
        if not click.confirm(
            "Updating your environment will detach it from the upstream remote (flxtrtwn/devcontainer) "
            "and push it to your set private remote repository. Continue?"
        ):
            sys.exit(0)
        else:
            if not private_remote:
                logger.error("You need to specify --private-remote for the initial update setup.")
                sys.exit(1)
            git.remote_rename("origin", "devcontainer_upstream")
            git.remote_add("origin", private_remote)
            git.set_default_remote_for_branch()
    devcontainer_repo_folder = Path("/tmp/devcontainer_upstream")
    shutil.rmtree(devcontainer_repo_folder, ignore_errors=True)
    devcontainer_repo_folder.mkdir(parents=True, exist_ok=True)
    with switch_dir(devcontainer_repo_folder):
        git.clone(devcontainer_repo_remote)
        shutil.rmtree(".git")
        devcontainer_project = Path("pyproject.toml")
        devcontainer_project.write_text(
            re.sub(
                r"^devious ?= ?{.+$",
                'devious = "^0.1.0"',
                devcontainer_project.read_text(encoding="utf-8"),
                flags=re.MULTILINE,
            )
        )
    shutil.copytree(devcontainer_repo_folder, REPO_CONFIG.project_root, dirs_exist_ok=True)
    shutil.rmtree(devcontainer_repo_folder)
    if current_remote == devcontainer_repo_remote:
        shutil.rmtree("tools/devious")
        git.add([Path("pyproject.toml"), Path("poetry.lock"), Path("tools/devious")])
        git.commit("Detach from devcontainer_upstream and lock Python environment")


@contextmanager
def switch_dir(dir: Path) -> Generator[None, Any, None]:
    current_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(current_dir)
