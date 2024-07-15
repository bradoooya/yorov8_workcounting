from ultralytics import YOLO
# モデルを選択
#model = YOLO("yolov8n.pt")
#model = YOLO("yolov8x.pt")
#model = YOLO("yolov8x-seg.pt")
model = YOLO('/home/houei/Desktop/development/yorov8/project_ML/model/best.pt')

model.to("cpu")


# 検出対象ファイル指定
#results = model("https://ultralytics.com/images/bus.jpg", save=True)
#results = model("./images/test2.jpg", save=True)
#results = model("./images/test2.mp4", save=True)

# WEBカメラからリアルタイム検出
confidence_threshold = 0.7
results = model(0 ,conf=confidence_threshold ,show=True)
for i in enumerate(results):
    print(i)


