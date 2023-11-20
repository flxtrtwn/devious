"""Wrapper for pytest cli."""

import logging
import subprocess
import webbrowser
from pathlib import Path

logger = logging.getLogger()


def test_directory(directory: Path, out_dir: Path | None = None, coverage: bool = False, vis: bool = False) -> bool:
    """Test directory with pytest and indicate failure with True (non-zero), optional coverage."""
    cmd = ["pytest", "-s", "-vvv", str(directory)]
    if coverage:
        cmd.extend([f"--cov={directory}", "--cov-report=term", f"--cov-report=html:{out_dir}"])
    tests_failed = subprocess.run(cmd).returncode == 1
    if vis and out_dir:
        visual_coverage(out_dir)
    return bool(tests_failed)


def visual_coverage(directory: Path) -> None:
    webbrowser.open(f"{directory}/index.html")
