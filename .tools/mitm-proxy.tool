#!/usr/env/bin bash

set -x

if [ $MITM_PROXY_INSTALLED ];
then
    echo "mitm-proxy is already installed."

    return 0
fi

mitm_proxy_version="10.0.0"

mitm_proxy_gz_path=/tmp/mitm-proxy.tar.gz
mitm_proxy_tar_path=/tmp/mitm-proxy.tar
mitm_proxy_tmp_dir_path=/tmp/mitm-proxy
mitm_proxy_dir_path=~/Documents/Tools/mitm-proxy

wget https://downloads.mitmproxy.org/$mitm_proxy_version/mitmproxy-$mitm_proxy_version-linux.tar.gz -O $mitm_proxy_gz_path

if [ ! -d $mitm_proxy_dir_path ];
then
    mkdir -p $mitm_proxy_dir_path
fi

mkdir -p $mitm_proxy_tmp_dir_path

rm -rf $mitm_proxy_dir_path

gunzip $mitm_proxy_gz_path

tar -xf $mitm_proxy_tar_path -C $mitm_proxy_tmp_dir_path

mv $mitm_proxy_tmp_dir_path/android-studio $mitm_proxy_dir_path

echo "# mitm-proxy" >> ~/.profile

echo 'export PATH="$PATH:$mitm_proxy_dir_path"' >> ~/.profile
echo "export MITM_PROXY_INSTALLED=1" >> ~/.profile