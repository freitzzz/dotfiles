#!/usr/bin/env bash

dirs=(".config/awesome" ".config/rofi" ".local/bin")

for dir in ${dirs[@]}; do
    sudo mount --bind ~/$dir/ $dir
done
