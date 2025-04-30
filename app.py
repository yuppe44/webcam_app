from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
    return render_template('stream.html', stream_url="http://localhost:8081/?action=stream")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8443, ssl_context=('cert.pem', 'key.pem'))