#!/usr/bin/env bash

#Change permissions of /dev/kvm for Android Emulator
echo "$(whoami)" | sudo -S chmod 777 /dev/kvm > /dev/null 2>&1
# export PATH=$PATH:/studio-data/platform-tools/ # export will not work
# Ensure the Android directory exists and has the correct permissions
# if [ ! -d "/studio-data/Android" ]; then
#   mkdir -p /studio-data/Android
# fi
# sudo chown -R "${USER}":"${USER}" /studio-data/Android

# yes | flutter doctor --android-licenses || test $? -eq 141
