"""Inspect project."""

import logging
import os
import subprocess
from pathlib import Path

import click

logger = logging.getLogger()


@click.group()
def inspect() -> None:
    """Inspect project."""


@inspect.command()
@click.argument("directory", type=Path, default=".")
def files(directory: str) -> None:
    """Inspect project files."""
    file_list: list[str] = []
    for _, _, files in os.walk(directory):
        file_list.extend(files)
    print(file_list)


@inspect.command()
@click.argument("directory", type=Path, default=".")
def licenses(directory: str) -> None:
    """Inspect project files."""
    accepted_licenses = [
        "MIT License",
        "BSD License",
        "Apache Software License",
        "Apache License 2.0",
        "Python Software Foundation License",
        "The Unlicense (Unlicense)",
    ]
    completed_process = subprocess.run(["pip-licenses", "--no-version"], capture_output=True, text=True)
    for line in completed_process.stdout.split("\n")[1:-1]:
        if not any(accepted_license in line for accepted_license in accepted_licenses):
            logger.warning("Check used license for: %s", line)
