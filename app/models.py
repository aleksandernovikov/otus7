from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    Минимальный пользователь
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50))

    posts = db.relationship('Post', back_populates='author')

    def __repr__(self):
        return f'{__class__} {self.username}'


class Category(db.Model):
    """
    Категория для постов
    """
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)

    posts = db.relationship('Post', back_populates='category')

    def __repr__(self):
        return f'{__class__} {self.title}'


class Post(db.Model):
    """
    Посты
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey(User.id))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))

    title = db.Column(db.String(150), nullable=False, unique=True)
    text = db.Column(db.Text(), nullable=False)

    author = db.relationship(User, back_populates='posts')
    category = db.relationship(Category, back_populates='posts')

    def __repr__(self):
        return f'{__class__} {self.title}'
