import zipfile

from .iformat import IFormatter
from .data.idata import IData
from .data.yolo_data import YoloData


class YoloFormatter(IFormatter):
    TYPE = "YOLO 1.1"

    def __init__(self):
        self.exception = ("label_colors.txt", "obj.names", "obj.data", "train.txt")

    def formatting(self, zip_data: zipfile.ZipFile) -> IData:
        data = YoloData()

        for file_info in zip_data.infolist():
            file_name = file_info.filename

            if file_name in self.exception:
                continue

            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', ".bmp")):
                with zip_data.open(file_name) as image_file:
                    image_bytes = image_file.read()
                    data.images.append({'filename': file_name, 'data': image_bytes})

            elif file_name.lower().endswith('.txt'):
                with zip_data.open(file_name) as txt_file:
                    txt_data = txt_file.read().decode('utf-8')
                    data.labels.append({'filename': file_name, 'data': txt_data})

        return data
