import torch
from ultralytics import YOLO

if __name__ == '__main__':
    # Load model
    model = YOLO(r".\models\yolo26s-pose.pt")  # build a new model from YAML

    print(f"Cuda available: {torch.cuda.is_available()}")

    # Train model
    results = model.train(
        data=r"datasets\hand-keypoints\hand-keypoints.yaml",
        epochs=100,
        imgsz=640,
        patience=100,
        device=0 if torch.cuda.is_available() else 'cpu',
        project=r".\hand-keypoints"
    )