# OS wrangling 
import os

# Importing dir creation function 
from utils import create_dir

# Pipeline function for dir creation 
def pipeline() -> None:
    """
    The pipeline function that creates all the necesary directories
    """
    # Infering the current file path 
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Creating the needed directories list 
    dirs = [
        'dataset/images/train',
        'dataset/images/val',
        'dataset/images/temp',
        'dataset/labels/train', 
        'dataset/labels/val', 
        'dataset/labels/temp'
    ]

    # Iterating over the directories list
    for dir in dirs:
        # Creating the full path 
        dir_path = os.path.join(current_path, '..', dir)

        # Creating the dir 
        create_dir(dir_path)

if __name__ == '__main__':
    pipeline()