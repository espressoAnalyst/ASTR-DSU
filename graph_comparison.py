import networkx as nx
import numpy as np

def build_directed_graph(adjacency_list):
    """
    Converts an adjacency list into a NetworkX directed graph.
    The list index represents the parent node.
    The list contents represent the directed edges to child nodes.
    """
    G = nx.DiGraph()
    
    for parent_node, children in enumerate(adjacency_list):
        # Ensure the parent node is added (important for singletons with empty lists)
        G.add_node(parent_node)
        
        for child in children:
            G.add_edge(parent_node, child)
            
    return G

def extract_cluster_metrics(G):
    """
    Calculates total clusters, mean height, max height, singletons, and returns node sets.
    """
    clusters = list(nx.weakly_connected_components(G))
    
    heights = []
    singletons = 0
    
    for cluster_nodes in clusters:
        if len(cluster_nodes) == 1:
            singletons += 1
            heights.append(0) 
        else:
            subgraph = G.subgraph(cluster_nodes)
            heights.append(nx.dag_longest_path_length(subgraph))
            
    return {
        "node_sets": clusters,
        "total_clusters": len(clusters),
        "mean_height": np.mean(heights) if heights else 0.0,
        "max_height": np.max(heights) if heights else 0,
        "singletons": singletons
    }

def evaluate_clusters(gt_clusters, pred_clusters):
    """
    Calculates recall and false positives for each ground truth cluster.
    """
    results = []
    
    for gt_set in gt_clusters:
        best_intersection = 0
        best_pred_set = set()
        
        for pred_set in pred_clusters:
            overlap = len(gt_set.intersection(pred_set))
            if overlap > best_intersection:
                best_intersection = overlap
                best_pred_set = pred_set
                
        recall = best_intersection / len(gt_set) if len(gt_set) > 0 else 0.0
        
        if best_intersection > 0:
            false_positives = len(best_pred_set - gt_set)
        else:
            false_positives = 0 
            
        results.append({
            "gt_nodes": gt_set,
            "is_singleton": len(gt_set) == 1,
            "recall": recall,
            "matched_pred_nodes": best_pred_set,
            "false_positives": false_positives
        })
        
    return results

# ==========================================
# Execution & Example Usage
# ==========================================

if __name__ == "__main__":
    # 1. Define your inputs in Adjacency List format
    # Index = Parent, Values = Children
    # Note: Use empty lists [] for nodes that have no children to ensure they 
    # are added to the graph, especially if they are singletons.
    
    array_gt = [
        [1, 2, 3],  # Node 0 -> edges to 1, 2, 3
        [4],        # Node 1 -> edge to 4
        [],         # Node 2 (leaf)
        [],         # Node 3 (leaf)
        [],         # Node 4 (leaf)
        [6],        # Node 5 -> edge to 6
        [],         # Node 6 (leaf)
        []          # Node 7 (singleton - no parents, no children)
    ]
    
    array_pred = [
        [1, 2],     # Node 0 missed node 3
        [4],        # Node 1 
        [],         # Node 2 
        [5],        # Node 3 incorrectly made parent of 5
        [],         # Node 4
        [6],        # Node 5
        [],         # Node 6
        [8],        # Node 7 incorrectly given child 8
        []          # Node 8 (leaf)
    ]
    
    # 2. Build the graphs
    graph_gt = build_directed_graph(array_gt)
    graph_pred = build_directed_graph(array_pred)
    
    # 3. Extract basic metrics
    metrics_gt = extract_cluster_metrics(graph_gt)
    metrics_pred = extract_cluster_metrics(graph_pred)
    
    # --- Print Basic Metrics ---
    print("=== Basic Graph Metrics ===")
    print("--- Ground Truth Graph ---")
    print(f"Total Clusters: {metrics_gt['total_clusters']}")
    print(f"Mean Height:    {metrics_gt['mean_height']:.2f}")
    print(f"Max Height:     {metrics_gt['max_height']}") 
    print(f"Singletons:     {metrics_gt['singletons']}\n")
    
    print("--- Predicted Graph ---")
    print(f"Total Clusters: {metrics_pred['total_clusters']}")
    print(f"Mean Height:    {metrics_pred['mean_height']:.2f}")
    print(f"Max Height:     {metrics_pred['max_height']}") 
    print(f"Singletons:     {metrics_pred['singletons']}\n")
    
    # 4. Advanced Evaluation
    print("=== Advanced Cluster Analysis ===")
    evaluation_results = evaluate_clusters(metrics_gt['node_sets'], metrics_pred['node_sets'])
    
    non_singleton_recalls = []
    
    for idx, res in enumerate(evaluation_results):
        gt_nodes = res['gt_nodes']
        
        print(f"\nGT Cluster {idx + 1} (Nodes {gt_nodes}):")
        print(f"  - Recall: {res['recall']:.2%}")
        
        if res['matched_pred_nodes']:
            print(f"  - Matched Pred Cluster: {res['matched_pred_nodes']}")
            print(f"  - False Positives: {res['false_positives']} node(s)")
        else:
            print("  - Matched Pred Cluster: None (Completely missed)")
            print("  - False Positives: N/A")
            
        if not res['is_singleton']:
            non_singleton_recalls.append(res['recall'])
    
    # 5. Final Mean Recall (Excluding Singletons)
    if non_singleton_recalls:
        mean_recall_no_singletons = np.mean(non_singleton_recalls)
        print(f"\n=> Mean System Recall (Excluding Singletons): {mean_recall_no_singletons:.2%}")
    else:
        print("\n=> Mean System Recall (Excluding Singletons): N/A (No complex clusters found)")