"""Wraps ssh calls."""
import logging
import os
import subprocess
from getpass import getpass
from pathlib import Path, PurePath

from paramiko import SSHClient, WarningPolicy

from devious import utils

logger = logging.getLogger()


def login(target: str, user: str = "root") -> None:
    subprocess.run(["ssh", "-l", user, target])


def run_command(target: str, command: str, user: str = "root") -> None:
    subprocess.run(["ssh", "-l", user, target, command])


class SSHSession:
    def __init__(self, ip_address: str, user: str = "root") -> None:
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(WarningPolicy())  # TODO: Is this safe?
        self.client.load_system_host_keys()
        private_key_files = list((Path.home() / ".ssh").glob("id_*"))
        self.client.connect(
            hostname=ip_address,
            username=user,
            passphrase=getpass("Enter SSH private cert key: "),
            allow_agent=False,
            key_filename=[str(file) for file in private_key_files],
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:  # pyright: ignore
        self.client.close()

    def run(self, command: list[str]) -> int:
        command_string = utils.stringify(command)
        logger.debug("Running remote command: %s", command_string)
        _, stdout, stderr = self.client.exec_command(command_string, bufsize=1, get_pty=True)
        while line := stdout.readline():
            print(line.strip("\n"))
        if returncode := stdout.channel.recv_exit_status():
            logger.error(stderr.read().decode())
            return returncode
        return 0

    def upload(self, src: Path, dest_dir: PurePath):
        if src.is_file():
            with self.client.open_sftp() as ftp_client:
                ftp_client.put(src.as_posix(), (dest_dir / src.name).as_posix())
        if src.is_dir():
            with self.client.open_sftp() as ftp_client:
                self.run(["rm", "-rf", dest_dir.as_posix()])  # TODO: Ask user?
                self.run(["mkdir", "-p", dest_dir.as_posix()])
                for path, dirs, files in os.walk(src):
                    for dir in dirs:
                        ftp_client.mkdir(str(dest_dir / Path(path).relative_to(src) / dir))
                    for file in files:
                        ftp_client.put(
                            (Path(path) / file).as_posix(),
                            (dest_dir / Path(path).relative_to(src) / str(file)).as_posix(),
                        )


# TODO: Check server for vulnerabilites, e.g. password authentication not no in /etc/ssh/sshd_config
