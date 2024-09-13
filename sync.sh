#!/usr/bin/env bash

dirs=(".config/awesome" ".config/rofi" ".config/picom" ".config/alacritty" ".local/bin" ".fonts")

for dir in ${dirs[@]}; do
    sudo mount --bind ~/$dir/ $dir
done
