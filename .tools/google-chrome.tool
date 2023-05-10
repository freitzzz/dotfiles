#!/usr/env/bin bash

set -x

google_chrome_dep_path=/tmp/google-chrome.deb

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o $google_chrome_dep_path

apt-get install -y $google_chrome_dep_path