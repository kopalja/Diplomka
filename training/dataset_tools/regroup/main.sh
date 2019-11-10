#!/bin/bash


### USAGE
# One parameter (path to processed folder)
# Delete, rename and redraw all files to update new changes

# Example ./main /home/kopi/local_git/dataset/processed/batch_2

cd "/home/kopi/diplomka/training/dataset_tools/regroup"

mkdir "$1/day/draw_tmp"
mkdir "$1/day/images_tmp"
mkdir "$1/day/xmls_tmp"

mkdir "$1/night/draw_tmp"
mkdir "$1/night/images_tmp"
mkdir "$1/night/xmls_tmp"

python regroup.py --root "$1"


rm -r "$1/day/draw"
rm -r "$1/day/images"
rm -r "$1/day/xmls"

rm -r "$1/night/draw"
rm -r "$1/night/images"
rm -r "$1/night/xmls"


mv "$1/day/draw_tmp" "$1/day/draw" 
mv "$1/day/images_tmp" "$1/day/images"
mv "$1/day/xmls_tmp" "$1/day/xmls"

mv "$1/night/draw_tmp" "$1/night/draw" 
mv "$1/night/images_tmp" "$1/night/images"
mv "$1/night/xmls_tmp" "$1/night/xmls"


echo "Change drawings"
rm -r "$1/day/draw"
rm -r "$1/night/draw"

mkdir "$1/day/draw"
mkdir "$1/night/draw"

python create_draw.py --root "$1/day"
python create_draw.py --root "$1/night"