from ASTR_DSU.dsu.dsu import StringDSU
from ASTR_DSU.data.data_streamer import stream_edges_from_disk

def main():
    dsu = StringDSU()
    file_path = "mock_database.csv" 
    
    print("Streaming data and building graph...")
    
    # The DSU consumes the generator stream directly
    for node1, node2 in stream_edges_from_disk(file_path):
        dsu.union(node1, node2)
        
    print("\nFinal Identity Groups Resolved:\n" + "-"*30)
    
    groups = dsu.get_grouped_components()
    for root, members in groups.items():
        print(f"Root Identity: {root} (Size: {dsu.size[root]})")
        print(f"Linked Records: {members}\n")

if __name__ == "__main__":
    main()