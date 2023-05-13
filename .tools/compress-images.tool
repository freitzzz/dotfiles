#!/usr/env/bin bash

set -x

if [ $COMPRESS_IMAGES_INSTALLED ];
then
    echo "compress-images is already installed."

    return 0
fi

compress_images_functions=$( cat << EOF
export function compress_images() {
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

export function compress_images_png() {
    compress_images ".png"
}

export function compress_images_jpg() {
    compress_images ".jpg"
}

export function compress_images_jpeg() {
    compress_images ".jpeg"
}
EOF
)

echo "# compress-images" >> ~/.profile

echo $compress_images_functions >> ~/.profile

echo "export COMPRESS_IMAGES_INSTALLED=1" >> ~/.profile