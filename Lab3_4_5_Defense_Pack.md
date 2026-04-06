# Lab 3, 4, 5 Defense Pack (Presentation + Oral Exam)

This pack is built from your actual implementations and report flow.
It is organized by lab, with theory, algorithm behavior, pitfalls, edge cases, and examiner-style questions.

---

## How To Use This Pack

1. Learn each lab in this order: problem -> algorithm idea -> correctness intuition -> complexity -> implementation details -> edge cases.
2. Practice answering questions out loud in 60-120 seconds each.
3. For hard questions, use the answer direction to structure your response.
4. Keep one cross-lab story in mind: traversal (Lab 3), shortest paths (Lab 4), spanning trees (Lab 5).

---

## Lab 3: DFS vs BFS on Many Graph Families

### What The Lab Is About

Lab 3 compares DFS and BFS on many graph topologies (including directed, undirected, sparse, dense, multi-edge, and self-loop variants) and visualizes traversal behavior.

Core files:
- `Lab3/main.py`
- `Lab3/comp.py`

### Implemented Algorithms

#### DFS (recursive)
- Visits one branch deeply before backtracking.
- Uses recursion stack + visited set.
- In code: `dfs(graph, start, visited=None, path=None)` in `Lab3/main.py`.

#### BFS (iterative queue)
- Visits nodes in increasing distance layers from the start.
- Uses deque queue + visited set.
- In code: `bfs(graph, start)` in `Lab3/main.py`.

#### Step-recording variants
- `dfs_steps(...)` and `bfs_steps(...)` capture state per step for animation/snapshots.

### Theory You Should Present

1. Traversal objective:
- DFS and BFS both enumerate the reachable component from a start node.

2. Correctness intuition:
- `visited` prevents revisits and guarantees termination on cyclic graphs.
- Every reachable node is eventually discovered via adjacency expansion.

3. Complexity:
- Both are $O(V + E)$ time using adjacency lists.
- Both are $O(V)$ auxiliary memory in worst case.

4. Practical difference:
- DFS memory is depth-sensitive (stack depth).
- BFS memory is frontier-width-sensitive (queue breadth).

### Important Implementation Behavior In Your Code

1. Graph generation covers many types in `make_graph(...)`, including:
- path, cycle, complete, star, bipartite, binary_tree, forest
- dag, directed_cycle, directed_multigraph
- grid, sparse, dense, simple
- multigraph, pseudograph, wheel, regular, weighted

2. Multigraph/pseudograph behavior:
- Traversal graph is collapsed to simple graph for DFS/BFS reachability.
- Visualization graph preserves multi-edges/self-loops for display.

3. Weighted graph behavior:
- Weights exist as edge attributes but DFS/BFS ignore weights.

4. Benchmarking behavior:
- Uses repeats (`REPEATS = 3`) and averages runtime.
- Heavy graph types use smaller test sizes to limit runtime.

### What Examiners Usually Probe

1. If both are $O(V+E)$, why can one still be faster?
- Constants, cache effects, recursion overhead, queue behavior, topology shape.

2. Is BFS always better for shortest path?
- Only for unweighted (or equal weight) graphs.

3. Does DFS find shortest paths in unweighted graphs?
- No, not guaranteed.

4. Why does traversal order change across runs/graphs?
- Depends on adjacency order.

### Lab 3 Edge Cases (Made-Up + Expected Behavior)

1. Single node, no edges:
- DFS/BFS both return `[0]`.

2. Disconnected graph from start node in one component:
- Both return only reachable nodes from start; not full graph.

3. Self-loop node (u,u):
- Node is visited once; loop does not cause infinite traversal due to `visited`.

4. Parallel edges (multigraph):
- Reachability unchanged after collapse to simple graph.

5. Directed cycle 0->1->2->0:
- Both terminate and visit each reachable node once.

6. Very deep path graph (chain):
- DFS recursion depth grows with n and may approach recursion limit.
- BFS queue remains small on a simple chain.

7. Very wide tree:
- BFS queue can become large at wide levels.
- DFS stack may stay moderate if depth is limited.

8. Weighted graph with misleading heavy/light edges:
- Traversal order unaffected by weights in this lab.

### Lab 3 Quick Oral Structure (90 seconds)

