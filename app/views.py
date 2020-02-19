import logging

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, login_manager, db
from .models import User, Post, Category

logger = logging.getLogger(__name__)


@app.route('/')
def home():
    posts = Post.query.limit(2).all()
    return render_template('index.html', posts=posts)


@app.route('/signup/', methods=['GET'])
def registration():
    return render_template('signup_form.html')


@app.route('/signup/', methods=['POST'])
def registration_process():
    """
    User registration
    """
    form = request.form
    check = all([
        form.get('login'), form.get('password1'),
        form.get('password1') == form.get('password2')
    ])
    if check:
        pass_hash = generate_password_hash(request.form.get('password1'))
        db.session.add(
            User(
                username=request.form.get('login'),
                password=pass_hash
            )
        )
        try:
            db.session.commit()
            flash('Успешная регистрация, можно войти, используя свои данные')
            return redirect(url_for('login'))
        except Exception as e:
            logger.exception(e)

    flash('Неверное имя пользователя или пароль')
    return redirect(url_for('registration'))


@app.route('/login/', methods=['GET'])
def login():
    return render_template('login_form.html')


@app.route('/login/', methods=['POST'])
def login_process():
    username, password = request.form.get('login'), request.form.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if check_password_hash(user.password, password):
            login_user(user)
            flash(f'Добро пожаловать {username}')
            return redirect(url_for('home'))

        flash('Неверное имя пользователя или пароль')
        return redirect(url_for('login'))

    flash('Для авторизации необходимо указать имя пользователя и пароль')
    return redirect(url_for('login'))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


@app.route('/posts/')
def post_list():
    posts = Post.query.all()
    return render_template('post_list.html', posts=posts)


@app.route('/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post.html', post=post)


@app.route('/category/<int:category_id>')
def get_category_posts(category_id):
    posts = Post.query.filter_by(category_id=category_id).all()
    return render_template('post_list.html', posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def context_processor():
    def all_categories():
        return Category.query.all()

    def last_posts():
        return Post.query.order_by(Post.created.desc()).limit(3).all()

    return {
        'all_categories': all_categories(),
        'last_posts': last_posts()
    }
