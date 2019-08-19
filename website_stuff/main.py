import os
import mysql.connector
import mysql.connector
import pymysql
from flask import Flask,render_template,request,session, jsonify, Response
import datetime
import pandas as pd
import json


## Connecting to the Google Cloud Database
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

global myEID

app = Flask(__name__)
app.secret_key = "iloveyou3000"

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login_index', methods=['GET', 'POST'])
def login_index():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
    adminError = None
    myEmail = request.form['email']
    myEID = request.form['EID']

    session['myEID'] = myEID

    # with cnx.cursor() as cursor:
    cursor = cnx.cursor()
    userCheck = cursor.execute('SELECT * FROM users WHERE EID = %s AND email = %s', (myEID, myEmail))
    entry = cursor.fetchall()
    
    num = list(entry)
    if len(num)==0:
        error = 'Invalid credentials'
        return render_template('login.html', error=error)
    else:
        myAdmin=0
        for element in num:
            if element[5]==1:
                myAdmin=1
                break
        error = None
    
    cnx.commit()
    cnx.close()

    return render_template("login_index.html", admin = myAdmin)

## Add user - form 
@app.route('/adduser')
def main1():
    return render_template('user_form.html')

## Add user - submitted form 
@app.route('/usersubmitted', methods=['GET', 'POST'])
def usersubmitted():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    EID = request.form['EID']
    admin = request.form['admin']

    if len(EID) != 7:
        return ("INVALID EID. PLEASE TRY AGAIN!")
    else:
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                  unix_socket=unix_socket, db=db_name)
        else:
            host = '127.0.0.1'
            cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
        cursor = cnx.cursor()

        myEID = session.get('myEID')
        print("THIS IS MY EID", myEID)

        userCheck = cursor.execute('SELECT * from users where EID = %s', (myEID,))
        entry = cursor.fetchall()
        print("THIS IS THE STUPID ENTRY", entry)
        print("THIS IS THE STUPID ENTRY", [x[5] for x in entry])

        tuplefromList = [x[5] for x in entry]
        adminCheck = tuplefromList[0]
        
        if adminCheck == 1:
            cursor.execute('INSERT INTO users(name, phone, email, EID, admin) VALUES (%s, %s, %s, %s, %s)', (name, phone, email, EID, admin))
            cnx.commit()
            cnx.close()
            adminError = None
        else:  
            adminError = 'You are not allowed to perform this action!'
            return render_template('login_index.html', adminError=adminError)
    
    return render_template('usersubmitted.html', name=name,email=email, phone=phone, EID=EID,admin=admin)
    
@app.route('/addvenue')
def main2():
    return render_template('venue_form.html')

@app.route('/venuesubmitted', methods=['GET', 'POST'])
def submitted_venue():
    bldg_code = request.form['bldg_code']
    floor_num = request.form['floor_num']
    room_num = request.form['room_num']
    room_capacity = request.form['room_capacity']

    start_time = '00:00'
    end_time = '23:00'
    slot_time = 60

    start_date = datetime.datetime.now().date()
    end_date = datetime.datetime.now().date() + datetime.timedelta(days=1)

    days = []
    date = start_date
   
    while date <= end_date:
        hours = []
        time = datetime.datetime.strptime(start_time, '%H:%M')
        end = datetime.datetime.strptime(end_time, '%H:%M')
        
        while time <= end:
            hours.append(time.strftime("%H:%M"))
            time += datetime.timedelta(minutes=slot_time)
        date += datetime.timedelta(days=1)
        days.append(hours)
        

        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                  unix_socket=unix_socket, db=db_name)
        else:
            host = '127.0.0.1'
            cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
        cursor = cnx.cursor()

        myEID = session.get('myEID')
        print("THIS IS MY EID", myEID)

        userCheck = cursor.execute('SELECT * from users where EID = %s', (myEID,))
        entry = cursor.fetchall()
        print("THIS IS THE STUPID ENTRY", entry)
        print("THIS IS THE STUPID ENTRY", [x[5] for x in entry])

        tuplefromList = [x[5] for x in entry]
        adminCheck = tuplefromList[0]
        
        if adminCheck == 1:
            cursor.execute('INSERT INTO venues(bldg_code, floor_num, room_num, room_capacity) VALUES (%s, %s, %s, %s)' , (bldg_code, floor_num, room_num, room_capacity))
            adminError = None

            venue = cursor.lastrowid
            print("THIS IS THE STUPID VENUE", venue)

            for time in hours:
                cursor.execute("INSERT INTO Time(venue_id, timeslot) VALUES (%s, %s)", (venue, time))
        else:
            adminError = 'You are not allowed to perform this action!'
            return render_template('login_index.html', adminError=adminError)
    cnx.commit()
    cnx.close()

    
    return render_template(
	    'venuesubmitted.html',
	    bldg_code = bldg_code,
	    floor_num = floor_num,
	    room_num = room_num,
	    room_capacity = room_capacity)
  
