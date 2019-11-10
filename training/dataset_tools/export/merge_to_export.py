
from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
from enum import Enum



def move_data(src_img, src_xml, dst_img, dst_xml):
    name_index = len([f for f in listdir(dst_xml) if isfile(join(dst_xml, f))])
    for image_name in [f for f in listdir(src_img) if isfile(join(src_img, f))]:
        name = 'my_' + str(name_index).zfill(6)
        shutil.copy(os.path.join(src_img, image_name), os.path.join(dst_img, name + '.jpg'))
        shutil.copy(os.path.join(src_xml, image_name[:-4] + '.xml'), os.path.join(dst_xml, name + '.xml'))
        name_index += 1      


class Data_Type(Enum):
    all_ = 'all'
    day = 'day'
    night = 'night'

parser = argparse.ArgumentParser()
parser.add_argument('--processed', type=str)
parser.add_argument('--exported', type=str)
parser.add_argument('--type', type=Data_Type, choices=list(Data_Type))
args = parser.parse_args()




images_day_folder = os.path.join(args.processed, 'day', 'images')
xmls_day_folder = os.path.join(args.processed, 'day', 'xmls')

images_night_folder = os.path.join(args.processed, 'night', 'images')
xmls_night_folder = os.path.join(args.processed, 'night', 'xmls')

dst_images_folder = os.path.join(args.exported, 'images')
dst_xmls_folder = os.path.join(args.exported, 'annotations', 'xmls')


# merge files
if args.type is Data_Type.all_ or args.type is Data_Type.day:
    move_data(images_day_folder, xmls_day_folder, dst_images_folder, dst_xmls_folder)

if args.type is Data_Type.all_ or args.type is Data_Type.night:
    move_data(images_night_folder, xmls_night_folder, dst_images_folder, dst_xmls_folder)

    