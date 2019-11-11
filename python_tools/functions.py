
import shutil
import os

def mkdir(path, force = False):
    try:
        os.mkdir(path)
    except FileExistsError:
        if force:
            shutil.rmtree(path)
            os.mkdir(path)




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