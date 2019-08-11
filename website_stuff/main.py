# [START gae_python37_cloudsql_mysql]

## IMPORT STATEMENTS
import os
from flask import Flask,render_template,request
import pymysql
import datetime

## Connecting to the Google Cloud Database
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)

global myEID

## LOGIN - FORM
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    
    with cnx.cursor() as cur: 
        cur.execute("SELECT * FROM users")
        # get all rows
        rows = cur.fetchall()
        for row in rows:
            x=("{0} {1}".format(row[0], row[1]))
        return x

## Once logged in, takes you to the index page with the welcome message
## LOGIN - FORM SUBMISSION
@app.route('/login_index', methods=['POST'])
def login_index():
    adminError = None
    myEmail = request.form['email']
    myEID = request.form['EID']
    
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    

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
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                  unix_socket=unix_socket, db=db_name)
        else:
            # If running locally, use the TCP connections instead
            # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
            # so that your application can use 127.0.0.1:3306 to connect to your
            # Cloud SQL instance
            host = '127.0.0.1'
            cnx = pymysql.connect(user=db_user, password=db_password,
                                  host=host, db=db_name)

        with cnx.cursor() as cursor:
            userCheck = cursor.execute('SELECT * FROM users WHERE EID = %s',(get_myEID()))
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
            #myAdmin=0
            if myAdmin==1:
                #myAdmin=1
                cursor.execute('INSERT INTO users(name, phone, email, EID, admin) VALUES(%s, %s, %s, %s, %s)', (name, phone, email, EID, admin))
                adminError = None
                return render_template('user_submitted_form.html', name=name,email=email, phone=phone, EID=EID,admin=admin)
            else:
                adminError = 'You are not allowed to perform this action!'
                return render_template('login_index', adminError = adminError)
        cnx.commit()

        return render_template(
        'user_submitted_form.html',
        name=name,
        email=email,
        phone=phone,
        EID=EID,
        admin=admin)


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
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

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


        userCheck = cursor.execute('SELECT * FROM users WHERE EID = %s',(get_myEID()))
        entry = cursor.fetchall()
        num = list(entry)
        #myAdmin=0

        for element in num:
            if element[5]==1:
                myAdmin=1
                cursor.execute('INSERT INTO venues(bldg_code, floor_num, room_num, room_capacity) VALUES(%s, %d, %d, %d)' , (bldg_code, floor_num, room_num, room_capacity))
                adminError = None

                venue = cursor.lastrowid

                for time in hours:
                    cursor.execute("INSERT INTO Time(venue_id, timeslot) VALUES (%d, %s)", (venue, time))
            else:
                adminError = 'You are not allowed to perform this action!'
                return render_template('login_index', adminError = adminError)
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

@app.route('/eventsubmitted')
def eventsubmitted():
    name = request.form['name']
    description = request.form['description']
    expected_attendance = request.form['expected_attendance']
    venue_id = request.form['venue_id']
    event_owner = request.form['event_owner']
    start_time = request.form['start_time']

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

        with cnx.cursor() as cursor:
            infoGrab = cursor.execute('SELECT * FROM venues WHERE venue_id = %', (venue_id))
            entry = cursor.fetchall()
            num = list(entry)

            if expected_attendance < int(num[4]):  
                venueCheck = cursor.execute('SELECT * FROM Time WHERE venue_id = % AND timeslot = %', (venue_id, start_time,))
                timeEntry = cursor.fetchall()
                #print(timeEntry)

                if timeEntry[1] is None: 
                    sql = "INSERT INTO events(name, description, expected_attendance, venue_id, event_owner, start_time) VALUES(%s, %s, %d, %d, %s, %s)"
                    cursor = db.cursor()
                    cursor.execute(sql, (name, description, expected_attendance, venue_id, event_owner, start_time))

                    updateTime = "UPDATE Time SET event_id = % WHERE timeslot = % and venue_id = % "
                    updateCount = "UPDATE Events SET current_attendance = 1"
                    insertJoin = "INSERT INTO confirmedEvents(event_id, user_id) VALUES (%, %)"      
                   
                    cursor.execute('SELECT user_id FROM users WHERE EID =%', (event_owner))
                    row = cursor.fetchall()
                    num = list(sum(row, ()))

                    ## TODO: IDK HOW TO GET THE INSERT JOIN TO WORK!!!!!!! PLEASE CHEEECKK!!!!!!!!!!!
                    # cursor.execute(insertJoin, (num[0], cursor.lastrowid))
                    cursor.execute(insertJoin, (num[0], cursor.lastrowid))
                    cursor.execute(updateTime,(cursor.lastrowid, start_time, venue_id))
                    cursor.execute(updateCount)
                else:
                    raise Exception('Error: Room already booked for that time')
            else:
                raise Exception('ERROR: Room capacity exceeded')
        cnx.commit()

    return render_template(
    'eventsubmitted.html',
    name = 'name',
    description = 'description',
    expected_attendance = 'expected_attendance',
    venue_id = 'venue_id',
    event_owner = 'event_owner',
    start_time = 'start_time')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)