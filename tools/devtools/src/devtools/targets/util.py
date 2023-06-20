"""Utility functions for target lifecycle."""
from pathlib import Path

import regex as re
from devtools.config import REPO_CONFIG


def extend_pythonpath(path: Path) -> None:
    envrc = REPO_CONFIG.project_root / ".envrc"
    content = envrc.read_text()
    envrc.write_text(
        re.sub(
            r"(pythonpath_add .+)\n(?!.*pythonpath_add.*)",
            rf"\g<1>\npythonpath_add {path.relative_to(REPO_CONFIG.project_root)}\n",
            content,
            flags=re.MULTILINE,
        )
    )