1. Goal: compare DFS and BFS on diverse graph structures.
2. Method: adjacency-list traversals + step capture + runtime benchmarking.
3. Theory: same asymptotic time $O(V+E)$, different memory profile by topology.
4. Result interpretation: topology impacts constants and frontier/stack shape.
5. Limitation: BFS/DFS here are traversal tools, not weighted shortest-path solvers.

### Lab 3 Examiner Questions (20)

1. Why do DFS and BFS have identical asymptotic time on adjacency lists?
Answer direction: each vertex and edge is processed at most once.

2. Give a graph where BFS uses more memory than DFS.
Answer direction: wide balanced tree.

3. Give a graph where DFS risks recursion-depth issues.
Answer direction: long chain/path graph.

4. Why is `visited` required for cyclic graphs?
Answer direction: prevents infinite revisits and duplicate processing.

5. What does BFS optimize in unweighted graphs?
Answer direction: minimum number of edges from start.

6. Can DFS produce different valid traversal orders on the same graph?
Answer direction: yes, depends on neighbor iteration order.

7. Why collapse multigraphs for traversal but keep them for visualization?
Answer direction: reachability is unchanged; visualization should reflect structure.

8. In your lab, do edge weights influence traversal order?
Answer direction: no, weights are ignored by DFS/BFS.

9. Why average over repeats during benchmarking?
Answer direction: reduce noise from system/process variance.

10. Why use smaller sizes for heavy graph types?
Answer direction: dense/complete families scale edge count quadratically.

11. Is path length metric in traversal equal to shortest path length?
Answer direction: no, here it means number of visited nodes/path list length.

12. If graph is disconnected, how to visit all nodes?
Answer direction: run traversal from each unvisited node (component-wise).

13. Could BFS ever visit a deeper node before a shallower one?
Answer direction: not in standard queue BFS on unweighted graph.

14. Could DFS be iterative instead of recursive?
Answer direction: yes, explicit stack equivalent.

15. What changes for directed graphs?
Answer direction: neighbors follow outgoing edges; reachability is directional.

16. If adjacency is matrix instead of list, complexity changes to?
Answer direction: often $O(V^2)$ because scanning all possible neighbors.

17. Why are snapshots useful pedagogically?
Answer direction: expose frontier/current/visited state transitions.

18. What is the worst-case BFS queue size?
Answer direction: up to $O(V)$.

19. What is the worst-case DFS recursion stack size?
Answer direction: up to $O(V)$.

20. State one real-world use of each.
Answer direction: DFS for cycle/component structure, BFS for minimum-hop routing.

---

## Lab 4: Dijkstra vs Floyd-Warshall (Shortest Paths)

### What The Lab Is About

Lab 4 compares single-source shortest paths (Dijkstra) against all-pairs shortest paths (Floyd-Warshall), including benchmarking by graph size and density plus visualization.

Core files:
- `Lab4/main.py`
- `Lab4/impl.py`
- `Lab4/main.tex`

### Implemented Algorithms

#### Dijkstra (min-heap)
- Computes shortest paths from one source to all reachable nodes.
- Uses relaxation with priority queue.
- In code: `dijkstra(self, graph, start_node)`.

#### Floyd-Warshall (dynamic programming)
- Computes shortest paths for every ordered pair (i,j).
- Uses DP over allowed intermediate vertices.
- In code: `floyd_warshall(self, graph)`.

### Theory You Should Present

1. Problem scope difference:
- Dijkstra: single-source.
- Floyd-Warshall: all-pairs.

2. Dijkstra correctness condition:
- Requires non-negative edge weights for greedy selection validity.

3. Floyd-Warshall DP recurrence:
- $d_{ij}^{(k)} = \min\left(d_{ij}^{(k-1)}, d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\right)$

4. Complexity:
- Dijkstra (heap + matrix scan here): practical behavior near $O(V^2)$ scanning per pop, with heap updates.
- Floyd-Warshall: $O(V^3)$ time, $O(V^2)$ space.

5. Data representation effect:
- Lab uses adjacency matrix (`INF` for absent edges), so sparse graphs do not gain full adjacency-list advantage.

### Important Implementation Behavior In Your Code

1. Graph generation:
- Builds connected weighted undirected matrix.
- First creates random spanning tree, then adds edges by density.

