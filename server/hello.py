from flask import Flask
import sqlite3
import json

def get_db_connection():
  conn = sqlite3.connect('./database/database.db')
  return conn

app = Flask(__name__)

QUEUE_ELEMENT_INDEXES = {
  'id': 0,
  'inserted_at': 1,
  'machine_id': 2,
  'user_id': 3,
  'series': 4,
  'repetition': 5,
  'status': 6,
}

@app.route('/')
def index():
  return "Olá, maromba."

@app.route('/queue/<int:machine_id>')
def queue(machine_id):
  return get_queue_for_machine(machine_id)

@app.route('/machines')
def machines():
  conn = get_db_connection()
  queue = conn.execute('SELECT * FROM machines').fetchall()
  return json.dumps(queue)

@app.route('/queue/<int:machine_id>/<int:user_id>')
def position_in_queue(machine_id, user_id):
  conn = get_db_connection()
  queue = get_queue_for_machine(machine_id)
  sorted_queue = queue.sort(key=key_for_sorting_queue).index(user_id)
  user_id_queue = list(map(lambda x: x[QUEUE_ELEMENT_INDEXES['user_id']], sorted_queue))
  return user_id_queue.index(user_id) + 1

@app.route('/queue/insert/<int:machine_id>/<int:user_id>/<int:series>/<int:repetitions>')
def insert_in_queue(machine_id, user_id):
  conn = get_db_connection()
  inserted = conn.execute('INSERT INTO queue_elements(machine_id, user_id, series, repetitions) VALUES(machine_id, user_id, series, repetitions)')

def key_for_sorting_queue(queue_element):
  return queue_element[QUEUE_ELEMENT_INDEXES['inserted_at']]

def get_queue_for_machine(machine_id):
  conn = get_db_connection()
  queue = conn.execute('SELECT * FROM queue_elements WHERE machine_id = ? AND status = \'WAITING\'', (machine_id,)).fetchall()
  return json.dumps(queue)


