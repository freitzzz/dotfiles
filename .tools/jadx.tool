#!/usr/env/bin bash

set -x

jadx_zip_path=/tmp/jadx.zip
jadx_dir_path=~/Documents/Tools/jadx

wget https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip -O $jadx_zip_path

if [ ! -d $jadx_dir_path ];
then
    mkdir -p $jadx_dir_path
fi

unzip $jadx_zip_path -d $jadx_dir_path

echo "# Jadx" >> ~/.profile
echo "" >> ~/.profile
echo "JADX_ROOT=$jadx_dir_path" >> ~/.profile
echo 'export PATH="$PATH:$JADX_ROOT/bin"'