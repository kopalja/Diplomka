

from PIL import Image, ImageFont, ImageDraw
import numpy as np

from lxml import etree
import os
from os.path import isfile, join
from os import listdir
import tensorflow as tf
from shutil import copyfile

import cv2


colors = {
    "car": "red",
    "bicycle": "blue",
    "truck": "green",
    "bus": "green",
    "motorbike": "yellow"
}

def draw_boxes(image, predictions):
    im = image.copy()
    draw = ImageDraw.Draw(im)

    i = 0
    for prediction in predictions:
        text_origin = np.array([prediction[0], prediction[1] - 20])

        draw.rectangle([prediction[0], prediction[1], prediction[2], prediction[3]], outline=colors[prediction[4]])

        font = ImageFont.truetype(font='font/FiraMono-Medium.otf', size = 20)
        draw.text((prediction[0], prediction[1]), str(i), fill=(255, 0, 0), font = font)
        i += 1
    return im





def create_xml_object(bbox):
    obj = etree.Element("object")
    name = etree.Element("name")
    pose = etree.Element("pose")
    truncated = etree.Element("truncated")
    occluded = etree.Element("occluded")
    bndbox = etree.Element("bndbox")
    difficult = etree.Element("difficult")

    if bbox[4] =="bus":
        name.text = "truck"
    else:
        name.text = bbox[4]

    pose.text = "Unspecified"
    truncated.text = "0"
    occluded.text = "0"
    difficult.text = "0"

    xmin = etree.Element("xmin")
    ymin = etree.Element("ymin")
    xmax = etree.Element("xmax")
    ymax = etree.Element("ymax")
    xmin.text = str(bbox[0])
    ymin.text = str(bbox[1])
    xmax.text = str(bbox[2])
    ymax.text = str(bbox[3])
    bndbox.append(xmin)
    bndbox.append(ymin)
    bndbox.append(xmax)
    bndbox.append(ymax)

    obj.append(name)
    obj.append(pose)
    obj.append(truncated)
    obj.append(occluded)
    obj.append(bndbox)
    obj.append(difficult)
    return obj


def create_xml_file(xmls_folder, name, image_shape, predictions):
    path_name = os.path.join(xmls_folder, name + '.xml')
    print(path_name)
    file = open(path_name, 'wb+')


    root = etree.Element("annotation")

    # filename node
    filename_node = etree.Element("filename")
    filename_node.text = name + '.jpg'
    root.append(filename_node)

    #size node
    size = etree.Element("size")
    width = etree.Element("width")
    width.text = str(image_shape[0])
    height = etree.Element("height")
    height.text = str(image_shape[1])
    depth = etree.Element("depth")
    depth.text = "3"
    size.append(width)
    size.append(height)
    size.append(depth)
    root.append(size)


    for bbox in predictions:
        obj = create_xml_object(bbox)
        root.append(obj)

    st = etree.tostring(root, pretty_print=True)
    file.write(st)
    file.close()

def modify_predictions(command, predictions):
    cmds = command.split()
    side = 0
    if cmds[1] == "t":
        side = 1
    elif cmds[1] == "r":
        side = 2
    elif cmds[1] == "b":
        side = 3
    predictions[int(cmds[0])][side] += int(cmds[2])
    return predictions










    