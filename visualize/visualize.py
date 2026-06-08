import networkx as nx
from pyvis.network import Network
from ASTR_DSU.dsu.dsu import StringDSU
from ASTR_DSU.data.data_streamer import stream_edges_from_disk

def visualize_dsu_graph(file_path):
    dsu = StringDSU()
    # Create a NetworkX graph object
    G = nx.Graph()
    
    print("Processing DSU and building graph...")
    
    # 1. Process data through DSU
    for node1, node2 in stream_edges_from_disk(file_path):
        dsu.union(node1, node2)
        
    # 2. Add nodes and edges to the visual graph based on the DSU parent structure
    # We will draw edges from every node directly to its DSU Root (Simulating Path Compression)
    groups = dsu.get_grouped_components()
    
    for root, members in groups.items():
        # Add the root node, made slightly larger
        G.add_node(root, title="ROOT IDENTITY", size=25, group=root)
        
        for member in members:
            if member != root:
                # Add child nodes and connect them to the root
                G.add_node(member, title="Alias", size=15, group=root)
                G.add_edge(member, root)

    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    print("Generating interactive HTML file...")

    # 3. Create the PyVis network
    # notebook=False ensures it runs as a standalone HTML file
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", select_menu=True)
    
    # Import the NetworkX graph into PyVis
    net.from_nx(G)
    
    # Add physics controls so you can play with the gravity and bounce
    net.show_buttons(filter_=['physics'])
    
    # Save and open the file
    output_file = "dsu_visualization.html"
    net.save_graph(output_file)
    print(f"Success! Open '{output_file}' in your web browser to see the visualization.")

if __name__ == "__main__":
    visualize_dsu_graph("mock_database.csv")