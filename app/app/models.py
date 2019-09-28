from controller import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import mysql
# from sqlalchemy.ext.declarative import declarative_base

Integer = mysql.INTEGER
# Base = declarative_base()
class User(UserMixin, db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(80), unique = True)
    password =db.Column(db.String(100), nullable=False)
    collegename = db.Column(db.String(100), nullable=False)
    themeid = db.Column(db.Integer(), db.ForeignKey('themes.id'), default=0)


    def __init__(self, username, password, collegename):
        self.username = username
        self.password = password
        self.collegename = collegename
    


    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Themes(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    theme = db.Column(db.String(32), nullable=False)
    def __init__(self, id, theme):
        self.id=id
        self.theme=theme

    def __repr__(self):
        return '<Themes %r>' % self.id

class Courses(db.Model):
    courseID = db.Column(db.Integer(), primary_key=True)
    coursename= db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, coursename):
        self.coursename = coursename

    def __repr__(self):
        return "%s" % (self.coursename)

# class College(db.Model):
#     collegeID = db.Column(db.Integer(), primary_key=True)
#     collegename = db.Column(db.String(100), nullable=False)

#     def __init__(self, collegename):
#         self.collegename = collegename

#     def __repr__(self):
#         return "%s" % (self.collegename)

class Collection(db.Model):
    collectionID = db.Column(db.Integer(), primary_key=True)
    collectionname = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(7), nullable=False)

    def __init__(self, collectionname, amount):
        self.collectionname = collectionname
        self.amount = amount

    def __repr__(self):
        return "%s" % (self.collectionname)

class Payment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    StudentUID = db.Column(db.String(15), db.ForeignKey("student.studentUID"), nullable=False, unique=False)
    CollectionID = db.Column(db.Integer(), db.ForeignKey("collection.collectionID"))

    def __init__(self, StudentUID, CollectionID):
        self.StudentUID = StudentUID
        self.CollectionID = CollectionID

    def __repr__(self):
        return "%s" % (self.CollectionID)


class Student(db.Model):
    studentUID = db.Column(db.String(15), unique=True, primary_key=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    Fname = db.Column(db.String(50), nullable=False)
    Mname = db.Column(db.String(50), nullable=False)
    Lname = db.Column(db.String(50), nullable=False)
    Course = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable = False)
    Fines = db.Column(db.DECIMAL(10, 2), default=0, nullable=False)
    Status = db.Column(db.DECIMAL(10,2), default = 1, nullable=False)
    contact_no = db.Column(db.String(11), nullable = False)
    profile_pic = db.Column(db.Text())
    attends = db.relationship('Attendance', backref='student', uselist=False)

    def __init__(self, studentUID, studentID, Fname, Mname, Lname, Course, year, contact_no, profile_pic):
        self.studentUID = studentUID
        self.studentID = studentID
        self.Fname = Fname
        self.Mname = Mname
        self.Lname = Lname
        self.Course = Course
        self.year = year
        self.contact_no = contact_no
        self.profile_pic = profile_pic

    def __repr__(self):
      return "Name is: {}, {} {} ".format(self.Lname, self.Fname, self.Mname)

class Events(db.Model):
    eventID = db.Column(db.Integer(), primary_key=True)
    eventname = db.Column(db.String(50), unique=True, nullable=False)
    eventdescription = db.Column(db.Text(), nullable = True)
    eventdate = db.Column(db.CHAR(10), nullable=False)
    eventfines = db.Column(db.DECIMAL(10, 2), nullable=True)
    attendance = db.relationship('Attendance', backref='event_attendance', uselist=False)

    def __init__(self, eventname, eventdescription, eventdate, eventfines):
        self.eventname = eventname
        self.eventdescription = eventdescription
        self.eventdate = eventdate
        self.eventfines = eventfines

    def _repr__(self):
        return "%s" % (self.eventname)

class Attendance(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    StudentUID = db.Column(db.String(15), db.ForeignKey("student.studentUID"), nullable=False, unique=False)
    EventID = db.Column(db.Integer(), db.ForeignKey('events.eventID'), nullable=False)
    signIn = db.Column(db.Integer(), nullable=True)
    signOut = db.Column(db.Integer(), nullable=True)
    # sfines = db.Column(db.DECIMAL(10, 2), default=0, nullable=False)

    def __init__(self, StudentUID, EventID, signIn, signOut):
        self.StudentUID = StudentUID
        self.EventID = EventID
        self.signIn = signIn
        self.signOut = signOut
        # self.Sfines = sfines

    def __repr__(self):
        return "%s" % (self.EventID)