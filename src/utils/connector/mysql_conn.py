import mysql.connector
import pandas as pd
from ..sql.queries import queries


def read_data(key):
    connection = mysql.connector.connect(
        host='localhost',
        user='user',
        password='user',
        database='tm_db',
        port=3307
    )
    df = pd.read_sql(queries[key], connection)
    connection.close()
    return df
