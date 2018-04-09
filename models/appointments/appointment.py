import uuid
from static.common.database import Database


class Appointment(object):
    def __init__(self, owner_id, date, time, confirmed=False, _id=None):
        self.owner_id = owner_id
        self.date = date
        self.time = time
        self.confirmed = confirmed
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            'owner_id': self.owner_id,
            'date': self.date,
            'time': self.time,
            'confirmed': self.confirmed,
            '_id': self._id
        }

    def save_to_db(self):
        Database.insert('appointments', self.json())

    def format_date(self):
        return '-'.join(reversed(self.date.split('-')))

    def as_text(self):
        return 'Du har en forespurgt aftale med OdenseFotografen d. {} kl. {}'.format(self.format_date(), self.time)

    @classmethod
    def find_by_id(cls, _id):
        app_data = Database.find_one('appointments', {'_id': _id})
        return cls(**app_data)
