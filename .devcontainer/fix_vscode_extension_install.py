#!/usr/bin/env python
import subprocess
from pathlib import Path

import jstyleson


def get_expected_extensions() -> set[str]:
    devcontainer_json_path = Path(".devcontainer/devcontainer.json")
    with devcontainer_json_path.open(encoding="utf-8", errors="ignore") as file:
        devcontainer_json = jstyleson.load(file)
    return set(devcontainer_json["customizations"]["vscode"]["extensions"])


def get_installed_extensions() -> set[str]:
    completed_process = subprocess.run(
        ["code", "--list-extensions"], capture_output=True
    )
    installed_extensions = str(completed_process.stdout).split(r"\n")[1:-1]
    return set(installed_extensions)


if __name__ == "__main__":
    for extension in get_expected_extensions() - get_installed_extensions():
        subprocess.run(["code", "--install-extension", extension, "--force"])
