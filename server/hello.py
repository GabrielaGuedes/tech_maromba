from flask import Flask, request, Response
import sqlite3
import json
import pdb
from flask_cors import CORS, cross_origin
import requests as rq

def get_db_connection():
  conn = sqlite3.connect('./database/database.db')
  return conn

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

QUEUE_ELEMENT_INDEXES = {
  'id': 0,
  'inserted_at': 1,
  'machine_id': 2,
  'user_id': 3,
  'series': 4,
  'repetitions': 5,
  'status': 6,
}

@app.route('/')
def index():
  return "Olá, maromba."

@app.route('/queue/<int:machine_id>')
def queue(machine_id):
  return json.dumps(get_current_user_waiting_machine(machine_id) + get_queue_for_machine(machine_id))

@app.route('/machines')
def machines():
  conn = get_db_connection()
  queue = conn.execute('SELECT * FROM machines').fetchall()
  return json.dumps(queue)

@app.route('/queue/<int:machine_id>/<int:user_id>')
def position_in_queue(machine_id, user_id, internal=False):
  conn = get_db_connection()
  queue = get_queue_for_machine(machine_id)
  queue.sort(key=key_for_sorting_queue)
  user_id_queue = list(map(lambda x: x[QUEUE_ELEMENT_INDEXES['user_id']], queue))
  if internal:
    if user_id in user_id_queue:
      return f"{user_id_queue.index(user_id) + 1}"
    return "null"
  else:
    if user_id in user_id_queue:
      return Response("{\"result\": " + f"\"{user_id_queue.index(user_id) + 1}\"" + "}", status=200, mimetype='application/json')
    return Response("{\"result\":\"null\"}", status=400, mimetype='application/json')

@app.route('/queue/insert', methods=['POST'])
def insert_in_queue():
  machine_id = request.json['machine_id']
  user_id = request.json['user_id']
  series = request.json['series']
  repetitions = request.json['repetitions']
  
  if not machine_id or not user_id or not series or not repetitions:
    return Response("{\"result\":\"Missing required param\"}", status=400, mimetype='application/json')
  else:
    if is_user_in_queue(machine_id, user_id):
      return Response("{\"result\":\"Failed. User already is in queue\"}", status=400, mimetype='application/json')
    conn = get_db_connection()
    inserted = conn.execute('INSERT INTO queue_elements(machine_id, user_id, series, repetitions) VALUES(?, ?, ?, ?)',
                            (machine_id, user_id, series, repetitions))
    conn.commit()
    conn.close()
    if int(position_in_queue(machine_id, user_id, True)) == 1 and not is_someone_at_machine(machine_id):
      queue = get_queue_for_machine(machine_id)
      call_first_from_queue(queue)
    return Response("{\"result\":\"Success\"}", status=200, mimetype='application/json')

@app.route('/queue/remove_first/<int:machine_id>', methods=['POST'])
def finish_execution(machine_id):
  remove_current_user_from_queue(machine_id)
  updated_queue = get_queue_for_machine(machine_id)
  if len(updated_queue) > 0:
    call_first_from_queue(updated_queue)
  return Response("{\"result\":\"Success\"}", status=200, mimetype='application/json')

@app.route('/notifications/<int:user_id>')
def notifications(user_id):
  conn = get_db_connection()
  return json.dumps(conn.execute('SELECT * FROM notifications WHERE user_id = ? ORDER BY inserted_at DESC', (user_id,)).fetchall())

@app.route('/queue/user_arrived/<int:user_id>/<int:machine_id>', methods=['POST'])
def user_arrived(user_id, machine_id):
  conn = get_db_connection()
  user_in_queue = conn.execute('SELECT * FROM queue_elements WHERE machine_id = ? AND status = \'WAITING_CONFIRMATION\' AND user_id = ?', (machine_id, user_id)).fetchall()[0]
  conn.close()
  if user_in_queue:
    repetitions = user_in_queue[QUEUE_ELEMENT_INDEXES['repetitions']]
    series = user_in_queue[QUEUE_ELEMENT_INDEXES['series']]
    queue_element_id = user_in_queue[QUEUE_ELEMENT_INDEXES['id']]
    try:
      rq.get(f'http://localhost:5000/{series}/{repetitions}')
    except:
      print("não foi possível se comunicar com o embarcado")
    update_first_from_queue_status(user_in_queue, "DOING")
    return Response("{\"result\":\"Success\"}", status=200, mimetype='application/json')
  else:
    return Response("{\"result\":\"User not found\"}", status=400, mimetype='application/json')

def key_for_sorting_queue(queue_element):
  return queue_element[QUEUE_ELEMENT_INDEXES['inserted_at']]

def get_queue_for_machine(machine_id):
  conn = get_db_connection()
  return conn.execute('SELECT * FROM queue_elements WHERE machine_id = ? AND status = \'WAITING\' ORDER BY inserted_at ASC', (machine_id,)).fetchall()

def get_current_user_waiting_machine(machine_id):
  conn = get_db_connection()
  return conn.execute('SELECT * FROM queue_elements WHERE machine_id = ? AND status = \'WAITING_CONFIRMATION\'', (machine_id,)).fetchall()

def is_user_in_queue(machine_id, user_id):
  position = position_in_queue(machine_id, user_id, True)
  if position != "null":
    return True
  else:
    return False

def remove_current_user_from_queue(machine_id):
  conn = get_db_connection()
  conn.execute('UPDATE queue_elements SET status = \'DONE\' WHERE machine_id = ? AND status = \'DOING\'', (machine_id,))
  conn.commit()
  conn.close()

def call_first_from_queue(queue):
  first = queue[0]
  notify_first_from_queue(first)
  update_first_from_queue_status(first, "WAITING_CONFIRMATION")

def update_first_from_queue_status(user_in_queue, new_status):
  conn = get_db_connection()
  conn.execute('UPDATE queue_elements SET status = ? WHERE id = ?', (new_status, user_in_queue[QUEUE_ELEMENT_INDEXES['id']],))
  conn.commit()
  conn.close()

def notify_first_from_queue(user_in_queue):
  conn = get_db_connection()
  machine_name = conn.execute('SELECT name FROM machines WHERE id = ?', (user_in_queue[QUEUE_ELEMENT_INDEXES['machine_id']],)).fetchall()[0][0]
  notification_message = f"Sua vez no aparelho {machine_name} chegou!"
  conn.execute('INSERT INTO notifications(user_id, machine_id, description) VALUES(?, ?, ?)',
                          (user_in_queue[QUEUE_ELEMENT_INDEXES['user_id']], user_in_queue[QUEUE_ELEMENT_INDEXES['machine_id']], notification_message))
  conn.commit()
  conn.close()

def is_someone_at_machine(machine_id):
  conn = get_db_connection()
  users = conn.execute('SELECT * FROM queue_elements WHERE machine_id = ? AND status = \'WAITING_CONFIRMATION\' OR status = \'DOING\'', (machine_id,)).fetchall()
  if len(users) > 0:
    return True
  else:
    return False
