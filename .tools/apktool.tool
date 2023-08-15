#!/usr/bin/env bash

set -x

if [ $APKTOOL_INSTALLED ];
then
    echo "apktool is already installed."

    return 0
fi

apktool_version="2.7.0"

apktool_dir_path=~/Documents/Tools/apktool
apktool_wrapper_path="$apktool_dir_path/apktool"
apktool_jar_path="$apktool_dir_path/apktool.jar"

if [ ! -d $apktool_dir_path ];
then
    mkdir -p $apktool_dir_path
fi

wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O $apktool_wrapper_path
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_$apktool_version.jar -O $apktool_jar_path

chmod +x $apktool_wrapper_path
chmod +x $apktool_jar_path

sudo cp $apktool_wrapper_path /usr/local/bin
sudo cp $apktool_jar_path /usr/local/bin

echo "# apktool" >> ~/.profile

echo "export APKTOOL_INSTALLED=1" >> ~/.profile