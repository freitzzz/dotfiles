#!/usr/bin/env bash

set -x

if [ $VSCODE_INSTALLED ];
then
    echo "VS Code is already installed."

    return 0
fi

vscode_deb_path=/tmp/vscode.deb

wget https://go.microsoft.com/fwlink/?LinkID=760868 -O $vscode_deb_path

apt-get install -y $vscode_deb_path

echo "# VS Code" >> ~/.profile

echo "export VSCODE_INSTALLED=1" >> ~/.profile
