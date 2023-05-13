#!/usr/env/bin bash

set -x

android_studio_gz_path=/tmp/studio.tar.gz
android_studio_tar_path=/tmp/*android-studio*.tar
android_studio_dir_path=~/Documents/Tools/android-studio

wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2022.2.1.19/android-studio-2022.2.1.19-linux.tar.gz -O $android_studio_gz_path

if [ ! -d $android_studio_dir_path ];
then
    mkdir -p $android_studio_path
fi

gunzip $android_studio_gz_path

tar -xf $android_studio_tar_path -C $android_studio_dir_path

echo "# Android Studio" >> ~/.profile
echo "export ANDROID_STUDIO_ROOT=$android_studio_dir_path" >> ~/.profile
echo 'export PATH="$PATH:$ANDROID_STUDIO_ROOT/bin"' >> ~/.profile