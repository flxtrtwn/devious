#!/usr/bin/env bash
source "${HOME}"/.bashrc

set -euo pipefail
shopt -s nullglob globstar

uv sync

pre-commit install >/dev/null 2>&1
git lfs install >/dev/null 2>&1
git lfs track "*.png" >/dev/null 2>&1
git lfs track "*.jpg" >/dev/null 2>&1

# DOCKER_XAUTHORITY=${HOME}/.Xauthority.docker
# cp ~/.Xauthority "$DOCKER_XAUTHORITY"
