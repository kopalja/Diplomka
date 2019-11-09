#/bin/bash

python video_to_images.py --root "/media/kopi/24F4-9A50/data"
cd keras-yolo3
python yolo_video.py --root "/media/kopi/24F4-9A50/data"
