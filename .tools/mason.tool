#!/usr/env/bin bash

set -x

if [ $MASON_INSTALLED ];
then
    echo "Mason is already installed."

    return 0
fi

function requires_flutter() {
    script_dir_path=$(dirname "$0")
    . $script_dir_path/../.sdks/flutter.sdk
}

requires_flutter

source ~/.profile

dart pub global activate mason_cli

echo "# Mason" >> ~/.profile

echo "export MASON_INSTALLED=1" >> ~/.profile