#!/usr/env/bin bash

set -x

if [ $ANDROID_STUDIO_INSTALLED ];
then
    echo "Android Studio is already installed."

    return 0
fi

android_studio_version="2022.2.1.19"

android_studio_gz_path=/tmp/studio.tar.gz
android_studio_tar_path=/tmp/studio.tar
android_studio_tmp_dir_path=/tmp/android-studio
android_studio_dir_path=~/Documents/Tools/android-studio

wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/$android_studio_version/android-studio-$android_studio_version-linux.tar.gz -O $android_studio_gz_path

if [ ! -d $android_studio_dir_path ];
then
    mkdir -p $android_studio_dir_path
fi

mkdir -p $android_studio_tmp_dir_path

rm -rf $android_studio_dir_path

gunzip $android_studio_gz_path

tar -xf $android_studio_tar_path -C $android_studio_tmp_dir_path

mv $android_studio_tmp_dir_path $android_studio_dir_path

echo "# Android Studio" >> ~/.profile
echo "export ANDROID_STUDIO_ROOT=$android_studio_dir_path" >> ~/.profile
echo 'export PATH="$PATH:$ANDROID_STUDIO_ROOT/bin"' >> ~/.profile

echo "export ANDROID_STUDIO_INSTALLED=1" >> ~/.profile
