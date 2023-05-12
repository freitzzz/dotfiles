#!/usr/env/bin bash

set -x

if ! command -v sdk >/dev/null 2>&1;
then
    wget -qO- https://get.sdkman.io | bash
else
    echo "sdkman is already installed."
fi