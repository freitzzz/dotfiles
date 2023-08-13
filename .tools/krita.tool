#!/usr/env/bin bash

set -x

if [ $KRITA_INSTALLED ];
then
    echo "krita is already installed."

    return 0
fi

apt-get install -y krita

echo "# krita" >> ~/.profile

echo "export KRITA_INSTALLED=1" >> ~/.profile