from ultralytics import YOLO
# モデルを選択
model = YOLO('./model/best.pt')

#実行デバイス指定
model.to("cpu")

# WEBカメラからリアルタイム検出
confidence_threshold = 0.7
results = model(source=0 ,conf=confidence_threshold ,show=False, stream=True)

"""
for i in enumerate(results):
    print(i)
"""

# 検出結果の個数をプリント
for result in results:
    num_detections = len(result.boxes)  # 検出されたバウンディングボックスの数を取得
    print(f"Number of detections: {num_detections}")
