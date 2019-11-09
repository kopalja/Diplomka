

from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
import numpy as np
from PIL import Image, ImageFont, ImageDraw

import tensorflow as tf
from lxml import etree

colors = {
    "car": "red",
    "bicycle": "blue",
    "truck": "green",
    "bus": "green",
    "motorbike": "yellow"
}


def recursive_parse_xml_to_dict(xml):
    if not xml:
        return {xml.tag: xml.text}
    result = {}
    for child in xml:
        child_result = recursive_parse_xml_to_dict(child)
        if child.tag != 'object':
            result[child.tag] = child_result[child.tag]
        else:
            if child.tag not in result:
                result[child.tag] = []
            result[child.tag].append(child_result[child.tag])
    return {xml.tag: result}


def draw_boxes(image, data):
    im = image.copy()
    draw = ImageDraw.Draw(im)

    i = 0
    for obj in data['object']:
        prediction = []
        prediction.append(float(obj['bndbox']['xmin']))
        prediction.append(float(obj['bndbox']['ymin']))
        prediction.append(float(obj['bndbox']['xmax']))
        prediction.append(float(obj['bndbox']['ymax']))

        text_origin = np.array([prediction[0], prediction[1] - 20])
        draw.rectangle([prediction[0], prediction[1], prediction[2], prediction[3]], outline=colors[obj['name']])

        #font = ImageFont.truetype(font='font/FiraMono-Medium.otf', size = 20)
        draw.text((prediction[0], prediction[1]), str(i), fill=(255, 0, 0))#, font = font)
        i += 1
    return im

#########################################################

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str)
args = parser.parse_args()

images_folder = os.path.join(args.root, 'images')
xmls_folder = os.path.join(args.root, 'xmls')
draw_folder = os.path.join(args.root, 'draw')


images_name = sorted([f for f in listdir(images_folder) if isfile(join(images_folder, f))])

for image_name in images_name:
    image_path = os.path.join(images_folder, image_name)
    xml_path = os.path.join(xmls_folder, image_name[:-4] + '.xml')

    with tf.gfile.GFile(xml_path, 'r') as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    data = recursive_parse_xml_to_dict(xml)['annotation']   
    draw = draw_boxes(Image.open(image_path), data)
    dest_draw_path = os.path.join(draw_folder, image_name)
    draw.save(dest_draw_path, "JPEG")
    # print(data)
    # exit()