"""Application abstractions."""
from abc import ABC, abstractmethod

from devtools.config import REPO_CONFIG


class Target(ABC):
    @abstractmethod
    def __init__(self, target_name: str) -> None:
        self.target_name = target_name
        self.target_dir = REPO_CONFIG.app_dir / self.target_name
        self.target_src_dir = self.target_dir / "src"
        self.target_build_dir = REPO_CONFIG.build_dir / self.target_name

    @classmethod
    @abstractmethod
    def create(cls, target_name: str) -> None:
        pass

    @abstractmethod
    def validate(self) -> bool:
        return False

    @abstractmethod
    def test(self) -> None:
        pass

    @abstractmethod
    def build(self, clean: bool = False) -> None:
        pass

    @abstractmethod
    def deploy(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def debug(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
