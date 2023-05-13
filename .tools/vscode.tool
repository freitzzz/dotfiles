#!/usr/env/bin bash

set -x

vscode_deb_path=/tmp/vscode.deb

wget https://go.microsoft.com/fwlink/?LinkID=760868 -O $vscode_deb_path

apt-get install -y $vscode_deb_path