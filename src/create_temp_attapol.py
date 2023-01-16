# Configuration reading 
import os

# CMD commands
import shutil

# Reading system
from sys import platform

# Regex
import re

# Importing dir creation function 
from utils import create_dir

def pipeline():
    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Downloading the images
    _target_dir = os.path.join(current_path, '..', 'dataset', 'attapol', 'temp')
    create_dir(_target_dir)

    # The directory where the data where downloaded
    _download_dir = os.path.join(current_path, '..', 'dataset', 'attapol', 'container_open_closed_attapol')

    # The directory where the data where downloaded
    images_dir = os.path.join(current_path, '..', 'dataset', 'attapol', 'container_open_closed_attapol', 'images')

    # The directory where the data where downloaded
    labels_dir = os.path.join(current_path, '..', 'dataset', 'attapol', 'container_open_closed_attapol', 'labels')

    # Images temp path
    images_temp = os.path.join(current_path, '..', 'dataset', 'images', 'temp')

    # Labels temp path
    labels_temp = os.path.join(current_path, '..','dataset', 'labels', 'temp')

    # Iterating over all the files in the _download_dir
    for dirpath, _, files in os.walk(_download_dir):
        for file_name in files:
            if file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.JPG'):
            
                _full_path = os.path.join(images_dir, file_name)
                # Moving the image to the temp dir
                shutil.move(_full_path, images_temp)
            
            elif file_name.endswith('.txt') or file_name.endswith('.TXT'):

                _full_path = os.path.join(labels_dir, file_name)
                # Moving the labels to the temp dir
                shutil.move(_full_path, labels_temp)


if __name__ == '__main__':
    pipeline()