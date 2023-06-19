import logging
from pathlib import PurePath

from devtools.targets.django_app.django_app import DjangoApp
from devtools.targets.microservice.microservice import Microservice

logger = logging.getLogger()

REGISTERED_TARGETS = []
