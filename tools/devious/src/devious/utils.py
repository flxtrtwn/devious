"""Simple utility functions for devious."""

import logging
import multiprocessing
import os
import string
from contextlib import contextmanager
from pathlib import Path
from timeit import default_timer as timer
from typing import Any, Callable, Dict, Generator, List, NoReturn

logger = logging.getLogger()


def stringify(commands: list[str]) -> str:
    return " ".join(commands)


@contextmanager
def wait_for_callable(callable_object: Callable[[], NoReturn]) -> Generator[None, Any, None]:
    """Execute code while waiting for a Process based on a Callable to complete."""
    process = multiprocessing.Process(target=callable_object)
    process.start()
    try:
        yield
    finally:
        start_time = timer()
        process.join()
        logger.debug("Process %s took %s longer than code in context manager.", callable_object, timer() - start_time)
        if process.exitcode:
            raise ValueError(f"Process {callable_object} completed with non-zero exit code.")


@contextmanager
def temp_env(all_caps: bool = False, **kwargs: str) -> Generator[None, Any, None]:
    """Temporary set environment variables, e.g. for expansion in templates."""
    if all_caps:
        kwargs = {key.upper(): value for key, value in kwargs.items()}
    old = dict(os.environ)
    os.environ.update(**kwargs)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old)


@contextmanager
def substitute_placeholders(
    placeholders: Dict[Path, List[str]], environment: Dict[str, str]
) -> Generator[None, Any, None]:
    """Copy a file with string substitution."""
    for path, strings_to_substitute in placeholders.items():
        for string_to_substitute in strings_to_substitute:
            if string_to_substitute not in environment:
                raise ValueError(f"{string_to_substitute} not defined in environment.")
    backed_up_files: Dict[Path, str] = {path: path.read_text(encoding="utf-8") for path in placeholders}
    for path, content in backed_up_files.items():
        path.write_text(string.Template(content).substitute(environment), encoding="utf-8")
    try:
        yield
    finally:
        for path, content in backed_up_files.items():
            path.write_text(content, encoding="utf-8")
