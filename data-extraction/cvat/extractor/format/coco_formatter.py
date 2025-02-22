import zipfile
from .iformat import IFormatter
from .data.idata import IData
from .data.coco_data import CocoData


class CocoFormatter(IFormatter):
    TYPE = "COCO 1.0"

    def __init__(self):
        pass

    def formatting(self, zip_data: zipfile.ZipFile) -> IData:
        data = CocoData()

        for file_info in zip_data.infolist():
            file_name = file_info.filename

            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', ".bmp")):
                with zip_data.open(file_name) as image_file:
                    image_bytes = image_file.read()
                    data.images.append({'filename': file_name, 'data': image_bytes})

            elif file_name.lower().endswith('.json'):
                with zip_data.open(file_name) as json_file:
                    json_data = json_file.read().decode('utf-8')
                    data.annotations = {'filename': file_name, 'data': json_data}

        return data
