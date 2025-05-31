import os
import requests
import threading
import time
import cv2

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask import Response, stream_with_context
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/video_proxy')
@login_required
def video_proxy():
    upstream = requests.get("http://localhost:8081/?action=stream", stream=True)

    def generate():
        for chunk in upstream.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    return Response(stream_with_context(generate()), content_type=upstream.headers['Content-Type'])

# ユーザークラス
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# ログインユーザー認識
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == os.getenv("LOGIN_USER") and pw == os.getenv("LOGIN_PASS"):
            login_user(User(user), remember=True)
            return redirect(url_for('stream'))
        else:
            return "Invalid credentials", 403
    return render_template('login.html')

@app.route('/stream')
@login_required
def stream():
    # mjpg-streamer で配信されるストリームURLを埋め込む
    return render_template('stream.html', stream_url=url_for('video_proxy'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def detect_and_record():
    cap = cv2.VideoCapture(0)  # Use device 0 (adjust as needed)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = any(cv2.contourArea(c) > 5000 for c in contours)

        if motion_detected:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out = cv2.VideoWriter(f'./record/recording_{timestamp}.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (320, 240))
            start_time = time.time()
            print(f"Motion detected! Recording started at {timestamp}.")

            while time.time() - start_time < 10:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            out.release()
            print(f"Recording saved: recording_{timestamp}.avi")

        frame1 = frame2
        ret, frame2 = cap.read()
        if not ret:
            break
    cap.release()

if __name__ == '__main__':
    motion_thread = threading.Thread(target=detect_and_record, daemon=True)
    motion_thread.start()
    app.run(host='192.168.11.11', debug=True, port=8443, ssl_context=('cert.pem', 'key.pem'))