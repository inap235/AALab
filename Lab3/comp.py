import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque
import os

# Create a directory for saving visualizations
os.makedirs("algorithm_comparison", exist_ok=True)


# Implementations of DFS and BFS
def dfs(graph, start, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, path)

    return path


def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    path = [start]

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path.append(neighbor)

    return path


# Function to measure algorithm performance
def measure_performance(graph, start_node, algorithm):
    start_time = time.time()
    if algorithm == "DFS":
        path = dfs(graph, start_node)
    else:  # BFS
        path = bfs(graph, start_node)
    end_time = time.time()

    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    memory_usage = len(
        path
    )  # Simple proxy for memory usage - size of the resulting path

    return {
        "execution_time": execution_time,
        "memory_usage": memory_usage,
        "path_length": len(path),
        "path": path,
    }


# Function to visualize the final path of both algorithms
def visualize_final_paths(G, graph_adj_list, start_node, graph_type):
    # Get DFS and BFS paths
    dfs_path = dfs(graph_adj_list, start_node)
    bfs_path = bfs(graph_adj_list, start_node)

    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Get node positions (consistent for both visualizations)
    if graph_type == "grid":
        pos = {node: node for node in G.nodes()}
    else:
        pos = nx.spring_layout(G, seed=42)

    # Draw DFS path
    nx.draw_networkx_edges(G, pos, ax=ax1, alpha=0.3)

    # Color nodes according to their order in DFS path
    node_colors = ["lightgray"] * len(G.nodes())
    for i, node in enumerate(dfs_path):
        node_colors[node] = plt.cm.viridis(i / len(dfs_path))

    nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=node_colors, node_size=500)
    nx.draw_networkx_labels(G, pos, ax=ax1)

    # Draw the DFS path as a sequence of edges with increasing line width
    for i in range(len(dfs_path) - 1):
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax1,
            edgelist=[(dfs_path[i], dfs_path[i + 1])],
            width=2,
            edge_color=plt.cm.viridis(i / len(dfs_path)),
            arrows=True,
        )

    ax1.set_title(
        f"DFS Path on {graph_type.title()} Graph\nPath length: {len(dfs_path)}"
    )
    ax1.axis("off")

    # Draw BFS path
    nx.draw_networkx_edges(G, pos, ax=ax2, alpha=0.3)

    # Color nodes according to their order in BFS path
    node_colors = ["lightgray"] * len(G.nodes())
    for i, node in enumerate(bfs_path):
        node_colors[node] = plt.cm.plasma(i / len(bfs_path))

    nx.draw_networkx_nodes(G, pos, ax=ax2, node_color=node_colors, node_size=500)
    nx.draw_networkx_labels(G, pos, ax=ax2)

    # Draw the BFS path as a sequence of edges with increasing line width
    for i in range(len(bfs_path) - 1):
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax2,
            edgelist=[(bfs_path[i], bfs_path[i + 1])],
            width=2,
            edge_color=plt.cm.plasma(i / len(bfs_path)),
            arrows=True,
        )

    ax2.set_title(
        f"BFS Path on {graph_type.title()} Graph\nPath length: {len(bfs_path)}"
    )
    ax2.axis("off")

    plt.tight_layout()
    plt.savefig(f"algorithm_comparison/{graph_type}_final_paths.png", dpi=300)
    plt.close()

    return dfs_path, bfs_path


# Function to compare algorithms for various node sizes with line graphs
def compare_algorithms_with_line_graphs(
    graph_types, sizes=[10, 20, 50, 100, 200], directed=False
):
    all_results = {}

    for graph_type in graph_types:
        results = {
            "DFS": {"execution_time": [], "memory_usage": [], "path_length": []},
            "BFS": {"execution_time": [], "memory_usage": [], "path_length": []},
        }

        for size in sizes:
            # Generate graph based on type and size
            if graph_type == "path":
                G = nx.path_graph(size)
            elif graph_type == "cycle":
                G = nx.cycle_graph(size)
            elif graph_type == "complete":
                G = nx.complete_graph(size)
            elif graph_type == "star":
                G = nx.star_graph(size - 1)
            elif graph_type == "binary_tree":
                depth = int(np.log2(size + 1))
                G = nx.balanced_tree(2, depth)
            elif graph_type == "grid":
                grid_size = int(np.sqrt(size))
                G = nx.grid_2d_graph(grid_size, grid_size)
            elif graph_type == "sparse":
                G = nx.gnp_random_graph(size, 0.2, seed=42)
                # Ensure graph is connected
                while not nx.is_connected(G):
                    G = nx.gnp_random_graph(size, 0.2, seed=np.random.randint(1000))
            else:  # Dense
                G = nx.gnp_random_graph(size, 0.7, seed=42)

            # Ensure we have a valid start node
            start_node = list(G.nodes())[0]

            # Convert NetworkX graph to adjacency list representation
            graph_adj_list = {node: list(G.neighbors(node)) for node in G.nodes()}

            # Run DFS and measure performance
            dfs_result = measure_performance(graph_adj_list, start_node, "DFS")
            results["DFS"]["execution_time"].append(dfs_result["execution_time"])
            results["DFS"]["memory_usage"].append(dfs_result["memory_usage"])
            results["DFS"]["path_length"].append(dfs_result["path_length"])

            # Run BFS and measure performance
            bfs_result = measure_performance(graph_adj_list, start_node, "BFS")
            results["BFS"]["execution_time"].append(bfs_result["execution_time"])
            results["BFS"]["memory_usage"].append(bfs_result["memory_usage"])
            results["BFS"]["path_length"].append(bfs_result["path_length"])

            # Visualize final paths for a medium-sized graph
            if size == 20:
                visualize_final_paths(G, graph_adj_list, start_node, graph_type)

        all_results[graph_type] = results

    # Create line graphs comparing performance metrics across sizes
    fig, axes = plt.subplots(3, len(graph_types), figsize=(5 * len(graph_types), 15))

    metrics = ["execution_time", "memory_usage", "path_length"]
    metric_titles = ["Execution Time (ms)", "Memory Usage (nodes)", "Path Length"]

    for i, graph_type in enumerate(graph_types):
        for j, (metric, title) in enumerate(zip(metrics, metric_titles)):
            ax = axes[j, i]

            # Plot DFS and BFS results
            ax.plot(sizes, all_results[graph_type]["DFS"][metric], "bo-", label="DFS")
            ax.plot(sizes, all_results[graph_type]["BFS"][metric], "ro-", label="BFS")

            ax.set_title(f"{title}\n{graph_type.title()} Graph")
            ax.set_xlabel("Number of Nodes")
            ax.set_ylabel(title)
            ax.grid(True)

            # Add a legend to the first plot in each row
            if i == 0:
                ax.legend()

    plt.tight_layout()
    plt.savefig(f"algorithm_comparison/performance_line_graphs.png", dpi=300)
    plt.close()

    return all_results


# Run the analysis on selected graph types
selected_graph_types = ["path", "cycle", "binary_tree", "grid", "sparse", "complete"]
results = compare_algorithms_with_line_graphs(selected_graph_types)

print(
    "Analysis complete! All visualizations saved in the 'algorithm_comparison' directory."
)