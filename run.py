# Import all scripts from src
from src.dataset_structure import pipeline as dataset_structure_pipeline
from src.download_images import pipeline as images_download_pipeline
from src.create_temp_images import pipeline as temp_images_pipeline
from src.download_labels import pipeline as labels_download_pipeline
from src.create_dataset import pipeline as yolo_dataset_pipeline
from src.yolo_train import yolo_v8_train
from src.attapol_import import pipeline as attapol_import_pipeline
from src.create_temp_attapol import pipeline as temp_attapol_pipeline
from src.download_test_dataset import pipeline as download_test_dataset
from src.false_labels_remover import pipeline as label_remover
from src.delete_empty import pipeline as delete_empty
from src.delete_no_labels_image import pipeline as delete_img_labels

def pipeline() -> None:
    """
    The functions executes all pipelines.
    """
    # Create folder structure for YOLO 
    dataset_structure_pipeline()
    # Import data from attapol
    attapol_import_pipeline()
    # Copy images and labels to temp folders
    temp_attapol_pipeline()
    # Delete false labels from label.txt
    label_remover()
    # Delete empty label.txt
    delete_empty()
    # Delete images and labels with no coresponding image
    delete_img_labels()
    # Downloading labeled images 
    images_download_pipeline()
    # Creating the temp images
    temp_images_pipeline()
    # Download labels
    labels_download_pipeline()
    # Download test dataset
    download_test_dataset()
    # Create dataset for YOLO 
    yolo_dataset_pipeline()
    # Creating YOLO model
    yolo_v8_train()

if __name__ == '__main__':
   pipeline()
