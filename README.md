# 📷 Webcam Proxy Stream（Flask + MJPG-streamer）

## 🇯🇵 概要 / Overview

このアプリは、**MJPG-streamer** が配信する MJPEG 映像を **Flask** を使ってブラウザへ再配信する軽量なプロキシアプリです。  
ローカルネットワーク上の Webカメラ映像を、簡単にブラウザで視聴できます。

This is a lightweight **Flask proxy app** that receives MJPEG streams from **MJPG-streamer** and redistributes them to the browser.  
Use it to view webcam feeds (e.g., from Raspberry Pi) in your browser with ease.

---

## 🖥️ デモ / Demo

ローカル動作イメージ：

Local usage preview:


---

## ⚙️ 使用技術 / Tech Stack

- Python 3.11  
- Flask  
- requests ライブラリ  
- HTML / CSS

---

## 🚀 セットアップ手順 / Setup
```
# リポジトリをクローン
git clone https://github.com/yuppe44/webcam_app.git
cd webcam_app

# （任意）仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# アプリ起動
python app.py
```

## ブラウザで以下にアクセス： / Open your browser and go to:
```
http://localhost:8081
```
## 🔗 MJPG-streamer 映像URL / MJPG-streamer URL

### デフォルトでは以下のURLから映像を受信します： / By default, the app expects the MJPEG stream at:
```
http://localhost:8080/?action=stream
```
### 必要に応じて app.py 内の MJPEG_STREAM_URL を編集してください： / To change this, modify MJPEG_STREAM_URL in app.py: 
```
MJPEG_STREAM_URL = 'http://<your-streamer-ip>:<port>/?action=stream'
```
## 📁 ディレクトリ構成 / Project Structure
```
webcam_app/
├── app.py             # Flask アプリ本体 / Flask main app
├── templates/
│   └── index.html     # フロントエンド HTML / Frontend page
├── requirements.txt   # 依存ライブラリ / Dependencies
```

## ⚠️ 注意点 / Notes
	•	MJPG-streamer が別ホストで動作している必要があります
	•	映像は OpenCV を使わずそのまま中継されます
	•	外部に公開する場合はセキュリティ対策が必要です
	•	MJPG-streamer must be running and accessible
	•	No OpenCV used — MJPEG is passed directly
	•	If deployed publicly, secure the app properly

⸻

## 📚 参考リンク / References
![MJPG-streamer GitHub](https://github.com/jacksonliam/mjpg-streamer)
Flask Documentation
Requests Library

⸻

## 🧠 作者 / Author

@yuppe44

