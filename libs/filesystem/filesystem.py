"""Filesystem related operations."""
from contextlib import contextmanager


@contextmanager
def temp_modified_file():
    try:
        yield
    except:
        pass
    finally:
        pass
