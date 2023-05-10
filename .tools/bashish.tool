#!/usr/env/bin bash

set -x

bashish_dir_path=~/Documents/Tools/bashish

git clone https://github.com/freitzzz/bashish $bashish_dir_path

(cd $bashish_dir_path; bash autogen.sh)