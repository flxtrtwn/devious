"""Wraps git commands."""
import subprocess
from pathlib import Path
from typing import Any, Iterable

import regex as re


def add(paths: Iterable[Path]):
    add_cmd = ["git", "add"]
    for path in paths:
        add_cmd.append(str(path))
    subprocess.run(add_cmd)


def commit(message: str, no_verify: bool = False):
    commit_cmd = ["git", "commit", "-m", message]
    if no_verify:
        commit_cmd.extend(["--no-verify"])
    subprocess.run(commit_cmd)


def push(remote: str = "origin", force: bool = False, mirror: bool = False) -> None:
    push_cmd = ["git", "push"]
    if force:
        push_cmd.extend(["--force-with-lease"])
    if mirror:
        push_cmd.extend(["--mirror"])
    if remote:
        push_cmd.extend([remote])
    subprocess.run(push_cmd)


def query_remote(remote_name: str = "origin") -> str | Any:
    query_remote_cmd = ["git", "remote", "show", remote_name]
    completed_process = subprocess.run(query_remote_cmd, capture_output=True, text=True)
    print(str(completed_process.stdout))
    if match := re.search(r"Push\s+URL: (https://.*?.git)", str(completed_process.stdout)):
        return match.group(1)
    raise ValueError("No remote found, output of %s: %s", query_remote_cmd, str(completed_process.stdout))


def clone(repo: str, folder: Path = Path("."), bare: bool = False) -> None:
    clone_cmd = ["git", "clone"]
    if bare:
        clone_cmd.extend(["--bare"])
    clone_cmd.extend([repo, folder.as_posix()])
    subprocess.run(clone_cmd)


def remote_add(name: str, target_repo: str) -> None:
    remote_add_cmd = ["git", "remote", "add", name, target_repo]
    subprocess.run(remote_add_cmd)


def remote_rename(old_name: str, new_name: str) -> None:
    remote_rename_cmd = ["git", "remote", "rename", old_name, new_name]
    subprocess.run(remote_rename_cmd)


def pull(remote: str = "origin", branch: str = "main", strategy: str = "merge") -> None:
    if strategy not in ["merge", "squash", "rebase"]:
        raise ValueError("Invalid pull strategy.")
    pull_cmd = ["git", "pull"]
    if strategy != "merge":
        pull_cmd.extend([f"--{strategy}"])
    if strategy != "rebase":
        pull_cmd.extend(["--no-rebase"])
    pull_cmd.extend([remote, branch])
    subprocess.run(pull_cmd)


def set_default_remote_for_branch(
    remote_name: str = "origin", local_branch_name: str = "main", remote_branch_name: str = "main"
) -> None:
    subprocess.run(["git", "push", "-u", remote_name, f"{local_branch_name}:{remote_branch_name}"])
