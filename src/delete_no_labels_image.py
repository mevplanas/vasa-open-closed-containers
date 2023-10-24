from pathlib import Path
import os
from sys import platform

def split_file_name(file:str, file_type: str):

    available_types = ['images', 'labels', 'temp']

    if file_type not in available_types:
        raise TypeError(f'file_type argument should be "images" or "labels", but "{file_type}" detected')

    if platform == 'win32':
        img_name = file.split(f'{file_type}\\')[1].split('.')[0]
    else:
        img_name = file.split(f'{file_type}/')[1].split('.')[0]

    return img_name

def pipeline():

    # Return current path
    curr_path = Path().absolute()
    # List all files and folder and construct absolute file paths 
    dir_train_images = os.path.join(curr_path, 'dataset', 'images','temp')
    dir_train_labels = os.path.join(curr_path, 'dataset', 'labels','temp')

    _labels = os.listdir(dir_train_labels)
    _images = os.listdir(dir_train_images)

    abs_train_labels = [os.path.join(dir_train_labels, x) for x in _labels]
    abs_train_images = [os.path.join(dir_train_images, x) for x in _images]

    for _img in abs_train_images:
        _img_name = split_file_name(_img, 'temp')
        if F"{_img_name}.txt" not in _labels or f"{_img_name}.txt" not in _labels:
             os.remove(_img)

    for _label in abs_train_labels:
        _label_name = split_file_name(_label, 'temp')
        if f"{_label_name}.jpg" not in _images and f"{_label_name}.JPG" not in _images:
            os.remove(_label)

if __name__ == '__main__':
    pipeline()