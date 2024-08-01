import sqlite3
import time
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS counter_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        json_data TEXT
    )
''')
n=  0
while True:
    n +=1
    cursor.execute("INSERT INTO counter_data (timestamp, json_data) VALUES (datetime('now'), '"+str(n)+"')")
    conn.commit()   
    time.sleep(1)