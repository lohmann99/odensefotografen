import os
from flask import Flask, render_template, request, session

from models.user import User
from static.common.database import Database

app = Flask(__name__)
secret = os.urandom(24)
app.secret_key = secret


@app.route('/')
def home():
    return render_template('home.html')


@app.before_first_request
def initialize():
    Database.initialize()


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    user = User.find_by_username(username)

    if user is not None and user.check_password(password):
        user.login()
        return render_template('profile.html', username=session['username'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(request.form['username'],
                    request.form['email'],
                    request.form['full_name'],
                    request.form['phone_number'],
                    request.form['password'])
        user.save_to_db()
        user.login()
        return render_template('profile.html', username=session['username'])

    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run()
