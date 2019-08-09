def adduser(EID_admin, name, phone, email, EID, admin):
    ## Grabs the row of information that connects to the user_id
    adminCheck = cursor.execute('''SELECT * FROM users WHERE EID = ? ''', (EID_admin,))
    entry = cursor.fetchone()

    ## Checking that the user is an admin
    if entry[5] == 1: 
        sql = "INSERT INTO users(name, phone, email, EID, admin) VALUES(?, ?, ?, ?, ?)"
        cursor.execute(sql, (name, phone, email, EID, admin))
        db.commit()
        return('New user added')
    else:
        raise Exception('ERROR: Not an admin') 


## Adding a venue

import datetime

def addvenue(EID_admin, bldg_code, floor_num, room_num, room_capacity):
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
        
    ## Grabs the row of information that connects to the user_id
    adminCheck = cursor.execute('''SELECT * FROM users WHERE EID = ? ''', (EID_admin,))
    entry = cursor.fetchone()

    ## Checking that the user is an admin
    if entry[5] == 1: 
        sql = "INSERT INTO venues(bldg_code, floor_num, room_num, room_capacity) VALUES(?, ?, ?, ?)"
        cursor.execute(sql, (bldg_code, floor_num, room_num, room_capacity))
        
        venue = cursor.lastrowid
        
        for time in hours:
            cursor.execute("INSERT INTO Time(venue_id, timeslot) values (?,?)", (venue,time,))
        db.commit()
        return('New venue added')
    else:
        raise Exception('ERROR: Not an admin') 
## start an event
from datetime import datetime, timedelta

def add_event(name, description, expected_attendance, venue_id, event_owner, start_time):
    cursor = db.cursor()
    adminCheck = cursor.execute('''SELECT * FROM venues WHERE venue_id = ? ''', (venue_id,))
    entry = cursor.fetchone()
    
    if expected_attendance < int(entry[4]):  
        venueCheck = cursor.execute('''SELECT * FROM Time WHERE venue_id = ? AND timeslot = ?''', (venue_id, start_time,))
        timeEntry = cursor.fetchone()
        #print(timeEntry)
        
        if timeEntry[1] is None: 
            sql = "INSERT INTO events(name, description, expected_attendance, venue_id, event_owner, start_time) VALUES(?, ?, ?, ?, ?, ?)"
            cursor = db.cursor()
            cursor.execute(sql, (name, description, expected_attendance, venue_id, event_owner, start_time))

            updateTime = "UPDATE Time SET event_id = ? WHERE timeslot = ? and venue_id = ? "
            updateCount = "UPDATE Events SET current_attendance = 1"
            insertJoin = "INSERT INTO confirmedEvents(event_id, user_id) VALUES (?, ?)"      
           
            sqlEID = "SELECT user_id FROM users WHERE EID = ?"
            cursor.execute(sqlEID, (event_owner,))
            row = cursor.fetchall()
            num = list(sum(row, ()))

            cursor.execute(insertJoin, (num[0], cursor.lastrowid))
            cursor.execute(updateTime,(cursor.lastrowid, start_time, venue_id))
            cursor.execute(updateCount)
#             joinEvent(event_owner,cursor.lastrowid)
            return('New event added')
        else:
            raise Exception('Error: Room already booked for that time')
    else:
        raise Exception('ERROR: Room capacity exceeded')
    
def freeTimeAtVenue(venue):
    sql =  "SELECT Timeslot FROM Time WHERE event_id is null AND venue_id = ?"
    cursor.execute (sql, (venue,))
    row = cursor.fetchall()
    num = list(sum(row, ()))
    print ("Free times for this venue are:")
    print (num)

def freeVenueAtTime(time):
    sql =  "SELECT venue_id FROM Time WHERE event_id is null AND timeslot = ?"
    cursor.execute(sql, (time,) )
    row = cursor.fetchall()
    num = list(sum(row, ()))
    print ("Venues that are free at this time are:")
    #return (num)
    for element in num:
        sql1 = "SELECT bldg_code, floor_num, room_num FROM venues WHERE venue_id = ?"
        cursor.execute(sql1, (element,) )
        row1 = cursor.fetchall()
        num1 = list(sum(row1, ()))
        print (num1)

def listedEvents(bldg_code, floor_num, room_num, time):
    venue_name = "SELECT venue_id FROM venues WHERE bldg_code = ? AND floor_num = ? AND room_num = ? "
    cursor.execute(venue_name, (bldg_code, floor_num, room_num,) )
    row1 = cursor.fetchall()
    num1 = list(sum(row1, ()))

    sql =  "SELECT event_id FROM Time WHERE venue_id=? AND timeslot = ?"
    
    for element1 in num1:
        cursor.execute(sql, (element1, time,))
        
    row = cursor.fetchall()
    num = list(sum(row, ()))
    print ("Events in %s %i.%i at %s:" % (bldg_code,floor_num,room_num,time))

    for element in num:
        sql1 = "SELECT name FROM events WHERE event_id = ?"
        cursor.execute(sql1, (element,) )
        row1 = cursor.fetchall()
        num1 = list(sum(row1, ()))
        print (num1)

def joinEvent(user_EID, event_id):
    sql = "SELECT user_id FROM users WHERE EID = ?"
    cursor.execute(sql, (user_EID,))
    row = cursor.fetchall()
    num = list(sum(row, ()))
    
    current_sql= "SELECT current_attendance FROM events WHERE event_id = ?"
    cursor.execute(current_sql,(event_id,))
    cur =  cursor.fetchall()
    
    total_sql= "SELECT expected_attendance FROM events WHERE event_id = ?"
    cursor.execute(total_sql,(event_id,))
    tot = cursor.fetchall()
    
    if cur[0] < tot[0]:
        sd = []
        for element in num:
            stopDuplicates = "SELECT * FROM confirmedEvents WHERE user_id = ? AND event_id = ?"
            cursor.execute(stopDuplicates, (element, event_id))
            sd = cursor.fetchall()
            print(sd)
            if len(sd)==0:
                sql1 = "INSERT INTO confirmedEvents(user_id, event_id) VALUES(?, ?) "
                cursor.execute(sql1, (element, event_id,))
                updateCount = "UPDATE Events SET current_attendance = current_attendance + 1"
                cursor.execute(updateCount)
            else:
                raise Exception('Error: This user is already going to this event')

    else:
        raise Exception('Error: Event is fully booked')

def remove_event(admin_EID, event_id):
    ## Grabs the row of information that connects to the user_id
    adminCheck = cursor.execute('''SELECT * FROM users WHERE EID = ? ''', (admin_EID,))
    entry = cursor.fetchone()

    ## Checking that the user is an admin
    if entry[5] == 1: 
        events_sql = ('''DELETE FROM events WHERE event_id = ?''')
        cs_sql = ('''DELETE FROM confirmedEvents WHERE event_id = ?''')
        cursor.execute(events_sql, (event_id,))
        cursor.execute(cs_sql, (event_id,))
        db.commit()
        return('Event deleted')
    else:
        raise Exception('ERROR: Not an admin') 