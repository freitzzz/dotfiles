#!/usr/bin/env bash

set -x

if [ $GHIDRA_INSTALLED ];
then
    echo "ghidra is already installed."

    return 0
fi

ghidra_version="10.3.2"
ghidra_build_date="20230711"

ghidra_zip_path="/tmp/ghidra-$ghidra_version-$ghidra_build_date"
ghidra_dir_path=~/Documents/Tools/ghidra
ghidra_bin_path="$ghidra_dir_path/ghidra_$ghidra_version_PUBLIC"

wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_$ghidra_version_build/ghidra_$ghidra_versionPUBLIC_$ghidra_build_date.zip -O $ghidra_zip_path

unzip -o $ghidra_zip_path -d $ghidra_dir_path

echo "# ghidra" >> ~/.profile

path_literal='$PATH'

echo "export PATH=$path_literal:$ghidra_bin_path" >> ~/.profile
echo "export GHIDRA_INSTALLED=1" >> ~/.profile
