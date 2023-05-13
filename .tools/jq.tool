#!/usr/env/bin bash

set -x

if [ $JQ_INSTALLED ];
then
    echo "jq is already installed."

    return 0
fi

apt-get install -y jq

echo "# jq" >> ~/.profile

echo "export JQ_INSTALLED=1" >> ~/.profile