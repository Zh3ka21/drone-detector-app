import random
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


class DatasetSplitter:
    """
    A utility class for splitting datasets into training, validation, and testing subsets.

    Attributes:
        input_folder (str or Path): Path to the input folder containing the dataset
        output_folder (str or Path): Path to the folder where the split datasets will be saved.
        train_ratio (float): Proportion of the dataset to allocate for training
        val_ratio (float): Proportion of the dataset to allocate for validation
        test_ratio (float): Proportion of the dataset to allocate for testing
        seed (int): Random seed for reproducibility
    """

    def __init__(self, input_folder, output_folder, train_ratio=0.75, val_ratio=0.15, test_ratio=0.1, seed=42):
        """
        Initializes the DatasetSplitter class with specified parameters.

        Args:
            input_folder (str or Path): Path to the folder containing the dataset.
            output_folder (str or Path): Path to save the split datasets.
            train_ratio (float): Proportion of data for training.
            val_ratio (float): Proportion of data for validation.
            test_ratio (float): Proportion of data for testing.
            seed (int): Random seed for reproducibility.

        Raises:
            ValueError: If the ratios are not between 0 and 1 or their sum does not equal 1.
        """
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

        if not (0 <= self.train_ratio <= 1 and 0 <= self.val_ratio <= 1 and 0 <= self.test_ratio <= 1):
            raise ValueError("Ratios must be between 0 and 1.")
        if round(self.train_ratio + self.val_ratio + self.test_ratio, 5) != 1.0:
            raise ValueError("The sum of train, val, and test ratios must equal 1.")

        self.output_folder.mkdir(parents=True, exist_ok=True)

    def folders(self, input_folder: str, output_folder: str):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)

    def ratio(self, ratio: tuple):
        if len(ratio) == 3:
            raise ValueError("The ratios len must be 3")
        if round(self.train_ratio + self.val_ratio + self.test_ratio, 5) != 1.0:
            raise ValueError("The sum of train, val, and test ratios must equal 1.")

        self.train_ratio, self.val_ratio, self.test_ratio = ratio

    def split(self):
        """
        Splits the dataset into training, validation, and testing subsets.

        This method randomly shuffles the top-level folders in the input dataset and
        splits them into three subsets based on the specified ratios.
        """
        all_folders = [folder for folder in self.input_folder.iterdir() if folder.is_dir()]

        random.seed(self.seed)
        random.shuffle(all_folders)

        total = len(all_folders)
        train_split = int(total * self.train_ratio)
        val_split = train_split + int(total * self.val_ratio)

        train_folders = all_folders[:train_split]
        val_folders = all_folders[train_split:val_split]
        test_folders = all_folders[val_split:]

        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(self._copy_folders, train_folders, self.output_folder / "train")
            executor.submit(self._copy_folders, val_folders, self.output_folder / "val")
            executor.submit(self._copy_folders, test_folders, self.output_folder / "test")

        print("Dataset successfully shuffled and split!")
        print(f"Training set: {len(train_folders)} folders")
        print(f"Validation set: {len(val_folders)} folders")
        print(f"Test set: {len(test_folders)} folders")

    @staticmethod
    def _copy_folders(folders, target_folder):
        """
        Copies a list of folders to the target directory.

        Args:
            folders (list[Path]): List of folder paths to copy.
            target_folder (Path): Destination directory for the folders.
        """
        target_folder.mkdir(parents=True, exist_ok=True)
        for folder in folders:
            shutil.copytree(folder, target_folder / folder.name)
