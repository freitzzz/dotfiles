#!/usr/env/bin bash

set -x

if [ $OH_MY_BASH_INSTALLED ];
then
    echo "Oh My Bash is already installed."

    return 0
fi

bash -c "$(wget https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh -O -)"

echo "source ~/.bash_aliases" >> ~/.bashrc
echo 'OSH_THEME="rr"' >> ~/.bashrc
echo 'EDITOR="nano"' >> ~/.bashrc

echo "# Oh My Bash" >> ~/.profile

echo "export OH_MY_BASH_INSTALLED=1" >> ~/.profile