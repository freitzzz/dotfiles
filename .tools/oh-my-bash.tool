#!/usr/env/bin bash

set -x

bash -c "$(wget https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh -O -)"

echo "source ~/.bash_aliases" >> ~/.bashrc
echo 'OSH_THEME="rr"' >> ~/.bashrc
echo 'EDITOR="nano"' >> ~/.bashrc
