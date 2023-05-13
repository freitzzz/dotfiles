#!/usr/env/bin bash

set -x

if [ $KEEPASS2_INSTALLED ];
then
    echo "Keepass2 is already installed."

    return 0
fi

apt-get install -y keepass2

echo "# Keepass2" >> ~/.profile

echo "export KEEPASS2_INSTALLED=1" >> ~/.profile
