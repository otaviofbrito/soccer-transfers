import pandas as pd
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt

from utils.connector.mysql_conn import read_data


# Not loans - Binary Directed : (i) ----> (j)

df = read_data('get_all_not_loan_transfers')

# Build graph

G = nx.DiGraph()


for _, row in df.iterrows():
    origin = row['left_club_id']
    destination = row['joined_club_id']
    G.add_edge(origin, destination)


in_degrees = dict(G.in_degree())

in_degrees_df = pd.DataFrame(list(in_degrees.items()), columns=[
                             'Club_ID', 'In_Degree'])

in_degrees_df.to_csv('in_degrees.csv', index=False)

sns.set_theme(style="darkgrid")
sns.lineplot(data=in_degrees_df, x='Club_ID', y='In_Degree',
             marker='o', markersize=4, palette='mako')
plt.savefig("output_plot.png")
