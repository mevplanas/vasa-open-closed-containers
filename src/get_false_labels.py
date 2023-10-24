import os
from pathlib import Path
from sys import platform
import shutil

def copy_false():
    # Current path
    curr_path = Path().absolute()
    # Croppped image dirs
    true_labes_dir = os.path.join(curr_path, 'dataset', 'attapol', 'true_labels')
    false_labels_dir = os.path.join(curr_path, 'dataset', 'attapol', 'false_labels')
    # Labels
    true_labels = os.listdir(true_labes_dir)
    # All labels
    closed_labels_dir = os.path.join(curr_path, 'notebooks', 'label_inference', 'dataset', 'closed')
    opened_labels_dir = os.path.join(curr_path, 'notebooks', 'label_inference', 'dataset','opened')
    closed_labels = os.listdir(closed_labels_dir)
    opened_labels = os.listdir(opened_labels_dir)

    closed_labels_abs = [os.path.join(closed_labels_dir, x) for x in closed_labels]
    opened_labels_abs = [os.path.join(opened_labels_dir, x) for x in opened_labels]

    all_labels = closed_labels_abs + opened_labels_abs

    for _label in all_labels:

        if platform == "win32":
            _label_name = _label_name.split('\\')[-1]
        else:
            _label_name = _label.split('/')[-1]
            
        if _label_name not in true_labels:
            shutil.copy(_label, false_labels_dir)
    

if __name__ == '__main__':
    copy_false()