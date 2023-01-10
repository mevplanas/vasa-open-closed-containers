# Configuration reading 
import os
import yaml

# Azure sdk
from azureml.core import Workspace, Dataset

# Importing dir creation function 
from utils import create_dir, cv_rewrite

def pipeline():
    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Reading the configuration file
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        _conf = yaml.safe_load(stream)

    
    # Initiating the connection to the workspace
    workspace = Workspace(**_conf.get('AZURE_WORKSPACE_CREDENTIALS'))

    # Downloading the images
    _download_dir = os.path.join(current_path, '..', 'dataset', 'images', 'raw')
    create_dir(_download_dir)
    
    dataset = Dataset.get_by_name(workspace, name='containers_open_closed')
    dataset.download(target_path=_download_dir, overwrite=True)

    # Checking images
    for dirpath, _, files in os.walk(_download_dir):
        for file_name in files:
            # Creating the full path 
            _full_path = os.path.join(dirpath, file_name)
            # Rewriting image to avoid corrupt image error
            cv_rewrite(_full_path)

if __name__ == '__main__':
    pipeline()