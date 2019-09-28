from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import re
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from controller import *
from datetime import timedelta, datetime
from models import *
from forms import *
import serial
import serial.tools.list_ports
import json
from serial import SerialException


createDB()
createTables()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'
# login_manager.login_message = "You need to login"

#Auto Detect ComPort for GSM, use gsm_port[0]
# gsm_port = [
#     x.device 
#     for x in serial.tools.list_ports.comports()
#     if '3G PC UI Interface' in x.description
# ]
#Auto Detect ComPort for Arduino Nano, use arduino_port[0] comment this out
arduino_port = [
    x.device 
    for x in serial.tools.list_ports.comports()
    if 'CH340' in x.description
]


# def send_text(number, text, path = gsm_port[0]):
#     ser = serial.Serial(path, timeout=1)
#     ser.write(('AT+CMGF=%d\r' % 1).encode())
#     ser.write(('AT+CMGS="%s"\r' % number).encode())
#     ser.write(('%s\x1a' % text).encode())
#     ser.close()
     

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except User.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('Admin rights needed to access this page')
    return redirect(url_for('adminlogin'))

@app.route('/scancard')
def scancard():
      return render_template('adminverify.html')

@app.route('/adminsetup', methods=['GET','POST'])
def admin_setup():
      form = AdminSetup()
      check = User.query.first()
      if check is None:
            if request.method=='POST' and form.validate_on_submit():
                  db.session.add(User(username=form.username.data, password=generate_password_hash(form.password.data), collegename=form.collegename.data))
                  list = form.courses.data
                  def commaSep(list):
                        new_list = re.split(', |,| ,',list)
                        for data in new_list:
                              db.session.add(Courses(coursename=data))
                  commaSep(list)
                  db.session.commit()
                  print list
                  # return render_template('homepage.html')
                  return redirect(url_for('adminlogin'))

      else:
            return redirect(url_for('adminlogin'))
      return render_template('adminsetup.html', form=form)

@app.route('/adminverify', methods=['GET','POST'])
def admin_verify():
      ser = serial.Serial(arduino_port[0], 9600)
      # ser = serial.Serial('COM4', 9600)
      response = ser.readline().decode("utf-8").strip()
      if response == "92 43 D9 D6" or "A1 12 E9 D4" or " 75 0E DD 5E" or "80 F6 0B A6":#ichange ni nga string sa UID sa imung card nga gamit
            return redirect(url_for('admin_setup'))#wala pa nko gigama ang adminsetup nga html, sulaye lng kung muredirect ba sya kung mgmatch ang string sa UID 
      else:
            flash("Access card not authorized")
            return redirect(url_for('scancard'))

