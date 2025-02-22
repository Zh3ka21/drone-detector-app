import os
from io import BytesIO
from PIL import Image
from .idata import IData


class CocoData(IData):
    def __init__(self):
        self.images = []
        self.annotations = None

    def download_images(self, image_dir: str):
        for image in self.images:
            image_path = os.path.join(image_dir, image["filename"].split("/")[-1].replace("png", "jpg"))
            image_data = BytesIO(image["data"])

            with Image.open(image_data) as img:
                img.convert("RGB").save(image_path, format="JPEG")

    def download_data(self, data_dir: str):
        if self.annotations:
            json_path = os.path.join(data_dir, self.annotations["filename"].split("/")[-1])
            with open(json_path, 'w', encoding='utf-8') as file:
                file.write(self.annotations["data"])
