from pathlib import Path
from ultralytics import YOLO
import os
from datetime import datetime

#ディレクトリ指定
current_dir = Path.cwd() 
project_dir = current_dir

#モデルのロード
model_path = project_dir / './model/best.pt'
model = YOLO(model_path)

#画像ディレクトリのパス
image_dir = project_dir / "/data/images/for_pred"

#予想結果の保存先のパス
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
save_dir = project_dir / f'/results/run_pred_test/{timestamp}'
os.makedirs(save_dir, mode=0o777, exist_ok=True) # 保存先フォルダが存在しない場合は作成

#画像ディレクトリからjpgファイルを取得
jpg_files = image_dir.glob("*.jpg")

for file in jpg_files:
    #推論の実行と結果の保存
    results = model.predict(str(file))

    # 各結果を保存
    for i, result in enumerate(results):
        save_path = os.path.join(save_dir, f'{file.stem}_result_{i}_.jpg')
        result.save(save_path)

