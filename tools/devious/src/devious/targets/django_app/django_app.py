import logging
import os
import shutil
import string
import subprocess
import sys
from pathlib import Path, PurePath

import ruamel.yaml

from devious import utils
from devious.config import REPO_CONFIG
from devious.targets.target import Target
from devious.wrappers import docker, linux, ssh

APP_CONFIG_DIR = Path(__file__).parent / "config"

logger = logging.getLogger()


class DjangoApp(Target):
    def __init__(
        self,
        target_name: str,
        base_target_dir: Path,
        base_build_dir: Path,
        domain_name: str,
        email: str,
        bind_ports: dict[int, int],
        application_port: int,
        deployment_dir: PurePath,
    ) -> None:
        Target.__init__(self, target_name, base_target_dir, base_build_dir)
        self.app_build_dir = self.target_build_dir / "app"
        self.domain_name = domain_name
        self.email = email
        self.bind_ports = bind_ports
        self.application_port = application_port
        self.deployment_dir = deployment_dir
        self.dev_django_manager = self.target_src_dir / "manage.py"
        self.build_django_manager = self.app_build_dir / "manage.py"
        self.build_docker_compose_yaml = self.target_build_dir / "docker-compose.yaml"
        self.deployed_django_manager = self.deployment_dir / "app" / "manage.py"
        self.deployed_docker_compose_yaml = self.deployment_dir / "docker-compose.yaml"

    @classmethod
    def create(cls, target_name: str) -> None:
        target_dir = REPO_CONFIG.app_dir / target_name
        target_src_dir = target_dir / "src"
        target_src_dir.mkdir(parents=True)
        subprocess.run(["django-admin", "startproject", target_name, target_src_dir.as_posix()])
        subprocess.run(["chmod", "+x", (target_src_dir / "manage.py").as_posix()])
        requirements_file = target_dir / "requirements.txt"
        requirements_file.touch()
        docker_compose_file = target_dir / "docker-compose.yaml"
        ruamel.yaml.YAML().dump(
            {
                "services": {
                    target_name: {
                        "build": {"context": ".", "network": "host"},
                        "ports": None,
                        "network_mode": "host",  # TODO: Apply proper networking
                    }
                }
            },
            docker_compose_file,
        )
        logger.info("Your target %s was set up, please register it in registered_targets.py.", target_name)

    def verify(self) -> bool:
        super().verify()
        if not next(
            self.target_dir.glob("requirements.txt"),
            None,  # pyright: ignore [reportGeneralTypeIssues]
        ):
            logger.error("No Python requirements specified.")
            return True
        if not self.target_src_dir.is_dir():
            logger.error("Missing a valid 'src' dir in %s.", self.target_dir)
            return True
        return False

    def build(self, clean: bool) -> None:
        """Build django app as Docker container."""
        subprocess.run(["django-admin", "makemessages", "-l", "de"], cwd=self.target_src_dir, check=True)
        subprocess.run(["django-admin", "compilemessages"], cwd=self.target_src_dir, check=True)

        if clean:
            shutil.rmtree(self.target_build_dir)  # TODO:, ignore_errors=True)
        try:
            shutil.copytree(self.target_src_dir, self.app_build_dir)
            shutil.copy(self.target_dir / "requirements.txt", self.target_build_dir)
            shutil.copy(self.target_dir / "docker-compose.yaml", self.target_build_dir)
        except FileExistsError:
            logger.error("%s exists already. To overwrite, build --clean.", self.target_build_dir)
            sys.exit(1)

        with utils.temp_env(
            app_name=self.target_name,
            exposed_ports=" ".join(str(docker_port) for _, docker_port in self.bind_ports.items()),
            application_port=str(self.application_port),
            deployment_dir=self.deployment_dir.as_posix(),
            domain_name=self.domain_name,
            all_caps=True,
        ):
            copy_files_with_substitution(APP_CONFIG_DIR, self.target_build_dir)
            configure_compose(self.target_build_dir, self.target_name, self.bind_ports)

    def test(self, coverage: bool) -> bool:
        # TODO: Implement tests for DjangoApp targets
        return False

    def deploy(self) -> None:
        subprocess.run([str(self.build_django_manager), "check", "--deploy"])
        with ssh.SSHSession(self.domain_name) as session:
            if session.run(["command", "-v", "docker", ">/dev/null 2>&1"]):
                session.run(docker.install_docker())
            if session.run(["command", "-v", "python", ">/dev/null 2>&1"]):
                session.run(linux.apt_get_install(["python-is-python3"]))
            session.upload(self.target_build_dir, self.deployment_dir)
            session.run(["chmod", "+x", self.deployed_django_manager.as_posix()])
            session.run(
                docker.docker_compose_run(
                    self.deployed_docker_compose_yaml,
                    [self.target_name, self.deployed_django_manager.as_posix(), "migrate"],
                )
            )
            # session.run( #TODO: Make interactive shells work
            #     docker.docker_compose_run(
            #         self.deployed_docker_compose_yaml,
            #         [
            #             self.target_name,
            #             self.deployed_django_manager.as_posix(),
            #             "createsuperuser",
            #         ],
            #     )
            # )
            # TODO: Run docker as non root user
            session.run(docker.docker_compose_build(self.deployed_docker_compose_yaml))
            session.run(
                set_up_ssl_cert(
                    docker_compose_yaml=self.deployed_docker_compose_yaml,
                    unsafe_nginx_conf=self.deployment_dir / "nginx.default.unsafe",
                    safe_nginx_conf=self.deployment_dir / "nginx.default",
                    domain_name=self.domain_name,
                    email=self.email,
                )
            )
            # TODO: docker compose run --rm certbot renew as cronjob

    def run(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            session.run(docker.docker_compose_up(docker_compose_yaml=self.deployed_docker_compose_yaml))

    def debug(self) -> None:
        subprocess.run(["django-admin", "makemessages", "-l", "de"], cwd=self.target_src_dir, check=True)
        subprocess.run(["django-admin", "compilemessages"], cwd=self.target_src_dir, check=True)
        subprocess.run(
            [str(self.dev_django_manager), "makemigrations", "--settings", f"{self.target_name}.debug_settings"],
            check=True,
        )
        subprocess.run(
            [str(self.dev_django_manager), "migrate", "--settings", f"{self.target_name}.debug_settings"], check=True
        )
        subprocess.run(
            [str(self.dev_django_manager), "runserver", "--settings", f"{self.target_name}.debug_settings"], check=True
        )

    def stop(self) -> None:
        with ssh.SSHSession(self.domain_name) as session:
            session.run(docker.docker_compose_stop(docker_compose_yaml=self.deployed_docker_compose_yaml))


def copy_files_with_substitution(template_dir: Path, target_dir: Path) -> None:
    """Copy a file with string substitution."""
    for template in template_dir.glob("*"):
        if template.is_file():
            (target_dir / template.name).write_text(
                string.Template((template_dir / template.name).read_text()).substitute(os.environ)
            )


def configure_compose(dir: Path, app_name: str, app_docker_ports: dict[int, int]) -> None:
    docker_compose_file = dir / "docker-compose.yaml"
    yaml = ruamel.yaml.YAML()
    data = yaml.load(docker_compose_file)
    data["services"][app_name].update(
        {"ports": [f"{str(host_port)}:{str(docker_port)}" for host_port, docker_port in app_docker_ports.items()]}
    )
    yaml.dump(data, docker_compose_file)


def set_up_ssl_cert(
    docker_compose_yaml: PurePath,
    unsafe_nginx_conf: PurePath,
    safe_nginx_conf: PurePath,
    domain_name: str,
    email: str,
    test_cert: bool = False,
) -> list[str]:
    backup_nginx_conf = safe_nginx_conf.parent / "nginx.default.backup"
    backup_cmd = ["cp", safe_nginx_conf.as_posix(), backup_nginx_conf.as_posix()]
    replacement_cmd = ["cp", unsafe_nginx_conf.as_posix(), safe_nginx_conf.as_posix()]
    set_up_ssl_cert_cmd = [
        "docker",
        "compose",
        "-f",
        docker_compose_yaml.as_posix(),
        "run",
        "--rm",
        "certbot",
        "certonly",
        "-v",
        "--agree-tos",
        "--non-interactive",
        "--email",
        email,
        "--webroot",
        "--webroot-path",
        "/var/www/certbot/",
        "-d",
        domain_name,
    ]
    if test_cert:
        set_up_ssl_cert_cmd.extend(["--test-cert"])
    restore_safe_conf_cmd = ["cp", backup_nginx_conf.as_posix(), safe_nginx_conf.as_posix()]
    delete_superfluous_confs_cmd = ["rm", unsafe_nginx_conf.as_posix(), backup_nginx_conf.as_posix()]
    return linux.chain_commands(
        [
            backup_cmd,
            replacement_cmd,
            docker.docker_compose_up(docker_compose_yaml, detached=True),
            set_up_ssl_cert_cmd,
            docker.docker_compose_stop(docker_compose_yaml),
            restore_safe_conf_cmd,
            delete_superfluous_confs_cmd,
        ],
        operator=";",
    )
