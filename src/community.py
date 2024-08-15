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
    if G.has_edge(origin, destination):
        G[origin][destination]['weight'] += 1
    else:
        G.add_edge(origin, destination, weight=1)


community = nx.community.louvain_communities(G)

print("edges>" + str(G.number_of_edges()))
print("nodes>" + str(G.number_of_nodes()))


colors = {}
for i, com in enumerate(community):
    color = plt.cm.tab20(i)  # Use a colormap for coloring the communities
    for node in com:
        colors[node] = color

# Draw the graph
plt.figure(figsize=(10, 8))

# Position the nodes using a layout algorithm
pos = nx.spring_layout(G, seed=42)

# Draw nodes with the assigned community colors
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=[colors[node] for node in G.nodes()])
nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=15)
nx.draw_networkx_labels(G, pos)

plt.title("Communities in Soccer Transfer Network")
plt.show()
# plt.savefig("output_plot.png")
