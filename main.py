from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from Forms.user import RegisterForm, LoginForm, RequestForm
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
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')  # Выход из ученой записи
@login_required
def logout():
    logout_user()
    return redirect("/")  # Возврат на основанную страницу


@app.route("/")
def index():  # Главная страница
    return render_template("index.html", anonymous=current_user.is_anonymous,
                           c_user=current_user, title="ОАО Подземстрой")


@app.route("/about_author")
def about_author():
    return render_template("about_author.html", anonymous=current_user.is_anonymous,
                           c_user=current_user, title="About author")


@app.route('/registration', methods=['GET', 'POST'])
def registration():  # Регистрация нового пользователя
    title = "Регистрация"
    db_sess = db_session.create_session()
    form_registration = RegisterForm()

    if form_registration.validate_on_submit():
        if form_registration.password.data != form_registration.password_again.data:
            # При различных паролях в первом и втором поле ввода
            return render_template('registration.html', anonymous=current_user.is_anonymous,
                                   c_user=current_user, title=title, form=form_registration,
                                   message="Пароли не совпадают")

        if db_sess.query(User).filter(User.email == form_registration.email.data).first():
            # При попытке создать пользователя на уже имеющуюся в базе данных почту
            return render_template('registration.html', anonymous=current_user.is_anonymous, c_user=current_user,
                                   title=title, form=form_registration,
                                   message="Такой пользователь уже есть")

        user = User(name=form_registration.name.data, email=form_registration.email.data)
        user.set_password(form_registration.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')  # Переадресация на страницу входа
    return render_template('registration.html', anonymous=current_user.is_anonymous,
                           c_user=current_user, title=title, form=form_registration)


@app.route('/login', methods=['GET', 'POST'])
def login():  # Вход в аккаунт
    db_sess = db_session.create_session()
    title = "Войти"
    form_login = LoginForm()
    if form_login.email.data and form_login.password.data:
        user = db_sess.query(User).filter(User.email == form_login.email.data).first()

        if not user:
            # Если пользователь отсутствует в базе данных
            return render_template('login.html', anonymous=current_user.is_anonymous,
                                   c_user=current_user, title=title, form=form_login,
                                   message="Такого пользователя нет")

        elif not check_password_hash(user.hashed_password, form_login.password.data):
            return render_template('login.html', anonymous=current_user.is_anonymous,
                                   c_user=current_user, title=title, form=form_login, message="Неверный пароль")

        # Если пароль из базы данных не совпадает с введенным
        else:
            login_user(user, remember=form_login.remember_me.data)
            return redirect('/')  # Корректный вход в учетную запись
            # Происходит переадрессация на главную страницу
    return render_template('login.html', anonymous=current_user.is_anonymous,
                           c_user=current_user, title=title, form=form_login, message='')


@app.route('/request', methods=['GET', 'POST'])
def make_request():
    form_request = RequestForm()

    if form_request.validate_on_submit():
        if str(current_user).split('>')[0] != '<User':
            return redirect('/login')
        else:
            db_sess = db_session.create_session()
            message = Message(user_name=current_user.name, text=form_request.text, contact=current_user.email)
            db_sess.add(message)
            return redirect('/')
    return render_template('make_request.html', anonymous=current_user.is_anonymous, c_user=current_user,
                           form=form_request)


if __name__ == '__main__':
    main()