2. Dijkstra details:
- Uses stale-entry skipping in priority queue (`if current_dist > distances[u]: continue`).
- Returns distances + predecessor array for reconstruction.

3. Floyd-Warshall details:
- Uses NumPy vectorized candidate matrix each k-iteration.
- Maintains `next_node` matrix for path reconstruction.

4. Reconstruction:
- Dijkstra reconstructs by backtracking predecessors.
- Floyd reconstructs by repeatedly following `next_node` hops.

5. Visualization states:
- Dijkstra states track current node, visited set, distances.
- Floyd states track current intermediate k and matrix evolution.

### What Examiners Usually Probe

1. Why Dijkstra fails on negative edges.
2. When all-pairs justifies Floyd despite cubic cost.
3. How representation (matrix vs list) shifts practical runtime.
4. Why path reconstruction needs extra structures (`previous`, `next_node`).

### Lab 4 Edge Cases (Made-Up + Expected Behavior)

1. Single node graph:
- Dijkstra distance to itself is 0.
- Floyd diagonal is 0.

2. Unreachable pair (if disconnected input supplied):
- Distances remain `INF`, reconstructed path empty.

3. Start equals end:
- Reconstruction returns `[start]`.

4. Negative edge with Dijkstra:
- Can produce incorrect result (algorithm assumption violated).

5. Negative cycle with Floyd:
- Distances can keep reducing conceptually; robust implementations detect via negative diagonal.
- Your implementation does not explicitly report negative-cycle errors.

6. Dense graph n=200:
- Floyd runtime increases steeply due to $O(V^3)$ loops.

7. Sparse graph with matrix representation:
- Dijkstra still scans many `INF` entries, reducing sparse advantage.

8. Equal-length alternative shortest paths:
- One valid predecessor chain chosen based on relaxation/ordering.

### Lab 4 Quick Oral Structure (90 seconds)

1. Goal: compare single-source vs all-pairs shortest-path strategies.
2. Method: weighted connected graph generation, two algorithms, repeat-based timings.
3. Theory: Dijkstra is greedy with non-negative constraint; Floyd is DP with cubic scaling.
4. Results: choice depends on query workload (one source vs all pairs) and graph size/density.
5. Limitation: negative-weight/negative-cycle handling requires explicit safeguards.

### Lab 4 Examiner Questions (20)

1. Why is Dijkstra invalid with negative edges?
Answer direction: greedy finalization can be overturned by later negative relaxation.

2. State Floyd-Warshall recurrence and meaning of k.
Answer direction: shortest path using intermediates from set {0..k}.

3. When would Floyd-Warshall be preferable despite $O(V^3)$?
Answer direction: many all-pairs queries on moderate-size dense graphs.

4. Why keep `previous` in Dijkstra?
Answer direction: to reconstruct actual path, not only distance value.

5. Why keep `next_node` in Floyd?
Answer direction: to route from i to j after DP finishes.

6. What does `INF` represent in adjacency matrix?
Answer direction: absence of direct edge.

7. How does connected-graph generation influence benchmark fairness?
Answer direction: avoids trivial unreachable-heavy cases and keeps comparisons meaningful.

8. What is stale heap entry skipping?
Answer direction: ignore outdated queue entries when a shorter distance already exists.

9. If all edge weights are 1, what could replace Dijkstra?
Answer direction: BFS for single-source shortest hops.

10. Is Floyd-Warshall suitable for very large sparse graphs?
Answer direction: usually no, cubic cost dominates.

11. How does matrix representation affect Dijkstra complexity in practice?
Answer direction: neighbor scans are over all V entries.

12. How to detect negative cycle after Floyd?
Answer direction: check if any diagonal entry dist[i][i] < 0.

13. Why run each test multiple times?
Answer direction: smooth timing variance and improve reproducibility.

14. If two shortest paths tie, must output be unique?
Answer direction: no, any shortest path is valid.

15. Can Dijkstra be modified to stop early?
Answer direction: yes for single-target query once target is extracted-finalized.

16. Compare memory footprints of the two algorithms.
Answer direction: Dijkstra lower; Floyd stores full VxV matrices.

17. How would adjacency list improve sparse-case Dijkstra?
Answer direction: iterate only existing neighbors, reducing wasted scans.

18. Explain why Floyd naturally handles directed graphs.
Answer direction: matrix need not be symmetric; recurrence remains valid.

