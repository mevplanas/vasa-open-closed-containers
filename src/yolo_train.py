from yolov5 import train
import os
import yaml
# Azure sdk
from azureml.core import Workspace
import mlflow
import os
import glob
from PIL import Image
import pandas as pd

def yolo_v5_train():
    """
    The function creates yolo model for object detection.
    """
    # Infering the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))
    # Reading the configuration file
    with open(os.path.join(current_path, '..', 'configuration.yml'), 'r') as stream:
        try:
            _conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # Path to experments directory
    train_dir = os.path.join(current_path, '..', 'runs', 'train')
    # Path to yolo configuration file
    data = os.path.join(current_path, '..', 'machine_learning', 'configuration.yml')
    # Define pretrained model
    pretrained_model = _conf['YOLO_V5_PARAMETERS']['pretrained_model']
    # Loading pre trained yolo model
    weights = os.path.join(current_path, '..', 'machine_learning', 'yolov5s.pt')
    
    #Enter details of your AzureML workspace
    subscription_id = _conf['AZURE_WORKSPACE_CREDENTIALS']['subscription_id']
    resource_group = _conf['AZURE_WORKSPACE_CREDENTIALS']['resource_group']
    workspace_name = _conf['AZURE_WORKSPACE_CREDENTIALS']['workspace_name']

    # Get Workspace instance from Azure
    ws = Workspace.get(name=workspace_name,
                    subscription_id=subscription_id,
                    resource_group=resource_group)

    # Defining the experiment name
    experiment_name = _conf['MLFLOW']['exp_containers_name']

    # Set up MLflow to track the metrics
    mlflow.set_tracking_uri(ws.get_mlflow_tracking_uri())
    mlflow.set_experiment(experiment_name)
    mlflow.autolog()

    # Starting the tracking of mlflow experiment
    mlflow.start_run()
    

    # Loading model training parameters
    batchsize = _conf['YOLO_V5_PARAMETERS']['batch_size']
    epochs = _conf['YOLO_V5_PARAMETERS']['epochs']
    imgsz = _conf['YOLO_V5_PARAMETERS']['imgsz']
    device = _conf['YOLO_V5_PARAMETERS']['device']

    # Logging parameters to MLFlow
    mlflow.log_params(
        {
            'batch_size' : batchsize,
            'epochs' : epochs,
            'imgsz' : imgsz,
            'device' : device,
            'pretrained_model' : pretrained_model
        }
    )

    # Calculate train and val images count
    train_data_dir = os.path.join(current_path, '..', 'machine_learning', 'train', 'images')
    val_data_dir = os.path.join(current_path, '..', 'machine_learning', 'val', 'images')
    # Get all train and val images as list
    train_data_lst = os.listdir(train_data_dir)
    val_data_lst = os.listdir(val_data_dir)

    # Adding jpg and png to new list
    train_data_img = []
    for img in train_data_lst:
        if img.endswith('.png') or img.endswith('.jpg') or img.endswith('.JPG'):
            train_data_img.append(img)

    val_data_img = []
    for img in val_data_lst:
        if img.endswith('.png') or img.endswith('.jpg') or img.endswith('.JPG'):
            val_data_img.append(img)

    # Get count of train and val images
    train_count = len(train_data_img)
    val_count = len(val_data_img)

    # Logging img counts to MLFlow
    mlflow.log_params(
        {
            'train_img_count' : train_count,
            'val_img_count' : val_count,
        }
    )

    # Train model on custom dataset
    train.run(data=data, weights=weights, batchsize=batchsize, epochs=epochs, imgsz=imgsz, device=device)

    # Get last created directory from train directory
    train_dirs = os.listdir(train_dir)
    dirs = [os.path.join(train_dir, dir) for dir in train_dirs]
    latest_dir = max(dirs, key=os.path.getctime)
    # Get YOLO experment name from absoulute experment directory path 
    yolo_exp = latest_dir.split('\\')[-1]
    # Logging YOLO exprement name
    mlflow.log_params({'YOLO_EXPERMENT': yolo_exp})
    # Logging png figures to MLFlow
    images = glob.glob(f'{latest_dir}/*.png')
    i=0
    for im in images:
        try:
            filename = im.split('/')[-1]
            array = Image.open(im)
            mlflow.log_image(array, filename)
            i+=1
        except Exception as e:
            print(e)
            i+=1

    # Logging jpeg figures to MLFlow
    images = glob.glob(f'{latest_dir}/*.jpg')
    i=0
    for im in images:
        try:
            filename = im.split('/')[-1]
            array = Image.open(im)
            mlflow.log_image(array, filename)
            i+=1
        except Exception as e:
            print(e)
            i+=1
    
    # Get model metrics from results.html
    results_html = os.path.join(latest_dir, 'results.html')
    table = pd.read_html(results_html)
    table = table[0]

    # Loggin images and labels count from results.html
    for index, row in table.iterrows():
        mlflow.log_params({
            f'{row["Class"]}_val_images' : row['Images'],
            f'{row["Class"]}_val_labels' : row['Labels']
        })
    
    # Logging metrics from results.html
    for index, row in table.iterrows():
        mlflow.log_metrics({
            f'{row["Class"]}_precision' : row['P'],
            f'{row["Class"]}_recall' : row['R'],
            f'{row["Class"]}_mAP@.5' : row['mAP@.5'],
            f'{row["Class"]}_mAP@.5:.95' : row['mAP@.5:.95'],
            })

    # Logging model to MLFlow
    path_to_model = os.path.join(latest_dir, 'weights\\best.pt')
    mlflow.log_params({'path_to_model': path_to_model})

    # Stop run
    mlflow.end_run()

if __name__ == '__main__':
    yolo_v5_train()