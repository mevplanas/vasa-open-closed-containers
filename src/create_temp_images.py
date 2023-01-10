# Configuration reading 
import os
import yaml

# CMD commands
import shutil

# Reading system
from sys import platform

# Regex 
import re

def pipeline():
    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Reading the configuration file
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        _conf = yaml.safe_load(stream)

    # The directory where the images where downloaded
    _download_dir = os.path.join(current_path, '..', 'dataset', 'images', 'raw')

    # The target dir 
    _target_dir = os.path.join(current_path, '..', 'dataset', 'images', 'temp')

    # Iterating over all the files in the _download_dir 
    for dirpath, _, files in os.walk(_download_dir):
        for file_name in files:
            # Creating the full path 
            _full_path = os.path.join(dirpath, file_name)
            
            if platform == "win32":
                # Creating the target name 
                _target_name = _full_path.split('raw\\')[-1]
                _target_name = re.sub('\\\\', '_', _target_name)
            else:
                _target_name = _full_path.split('raw/')[-1]
                _target_name = re.sub('//|/', '_', _target_name)
            # Creating the full target path
            _target_path = os.path.join(_target_dir, _target_name)

            # Moving the image to the temp dir
            shutil.move(_full_path, _target_path)

    # Deleting the raw dir
    shutil.rmtree(_download_dir)

if __name__ == '__main__':
    pipeline()