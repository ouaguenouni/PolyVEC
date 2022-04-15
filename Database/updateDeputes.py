import json
import sqlite3

with open('../scrapping/scrapping position/results.json', 'r') as f:
  deputes = json.load(f)

conn = sqlite3.connect('test.db')
c = conn.cursor()

for d in deputes:
    c.execute('''
              UPDATE deputes 
              SET x = \''''+str(deputes[d]["position"][0])+'''\', y =\''''+str(deputes[d]["position"][1])+'''\'
              WHERE nom =\"'''+str(deputes[d]["nom"])+'''\";''')

conn.commit()