from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Category, Post


def get_or_create(model, **kwargs):
    """
    Получить запись или создать, если ее нет
    """
    object_default_data = {}
    if 'default' in kwargs:
        object_default_data = kwargs.pop('default')
    try:
        object = db.session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        object = model(**kwargs, **object_default_data)
        db.session.add(object)
        db.session.flush()
        db.session.commit()
    return object


if __name__ == '__main__':
    username, password = 'admin', 'password'
    user = get_or_create(User, username=username, default={'password': generate_password_hash(password)})
    print(user)

    categories = {'frontend', 'backend'}
    for category in categories:
        category = get_or_create(Category, title=category)
        print(category)

        title = f'new post in {category.title} category'.capitalize()
        text = f'{category.title} post content ' * 20
        post = get_or_create(
            Post,
            author_id=user.id,
            category_id=category.id,
            title=title,
            default={'text': text.capitalize()}
        )
        print(post)
