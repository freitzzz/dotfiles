#!/usr/bin/env bash

set -x

if [ $COMPRESS_IMAGES_INSTALLED ];
then
    echo "compress-images is already installed."

    return 0
fi

compress_images_functions=$( cat << EOF
function compress_images() {
    images_path="*.png"

    if ! [[ -z "$1" ]];
    then
        echo images_path=$1
    fi

    for file in $images_path     
    do
        cwebp -q 80 "$file" -o "${file%.*}.webp"
    done
}

function compress_images_png() {
    compress_images ".png"
}

function compress_images_jpg() {
    compress_images ".jpg"
}

function compress_images_jpeg() {
    compress_images ".jpeg"
}

export -f compress_images
export -f compress_images_png
export -f compress_images_jpg
export -f compress_images_jpeg
EOF
)

echo "# compress-images" >> ~/.profile

echo "$compress_images_functions" >> ~/.profile

echo "export COMPRESS_IMAGES_INSTALLED=1" >> ~/.profile