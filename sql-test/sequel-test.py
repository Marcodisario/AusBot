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

