"""Common linux utility commands."""


def chain_commands(commands: list[list[str]], operator: str = "&&") -> list[str]:
    chained_command = commands.pop(0)
    for command in commands:
        chained_command.extend([operator] + command)
    return chained_command


def apt_get_install(apps: list[str]) -> list[str]:
    cmd = [
        "export",
        "DEBIAN_FRONTEND=noninteractive" "&&" "apt-get",
        "update",
        "&&",
        "apt-get",
        "install",
        "--yes",
    ]
    cmd.extend(apps)
    return cmd
