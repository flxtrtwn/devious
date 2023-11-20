# ruff: noqa: F401

import logging
from pathlib import PurePath  # Should be used for specifying remote paths

from devtools.config import REPO_CONFIG
from devtools.targets.django_app.django_app import DjangoApp
from devtools.targets.lib.lib import Lib
from devtools.targets.microservice.microservice import Microservice
from devtools.targets.target import Target
from devtools.targets.tool.tool import Tool

logger = logging.getLogger()

REGISTERED_TARGETS: list[Target] = [Tool("devtools", REPO_CONFIG.tool_dir, REPO_CONFIG.build_dir)]
