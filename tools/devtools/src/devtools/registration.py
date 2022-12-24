from typing import Type

from devtools.registered_targets import REGISTERED_TARGETS
from devtools.targets.django_app.django_app import DjangoApp
from devtools.targets.microservice.microservice import Microservice
from devtools.targets.target import Target


def find_target(target_name: str) -> Target:
    for target in REGISTERED_TARGETS:
        if target.target_name == target_name:
            return target
    raise ValueError(f"No target with name {target_name}")


def register_target(target_name: str, target_type: Type[Target]) -> None:
    target_type.create(target_name)


def from_string(target_type: str) -> Type[Target]:
    return KNOWN_TARGETS[target_type]


KNOWN_TARGETS = {"django-app": DjangoApp, "microservice": Microservice}
