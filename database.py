import pymysql
from app import app
#Establishes connection to SQL database with login criteria based on contents in config file
def get_connection():
    return pymysql.connect(host=app.config['DB_HOST'],
                           user=app.config['DB_USER'],
                           password=app.config['DB_PASS'],
                           database=app.config['DB_DATABASE'],
                           cursorclass=pymysql.cursors.DictCursor)
#Calls events from SQL database
def get_events():
    sql = "SELECT * FROM events ORDER BY date"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
#Inserts new events into database
def insert_event(name, date, host, description):
    sql = "INSERT INTO events (name, date, host, description) values (%s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, date, host, description))
        conn.commit()
# Selects information of a specific event based on event id
def get_event(event_id):
    sql = "SElECT * FROM events WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id))
            return cursor.fetchone()

#Updates existing event in SQL database
def edit_event(name, date, host, description, event_id):
    sql = 'UPDATE events SET name = %s, date = %s, host = %s, description = %s WHERE event_id = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, date, host, description, event_id))
        conn.commit()
#Drops events from the events table in the database
def delete(event_id):
    sql = "DELETE FROM events WHERE event_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id))
        conn.commit()
#Inserts attendee based on user inout
def insert_attendee(name, email, comment, event_id):
    sql = "INSERT INTO attendees (event, name, email, comment) VALUES (%s, %s, %s, %s)"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, email, comment, event_id))
        conn.commit()
#Pulls attendees from dataabse
def get_attendees(event_id):
    sql = 'SELECT * FROM attendees WHERE event = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (event_id))
            return cursor.fetchall()
#Pulls data for a specfic attendee based on their id
def get_attendance(id, event_id):
    sql = 'SELECT * FROM attendees WHERE attendee_id= %s AND event= %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (id, event_id))
            return cursor.fetchone()
#Updates an existing attendees data in the database
def edit_attendee(id, name, email, comment):
    sql = 'UPDATE attendees SET name = %s, email = %s, comment = %s WHERE attendee_id = %s'
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, email, comment, id))
        conn.commit()
#Removes attendees if the user desires
def delete_attendee(attendee_id):
    sql = "DELETE FROM attendees WHERE attendee_id = %s"
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (attendee_id))
        conn.commit()







