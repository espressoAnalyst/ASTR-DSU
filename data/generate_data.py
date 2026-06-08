import random
import csv

# --- Synthetic Data Pools ---
first_names = ["john", "alice", "bob", "emma", "michael", "sarah", "david", "lisa", "james", "mary"]
last_names = ["smith", "doe", "jones", "brown", "davis", "miller", "wilson", "moore", "taylor", "anderson"]
domains = ["gmail.com", "yahoo.com", "hotmail.com", "work.com", "school.edu"]

def generate_person_aliases():
    """Generates a cluster of 5 connected identifiers belonging to one fake person."""
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    num = random.randint(10, 999)
    
    email1 = f"{fn}.{ln}{num}@{random.choice(domains)}"
    email2 = f"{fn}{num}@{random.choice(domains)}"
    username = f"{fn}_{ln}_{num}"
    phone = f"555-{random.randint(1000, 9999)}"
    device_id = f"DEV-{random.randint(10000, 99999)}"
    
    return [email1, email2, username, phone, device_id]

def main():
    edges = []
    target_rows = 500
    
    print(f"Generating {target_rows} rows of synthetic data...")
    
    while len(edges) < target_rows:
        # Get a group of aliases for one person
        aliases = generate_person_aliases()
        
        # Randomly decide how many of these aliases this person actually used (2 to 5)
        num_aliases_used = random.randint(2, 5)
        active_aliases = random.sample(aliases, num_aliases_used)
        
        # Create edges (connections) between their used aliases
        for i in range(len(active_aliases) - 1):
            if len(edges) < target_rows:
                edges.append([active_aliases[i], active_aliases[i+1]])

    # Shuffle the edges so the data isn't perfectly grouped (simulating messy real-world data)
    random.shuffle(edges)
    
    # Write to CSV
    filename = "mock_database.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(edges)
        
    print(f"Success! Created '{filename}' with {len(edges)} rows.")

if __name__ == "__main__":
    main()