import glob
import os
import random
import shutil
import argparse

'''
Split dataset to train and val.

src dataset will be split randomly.

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


example:
python split_dataset.py --src_path=your_source_data_path --train_ratio=0.9


'''

parser = argparse.ArgumentParser()

parser.add_argument("--src_path", default="",
                    type=str, help='path of source data')
parser.add_argument("--train_ratio", default=0.95,
                    type=float, help='ratio of train set. range: (0, 1)')
args = parser.parse_args()


def write_data(file_name, data_list):
    f = open(file_name, 'w')
    for item in data_list:
        d = item.split("\\")[-1].split("/")[-1].split('.')[0]
        f.write(d + '\n')
    f.close()
    print('File saved at: {}'.format(file_name))


if __name__ == "__main__":

    src_xml_path = os.path.join(args.src_path, 'Annotations')
    if not os.path.exists(src_xml_path):
        raise ValueError("[Error] Annotations path cannot be found from : {}".format(src_xml_path))

    # create ImageSets
    image_sets_path = os.path.join(args.src_path, 'ImageSets/Main')
    if not os.path.exists(image_sets_path):
        os.makedirs(image_sets_path)

    all_files = glob.glob(os.path.join(src_xml_path, "*.xml"))

    random.shuffle(all_files)
    train_len = int(len(all_files) * args.train_ratio)

    train_set = all_files[0:train_len]
    val_set = all_files[train_len: len(all_files)]

    print('all samples num: {}'.format(len(all_files)))
    print('train set num: {}'.format(len(train_set)))
    print('val set num: {}'.format(len(val_set)))
    print('===='*20)

    write_data(os.path.join(image_sets_path, 'trainval.txt'), all_files)
    write_data(os.path.join(image_sets_path, 'train.txt'), train_set)
    write_data(os.path.join(image_sets_path, 'val.txt'), val_set)

    print('Finished.')

