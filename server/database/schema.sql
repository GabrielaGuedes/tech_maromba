DROP TABLE IF EXISTS queue_elements;
DROP TABLE IF EXISTS machines;
DROP TABLE IF EXISTS users;

CREATE TABLE queue_elements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  inserted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  machine_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  series INTEGER NOT NULL,
  repetitions INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'WAITING'
);

CREATE TABLE machines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  busy BOOLEAN DEFAULT FALSE
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);