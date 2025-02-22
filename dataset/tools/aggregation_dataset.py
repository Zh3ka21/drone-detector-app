import shutil
from pathlib import Path


class DatasetAggregator:
    def __init__(self, input_folder, output_folder):
        """
        Args:
            input_folder (str or Path): Path to the folder containing train, val, and test datasets.
            output_folder (str or Path): Path to save the aggregated datasets and metadata.
        """
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def aggregate(self):
        """
        Performs the aggregation of datasets and generates metadata.
        """
        dataset_types = ['train', 'val', 'test']
        metadata = {
            "task_count_all": 0,
            "tasks": {"train": [], "val": [], "test": []},
            "image_counts": {dtype: 0 for dtype in dataset_types},
            "task_counts_by_type": {dtype: 0 for dtype in dataset_types}
        }

        for dataset_type in dataset_types:
            type_input_folder = self.input_folder / dataset_type
            type_output_images = self.output_folder / dataset_type / "images"
            type_output_labels = self.output_folder / dataset_type / "labels"

            type_output_images.mkdir(parents=True, exist_ok=True)
            type_output_labels.mkdir(parents=True, exist_ok=True)

            for task_folder in type_input_folder.iterdir():
                if task_folder.is_dir():
                    task_name = task_folder.name
                    metadata["tasks"][dataset_type].append(task_name)

                    image_count = self._aggregate_files(
                        source_folder=task_folder / "images",
                        target_folder=type_output_images,
                        task_name=task_name,
                    )
                    metadata["image_counts"][dataset_type] += image_count

                    self._aggregate_files(
                        source_folder=task_folder / "labels",
                        target_folder=type_output_labels,
                        task_name=task_name,
                    )

            metadata["task_counts_by_type"][dataset_type] = len(metadata["tasks"][dataset_type])

        metadata["task_count_all"] = sum(metadata["task_counts_by_type"].values())

        self._save_metadata(metadata)

    def _aggregate_files(self, source_folder, target_folder, task_name):
        """
        Aggregates files from the source folder to the target folder, renaming them with a task prefix.

        Args:
            source_folder (Path): Path to the folder containing the source files.
            target_folder (Path): Path to the folder where the aggregated files will be saved.
            task_name (str): Name of the task.
            prefix (str): Prefix for the new filenames.
        """
        if not source_folder.exists():
            return

        file_count = 0
        for idx, file in enumerate(source_folder.iterdir(), start=1):
            if file.is_file():
                new_name = f"{task_name}_{file.name}"
                shutil.copy(file, target_folder / new_name)
                file_count += 1

        return file_count

    def _save_metadata(self, metadata):
        """
        Saves the metadata to a file.

        Args:
            metadata (dict): Metadata dictionary containing task information.
        """
        metadata_file = self.output_folder / "metadata.txt"
        with metadata_file.open("w") as f:
            f.write(f"Count tasks: {metadata['task_count_all']}\n")

            f.write("\n")
            for dataset_type, count in metadata["task_counts_by_type"].items():
                f.write(f"{dataset_type.capitalize()} task count: {count}\n")

            f.write("\n")
            for dataset_type, count in metadata["image_counts"].items():
                f.write(f"{dataset_type.capitalize()} image count: {count}\n")

            for dataset_type, tasks in metadata["tasks"].items():
                f.write("\n")
                f.write(f"{dataset_type.capitalize()} tasks:\n")
                for task in tasks:
                    f.write(f"{task.split('_')[-1]}\n")
