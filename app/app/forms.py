import datetime as datetime
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import *
from wtforms.fields.html5 import DateField, DateTimeField
from models import *

class AdminSetup(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15, message="Invalid input")])
    password = StringField('Password', validators=[InputRequired(), Length(min=8, max=15, message="Invalid input")])
    collegename = StringField('College Name', validators=[InputRequired(), Length(min=3, max=100, message="Invalid input")])
    courses = StringField('Courses/Society', validators=[Length(min=0)], default=None)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15, message="Invalid input")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=15, message=None)])

class CreateEvent(FlaskForm):
    eventname = StringField('Event Name', validators=[InputRequired(), Length(min=2,max=50,message="Invalid input")])
    eventdate = DateField('Event Date', format='%Y-%m-%d')
    eventdescription = StringField('Event Description', validators=[InputRequired()]) 
    eventfines = DecimalField('Event Fines', validators=[InputRequired()], default=0)

class StudentForm(FlaskForm):
    Fname = StringField('First Name', validators=[DataRequired()])
    Mname = StringField('Middle Name', validators=[DataRequired()])
    Lname = StringField('Last Name', validators=[DataRequired()])
    studentID = StringField('ID Number', validators=[DataRequired()])
    Course = StringField('Course', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    studentUID = PasswordField('Unique ID', validators=[DataRequired()])
    contact_no = IntegerField('Contact Number', validators=[DataRequired()])
    profile_pic = StringField('Profile Pic URI')	

class MessageForm(FlaskForm):
    number = IntegerField ("Number: ",  [validators.InputRequired()])
    message = TextAreaField ("Message: ", [validators.InputRequired()] ,render_kw={"maxlength": "160"})
    submit = SubmitField ("Submit")
    
class NewCollection(FlaskForm):
    collectionname = StringField('Collection Name', validators= [DataRequired()])
    amount = StringField('Amount', validators= [DataRequired()], default=0.00)
    Course = StringField('Course', validators=[DataRequired()])
    year = SelectField('Year', validators=[DataRequired()], choices=[(0, "All students"), (1, "All 1st Year"),(2, "All 2nd Year"),(3, "All 3rd Year"),(4, "All 4th Year")],coerce=str, default=2)

class upEvent(FlaskForm):
    eventname = StringField('Event Name', validators=[InputRequired(), Length(min=2,max=50,message="Invalid input")])
    eventdate = DateField('Event Date', format='%Y-%m-%d')
    eventdescription = StringField('Event Description', validators=[InputRequired()]) 
    eventfines = DecimalField('Event Fines', validators=[InputRequired()], default=0)