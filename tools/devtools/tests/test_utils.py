"""Tests for os_util module."""
import os
from typing import NoReturn

import pytest
from devtools import utils


def callable_raising_exception() -> NoReturn:
    raise Exception


def test_wait_for_process() -> None:
    """Tests exception for process with non-zero exit code."""
    with pytest.raises(ValueError):
        with utils.wait_for_callable(callable_raising_exception):
            pass


def test_temp_env() -> None:
    """Test environment state when using temp_env context manager."""
    old_env = dict(os.environ)
    with utils.temp_env(test="test_variable"):
        assert os.environ.get("test") == "test_variable"
        os.environ["test2"] = "test_variable"
        assert os.environ.get("test2") == "test_variable"
    assert old_env == dict(os.environ)
    with utils.temp_env(all_caps=True, test="test_variable"):
        assert os.environ.get("TEST") == "test_variable"
        assert "test" not in os.environ
