


from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils

from os import listdir
from os.path import isfile, join
from PIL import Image
from PIL import ImageDraw
import argparse
import os

import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.common import mkdir, All_Day_Night, get_files, parse_xml_to_dict


def resize_and_copy_images(src_folder, dst_folder, width, height):
    for image_name in get_files(src_folder):
        image_path = os.path.join(src_folder, image_name)
        im = Image.open(image_path)
        im.thumbnail((width, height), Image.ANTIALIAS)
        im.save(os.path.join(dst_folder, image_name), "JPEG")


def generate_txts(src_folder, dst_folder, width, height):
    # private function
    def rescale(pos, or_size, new_size):
        return int((int(pos) / or_size) * new_size)

    for xml_name in get_files(src_folder):
        detections_file = open(os.path.join(dst_folder, xml_name[:-4]  + '.txt'), 'w+')
        data = parse_xml_to_dict(os.path.join(src_folder, xml_name))['annotation']

        or_width, or_height = int(data['size']['width']), int(data['size']['height'])
        for obj in data['object']:
            xmin = rescale(obj['bndbox']['xmin'], or_width, width)
            ymin = rescale(obj['bndbox']['ymin'], or_height, height)
            xmax = rescale(obj['bndbox']['xmax'], or_width, width)
            ymax = rescale(obj['bndbox']['ymax'], or_height, height)
            detections_file.write("{0} {1} {2} {3} {4} \n".format(obj['name'], xmin, ymin, xmax, ymax))
        detections_file.close()
            



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type = All_Day_Night, choices=list(All_Day_Night))
    parser.add_argument('--width', type = int)
    parser.add_argument('--height', type = int)
    args = parser.parse_args()

    testing_name = args.type.value + '_' + str(args.width) + 'x' + str(args.height)
    testing_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing/exported', testing_name)



    # prepare testing tree
    dst_images_folder = os.path.join(testing_folder, 'images')
    dst_txts_folder = os.path.join(testing_folder, 'txts')
    mkdir(testing_folder)
    mkdir(dst_images_folder)
    mkdir(dst_txts_folder)

    # copy images
    src_data_folder = os.path.join(os.environ['LOCAL_GIT'], 'testing/data')

    if args.type is All_Day_Night.all_ or args.type is All_Day_Night.day:
        resize_and_copy_images(os.path.join(src_data_folder, 'day', 'images'), dst_images_folder, args.width, args.height)
        generate_txts(os.path.join(src_data_folder, 'day', 'xmls'), dst_txts_folder, args.width, args.height)


    if args.type is All_Day_Night.all_ or args.type is All_Day_Night.night:
        resize_and_copy_images(os.path.join(src_data_folder, 'night', 'images'), dst_images_folder, args.width, args.height)
        generate_txts(os.path.join(src_data_folder, 'night', 'xmls'), dst_txts_folder, args.width, args.height)






