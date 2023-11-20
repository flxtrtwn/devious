"""Common linux utility commands."""


def chain_commands(commands: list[list[str]], operator: str = "&&") -> list[str]:
    chained_command = commands.pop(0)
    for command in commands:
        chained_command.extend([operator] + command)
    return chained_command


def apt_get_install(apps: list[str]) -> list[str]:
    cmd = ["export", "DEBIAN_FRONTEND=noninteractive" "&&" "apt-get", "update", "&&", "apt-get", "install", "--yes"]
    cmd.extend(apps)
    return cmd


def append_to_file_not_contains(not_contains: str, to_append: str) -> list[str]:
    return [
        "grep",
        "-q",
        f"'{not_contains}'",
        "/etc/nginx/api_backends.conf",
        "||",
        "cat",
        "<<EOT",
        ">>",
        "/etc/nginx/api_backends.conf",
        "\n",
        f"{to_append}",
    ]
