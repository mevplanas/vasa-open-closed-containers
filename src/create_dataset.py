# OS moving
import fnmatch
import os
import shutil

# Iterationg tracking
from tqdm import tqdm

# Configuration reading 
import yaml

# Randomness 
import random

def move_files(
    keys: list, 
    source_dir: str, 
    target_dir: str, 
    image_dict: dict,
    tqdm_message: str = 'Moving files'
    ) -> None:
    """
    Function that moves the files from source_dir to target_dir  
    
    Arguments
    ---------
    keys : list
        List of keys to move 
    source_dir : str
        Source directory 
    target_dir : str
        Target directory 
    image_dict : dict
        Dictionary with the image names 
    """
    # Iterating over the keys 
    for key in tqdm(keys, desc=tqdm_message, total=len(keys)):
        # Creating the full path 
        _full_path = os.path.join(source_dir, image_dict[key])
        # Creating the target path 
        _target_path = os.path.join(target_dir, image_dict[key])
        # Moving the image to the temp dir
        shutil.move(_full_path, _target_path)

def pipeline() -> None:
    """
    The function copy all images from temp file to images file. 
    """
    # Infering the current file path 
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Reading the configuration file 
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        _conf = yaml.safe_load(stream)

    # Extracting the train val split
    _train_val_split = _conf.get('TRAIN_VAL_SPLIT')

    # Defining the path to the images dir 
    _images_dir_temp = os.path.join(current_path, '..', 'dataset', 'images', 'temp')

    # Defining the path to labels 
    _labels_dir_temp = os.path.join(current_path, '..', 'dataset', 'labels', 'temp')

    # Listing the files in the temp dir 
    _images = os.listdir(_images_dir_temp)
    _labels = os.listdir(_labels_dir_temp)

    # Creating a dictionary with no file ending for images
    _images_dict = {file_name.split('.')[0]: file_name for file_name in _images}
    _labels_dict = {file_name.split('.')[0]: file_name for file_name in _labels}

    # Only leaving the intersecting keys 
    _keys = list(set(_images_dict.keys()).intersection(set(_labels_dict.keys())))

    # Shuffling the keys 
    random.shuffle(_keys)

    # Spliting the keys into train and test keys 
    _train_keys = _keys[:int(len(_keys) * _train_val_split)]
    _test_keys = _keys[int(len(_keys) * _train_val_split):]

    # Defining the path to machine_learning dir 
    _ml_dir = os.path.join(current_path, '..', 'machine_learning')

    # Defining the train and val directories for images and labels 
    _images_dir_train = os.path.join(_ml_dir, 'train', 'images')
    _images_dir_val = os.path.join(_ml_dir, 'val', 'images')
    _labels_dir_train = os.path.join(_ml_dir, 'train', 'labels')
    _labels_dir_val = os.path.join(_ml_dir, 'val', 'labels')

    # Creating the train and val directories for images and labels
    os.makedirs(_images_dir_train, exist_ok=True)
    os.makedirs(_images_dir_val, exist_ok=True)
    os.makedirs(_labels_dir_train, exist_ok=True)
    os.makedirs(_labels_dir_val, exist_ok=True)

    # Populating the training images 
    move_files(_train_keys, _images_dir_temp, _images_dir_train, _images_dict, 'Moving training images')
    
    # Populating the training labels
    move_files(_train_keys, _labels_dir_temp, _labels_dir_train, _labels_dict, 'Moving training labels')
    
    # Populating the testing images
    move_files(_test_keys, _images_dir_temp, _images_dir_val, _images_dict, 'Moving testing images')

    # Populating the testing labels
    move_files(_test_keys, _labels_dir_temp, _labels_dir_val, _labels_dict, 'Moving testing labels')

if __name__ == '__main__':
    pipeline()