

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import time
import numpy as np
import argparse
from collections import deque
from collections import defaultdict
import os
import sys
import matplotlib
from matplotlib.lines import Line2D

matplotlib.use("Agg")

DFS_COLOR   = "#d62728"   # red
BFS_COLOR   = "#1f77b4"   # blue
DFS_MARKER  = "o"
BFS_MARKER  = "s"
LINEWIDTH   = 2.0
GRID_ALPHA  = 0.35

plt.rcParams.update({
    "font.family":      "serif",
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.labelsize":   11,
    "legend.fontsize":  9,
    "xtick.labelsize":  9,
    "ytick.labelsize":  9,
    "figure.facecolor": "white",
    "axes.facecolor":   "#fafafa",
    "axes.edgecolor":   "#cccccc",
    "grid.color":       "#e0e0e0",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.6,
})

os.makedirs("graph_visualizations", exist_ok=True)
sys.setrecursionlimit(50_000)

# Output/performance controls
CREATE_GIFS = True
SNAPSHOT_DPI = 120
CHART_DPI = 120


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run DFS/BFS benchmark suite and generate graph visualizations."
    )
    parser.add_argument(
        "--with-gifs",
        action="store_true",
        help="Generate animated GIF traversals (disabled by default to save time).",
    )
    return parser.parse_args()

# ── DFS / BFS implementations ───────────────────────────────────────────────

