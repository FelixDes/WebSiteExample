from flask import Flask, render_template
#from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send
from werkzeug.security import check_password_hash

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
app.config[
    'SECRET_KEY'] = "_ti{qxjtrdygXpNadwPPGaOh{zBawz^GBBpoIU|qpGpEVzgRzqhqeZ]hv_oeBhb|WBkmdRANtw}akIfMgOLm{r]ZnYiZcBFXZz{'"


def main():
    app.run(port=8081)


@app.route("/")
def index():
    return render_template("index.html", title="ОАО Подземстрой")

@app.route("/about_author")
def about_author():
    return render_template("about_author.html", title="About author")

main()