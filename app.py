import os
from flask import Flask, render_template, request, session

from models.users.user import User
from static.common.database import Database

app = Flask(__name__)
secret = os.urandom(24)
app.secret_key = secret


@app.before_first_request
def initialize():
    Database.initialize()


@app.route('/')
def home():
        return render_template('home.html')


from models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        user = User.find_by_username(session['username'])
        user.make_appointment(request.form['date'], request.form['time'])
        user.update()
        appointments = user.populate_appointments()

        return render_template('profile.html', user=user, appointments=appointments)

    else:
        return render_template('new_appointment.html')


if __name__ == '__main__':
    app.run()
