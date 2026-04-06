import csv
import heapq
import random
import time
from pathlib import Path
from io import BytesIO

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from PIL import Image


INF = float("inf")


class GraphAnalyzer:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def _build_nx_graph(self, graph):
        """Build a NetworkX graph from adjacency-matrix representation."""
        n = len(graph)
        G = nx.Graph()
        for i in range(n):
            G.add_node(i)
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i, j] != INF:
                    G.add_edge(i, j, weight=graph[i, j])
        return G

    def _dijkstra_states(self, graph, start_node):
        """Collect per-step states for Dijkstra visualization."""
        n = len(graph)
        distances = [INF] * n
        previous = [None] * n
        visited = [False] * n
        distances[start_node] = 0.0

        states = []
        pq = [(0.0, start_node)]
        while pq:
            current_dist, u = heapq.heappop(pq)
            if current_dist > distances[u] or visited[u]:
                continue

            visited[u] = True

            for v in range(n):
                w = graph[u, v]
                if w == INF or u == v or visited[v]:
                    continue

                new_dist = distances[u] + w
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous[v] = u
                    heapq.heappush(pq, (new_dist, v))

            states.append(
                {
                    "visited": visited.copy(),
                    "current": u,
                    "distances": distances.copy(),
                    "previous": previous.copy(),
                }
            )

        return states

    def _floyd_states(self, graph):
        """Collect event-driven states for Floyd-Warshall visualization."""
        n = len(graph)
        dist = np.array(graph, dtype=float, copy=True)
        next_node = np.full((n, n), -1, dtype=int)

        for i in range(n):
            for j in range(n):
                if i != j and dist[i, j] != INF:
                    next_node[i, j] = j

        states = [
            {
                "event": "init",
                "k": 0,
                "i": 0,
                "j": 0,
                "processed_k": [],
                "cross_path": [],
                "accepted_path": [],
                "old_dist": INF,
                "new_dist": INF,
                "dist": np.array(dist, copy=True),
                "next_node": np.array(next_node, copy=True),
            }
        ]

        for k in range(n):
            improved_in_k = 0
            for i in range(n):
                if i == k or dist[i, k] == INF:
                    continue
                for j in range(n):
                    if j == i or j == k or dist[k, j] == INF:
                        continue

                    candidate = dist[i, k] + dist[k, j]
                    if candidate < dist[i, j]:
                        old_dist = dist[i, j]

                        path_i_k = self.reconstruct_path_floyd(next_node, i, k)
                        path_k_j = self.reconstruct_path_floyd(next_node, k, j)
                        cross_path = []
                        if path_i_k and path_k_j:
                            cross_path = path_i_k + path_k_j[1:]

                        next_node[i, j] = next_node[i, k]
                        dist[i, j] = candidate

                        accepted_path = self.reconstruct_path_floyd(next_node, i, j)

                        states.append(
                            {
                                "event": "update",
                                "k": k,
                                "i": i,
                                "j": j,
                                "processed_k": list(range(k + 1)),
                                "cross_path": cross_path,
                                "accepted_path": accepted_path,
                                "old_dist": old_dist,
                                "new_dist": candidate,
                                "dist": np.array(dist, copy=True),
                                "next_node": np.array(next_node, copy=True),
                            }
                        )
                        improved_in_k += 1

            if improved_in_k == 0:
                states.append(
                    {
                        "event": "checkpoint",
                        "k": k,
                        "i": k,
                        "j": k,
                        "processed_k": list(range(k + 1)),
                        "cross_path": [],
                        "accepted_path": [],
                        "old_dist": INF,
                        "new_dist": INF,
                        "dist": np.array(dist, copy=True),
                        "next_node": np.array(next_node, copy=True),
                    }
                )

        return states

    def _draw_dijkstra_state(self, ax, G, pos, state, step, total_steps):
        """Render one Dijkstra state using impl.py styling."""
        visited = state["visited"]
        current = state["current"]
        distances = state["distances"]
        previous = state["previous"]

        for u, v, data in G.edges(data=True):
            ax.plot(
                [pos[u][0], pos[v][0]],
                [pos[u][1], pos[v][1]],
                "k-",
                alpha=0.3,
                linewidth=data["weight"] / 10,
            )

        for node in G.nodes():
            if node == current:
                color = "red"
            elif visited[node]:
                color = "green"
            else:
                color = "skyblue"

            ax.plot(pos[node][0], pos[node][1], "o", markersize=15, color=color)
            label = distances[node] if distances[node] != INF else "∞"
            if label != "∞":
                label = int(label)
            ax.annotate(
                f"{node}\\n({label})",
                xy=pos[node],
                ha="center",
                va="center",
                fontsize=9,
            )

        for node in range(len(visited)):
            if previous[node] is not None:
                ax.plot(
                    [pos[previous[node]][0], pos[node][0]],
                    [pos[previous[node]][1], pos[node][1]],
                    "b-",
                    alpha=0.5,
                    linewidth=2,
                )

        red_patch = mpatches.Patch(color="red", label="Current Node")
        green_patch = mpatches.Patch(color="green", label="Visited Nodes")
        blue_patch = mpatches.Patch(color="skyblue", label="Unvisited Nodes")
        blue_line = mpatches.Patch(color="blue", label="Current Shortest Paths", alpha=0.5)
        ax.legend(handles=[red_patch, green_patch, blue_patch, blue_line], loc="upper right", fontsize=9)

        ax.set_title(f"Dijkstra's Algorithm - Step {step}/{total_steps}")
        ax.axis("off")

    def _draw_floyd_state(self, ax, G, pos, state, step, total_steps, source_node, target_node):
        """Render one Floyd-Warshall state in a Dijkstra-like style."""
        k = state["k"]
        i = state["i"]
        j = state["j"]
        dist = state["dist"]
        next_node = state["next_node"]
        processed_k = state.get("processed_k", [])
        cross_path = state.get("cross_path", [])
        accepted_path = state.get("accepted_path", [])

        for u, v, data in G.edges(data=True):
            ax.plot(
                [pos[u][0], pos[v][0]],
                [pos[u][1], pos[v][1]],
                "k-",
                alpha=0.25,
                linewidth=max(data["weight"] / 12, 0.8),
            )

        # Highlight the path being tested through k (i -> k -> j).
        if len(cross_path) >= 2:
            for idx in range(len(cross_path) - 1):
                u, v = cross_path[idx], cross_path[idx + 1]
                ax.plot(
                    [pos[u][0], pos[v][0]],
                    [pos[u][1], pos[v][1]],
                    color="orange",
                    alpha=0.7,
                    linewidth=2.5,
                    linestyle="--",
                )

        # Draw accepted update path i -> j for this event.
        if len(accepted_path) >= 2:
            for idx in range(len(accepted_path) - 1):
                u, v = accepted_path[idx], accepted_path[idx + 1]
                ax.plot(
                    [pos[u][0], pos[v][0]],
                    [pos[u][1], pos[v][1]],
                    color="blue",
                    alpha=0.9,
                    linewidth=3,
                )

        # Keep a focused source->target path visible, similar to final path feel in Dijkstra.
        focused_path = self.reconstruct_path_floyd(next_node, source_node, target_node)
        if len(focused_path) >= 2:
            for idx in range(len(focused_path) - 1):
                u, v = focused_path[idx], focused_path[idx + 1]
                ax.plot(
                    [pos[u][0], pos[v][0]],
                    [pos[u][1], pos[v][1]],
                    color="purple",
                    alpha=0.8,
                    linewidth=2,
                )

        for node in G.nodes():
            if node == k:
                color = "red"
            elif node == i:
                color = "green"
            elif node == j:
                color = "gold"
            elif node in processed_k:
                color = "lightgreen"
            else:
                color = "skyblue"

            ax.plot(pos[node][0], pos[node][1], "o", markersize=15, color=color)
            source_dist = dist[source_node, node]
            label = "∞" if source_dist == INF else f"{source_dist:.0f}"
            ax.annotate(
                f"{node}\\n({label})",
                xy=pos[node],
                ha="center",
                va="center",
                fontsize=9,
            )

        red_patch = mpatches.Patch(color="red", label=f"Current k={k}")
        green_patch = mpatches.Patch(color="green", label=f"From i={i}")
        gold_patch = mpatches.Patch(color="gold", label=f"To j={j}")
        cyan_patch = mpatches.Patch(color="skyblue", label="Unprocessed Nodes")
        light_green_patch = mpatches.Patch(color="lightgreen", label="Processed k Nodes")
        cross_line = mpatches.Patch(color="orange", label="Path Tested via k")
        accept_line = mpatches.Patch(color="blue", label="Accepted Shorter Path")
        focus_line = mpatches.Patch(color="purple", label=f"Current {source_node}->{target_node} Path")

        ax.legend(
            handles=[
                red_patch,
                green_patch,
                gold_patch,
                cyan_patch,
                light_green_patch,
                cross_line,
                accept_line,
                focus_line,
            ],
            loc="upper right",
            fontsize=8,
        )

        global_label = "∞"
        if dist[source_node, target_node] != INF:
            global_label = f"{dist[source_node, target_node]:.0f}"

        event = state.get("event", "update")
        if event == "update":
            old_label = "∞" if state["old_dist"] == INF else f"{state['old_dist']:.0f}"
            new_label = "∞" if state["new_dist"] == INF else f"{state['new_dist']:.0f}"
            subtitle = f"update ({i}->{j}) via {k}: {old_label} -> {new_label}"
        elif event == "checkpoint":
            subtitle = f"no updates for k={k}"
        else:
            subtitle = "initial distances"

        ax.set_title(
            f"Floyd-Warshall - Step {step}/{total_steps} | "
            f"{subtitle} | {source_node}->{target_node}={global_label}"
        )
        ax.axis("off")

    def generate_graph(self, num_nodes, density, weight_range=(1, 20)):
        """Generate a connected undirected weighted graph as adjacency matrix."""
        graph = np.full((num_nodes, num_nodes), INF, dtype=float)
        np.fill_diagonal(graph, 0.0)

        # Build a random spanning tree first so the graph stays connected.
        for node in range(1, num_nodes):
            parent = self.rng.randint(0, node - 1)
            weight = self.rng.randint(weight_range[0], weight_range[1])
            graph[node, parent] = weight
            graph[parent, node] = weight

        # Add remaining edges based on requested density.
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if graph[i, j] != INF:
                    continue
                if self.rng.random() < density:
                    weight = self.rng.randint(weight_range[0], weight_range[1])
                    graph[i, j] = weight
                    graph[j, i] = weight

        return graph

    def dijkstra(self, graph, start_node):
        """Single-source shortest paths using Dijkstra with a min-heap."""
        n = len(graph)
        distances = [INF] * n
        previous = [None] * n
        distances[start_node] = 0.0

        pq = [(0.0, start_node)]
        while pq:
            current_dist, u = heapq.heappop(pq)
            if current_dist > distances[u]:
                continue

            for v in range(n):
                w = graph[u, v]
                if w == INF or u == v:
                    continue

                new_dist = current_dist + w
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous[v] = u
                    heapq.heappush(pq, (new_dist, v))

        return distances, previous

    def floyd_warshall(self, graph):
        """All-pairs shortest paths using vectorized Floyd-Warshall DP."""
        n = len(graph)
        dist = np.array(graph, dtype=float, copy=True)
        next_node = np.full((n, n), -1, dtype=int)

        for i in range(n):
            for j in range(n):
                if i != j and dist[i, j] != INF:
                    next_node[i, j] = j

        for k in range(n):
            candidate = dist[:, [k]] + dist[[k], :]
            improved = candidate < dist
            for i in range(n):
                improved_js = np.where(improved[i])[0]
                for j in improved_js:
                    next_node[i, j] = next_node[i, k]
            dist = np.minimum(dist, candidate)

        return dist, next_node

    def reconstruct_path_dijkstra(self, previous, start, end):
        if start == end:
            return [start]
        if previous[end] is None:
            return []

        path = [end]
        while path[0] != start:
            parent = previous[path[0]]
            if parent is None:
                return []
            path.insert(0, parent)
        return path

    def reconstruct_path_floyd(self, next_node, start, end):
        if start == end:
            return [start]
        if next_node[start, end] == -1:
            return []

        path = [start]
        while path[-1] != end:
            nxt = next_node[path[-1], end]
            if nxt == -1:
                return []
            path.append(int(nxt))
        return path

    def visualize_dijkstra_snapshot(self, graph, start_node, output_dir):
        """Create a Dijkstra snapshot matching GIF rendering style."""
        states = self._dijkstra_states(graph, start_node)
        if not states:
            return

        G = self._build_nx_graph(graph)
        pos = nx.spring_layout(G, seed=42)

        frame_idx = len(states) // 2
        fig, ax = plt.subplots(figsize=(10, 8))
        self._draw_dijkstra_state(ax, G, pos, states[frame_idx], frame_idx + 1, len(states))
        fig.tight_layout()
        fig.savefig(output_dir / "dijkstra_snapshot.png", dpi=200, bbox_inches="tight")
        plt.close(fig)

    def visualize_floyd_warshall_snapshot(self, graph, output_dir, source_node=0, target_node=None):
        """Create a Floyd-Warshall snapshot matching GIF rendering style."""
        states = self._floyd_states(graph)
        if not states:
            return

        if target_node is None:
            target_node = len(graph) - 1

        G = self._build_nx_graph(graph)
        pos = nx.spring_layout(G, seed=42)

        frame_idx = len(states) // 2
        fig, ax = plt.subplots(figsize=(10, 8))
        self._draw_floyd_state(
            ax,
            G,
            pos,
            states[frame_idx],
            frame_idx + 1,
            len(states),
            source_node,
            target_node,
        )
        fig.tight_layout()
        fig.savefig(output_dir / "floyd_warshall_snapshot.png", dpi=200, bbox_inches="tight")
        plt.close(fig)

    def _fig_to_pil(self, fig):
        """Convert matplotlib figure to PIL Image."""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=80, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        return img.convert('RGB')

    def generate_dijkstra_gif(self, graph, start_node, output_dir):
        """Generate Dijkstra GIF using the same rendering style as snapshots."""
        states = self._dijkstra_states(graph, start_node)
        if not states:
            return

        G = self._build_nx_graph(graph)
        pos = nx.spring_layout(G, seed=42)

        frames = []
        for idx, state in enumerate(states):
            fig, ax = plt.subplots(figsize=(10, 8))
            self._draw_dijkstra_state(ax, G, pos, state, idx + 1, len(states))
            fig.tight_layout()
            frames.append(self._fig_to_pil(fig))
            plt.close(fig)

        if frames:
            frames[0].save(
                output_dir / "dijkstra_animation.gif",
                save_all=True,
                append_images=frames[1:],
                duration=1000,
                loop=0
            )

    def generate_floyd_warshall_gif(self, graph, output_dir, source_node=0, target_node=None):
        """Generate Floyd-Warshall GIF using the same rendering style as snapshots."""
        states = self._floyd_states(graph)
        if not states:
            return

        if target_node is None:
            target_node = len(graph) - 1

        G = self._build_nx_graph(graph)
        pos = nx.spring_layout(G, seed=42)

        frames = []
        for idx, state in enumerate(states):
            fig, ax = plt.subplots(figsize=(10, 8))
            self._draw_floyd_state(
                ax,
                G,
                pos,
                state,
                idx + 1,
                len(states),
                source_node,
                target_node,
            )
            fig.tight_layout()
            frames.append(self._fig_to_pil(fig))
            plt.close(fig)

        if frames:
            frames[0].save(
                output_dir / "floyd_warshall_animation.gif",
                save_all=True,
                append_images=frames[1:],
                duration=1000,
                loop=0
            )

    def empirical_analysis(
        self,
        sizes,
        repetitions=5,
        sparse_density=0.1,
        dense_density=0.7,
    ):
        results = {
            "sizes": list(sizes),
            "dijkstra_sparse": [],
            "dijkstra_dense": [],
            "floyd_sparse": [],
            "floyd_dense": [],
        }

        for size in sizes:
            dij_sparse_sum = 0.0
            dij_dense_sum = 0.0
            fw_sparse_sum = 0.0
            fw_dense_sum = 0.0

            for _ in range(repetitions):
                sparse = self.generate_graph(size, sparse_density)
                dense = self.generate_graph(size, dense_density)

                start = time.perf_counter()
                self.dijkstra(sparse, 0)
                dij_sparse_sum += time.perf_counter() - start

                start = time.perf_counter()
                self.dijkstra(dense, 0)
                dij_dense_sum += time.perf_counter() - start

                start = time.perf_counter()
                self.floyd_warshall(sparse)
                fw_sparse_sum += time.perf_counter() - start

                start = time.perf_counter()
                self.floyd_warshall(dense)
                fw_dense_sum += time.perf_counter() - start

            # Store milliseconds for easier report usage.
            results["dijkstra_sparse"].append((dij_sparse_sum / repetitions) * 1000.0)
            results["dijkstra_dense"].append((dij_dense_sum / repetitions) * 1000.0)
            results["floyd_sparse"].append((fw_sparse_sum / repetitions) * 1000.0)
            results["floyd_dense"].append((fw_dense_sum / repetitions) * 1000.0)

            print(f"Completed n={size}")

        return results


