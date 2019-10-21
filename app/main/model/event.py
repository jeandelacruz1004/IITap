import datetime
import jwt
from .. import db, flask_bcrypt

class Event(db.Model):
    """ Event Model for storing event related details """
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(100), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False)
    eventDate = db.Column(db.DateTime, nullable=False)
    eventStartTime = db.Column(db.Time)
    eventEndTime = db.Column(db.Time)
    eventDescription = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=False)
    fee = db.Column(db.Integer, default=0)
    public_id = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Event({}, {}, {}, {}, {}, {}, {})".format(self.eventName, self.location, self.eventDate, self.eventStartTime, self.eventEndTime, self.eventDescription, self.fee)