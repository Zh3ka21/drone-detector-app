from .coco_formatter import CocoFormatter
from .yolo_formatter import YoloFormatter


class FormatFabric:
    def create(self, type: str):
        match type:
            case "coco": return CocoFormatter()
            case "yolo": return YoloFormatter()
