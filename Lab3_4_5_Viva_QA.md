# Lab 3-4-5 Viva Q and A (Integrated, Concise)

This file pairs each question with a direct model answer for fast oral rehearsal.

---

## Lab 3: DFS vs BFS (20)

1. Q: Why do DFS and BFS have identical asymptotic time on adjacency lists?
A: Because each reachable vertex is discovered once and each edge is examined at most once, giving O(V+E).

2. Q: Give a graph where BFS uses more memory than DFS.
A: A wide balanced tree; BFS stores a large frontier level, while DFS stores mainly one root-to-leaf path.

3. Q: Give a graph where DFS risks recursion-depth issues.
A: A long chain/path graph of length n, where recursion depth is about n.

4. Q: Why is visited required for cyclic graphs?
A: It prevents revisiting nodes forever and guarantees termination.

5. Q: What does BFS optimize in unweighted graphs?
A: Minimum number of edges (minimum hop count) from the start node.

6. Q: Can DFS produce different valid traversal orders on the same graph?
A: Yes. Order depends on neighbor iteration order in the adjacency structure.

7. Q: Why collapse multigraphs for traversal but keep them for visualization?
A: Reachability is unchanged by parallel edges, but visualization should still show true graph structure.

8. Q: In your lab, do edge weights influence traversal order?
A: No. DFS and BFS in Lab 3 ignore weights.

9. Q: Why average over repeats during benchmarking?
A: To reduce timing noise from OS scheduling, cache effects, and short-run jitter.

10. Q: Why use smaller sizes for heavy graph types?
A: Complete/dense-like families have O(n^2) edges, so runtime and plotting cost grow quickly.

11. Q: Is path length metric in traversal equal to shortest path length?
A: No. In this context it reflects visited-order list length, not shortest weighted/unweighted path distance.

12. Q: If graph is disconnected, how to visit all nodes?
A: Run DFS/BFS from every still-unvisited vertex (component-wise traversal).

13. Q: Could BFS ever visit a deeper node before a shallower one?
A: Not in standard queue BFS on an unweighted graph.

14. Q: Could DFS be iterative instead of recursive?
A: Yes. Replace recursion with an explicit stack.

15. Q: What changes for directed graphs?
A: Traversal follows outgoing edges only, so reachability becomes directional.

16. Q: If adjacency is matrix instead of list, complexity changes to?
A: Typically O(V^2), since neighbor checks scan all possible vertices per node.

17. Q: Why are snapshots useful pedagogically?
A: They make current node, visited set, and frontier evolution visible step by step.

18. Q: What is the worst-case BFS queue size?
A: O(V).

19. Q: What is the worst-case DFS recursion stack size?
A: O(V).

20. Q: State one real-world use of each.
A: DFS: cycle/component structure analysis. BFS: minimum-hop routing in unweighted networks.

---

## Lab 4: Dijkstra vs Floyd-Warshall (20)

1. Q: Why is Dijkstra invalid with negative edges?
A: Its greedy finalization assumes distances never improve later; negative edges can violate that assumption.

2. Q: State Floyd-Warshall recurrence and meaning of k.
A: d_ij^(k) = min(d_ij^(k-1), d_ik^(k-1) + d_kj^(k-1)); k is the highest-index allowed intermediate vertex.

3. Q: When would Floyd-Warshall be preferable despite O(V^3)?
A: When you need all-pairs shortest paths repeatedly on moderate-size dense graphs.

4. Q: Why keep previous in Dijkstra?
A: To reconstruct actual shortest paths, not just final distance values.

5. Q: Why keep next_node in Floyd?
A: To reconstruct a route from i to j after DP completes.

6. Q: What does INF represent in adjacency matrix?
A: No direct edge between those two vertices.

7. Q: How does connected-graph generation influence benchmark fairness?
A: It avoids degenerate disconnected cases and keeps algorithm comparisons meaningful.

8. Q: What is stale heap entry skipping?
A: Ignoring popped queue entries whose distance is outdated compared with current best.

9. Q: If all edge weights are 1, what could replace Dijkstra?
A: BFS for single-source shortest hop count.

10. Q: Is Floyd-Warshall suitable for very large sparse graphs?
A: Usually no, because O(V^3) time dominates.

11. Q: How does matrix representation affect Dijkstra complexity in practice?
A: It forces scanning V potential neighbors each step, even when most are absent.

12. Q: How to detect negative cycle after Floyd?
A: Check diagonal entries; any dist[i][i] < 0 indicates a negative cycle.

13. Q: Why run each test multiple times?
A: To smooth variance and report a stable average runtime.

14. Q: If two shortest paths tie, must output be unique?
A: No. Any one of the shortest paths is valid.

15. Q: Can Dijkstra be modified to stop early?
A: Yes, for single-target queries you can stop when target is extracted with final distance.

16. Q: Compare memory footprints of the two algorithms.
A: Dijkstra is lighter; Floyd stores full VxV distance and routing matrices.

17. Q: How would adjacency list improve sparse-case Dijkstra?
A: It iterates only real neighbors, reducing wasted scans and lowering practical runtime.

18. Q: Explain why Floyd naturally handles directed graphs.
A: The matrix can be asymmetric; recurrence does not require undirected symmetry.

19. Q: What happens if start node is isolated?
A: Distance to itself is 0; all other distances remain INF.

20. Q: Give one real-world use case each.
A: Dijkstra: point-to-all routing from one source. Floyd: precomputed all-pairs latency table.

---

