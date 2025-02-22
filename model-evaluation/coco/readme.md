# COCO Evaluation Tool

## Overview

This Python class provides a comprehensive tool for evaluating object detection or segmentation results using the COCO (Common Objects in Context) evaluation method. It supports processing multiple ground truth and detection JSON files, performing detailed evaluations, and aggregating metrics.

## Features

- Evaluate object detection/segmentation results using COCO metrics
- Support for multiple ground truth and detection JSON file pairs
- Flexible IoU (Intersection over Union) type selection
- Output evaluation results to a file
- Calculate and display average metrics across multiple evaluations

## Requirements (requirements.txt)

- Python 3.8+
- pycocotools
- json
- collections

## Installation

```bash
pip install pycocotools
```

## Usage

### Initialization

```python
eval_tool = COCOEvalTool(json_gds=['/path/to/detections1.json', ...],
                         jsons_gts=['/path/to/groundtruth1.json', ...])
```

### Evaluation Methods

#### Evaluate Single File Pair

```python
eval_tool.base_eval(gt_path='ground_truth.json',
                    gd_path='detections.json',
                    iouType='bbox')
```

#### Batch Evaluation

```python
# Evaluate multiple JSON file pairs and save results
eval_tool.evaluate_by_list_json_files(output_file='evaluation_results.txt')
```

#### Display Average Metrics

```python
# Print average metrics
eval_tool.display_average_coco_metrics(filename='')

# Or save metrics to a JSON file
eval_tool.display_average_coco_metrics(filename='',
                                       file_path='averaged_metrics.json')
```

## Parameters

- `json_gds`: List of paths to detection JSON files
- `jsons_gts`: List of paths to ground truth JSON files
- `iouType`: Evaluation type (default: 'bbox')
  - 'bbox': Bounding box detection
  - 'segm': Segmentation masks

## Output

- Evaluation results include standard COCO metrics:
  - Average Precision (AP)
  - Average Recall (AR)
  - Metrics at different IoU thresholds

## Notes

- Ensure ground truth and detection files are paired correctly
- JSON files should follow COCO annotation format
