import psycopg2

conn = psycopg2.connect(
    host="195.154.45.91",
    database="politicometre",
    user="politicometre",
    password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
    sslmode ='disable')

#conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM texts")

result = c.fetchall()

for row in result:
    print(row)
    print("\n")