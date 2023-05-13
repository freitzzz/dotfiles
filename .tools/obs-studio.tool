#!/usr/env/bin bash

set -x

if [ $OBS_STUDIO_INSTALLED ];
then
    echo "OBS Studio is already installed."

    return 0
fi

apt-get install -y obs-studio

echo "# OBS Studio" >> ~/.profile

echo "export OBS_STUDIO_INSTALLED=1" >> ~/.profile