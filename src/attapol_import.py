# Configuration reading 
import os
import yaml

# Azure sdk
from azureml.core import Workspace, Dataset, Datastore

# Importing utils functions
from utils import create_dir, cv_rewrite, labels_renamer


def pipeline():
    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Reading the configuration file
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        _conf = yaml.safe_load(stream)

    # Get Datastore name
    az_datastore = _conf['AZ_OPEN_CLOSED_ATTAPOL']['datastore']
    # Get Datastore name
    az_dataset = _conf['AZ_OPEN_CLOSED_ATTAPOL']['dataset']

    # Initiating the connection to the workspace
    workspace = Workspace(**_conf.get('AZURE_WORKSPACE_CREDENTIALS'))

    # Downloading the images
    _download_dir = os.path.join(current_path, '..', 'dataset', 'attapol')
    create_dir(_download_dir)
    
    datastore = Datastore.get(workspace, az_datastore)
    dataset = Dataset.File.from_files(path=(datastore, az_dataset))

    dataset.download(target_path=_download_dir, overwrite=True)

     # Checking images
    for dirpath, _, files in os.walk(_download_dir):
        for file_name in files:
            # Creating the full path 
            _full_path = os.path.join(dirpath, file_name)
            # Rewriting image to avoid corrupt image error
            cv_rewrite(_full_path)
    
    # Renaming attapol labels filenames
    labels_dir = os.path.join(_download_dir, 'container_open_closed_attapol', 'labels')
    labels_renamer(labels_dir)

if __name__ == '__main__':
    pipeline()