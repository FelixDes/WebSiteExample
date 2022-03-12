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
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = \
    "_ti{qxjtrdygXpNadwPPGaOh{zBawz^GBBpoIU|qpGpEVzgRzqhqeZ]hv_oeBhb|WBkmdRANtw}akIfMgOLm{r]ZnYiZcBFXZz{'"


def main():
    db_session.global_init("db/main.db")

    app.run(port=8081)


@login_manager.user_loader
def load_user(user_id):  # Получение пользовотеля по id из базы данных
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')  # Выход из учётной записи
@login_required
def logout():
    logout_user()
    return redirect("/")  # Возврат на основную страницу


@app.route("/")
def index():
    try:
        is_admin = current_user.is_admin
    except AttributeError:  # В случае анонимного пользователя
        is_admin = False
    return render_template("index.html", anonymous=str(current_user).split('>')[0] == '<User', admin=is_admin,
                           c_user=current_user, title="ОАО Подземстрой")


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


@app.route('/login', methods=['GET', 'POST'])
def login():  # Вход в аккаунт
    form = LoginForm()

    if form.email.data and form.password.data:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if not user:
            # Если пользователь отсутствует в базе данных
            return render_template('login.html', title="Войти", form=form,
                                   message="Такого пользователя нет")

        elif not check_password_hash(user.hashed_password, form.password.data):
            return render_template('login.html', title="Войти", form=form, message="Неверный пароль")

        # Если пароль из базы данных не совподает с введённым
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')  # Корректный вход в учётную запись
            # Происходит переадрессация на главную страницу
    return render_template('login.html', title="Войти", form=form, message='')


if __name__ == '__main__':
    main()
