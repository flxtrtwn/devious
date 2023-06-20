import logging
from pathlib import PurePath  # Should be used for specifying remote paths

from devtools.targets.django_app.django_app import DjangoApp
from devtools.targets.microservice.microservice import Microservice
from devtools.targets.target import Target
from devtools.targets.tool.tool import Tool

logger = logging.getLogger()

REGISTERED_TARGETS: list[Target] = [Tool("devtools")]
