import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])  # http://localhost/
def index():
    return render_template('index.html', names={})


@app.route('/save', methods=['POST'])  # http://localhost/save -> POST
def save_name():
    user_name = request.form['user_name']
    user_lastname = request.form['user_name_lastname']
    conn = sqlite3.connect('users_db.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name text,
        lastname text
    )
    """)
    conn.commit()

    cursor.execute("""
    INSERT INTO users (name, lastname)
    VALUES (?, ?)
    """, (user_name, user_lastname))

    conn.commit()
    conn.close()
    users_data = get_user_data()
    return render_template('user_list.html', users=users_data)


@app.route('/users', methods=['GET'])  # http://localhost/users
def users_list():
    users_data = get_user_data()
    return render_template('user_list.html', users=users_data)


def get_user_data():
    conn = sqlite3.connect('users_db.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users
    """)
    users_data = cursor.fetchall()
    return users_data


if __name__ == '__main__':
    app.run(debug=True, port=5001)
