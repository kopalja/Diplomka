from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str)
args = parser.parse_args()


#root = "/home/kopi/stuff/annotator"

draw_folder = os.path.join(args.root, 'tmp', 'draw')
images_folder = os.path.join(args.root, 'tmp', 'images')
xmls_folder = os.path.join(args.root, 'tmp', 'xmls')
dst_images_folder = os.path.join(args.root, 'dataset', 'images')
dst_xmls_folder = os.path.join(args.root, 'dataset', 'xmls')

name_index = len([f for f in listdir(dst_images_folder) if isfile(join(dst_images_folder, f))])


draw_names = [f for f in listdir(draw_folder) if isfile(join(draw_folder, f))]
images_name = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]


#copy files
for draw_name in draw_names:
    or_name = draw_name[:-4]
    name = 'my_' + str(name_index).zfill(6)
    shutil.copy(os.path.join(images_folder, or_name + '.jpg'), os.path.join(dst_images_folder, name + '.jpg'))
    shutil.copy(os.path.join(xmls_folder, or_name + '.xml'), os.path.join(dst_xmls_folder, name + '.xml'))
    name_index += 1  


# remove files
for image_name in images_name:
    name = image_name[:-4]
    os.remove(os.path.join(images_folder, name + '.jpg'))
    try:
        os.remove(os.path.join(draw_folder, name + '.jpg'))
    except:
        pass
    os.remove(os.path.join(xmls_folder, name + '.xml'))

    