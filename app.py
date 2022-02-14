from os import EX_TEMPFAIL, name
from flask import Flask, render_template, request, url_for, redirect
import csv
from os.path import exists

from flask.wrappers import Request

app = Flask(__name__)

if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')

import database

#Data validation for events
def check_event(name, host):
    error = ""
    msg =[]
    if not name:
        msg.append("Event name is missing!")
    if not host:
        msg.append("Host is missing!")
    if len(msg) > 0:
        error = "\n".join(msg)
    return error
#Data validation for attendees
def check_attendee(name):
    error = ""
    msg = []
    if not name:
        msg.append("Name is missing!")
    if len(name) > 30:
        msg.append("Name is too long!")
    if len(msg) > 0:
        error = "\n".join(msg)
    return error




#Renders index template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events/')
def list_events():
    events = database.get_events()
    return render_template('events.html', events=events)

#Pulls data from SQL database and makes it so the HTML pull from it
@app.route('/events/<event_id>')
def events(event_id=None):
    if event_id:
        event_id = int(event_id)
        event = database.get_event(event_id)
        attendees = database.get_attendees(event_id)
        return render_template('event.html',event_id = event_id,event=event, attendees=attendees)
    else:
        events = database.get_events()
        return redirect(url_for('list_events', events=events))
    
#Adds functionality for the user to add thier own events by pulling the data from the CSV adding the new data and uses the set_event to send it back into the CSV
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        date = request.form['date']
        name = request.form['name']
        host= request.form['host']
        description = request.form['description']
        error = check_event(name, host)
        if error:
            return render_template("events_form.html", error = error, name = name, host=host)
        database.insert_event(name,date,host,description)
        return redirect(url_for('events'))
    else:
        return render_template('events_form.html')
#Adds functionality to remove events from the SQL database by pulling from the database adn running the delete function from database to remove the events as well as removing all attendees from that event
@app.route('/events/<event_id>/delete', methods=['GET', 'POST'])
def delete(event_id=None):
    if request.method != 'POST':
        event_id = int(event_id)
        event = database.get_event(event_id)
        return render_template('delete_form.html', event = event)
    else: 
        event_id = int(event_id)
        attendees = database.get_attendees(event_id)
        for attendee in attendees:
            database.delete_attendee(attendee['attendee_id'])
        database.delete(event_id)
        return redirect(url_for('list_events'))
#Pulls data from a specified event then removes the old data and replaces it with the data entered by the user
@app.route('/events/<event_id>/edit', methods=['GET', 'POST'])
def edit(event_id=None):
    event_id = event_id
    event = database.get_event(event_id)
    if request.method == 'POST':
        date = request.form['date']
        name = request.form['name']
        host = request.form['host']
        description = request.form['description']
        database.edit_event(name, date, host, description, event_id)
        return redirect(url_for('events', event_id=event_id))
    else:
        return render_template('events_form.html', event = event)

#Adds attendes to SQL database and pulls from database function to route to SQL
@app.route('/events/<event_id>/attendees/add', methods=['GET', 'POST'])
def add_attendee(event_id=None):
    if request.method =='POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']
        error = check_attendee(name)
        if error:
            return render_template("attendee_form.html", error =error, name = name)
        database.insert_attendee(event_id, name, email, comment)
        return redirect(url_for('events', event_id=event_id))
    else:
        return render_template("attendee_form.html")

#Edits the database for attendees and pulls from database function to route to SQL
@app.route('/events/<event_id>/attendees/<attendee_id>/edit', methods = ['GET', 'POST'])
def edit_attendee(attendee_id=None, event_id=None):
    event_id = int(event_id)
    event = database.get_event(event_id)
    attendee_id = int(attendee_id)
    attendee = database.get_attendance(attendee_id, event_id)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']
        database.edit_attendee(attendee_id, name, email, comment)
        return redirect(url_for('events', event_id=event_id))
    else:
        return render_template('attendee_form.html', event=event, attendee=attendee)


#Deletes the database for attendees and pulls from database function to route to SQL
@app.route('/events/<event_id>/attendees/<attendee_id>/delete')
def delete_attendee(attendee_id=None, event_id=None):
    if attendee_id:
        attendee_id = int(attendee_id) 
        event_id=int(event_id)
        database.delete_attendee(attendee_id)
        return redirect(url_for('events', event_id=event_id))