"""Update utilities."""

import logging
import os
import shutil
import subprocess
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
def update(private_remote: str) -> None:
    """Update dev environment with latest changes from devious repository.

    Needs to be used initially to decouple the devious upstream.
    The update is a simple file copy from a temporary cloned git repository.
    It can only add and update but not delete files.
    """

    devious_repo_remote = "https://github.com/flxtrtwn/devious.git"
    current_remote = git.query_remote()
    if current_remote == devious_repo_remote:
        if not click.confirm(
            "Updating your environment will detach it from the upstream remote (flxtrtwn/devious) "
            "and push it to your set private remote repository. Continue?"
        ):
            sys.exit(0)
        else:
            if not private_remote:
                logger.error("You need to specify --private-remote for the initial update setup.")
                sys.exit(1)
            git.remote_rename("origin", "devious_upstream")
            git.remote_add("origin", private_remote)
            git.set_default_remote_for_branch()
    devious_repo_folder = Path("/tmp/devious_upstream")
    shutil.rmtree(devious_repo_folder, ignore_errors=True)
    devious_repo_folder.mkdir(parents=True, exist_ok=True)
    with switch_dir(devious_repo_folder):
        git.clone(devious_repo_remote)
        shutil.rmtree(".git")
        shutil.rmtree("tools/devious")
        Path("registered_targets.py").unlink()
        Path("README.md").unlink()
        devious_project = Path("pyproject.toml")
        devious_project.write_text(
            re.sub(
                r"^devious ?= ?{.+$", 'devious = "*"', devious_project.read_text(encoding="utf-8"), flags=re.MULTILINE
            ),
            encoding="utf-8",
        )
    shutil.copytree(devious_repo_folder, REPO_CONFIG.project_root, dirs_exist_ok=True)
    shutil.rmtree(devious_repo_folder)
    if current_remote == devious_repo_remote:
        subprocess.run(["poetry", "update"], check=True)
        Path("README.md").unlink()
        git.add([Path("pyproject.toml"), Path("poetry.lock"), Path("tools"), Path("README.md")])
        git.commit("Detach from devious_upstream and lock Python environment")


@contextmanager
def switch_dir(dir: Path) -> Generator[None, Any, None]:
    current_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(current_dir)
