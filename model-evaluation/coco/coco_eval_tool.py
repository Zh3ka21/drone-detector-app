import os
import sys
import json
from collections import defaultdict
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from coco.utils import sort_paths_by_number, parse_eval_line

class COCOEvalTool:
    def __init__(self, json_gds: list[str], json_gts: list[str]):
        self.json_gds = json_gds
        self.json_gts = json_gts

    def _base_eval(self, gt_path: str, gd_path: str, iouType: str = 'bbox'):
        """Evaluates a single pair of ground truth and detection files using COCO evaluation.

        Args:
            gt_path (str): Path to the ground truth JSON file.
            gd_path (str): Path to the detection JSON file.
            iouType (str, optional): Type of evaluation ('bbox', 'segm', etc.). Default is 'bbox'.
        """
        # Initialize COCO ground truth and detection objects
        coco_gt = COCO(gt_path)
        coco_det = coco_gt.loadRes(gd_path)

        # Perform evaluation
        coco_eval = COCOeval(coco_gt, coco_det, iouType)
        coco_eval.evaluate()
        coco_eval.accumulate()
        coco_eval.summarize()

    def evaluate_by_list_json_files(self, output_file: str = "coco/results/output.txt"):
        """
        Evaluates multiple ground truth and detection JSON files and writes the results to an output file.
        
        Parameters:
        - output_file (str): Path to the output file where evaluation results will be saved.
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Sort the paths by numbers (To aggregate JSON with ground truths and JSON with detections)
        sorted_gds = sort_paths_by_number(self.json_gds)
        sorted_gts = sort_paths_by_number(self.json_gts)
        
        # Redirect sys.stdout to the output file
        sys_output = sys.stdout
        with open(output_file, 'w') as f:
            sys.stdout = f
            for gt_path, gd_path in zip(sorted_gts, sorted_gds):
                self._base_eval(gt_path, gd_path)           
        sys.stdout = sys_output

    def display_average_coco_metrics(self, filename: str = '', file_path: str = "coco/results/output.json"):
        """
        Computes and displays the average COCO metrics from a summary output file.

        Parameters:
        - filename (str): Path to the file containing evaluation results.
        - file_path (str): Path to save the averaged results as a JSON file. If not provided, results are printed.
        """
        # Initialize a dictionary to store the sums and counts
        metrics = defaultdict(lambda: {'sum': 0, 'count': 0})

        # Read the evaluation results from the file
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = parse_eval_line(line)
                if key and value is not None:
                    metrics[key]['sum'] += value
                    metrics[key]['count'] += 1

        # Calculate averages
        averages = {key: data['sum'] / data['count'] for key, data in metrics.items() if data['count'] > 0}

        # Output the results
        if not file_path:
            # Print the results
            for key, avg in averages.items():
                print(f"{key} = {avg:.3f}")
        else:
            # Save the results to a JSON file
            with open(file_path, 'w') as json_file:
                json.dump(averages, json_file, indent=4)

    @staticmethod
    def display_txt_file(output_file):
        if os.path.exists(output_file) and output_file.endswith('.txt'):
            with open(output_file, 'r') as file:
                content = file.read()
                print(content)
        else:
            print(f"File {output_file} does not exist or is not a .txt file.")
