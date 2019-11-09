

import os
import shutil
import argparse

def create_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)

parser = argparse.ArgumentParser()
parser.add_argument('--batch_name', type=str)
args = parser.parse_args()



output_root = os.path.join("/home/kopi/local_git/dataset/processed", args.batch_name)
day = os.path.join(output_root, "day")
night = os.path.join(output_root, "night")

create_dir(output_root)
create_dir(day)
create_dir(night)
for c in ["draw", "images", "xmls"]:
    create_dir(os.path.join(day, c))
    create_dir(os.path.join(night, c))
