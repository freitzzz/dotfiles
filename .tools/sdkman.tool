#!/usr/env/bin bash

set -x

if [ ! $SDKMAN_INSTALLED ];
then
    wget -qO- https://get.sdkman.io | bash

    sdkman_init_snippet=$( cat << EOF
#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$SDKMAN_DIR_RAW"
[[ -s "${SDKMAN_DIR_RAW}/bin/sdkman-init.sh" ]] && source "${SDKMAN_DIR_RAW}/bin/sdkman-init.sh"
EOF
)
    echo "$sdkman_init_snippet" >> ~/.profile
    echo "export SDKMAN_INSTALLED=1" >> ~/.profile
else
    echo "sdkman is already installed."
fi