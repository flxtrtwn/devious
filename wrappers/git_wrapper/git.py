"""Wraps git commands."""
import subprocess
from pathlib import Path

import regex as re


def push(remote: str = "origin", force: bool = False, mirror: bool = False) -> None:
    push_cmd = ["git", "push"]
    if force:
        push_cmd.extend(["--force-with-lease"])
    if mirror:
        push_cmd.extend(["--mirror"])
    if remote:
        push_cmd.extend([remote])
    subprocess.run(push_cmd)


def query_remote(remote_name: str = "origin"):
    query_remote_cmd = ["git", "remote", remote_name]
    completed_process = subprocess.run(query_remote_cmd, capture_output=True, text=True)
    if match := re.search(r"Push\s+URL: (https://.*?.git)", completed_process.stdout):
        return match.group(1)
    raise ValueError(
        "No remote found, output of %s: %s", query_remote_cmd, completed_process.stdout
    )


def clone(repo: str, folder: Path = Path("."), bare: bool = False) -> None:
    clone_cmd = ["git", "clone"]
    if bare:
        clone_cmd.extend(["--bare"])
    clone_cmd.extend([repo, folder.as_posix()])
    subprocess.run(clone_cmd)


def remote_add(name: str, target_repo: str) -> None:
    remote_add_cmd = ["git", "remote", "add", name, target_repo]
    subprocess.run(remote_add_cmd)


def pull(remote: str = "origin", branch: str = "main"):
    pull_cmd = ["git", "pull", remote, branch]
    subprocess.run(pull_cmd)