@app.route('/', methods=['GET','POST'])
def adminlogin():
      form = LoginForm()
      check = User.query.first()
      if check is None:
            return redirect(url_for('scancard'))
      else:
            if request.method=='POST' and form.validate_on_submit():
                  session.pop('user', None)
                  user = User.query.filter_by(username=form.username.data).first()
                  if user:
                        if check_password_hash(user.password, form.password.data):
                              login_user(user, remember=True)
                              session['user'] = user.username
                              session['id'] = user.id
                              session['themeid'] = user.themeid
                              return redirect(url_for('homepage'))
                        else:
                              flash("Incorrect Password")
                              return render_template('adminlogin.html', form=form)
                  else:
                        flash("Username does not exist")
                        return render_template('adminlogin.html', form=form)
      return render_template('adminlogin.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('adminlogin'))

@app.route('/homepage')
@login_required
def homepage():
      return render_template('homepage.html')

# @app.route('/events')
# @login_required
# def events():
#       return render_template('events.html')

# @app.route('/events/createevent')
# @login_required
# def createevent():
#       form = CreateEvent()
#       if request.method=='POST' and form.validate_on_submit():
#             msg = "Event successfully created!"
#             db.session.add(Events(eventname=form.eventname.data, eventdate=form.eventdate.data, eventfines=form.eventfines.data))
#             db.session.commit
#             return render_template('createevent.html')
#       return render_template('createevent.html')


#start
@app.route('/students')
@login_required
def students():
    students = Student.query.all()
    for x in students: 
        print(x.Fname)
    return render_template('students.html', data = students)

@app.route('/registration', methods = ['GET', 'POST'])
@login_required
def registration():
      courses = Courses.query.all()
      form = StudentForm()
      if request.method == "POST":
      # if request.method == "POST" and form.validate():
            select_course = request.form.get('courses')
            user = Student(studentUID = form.studentUID.data, Fname = form.Fname.data, Mname=form.Mname.data, Lname = form.Lname.data ,Course = select_course,\
            studentID = form.studentID.data, year = form.year.data, contact_no = form.contact_no.data, profile_pic = form.profile_pic.data)
            print(user)
            db.session.add(user)
            db.session.commit()
            return redirect('/registration')
      else:
            return render_template('registration.html' , form = form, courses = courses)

@app.route('/check_availability/<studentUID>', methods = ['GET', 'POST'])
def check_availability(studentUID):
      state = db.session.query(db.session.query(Student).filter_by(studentUID = studentUID).exists()).scalar()
      if state == True:
            return "true"
      else:
            return "false"

@app.route('/take_picture', methods = ['GET', 'POST'])
@login_required
def take_picture():
    if request.method == 'POST':
        return redirect(url_for('students'))
    return render_template('picture.html')

@app.route('/scan_id', methods = ['GET', 'POST'])
@login_required
def scan_id():
    # ser = serial.Serial(arduino_port[0], 9600)
    # response = ser.readline().decode("utf-8").strip()
    # print(response)
    # ser.close()
    return render_template('scanning.html')

@app.route('/scan_id/scanning', methods = ['POST', 'GET'])
@login_required
def scanning():
      # ser = serial.Serial(arduino_port[0], 9600)
      # # ser = serial.Serial('COM4', 9600)
      # response = ser.readline().decode("utf-8").strip()
      # print(response)
      # ser.close()
      try: 
            global ser
            ser = serial.Serial(arduino_port[0], 9600)
            response = ser.readline().decode("utf-8").strip()
            print("Port is open")
      except SerialException:
            ser.close()
            ser.open()
            response = ser.readline().decode("utf-8").strip()

      return render_template('scanning.html', data = json.dumps(response))

@app.route('/scan_id/scanning/success')
@login_required
def success(): 
    return render_template('success.html')

@app.route('/send_sms', methods =["POST", "GET"])
@login_required
def send_sms(): 
      form = MessageForm()
      if request.method == "POST":
            option = request.form.get('to')
            message = form.message.data
            if (option == "all"):
                  x= db.session.query(Student.contact_no).all()
                  for numbers in x: 
                        print(numbers)
                        send_text(numbers,message)
            elif (option == "first"):
                  x = db.session.query(Student.contact_no).filter(Student.year == 1)
                  for numbers in x: 
                        print(numbers)
                        send_text(numbers,message)
            elif (option == "second"):
                  x = db.session.query(Student.contact_no).filter(Student.year == 2)
                  for numbers in x: 
                        print(numbers)
                        send_text(numbers,message)
            elif (option == "third"):
                  x = db.session.query(Student.contact_no).filter(Student.year == 3)
                  for numbers in x: 
                        print(numbers)
                        send_text(numbers,message)
            elif (option == "fourth"):
                  x = db.session.query(Student.contact_no).filter(Student.year == 4)
                  for numbers in x: 
                        print(numbers)
                        send_text(numbers,message)
            flash('Message Sent Successfully')
      return render_template('smsblast.html', form = form)

@app.route('/events', methods = ['POST', 'GET'])
@login_required
def events(): 
      events = Events.query.all()     
      print(type(events))
      return render_template('events.html', data = events)

@app.route('/events/add_event', methods = ['POST', 'GET'])
@login_required
def add_event():
    form = CreateEvent(request.form)
    if request.method == "POST": 
        events = Events(eventname = form.eventname.data, eventdescription = form.eventdescription.data, eventdate = form.eventdate.data, eventfines = form.eventfines.data)
        db.session.add(events)
        db.session.commit()
        return redirect ('/events')
    else: 
        return render_template('createevent.html', form = form)

@app.route('/events/delete/<int:eventID>', methods = ['POST', 'GET'])
@login_required
def delete_event(eventID): 
      Events.query.filter_by(eventID= eventID).delete()
      db.session.commit()
      print('Deleted event {}'.format(eventID))
      return redirect ('/events')

      
@app.route('/events/edit/<int:eventID>', methods = ['GET', 'POST'])
@login_required
def edit_event(eventID):
      form = upEvent(request.form)

      if request.method == "POST" and form.validate_on_submit(): 
          check = Events.query.filter_by(eventID=eventID).first()
          name = Events.query.filter_by(eventname=form.eventname.data).first()
          if name is None:
              check.eventname = form.eventname.data
              check.eventdescription = form.eventdescription.data
              check.eventdate = form.eventdate.data
              check.eventfines = form.eventfines.data

              db.session.commit()

              flash("Edit Successful!")
              return redirect('/events')
          else:
              flash("Event name already exists!")
              return render_template("updateevent.html", form=form, eventID=eventID)
      else:
          return render_template("updateevent.html", form=form, eventID=eventID)


@app.route('/attendance_type/<int:eventID>', methods = ['GET', 'POST'])
@login_required
def attendance_type(eventID):
      print(eventID)
      if request.method == "POST":
            result = request.form.get("singwhat");
            return redirect(url_for('take_attendance', eventID =eventID, result = result))
      return render_template('signinout.html', eventID = eventID)

@app.route('/attendance_type/<int:eventID>/<result>', methods = ['POST', 'GET'])
@login_required
def take_attendance(result, eventID):
      eventName = Events.query.filter_by(eventID = eventID).first()
      return render_template('attendance.html', result = result, eventID = eventID, eventName = eventName.eventname)

@app.route('/attendance_type/IN', methods = ['GET', 'POST'])
@login_required
def signingIn():
      my_var = request.args.get('my_var', None)
      # ser = serial.Serial(arduino_port[0], 9600)
      # response = ser.readline().decode("utf-8").strip()
      
      try: 
            global ser
            ser = serial.Serial(arduino_port[0], 9600)
            response = ser.readline().decode("utf-8").strip()
            print("Port is open")
      except SerialException:
            ser.close()
            ser.open()
            response = ser.readline().decode("utf-8").strip()

   
      print(my_var)
      student_match = Student.query.filter_by(studentUID = response).first()

      if (student_match):
            student_ID = student_match.studentUID
            check = Attendance.query.filter_by(StudentUID = response, EventID = my_var, signIn = 1).first()
            if (check):
                  print("NAAAA!!")
                  return json.dumps({ 
                        'attendance_type' : 'Sign In',
                        'f_name' : '',
                        'm_name': '',
                        "l_name" : '',
                        "year" : '',
                        "course": '',
                        "profile": ' ',
                        "id_no" : ' ',
                        'message': "Student Already Signed In for this Event"
                        })
            else:
                  print("WALAAA!")
                  attendance = Attendance(StudentUID = response,EventID = my_var, signIn = 1, signOut =None)
                  db.session.add(attendance)
                  db.session.commit()
                  return json.dumps({
                        'attendance_type' : 'Sign In',
                        'f_name' : student_match.Fname,
                        'm_name': student_match.Mname,
                        "l_name" : student_match.Lname,
                        "year" : student_match.year,
                        "course": student_match.Course,
                        "profile": student_match.profile_pic,
                        "id_no" : student_match.studentID,
                        'message' : ''
                        })
      else:
            return json.dumps({'message': "Student Doesn't Exist in the database"})
            
@app.route('/attendance_type/OUT', methods = ['POST', 'GET'])
@login_required
def signingOut():
      my_var = request.args.get('my_var', None)
      # ser = serial.Serial(arduino_port[0], 9600)
      # response = ser.readline().decode("utf-8").strip()
      # print(my_var)
      # ser.close()
      try: 
            global ser
            ser = serial.Serial(arduino_port[0], 9600)
            response = ser.readline().decode("utf-8").strip()
            print("Port is open")
      except SerialException:
            ser.close()
            ser.open()
            response = ser.readline().decode("utf-8").strip()

      student_match = Student.query.filter_by(studentUID = response).first()
      if (student_match): 
            student_match = Student.query.filter_by(studentUID = response).first()
            check = Attendance.query.filter_by(StudentUID = response, EventID = my_var, signOut = 1).first()

            if (check):
                  return json.dumps({ 
                        'attendance_type' : 'Sign In',
                        'f_name' : '',
                        'm_name': '',
                        "l_name" : '',
                        "year" : '',
                        "course": '',
                        "profile": ' ',
                        "id_no" : ' ',
                        'message': "Student Already Signed Out for this Event"
                        })
            else: 
                  sign_out = Attendance.query.filter_by(StudentUID = response, EventID = my_var).first()
                  sign_out.signOut = 1
                  db.session.commit()
                  return json.dumps({
                        'attendance_type' : 'Sign Out',
                        'f_name' : student_match.Fname,
                        'm_name': student_match.Mname,
                        "l_name" : student_match.Lname,
                        "year" : student_match.year,
                        "course": student_match.Course,
                        "profile": student_match.profile_pic,
                        "id_no" : student_match.studentID,
                        'message' : ''
                        })
      else:
            return json.dumps({'message': "Student Doesn't Exist in the database"}) 

@app.route('/events/attendance/<int:eventID>', methods = ['POST', 'GET'])
@login_required
def list_attendance(eventID):
      event = Attendance.query.filter_by(EventID = eventID).all()
      eventName = Events.query.filter_by(eventID = eventID).first()
      
      query = db.session.query(Attendance.signIn, Attendance.signOut, Attendance.StudentUID, Student.Fname, Student.Mname,
                  Student.Lname, Student.studentID, Student.Course, Student.year).outerjoin(Student, Events).filter_by(eventID = eventID).order_by(Student.Lname)
      return render_template('attendancelist.html', eventName = eventName, query =query, eventID = eventID)

@app.route('/collection/scancard')
@login_required
def collection_scan():
      return render_template('scanpayment.html')


@app.route('/collections', methods=['GET', 'POST'])
@login_required
def collection():     
      form = NewCollection()
      collection = Collection.query.all()
      return render_template('collection.html', data=collection, form=form)


@app.route('/collection/<int:CollectionID>', methods=['GET', 'POST'])
@login_required
def Collection_StudentList(CollectionID):
        if request.method == 'POST':
              students = Student.query.join(Payment).filter(Payment.StudentUID == Payment.StudentUID).filter(
                    Payment.CollectionID == request.form['students']).all()

              return render_template('collectionStudents.html', data=students)

        return render_template('collectionStudents.html', data=students )        

@app.route('/collection/delete/<collectionID>', methods=['GET', 'POST'])
@login_required
def delete_collection(collectionID):
      if request.method == 'POST':
              # students = Student.query.join(Payment).filter(Payment.StudentUID == Payment.StudentUID).filter(
              #   Payment.CollectionID == collectionID).first()
              print collectionID
              Payment.query.filter_by(CollectionID = collectionID).delete()
              db.session.commit()

              # if students is None:
              #         collections = Collection.query.all()  

              Collection.query.filter_by(collectionID = collectionID).delete()
              db.session.commit()
              collections = Collection.query.all()
              flash("deleted")
                      
      # else:
      #         return redirect(url_for('collection'))

              #   print "di ma delete megs"
              #   flash("cannot delete this collection students already paid for this")

      return redirect(url_for('collection'))


@app.route('/collection/new_collection', methods=['GET', 'POST'])
@login_required
def new_collection():
      form = NewCollection()
      collections = Collection.query.all()  
      if request.method=='POST':
              checkCollection = Collection.query.filter_by(collectionname = form.collectionname.data).first()
              if checkCollection is None:
                                      
                      db.session.add(Collection(collectionname=form.collectionname.data, amount=form.amount.data))
                      db.session.commit()
                      collections = Collection.query.all()  


                      return redirect(url_for('collection'))
      else:
              flash('Naa na po na na collections')
              return redirect(url_for('collection'))

      return redirect(url_for('collection'))

@app.route('/collection/add_payment', methods=['GET', 'POST'])
@login_required
def collection_payment():
      try: 
            global ser
            ser = serial.Serial(arduino_port[0], 9600)
            response = ser.readline().decode("utf-8").strip()
            print("Port is open")
      except SerialException:
            ser.close()
            ser.open()
            response = ser.readline().decode("utf-8").strip()
      
      # students = Student.query.join(Payment).filter(Payment.StudentUID == response).filter(
      #               Payment.CollectionID == request.form['payment']).first()      
      # print(students.studentUID)

      

      # query = db.session.query(Collection.collectionID, Collection.collectionname, Student.Fname, Student.Mname,
            # Student.Lname, Student.studentID, Student.Course, Student.year).outerjoin(Payment, Collection).filter_by(collectionID = request.form['payment']).first()

      check = Student.query.filter_by(studentUID = response).first()
      db.session.add(Payment(StudentUID=response, CollectionID=request.form['payment']))
      db.session.commit()
      #message2 pa taaaaa ;(

                        
      return redirect(url_for('collection'))

@app.route('/swaptheme/<int:themeid>', methods=['GET', 'POST'])
def swaptheme(themeid):
    user = User.query.filter_by(id=session['id']).first()
    print(session['id'])
    user.themeid = themeid
    db.session.commit()
    session['themeid'] = themeid
    return "hahahah"


@app.before_request
def make_session_permanent():
      session.permanent = True
      app.permanent_session_lifetime = timedelta(minutes=120)

if __name__ == "__main__":
      app.run(debug=True)

