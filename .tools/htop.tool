#!/usr/env/bin bash

set -x

if [ $HTOP_INSTALLED ];
then
    echo "htop is already installed."

    return 0
fi

apt-get install -y htop

echo "# htop" >> ~/.profile

echo "export HTOP_INSTALLED=1" >> ~/.profile