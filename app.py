import os
import uuid

from flask import Flask, redirect, render_template, request
from flask import send_from_directory, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .models.base import Base
from .models.users import User

app = Flask(__name__)
engine = create_engine(
    'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        os.environ.get('POSTGRES_USER'),
        os.environ.get('POSTGRES_PASSWORD'),
        os.environ.get('POSTGRES_HOST'),
        os.environ.get('POSTGRES_PORT'),
        os.environ.get('POSTGRES_DB'),
    )
)
Base.metadata.create_all(engine)
session = Session(engine)


@app.route('/', methods=['GET'])
def index():
    """Homepage controller.

    Returns:
        redirect: user list page
    """
    return redirect(url_for('user_list'))


@app.route('/users', methods=['GET'])
def user_list():
    """Users list controller.

    Retrieve all users from the DB and show them in a list view.

    Returns:
        template: user list template.
    """
    users = get_users_data()
    return render_template('user_list.html', users=users)


@app.route('/users/add', methods=['GET'])
def users_add():
    """Users add controller.

    Returns:
        template: user add template.
    """
    return render_template('user_add.html')


@app.route('/save', methods=['POST'])
def save_user():
    """Save user data controller.

    Generate an unique `user_hash` for each user. This hash is used to identify
    users in URLs, to avoid exposing its ID column.

    Returns:
        redirect: list of users view, after save.
    """
    name = request.form['name']
    lastname = request.form['lastname']
    description = request.form['description']
    picture = request.files["picture"]
    user_hash = generate_user_hash()
    _upload_user_picture(user_hash, picture)
    _save_user(
        name=name, lastname=lastname,
        user_hash=user_hash, description=description
    )
    return redirect(url_for('user_list'))


def _upload_user_picture(user_hash, picture):
    upload_path = f'uploads/{user_hash}'
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    if picture.filename != '':
        picture.save(f'uploads/{user_hash}/picture.png')


def _save_user(**kwargs):
    """Save user data to database.
    """
    user = User(**kwargs)
    session.add(user)
    session.commit()


@app.route('/uploads/<user_hash>/<filename>')
def serve_image(filename, user_hash):
    return send_from_directory(
        f'uploads/{user_hash}/',
        filename
    )


@app.route('/users/<string:user_hash>/details', methods=['GET'])
def user_details(**kwargs):
    """User details controller.

    Retrieve user details view data.

    Returns:
        template: user details view.
    """
    user_hash = kwargs.get('user_hash')
    user_data = get_users_data(user_hash)
    return render_template('user_details.html', user=user_data)


@app.route('/users/<string:user_hash>/edit', methods=['POST', 'GET'])
def edit_user(**kwargs):
    """Edit user controller.

    Handle both HTTP calls: GET and POST, to fulfill the form with user
    data and save the new content.
    """
    user_hash = kwargs.get('user_hash')
    if request.method == 'GET':
        user_data = get_users_data(user_hash)
        return render_template(
            'user_edit.html',
            user=user_data
        )
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        description = request.form['description']
        picture = request.files["picture"]
        _upload_user_picture(user_hash, picture)
        _update_user_data(
            user_hash, name=name, lastname=lastname,
            description=description
        )
        return redirect(url_for('user_details', user_hash=user_hash))


def _update_user_data(user_hash, **kwargs):
    """Update user data in database.

    Args:
        user_hash (str): user to be updated.
    """
    values = {
        User.name: kwargs.get('name'),
        User.lastname: kwargs.get('lastname'),
        User.description: kwargs.get('description'),
    }
    session.query(User).filter_by(user_hash=user_hash).update(values)
    session.commit()


@app.route('/users/<string:user_hash>/delete', methods=['GET'])
def delete_user(**kwargs):
    """Delete user controller.

    Returns:
        redirect: user list view.
    """
    user_hash = kwargs.get('user_hash')
    session.query(User).filter_by(user_hash=user_hash).delete()
    session.commit()
    return redirect(url_for('user_list'))


def generate_user_hash():
    """Generate user hash.

    Unique identifier for users, to be used in views and URLs

    Returns:
        str: uuid string representation
    """
    return uuid.uuid4().hex


def get_users_data(user_hash=None):
    """Retrieve user data from database.

    It can return either all users data or one user data if `user_hash`
    is provided.

    Args:
        user_hash (str, optional): user identifier. Defaults to None.

    Returns:
        User: SQLAlchemy records for User model.
    """
    if not user_hash:
        return session.query(User).all()
    return session.query(User).filter_by(user_hash=user_hash).scalar()


@app.route('/users/search', methods=['POST'])
def user_search(**kwargs):
    """User search controller
    """
    search_data = request.form['search_value']
    users = _search_user(search_data)
    return redirect(url_for('user_list', users=users))


def _search_user(search_data):
    """Search users from database.
    """
    return session.query(User).filter(User.name.like('%' + search_data + '%')).all()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
