import sys
# Add the parent directory of coco_eval_tools to the path
sys.path.append('/home/eugene/Desktop/arch/machine-lerning-project/DroneDetector')

from coco.coco_eval_tool import COCOEvalTool

base_path = "/home/eugene/Desktop/arch/test-data"
coco = COCOEvalTool(
    json_gds = [f"{base_path}/task_194.json"],
    json_gts = [f"{base_path}/instances_default.json"]
) 

path_to_results = "output.txt"
coco.evaluate_by_list_json_files(path_to_results)
coco.display_average_coco_metrics(path_to_results)
