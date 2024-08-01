import sqlite3
conn = sqlite3.connect('example.db')

cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS counter_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        json_data TEXT
    )
''')



cursor.execute("INSERT INTO counter_data (timestamp, json_data) VALUES (?, ?)", ('2022-10-15 08:30:00', 'example'))
conn.commit()   



cursor.execute("SELECT * FROM counter_data ORDER BY id DESC LIMIT 1")
last_row = cursor.fetchone()

print(last_row)