"""Docker related commands."""

from pathlib import PurePath

from devious.wrappers import linux


def install_docker() -> list[str]:
    return linux.chain_commands(
        [
            linux.apt_get_install(["ca-certificates", "curl", "gnupg"]),
            ["install", "-m", "0755", "-d", "/etc/apt/keyrings"],
            [
                "curl",
                "-fsSl",
                "https://download.docker.com/linux/ubuntu/gpg",
                "|",
                "gpg",
                "--dearmor",
                "-o",
                "/etc/apt/keyrings/docker.gpg",
                "--yes",
            ],
            ["chmod", "a+r", "/etc/apt/keyrings/docker.gpg"],
            [
                "echo",
                '"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] '
                'https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable"',
                "|",
                "tee",
                "/etc/apt/sources.list.d/docker.list > /dev/null",
            ],
            linux.apt_get_install(
                ["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"]
            ),
        ]
    )


def docker_build(dockerfile_dir: PurePath, app_name: str, cache: bool = True) -> list[str]:
    docker_build_cmd = ["docker", "build", dockerfile_dir.as_posix(), "-t", app_name, "--network", "host"]
    if not cache:
        docker_build_cmd.extend(["--no-cache"])
    return docker_build_cmd


def docker_compose_build(docker_compose_file: PurePath) -> list[str]:
    return ["docker", "compose", "-f", docker_compose_file.as_posix(), "build"]


def docker_run(bind_ports: dict[int, int], name: str, detached: bool = True) -> list[str]:
    cmd = [
        "docker",
        "run",
        "-it",
        "--network",
        "host",  # TODO: Remove network host
        # TODO: "--user",
        # TODO: "1000",
    ]
    [
        cmd.extend(["-p", f"127.0.0.1:{str(host_port)}:{str(docker_port)}"])
        for host_port, docker_port in bind_ports.items()
    ]
    if detached:
        cmd.extend(["-d"])
    cmd.extend([name])
    return cmd


def docker_stop(name: str) -> list[str]:
    return ["docker", "stop", f"$(docker ps -q --filter ancestor={name})"]


def docker_stop_dangling() -> list[str]:
    return [
        "for i in $(docker images -q --filter dangling=true) ; do docker container ps -q --filter ancestor=$i ; done | xargs docker stop"
    ]


def docker_compose_up(docker_compose_yaml: PurePath, detached: bool = True) -> list[str]:
    cmd = ["docker", "compose", "-f", docker_compose_yaml.as_posix(), "up", "--remove-orphans"]
    if detached:
        cmd.append("-d")
    return cmd


def docker_compose_down(docker_compose_yaml: PurePath) -> list[str]:
    return ["docker", "compose", "-f", docker_compose_yaml.as_posix(), "down", "--remove-orphans"]


def docker_compose_stop(docker_compose_yaml: PurePath) -> list[str]:
    return ["docker", "compose", "-f", docker_compose_yaml.as_posix(), "stop"]


def docker_compose_run(docker_compose_yaml: PurePath, commands: list[str]) -> list[str]:
    return ["docker", "compose", "-f", docker_compose_yaml.as_posix(), "run", *commands]


def docker_compose_exec(docker_compose_yaml: PurePath, commands: list[str]) -> list[str]:
    return ["docker", "compose", "-f", docker_compose_yaml.as_posix(), "exec", *commands]


def restart_docker() -> list[str]:
    return ["service", "docker", "restart"]


def docker_remove_containers() -> list[str]:
    return ["docker", "rm", "-f", "$(docker ps -a -q)"]
