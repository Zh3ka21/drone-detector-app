import json
import os
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()


class YoloToCoco:
    def __init__(self, dataset_path, output_path, image_extension=".png"):
        self.dataset_path = Path(dataset_path)
        self.output_path = Path(output_path)
        self.image_extension = image_extension
        self.annotation_id = 1  # Keep annotation IDs unique across images

        # Define categories based on environment variables
        self.categories = [
            {"id": 1, "name": os.getenv("CATEGORY_ID_1", "class_1"), "supercategory": ""},
            {"id": 2, "name": os.getenv("CATEGORY_ID_2", "class_2"), "supercategory": ""},
            {"id": 3, "name": os.getenv("CATEGORY_ID_3", "class_3"), "supercategory": ""},
            {"id": 6, "name": os.getenv("CATEGORY_ID_6", "class_6"), "supercategory": ""},
            {"id": 9, "name": os.getenv("CATEGORY_ID_9", "class_9"), "supercategory": ""},
            {"id": 10, "name": os.getenv("CATEGORY_ID_10", "class_10"), "supercategory": ""}
        ]

        self.info = {
                     "contributor": os.getenv("INFO_CONTRIBUTOR"),
                     "date_created": os.getenv("INFO_DATE_CREATED"),
                     "description": os.getenv("INFO_DESCRIPTION"),
                     "url": os.getenv("INFO_URL"),
                     "version": os.getenv("INFO_VERSION"),
                     "year": os.getenv("INFO_YEAR")
        }


    def convert(self):
        """Process each task directory separately."""
        for task_path in sorted(self.dataset_path.glob("task_*")):
            labels_path = task_path / "labels"
            images_path = task_path / "images"

            if not labels_path.exists() or not images_path.exists():
                print(f"Skipping {task_path.name}, missing labels or images folder.")
                continue

            # Prepare COCO dataset structure for this task
            coco_dataset = {
                "licenses": json.loads(os.getenv("LICENSES", "[]")),
                "info": self.info,
                "categories": self.categories,
                "images": [],
                "annotations": [],
            }

            image_id_map = {}  # Local mapping for image filenames -> COCO image_id
            image_counter = 1  # Start image_id from 1 (like CVAT)

            for label_file in tqdm(labels_path.glob("*.txt"), desc=f"Processing {task_path.name}"):
                image_name = label_file.stem + self.image_extension
                image_path = images_path / image_name

                if not image_path.exists():
                    print(f"Warning: Image {image_name} not found, skipping.")
                    continue

                # Assign an image_id
                image_id = image_id_map.get(image_name, image_counter)
                if image_name not in image_id_map:
                    image_id_map[image_name] = image_counter
                    coco_dataset["images"].append({
                        "id": image_counter,
                        "file_name": image_name,
                        "width": 1920,  # Adjust if needed
                        "height": 1080   # Adjust if needed
                    })
                    image_counter += 1

                # Convert annotations
                with open(label_file, "r") as f:
                    for line in f.readlines():
                        parts = line.strip().split()
                        if len(parts) < 5:
                            continue  # Invalid format

                        category_id = int(parts[0]) + 1  # Shift YOLO class ID (+1)
                        x_center, y_center, width, height = map(float, parts[1:5])

                        # Convert YOLO bbox format to COCO format
                        bbox = [
                            round((x_center - width / 2) * 1920, 4),  # x_min
                            round((y_center - height / 2) * 1080, 4),  # y_min
                            round(width * 1920, 4),  # bbox_width
                            round(height * 1080, 4)  # bbox_height
                        ]


                        # Construct COCO annotation format
                        annotation = {
                            "id": self.annotation_id,
                            "image_id": image_id,
                            "category_id": category_id,
                            "bbox": bbox,
                            "area": bbox[2] * bbox[3],
                            "iscrowd": 0,
                            "segmentation": [],  
                            "attributes": {
                                "occluded": False,
                                "rotation": 0.0,
                                "track_id": 0,
                                "keyframe": True
                            }
                        }
                        coco_dataset["annotations"].append(annotation)
                        self.annotation_id += 1

            # Save JSON in task-specific folder
            task_output_path = self.output_path / task_path.name
            task_output_path.mkdir(parents=True, exist_ok=True)
            output_file = task_output_path / f"{task_path.name}_coco.json"

            with open(output_file, "w") as f:
                json.dump(coco_dataset, f)

            print(f"COCO annotations saved at {output_file}")
