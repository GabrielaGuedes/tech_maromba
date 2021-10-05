from flask import Flask, request
import sqlite3
import json
import pdb

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
  return json.dumps(get_queue_for_machine(machine_id))

@app.route('/machines')
def machines():
  conn = get_db_connection()
  queue = conn.execute('SELECT * FROM machines').fetchall()
  return json.dumps(queue)

@app.route('/queue/<int:machine_id>/<int:user_id>')
def position_in_queue(machine_id, user_id):
  conn = get_db_connection()
  queue = get_queue_for_machine(machine_id)
  queue.sort(key=key_for_sorting_queue)
  user_id_queue = list(map(lambda x: x[QUEUE_ELEMENT_INDEXES['user_id']], queue))
  if user_id in user_id_queue:
    return f"{user_id_queue.index(user_id) + 1}"
  return "null"

@app.route('/queue/insert', methods=['POST'])
def insert_in_queue():
  machine_id = request.json['machine_id']
  user_id = request.json['user_id']
  series = request.json['series']
  repetitions = request.json['repetitions']
  
  if not machine_id or not user_id or not series or not repetitions:
    return "Missing required param"
  else:
    conn = get_db_connection()
    inserted = conn.execute('INSERT INTO queue_elements(machine_id, user_id, series, repetitions) VALUES(?, ?, ?, ?)',
                            (machine_id, user_id, series, repetitions))
    conn.commit()
    conn.close()
    return "Success"

def key_for_sorting_queue(queue_element):
  return queue_element[QUEUE_ELEMENT_INDEXES['inserted_at']]

def get_queue_for_machine(machine_id):
  conn = get_db_connection()
  return conn.execute('SELECT * FROM queue_elements WHERE machine_id = ? AND status = \'WAITING\'', (machine_id,)).fetchall()


