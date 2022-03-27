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
    app.run(port=9999)


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
                           c_user=current_user, title="ОАО Подземстрой", message_lst=get_message_list())


@app.route("/about_author")
def about_author():
    return render_template("about_author.html", anonymous=current_user.is_anonymous,
                           c_user=current_user, title="About author")


@app.route('/registration', methods=['GET', 'POST'])
def registration():  # Регистрация нового пользователя
    title = "Регистрация"
    form_registration = RegisterForm()

    if form_registration.validate_on_submit():
        if form_registration.password.data != form_registration.password_again.data:
            # При различных паролях в первом и втором поле ввода
            return render_template('registration.html', anonymous=current_user.is_anonymous, c_user=current_user,
                                   title=title, form=form_registration, message="Пароли не совпадают")

        if is_user_in_database(form_registration.email.data):
            # При попытке создать пользователя на уже имеющуюся в базе данных почту
            return render_template('registration.html', anonymous=current_user.is_anonymous, c_user=current_user,
                                   title=title, form=form_registration, message="Такой пользователь уже есть")

        add_user(form_registration.name.data, form_registration.email.data, form_registration.password.data)

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
        if current_user.is_anonymous:
            return redirect('/login')
        else:
            add_message(current_user.name, form_request.text.data, current_user.email)
            return redirect('/')
    return render_template('make_request.html', anonymous=current_user.is_anonymous, c_user=current_user,
                           form=form_request)


def get_message_list():
    db_sess = db_session.create_session()
    message_lst = []
    for i in db_sess.query(Message).filter():
        message_lst.append((f"<strong>{i.user_name.capitalize()}: </strong>" f"{i.text} <sub>{i.created_date.strftime('%H:%M')} {i.contact}</sub>", i.id))
    print(message_lst)
    return message_lst


def is_user_in_database(email):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.email == email).first()


def add_user(name, email, password):
    db_sess = db_session.create_session()
    user = User(name=name, email=email)
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()


def add_message(user_name, text, contact):
    db_sess = db_session.create_session()
    message = Message(user_name=user_name, text=text, contact=contact)
    db_sess.add(message)
    db_sess.commit()


if __name__ == '__main__':
    main()
