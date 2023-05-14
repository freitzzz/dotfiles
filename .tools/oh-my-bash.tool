#!/usr/env/bin bash

set -x

if [ $OH_MY_BASH_INSTALLED ];
then
    echo "Oh My Bash is already installed."

    return 0
fi

wget -qO- https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh | bash

sed -i 's/OSH_THEME.*/OSH_THEME="rr"/g' ~/.bashrc

echo 'export EDITOR="nano"' >> ~/.bashrc
echo "source ~/.bash_aliases" >> ~/.bashrc

echo "# Oh My Bash" >> ~/.profile

echo "export OH_MY_BASH_INSTALLED=1" >> ~/.profile