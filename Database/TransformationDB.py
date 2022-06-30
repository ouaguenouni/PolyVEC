import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="195.154.45.91",
    database="politicometre",
    user="politicometre",
    password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
    sslmode ='disable')

def newTransformation(id,type,result):
    c = conn.cursor()
    c.execute('''
                  INSERT INTO deputes( text_id, type, result)
                  VALUES(\'''' + id + '''\', \'''' + type + '''\', \'''' + result + '''\');
                  ''')