19. What happens if start node is isolated?
Answer direction: only self distance finite; others stay INF.

20. Give one real-world use case each.
Answer direction: Dijkstra for single-source routing; Floyd for precomputed all-pairs latency tables.

---

## Lab 5: Kruskal vs Prim (Minimum Spanning Tree)

### What The Lab Is About

Lab 5 studies greedy MST construction by comparing Kruskal and Prim across graph sizes and densities, with visual snapshots/animations and performance plots.

Core files:
- `Lab5/impl.py`
- `Lab5/main.py`
- `Lab5/main.tex`

### Implemented Algorithms

#### Kruskal
- Sort edges by weight ascending.
- Add edge if it connects two different components.
- Component tracking uses Disjoint Set Union (Union-Find).

#### Prim
- Start from one node and grow one tree.
- Always pick lightest frontier edge from current tree to outside.
- Uses min-heap priority queue.

### Theory You Should Present

1. Problem:
- Build a minimum total-weight spanning tree in connected, weighted, undirected graph.

2. Greedy validity (cut property):
- Lightest edge crossing a cut that respects current partial solution is safe to add.

3. Complexity:
- Kruskal: $O(E \log E)$ plus near-constant amortized union-find operations.
- Prim (heap): $O((V+E)\log V)$.

4. Structure difference:
- Kruskal grows a forest and merges components.
- Prim grows one connected tree from a seed node.

5. Output property:
- Both return an MST of size exactly $V-1$ edges in connected graph.

### Important Implementation Behavior In Your Code

1. DisjointSet optimizations:
- Path compression in `find`.
- Union by rank in `union`.

2. Graph generation:
- Random geometric-style weights from Euclidean node positions.
- Connectivity enforced by linking components if needed.

3. Step tracking:
- Both algorithms record intermediate MST edges for snapshots/animation.

4. Benchmarking:
- Node sizes include up to 1000.
- Both sparse (`density=0.3`) and dense (`density=0.7`) tested.
- Averaged over multiple trials.

### What Examiners Usually Probe

1. Why union-find is critical for Kruskal.
2. Why Prim may outperform in practice despite similar asymptotic dense-case form.
3. Whether equal weights break correctness (they do not).
4. What happens on disconnected inputs (minimum spanning forest).

### Lab 5 Edge Cases (Made-Up + Expected Behavior)

1. Single node:
- MST is empty edge set, total weight 0.

2. Two nodes one edge:
- MST is that edge.

3. All edges equal weight:
- Many valid MSTs exist; algorithms may pick different trees but equal total weight.

4. Complete graph with random weights:
- Both produce MST with V-1 edges; Kruskal pays global sort cost.

5. Star graph with cheap center-leaf edges:
- Prim from center often picks MST quickly via frontier.

6. Disconnected graph (without enforced bridging):
- True MST does not exist globally; result should be minimum spanning forest.

7. Parallel edges between same nodes:
- Lower-weight parallel edge is preferred for MST if representation preserves both.

8. Negative weights:
- Both algorithms remain valid for MST in undirected graphs (unlike Dijkstra).

9. Very dense graph n=1000:
- Memory/time pressure increases strongly due to large E.

10. Tie-heavy graph:
- Different but equally optimal MST structures can be returned.

### Lab 5 Quick Oral Structure (90 seconds)

1. Goal: compare two greedy MST strategies.
2. Method: geometric weighted graphs, density sweep, repeated timing, visual state tracking.
3. Theory: cut property, Kruskal with DSU, Prim with heap frontier.
4. Results: practical performance differs by constants and graph structure.
5. Limitation: results depend on graph model and implementation details.

### Lab 5 Examiner Questions (20)

1. Define MST formally.
Answer direction: spanning tree minimizing total edge weight.

2. Why does Kruskal need cycle detection?
Answer direction: avoid violating tree acyclicity while adding light edges.

3. How does DSU improve Kruskal runtime?
Answer direction: near-constant component membership/merge operations.

4. Why does Prim use a priority queue?
Answer direction: repeatedly extract minimum frontier edge efficiently.

5. Can Prim and Kruskal output different MST structures?
Answer direction: yes, especially with ties.

6. Must their total MST weight match?
Answer direction: yes, all MSTs have same minimum total weight.

