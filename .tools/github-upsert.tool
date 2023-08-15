#!/usr/bin/env bash

set -x

if [ $GITHUB_UPSERT_INSTALLED ];
then
    echo "github-upsert is already installed."

    return 0
fi

function requires_node() {
    script_dir_path=$(dirname "$0")
    . $script_dir_path/../.sdks/node.sdk
}

requires_node

sudo npm install -g @web-pacotes/github-upsert

echo "# github-upsert" >> ~/.profile

echo "export GITHUB_UPSERT_INSTALLED=1" >> ~/.profile