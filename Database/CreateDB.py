import sqlite3
import json
from sqlite3 import Error

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS deputes
          (id INTEGER PRIMARY KEY, nom TEXT UNIQUE, x FLOAT, y FLOAT)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS texts
          (id INTEGER PRIMARY KEY, deputes_id INTEGER, text TEXT, FOREIGN KEY(deputes_id) REFERENCES deputes (id))
          ''')

with open('../scrapping/scrapping position/results.json', 'r') as f:
  deputes = json.load(f)

conn = sqlite3.connect('test.db')
c = conn.cursor()

for d in deputes:
    c.execute('''
              INSERT INTO deputes ( nom, x, y) VALUES
              (\"'''+str(deputes[d]["nom"])+'''\", \''''+str(deputes[d]["position"][0])+'''\', \''''+str(deputes[d]["position"][1])+'''\');
              ''')

conn.commit()