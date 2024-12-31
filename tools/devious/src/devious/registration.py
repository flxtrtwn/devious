import importlib
from typing import Dict, List, Type

from devious.config import REPO_CONFIG
from devious.targets.django_app.django_app import DjangoApp
from devious.targets.microservice.microservice import Microservice
from devious.targets.target import Target
from devious.targets.webapp.webapp import Webapp

registered_targets = importlib.import_module("registered_targets", package=str(REPO_CONFIG.registered_targets_path))
REGISTERED_TARGETS: List[Target] = registered_targets.REGISTERED_TARGETS


def find_target(target_name: str) -> Target:
    for target in REGISTERED_TARGETS:
        if target.target_name == target_name:
            return target
    raise ValueError(f"No target with name {target_name}")


def register_target(target_name: str, target_type: Type[Target]) -> None:
    target_type.create(target_name)


def from_string(target_type: str) -> Type[Target]:
    return KNOWN_TARGETS[target_type]


def verify_registration() -> bool:
    target_names = [target.target_name for target in REGISTERED_TARGETS]
    return len(target_names) != len(set(target_names))


KNOWN_TARGETS: Dict[str, Type[Target]] = {"django-app": DjangoApp, "microservice": Microservice, "webapp": Webapp}
