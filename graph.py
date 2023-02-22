import networkx as nx
import pymongo

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
n_db = client["n_db"]

# Create a Graph object
G = nx.Graph()

# Function to compare nodes and create an edge between them
def compare_and_connect(G, node1, node2):
    if G.nodes[node1]["value"]["source"]["name"] == G.nodes[node2]["value"]["source"]["name"]:
        G.add_edge(node1, node2)
    if G.nodes[node1]["value"]["author"] == G.nodes[node2]["value"]["author"]:
        G.add_edge(node1, node2)
    elif G.nodes[node1]["date"] == G.nodes[node2]["date"]:
        G.add_edge(node1, node2)

# Function to search a node in the graph based on article id
def search_node(article_id):
    for node in G.nodes:
        if node == article_id:
            for neighbor in G[node]:
                return G.nodes[neighbor]

# Iterate over all collections in the database
for coll_name in n_db.list_collection_names():
    collection = n_db[coll_name]
    
    # Add nodes with values from the objects in the collection
    for obj in collection.find():
        node_name = f"{obj['_id']}"

        # Skip processing the "users" collection
        if collection.name == "users":
            continue
        
        G.add_node(node_name, value=obj['value'], date=obj.get("date", None))

# Iterate over all pairs of nodes and compare their "date" values
for i, node1 in enumerate(G.nodes):
    for j in range(i+1, len(G.nodes)):
        node2 = list(G.nodes)[j]
        compare_and_connect(G, node1, node2)