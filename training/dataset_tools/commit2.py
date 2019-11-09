from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str)
args = parser.parse_args()


#root = "/home/kopi/stuff/annotator"

images_folder = os.path.join(args.root, 'images')
xmls_folder = os.path.join(args.root, 'xmls')
draw_folder = os.path.join(args.root, 'draw')

dst_images_folder = os.path.join(args.root, 'images2')
dst_xmls_folder = os.path.join(args.root, 'xmls2')
dst_draw_folder = os.path.join(args.root, 'draw2')

name_index = len([f for f in listdir(dst_images_folder) if isfile(join(dst_images_folder, f))])


images_name = sorted([f for f in listdir(images_folder) if isfile(join(images_folder, f))])


# #copy files
# for image_name in images_name:
#     or_name = image_name[:-4]
#     name = 'my_' + str(name_index).zfill(6)
#     shutil.copy(os.path.join(images_folder, or_name + '.jpg'), os.path.join(dst_images_folder, name + '.jpg'))
#     shutil.copy(os.path.join(xmls_folder, or_name + '.xml'), os.path.join(dst_xmls_folder, name + '.xml'))
#     name_index += 1  


#copy files
for image_name in images_name:
    or_name = image_name[:-4]
    name = 'my_' + str(name_index).zfill(6)
    shutil.copy(os.path.join(images_folder, or_name + '.jpg'), os.path.join(dst_images_folder, name + '.jpg'))
    shutil.copy(os.path.join(xmls_folder, or_name + '.xml'), os.path.join(dst_xmls_folder, name + '.xml'))
    shutil.copy(os.path.join(draw_folder, or_name + '.jpg'), os.path.join(dst_draw_folder, name + '.jpg'))
    name_index += 1  




# remove files
# for image_name in images_name:
#     name = image_name[:-4]
#     os.remove(os.path.join(images_folder, name + '.jpg'))
#     try:
#         os.remove(os.path.join(draw_folder, name + '.jpg'))
#     except:
#         pass
#     os.remove(os.path.join(xmls_folder, name + '.xml'))

    