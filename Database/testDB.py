import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("SELECT nom,text FROM texts JOIN deputes ON texts.deputes_id = deputes.id")

result = c.fetchall()

for row in result:
    print(row)
    print("\n")