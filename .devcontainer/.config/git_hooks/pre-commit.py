#!/usr/bin/env python3

import sys
from pathlib import Path

from wrappers.pytest_wrapper import pytest

if __name__ == "__main__":
    if not pytest.test_directory(Path(".")):
        sys.exit(1)
