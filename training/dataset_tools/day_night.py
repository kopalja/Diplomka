


from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
from PIL import Image
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str)
args = parser.parse_args()


#root = "/home/kopi/stuff/annotator"

images_folder = os.path.join(args.root, 'images')
xmls_folder = os.path.join(args.root, 'xmls')
draw_folder = os.path.join(args.root, 'draw')

dst_day_images_folder = os.path.join(args.root, 'day', 'images')
dst_day_xmls_folder = os.path.join(args.root, 'day', 'xmls')
dst_day_draw_folder = os.path.join(args.root, 'day', 'draw')

dst_night_images_folder = os.path.join(args.root, 'night', 'images')
dst_night_xmls_folder = os.path.join(args.root, 'night', 'xmls')
dst_night_draw_folder = os.path.join(args.root, 'night', 'draw')

name_index = 0 # len([f for f in listdir(dst_images_folder) if isfile(join(dst_images_folder, f))])


images_name = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]


# #copy files
# for image_name in images_name:
#     or_name = image_name[:-4]
#     name = 'my_' + str(name_index).zfill(6)
#     shutil.copy(os.path.join(images_folder, or_name + '.jpg'), os.path.join(dst_images_folder, name + '.jpg'))
#     shutil.copy(os.path.join(xmls_folder, or_name + '.xml'), os.path.join(dst_xmls_folder, name + '.xml'))
#     name_index += 1  


def copy_files(name, day):
    if day:
        shutil.copy(os.path.join(images_folder, name + '.jpg'), os.path.join(dst_day_images_folder, name + '.jpg'))
        shutil.copy(os.path.join(xmls_folder, name + '.xml'), os.path.join(dst_day_xmls_folder, name + '.xml'))
        shutil.copy(os.path.join(draw_folder, name + '.jpg'), os.path.join(dst_day_draw_folder, name + '.jpg'))
    else:
        shutil.copy(os.path.join(images_folder, name + '.jpg'), os.path.join(dst_night_images_folder, name + '.jpg'))
        shutil.copy(os.path.join(xmls_folder, name + '.xml'), os.path.join(dst_night_xmls_folder, name + '.xml'))
        shutil.copy(os.path.join(draw_folder, name + '.jpg'), os.path.join(dst_night_draw_folder, name + '.jpg'))


#copy files
for image_name in images_name:
    image_path = os.path.join(images_folder, image_name)
    img = Image.open(image_path).convert('LA')
    img_ar = np.asarray(img)
    copy_files(image_name[:-4],  np.mean(img_ar) > 164)





    # or_name = image_name[:-4]
    # name = 'my_' + str(name_index).zfill(6)
    # shutil.copy(os.path.join(images_folder, or_name + '.jpg'), os.path.join(dst_images_folder, name + '.jpg'))
    # shutil.copy(os.path.join(xmls_folder, or_name + '.xml'), os.path.join(dst_xmls_folder, name + '.xml'))
    # shutil.copy(os.path.join(draw_folder, or_name + '.jpg'), os.path.join(dst_draw_folder, name + '.jpg'))
    # name_index += 1  




# remove files
# for image_name in images_name:
#     name = image_name[:-4]
#     os.remove(os.path.join(images_folder, name + '.jpg'))
#     try:
#         os.remove(os.path.join(draw_folder, name + '.jpg'))
#     except:
#         pass
#     os.remove(os.path.join(xmls_folder, name + '.xml'))

    