@app.route('/addevent')
def main3():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
    cursor = cnx.cursor()    
    df = pd.read_sql_query("SELECT * FROM venues", cnx)
    return render_template('event_form.html', tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values )

@app.route('/eventsubmitted', methods=['GET', 'POST'])
def eventsubmitted():
    name = request.form['name']
    description = request.form['description']
    expected_attendance = request.form['expected-attendance']
    venue_id = request.form['venue_id']
    event_owner = request.form['event_owner']
    start_time = request.form['start_time']

    print(name, description, venue_id, event_owner, start_time)

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")      
    cursor = cnx.cursor()    
    infoGrab = cursor.execute('SELECT * FROM venues WHERE venue_id = %s', (venue_id,))
    entry = cursor.fetchall()

    print("THIS IS ENTRY", entry)

    tuplefromList = [x[4] for x in entry]
    venueAttendance = int(tuplefromList[0])

    print(tuplefromList)
    print("VENUE ATTENDANCE:", venueAttendance)
            

    if int(expected_attendance) < venueAttendance:  
        venueCheck = cursor.execute('SELECT * FROM Time WHERE venue_id = %s AND timeslot = %s', (venue_id, start_time,))
        timeEntry = cursor.fetchall()
        tuplefromTimeEntry = [x[1] for x in timeEntry]

        if tuplefromTimeEntry[0] is None: 
            sql = "INSERT INTO events(name, description, expected_attendance, venue_id, event_owner, start_time) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, description, expected_attendance, venue_id, event_owner, start_time))
   
            eventID = cursor.lastrowid

            ## UPDATES THE TIME TABLE
            updateTime = "UPDATE Time SET event_id = %s WHERE timeslot = %s and venue_id = %s "
            cursor.execute(updateTime,(eventID, start_time, venue_id))

            ## INSERT JOIN
            cursor.execute('SELECT * FROM users WHERE EID = %s', (event_owner,))
            row = cursor.fetchall()

            tuplefromID = [x[0] for x in row]
            userID = tuplefromID[0]

            insertJoin = "INSERT INTO confirmedEvents(event_id, user_id) VALUES (%s, %s)" 
            cursor.execute(insertJoin, (eventID, userID))

            ## MODIFIES THE CURRENT ATTENDANCE
            updateCount = "UPDATE events SET current_attendance = 1 WHERE event_id = %s"
            cursor.execute(updateCount, (eventID,))
            
        else:
            raise Exception('Error: Room already booked for that time')
    else:
        raise Exception('ERROR: Room capacity exceeded')
    cnx.commit()

    return render_template(
    'eventsubmitted.html',
    name = name,
    description = description,
    expected_attendance = expected_attendance,
    venue_id = venue_id,
    event_owner = event_owner,
    start_time = start_time)



