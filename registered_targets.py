"""Configuration file for devious."""
# ruff: noqa: F401
# pylint:disable=unused-import
# pyright: reportUnusedImport=false

import logging
from pathlib import PurePath  # Should be used for specifying remote paths

from devious.config import REPO_CONFIG
from devious.targets.django_app.django_app import DjangoApp
from devious.targets.microservice.microservice import Microservice
from devious.targets.target import Target
from devious.targets.webapp.webapp import Webapp

logger = logging.getLogger()

REGISTERED_TARGETS: list[Target] = []
