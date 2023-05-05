# OS moving
import os
import shutil

# Iterationg tracking
from tqdm import tqdm


def remove_reapeated(list_one: list, list_two: list) -> list:
    """
    The function deletes repeating elements from first list in comparison with second list

    Arguments
    ---------
    list_one : list 
        first list from which values will be removed
    list_two : list
        comparison list element

    Outputs
    -------
    list_diff : list
        list with removed reapeated values
    """
    # Iterate through list 
    list_diff = []
    for el in list_one:
        # Checking repeating elements
        if el not in list_two:
            # If repeats remove element
            list_diff.append(el)

    return list_diff


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

    # Defining the path to the images dir 
    _images_dir_temp = os.path.join(current_path, '..', 'dataset', 'images', 'temp')

    # Defining the path to labels 
    _labels_dir_temp = os.path.join(current_path, '..', 'dataset', 'labels', 'temp')

    # Define the path to test images
    _images_dir_test = os.path.join(current_path, '..', 'dataset', 'test', 'images')

    # Define the path to labels
    _labels_dir_test = os.path.join(current_path, '..', 'dataset', 'test', 'labels')
    
    # Listing the files in the temp dir 
    _images = os.listdir(_images_dir_temp)
    _labels = os.listdir(_labels_dir_temp)

    # Listing the file in the test dir
    _images_test = os.listdir(_images_dir_test)
    _labels_test = os.listdir(_labels_dir_test)

    # Removing repeating values between temp and test directories
    _images = remove_reapeated(_images, _images_test)
    _labels = remove_reapeated(_labels, _labels_test)

    # Creating a dictionary with no file ending for images
    _images_dict = {file_name.split('.')[0]: file_name for file_name in _images}
    _labels_dict = {file_name.split('.')[0]: file_name for file_name in _labels}

    # Only leaving the intersecting keys 
    _keys = list(set(_images_dict.keys()).intersection(set(_labels_dict.keys())))

    # Defining the path to machine_learning dir 
    _ml_dir = os.path.join(current_path, '..', 'machine_learning')

    # Defining the train and val directories for images and labels 
    _images_dir_train = os.path.join(_ml_dir, 'train', 'images')
    _labels_dir_train = os.path.join(_ml_dir, 'train', 'labels')
    _dir_val = os.path.join(_ml_dir, 'val')

    # Creating the train and val directories for images and labels
    os.makedirs(_images_dir_train, exist_ok=True)
    os.makedirs(_labels_dir_train, exist_ok=True)
    os.makedirs(_dir_val, exist_ok=True)

    # Populating the training images 
    move_files(_keys, _images_dir_temp, _images_dir_train, _images_dict, 'Moving training images')
    
    # Populating the training labels
    move_files(_keys, _labels_dir_temp, _labels_dir_train, _labels_dict, 'Moving training labels')
    
    # Move validation images and labels
    shutil.move(_images_dir_test, _dir_val)
    shutil.move(_labels_dir_test, _dir_val)

if __name__ == '__main__':
    pipeline()