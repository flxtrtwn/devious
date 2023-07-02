#!/usr/bin/env bash
source ${HOME}/.bashrc

set -euo pipefail
shopt -s nullglob globstar

pre-commit install
git lfs install
git lfs track "*.png"
git lfs track "*.jpg"

find /home/$USER/.platformio/packages/contrib-piohome/ -maxdepth 1 -name "main*" -exec sed -i 's#"\\\\":"/"#"/":"/"#g' {} + || echo "PlatformIO extension was not loaded when modification was tried"
sudo chmod a+rw /dev/ttyACM0 || true
