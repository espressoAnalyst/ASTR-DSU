import os
import pprint

class DiskDSU:
    def __init__(self):
        # Maps string token to an integer ID for fast DSU operations
        self.string_to_id = {}
        self.id_to_string = []  # Array index acts as the integer ID
        
        # Core DSU structures using integer IDs
        self.parent = []
        self.rank = []

    def _get_or_create_id(self, node_str: str) -> int:
        """Assigns a unique integer ID to a string node if it doesn't exist."""
        if node_str not in self.string_to_id:
            new_id = len(self.id_to_string)
            self.string_to_id[node_str] = new_id
            self.id_to_string.append(node_str)
            
            # Initialize DSU structures for this new element
            self.parent.append(new_id)
            self.rank.append(0)
            return new_id
        return self.string_to_id[node_str]

    def find(self, i: int) -> int:
        """Find the representative of the set with iterative path compression."""
        root = i
        while root != self.parent[root]:
            root = self.parent[root]
            
        # Path compression
        curr = i
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt
            
        return root

    def union(self, u_str: str, v_str: str) -> bool:
        """Unites the sets containing u_str and v_str. Returns True if a union happened."""
        root_u = self.find(self._get_or_create_id(u_str))
        root_v = self.find(self._get_or_create_id(v_str))

        if root_u != root_v:
            # Union by Rank
            if self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            elif self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False

    def get_string_components_dict(self) -> dict:
        """
        Processes the internal tree and returns a standard Python dictionary.
        Keys: Root string element of a component.
        Values: List of all string elements belonging to that component.
        """
        components = {}
        for node_str, node_id in self.string_to_id.items():
            root_id = self.find(node_id)
            root_str = self.id_to_string[root_id]
            
            if root_str not in components:
                components[root_str] = []
            components[root_str].append(node_str)
            
        return components


def run_dsu_pipeline(file_path: str, delimiter: str = ",") -> dict:
    """
    Streams a large edge list file from disk line-by-line, runs DSU,
    and returns a dictionary of string-based connected components.
    """
    dsu = DiskDSU()
    
    print(f"[*] Starting to stream edges from: {file_path}")
    
    # Open file using a generator so the actual edge list never floods RAM
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            cleaned_line = line.strip()
            
            # Ignore empty lines or comment headers
            if not cleaned_line or cleaned_line.startswith("#"): 
                continue
                
            try:
                node_u, node_v = cleaned_line.split(delimiter)
                # Strip spaces around elements if they exist
                dsu.union(node_u.strip(), node_v.strip())
            except ValueError:
                print(f"[Warning] Skipping malformed line {line_num}: '{cleaned_line}'")
                
    print("[*] DSU processing complete. Building final dictionary...")
    
    # Generate and return the final string: string[] dictionary
    return dsu.get_string_components_dict()


# --- Demo and Execution ---
if __name__ == "__main__":
    # 1. Setup a dummy text file on disk to simulate your dataset
    file_to_process = "net.txt.txt"

    # 2. Run the DSU pipeline on the file
    # Replace 'sample_file' with your actual path (e.g., 'D:/data/my_huge_edges.csv')
    result_dict = run_dsu_pipeline(file_to_process, delimiter=",")
    
    # 3. Output the final string data dictionary
    print("\n[+] Final Python Dictionary (String Values Only):")
    pprint.pprint(result_dict)
    
    # Cleanup dummy file
    if os.path.exists(file_to_process):
        os.remove(file_to_process)