def dfs(graph, start, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(start)
    path.append(start)
    for nb in graph[start]:
        if nb not in visited:
            dfs(graph, nb, visited, path)
    return path


def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    path = [start]
    while queue:
        v = queue.popleft()
        for nb in graph[v]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                path.append(nb)
    return path


# ── Step-recording variants (for animated GIFs) ─────────────────────────────

def dfs_steps(graph, start, visited=None, path=None, steps=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if steps is None:
        steps = []
    visited.add(start)
    path.append(start)
    steps.append({
        "visited": visited.copy(),
        "path": path.copy(),
        "current": start,
        "frontier": [n for n in graph[start] if n not in visited],
    })
    for nb in graph[start]:
        if nb not in visited:
            dfs_steps(graph, nb, visited, path, steps)
    return path, steps


def bfs_steps(graph, start):
    visited = {start}
    queue = deque([start])
    path = [start]
    steps = [{
        "visited": visited.copy(),
        "path": path.copy(),
        "current": start,
        "queue": list(queue),
        "frontier": list(graph[start]),
    }]
    while queue:
        current = queue.popleft()
        frontier = []
        for nb in graph[current]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                path.append(nb)
                frontier.append(nb)
        if frontier:
            steps.append({
                "visited": visited.copy(),
                "path": path.copy(),
                "current": current,
                "queue": list(queue),
                "frontier": frontier,
            })
    return path, steps


# ── Animated GIF visualisation ───────────────────────────────────────────────

NODE_COLORS = {
    "current":   "#d62728",
    "frontier":  "#ff7f0e",
    "visited":   "#2ca02c",
    "unvisited": "#d9d9d9",
}

def _get_pos(G, graph_type):
    if graph_type == "grid":
        return {node: node for node in G.nodes()}
    return nx.spring_layout(G, seed=42)


def _draw_graph_edges(G, pos, ax, directed=False):
    """Draw edges and make parallel edges/self-loops visible on Multi(Graph/DiGraph)."""
    if isinstance(G, (nx.MultiGraph, nx.MultiDiGraph)):
        edges = list(G.edges(keys=True))
        multiplicity = defaultdict(int)
        for u, v, _ in edges:
            key = (u, v) if directed else tuple(sorted((u, v)))
            multiplicity[key] += 1

        used = defaultdict(int)
        for u, v, _ in edges:
            key = (u, v) if directed else tuple(sorted((u, v)))
            idx = used[key]
            used[key] += 1
            total = multiplicity[key]

            # --- Explicit Self-Loop Handling ---
            if u == v:
                node_x, node_y = pos[u]
                # Shift loop center slightly for visibility
                angle = 1.5 + (idx * 0.8)  # varied angle for multiple loops
                dist = 0.15
                cx = node_x + np.cos(angle) * dist
                cy = node_y + np.sin(angle) * dist
                radius = 0.08
                
                # Draw loop as a Circle patch
                circle = mpatches.Circle((cx, cy), radius, color="#888888", 
                                         fill=False, alpha=0.6, linewidth=1.5)
                ax.add_patch(circle)
                # Omit arrow for loops to keep it simple/clean
                continue

            # --- Parallel Edge Handling ---
            if total == 1:
                rad = 0.0
            else:
                # Symmetrical spread for parallel edges
                center = (total - 1) / 2
                rad = (idx - center) * 0.20  # increased spread

            # Force patch-based drawing for curvature support (arrows=True)
            # Use arrowstyle='-' for undirected to hide the arrowhead but keep curve
            style = "-|>" if directed else "-"
            
            nx.draw_networkx_edges(
                G,
                pos,
                ax=ax,
                edgelist=[(u, v)],
                arrows=True,
                arrowstyle=style,
                alpha=0.6,
                width=1.8,
                edge_color="#888888",
                connectionstyle=f"arc3,rad={rad}",
            )
        return

    nx.draw_networkx_edges(G, pos, ax=ax, arrows=directed, alpha=0.25,
                           edge_color="#888888")


def create_animated_visualization(G, steps, algorithm, graph_type, directed=False):
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = _get_pos(G, graph_type)

    def update(frame_idx):
        ax.clear()
        step = steps[frame_idx]
        visited = step["visited"]
        current = step["current"]
        frontier = step.get("frontier", [])

        _draw_graph_edges(G, pos, ax, directed)

        all_nodes = list(G.nodes())
        colors, sizes = [], []
        for node in all_nodes:
            if node == current:
                colors.append(NODE_COLORS["current"]); sizes.append(700)
            elif node in frontier:
                colors.append(NODE_COLORS["frontier"]); sizes.append(500)
            elif node in visited:
                colors.append(NODE_COLORS["visited"]); sizes.append(500)
            else:
                colors.append(NODE_COLORS["unvisited"]); sizes.append(500)

        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=all_nodes,
                               node_color=colors, node_size=sizes,
                               edgecolors="white", linewidths=1.2)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight="bold")

        queue_str = f"Queue: {step.get('queue', [])}" if algorithm == "BFS" else ""

        legend_elements = [
            Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=NODE_COLORS["current"], markersize=14,
                   label="Current"),
            Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=NODE_COLORS["frontier"], markersize=14,
                   label="Frontier"),
            Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=NODE_COLORS["visited"], markersize=14,
                   label="Visited"),
            Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=NODE_COLORS["unvisited"], markersize=14,
                   label="Unvisited"),
        ]
        ax.legend(handles=legend_elements, loc="upper right", fontsize=9,
                  framealpha=0.9)
        ax.set_title(
            f"{algorithm} on {graph_type.replace('_',' ').title()} Graph "
            f"— Step {frame_idx+1}/{len(steps)}\n{queue_str}",
            fontsize=13, fontweight="bold",
        )
        ax.axis("off")

    ani = animation.FuncAnimation(fig, update, frames=len(steps),
                                  interval=3000, repeat=True)
    plt.tight_layout()
    ani.save(
        f"graph_visualizations/{algorithm}_{graph_type}_animated.gif",
        writer="pillow", fps=1/3,
    )
    plt.close(fig)


def create_snapshot(G, steps, algorithm, graph_type, directed=False):
    """Save a single PNG of the final traversal state (for the report)."""
    fig, ax = plt.subplots(figsize=(7, 5.5))
    pos = _get_pos(G, graph_type)
    step = steps[-1]
    visited = step["visited"]
    current = step["current"]

    _draw_graph_edges(G, pos, ax, directed)

    all_nodes = list(G.nodes())
    colors = []
    for node in all_nodes:
        if node == current:
            colors.append(NODE_COLORS["current"])
        elif node in visited:
            colors.append(NODE_COLORS["visited"])
        else:
            colors.append(NODE_COLORS["unvisited"])

    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=all_nodes,
                           node_color=colors, node_size=450,
                           edgecolors="white", linewidths=1.2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_weight="bold")

    legend_elements = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=NODE_COLORS["current"], markersize=14,
               label="Last visited"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=NODE_COLORS["visited"], markersize=14,
               label="Visited"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=NODE_COLORS["unvisited"], markersize=14,
               label="Unvisited"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=9,
              framealpha=0.9)
    ax.set_title(
        f"{algorithm} — {graph_type.replace('_',' ').title()} Graph "
        f"(final state, {len(step['visited'])} nodes visited)",
        fontsize=13, fontweight="bold",
    )
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(
        f"graph_visualizations/{algorithm}_{graph_type}_snapshot.png", dpi=SNAPSHOT_DPI
    )
    plt.close(fig)


