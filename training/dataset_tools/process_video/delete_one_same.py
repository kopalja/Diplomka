

from os.path import isfile, join
from os import listdir
import os
import shutil
import argparse
import numpy as np
from PIL import Image, ImageFont, ImageDraw

import tensorflow as tf
from lxml import etree




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


def check_validation(data):
    x = 0
    if not 'object' in data:
        return False
    if len(data['object']) > 11:
        return False

    w = np.ones(1921)
    for obj in data['object']:
        if w[int(obj['bndbox']['xmin'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['xmin'])] = 0
    w = np.ones(1921)
    for obj in data['object']:
        if w[int(obj['bndbox']['xmax'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['xmax'])] = 0
    w = np.ones(1081)
    for obj in data['object']:
        if w[int(obj['bndbox']['ymin'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['ymin'])] = 0
    w = np.ones(1081)
    for obj in data['object']:
        if w[int(obj['bndbox']['ymax'])] == 0:
            #return False
            x += 1
        w[int(obj['bndbox']['ymax'])] = 0

    if x > 3:
        return False
    return True

#########################################################

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str)
args = parser.parse_args()


day_folder = os.pardir.join(args.root, 'day')
night_folder = os.pardir.join(args.root, 'night')

for category_root in [day_folder, night_folder]:

    draw_folder = os.path.join(category_root, 'draw')
    xmls_folder = os.path.join(category_root, 'xmls')

    xmls_name = sorted([f for f in listdir(xmls_folder) if isfile(join(xmls_folder, f))])
    for xml_name in xmls_name:
        draw_path = os.path.join(draw_folder, xml_name[:-4] + '.xml')
        xml_path = os.path.join(xmls_folder, xml_name)

        with tf.gfile.GFile(xml_path, 'r') as fid:
            xml_str = fid.read()
        xml = etree.fromstring(xml_str)
        data = recursive_parse_xml_to_dict(xml)['annotation']   
        if check_validation(data) == False:
            # #print(image_name)
            # im = Image.open(image_path)
            # im.show()
            # aaa = input()
            # x += 1
            # # exit()
            os.remove(draw_folder)



