import pandas as pd
import psycopg2

def get_df(req):
    """
    Run an SQL Query on our dataset and return the result in the form of a Python dictionnary.
    """
    conn = psycopg2.connect(
        host="195.154.45.91",
        database="politicometre",
        user="politicometre",
        password="095a520b4023169a50fee97f1c4bb856fbf4e9a8a9ac1247",
        sslmode ='disable')
    c = conn.cursor()
    c.execute(req)
    cols = ([desc[0] for desc in c.description])
    data = {col:[] for col in cols}
    for it in c:
        for i in range(len(it)):
            data[cols[i]].append(it[i])
    return data