def create_combined_snapshot(G, dfs_st, bfs_st, graph_type, directed=False):
    """Side-by-side DFS + BFS snapshot in a single PNG (fewer images for LaTeX)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
    pos = _get_pos(G, graph_type)

    for ax, steps, label in [(ax1, dfs_st, "DFS"), (ax2, bfs_st, "BFS")]:
        step = steps[-1]
        visited = step["visited"]
        current = step["current"]

        _draw_graph_edges(G, pos, ax, directed)
        all_nodes = list(G.nodes())
        colors = []
        for node in all_nodes:
            if node == current:
                colors.append(NODE_COLORS["current"])
            elif node in visited:
                colors.append(NODE_COLORS["visited"])
            else:
                colors.append(NODE_COLORS["unvisited"])
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=all_nodes,
                               node_color=colors, node_size=400,
                               edgecolors="white", linewidths=1.0)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight="bold")
        ax.set_title(f"{label} traversal", fontsize=12, fontweight="bold")
        ax.axis("off")

    legend_elements = [
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=NODE_COLORS["current"], markersize=12,
               label="Last visited"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=NODE_COLORS["visited"], markersize=12,
               label="Visited"),
        Line2D([0], [0], marker="o", color="w",
               markerfacecolor=NODE_COLORS["unvisited"], markersize=12,
               label="Unvisited"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=3,
               fontsize=9, framealpha=0.9)
    fig.suptitle(
        f"{graph_type.replace('_',' ').title()} Graph ($n=15$)",
        fontsize=13, fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.94])
    fig.savefig(
        f"graph_visualizations/combined_{graph_type}_snapshot.png", dpi=SNAPSHOT_DPI
    )
    plt.close(fig)


# ── Performance measurement ──────────────────────────────────────────────────

REPEATS = 3

def measure_performance(graph, start_node, algorithm):
    times = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        if algorithm == "DFS":
            path = dfs(graph, start_node)
        else:
            path = bfs(graph, start_node)
        times.append((time.perf_counter() - t0) * 1000)
    avg_time = sum(times) / len(times)
    return {
        "execution_time": avg_time,
        "memory_usage":   len(path),
        "path_length":    len(path),
    }


# ── Graph generators ────────────────────────────────────────────────────────

def make_graph(graph_type, size):
    """Return traversal graph, directed flag, and visualization graph."""
    directed = False
    G_vis = None
    if graph_type == "path":
        G = nx.path_graph(size)
    elif graph_type == "cycle":
        G = nx.cycle_graph(size)
    elif graph_type == "complete":
        G = nx.complete_graph(size)
    elif graph_type == "star":
        G = nx.star_graph(size - 1)
    elif graph_type == "bipartite":
        half = size // 2
        G = nx.complete_bipartite_graph(half, size - half)
    elif graph_type == "binary_tree":
        depth = max(1, int(np.log2(max(size, 2))))
        G = nx.balanced_tree(2, depth)
    elif graph_type == "forest":
        depth = max(1, int(np.log2(max(size // 2, 2))))
        G1 = nx.balanced_tree(2, depth)
        G2 = nx.balanced_tree(2, depth)
        G = nx.disjoint_union(G1, G2)
        G.add_edge(0, len(G1))
    elif graph_type == "dag":
        directed = True
        G = nx.DiGraph()
        for i in range(size - 1):
            G.add_edge(i, i + 1)
            if i < size - 2:
                G.add_edge(i, i + 2)
    elif graph_type == "directed_cycle":
        directed = True
        G = nx.DiGraph()
        for i in range(size - 1):
            G.add_edge(i, i + 1)
        G.add_edge(size - 1, 0)
        for i in range(0, size - 2, 2):
            G.add_edge(i, i + 2)
    elif graph_type == "grid":
        side = max(1, int(np.sqrt(size)))
        G = nx.grid_2d_graph(side, side)
    elif graph_type == "sparse":
        G = nx.gnp_random_graph(size, 0.2, seed=42)
        while not nx.is_connected(G):
            G = nx.gnp_random_graph(size, 0.2, seed=np.random.randint(1000))
    elif graph_type == "dense":
        G = nx.gnp_random_graph(size, 0.7, seed=42)
    elif graph_type == "simple":
        # Simple graph: connected, no multi-edges, no self-loops (sparse Erdos-Renyi)
        G = nx.gnp_random_graph(size, 0.15, seed=7)
        while not nx.is_connected(G):
            G = nx.gnp_random_graph(size, 0.15, seed=np.random.randint(1000))
    elif graph_type == "multigraph":
        # Multigraph: path backbone + duplicate edges; converted to simple for traversal
        MG = nx.MultiGraph()
        MG.add_nodes_from(range(size))
        for i in range(size - 1):
            MG.add_edge(i, i + 1)
            MG.add_edge(i, i + 1)          # duplicate edge
        if size > 2:
            for i in range(0, size - 2, 3):
                MG.add_edge(i, i + 2)      # extra skip edge
        G = nx.Graph(MG)                   # collapse to simple graph for DFS/BFS
        G_vis = MG                         # keep multi-edges visible in figures
    elif graph_type == "pseudograph":
        # Pseudograph: self-loops + multi-edges; collapsed to simple for traversal
        PG = nx.MultiGraph()
        PG.add_nodes_from(range(size))
        for i in range(size - 1):
            PG.add_edge(i, i + 1)
            PG.add_edge(i, i + 1)          # parallel edge
        for i in range(0, size, 4):
            PG.add_edge(i, i)              # self-loop
        G = nx.Graph(PG)
        G.remove_edges_from(nx.selfloop_edges(G))
        G_vis = PG                         # keep loops + multi-edges visible in figures
    elif graph_type == "directed_multigraph":
        directed = True
        DMG = nx.MultiDiGraph()
        DMG.add_nodes_from(range(size))
        for i in range(size - 1):
            DMG.add_edge(i, i + 1)
            DMG.add_edge(i, i + 1)         # parallel directed edge
        if size > 2:
            for i in range(0, size - 2, 3):
                DMG.add_edge(i, i + 2)
        G = nx.DiGraph(DMG)                # collapse to simple digraph for traversal
        G_vis = DMG                        # keep parallel arcs visible in figures
    elif graph_type == "wheel":
        # Wheel graph: hub connected to all nodes in a cycle of (size-1) nodes
        G = nx.wheel_graph(size)
    elif graph_type == "regular":
        # 3-regular (cubic) graph; use size even and size >= 4
        k = 3
        n = size if (size % 2 == 0 and size >= 4) else (size + 1 if size >= 4 else 4)
        G = nx.random_regular_graph(k, n, seed=42)
    elif graph_type == "weighted":
        # Weighted graph: sparse random graph with integer weights on edges
        # For traversal purposes weights are ignored; stored as edge attribute
        G = nx.gnp_random_graph(size, 0.15, seed=13)
        while not nx.is_connected(G):
            G = nx.gnp_random_graph(size, 0.15, seed=np.random.randint(1000))
        rng = np.random.default_rng(42)
        for u, v in G.edges():
            G[u][v]["weight"] = int(rng.integers(1, 20))
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")
    if G_vis is None:
        G_vis = G
    return G, directed, G_vis


def to_adj_list(G):
    return {node: list(G.neighbors(node)) for node in G.nodes()}


# ── Per-type scaled comparison ───────────────────────────────────────────────

def compare_algorithms_scaled(graph_type, sizes):
    results = {
        "DFS": {"execution_time": [], "memory_usage": [], "path_length": []},
        "BFS": {"execution_time": [], "memory_usage": [], "path_length": []},
    }

    # Generate GIF + snapshot on a small graph (15 nodes) for illustration
    small_n = 15
    G_small, directed, G_small_vis = make_graph(graph_type, small_n)
    adj_small = to_adj_list(G_small)
    start_small = list(G_small.nodes())[0]

    _, d_steps = dfs_steps(adj_small, start_small)
    _, b_steps = bfs_steps(adj_small, start_small)

    if CREATE_GIFS:
        create_animated_visualization(G_small_vis, d_steps, "DFS", graph_type, directed)
        create_animated_visualization(G_small_vis, b_steps, "BFS", graph_type, directed)
    create_snapshot(G_small_vis, d_steps, "DFS", graph_type, directed)
    create_snapshot(G_small_vis, b_steps, "BFS", graph_type, directed)
    create_combined_snapshot(G_small_vis, d_steps, b_steps, graph_type, directed)

    for size in sizes:
        G, _, _ = make_graph(graph_type, size)
        start_node = list(G.nodes())[0]
        adj = to_adj_list(G)

        for algo in ("DFS", "BFS"):
            r = measure_performance(adj, start_node, algo)
            results[algo]["execution_time"].append(r["execution_time"])
            results[algo]["memory_usage"].append(r["memory_usage"])
            results[algo]["path_length"].append(r["path_length"])

    # ── Line chart (3 metrics) ───────────────────────────────────────────────
    fig, axs = plt.subplots(3, 1, figsize=(10, 14))
    metrics = ["execution_time", "memory_usage", "path_length"]
    ylabels = ["Execution Time (ms)", "Memory Usage (nodes visited)", "Path Length"]

    for i, (metric, ylabel) in enumerate(zip(metrics, ylabels)):
        axs[i].plot(sizes, results["DFS"][metric],
                    color=DFS_COLOR, marker=DFS_MARKER, linewidth=LINEWIDTH,
                    label="DFS", markeredgecolor="white", markersize=7)
        axs[i].plot(sizes, results["BFS"][metric],
                    color=BFS_COLOR, marker=BFS_MARKER, linewidth=LINEWIDTH,
                    label="BFS", markeredgecolor="white", markersize=7)
        axs[i].set_title(f"{ylabel}  —  {graph_type.replace('_',' ').title()} Graph",
                         fontweight="bold")
        axs[i].set_xlabel("Number of Nodes  $n$")
        axs[i].set_ylabel(ylabel)
        axs[i].legend(framealpha=0.9)
        axs[i].grid(True, alpha=GRID_ALPHA)

    fig.tight_layout(pad=2.0)
    fig.savefig(f"graph_visualizations/comparison_{graph_type}_scaled.png", dpi=CHART_DPI)
    plt.close(fig)

    # ── Bar chart at each size ───────────────────────────────────────────────
    n_sizes = len(sizes)
    fig, axs = plt.subplots(1, n_sizes, figsize=(5 * n_sizes, 7))
    if n_sizes == 1:
        axs = [axs]

    for i, size in enumerate(sizes):
        x = np.arange(len(metrics))
        w = 0.35
        dfs_vals = [results["DFS"][m][i] for m in metrics]
        bfs_vals = [results["BFS"][m][i] for m in metrics]

        bars_d = axs[i].bar(x - w / 2, dfs_vals, w, label="DFS",
                            color=DFS_COLOR, alpha=0.85, edgecolor="white")
        bars_b = axs[i].bar(x + w / 2, bfs_vals, w, label="BFS",
                            color=BFS_COLOR, alpha=0.85, edgecolor="white")

        axs[i].set_title(f"$n = {size}$", fontweight="bold")
        axs[i].set_xticks(x)
        axs[i].set_xticklabels(["Time (ms)", "Memory", "Path Len"], rotation=30)
        axs[i].legend(fontsize=8, framealpha=0.9)
        axs[i].grid(True, axis="y", alpha=GRID_ALPHA)

        axs[i].bar_label(bars_d, fmt="%.2f", padding=3, fontsize=7)
        axs[i].bar_label(bars_b, fmt="%.2f", padding=3, fontsize=7)

    fig.suptitle(
        f"DFS vs BFS  —  {graph_type.replace('_',' ').title()} Graph",
        fontsize=15, fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(f"graph_visualizations/bar_comparison_{graph_type}_scaled.png", dpi=CHART_DPI)
    plt.close(fig)

    return results


# ── Run all graph types ──────────────────────────────────────────────────────

GRAPH_TYPES = [
    "path", "cycle", "complete", "star", "bipartite", "binary_tree",
    "forest", "dag", "directed_cycle", "grid", "sparse", "dense",
    "simple", "multigraph", "pseudograph", "directed_multigraph",
    "wheel", "regular", "weighted",
]

HEAVY_TYPES = {"complete", "bipartite", "dense"}  # O(n^2) edges
STANDARD_SIZES = [100, 200, 300, 400]
HEAVY_SIZES    = [50, 100, 150, 200]


def generate_and_analyze_graphs():
    results = {}
    for gt in GRAPH_TYPES:
        sizes = HEAVY_SIZES if gt in HEAVY_TYPES else STANDARD_SIZES
        print(f"  {gt} …", flush=True)
        results[gt] = compare_algorithms_scaled(gt, sizes)
    return results


def validate_graph_implementations(sample_size=15):
    """Quick sanity check that every graph type supports both traversals."""
    errors = []
    for gt in GRAPH_TYPES:
        try:
            G, _, _ = make_graph(gt, sample_size)
            adj = to_adj_list(G)
            if not adj:
                raise ValueError("Empty adjacency list")
            start = next(iter(G.nodes()))
            dfs_path = dfs(adj, start)
            bfs_path = bfs(adj, start)
            if not dfs_path or not bfs_path:
                raise ValueError("Traversal produced an empty path")
        except Exception as exc:
            errors.append(f"{gt}: {exc}")

    if errors:
        msg = "\n".join(errors)
        raise RuntimeError(f"Graph implementation validation failed:\n{msg}")

    print(f"Validated DFS/BFS availability for {len(GRAPH_TYPES)} graph types.")


# ── Summary bar charts across all types ──────────────────────────────────────

def create_summary_visualization(results):
    graph_types = list(results.keys())
    pretty = [g.replace("_", " ").title() for g in graph_types]

    # --- Execution time at each size index ---
    for idx_label, size_idx in [(0, 0), (1, -1)]:
        fig, ax = plt.subplots(figsize=(14, 6))

        dfs_t = [results[g]["DFS"]["execution_time"][size_idx] for g in graph_types]
        bfs_t = [results[g]["BFS"]["execution_time"][size_idx] for g in graph_types]

        x = np.arange(len(graph_types))
        w = 0.35

        bars_d = ax.bar(x - w / 2, dfs_t, w, label="DFS",
                        color=DFS_COLOR, alpha=0.85, edgecolor="white")
        bars_b = ax.bar(x + w / 2, bfs_t, w, label="BFS",
                        color=BFS_COLOR, alpha=0.85, edgecolor="white")

        label = "smallest" if size_idx == 0 else "largest"
        ax.set_title(f"DFS vs BFS  —  Execution Time at {label} tested size",
                     fontsize=14, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(pretty, rotation=35, ha="right")
        ax.set_ylabel("Time (ms)")
        ax.legend(fontsize=10, framealpha=0.9)
        ax.grid(True, axis="y", alpha=GRID_ALPHA)
        ax.bar_label(bars_d, fmt="%.3f", padding=3, fontsize=7)
        ax.bar_label(bars_b, fmt="%.3f", padding=3, fontsize=7)

        fig.tight_layout()
        fig.savefig(
            f"graph_visualizations/overall_time_comparison_{label}.png", dpi=150
        )
        plt.close(fig)

    # --- Memory comparison at largest size ---
    fig, ax = plt.subplots(figsize=(14, 6))
    dfs_m = [results[g]["DFS"]["memory_usage"][-1] for g in graph_types]
    bfs_m = [results[g]["BFS"]["memory_usage"][-1] for g in graph_types]

    x = np.arange(len(graph_types))
    w = 0.35
    ax.bar(x - w / 2, dfs_m, w, label="DFS", color=DFS_COLOR, alpha=0.85,
           edgecolor="white")
    ax.bar(x + w / 2, bfs_m, w, label="BFS", color=BFS_COLOR, alpha=0.85,
           edgecolor="white")

    ax.set_title("DFS vs BFS  —  Nodes Visited at largest tested size",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(pretty, rotation=35, ha="right")
    ax.set_ylabel("Nodes visited")
    ax.legend(fontsize=10, framealpha=0.9)
    ax.grid(True, axis="y", alpha=GRID_ALPHA)
    fig.tight_layout()
    fig.savefig("graph_visualizations/overall_memory_comparison.png", dpi=150)
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = parse_args()
    CREATE_GIFS = args.with_gifs
    print("Running benchmarks …")
    validate_graph_implementations()
    results = generate_and_analyze_graphs()
    create_summary_visualization(results)
    print("Done – all figures saved in graph_visualizations/")