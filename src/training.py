import comet_ml
import torch
from ultralytics import YOLO


def train():
    API_KEY = ""
    PROJECT_NAME = ""
    MODEL_PATH = "models/yolov8m.pt"

    if torch.cuda.is_available():
        model = YOLO(MODEL_PATH)

        torch.cuda.empty_cache()
        comet_ml.init(api_key=API_KEY,
                      project_name=PROJECT_NAME)

        model.train(data='config/config.yaml',
                    project=PROJECT_NAME,
                    epochs=150,
                    batch=32,
                    imgsz=640,
                    device=0,
                    patience=10,
                    save_period=10,
                    workers=12,
                    box=7.5,
                    hsv_h=0.015,
                    hsv_s=0.7,
                    hsv_v=0.4,
                    translate=0.1,
                    scale=0.5,
                    shear=0.05,
                    degrees=0.1,
                    flipud=0.5,
                    fliplr=0.5
                    )


if __name__ == "__main__":
    train()
