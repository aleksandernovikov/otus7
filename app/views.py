from flask import render_template, request
from flask_login import login_required, logout_user

from app import app, login_manager, db
from .models import User


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/registration/', methods=['GET'])
def registration_form():
    return render_template('registration.html')


@app.route('/registration/', methods=['POST'])
def registration_work():
    if request.form.get('password1') == request.form.get('password2'):
        login = request.form.get('login')
        db.session.add(
            User(username=login, password=request.form.get('password1'))
        )
        db.session.commit()

    return 'some work'


@app.route('/login/')
def login():
    return "you are logged in!"


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return "you are logged out"


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
