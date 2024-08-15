import mysql.connector
import pandas as pd
import networkx as nx
from utils.connector.mysql_conn import read_data

# Binary undirected graph : o <---> o

df = read_data('get_all_clubs')
print(df)
