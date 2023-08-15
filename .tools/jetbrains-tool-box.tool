#!/usr/bin/env bash

set -x

if [ $JETBRAINS_TOOL_BOX_INSTALLED ];
then
    echo "jetbrains-tool-box is already installed."

    return 0
fi

function requires_fuse() {
    script_dir_path=$(dirname "$0")
    . $script_dir_path/../.sdks/fuse.sdk
}

requires_fuse

source ~/.profile

jetbrains_tool_box_version="2.0.2.16660"

jetbrains_tool_box_gz_path=/tmp/jetbrains-tool-box.tar.gz
jetbrains_tool_box_tar_path=/tmp/jetbrains-tool-box.tar
jetbrains_tool_box_tmp_dir_path=/tmp/jetbrains-tool-box
jetbrains_tool_box_dir_path=~/Documents/Tools/jetbrains-tool-box

wget https://download-cdn.jetbrains.com/toolbox/jetbrains-toolbox-$jetbrains_tool_box_version.tar.gz -O $jetbrains_tool_box_gz_path

if [ ! -d $jetbrains_tool_box_dir_path ];
then
    mkdir -p $jetbrains_tool_box_dir_path
fi

mkdir -p $jetbrains_tool_box_tmp_dir_path

rm -rf $jetbrains_tool_box_dir_path

gunzip $jetbrains_tool_box_gz_path

tar -xf $jetbrains_tool_box_tar_path -C $jetbrains_tool_box_tmp_dir_path

mv $jetbrains_tool_box_tmp_dir_path/jetbrains-toolbox-$jetbrains_tool_box_version $jetbrains_tool_box_dir_path

echo "# jetbrains-tool-box" >> ~/.profile

echo 'export PATH="$PATH:$jetbrains_tool_box_dir_path"' >> ~/.profile
echo "export JETBRAINS_TOOL_BOX_INSTALLED=1" >> ~/.profile