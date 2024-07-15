from pathlib import Path
from ultralytics import YOLO

model = YOLO('./model/best.pt')


jpg_files = Path(".").glob("*.jpg")

for file in jpg_files:
    model.predict(f'./{file}', save=True)