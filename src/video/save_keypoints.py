import csv
from pathlib import Path

def write_row(keypoints):
    gesture = "ok_sign"
    path = Path(fr"C:\GERARD\Coding\Projects\jarvis/datasets/gestures/{gesture}.csv")
    path.touch(exist_ok=True)
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([gesture] + list(keypoints))