"""Simple utility functions for devious."""


import logging
import multiprocessing
import os
from contextlib import contextmanager
from timeit import default_timer as timer
from typing import Any, Callable, Generator, NoReturn

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