7. Why exactly V-1 edges in MST?
Answer direction: tree property on V vertices.

8. What if graph is disconnected?
Answer direction: no spanning tree over all vertices; get forest instead.

9. Are negative edge weights a problem for MST algorithms?
Answer direction: no, still valid in undirected case.

10. Compare edge-centric vs vertex-centric greediness.
Answer direction: Kruskal global edge ordering vs Prim local frontier growth.

11. Dense graph: why can Kruskal suffer?
Answer direction: sorting very large edge set dominates.

12. Sparse graph: why can Kruskal still be competitive?
Answer direction: fewer edges reduce sort burden.

13. What is path compression intuitively?
Answer direction: flatten find paths for future speed.

14. What is union by rank intuitively?
Answer direction: attach shallower tree below deeper to limit height.

15. Can we start Prim from any node?
Answer direction: yes; total MST weight remains optimal.

16. Why run benchmarks at two densities?
Answer direction: expose algorithm behavior under different E/V regimes.

17. Why repeat trials per size?
Answer direction: reduce randomness/noise from graph generation and runtime jitter.

18. If many equal weights, is result deterministic?
Answer direction: depends on tie-breaking order.

19. Real-world setting where Kruskal is natural?
Answer direction: edge-list pipelines / offline sorted edge processing.

20. Real-world setting where Prim is natural?
Answer direction: incremental network expansion from existing hub/tree.

---

## Cross-Lab Synthesis You Should Say In Presentation

1. Lab 3 (Traversal):
- Reachability and visit order, not weighted optimization.

2. Lab 4 (Shortest Paths):
- Optimize path cost between nodes.
- Single-source vs all-pairs tradeoff.

3. Lab 5 (Spanning Tree):
- Optimize global connectivity cost without cycles.

4. Technique contrast:
- Greedy appears in Dijkstra, Prim, Kruskal.
- Dynamic programming is explicit in Floyd-Warshall.

5. Representation matters:
- Adjacency list vs matrix can shift practical performance even when high-level algorithm is same.

6. Asymptotics vs constants:
- Big-O predicts trend; implementation details decide practical crossover at your tested sizes.

---

## Ultra-Hard Defense Questions (Bonus 12)

1. Provide a formal cut-property argument for both Prim and Kruskal.
2. Prove why BFS gives shortest path in unweighted graphs but DFS does not.
3. Give a concrete negative-edge counterexample where Dijkstra fails.
4. Explain how changing Lab 4 to adjacency list would alter complexity and measured curves.
5. If Lab 3 adjacency ordering is randomized each run, what metrics remain stable and what changes?
6. Why can two different MSTs have same weight? Give a tied-weight graph and two valid outputs.
7. For Lab 4, discuss numerical stability concerns with floating weights and INF handling.
8. Compare memory bounds across all labs and identify worst practical bottleneck at n=1000.
9. If graph updates online (edge insertions), which algorithms adapt better and which require recomputation?
10. Show how to detect and report invalid assumptions early in each lab pipeline.
11. If asked to optimize one bottleneck per lab, what exact code-level refactor would you propose?
12. Design one fair benchmarking protocol that can compare Labs 3/4/5 style algorithms under a shared hardware-noise model.

---

## Final 2-Minute Combined Script

"Lab 3 studies graph traversal behavior with DFS and BFS across many graph families. The key theoretical result is equal asymptotic time $O(V+E)$ with different memory profiles depending on graph shape. Lab 4 moves from traversal to weighted shortest paths, contrasting Dijkstra for single-source queries and Floyd-Warshall for all-pairs precomputation; the major constraint is non-negative weights for Dijkstra and cubic scaling for Floyd. Lab 5 studies minimum spanning trees using two greedy methods, Kruskal with union-find and Prim with a frontier heap. Across all three labs, I connect theory to implementation: data representation, tie handling, and constants strongly influence empirical performance, so algorithm choice is determined by both asymptotic guarantees and workload structure." 

---

## Fast Self-Check Before Presentation

1. Can you explain each algorithm in 30 seconds without notes?
2. Can you state each key complexity from memory?
3. Can you give one failure mode/assumption violation per lab?
4. Can you defend one empirical trend with both theory and implementation details?
5. Can you answer why your chosen representation affects observed runtime?

If yes, you are presentation-ready.
