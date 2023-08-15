#!/usr/bin/env bash

set -x

if [ $NEOFETCH_INSTALLED ];
then
    echo "Neofetch is already installed."

    return 0
fi

apt-get install -y neofetch

echo "# Neofetch" >> ~/.profile

echo "export NEOFETCH_INSTALLED=1" >> ~/.profile