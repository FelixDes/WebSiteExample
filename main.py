from flask import Flask, render_template
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# from flask_socketio import SocketIO, send
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from Forms.user import RegisterForm, LoginForm
from data import db_session
from data.messages import Message
from data.users import User

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
app.config['SECRET_KEY'] = \
    "_ti{qxjtrdygXpNadwPPGaOh{zBawz^GBBpoIU|qpGpEVzgRzqhqeZ]hv_oeBhb|WBkmdRANtw}akIfMgOLm{r]ZnYiZcBFXZz{'"


def main():
    db_session.global_init("db/main.db")

    app.run(port=8081)


@app.route("/")
def index():
    return render_template("index.html", title="ОАО Подземстрой")


@app.route("/about_author")
def about_author():
    return render_template("about_author.html", title="About author")


@app.route('/registration', methods=['GET', 'POST'])
def registration():  # Регистрация нового пользователя
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title="Регистрация", form=form,
                                   message="Пароли не совпадают")
            # При различных паролях в первом и втором поле ввода

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title="Регистрация", form=form,
                                   message="Такой пользователь уже есть")
            # При попытке создать пользователя на уже имеющуюся в базе данных почту
        user = User(  # Создание нового пользователя
            name=form.name.data,
            email=form.email.data,
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')  # Переадресация на страницу входа
    return render_template('registration.html', title="Регистрация", form=form)


if __name__ == '__main__':
    main()
