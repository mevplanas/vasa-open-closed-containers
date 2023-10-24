from pathlib import Path
import os
from sys import platform


def find_file(files:str, intrest_file: str) -> str:
    """
    Desc
    -----
    Function find filename in filenames list without extension

    Parameters:
    ----
    :param files: list of all files 
    :param intrest_file: file name without extension

    Returns:
    file: str
        full path of filename from files list 

    """
    for file in files:
        _no_ext = os.path.splitext(file)[0]
        if _no_ext == intrest_file:
            return file
        


def pipeline():
    # Return current path
    curr_path = Path().absolute()

    dir_train_labels = os.path.join(curr_path, 'dataset', 'labels','temp')

    _labels = os.listdir(dir_train_labels)

    abs_train_labels = [os.path.join(dir_train_labels, x) for x in _labels]

    # Iterates throug all label files 
    for _label in abs_train_labels:
        # Open file
        if _label.endswith('.txt') or _label.endswith('.TXT'):
            with open(_label) as _file:
                lines =_file.readlines()
                _file.close()
                # Check if lenght of lines in txt file in equal to 0
                if len(lines) == 0:
                    if os.path.exists(_label):
                        os.remove(_label)

    

if __name__ == '__main__':
    pipeline()