# OS wrangling 
from email.mime import image
import os
# Computer vision
import cv2

# Directory creation
def create_dir(dir_path: str) -> None:
    """
    Function to create a directory
    
    Arguments
    ---------
    dir_path: str
        Path to the directory to be created

    Returns
    -------
    None
        Creates the directory along with all the intermediate dirs
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def pascal_voc_to_yolo(
    x_min: float, 
    y_min: float, 
    x_max: float, 
    y_max: float, 
    image_w: float, 
    image_h: float
    ) -> list:
    """
    The function that converts pascal_voc coordinates to yolo coordinates

    Arguments
    ---------
    x_min: float
        x_min x coordinate of the top left corner of the bounding box
    y_min: float
        y_min y coordinate of the top left corner of the bounding box
    x_max: float
        x_max x coordinate of the bottom right corner of the bounding box
    y_max: float
        y_max y coordinate of the bottom right corner of the bounding box
    image_w: float
        width of the image in pixels
    image_h: float
        height of the image in pixels
    
    Returns
    -------
    list
        list of [x_center, y_center, width, height] of the yolo rectangle
    """
    # Center of the yolo rectangle
    x_center = (x_min + x_max) / (2 * image_w)
    y_center = (y_min + y_max) / (2 * image_h)
    
    # Width and height of the yolo rectangle
    w = (x_max - x_min) / image_w
    h = (y_max - y_min) / image_h
    
    # Returning
    return [x_center, y_center, w, h]

def azure_to_pascal(
    top_x: float, 
    bottom_x: float, 
    top_y: float, 
    bottom_y: float, 
    image_w: float,
    image_h: float
):
    """
    Converts the raw azure coordinates to pascal_voc format 

    Arguments
    ---------
    top_x: float
        x coordinate of the top left corner of the bounding box
    bottom_x: float
        x coordinate of the bottom right corner of the bounding box
    top_y: float
        y coordinate of the top left corner of the bounding box
    bottom_y: float
        y coordinate of the bottom right corner of the bounding box
    image_w: float
        width of the image in pixels
    image_h: float
        height of the image in pixels
    
    Returns
    -------
    list
        list of [x_min, y_min, x_max, y_max] of the pascal rectangle
    """
    # Applying the transformations
    x_min = top_x * image_w
    x_max = bottom_x * image_w
    y_min = top_y * image_h
    y_max = bottom_y * image_h

    return [x_min, y_min, x_max, y_max]

def cv_rewrite(image_path: str) -> None:
    """
    The function rewrites image.

    Arguments
    ---------
    image_path: str
        image file path
    """
    # Reading image
    if image_path.endswith('.png') or image_path.endswith('.jpg') or image_path.endswith('.JPG'):
        try: 
            img = cv2.imread(image_path)
            # Deleting original image
            os.remove(image_path)
            # Writing newly created image
            cv2.imwrite(image_path, img)
        # Exception 
        except Exception as e:
            print(e)
            print('image deleted:' + image_path)


def class_to_int(label_class):
    """
    The function converts label class name into integer value

    Arguments
    ---------
    label_class: str
        labels class as string
    
    Output
    ------
    label_int: int
        label class as integer
    """
    # If statement for labels class name check
    if label_class == 'closed':
        label_int = 0
    else:
        label_int = 1
    
    return label_int


def labels_delete(labels_dir: str, max_width: float, max_height: float):
    """
    The function deletes labels with bigger width and height values than allowed.

    Arguments
    ---------
    labels_dir: str
        directory with label txt file
    max_width: float
        highest allowed label width
    max_height: float
        highest allowed label height
    """
    # Get all label files in a list
    labels = os.listdir(labels_dir)
    # Iterate through all files 
    for label in labels:
        # Construct abs file path
        label_path = os.path.join(labels_dir, label)
        # Open txt file
        with open(label_path, 'r') as contents:
            # Reading all lines in txt file
            lines = contents.readlines()
            # Closing txt
            contents.close()
        # Overwrite txt file with line by if condition
        with open(label_path, 'w') as data:
            # Iterate through all lines in txt file
            for line in lines:
                # Remove blank lines
                a = line.strip()
                # Split elements in line between spaces
                lst = a.split(' ')
                # Write line into txt file if height 
                # and width is equal or less than max_width and max_height
                if float(lst[3]) <= max_width and float(lst[4]) <= max_height:
                    data.write(line)
            # Closing txt
            data.close()


def labels_renamer(labels_dir: str):
    """
    The functions renames attapol labels

    Arguments
    ---------
    labels_dir: str
        folder with open/closed labels
    """
    # Get all label files in a list
    labels = os.listdir(labels_dir)
    # Iterate thorugh all labels
    for _label in labels:
        # Construct new label filename
        _label_str_el = _label.split('_')
        _label_str_el = _label_str_el[1:]
        label = '_'.join(_label_str_el)
        # Renaming label
        src_file_path = os.path.join(labels_dir, _label)
        dest_file_path = os.path.join(labels_dir, label)
        os.rename(src_file_path, dest_file_path)

    
