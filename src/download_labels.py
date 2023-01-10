# Azure SDK
from azureml.core import Workspace, Dataset

# OS traversal
import os

# Configuration reading
import yaml

# Data wrangling
import pandas as pd 

# Coordinate wrangling 
from utils import pascal_voc_to_yolo, azure_to_pascal, class_to_int

# Iteration tracking 
from tqdm import tqdm

# Get Azure image labels dataframe
def pipeline() -> None:
    """
    The function that downloads all labels from defined container
    and returns labels dataframe
    """

    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Reading the configuration file
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        try:
            _conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Initiating the connection to the workspace
    workspace = Workspace(**_conf.get('AZURE_WORKSPACE_CREDENTIALS'))

    # Getting the label versions
    _versions = _conf.get('OPEN_CLOSED_LABELS')

    # Creating a placeholder dataframe 
    _d = pd.DataFrame({})

    for _version in _versions:
        # Downloading the images
        _dataset = Dataset.get_by_name(
            workspace, 
            name=f'{_version}'
            )
        _df = _dataset.to_pandas_dataframe()

        # Concatenating
        _d = pd.concat([_d, _df], axis=0)
    
    

    # Reseting the index
    _d.reset_index(drop=True, inplace=True)

    # Leaving only the needed columns 
    _d = _d[['image_url', 'label', 'image_height', 'image_width']].copy()

    # Iterating over the rows and saving the labels to disk 
    for _, _row in tqdm(_d.iterrows(), desc='Saving the labels', total=_d.shape[0]):
        # Saving the image height and widht
        _h = _row['image_height']
        _w = _row['image_width']

        # Creating the final name for the label file 
        _name = str(_row['image_url']).split('/')[1:]
        _name = '_'.join(_name)
        _name = _name.split('.')[0]
        _name = f'{_name}.txt'

        # Extracting the label list 
        _labels = _row['label']

        # Creating the yolo coordinate placeholder 
        _yolo = []
        for _label in _labels:
            # Converting from azure to pascal
            _label_pascal = azure_to_pascal(
                top_x=_label['topX'], 
                bottom_x=_label['bottomX'], 
                top_y=_label['topY'], 
                bottom_y=_label['bottomY'], 
                image_w=_w,
                image_h=_h
            )

            # Converting from pascal to yolo 
            _label_yolo = pascal_voc_to_yolo(
                x_min=_label_pascal[0],
                y_min=_label_pascal[1],
                x_max=_label_pascal[2],
                y_max=_label_pascal[3],
                image_w=_w,
                image_h=_h
            )

            _label_yolo.insert(0, class_to_int(_label['label']))
            # Appending to the placeholder
            _yolo.append(_label_yolo)

        # Name of the txt file 
        _name_txt = os.path.join(current_path, '..', 'dataset', 'labels', 'temp', _name)

        # If the file already exists we delete it 
        if os.path.exists(_name_txt):
            os.remove(_name_txt)

        # Writing the coordinates to file 
        with open(_name_txt, 'w') as f:
            for _label in _yolo:
                f.write(f'{_label[0]} {_label[1]} {_label[2]} {_label[3]} {_label[4]}\n')

if __name__ == '__main__':
   pipeline()