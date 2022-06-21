import os
import mysql.connector
from flask import (Flask, render_template, url_for, request, redirect, flash)

# DB Setup
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'rootpasswd123',
    database = 'contacts'
)
cursor = db.cursor()

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

# URL routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def messages():
    messages = []
    #
    if db.is_connected():
        cursor.execute('SELECT * FROM messages')
        messages = cursor.fetchall()
    else:
        messages.append(('-1', 'ERROR', 'support@organization.com', 'Failed to read messages; DB not connected'))
    #
    return render_template('messages.html', content = messages)

# Functionality
@app.route('/addmessage', methods = ['POST'])
def add_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    #
    command = 'INSERT INTO messages(name, email, message) VALUES (%s, %s, %s)'
    #
    if db.is_connected():
        try:
            cursor.execute(command, (name, email, message))
            db.commit()
            #
            flash('Message sent successfully')
        except:
            flash('Failed to send message; error in DB backend')
    else:
        flash('Failed to send message; DB not connected')
    #
    return redirect(url_for('index'))

@app.route('/deletemessage')
def delete_message():
    index = request.args.get('id')
    #
    command = 'DELETE FROM messages WHERE ID = %s'
    #
    if db.is_connected():
        try:
            cursor.execute(command, (index, ))
            db.commit()
            #
            flash('Message deleted successfully')
        except:
            flash('Failed to delete message; error in DB backend')
    else:
        flash('Failed to delete message; DB not connected')
    #
    return redirect(url_for('messages'))

# Start web server
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80, debug = True)

    # DB Cleanup
    if db.is_connected():
        db.close()
