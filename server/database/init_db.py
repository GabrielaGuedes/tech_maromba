import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO machines (name) VALUES (?)",
            ('Cadeira extensora',)
            )
cur.execute("INSERT INTO machines (name) VALUES (?)",
            ('Cadeira flexora',)
            )
cur.execute("INSERT INTO machines (name) VALUES (?)",
            ('Cadeira abdutora',)
            )
cur.execute("INSERT INTO machines (name) VALUES (?)",
            ('Cadeira adutora',)
            )
cur.execute("INSERT INTO machines (name) VALUES (?)",
            ('Leg press',)
            )
cur.execute("INSERT INTO machines (name) VALUES (?)",
            ('Pulley',)
            )

cur.execute("INSERT INTO users (name) VALUES (?)",
            ('Larry Lagosta',)
            )
cur.execute("INSERT INTO users (name) VALUES (?)",
            ('Dobby Maromba',)
            )
cur.execute("INSERT INTO users (name) VALUES (?)",
            ('Emoji Maromba',)
            )
cur.execute("INSERT INTO users (name) VALUES (?)",
            ('Moana Maromba',)
            )
cur.execute("INSERT INTO users (name) VALUES (?)",
            ('Tuk Maromba',)
            )

cur.execute("INSERT INTO queue_elements (machine_id, user_id, series, repetitions) VALUES (?, ?, ?, ?)",
            (1, 1, 4, 10)
            )

connection.commit()
connection.close()