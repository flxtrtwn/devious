#!/bin/bash

# This script is intended to be run on a non-priviledged user account
# Machine restart is required to add user to docker group

set -e
trap "exit" INT

# Make sure current user home contains files needed in devcontainer
touch ${HOME}/.netrc
touch ${HOME}/.Xauthority
mkdir -p ~/.ssh

export REPOSITORY_ROOT=$(realpath "$(dirname $0)"/..)

#TODO: Check if new script works
if [ ! -x "$(command -v docker)" ]; then
	echo "Docker is not installed. Installing Docker..."
	sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
	echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
         "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update && sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    # sudo echo "{"dns":[8.8.8.8]}" > /etc/docker/daemon.json for dns problems, !overwrites daemon.json!
fi
if ! docker info >/dev/null 2>&1; then
	echo "Docker is not running. Starting Docker..."
	sudo service docker start
fi
if [ ! -x "$(command -v gh)" ]; then
	echo "GitHub CLI is not installed. Installing Docker..."
	sudo apt-get update && sudo apt-get install -y gh
fi

if id -nG $USER | grep -qw docker; then
	echo "$USER already in docker group."
else
	echo "Adding $USER to docker group..."
	sudo usermod -aG docker $USER
fi

if [ ! -x "$(command -v git)" ] || [ ! -x "$(command -v git-lfs)" ] || [ ! -x "$(command -v wget)" ]; then
	echo "Installing git, git lfs and wget..."
	sudo apt-get update && sudo apt-get install -y git git-lfs wget
fi

if [ ! -x "/opt/wsl-sudo/wsl-sudo.py" ]; then
    echo "Installing wudo for windows admin privileges"
    sudo git clone https://github.com/Chronial/wsl-sudo.git /opt/wsl-sudo
    # echo alias wudo=\"python3 /opt/wsl-sudo/wsl-sudo.py\" >> ~/.bash_aliases
fi

USER_ENV_FILE=${REPOSITORY_ROOT}/.devcontainer/.user_env
if [ ! "$(tail -n 1 $USER_ENV_FILE)" = "USER=$USER" ]; then
	echo "Setting User $USER in .user_env file..."
	echo "USER=$USER" >>$USER_ENV_FILE
fi

HOST_DISPLAY=10
DOCKER_DISPLAY=99
AUTH_COOKIE=$(xauth list | grep "^$(hostname)/unix:$HOST_DISPLAY " | awk '{print $3}')
CONTAINER_HOSTNAME=devious
DOCKER_XAUTHORITY=${HOME}/.Xauthority.docker
rm $DOCKER_XAUTHORITY || echo "Adding $DOCKER_XAUTHORITY"
touch "$DOCKER_XAUTHORITY"
xauth -f ${DOCKER_XAUTHORITY} add ${CONTAINER_HOSTNAME}/unix:${DOCKER_DISPLAY} MIT-MAGIC-COOKIE-1 ${AUTH_COOKIE}
CONTAINER_SOCKET=/tmp/.X11-unix/X${DOCKER_DISPLAY}
sudo apt update && sudo apt install daemonize
DAEMON_LOCKFILE=${HOME}/.socat-x11-bridge.lock
sudo kill "$(cat "$DAEMON_LOCKFILE")" || echo "Process with PID in $DAEMON_LOCKFILE not running"
rm "$DAEMON_LOCKFILE" || echo "No lockfile existing at $DAEMON_LOCKFILE"
daemonize -l "$DAEMON_LOCKFILE" -p "$DAEMON_LOCKFILE" /usr/bin/socat TCP:localhost:60${HOST_DISPLAY},fork,reuseaddr UNIX-LISTEN:${CONTAINER_SOCKET}
