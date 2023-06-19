import logging
import os
import shutil
import string
import sys
from getpass import getpass
from pathlib import Path, PurePath

from devtools.config import REPO_CONFIG
from devtools.targets.target import Target

from libs.processing import processing
from wrappers.docker_wrapper import docker
from wrappers.linux_wrapper import linux
from wrappers.ssh_wrapper import ssh

MICROSERVICE_CONFIG_DIR = Path(__file__).parent / "microservice_config/"
NGINX_CONFIG_DIR = Path(__file__).parent / "nginx_config/"

logger = logging.getLogger()


class Microservice(Target):
    """A microservice is a single docker container that can be deployed to a VM.
    It is expected that the VM runs an NGINX instance.
    Reverse-proxying requests to the service is configured on deploy.
    If no NGINX is installed on the deployment VM, it is installed."""

    def __init__(
        self,
        target_name: str,
        domain_name: str,
        application_port: int,
        email: str,
        deployment_dir: PurePath,
    ) -> None:
        Target.__init__(self, target_name)
        self.app_build_dir = self.target_build_dir / "app"
        self.domain_name = domain_name
        self.email = email
        self.deployment_dir = deployment_dir
        self.application_port = application_port

    @classmethod
    def create(cls, target_name: str) -> None:
        target_dir = REPO_CONFIG.app_dir / target_name
        target_src_dir = target_dir / "src"
        target_src_dir.mkdir(parents=True)
        requirements_file = target_dir / "requirements.txt"
        requirements_file.touch()
        fastapi_entrypoint = target_src_dir / "main.py"
        fastapi_entrypoint.write_text(example_main_py())
        logger.info(
            "Your target %s was set up, please register it in registered_targets.py.",
            target_name,
        )

    def validate(self) -> bool:
        if not next(
            self.target_dir.glob("requirements.txt"),
            None,  # pyright: ignore [reportGeneralTypeIssues]
        ):
            logger.error("No Python requirements specified.")
            return False
        if not next(
            self.target_dir.glob("Dockerfile"),
            None,  # pyright: ignore [reportGeneralTypeIssues]
        ):
            logger.error("No Dockerfile.")
            return False
        if not self.target_src_dir.is_dir():
            logger.error("Missing a valid 'src' dir in %s.", self.target_dir)
            return False
        return True

    def build(self, clean: bool = False) -> None:
        """Build microservise as Docker container."""
        if clean:
            shutil.rmtree(self.target_build_dir, ignore_errors=True)
        try:
            shutil.copytree(self.target_src_dir, self.app_build_dir)
            shutil.copy(self.target_dir / "requirements.txt", self.target_build_dir)
        except FileExistsError:
            logger.error(
                "%s exists already. To overwrite, build --clean.", self.target_build_dir
            )
            sys.exit(1)
        api_key = getpass("Enter default API Key or leave empty to leave as is: ")
        with processing.temp_env(
            target_name=self.target_name,
            application_port=str(self.application_port),
            deployment_dir=self.deployment_dir.as_posix(),
            domain_name=self.domain_name,
            api_key=api_key,
            all_caps=True,
        ):
            copy_files_with_substitution(MICROSERVICE_CONFIG_DIR, self.target_build_dir)
            copy_files_with_substitution(
                NGINX_CONFIG_DIR, self.target_build_dir / "nginx_config"
            )
        if not api_key:
            (self.target_build_dir / "nginx_config" / "api_keys.conf").unlink()

    def test(self) -> None:
        pass

    def deploy(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            if session.run(["command", "-v", "docker", ">/dev/null 2>&1"]):
                session.run(docker.install_docker())
            if session.run(["command", "-v", "python", ">/dev/null 2>&1"]):
                session.run(linux.apt_get_install(["python-is-python3"]))
            if session.run(["command", "-v", "nginx", ">/dev/null 2>&1"]):
                session.run(linux.apt_get_install(["nginx"]))
                session.run(["rm", "/etc/nginx/sites-available/default"])
                session.run(["rm", "/etc/nginx/sites-enabled/default"])
            session.run(
                [
                    "cp",
                    "-r",
                    (self.deployment_dir / "nginx_config").as_posix() + "/.",
                    "/etc/nginx/",
                ]
            )
            session.upload(self.target_build_dir, self.deployment_dir)
            session.run(
                [
                    "cp",
                    (self.deployment_dir / f"api.conf").as_posix(),
                    f"/etc/nginx/api_conf.d/api_{self.target_name}.conf",
                ]
            )
            api_backend_append_string = (
                self.target_build_dir / "api_backend.conf"
            ).read_text()
            api_backend_append_string_first_line = (
                (self.target_build_dir / "api_backend.conf").read_text().split("\n")[0]
            )
            session.run(
                [
                    "grep",
                    "-q",
                    f"'{api_backend_append_string_first_line}'",
                    "/etc/nginx/api_backends.conf",
                    "||",
                    "cat",
                    "<<EOT",
                    ">>",
                    "/etc/nginx/api_backends.conf",
                    "\n",
                    f"{api_backend_append_string}",
                ]
            )
            session.run(docker.docker_build(self.deployment_dir, self.target_name))
            session.run(
                set_up_ssl_cert(
                    domain_name=self.domain_name,
                    email=self.email,
                )
            )

    def run(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            session.run(
                docker.docker_run(
                    {self.application_port: self.application_port},
                    self.target_name,
                )
            )
            session.run(["service", "nginx", "start"])

    def debug(self) -> None:
        pass

    def stop(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            session.run(
                docker.docker_stop(
                    self.target_name,
                )
            )
            session.run(["service", "nginx", "stop"])


def copy_files_with_substitution(template_dir: Path, target_dir: Path) -> None:
    """Copy a file with string substitution."""
    target_dir.mkdir(parents=True, exist_ok=True)
    for template in template_dir.rglob("*"):
        if template.is_dir():
            (target_dir / template.relative_to(template_dir)).mkdir(
                parents=True, exist_ok=True
            )
            continue
        (target_dir / template.relative_to(template_dir)).write_text(
            string.Template(template.read_text()).substitute(os.environ)
        )


def set_up_ssl_cert(
    domain_name: str,
    email: str,
) -> list[str]:
    certbot_cmd = [
        "certbot",
        "--nginx",
        "--agree-tos",
        "--test-cert",  # TODO: Get full cert
        "--non-interactive",
        "--email",
        email,
        "-d",
        domain_name,
    ]
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
    return """from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: int, q: Union[str, None] = None
) -> dict[str, int | str | None]:
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict[str, str | int]:
    return {"item_name": item.name, "item_id": item_id}
"""
