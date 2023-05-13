#!/usr/env/bin bash

set -x

if [ ! $SDKMAN_INSTALLED ];
then
    wget -qO- https://get.sdkman.io | bash

    sdkman_init_snippet=$( cat << EOF
#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$SDKMAN_DIR/bin/sdkman-init.sh" ]] && source "$SDKMAN_DIR/bin/sdkman-init.sh"

export SDKMAN_INSTALLED=1
EOF
)
    echo "$sdkman_init_snippet" >> ~/.profile
else
    echo "sdkman is already installed."
fi