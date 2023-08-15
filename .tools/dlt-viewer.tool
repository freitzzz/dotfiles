#!/usr/env/bin bash

set -x

if [ $DLT_VIEWER_INSTALLED ];
then
    echo "dlt-viewer is already installed."

    return 0
fi

wget -qO- https://gist.githubusercontent.com/freitzzz/a36a60cd9cc923a30af9699e388bc061/raw/dlt_viewer_install.bash | bash

echo "# dlt-viewer" >> ~/.profile

echo "export DLT_VIEWER_INSTALLED=1" >> ~/.profile