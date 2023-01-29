import sqlite3
import uuid

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', names={})


@app.route('/save', methods=['POST'])
def save_name():
    name = request.form['name']
    lastname = request.form['lastname']
    conn = sqlite3.connect('users_db.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id text,
        name text,
        lastname text
    )
    """)
    conn.commit()

    user_id = generate_user_id()
    cursor.execute("""
    INSERT INTO users (user_id, name, lastname)
    VALUES (?, ?, ?)
    """, (user_id, name, lastname))

    conn.commit()
    conn.close()
    users_data = get_user_data()
    return render_template('user_list.html', users=users_data)


@app.route('/users/<string:user_id>/edit', methods=['POST', 'GET'])
def edit_user(**kwargs):
    user_id = kwargs.get('user_id')
    if request.method == 'GET':
        user_data = get_user_data(user_id)[0]
        return render_template(
            'user_edit.html',
            user_id=user_id,
            name=user_data[1],
            lastname=user_data[2]
        )
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        conn = sqlite3.connect('users_db.db')
        cursor = conn.cursor()
        query = (
            f"UPDATE users SET name='{name}', lastname='{lastname}' "
            f"WHERE user_id='{user_id}'"
        )
        cursor.execute(query)
        conn.commit()
        conn.close()
        return render_template(
            'user_list.html',
            users=get_user_data()
        )


@app.route('/users', methods=['GET'])
def users_list():
    users_data = get_user_data()
    return render_template('user_list.html', users=users_data)


@app.route('/users/<string:user_id>/details', methods=['GET'])
def user_details(**kwargs):
    user_id = kwargs.get('user_id')
    user_data = get_user_data(user_id)
    return render_template('user_details.html', user=user_data[0])


@app.route('/users/<string:user_id>/delete', methods=['GET'])
def delete_user(**kwargs):
    user_id = kwargs.get('user_id')
    conn = sqlite3.connect('users_db.db')
    cursor = conn.cursor()
    query = (
        f"DELETE FROM users WHERE user_id='{user_id}'"
    )
    cursor.execute(query)
    conn.commit()
    conn.close()
    return render_template(
        'user_list.html',
        users=get_user_data()
    )


def generate_user_id():
    return str(uuid.uuid4()).replace('-', '')


def get_user_data(user_id=None):
    conn = sqlite3.connect('users_db.db')
    cursor = conn.cursor()
    query = """
        SELECT * FROM users
    """
    if user_id:
        query = f"{query} WHERE user_id = '{user_id}'"
    cursor.execute(query)
    users_data = cursor.fetchall()
    return users_data


if __name__ == '__main__':
    app.run(debug=True, port=5001)
