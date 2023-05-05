# Configuration reading 
import os
import yaml

# Azure sdk
from azureml.core import Workspace, Dataset, Datastore

# Importing dir creation function 
from utils import create_dir, cv_rewrite


def pipeline():
    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Reading the configuration file
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        _conf = yaml.safe_load(stream)

    # Get Datastore name and data version
    az_datastore = _conf['AZ_OPEN_CLOSED_TEST']['datastore']
    az_dataset = _conf['AZ_OPEN_CLOSED_TEST']['dataset']

    # Initiating the connection to the workspace
    workspace = Workspace(**_conf.get('AZURE_WORKSPACE_CREDENTIALS'))

    # Downloading the images
    _download_dir = os.path.join(current_path, '..', 'dataset', 'test')
    create_dir(_download_dir)
    
    # Get test data from Azure
    datastore = Datastore.get(workspace, az_datastore)
    datastore.download(target_path=_download_dir, overwrite=True)

     # Checking images
    for dirpath, _, files in os.walk(_download_dir):
        for file_name in files:
            # Creating the full path 
            _full_path = os.path.join(dirpath, file_name)
            # Rewriting image to avoid corrupt image error
            cv_rewrite(_full_path)


if __name__ == '__main__':
    pipeline()