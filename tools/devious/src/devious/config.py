"""Custom configuration of utilities like logging."""

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)


class CustomFormatter(logging.Formatter):
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32m"
    blue = "\x1b[32m"
    reset = "\x1b[0m"
    format_string = "%(asctime)s | %(levelname)s | %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format_string + reset,
        logging.INFO: green + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


[handler.setFormatter(CustomFormatter()) for handler in logging.getLogger().handlers]


class RepoConfig:
    """Context object class for click.ContextObject obj attribute."""

    def __init__(
        self,
        project_root: Path,
        build_dir: Path,
        tool_dir: Path,
        lib_dir: Path,
        app_dir: Path,
        registered_targets_path: Path,
        metrics_dir: Path,
    ) -> None:
        self.project_root = project_root
        self.build_dir = build_dir
        self.tool_dir = tool_dir
        self.lib_dir = lib_dir
        self.app_dir = app_dir
        self.registered_targets_path = registered_targets_path
        self.metrics_dir = metrics_dir


REPO_CONFIG = RepoConfig(
    project_root=Path(os.environ["PROJECT_ROOT"]),
    build_dir=Path(os.environ["BUILD_DIR"]),
    tool_dir=Path(os.environ["TOOL_DIR"]),
    lib_dir=Path(os.environ["LIB_DIR"]),
    app_dir=Path(os.environ["APP_DIR"]),
    registered_targets_path=Path(os.environ["REGISTERED_TARGETS"]),
    metrics_dir=Path(os.environ["METRICS_DIR"]),
)
