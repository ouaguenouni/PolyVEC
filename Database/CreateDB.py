import json
import psycopg2

conn = psycopg2.connect(
    host="195.154.45.91",
    database="politicometre",
    user="politicometre",
    password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
    sslmode ='disable')

c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS deputes
          (id SERIAL PRIMARY KEY, nom TEXT UNIQUE, x FLOAT, y FLOAT);
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS texts
          (id SERIAL PRIMARY KEY, deputes_id INTEGER, text TEXT, FOREIGN KEY(deputes_id) REFERENCES deputes (id));
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS transformation
          (id SERIAL PRIMARY KEY, text_id INTEGER, type INTEGER, result TEXT, FOREIGN KEY(text_id) REFERENCES texts (id));
          ''')

with open('../scrapping/scrapping position/results.json', 'r') as f:
  deputes = json.load(f)

for d in deputes:
    c.execute('''
              INSERT INTO deputes( nom, x, y)
              VALUES(\''''+str(deputes[d]["nom"].replace("'","''"))+'''\', \''''+str(deputes[d]["position"][0])+'''\', \''''+str(deputes[d]["position"][1])+'''\');
              ''')

conn.commit()