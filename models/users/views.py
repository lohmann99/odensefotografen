from flask import Blueprint, render_template, request, redirect, session

from models.users.user import User

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_username(username)
        if user is not None and user.check_password(password):
            user.login()
            return redirect('users/profile')
        else:
            return 'The username or password was incorrect.'
    else:
        return render_template('users/login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(request.form['username'],
                    request.form['email'],
                    request.form['full_name'],
                    request.form['phone_number'],
                    [],
                    request.form['password'])
        user.save_to_db()
        user.login()
        return redirect('users/profile')

    else:
        return render_template('users/register.html')


@user_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    user = User.find_by_username(session['username'])
    appointments = user.populate_appointments()

    return render_template('users/profile.html', appointments=appointments)
