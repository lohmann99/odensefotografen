import uuid
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from static.common.database import Database
from models.appointments.appointment import Appointment


class User(object):
    def __init__(self, username, email, full_name, phone_number, appointments=None, password=None, pw_hash=None, _id=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.phone_number = phone_number
        self.pw_hash = pw_hash
        self.set_password(password)
        self.appointments = [] if appointments is None else appointments
        self._id = uuid.uuid4().hex if _id is None else _id

    def set_password(self, password):
        if self.pw_hash is None:
            self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def login(self):
        session['username'] = self.username

    @staticmethod
    def logout():
        session['username'] = None

    def first_name(self):
        return self.full_name.split(' ')[0]

    def make_appointment(self, date, time):
        new_app = Appointment(self._id, date, time)
        self.appointments.append(new_app)
        new_app.save_to_db()

    def populate_appointments(self):
        populated = []
        for _id in self.appointments:
            populated.append(Appointment.find_by_id(_id))
        return populated

    def save_to_db(self):
        Database.insert('users', self.json())

    def update(self):
        Database.update_by_id('users', self._id, self.json())

    def json(self):
        return {
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'appointments': self.appointments,
            'pw_hash': self.pw_hash,
            '_id': self._id
        }

    @classmethod
    def find_by_id(cls, _id):
        user_data = Database.find_one('users', {'_id': _id})
        return cls(**user_data)

    @classmethod
    def find_by_email(cls, email):
        user_data = Database.find_one('users', {'email': email})
        return cls(**user_data)

    @classmethod
    def find_by_username(cls, username):
        user_data = Database.find_one('users', {'username': username})
        return cls(**user_data)



