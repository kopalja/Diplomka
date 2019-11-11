


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



from tools.Day_night_enum import Data_Type




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--processed', type=str)
    parser.add_argument('--ex', type=str)
    parser.add_argument('--type', type=Data_Type, choices=list(Data_Type))
    args = parser.parse_args()
    print(args.ex)
    exit()


    engine = DetectionEngine("300_edgetpu.tflite")

    #engine = DetectionEngine("retrain_64_edgetpu.tflite")

    labels = dataset_utils.ReadLabelFile("vehicles_labels.txt")




    allowed_objects = ["car", "motorcycle", "motorbike", "bus", "truck", "bicycle"]

    mypath = "/home/kopi/python_root/Diplomka/mAP_testing"
    images_path = os.path.join(mypath, "images")
    detections_path = os.path.join(mypath, "detection-results")
    onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]


    for image_name in onlyfiles:
        image_path = os.path.join(images_path, image_name)
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        detections_file = open(os.path.join(detections_path, image_name[:-4]  + '.txt'), 'w+')
        # Run inference.
        ans = engine.DetectWithImage(image, threshold=0.0, keep_aspect_ratio=False, relative_coord=False, top_k=10)

        if ans:
            for obj in ans:
                #print(obj.label_id)
                if labels[obj.label_id] in allowed_objects:
                    name = labels[obj.label_id]
                    if name == "motorcycle":
                        name = "motorbike"
                    elif name == "bus":
                        name = "truck"
                    box = obj.bounding_box.flatten().tolist()
                    detections_file.write("{0} {1} {2} {3} {4} {5} \n".format(name, obj.score, round(box[0]), round(box[1]), round(box[2]), round(box[3])))
                    #draw.rectangle(box, outline='red')
        #image.show()
        detections_file.close()
        #exit()
