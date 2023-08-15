#!/usr/bin/env bash

set -x

if [ $WEBP_INSTALLED ];
then
    echo "webp is already installed."

    return 0
fi

apt-get install -y webp

echo "# webp" >> ~/.profile

echo "export WEBP_INSTALLED=1" >> ~/.profile