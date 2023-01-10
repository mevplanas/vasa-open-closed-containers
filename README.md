# vasa-open-closed-containers

Codes that house the creation of the open/closed identifier of garbage containers

VASA in Lithuanian stands for:

`V` - Vilniaus (Vilnius)
`A`- Atliekų (Waste)
`S` - Sistemos (System)
`A` - Administratorius (Administrator)

The main purpose of this project - detect and classify trash around waste containers from a photo.

`Third part of this project - detect opened or closed container lid is from a given photo.`

The structure of the project is as follows:

```
├── dataset
│   ├── images
│   │    ├── raw
│   │    ├── temp
│   │    ├── train
│   │    └── val
│   └── labels
│        ├── temp
│        ├── train
│        └── val
├── machine_learning
│   ├── __init__.py
│   ├── configuration.yml
│   ├── yolov5s.pt
│   ├── images
│   │    ├── train
│   │    └── val
│   └── labels
│        ├── train
│        └── val
├── README.md
├── requirements.txt
├── configuration-example.yml
├── configuration.yml
├── Dockerfile
├── env.yml
├── notebooks
│    ├── __init__.py
│    └── .ipynb
├── src
│    ├── __init__.py
│    ├── create_dataset.py
│    ├── create_temp_images.py
│    ├── dataset_structure.py
│    ├── download_images.py
│    ├── download_labels.py
│    ├── predict_bbox.py
│    └── yolo_train.py
├── __init__.py
├── run.py
└── utils.py
```

All the scripts that are used in the project are located in the `src` folder.

# Virtual environment creation

The Python version for this project is 3.9.

All the packages needed are listed in requirements.txt file.

# Docker

To use docker, run the command to build the image:

```
docker build -t vasa .
```

To run the container and sync the volumes dataset/ with the app/dateset in the container, run the command:

```
docker run -it --rm -v $(pwd)/dataset/:/app/dataset/ vasa
```

# Linux

## Virtualenv

The package managment is done with virtualenv

```
# Creating the empty env
virtualenv -p python3.9 venv-vasa

# Activating
source venv-vasa/bin/activate

# Populating with packages
pip install -r requirements.txt
```

## Anaconda

To use anaconda in Ubuntu use the commands:

```
# Creating an empty env
conda create -n venv-vasa python=3.9

# Activating the env
conda activate venv-vasa

# Installing pip
conda install pip

# Installing the packages
pip install -r requirements.txt
```

# Windows

Pip is used in Windows.

```
## Creating environment
python3 -m venv venv-vasa

## Activating environment
venv-vasa\Scripts\activate

## Installing all the packages
python3 -m pip install -r requirements.txt
```

## Installing pytorch

Please follow the guide here: https://pytorch.org/

# Scripts

# All scripts should be run sequentaly

## 1. Create folder structure for YOLO

```
python -m src.dataset_structure
```

The created directory tree:

```
├── dataset
│   ├── images
│   │   ├── raw
│   │   ├── temp
│   │   ├── train
│   │   └── val
│   └── labels
│       ├── temp
│       ├── train
│       └── val
```

## 2. Downloading labeled images

```
python -m src.download_images
```

The command downloads labeled images from Azure Storage container to the `dataset/images/raw` directory.

## 3. Creating the temp images

```
python -m src.create_temp_images
```

The command wrangles the images in the `raw` directory and creates files in the `temp` directory that adheres to the labeling file convention.

## 4. Download labels

```
python -m src.download_labels
```

The command downloads labels from Azure Storage container to the `dataset/labels/temp` directory.

## 5. Create dataset for YOLO

```
python -m src.create_dataset
```

Creates a dataset for the YOLO algorithm. The images are saved in the directories:

```
├── images
│   ├── train
│   └── val
```

The labels are saved in:

```
└── labels
    ├── train
    └── val
```

## 7. Create YOLO model

```
python -m src.yolo_train
```

Creates YOLOv5 model for open/closed detection.
