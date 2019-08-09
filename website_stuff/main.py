# [START gae_python37_cloudsql_mysql]

## IMPORT STATEMENTS
import os
from flask import Flask,render_template,request
import pymysql

## Connecting to the Google Cloud Database
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)


## LOGIN - FORM
@app.route('/')
def login():
    return render_template('login.html')

## Once logged in, takes you to the index page with the welcome message
## LOGIN - FORM SUBMISSION
@app.route('/login_index', methods=['POST'])
def login_index():
    global myEID
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
            userCheck = cursor.execute('SELECT * FROM users WHERE EID = %s', (myEID))
            entry = cursor.fetchall()
            num = list(entry)
            myAdmin=0

            for element in num:
                if element[5]==1:
                    myAdmin=1
                    cursor.execute('INSERT INTO users (name, phone, email, EID, admin) VALUES(%s, %s, %s, %s, %s)' , (name, phone, email, EID, admin))
                    adminError = None
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

@app.route('/venuesubmitted')
def submitted_venue():
    bldg_code = request.form['bldg_code']
    floor_num = request.form['floor_num']
    room_num = request.form['room_num']
    room_capacity = request.form['room_capacity']

    if len(EID) != 7: ## NOT SURE HOW TO DO THIS <-- maybe do myAdmin == 1 
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
            userCheck = cursor.execute('SELECT * FROM users WHERE EID = %s', (myEID))
            entry = cursor.fetchall()
            num = list(entry)
            myAdmin=0

            for element in num:
                if element[5]==1:
                    myAdmin=1
                    cursor.execute('INSERT INTO  venues(bldg_code, floor_num, room_num, room_capacity) VALUES(%s, %d, %d, %d)' , (bldg_code, floor_num, room_num, room_capacity))
                    adminError = None
                else:
                    adminError = 'You are not allowed to perform this action!'
                    return render_template('login_index', adminError = adminError)
        cnx.commit()

        return render_template(
        'venuesubmitted.html',
        bldg_code = bldg_code,
        floor_num = floor_num,
        room_num = room_num,
        room_capacity = room_capacity,
        )
    

@app.route('/addevent')
def main3():
    return ('Help Me')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)