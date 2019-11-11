import datetime
import jwt
from .. import db, flask_bcrypt

class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(100), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    eventDate = db.Column(db.DateTime, nullable=False)
    eventDescription = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=False)
    fee = db.Column(db.Integer, default=0)
    public_id = db.Column(db.String(100), unique=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "Event({}, {}, {}, {}, {}, {}, {})".format(self.eventName, self.location, self.eventDate, self.eventDescription, self.fee)