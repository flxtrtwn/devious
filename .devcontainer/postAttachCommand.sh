#!/usr/bin/env bash
source ${HOME}/.bashrc

set -euo pipefail
shopt -s nullglob globstar

pre-commit install
