#!/usr/bin/env bash

set -x

if [ $HUGO_INSTALLED ];
then
    echo "Hugo is already installed."

    return 0
fi

apt-get install -y hugo

echo "# Hugo" >> ~/.profile

echo "export HUGO_INSTALLED=1" >> ~/.profile