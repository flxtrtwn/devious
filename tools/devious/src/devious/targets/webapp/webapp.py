import logging
import os
import string
from contextlib import contextmanager
from pathlib import Path, PurePath
from typing import Any, Dict, Generator, List

import dotenv
import ruamel.yaml

from devious.config import REPO_CONFIG
from devious.targets import target
from devious.targets.target import Target
from devious.wrappers import docker, linux, pytest, ssh

WEBAPP_CONFIG_DIR = Path(__file__).parent / "webapp_config/"
NGINX_CONFIG_DIR = Path(__file__).parent / "nginx_config/"

YAML = ruamel.yaml.YAML()

logger = logging.getLogger()


class Webapp(Target):
    """A webapp is a docker compose unit that can be deployed to a VM.
    It is expected that the VM runs an NGINX instance.
    Reverse-proxying requests to the service is configured on deploy.
    If no NGINX is installed on the deployment VM, it is installed."""

    def __init__(
        self,
        target_name: str,
        base_target_dir: Path,
        base_build_dir: Path,
        domain_name: str,
        application_port: int,
        email: str,
        deployment_dir: PurePath,
    ) -> None:
        Target.__init__(self, target_name, base_target_dir, base_build_dir)
        self.app_build_dir = self.target_build_dir / "app"
        self.domain_name = domain_name
        self.email = email
        self.deployment_dir = deployment_dir
        self.application_port = application_port
        self.entrypoint = self.target_src_dir / "main.py"
        self.deployed_docker_compose_yaml = self.deployment_dir / "docker-compose.yaml"
        self.secrets_yaml = self.target_dir / "secrets.yaml"

    @classmethod
    def create(cls, target_name: str) -> None:
        target_dir = REPO_CONFIG.app_dir / target_name
        target_dir.mkdir(parents=True)
        target_src_dir = target_dir / "src" / target_name
        target_src_dir.mkdir(parents=True)
        entrypoint = target_src_dir / "main.py"
        (target_src_dir.parent / "pyproject.toml").touch()
        entrypoint.write_text(example_main_py())
        (target_src_dir / "__init__.py").touch()
        target_tests_dir = target_dir / "tests"
        target_tests_dir.mkdir(parents=True)
        target.extend_pythonpath(target_src_dir.parent)
        docker_compose_file = target_dir / "docker-compose.yaml"
        ruamel.yaml.YAML().dump(
            {"services": {target_name: {"build": {"context": ".", "network": "host"}, "ports": None}}},
            docker_compose_file,
        )
        (target_dir / "secrets.yaml").write_text("path/to/file:\n  - SECRET_ID")
        logger.info("Your target %s was set up, please register it in registered_targets.py.", target_name)

    def verify(self) -> bool:
        if super().verify():
            return True
        if not next(
            self.target_dir.glob("pyproject.toml"),
            None,  # pyright: ignore [reportGeneralTypeIssues]
        ):
            logger.error("No Python requirements specified.")
            return True
        if not next(
            self.target_dir.glob("docker-compose.yaml"),
            None,  # pyright: ignore [reportGeneralTypeIssues]
        ):
            logger.error("No Docker compose file.")
            return True
        if not self.target_src_dir.is_dir():
            logger.error("Missing a valid 'src' dir in %s.", self.target_dir)
            return True
        return False

    def build(self, clean: bool = True) -> None:
        """Build webapp as Docker compose unit."""
        docker.docker_compose_build(self.target_dir / "docker-compose.yaml")

    def test(self, coverage: bool) -> bool:
        coverage_dir = REPO_CONFIG.metrics_dir / "pytest-coverage" / self.target_name
        return pytest.test_directory(REPO_CONFIG.project_root, out_dir=coverage_dir, coverage=coverage, vis=False)

    def deploy(self, test: bool) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            if session.run(["command", "-v", "docker", ">/dev/null 2>&1"]):
                session.run(docker.install_docker())
            if session.run(["command", "-v", "python", ">/dev/null 2>&1"]):
                session.run(linux.apt_get_install(["python-is-python3"]))
            if session.run(["command", "-v", "nginx", ">/dev/null 2>&1"]):
                session.run(linux.apt_get_install(["nginx"]))
                session.run(["rm", "/etc/nginx/sites-available/default"])
                session.run(["rm", "/etc/nginx/sites-enabled/default"])
            secrets: Dict[Path, List[str]] = {}
            try:
                secrets = {
                    self.target_dir / path: strings_to_substitute
                    for path, strings_to_substitute in YAML.load(self.secrets_yaml.read_text(encoding="utf-8")).items()
                }
                dotenv.load_dotenv(dotenv_path=self.target_dir / ".env")
            except FileNotFoundError:
                pass
            with substitute_placeholders(secrets, environment=os.environ):
                session.upload(self.target_dir, self.deployment_dir)
            session.run(["cp", "-r", (self.deployment_dir / "nginx_config").as_posix() + "/.", "/etc/nginx/"])
            session.run(docker.docker_compose_build(self.deployed_docker_compose_yaml))
            session.run(set_up_ssl_cert(domain_name=self.domain_name, email=self.email, test_cert=test))

    def run(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            session.run(docker.docker_compose_up(docker_compose_yaml=self.deployed_docker_compose_yaml))
            session.run(["service", "nginx", "start"])

    def debug(self, full: bool = False) -> None:
        # TODO: Ask which debug mode
        if full:
            self.build()
            docker.docker_compose_up(self.target_dir / "docker-compose.yaml")
        else:
            raise NotImplementedError
            # subprocess.run(["fastapi", "dev", self.target_src_dir / "main.py"])
            # subprocess.run(
            #     [
            #         "uvicorn",
            #         self.entrypoint.relative_to(self.target_src_dir.parent).with_suffix("").as_posix().replace("/", ".")
            #         + ":app",
            #         "--reload",
            #         "--reload-dir",
            #         self.target_src_dir,
            #         "--port",
            #         str(self.application_port),
            #     ]
            # )

    def stop(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            session.run(docker.docker_compose_stop(docker_compose_yaml=self.deployed_docker_compose_yaml))


@contextmanager
def substitute_placeholders(
    placeholders: Dict[Path, List[str]], environment: Dict[str, str]
) -> Generator[None, Any, None]:
    """Copy a file with string substitution."""
    for path, strings_to_substitute in placeholders.items():
        for string_to_substitute in strings_to_substitute:
            if string_to_substitute not in environment:
                raise ValueError(f"{string_to_substitute} not defined in environment.")
    backed_up_files: Dict[Path, str] = {path: path.read_text(encoding="utf-8") for path in placeholders}
    for path, content in backed_up_files.items():
        path.write_text(string.Template(content).substitute(environment), encoding="utf-8")
    try:
        yield
    finally:
        for path, content in backed_up_files.items():
            path.write_text(content, encoding="utf-8")


def configure_compose(dir: Path, app_name: str, app_docker_ports: dict[int, int]) -> None:
    docker_compose_file = dir / "docker-compose.yaml"
    data = YAML.load(docker_compose_file)
    data["services"][app_name].update(
        {"ports": [f"{str(host_port)}:{str(docker_port)}" for host_port, docker_port in app_docker_ports.items()]}
    )
    YAML.dump(data, docker_compose_file)


def set_up_ssl_cert(domain_name: str, email: str, test_cert: bool = False) -> list[str]:
    """Set up SSL certificate for nginx."""
    certbot_cmd = ["certbot", "--nginx", "--agree-tos", "--non-interactive", "--email", email, "-d", domain_name]
    if test_cert:
        certbot_cmd.append("--test-cert")
    return linux.chain_commands(
        [
            linux.apt_get_install(["python3", "python3-venv", "libaugeas0"]),
            ["python3", "-m", "venv", "/opt/certbot/"],
            ["/opt/certbot/bin/pip", "install", "--upgrade", "pip"],
            ["/opt/certbot/bin/pip", "install", "certbot", "certbot-nginx"],
            ["ln", "-s", "/opt/certbot/bin/certbot", "/usr/bin/certbot"],
            ["pkill", "nginx"],
            certbot_cmd,
            ["pkill", "nginx"],
        ],
        operator=";",
    )


def example_main_py():
    return """import asyncio
import concurrent.futures
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import github
import github.CheckRun
import pydantic
import zoneinfo
from fastapi import FastAPI, Header, HTTPException

try:
    # test_main is not in production container but can be used for load tests in test container
    # pylint: disable=unused-import
    from test import test_main  # noqa F401
except ImportError:
    print("PRODUCTION MODE")
    TEST = False
else:
    print("TEST MODE")
    TEST = True


class SomePayload(pydantic.BaseModel):
    some_string: str

    @pydantic.field_validator("some_string")
    @classmethod
    def validate_state(cls, value):
        if value == "incorrect":
            logger.debug("Ignoring incorrect value.")
            raise HTTPException(status_code=406, detail="Incorrect value")
        return value

class Webhook(pydantic.BaseModel):
    some_payload: SomePayload


logger = util.get_logger()
logger.setLevel(logging.INFO)
if TEST:
    logger.setLevel(logging.DEBUG)

app = FastAPI()

MAX_RETRIES = 10


@app.post("/")
async def bot(webhook: Webhook, x_some_header: str = Header()):

    event = some_header

    supported_events = ["some_event"]

    if event not in supported_events:
        logger.debug("Unsupported event: %s", event)
        raise HTTPException(status_code=406)

    logger.info("Handling request with id: %s request_id)

    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        try:
            await loop.run_in_executor(
                pool,
                process_event,
                webhook.some_payload.some_string,
            )
        except Exception as exc:
            logger.exception("Failed to process request with id %s", request_id)
            raise HTTPException(status_code=500) from exc

    logger.info("Finished request with id %s", request_id)
    return "ok"


def process_event(some_string: str):

    # Some setup code

    retries = 0
    while retries <= MAX_RETRIES:
        try:
            # Some application code
            return
        except Exception:
            logger.exception("Retry handling of event with some string: %s due to unexpected event", some_string)
            retries += 1
    raise ValueError(f"Failed to process request for event with some string: {some_string} after {retries} retries.")


@app.get("/")
async def alive():
    return "ok"
"""
