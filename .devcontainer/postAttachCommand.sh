#!/usr/bin/env bash
source ${HOME}/.bashrc

set -euo pipefail
shopt -s nullglob globstar

pre-commit install >/dev/null 2>&1
git lfs install >/dev/null 2>&1
git lfs track "*.png" >/dev/null 2>&1
git lfs track "*.jpg" >/dev/null 2>&1

sudo chmod a+rw /dev/ttyACM0 >/dev/null 2>&1 || echo "No device on /dev/ttyACM0"
sudo chmod a+rw /dev/ttyUSB0 >/dev/null 2>&1 || echo "No device on /dev/ttyUSB0"
find /home/$USER/.platformio/packages/contrib-piohome/ -maxdepth 1 -name "main*" -exec sed -i 's#"\\\\":"/"#"/":"/"#g' {} + || echo "PlatformIO extension was not loaded when modification was tried"
