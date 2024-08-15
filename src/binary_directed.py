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
out_degrees = dict(G.out_degree())

in_degrees_df = pd.DataFrame(
    list(in_degrees.items()), columns=['Club_ID', 'Degree'])
out_degrees_df = pd.DataFrame(
    list(out_degrees.items()), columns=['Club_ID', 'Degree'])


in_degrees_df['Degree Type'] = 'In-Degree'
out_degrees_df['Degree Type'] = 'Out-Degree'

# Combine both DataFrames
combined_df = pd.concat([in_degrees_df, out_degrees_df])

combined_df = combined_df[combined_df['Degree'] != 0]

combined_df.to_csv('degrees.csv', index=False)

# Count occurrences of each degree type
degree_counts = combined_df.groupby(
    ['Degree Type', 'Degree']).size().reset_index(name='Count')

# Plotting the scatter plot
plt.figure(figsize=(10, 6))
# sns.scatterplot(data=degree_counts, x='Degree', y='Count', hue='Degree_Type', style='Degree_Type', palette={'In-Degree': 'blue', 'Out-Degree': 'red'}, s=100, alpha=0.7)

sns.lmplot(
    data=degree_counts,
    x="Degree", y="Count", hue="Degree Type",
    height=5, palette={'In-Degree': 'blue', 'Out-Degree': 'red'}, markers=['o', 'x']
)

# Add labels and title
plt.xlabel('Degree')
plt.ylabel('Number of nodes')

print("edges>" + str(G.number_of_edges()))
print("nodes>" + str(G.number_of_nodes()))

plt.savefig("output_plot.png")
