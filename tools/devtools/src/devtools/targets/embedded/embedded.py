import logging
import string
from pathlib import Path

from devtools.config import REPO_CONFIG
from devtools.targets.target import Target

logger = logging.getLogger()

PLATFORMIO_TEMPLATE="""[platformio]
build_dir = /workspace/build/${APP_NAME}
[env:release]
platform = atmelavr
framework = arduino
board = megaatmega2560
"""

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
        target_dir = REPO_CONFIG.app_dir / target_name
        target_dir.mkdir(parents=True)
        platformio_file = (target_dir / "platformio.ini")
        platformio_file.write_text(string.Template(PLATFORMIO_TEMPLATE).substitute(
                    {"APP_NAME":target_name}
                ))
        # target_tests_dir = target_dir / "tests"
        # target_tests_dir.mkdir(parents=True)
        logger.info(
            "Your target %s was set up, please register it in registered_targets.py.",
            target_name,
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
        raise NotImplementedError

    def deploy(self) -> None:
        logger.info("Please use the PlatformIO extension for deployment.")

    def run(self) -> None:
        raise NotImplementedError

    def debug(self) -> None:
        logger.info("Please use the PlatformIO extension for debugging.")

    def stop(self) -> None:
        raise NotImplementedError
