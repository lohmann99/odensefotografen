import uuid

from flask import session

from werkzeug.security import generate_password_hash, check_password_hash

from static.common.database import Database


class User(object):
    def __init__(self, username, email, full_name, phone_number, password=None, pw_hash=None, _id=None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.phone_number = phone_number
        self.pw_hash = pw_hash
        self.set_password(password)
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

    @staticmethod
    def register(username, email, full_name, phone_number, password):
        if Database.find_one('users', {'username': username}) is not None:
            return 'The username is already taken'
        elif Database.find_one('users', {'email': email}) is not None:
            return 'The e-mail is already registered to a user'
        else:
            new_user = User(username, email, full_name, phone_number, password)
            new_user.save_to_db()

    def make_appointment(self):
        pass

    def save_to_db(self):
        Database.insert('users', self.json())

    def json(self):
        return {
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
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
        print(username)
        user_data = Database.find_one('users', {'username': username})
        print(user_data)
        return cls(**user_data)