## Display timeslot availability at a venue
@app.route('/venuetimeslot')
def menu4():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    cursor = cnx.cursor()
    df = pd.read_sql_query("SELECT * FROM venues", cnx)
    return render_template("venuetimeslot_form.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values)

@app.route('/displayedvenuetimeslot', methods=['GET', 'POST'])
def open_venuetimeslot():

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    cursor = cnx.cursor()
    venue_id = request.form['venue_id']

    sql =  "SELECT Timeslot FROM Time WHERE event_id is null AND venue_id = %s"
    cursor.execute (sql, (venue_id,))
    row = cursor.fetchall()
    num = list(sum(row, ()))
    
    print ("Free times for this venue are:")
    print (num)

    jnum = json.dumps(num)
    
    if request.user_agent.platform == "android":
        return jnum
    else:
        df = pd.read_sql_query("SELECT * FROM Time", cnx)
        return render_template("displayedvenuetimeslot.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values, num=num)

## Display all venues where a particular timeslot is available¶
@app.route('/timeslotform')
def menu5():
    return render_template("timeslotform.html")

@app.route('/displayedtimeslot', methods=['GET', 'POST'])
def displayedtimeslot():

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
    
    cursor = cnx.cursor()
    time = request.form['time']

    sql =  "SELECT venue_id FROM Time WHERE event_id is null AND timeslot = %s"
    cursor.execute(sql, (time,) )
    row = cursor.fetchall()
    print(row)
    num = list(sum(row, ()))
    
    print("AVAILABILITY:", num)
    
    print ("Venues that are free at this time are:")

    availableVenues = []

    for x in num:
        sql1 = "SELECT bldg_code, floor_num, room_num FROM venues WHERE venue_id = %s"
        cursor.execute(sql1, (x,) )
        row1 = cursor.fetchall()
        num1 = tuple(sum(row1, ()))

        print("THIS IS NUM1", num1, type(num1))

        availableVenues.append(tuple(num1))
        print ("what is this?:",num1)
	
    javailableVenues = json.dumps(availableVenues)
    print(javailableVenues)

    if request.user_agent.platform == "android":
        return javailableVenues
    else:
        return render_template("displayedtimeslot.html", num1=availableVenues)

@app.route('/joinform')
def joinform():

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    cursor = cnx.cursor()
    df = pd.read_sql_query("SELECT * FROM events", cnx)
    return render_template("joinform.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values)

# NEEDS TO BE FIXED BUT PUSHING FOR NOW
@app.route('/joinsubmittedjson') 
def joinsubmittedjson():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    
    data = request.get_json() 
    EID = data['EID']
    print (EID)
    event_id = data['event_id']
    print (event_id)

    sql = "SELECT user_id FROM users WHERE EID = %s"
    cursor.execute(sql, (EID,))
    row = cursor.fetchall()
    num = list(sum(row, ()))
    print("NUM",num)
    
    current_sql= "SELECT current_attendance FROM events WHERE event_id = %s"
    cursor.execute(current_sql,(event_id,))
    cur =  cursor.fetchall()
    print("CUR", cur, cur[0])
    
    total_sql= "SELECT expected_attendance FROM events WHERE event_id = %s"
    cursor.execute(total_sql,(event_id,))
    tot = cursor.fetchall()
    print("TOT", tot, tot[0])
    
    if cur[0] < tot[0]:
        sd = []
        for element in num:
            stopDuplicates = "SELECT * FROM confirmedEvents WHERE user_id = %s AND event_id = %s"
            cursor.execute(stopDuplicates, (element, event_id,))
            sd = cursor.fetchall()
            print("SD", sd)
            print("ELEMENT", element)

            if len(sd)==0:
                sql1 = "INSERT INTO confirmedEvents(user_id, event_id) VALUES (%s, %s) "
                cursor.execute(sql1, (element, event_id,))
                updateCount = "UPDATE events SET current_attendance = current_attendance + 1 WHERE event_id = %s"
                cursor.execute(updateCount, (event_id,))
                cnx.commit()
            else:
                adminError = 'Error: This user is already going to this event'
                return render_template('login_index.html', adminError=adminError)
    else:
        adminError = 'Error: Event is fully booked'
        return render_template('login_index.html', adminError=adminError)

    df = pd.read_sql_query("SELECT * FROM events", cnx)

    return render_template("joinsubmitted.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values, EID=EID, event_id=event_id)


@app.route('/joinsubmitted', methods=['GET', 'POST'])
def joinsubmitted():

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    cursor = cnx.cursor()

    EID = request.form['EID']
    event_id = request.form['event_id']

    sql = "SELECT user_id FROM users WHERE EID = %s"
    cursor.execute(sql, (EID,))
    row = cursor.fetchall()
    num = list(sum(row, ()))
    print("NUM",num)
    
    current_sql= "SELECT current_attendance FROM events WHERE event_id = %s"
    cursor.execute(current_sql,(event_id,))
    cur =  cursor.fetchall()
    print("CUR", cur, cur[0])
    
    total_sql= "SELECT expected_attendance FROM events WHERE event_id = %s"
    cursor.execute(total_sql,(event_id,))
    tot = cursor.fetchall()
    print("TOT", tot, tot[0])
    
    if cur[0] < tot[0]:
        sd = []
        for element in num:
            stopDuplicates = "SELECT * FROM confirmedEvents WHERE user_id = %s AND event_id = %s"
            cursor.execute(stopDuplicates, (element, event_id,))
            sd = cursor.fetchall()
            print("SD", sd)
            print("ELEMENT", element)

            if len(sd)==0:
                sql1 = "INSERT INTO confirmedEvents(user_id, event_id) VALUES (%s, %s) "
                cursor.execute(sql1, (element, event_id,))
                updateCount = "UPDATE events SET current_attendance = current_attendance + 1 WHERE event_id = %s"
                cursor.execute(updateCount, (event_id,))
                cnx.commit()
            else:
                adminError = 'Error: This user is already going to this event'
                return render_template('login_index.html', adminError=adminError)
    else:
        adminError = 'Error: Event is fully booked'
        return render_template('login_index.html', adminError=adminError)

    df = pd.read_sql_query("SELECT * FROM events", cnx)

    return render_template("joinsubmitted.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values, EID=EID, event_id=event_id)

@app.route('/venueevents')
def menu6():

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
   
    cursor = cnx.cursor()
    df = pd.read_sql_query("SELECT * FROM venues", cnx)
    return render_template("venueevents_form.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values)

@app.route('/displayvenue', methods=['GET', 'POST'])
def displayvenue():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
   
    cursor = cnx.cursor()
    myEID = session.get('myEID')

    print("THIS IS MY EID", myEID)
    venue_id = request.form['venue_id']
    time = request.form['time']

    sql =  "SELECT event_id FROM Time WHERE venue_id= %s AND timeslot = %s"
    
    cursor.execute(sql, (venue_id, time,))    
    row = cursor.fetchall()
    num = list(sum(row, ()))
    #print ("Events in %s %i.%i at %s:" % (bldg_code,floor_num,room_num,time))

    stuff = []

    beep = num[0]

    for element in num:
        sql1 = "SELECT * FROM events WHERE event_id = %s"
        cursor.execute(sql1, (element,) )
        row1 = cursor.fetchall()
        num1 = tuple(sum(row1, ()))
        stuff.append(tuple(num1))
	
    jstuff = json.dumps(stuff)
    
    if request.user_agent.platform == "android":
        return jstuff
    else:
        if beep is not None:
            df = pd.read_sql_query(("SELECT * FROM events WHERE event_id = %s" % beep), cnx)
            return render_template("displayedevents.html", tables=[df.to_html(classes='data', index=False, header="true")], titles=df.columns.values)
        else:
            lol = "There are no events at this time and venue."
            return render_template("displayedevents.html", lol = lol)
@app.route('/deleteuser')
def deletemain():
    return render_template('delete_user_form.html')

## Add user - submitted form 
@app.route('/userdeleted', methods=['GET', 'POST'])
def deleted_form():
    email = request.form['email']
    EID = request.form['EID']

    myEID = session.get('myEID')
    print("THIS IS MY EID", myEID)

    if len(EID) != 7:
        return ("INVALID EID. PLEASE TRY AGAIN!")
    else:
        
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                  unix_socket=unix_socket, db=db_name)
        else:
            host = '127.0.0.1'
            cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
       
        cursor = cnx.cursor()

        userCheck = cursor.execute('SELECT * FROM users WHERE EID = %s AND email = %s', (EID, email))
        entry = cursor.fetchall()
        
        num = list(entry)
        if len(num)==0:
            error = 'Invalid credentials'
            return render_template('delete_user_form.html', error=error)
        else:
            
            myEID = session.get('myEID')
            print("THIS IS MY EID", myEID)

            userCheck = cursor.execute('SELECT * from users where EID = %s', (myEID,))
            entry = cursor.fetchall()
       

            tuplefromList = [x[5] for x in entry]
            adminCheck = tuplefromList[0]
            
            if adminCheck == 1:
                cursor.execute('DELETE FROM users WHERE EID = %s', (EID,))
                cnx.commit()
                adminError = None
            else:  
                adminError = 'You are not allowed to perform this action!'
                return render_template('login_index.html', adminError=adminError)
        return render_template('user_deleted_form.html', email=email,EID=EID)


@app.route('/deleteevent')
def deletemain1():
    return render_template('delete_event_form.html')
 
@app.route('/eventdeleted', methods=['GET', 'POST'])
def deleted_form1():
    event_id = request.form['event_id']

    myEID = session.get('myEID')
    print("THIS IS MY EID", myEID)

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
   
    cursor = cnx.cursor()

    myEID = session.get('myEID')
    print("THIS IS MY EID", myEID)

    userCheck = cursor.execute('SELECT * from users where EID = %s', (myEID,))
    entry = cursor.fetchall()

    tuplefromList = [x[5] for x in entry]
    adminCheck = tuplefromList[0]
    
    if adminCheck == 1:
        events_sql = ('DELETE FROM events WHERE event_id = %s')
        cs_sql = ('DELETE FROM confirmedEvents WHERE event_id = %s')
        time_sql = ('DELETE FROM Time WHERE event_id = %s')
        cursor.execute(events_sql, (event_id,))
        cursor.execute(cs_sql, (event_id,))
        cursor.execute(time_sql, (event_id,))
        
        cnx.commit()
        adminError = None
    else:  
        adminError = 'You are not allowed to perform this action!'
        return render_template('login_index.html', adminError=adminError)
    return render_template('event_deleted_form.html', event_id=event_id)


@app.route('/usertable', methods=['GET', 'POST'])
def usertable():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name)
    else:
    	host = '127.0.0.1'
    	cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing1", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
   
    cursor = cnx.cursor() 
    result = cursor.execute("Select * from users")
    dd = cursor.fetchall()
    column = ["user_id", "name", "phone", "email", "EID", "admin"]
    list =[]
    
    for item in dd:
        hello = dict(zip(column, item))
        list.append(hello.copy())
    
    jusers = json.dumps(list).replace("null","empty")
    #jusers = jsonify(list)
    print(jusers)

    return Response(jusers, mimetype='application/json')
    
@app.route('/eventtable', methods=['GET', 'POST'])
def eventtable():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)

    else: 
    	host = '127.0.0.1'
    	cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing1", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    cursor = cnx.cursor() 
    result = cursor.execute("Select * from events")
    dd = cursor.fetchall()
    column = ["event_id", "name", "description", "expected_attendance", "current_attendance", "venue_id", "event_owner", "start_time"]
    
    list =[]
    
    for item in dd:
        hello = dict(zip(column, item))
        list.append(hello.copy())
    
    jevents = json.dumps(list).replace("null","empty")
    #jevents = jsonify(list)

    print(jevents)


    return Response(jevents, mimetype='application/json')

@app.route('/venuetable', methods=['GET', 'POST'])
def venuetable():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing1", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
   
    cursor = cnx.cursor() 
    result = cursor.execute("Select * from venues")
    dd = cursor.fetchall()
    column = ["venue_id", "bldg_code", "floor_num", "room_num", "room_capacity","open_time","close_time"]
    
    list =[]
    
    for item in dd:
        hello = dict(zip(column, item))
        list.append(hello.copy())
    
    jvenue = json.dumps(list).replace("null","empty")
    #jvenue = jsonify(list)

    print(jvenue)
    return Response(jvenue, mimetype='application/json')

@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
    	host = '127.0.0.1'
    	cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing1", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")
   
    cursor = cnx.cursor() 
    result = cursor.execute("Select * from Time")
    dd = cursor.fetchall()
    column = ["time_id","event_id", "venue_id", "timeslot"]
    
    list =[]
    
    for item in dd:
        hello = dict(zip(column, item))
        list.append(hello.copy())
    
    jtime = json.dumps(list).replace("null","empty")
    #jtime = jsonify(list)

    print(jtime)
    return Response(jtime, mimetype='application/json')




if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(host='localhost', debug=True)
