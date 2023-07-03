import logging
from pathlib import Path

from devtools.targets.target import Target

logger = logging.getLogger()


class Embedded(Target):
    """An embedded target managed with PlatformIO extension."""

    def __init__(
        self,
        target_name: str,
        base_target_dir: Path,
        base_build_dir: Path,
    ) -> None:
        Target.__init__(self, target_name, base_target_dir, base_build_dir)
        self.target_src_dir = self.target_dir / target_name

    @classmethod
    def create(cls, target_name: str) -> None:
        logger.error(
            'Please use the PlatformIO VSCode extension to create embedded targets in the "apps" directory '
            "and register it afterwards in registered_targets.py."
        )

    def verify(self) -> bool:
        if super().verify():
            return True
        if not next(
            self.target_dir.glob("platformio.ini"),
            None,  # pyright: ignore [reportGeneralTypeIssues]
        ):
            logger.error("No platformio.ini file in %s.", self.target_dir)
            return True
        return False

    def build(self, clean: bool) -> None:
        """Build microservise as Docker container."""
        logger.info("Please use the PlatformIO VSCode extension for building.")

    def test(self, coverage: bool) -> bool:
        logger.warning(
            "Target %s was not tested, please test it with the PlatformIO VSCode Extension.",
            self.target_name,
        )
        return False

    def deploy(self) -> None:
        logger.info("Please use the PlatformIO extension for deployment.")

    def run(self) -> None:
        raise NotImplementedError

    def debug(self) -> None:
        logger.info("Please use the PlatformIO extension for debugging.")

    def stop(self) -> None:
        raise NotImplementedError
