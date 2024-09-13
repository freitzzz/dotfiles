#!/usr/bin/env bash

dirs=(".config/awesome" ".config/rofi" ".config/picom" ".config/alacritty" ".config/aliases" ".local/bin")

for dir in ${dirs[@]}; do
    sudo mount --bind ~/$dir/ $dir
done
