#!/usr/bin/env bash

set -x

if [ $WIRESHARK_INSTALLED ];
then
    echo "wireshark is already installed."

    return 0
fi

apt-get install -y wireshark

echo "# wireshark" >> ~/.profile

echo "export WIRESHARK_INSTALLED=1" >> ~/.profile