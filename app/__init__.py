from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static/', static_folder='static')
app.config['SECRET_KEY'] = "qwertyhnbnmm123536778_secret_key"
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models

if __name__ == '__main__':
    app.run()
