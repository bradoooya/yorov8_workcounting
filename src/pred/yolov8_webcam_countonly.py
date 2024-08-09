from ultralytics import YOLO
import sys
sys.path.append("/home/houei/Desktop/development/yorov8/project_ML/src")

from utils.utils import LCD, LCDMessage

# モデルを選択
model = YOLO('./model/best.pt')

#実行デバイス指定
model.to("cpu")

# WEBカメラからリアルタイム検出
confidence_threshold = 0.7
results = model(source=0 ,conf=confidence_threshold ,show=False, stream=True)

try:
    lcd =  LCD()
    lcd_pred = LCDMessage(lcd)
    for result in results:
        num_detections = len(result.boxes)  # 検出されたバウンディングボックスの数を取得
        text = f"Number of detections: {num_detections}"
        print(text)
        lcd_pred.display_message(text, display_duration=10)
except Exception as e:
    print(e)
except ValueError as e:
    print(e)
finally:
    lcd.clear()
    
