import sys
sys.path.append('/home/kopi/stuff/annotator/ffmpeg-4.2.1')



import time

import argparse
import platform
import subprocess
from os.path import isfile, join
from os import listdir
from PIL import Image
from PIL import ImageDraw
import cv2

from os.path import isfile, join
from os import listdir
import os

import  ffmpeg 

def check_rotation(path_video_file):
    # this returns meta-data of the video file in form of a dictionary
    meta_dict = ffmpeg.probe(path_video_file)

    # from the dictionary, meta_dict['streams'][0]['tags']['rotate'] is the key
    # we are looking for
    rotateCode = None
    rotate = meta_dict.get('streams', [dict(tags=dict())])[0].get('tags', dict()).get('rotate', 0)
    if rotate == 0:
        return None

    if int(meta_dict['streams'][0]['tags']['rotate']) == 90:
        rotateCode = cv2.ROTATE_90_CLOCKWISE
    elif int(meta_dict['streams'][0]['tags']['rotate']) == 180:
        rotateCode = cv2.ROTATE_180
    elif int(meta_dict['streams'][0]['tags']['rotate']) == 270:
        rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE

    return rotateCode

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str)
parser.add_argument('--frame', type=int, default=60)
args = parser.parse_args()



images_folder = os.path.join(args.root, "raw_images")

for category in ["cloudy", "dark", "sunny"]:
#for category in ["rainy", "rainy2"]:
    videos_folder = os.path.join(args.root, "raw_footage", category)
    videos_names = [f for f in listdir(videos_folder) if isfile(join(videos_folder, f))]



    start_index = len([f for f in listdir(images_folder) if isfile(join(images_folder, f))])
    created_images = 0
    for video in videos_names:
        video_path = os.path.join(videos_folder, video)

        #print(video_path)
        vidcap = cv2.VideoCapture(video_path)
        rotateCode = check_rotation(video_path)

        i = 0
        success = True
        while success:
            success, img = vidcap.read()
            i += 1
            if not success:
                break

            if rotateCode is not None:
                img = cv2.rotate(img, rotateCode) 

            if i % args.frame == 0:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
                image = Image.fromarray(img)
                image_name = "my_" + str(start_index + created_images).zfill(6) + ".jpg";
                image.save(images_folder + '/' + image_name)
                created_images += 1


