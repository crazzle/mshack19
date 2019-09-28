import pathlib

from models.database import DatabaseConnection
import pandas as pd

"""
delete db and recreate it
"""

def normalize(s):
    return (s-s.min())/(s.max()-s.min())

db_file = pathlib.Path.cwd().parent.joinpath('database', 'features.db')
pathlib.Path.unlink(db_file)  # THIS DELETES THE DB

db = DatabaseConnection(db_file)

data = pd.read_csv("../datasets/final.csv")
data[["public_transport","nightlife","shops","near_university","avg_cost"]] = data[["public_transport","nightlife","shops","near_university","avg_cost"]].apply(normalize, axis=0)

with db:
    db.cursor.execute("""
        create table standard_heat(
                lat,
                long,
                public_transport,
                nightlife,
                shops,
                near_university,
                avg_cost
            )
    """)
    db.cursor.executemany('INSERT INTO standard_heat VALUES (?,?,?,?,?,?,?)', data.values.tolist())
    db.connection.commit()
