#!/usr/env/bin bash

set -x

if [ $SQLITE_BROWSER_INSTALLED ];
then
    echo "SQLite Browser is already installed."

    return 0
fi

apt-get install -y sqlitebrowser

echo "# SQLite Browser" >> ~/.profile

echo "export SQLITE_BROWSER_INSTALLED=1" >> ~/.profile