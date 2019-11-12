
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils

from os import listdir
from os.path import isfile, join
from PIL import Image
from PIL import ImageDraw
import os
import argparse
import sys
sys.path.insert(0, os.environ['PROJECT_ROOT'])
from python_tools.common import get_files, mkdir



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type = str)
    parser.add_argument('--testing_data', type = str)
    parser.add_argument('--output_dir', type = str, default = 'model_detection_txts')
    args = parser.parse_args()

    engine = DetectionEngine(args.model_path)
    labels = dataset_utils.ReadLabelFile("vehicles_labels.txt")
    allowed_objects = ["car", "motorcycle", "motorbike", "bus", "truck", "bicycle"]
    images_path = os.path.join(args.testing_data, 'images')
    mkdir(args.output_dir, force = True)

    for image_name in get_files(images_path):
        image = Image.open(os.path.join(images_path, image_name))

        # Run inference.
        ans = engine.DetectWithImage(image, threshold=0.0, keep_aspect_ratio=False, relative_coord=False, top_k=10)

        if ans:
            detections_file = open(os.path.join(args.output_dir, image_name[:-4]  + '.txt'), 'w+')
            for obj in ans:
                if labels[obj.label_id] in allowed_objects:
                    name = labels[obj.label_id]
                    if name == "motorcycle":
                        name = "motorbike"
                    elif name == "bus":
                        name = "truck"
                    box = obj.bounding_box.flatten().tolist()
                    detections_file.write("{0} {1} {2} {3} {4} {5} \n".format(name, obj.score, round(box[0]), round(box[1]), round(box[2]), round(box[3])))
            detections_file.close()




