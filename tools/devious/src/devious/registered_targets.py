# ruff: noqa: F401

import logging
from pathlib import PurePath  # Should be used for specifying remote paths

from devious.config import REPO_CONFIG
from devious.targets.django_app.django_app import DjangoApp
from devious.targets.lib.lib import Lib
from devious.targets.microservice.microservice import Microservice
from devious.targets.target import Target
from devious.targets.tool.tool import Tool

logger = logging.getLogger()

REGISTERED_TARGETS: list[Target] = [Tool("devious", REPO_CONFIG.tool_dir, REPO_CONFIG.build_dir)]
