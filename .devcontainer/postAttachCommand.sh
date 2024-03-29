#!/usr/bin/env bash
source ${HOME}/.bashrc

set -euo pipefail
shopt -s nullglob globstar

poetry config virtualenvs.in-project true
poetry install --no-cache
source "$(poetry env info --path)"/bin/activate

pre-commit install >/dev/null 2>&1
git lfs install >/dev/null 2>&1
git lfs track "*.png" >/dev/null 2>&1
git lfs track "*.jpg" >/dev/null 2>&1

DOCKER_XAUTHORITY=${HOME}/.Xauthority.docker
cp ~/.Xauthority "$DOCKER_XAUTHORITY"

#Change permissions of /dev/kvm for Android Emulator
echo "$(whoami)" | sudo -S chmod 777 /dev/kvm > /dev/null 2>&1
export PATH=$PATH:/studio-data/platform-tools/
# Ensure the Android directory exists and has the correct permissions
if [ ! -d "/studio-data/Android" ]; then
  mkdir -p /studio-data/Android
fi
sudo chown -R ${USER}:${USER} /studio-data/Android
