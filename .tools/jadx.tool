#!/usr/bin/env bash

set -x

if [ $JADX_INSTALLED ];
then
    echo "Jadx is already installed."

    return 0
fi

jadx_zip_path=/tmp/jadx.zip
jadx_dir_path=~/Documents/Tools/jadx

wget https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip -O $jadx_zip_path

if [ ! -d $jadx_dir_path ];
then
    mkdir -p $jadx_dir_path
fi

unzip -o $jadx_zip_path -d $jadx_dir_path

echo "# Jadx" >> ~/.profile
echo "" >> ~/.profile
echo "JADX_ROOT=$jadx_dir_path" >> ~/.profile
echo 'export PATH="$PATH:$JADX_ROOT/bin"' >> ~/.profile

echo "export JADX_INSTALLED=1" >> ~/.profile