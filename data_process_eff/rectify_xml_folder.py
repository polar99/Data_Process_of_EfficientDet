import os
import glob
import xml.etree.ElementTree as ET
import argparse

'''
File structure:
----src_path
    ----JPEGImages
        xxx_1.jpg
        xxx_2.jpg
        ...
    ----Annotations (*.xml  in VOC format)
        xxx_1.xml
        xxx_2.xml
        ...
src_path must be provided while dst_folder_name is optional. If dst_folder_name is not given, the dst_folder_name will 
be set to sub-folder name of src_path

'''



parser = argparse.ArgumentParser()

parser.add_argument("--src_path", default="",
                    type=str, help='path of source data')
parser.add_argument("--dst_folder_name", default=None,
                    type=str, help='dst name for [folder] in xml')

args = parser.parse_args()

all_xmls = glob.glob(os.path.join(args.src_path, 'Annotations', '*.xml'))
print('num:{}'.format(len(all_xmls)))

if args.dst_folder_name is None:
    dst_folder_name = args.src_path.strip('\\').strip('/').split('\\')[-1].split('/')[-1]
else:
    dst_folder_name = args.dst_folder_name

print('dst_folder_name is set to: {}'.format(dst_folder_name))

for xml_item in all_xmls:

    base_name = xml_item.split('\\')[-1].split('/')[-1].split('.')[0]

    tree = ET.parse(xml_item)
    root = tree.getroot()

    folder_node = root.find('folder')
    folder_node.text = dst_folder_name

    # check filename if is same as xml.
    xml_filename = base_name
    filename_node = root.find('filename')
    if filename_node.text.split('.')[0] != base_name:
        filename_node.text = base_name + '.jpg'

    tree.write(xml_item)

print('Finished.')


