# [START gae_python37_cloudsql_mysql]

## IMPORT STATEMENTS
import os
from flask import Flask,render_template,request,session
import pymysql
import datetime
import pandas as pd


## Connecting to the Google Cloud Database
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.secret_key = "iloveyou3000"

global myEID

## LOGIN - FORM
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    
    with cnx.cursor() as cur: 
        cur.execute("SELECT * FROM users")
        # get all rows
        rows = cur.fetchall()
        for row in rows:
            x=("{0} {1}".format(row[0], row[1]))
        return x

@app.route('/test1', methods=['GET', 'POST'])
def test1():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    
    with cnx.cursor() as cur: 
        cur.execute("SELECT * FROM venues")
        # get all rows
        rows = cur.fetchall()
        for row in rows:
            x=("{0} {1}".format(row[0], row[1]))
        return x

@app.route('/test2', methods=['GET', 'POST'])
def test2():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    
    with cnx.cursor() as cur: 
        cur.execute("SELECT * FROM events")
        # get all rows
        rows = cur.fetchall()
        for row in rows:
            x=("{0} {1}".format(row[0], row[1]))
        return x

## Once logged in, takes you to the index page with the welcome message
## LOGIN - FORM SUBMISSION
@app.route('/login_index', methods=['GET', 'POST'])
def login_index():
    adminError = None
    myEmail = request.form['email']
    myEID = request.form['EID']
    session['myEID'] = myEID
    
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")

    

    with cnx.cursor() as cursor:
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
    return render_template('login_index.html', admin = myAdmin)

def get_myEID():
    myEID = request.form['EID']
    return (myEID)


    
## Add user - form 
@app.route('/adduser')
def main1():
    return render_template('user_form.html')

## Add user - submitted form 
@app.route('/usersubmitted', methods=['POST'])
def submitted_form():
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


        with cnx.cursor() as cursor:
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
                adminError = None
            else:  
                adminError = 'You are not allowed to perform this action!'
                return render_template('login_index.html', adminError=adminError)
        return render_template('user_submitted_form.html', name=name,email=email, phone=phone, EID=EID,admin=admin)


@app.route('/addvenue')
def main2():
    return render_template('venue_form.html')

@app.route('/venuesubmitted', methods=['POST'])
def submitted_venue():
    bldg_code = request.form['bldg_code']
    floor_num = request.form['floor_num']
    room_num = request.form['room_num']
    room_capacity = request.form['room_capacity']

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")


    with cnx.cursor() as cursor:
        ## TIME STUFF (?)
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
        myEID = session.get('myEID')
        print("THIS IS MY EID", myEID)

        userCheck = cursor.execute('SELECT * from users where EID = %s', (myEID,))
        entry = cursor.fetchall()
        print("THIS IS THE STUPID ENTRY", entry)
        print("THIS IS THE STUPID ENTRY", [x[5] for x in entry])

        tuplefromList = [x[5] for x in entry]
        adminCheck = tuplefromList[0]
        
        if adminCheck == 1:
            cursor.execute('INSERT INTO venues(bldg_code, floor_num, room_num, room_capacity) VALUES(%s, %s, %s, %s)' , (bldg_code, floor_num, room_num, room_capacity))
            venue = cursor.lastrowid

            for time in hours:
                cursor.execute("INSERT INTO Time(venue_id, timeslot) VALUES (%s, %s)", (venue, time))
        else:  
            adminError = 'You are not allowed to perform this action!'
            return render_template('login_index.html', adminError=adminError)
    cnx.commit()

    return render_template(
    'venuesubmitted.html',
    bldg_code = bldg_code,
    floor_num = floor_num,
    room_num = room_num,
    room_capacity = room_capacity)
    

    
@app.route('/addevent')
def main3():
    return render_template('event_form.html')

@app.route('/eventsubmitted', methods=['POST'])
def eventsubmitted():
    name = request.form['name']
    description = request.form['description']
    expected_attendance = request.form['expected-attendance']
    venue_id = request.form['venue_id']
    event_owner = request.form['event_owner']
    start_time = request.form['start_time']

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = mysql.connector.connect(host="127.0.0.1", user = "root", password = "root", database = "testing", unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock")


    with cnx.cursor() as cursor:
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
            print(tuplefromTimeEntry)
            times = tuplefromTimeEntry[0]

            if times is None: 
                sql = "INSERT INTO events(name, description, expected_attendance, venue_id, event_owner, start_time) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, description, expected_attendance, venue_id, event_owner, start_time))
       
                eventID = cursor.lastrowid
                print(eventID)

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
                updateCount = "UPDATE events SET current_attendance = 1"
                cursor.execute(updateCount)
                
            else:
                adminError = 'Error: Room already booked for that time'
                return render_template('login_index.html', adminError=adminError)
        else:
            adminError = 'ERROR: Room capacity exceeded'
            return render_template('login_index.html', adminError=adminError)
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
    return render_template("venuetimeslot_form.html", tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/displayedvenuetimeslot', methods=['POST'])
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

    df = pd.read_sql_query("SELECT * FROM Time", cnx)
    return render_template("displayedvenuetimeslot.html", tables=[df.to_html(classes='data')], titles=df.columns.values, num=num)

## Display all venues where a particular timeslot is available¶
@app.route('/timeslotform')
def menu5():
    return render_template("timeslotform.html")

@app.route('/displayedtimeslot', methods=['POST'])
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
        num1 = list(sum(row1, ()))

        for i in num1:
            availableVenues.append(i)
        print ("what is this?:",num1)
        print("X", x)

    return render_template("displayedtimeslot.html", num1=availableVenues)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)