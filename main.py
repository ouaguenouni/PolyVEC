from api.database import *
import pandas as pd

def test_df_loading():
    d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 10")
    df = pd.DataFrame(d)
    print(df)

d = get_df("SELECT nom, text, x, y from deputes join texts on texts.deputes_id = deputes.id LIMIT 10")
df = pd.DataFrame(d)
print(df["texts"][0])
