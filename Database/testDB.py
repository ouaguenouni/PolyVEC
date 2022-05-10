import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="195.154.45.91",
    database="politicometre",
    user="politicometre",
    password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
    sslmode ='disable')

def run(req):
    c = conn.cursor()
    c.execute(req)
    cols = ([desc[0] for desc in c.description])
    data = {col:[] for col in cols}
    for it in c:
        for i in range(len(it)):
            data[cols[i]].append(it[i])
    return data


#conn = sqlite3.connect('test.db')
c = conn.cursor()

ch = """
SELECT
    table_schema || '.' || table_name
FROM
    information_schema.tables
WHERE
    table_type = 'BASE TABLE'
AND
    table_schema NOT IN ('pg_catalog', 'information_schema');
"""

#result = run(ch).fetchall()
#print("Result: ", result)

D = run("SELECT * FROM deputes LIMIT 10")
D = run("SELECT * FROM texts LIMIT 10")
D = run("SELECT nom, text, x, y from texts join deputes ON deputes.id=texts.deputes_id LIMIT 10")
df = pd.DataFrame(D)
print(df)

#for r in results2:
#print(r)


