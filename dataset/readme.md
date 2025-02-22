# Tools for dataset

## Overview

This module implements all the tools for working with the dataset.

## Features

- Dataset analysis
- Dataset split (splitting the dataset into training, validation and testing)
- Dataset aggregation (combining all tasks into one large dataset)

## Requirements

- skimage
- pycocotools

## Installation

```bash
pip install skimage pycocotools
```

## Dataset analysis
Node **dataset_analysis.ipynb** is needed to study the features of the dataset in the coco format.

### Configuration
Before working, set up the variables as shown below.
```bash
root_dir   = "D:/Datasets/CocoAnotations"               # path to the root directory with the dataset
images_dir = "images"                                   # directory with images relative to root
annotations_path = root_dir + "/instances_default.json" # path to file with coco annotation
```

### Run
After setting up, run each cell one by one and look at the evaluation results. If you only downloaded the coco annotations as json, you may not run the last cell.

## Dataset splitter
This tool is designed to split the dataset into training, validation and testing.  
It should be clarified that the dataset must be of the type presented in **data-extraction/cvat**

### Configuration
Before splitting the dataset, change all paths.
```bash
input_folder  = "D:\Datasets\YoloDrone"       # dataset in data-extraction/cvat format
output_folder = "D:\Datasets\YoloDroneSplit"  # path to save dataset
train, val, test = ratio = (0.75, 0.15, 0.1)  # percentage of division into sub-datasets
```

### View
The directory looks like this:
```
 root   
   ├── train
   │   ├── task_1
   │   │    ├── images
   │   │    └── labels
   │   ├── ...
   │   └── task_N
   │
   ├── val
   │   ├── task_2
   │   ├── ...
   │   └── task_N
   │ 
   └── test
       ├── task_3
       ├── ...
       └── task_N
```
It should be noted that this type of division will need to be used to aggregate the dataset.

## Dataset aggregator
This tool is designed to combine datasets of tasks into a large dataset.

### Configuration
Before splitting the dataset, change all paths.
```bash
input_aggregation_folder = "D:\Datasets\YoloDroneSplit" # Path to the directory with the split dataset
output_aggregation_folder = "D:\Datasets\YoloDroneAll"  # path to save dataset
```

### Run
After setup and preliminary splitting, run the cell with aggregation.
