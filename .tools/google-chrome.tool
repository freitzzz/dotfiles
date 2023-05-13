#!/usr/env/bin bash

set -x

if [ $GOOGLE_CHROME_INSTALLED ];
then
    echo "Google Chrome is already installed."

    return 0
fi

google_chrome_dep_path=/tmp/google-chrome.deb

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O $google_chrome_dep_path

apt-get install -y $google_chrome_dep_path

echo "# Google Chrome" >> ~/.profile

echo "export GOOGLE_CHROME_INSTALLED=1" >> ~/.profile