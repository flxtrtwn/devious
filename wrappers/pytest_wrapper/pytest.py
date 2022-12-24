"""Wrapper for pytest cli."""

import logging
import subprocess
import webbrowser
from pathlib import Path

logger = logging.getLogger()


def test_directory(
    directory: Path,
    out_dir: Path | None = None,
    coverage: bool = False,
    vis: bool = False,
) -> bool:
    """Test directory with pytest and return if passed, optional coverage."""
    cmd = ["pytest", str(directory)]
    if coverage:
        cmd.extend(
            [
                f"--cov={directory}",
                "--cov-report=term",
                f"--cov-report=html:{out_dir}",
            ]
        )
    tests_passed = not subprocess.run(cmd).returncode
    if vis and out_dir:
        visual_coverage(out_dir)
    return tests_passed


def visual_coverage(directory: Path) -> None:
    webbrowser.open(f"{directory}/index.html")
