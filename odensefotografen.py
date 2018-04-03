import os
from flask import Flask, render_template, request, session

from models.user import User
from static.common.database import Database

app = Flask(__name__)
secret = os.urandom(24)
app.secret_key = secret


@app.route('/')
def home():
    return render_template('login.html')


@app.before_first_request
def initialize():
    Database.initialize()


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_username(username)

        if user is not None and user.check_password(password):
            user.login()
            return render_template('profile.html', user=user)
        else:
            # TODO: Throw an error that lets the user know the password or username was wrong.
            # TODO: Render login.html along with the error thrown.
            return 'I could not log you in'
    elif session['username'] is not None:
        user = User.find_by_username(session['username'])
        return render_template('profile.html', user=user)
    else:
        return render_template('login.html')


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
        return render_template('profile.html', user=user)

    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run()