def save_csv(results, output_dir):
    out_path = output_dir / "benchmark_results.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "nodes",
                "dijkstra_sparse_ms",
                "dijkstra_dense_ms",
                "floyd_sparse_ms",
                "floyd_dense_ms",
            ]
        )
        for i, size in enumerate(results["sizes"]):
            writer.writerow(
                [
                    size,
                    results["dijkstra_sparse"][i],
                    results["dijkstra_dense"][i],
                    results["floyd_sparse"][i],
                    results["floyd_dense"][i],
                ]
            )


def _style_axes(ax, title):
    ax.set_title(title)
    ax.set_xlabel("Number of nodes")
    ax.set_ylabel("Average time (ms)")
    ax.grid(True, alpha=0.3)
    ax.legend()


def save_plots(results, output_dir):
    sizes = results["sizes"]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, results["dijkstra_sparse"], marker="o", label="Sparse (p=0.1)")
    ax.plot(sizes, results["dijkstra_dense"], marker="s", label="Dense (p=0.7)")
    _style_axes(ax, "Dijkstra empirical runtime")
    fig.tight_layout()
    fig.savefig(output_dir / "dijkstra_sparse_dense.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, results["floyd_sparse"], marker="o", label="Sparse (p=0.1)")
    ax.plot(sizes, results["floyd_dense"], marker="s", label="Dense (p=0.7)")
    _style_axes(ax, "Floyd-Warshall empirical runtime")
    fig.tight_layout()
    fig.savefig(output_dir / "floyd_sparse_dense.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, results["dijkstra_sparse"], marker="o", label="Dijkstra")
    ax.plot(sizes, results["floyd_sparse"], marker="s", label="Floyd-Warshall")
    _style_axes(ax, "Algorithm comparison on sparse graphs")
    fig.tight_layout()
    fig.savefig(output_dir / "comparison_sparse.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, results["dijkstra_dense"], marker="o", label="Dijkstra")
    ax.plot(sizes, results["floyd_dense"], marker="s", label="Floyd-Warshall")
    _style_axes(ax, "Algorithm comparison on dense graphs")
    fig.tight_layout()
    fig.savefig(output_dir / "comparison_dense.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, results["dijkstra_sparse"], marker="o", label="Dijkstra sparse")
    ax.plot(sizes, results["dijkstra_dense"], marker="o", label="Dijkstra dense")
    ax.plot(sizes, results["floyd_sparse"], marker="s", label="Floyd sparse")
    ax.plot(sizes, results["floyd_dense"], marker="s", label="Floyd dense")
    _style_axes(ax, "Overall runtime comparison")
    fig.tight_layout()
    fig.savefig(output_dir / "overall_runtime.png", dpi=200)
    plt.close(fig)


def main():
    analyzer = GraphAnalyzer(seed=42)
    output_dir = Path(__file__).resolve().parent / "report_images"
    output_dir.mkdir(parents=True, exist_ok=True)

    sizes = list(range(20, 201, 20))
    repetitions = 5

    print("Running empirical analysis...")
    results = analyzer.empirical_analysis(
        sizes=sizes,
        repetitions=repetitions,
        sparse_density=0.1,
        dense_density=0.7,
    )

    save_csv(results, output_dir)
    save_plots(results, output_dir)

    print("Generating algorithm visualization snapshots...")
    sample_graph = analyzer.generate_graph(num_nodes=12, density=0.3)
    analyzer.visualize_dijkstra_snapshot(sample_graph, 0, output_dir)
    analyzer.visualize_floyd_warshall_snapshot(sample_graph, output_dir, source_node=0, target_node=11)

    print("Generating animated GIFs...")
    analyzer.generate_dijkstra_gif(sample_graph, 0, output_dir)
    analyzer.generate_floyd_warshall_gif(sample_graph, output_dir, source_node=0, target_node=11)

    dijkstra_dist, dijkstra_prev = analyzer.dijkstra(sample_graph, 0)
    floyd_dist, floyd_next = analyzer.floyd_warshall(sample_graph)

    target = 11
    dij_path = analyzer.reconstruct_path_dijkstra(dijkstra_prev, 0, target)
    fw_path = analyzer.reconstruct_path_floyd(floyd_next, 0, target)

    print("\nSample shortest-path check (0 -> 11):")
    print(f"Dijkstra path: {dij_path}, distance={dijkstra_dist[target]:.2f}")
    print(f"Floyd path:    {fw_path}, distance={floyd_dist[0, target]:.2f}")
    print(f"\nSaved results in: {output_dir}")


if __name__ == "__main__":
    main()