## Lab 5: Kruskal vs Prim (20)

1. Q: Define MST formally.
A: A spanning tree of a connected weighted undirected graph with minimum possible total edge weight.

2. Q: Why does Kruskal need cycle detection?
A: It adds globally light edges, so cycle checks are needed to keep the result a tree.

3. Q: How does DSU improve Kruskal runtime?
A: It supports near-constant amortized find/union operations for component checks.

4. Q: Why does Prim use a priority queue?
A: To repeatedly choose the lightest frontier edge efficiently.

5. Q: Can Prim and Kruskal output different MST structures?
A: Yes, especially when edge weights tie.

6. Q: Must their total MST weight match?
A: Yes, both are optimal MST algorithms, so total weight is minimum.

7. Q: Why exactly V-1 edges in MST?
A: Any tree on V vertices has V-1 edges.

8. Q: What if graph is disconnected?
A: No global MST exists; algorithms produce a minimum spanning forest.

9. Q: Are negative edge weights a problem for MST algorithms?
A: No, MST algorithms remain valid with negative edges in undirected graphs.

10. Q: Compare edge-centric vs vertex-centric greediness.
A: Kruskal is edge-centric (global sorted edges), Prim is vertex/frontier-centric (grow one tree).

11. Q: Dense graph: why can Kruskal suffer?
A: Sorting very large edge sets dominates runtime.

12. Q: Sparse graph: why can Kruskal still be competitive?
A: Fewer edges reduce sorting cost and DSU checks stay cheap.

13. Q: What is path compression intuitively?
A: During find, nodes are rewired closer to root so future finds are faster.

14. Q: What is union by rank intuitively?
A: Attach shallower tree under deeper tree to limit height growth.

15. Q: Can we start Prim from any node?
A: Yes. For connected graphs, total MST optimal weight is unchanged.

16. Q: Why run benchmarks at two densities?
A: To compare behavior under different E/V regimes (sparse vs dense).

17. Q: Why repeat trials per size?
A: To reduce randomness from graph generation and timing noise.

18. Q: If many equal weights, is result deterministic?
A: Not necessarily; tie-breaking order can change selected edges.

19. Q: Real-world setting where Kruskal is natural?
A: Offline edge-list processing where edges are already available globally.

20. Q: Real-world setting where Prim is natural?
A: Incremental network expansion from an existing connected core/hub.

---

## Ultra-Hard Bonus (12)

1. Q: Provide a formal cut-property argument for both Prim and Kruskal.
A: For any cut that respects the current partial solution, the lightest crossing edge is safe. Prim picks the lightest edge from current tree cut; Kruskal picks global lightest safe edge across component cuts.

2. Q: Prove why BFS gives shortest path in unweighted graphs but DFS does not.
A: BFS explores by layers of hop count, so first discovery of a node uses minimum hops. DFS commits deep before exhausting shallower alternatives, so it can miss shorter-hop routes.

3. Q: Give a concrete negative-edge counterexample where Dijkstra fails.
A: Example: s->a=2, s->b=5, b->a=-10. Dijkstra may finalize a at 2 before exploring b, but true shortest to a is -5 via b.

4. Q: Explain how changing Lab 4 to adjacency list would alter complexity and measured curves.
A: Sparse-case Dijkstra would improve substantially by iterating only real neighbors; curve slope and constants would drop versus matrix scans.

5. Q: If Lab 3 adjacency ordering is randomized each run, what metrics remain stable and what changes?
A: Reachability count and asymptotic class stay stable; exact traversal order and some constant-factor timing vary.

6. Q: Why can two different MSTs have same weight? Give a tied-weight graph and two valid outputs.
A: Ties allow multiple edge choices with equal total cost. In a 4-cycle of all weight 1, removing any one edge gives a valid MST of weight 3.

7. Q: For Lab 4, discuss numerical stability concerns with floating weights and INF handling.
A: Repeated floating additions can accumulate small error; INF comparisons must be handled carefully to avoid invalid relaxations and NaN propagation.

8. Q: Compare memory bounds across all labs and identify worst practical bottleneck at n=1000.
A: Lab 3 traversals are O(V) auxiliary; Lab 5 is O(V+E); Lab 4 Floyd is O(V^2) matrices and is the strongest memory pressure among these methods.

9. Q: If graph updates online (edge insertions), which algorithms adapt better and which require recomputation?
A: BFS/DFS can be rerun locally or fully depending task; Dijkstra usually reruns from source; Floyd often needs broad recomputation; MST can be updated with dynamic structures but basic implementations typically recompute.

10. Q: Show how to detect and report invalid assumptions early in each lab pipeline.
A: Add pre-checks: non-negative weights for Dijkstra, connectivity requirement when claiming MST, graph-size/recursion guards for DFS, and optional negative-cycle detection for Floyd.

11. Q: If asked to optimize one bottleneck per lab, what exact code-level refactor would you propose?
A: Lab 3: iterative DFS to avoid recursion risk; Lab 4: adjacency-list Dijkstra for sparse graphs; Lab 5: optimize edge handling and avoid repeated heavy plotting in benchmark loops.

12. Q: Design one fair benchmarking protocol that can compare Labs 3/4/5 style algorithms under a shared hardware-noise model.
A: Fixed seeds, warm-up runs, same machine load, multiple repetitions, median plus confidence interval, identical graph families per size/density, and separate timing from visualization.

---

## One-Line Drill Mode

Use this when revising fast: read the question and answer in one breath, then restate answer with one extra example.
