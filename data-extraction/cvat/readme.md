# CVAT task export

## Overview

This Python module provides the ability to export tasks and task lists from the CVAT to which the user connects

## Features

- Export dataset in yolo and coco format
- Export task list
- Writing and reading a list of tasks from .txt

## Requirements

- cvat-sdk
- urllib3
- zipfile

## Installation

```bash
pip install urllib3 cvat-sdk
```

## Configuration

Before exporting the dataset, you need to register the configuration for the user's cvat.  
The user configuration might look something like this:  
```bash
cvat_url = "https://cvat.mycloud/"
cvat_user = "RootUser"
cvat_password = "12345Qwerty"
organization = "MyOrganization"
```
After setting up the user, run all cells (optional for task list).

## Output dataset
Yolo dataset looks like:  
```
 root   
   └── task_1
       ├── images
       │   ├── frame_000000.PNG
       │   ├── ...
       │   └── frame_NNNNNN.PNG  
       └── labels
           ├── frame_000000.txt
           ├── ...
           └── frame_NNNNNN.txt
   ...
```

Coco dataset looks like:  
```
 root   
   └── task_1
       ├── images
       │   ├── frame_000000.PNG
       │   ├── ...
       │   └── frame_NNNNNN.PNG  
       └── labels
           └── instances_default.json 
   ...
```