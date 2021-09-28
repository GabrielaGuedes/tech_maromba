from flask import Flask
import sqlite3
import json

def get_db_connection():
  conn = sqlite3.connect('./database/database.db')
  return conn

app = Flask(__name__)

@app.route('/')
def index():
  return "Olá, maromba."

@app.route('/queue/<int:machine_id>')
def queue(machine_id):
  conn = get_db_connection()
  queue = conn.execute('SELECT * FROM queue_elements WHERE machine_id = ?', (machine_id,)).fetchall()
  return json.dumps(queue)

@app.route('/machines')
def machines():
  conn = get_db_connection()
  queue = conn.execute('SELECT * FROM machines').fetchall()
  return json.dumps(queue)

