
import shutil
import os
from enum import Enum
from os import listdir
from os.path import isfile, join

class All_Day_Night(Enum):
    all_ = 'all'
    day = 'day'
    night = 'night'


# Force delete folder if exist
def mkdir(path, force = False):
    try:
        os.mkdir(path)
    except FileExistsError:
        if force:
            shutil.rmtree(path)
            os.mkdir(path)



def parse_xml_to_dict(xml_path):
    # private
    def recursive_parse_xml_to_dict(xml):
        if not len(xml):
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

    import tensorflow as tf
    from lxml import etree
    with tf.gfile.GFile(xml_path, 'r') as fid:
        xml_str = fid.read()
    xml = etree.fromstring(xml_str)
    return recursive_parse_xml_to_dict(xml)




def get_files(dir):
    return [f for f in listdir(dir) if isfile(join(dir, f))]