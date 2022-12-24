#!/bin/bash

# Make sure current user home contains files needed in devcontainer
touch ${HOME}/.netrc
touch ${HOME}/.gitconfig
touch ${HOME}/.Xauthority
mkdir -p ~/.ssh

export REPOSITORY_ROOT=$(realpath "$(dirname $0)"/..)

source ${REPOSITORY_ROOT}/.devcontainer/set_up_host.sh || echo "Failed to set up host."
