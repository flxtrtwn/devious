#!/bin/bash
set -e
trap "exit" INT

#TODO: Check if new script works
if [ ! -x "$(command -v docker)" ]; then
	echo "Docker is not installed. Installing Docker..."
	sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
	echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
         "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt-get update
	sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    # sudo echo "{"dns":[8.8.8.8]}" > /etc/docker/daemon.json for dns problems, !overwrites daemon.json!
elif ! docker info >/dev/null 2>&1; then
	echo "Docker is not running. Starting Docker..."
	sudo service docker start
else
	echo "Docker already installed and running."
fi

if id -nG $USER | grep -qw docker; then
	echo "$USER already in docker group."
else
	echo "Adding $USER to docker group..."
	sudo usermod -aG docker $USER
fi

if [ -x "$(command -v git)" ] || [ -x "$(command -v git-lfs)" ] || [ -x "$(command -v wget)" ]; then
	echo "git, git-lfs and wget already installed."
else
	echo "Installing git, git lfs and wget..."
	sudo apt-get install -y git git-lfs wget
fi

DEVCONTAINER_GIT_CONFIG=${REPOSITORY_ROOT}/.gitconfig
USER_GIT_CONFIG=~/.gitconfig
echo cmp $DEVCONTAINER_GIT_CONFIG $USER_GIT_CONFIG

if cmp $DEVCONTAINER_GIT_CONFIG $USER_GIT_CONFIG; then
	echo ".gitconfig of user $USER is identical to devcontainer .gitconfig."
else
	read -p "Replace .gitconfig of user $USER with the devcontainer .gitconfig? [y/n]: " REPLACE_USER_GIT_CONFIG
	if [ $REPLACE_USER_GIT_CONFIG = "y" ]; then
		cp $DEVCONTAINER_GIT_CONFIG $USER_GIT_CONFIG
		echo "Replaced .gitconfig of user $USER."
	fi
fi

USER_ENV_FILE=${REPOSITORY_ROOT}/.devcontainer/.user_env
if [ "$(tail -n 1 $USER_ENV_FILE)" = "USER=$USER" ]; then
	echo "User in .user_env file is already set correctly."
else
	echo "Setting User $USER in .user_env file..."
	echo "USER=$USER" >>$USER_ENV_FILE
fi
