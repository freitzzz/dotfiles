#!/usr/bin/env bash

set -x

if [ $BATCAT_INSTALLED ];
then
    echo "batcat is already installed."

    return 0
fi

apt-get install -y bat

echo "# bat cat" >> ~/.profile

echo "export BATCAT_INSTALLED=1" >> ~/.profile