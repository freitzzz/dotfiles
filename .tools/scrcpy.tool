#!/usr/bin/env bash

set -x

if [ $SCRCPY_INSTALLED ];
then
    echo "scrcpy is already installed."

    return 0
fi

wget -qO- https://gist.githubusercontent.com/freitzzz/a432ef8303108ca525601bacb81a7b1b/raw/scrcpy_install.bash | bash

echo "# scrcpy" >> ~/.profile

echo "export SCRCPY_INSTALLED=1" >> ~/.profile