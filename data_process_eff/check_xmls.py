import xml.etree.ElementTree as ET
import os
import glob
from tqdm import tqdm
import argparse
'''
Check xml files and rectify invalid annotations.

example:
python check_xmls.py --xml_path=your_xml_path
'''

parser = argparse.ArgumentParser()

parser.add_argument("--xml_path", default="",
                    type=str, help='root path of xmls')
args = parser.parse_args()

if args.xml_path is None:
    raise ValueError('[Error] Path of xmls can not be None!')
if not os.path.exists(args.xml_path):
    raise ValueError('[Error] Path of xmls can not be found! Please check: {}'.format(args.xml_path))


all_xmls = glob.glob(os.path.join(args.xml_path, '*.xml'))

print('xml path:{}'.format(args.xml_path))
print('{} xmls are found.'.format(len(all_xmls)))

invalid_xmls = []

with tqdm(all_xmls) as pbar:


    for item in pbar:
        tree = ET.parse(item)
        root = tree.getroot()

        size_node = root.find('size')
        h = int(size_node.find('height').text)
        w = int(size_node.find('width').text)

        object_nodes = root.findall('object')

        is_invalid = False
        for obj_node in object_nodes:
            xmin = int(obj_node.find('bndbox').find('xmin').text)
            ymin = int(obj_node.find('bndbox').find('ymin').text)
            xmax = int(obj_node.find('bndbox').find('xmax').text)
            ymax = int(obj_node.find('bndbox').find('ymax').text)

            if xmin <= 0:
                obj_node.find('bndbox').find('xmin').text = str('1')
                is_invalid = True
            elif ymin <= 0:
                obj_node.find('bndbox').find('ymin').text = str('1')
                is_invalid = True
            elif xmax >= w:
                obj_node.find('bndbox').find('xmax').text = str(w - 1)
                is_invalid = True
            elif ymax >= h:
                obj_node.find('bndbox').find('ymax').text = str(h - 1)
                is_invalid = True

        if is_invalid:
            invalid_xmls.append(item)

        # update xmls
        tree.write(item)

    pbar.close()


# log invalid xmls
print('===='*20)
if len(invalid_xmls) > 0:
    print('Invalid xml files:')
    for item in invalid_xmls:
        print(item)
else:
    print('There is no invalid xml file.')


print('Finished.')











