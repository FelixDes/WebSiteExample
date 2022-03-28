# WebSiteExample
Flask+SQLAlchemy website example

Applied features:
* registration and logining using flask_login
* saving user data in database using SQLAlchemy
* interactive map using [Yandex Maps](https://yandex.ru/dev/maps/archive/doc/jsapi/1.x/dg/tasks/quick-start.html)
* light/dark theme switcher
* ability to send message from site to database
* messages to json parser

Site was placed in [Heroku](https://fkn-web-tech.herokuapp.com/)

For running application from terminal do those steps:
1. Install [Python 3.9.9](https://www.python.org/downloads/release/python-399/)
2. Set absolute python path venv/pyvenv.cfg to home, base-prefix, base-exec-prefix and base-executable
3. Set absolute database path to DATABASE_PATH in main using {/} for every level (something like: C:/Users/user/PythonProject/db/main.db)
4. Open terminal and type: {Path to project}\venv\Scripts\python.exe {Path to project}\main.py
5. Open link from the terminal