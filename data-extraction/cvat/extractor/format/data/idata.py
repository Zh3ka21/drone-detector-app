from abc import ABC, abstractmethod


class IData(ABC):
    @abstractmethod
    def download_images(self, image_dir: str):
        pass

    @abstractmethod
    def download_data(self, data_dir: str):
        pass
