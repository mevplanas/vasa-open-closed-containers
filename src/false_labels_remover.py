from pathlib import Path
import os
from zipfile import ZipFile
from sys import platform
from collections import defaultdict

def create_dict(label_tuples):
    default_dict = defaultdict(list)
    for label, row in label_tuples:
       default_dict[label].append(row)
    
    return default_dict

def delete_false_labels(all_labels: dict, false_labels:dict):
    for _txt, _full_path in all_labels.items():
        # Get txt file with false labels
        _bad_labels = false_labels.get(_txt)
        # Remove false label from txt file
        if _bad_labels != None:
            with open(_full_path, 'r+') as stream:
                lines = stream.readlines()
                _bad_labels.sort(reverse=True)
                for _index in _bad_labels:
                    del lines[int(_index)]
                stream.seek(0)
                stream.truncate()
                stream.writelines(lines)

def detect_class(
        img_label_name: str, 
        class_dict: dict = {
            'closed': 0,
            'opened': 1,
        }
        ):
    # Setting the default class to 0
    label_class = 0
    label = 'closed'

    # Iterating over the class_dict and infering with what string does the label start
    for key, value in class_dict.items():
        if img_label_name.startswith(key):
            label_class = value
            label = key
            break

    # Removing the class from the label name
    img_label_name = img_label_name.split(f"{label}_")[-1]

    # Returning the tuple
    return (img_label_name, label_class)

def pipeline():

    # Return current path
    curr_path = Path().absolute()

    # List all files and folder and construct absolute file paths 
    false_labels_zip =  os.path.join(curr_path, 'dataset', 'attapol', 'bad_labels.zip')
    false_labels_img=  os.path.join(curr_path, 'dataset', 'attapol','bad_labels')

    dir_train_labels = os.path.join(curr_path, 'dataset', 'labels', 'temp')

    _train_labels = os.listdir(dir_train_labels)

    abs_train_labels = [os.path.join(dir_train_labels, x) for x in _train_labels]

    # Store all absolute file filepaths and filename into dictionary
    dict_all_labels = {}
    for _label in abs_train_labels:
        if platform == "win32":
            _label_split = _label.split('temp\\')[-1]
        else:
            _label_split = _label.split('temp/')[-1]
        
        dict_all_labels.update({_label_split: _label})

    # Extract and construct false labels filepaths
    os.makedirs(false_labels_img, exist_ok=True)
    with ZipFile(false_labels_zip) as zip:
        zip.extractall(false_labels_img)

    false_labels_img = os.path.join(curr_path, 'dataset', 'attapol', 'bad_labels')

    labels = os.listdir(false_labels_img)
    abs_labels = [os.path.join(false_labels_img, x) for x in labels]

    # Create list of tuples with label filepaths and false label row
    labels_collection = []
    for _abs_label in abs_labels:

        if platform == "win32":
            _target_name = _abs_label.split('bad_labels\\')[-1].split('.')[0]
        else:
            _target_name = _abs_label.split('bad_labels/')[-1].split('.')[0]

        _target_name = detect_class(_target_name)
        label_row = _target_name[0][-1]
        __target_name = _target_name[0]
        _target_name_txt = f"{__target_name[0:-2]}.txt"
        labels_collection.append((_target_name_txt,label_row))

    labels_dict = create_dict(labels_collection)

    # Delete false labels
    delete_false_labels(all_labels=dict_all_labels,false_labels=labels_dict)


if __name__ == '__main__':
    pipeline()