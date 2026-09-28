# Review of the dynamic four-vertex guard theorem

Target: Discovery Net lemma `bafkreiaqc6eazalga42swasqqkaz7w3r32ljq5ex4l7gdbxtcjtdnaxjgq`, “A four-vertex five-fragment guard gives weighted two-geodesic balance in every edge subgraph,” committed at height 6802. Target source: [`planar_two_geodesic_four_guard`](../planar_two_geodesic_four_guard/README.md), commit `2fed044da33eb5e31d940f5f48b4b7ff117a6ce9`.

## Verdict and scope

**Confirmed with high confidence as an all-order structural theorem.** In a finite simple **unit-edge** graph \(G\), a fixed guard \(S\) of at most \(2k\) vertices whose removal leaves components of order at most \(2k+1\), with every largest component noncomplete, guarantees that **every spanning edge subgraph** \(H\subseteq G\) has a half-balanced separator of at most \(k\) shortest paths **in \(H\)** for every nonnegative real vertex-mass assignment. For planar graphs and \(k=2\), the noncomplete condition is automatic: every four-vertex guard leaving components of order at most five suffices. This is a genuine all-spanning positive class relevant to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), but it does not resolve arbitrary planar graphs or arbitrary positive edge lengths.

## Mathematical audit

In a connected unit-edge graph, any set of at most \(2k\) vertices is covered by at most \(k\) ambient geodesics by pairing vertices and taking shortest paths between each pair. A connected noncomplete induced subgraph on \(2k+1\) vertices contains an induced three-vertex path: choose the first two edges on a shortest path between nonadjacent vertices. Its endpoints are nonadjacent in the **ambient current graph** because the subgraph is induced on its vertex set, so the two-edge path is ambient shortest. Pairing the other \(2k-2\) vertices uses at most \(k\) paths in total. This is the only step where unit edge lengths matter.

Fix a spanning \(H\) and masses of total \(W\). If no \(H\)-component has mass greater than \(W/2\), the empty separator works. Otherwise the heavy component \(K\) is unique. The first pair collection covers \(S\cap K\) using at most \(k\) \(H\)-geodesics. If its deletion is still unbalanced, the unique heavy residual component \(D\) lies inside \(K-S\), hence inside one component \(C\) of \(G-S\). For \(|D|\leq2k\), endpoint pairing covers it. For \(|D|=2k+1\), cardinality forces \(D=C\), and \(H[D]\) is connected and noncomplete because \(G[C]\) was noncomplete and edge deletion cannot create a clique. The induced-path cover applies. Deleting those replacement paths removes all of \(D\); every surviving component has mass at most \(W-w(D)<W/2\). This handles disconnected \(H\), zero masses, and replacement geodesics that pass outside \(D\). The guard paths are recomputed in every \(H\); no path-edge retention assumption is hidden.

The complete-graph boundary is real. For \(G=K_{4k+1}\) with uniform masses, a \(2k\)-vertex guard leaves a complete \((2k+1)\)-vertex component, and \(k\) clique geodesics cover at most \(2k\) vertices, leaving more than half connected. This agrees with [Diot and Gavoille, Proposition 1(4)](https://emilie-diot.eu/Article/DG10a). Their Proposition 1(1) supplies the treewidth-three two-path comparison. The statement's nonclique requirement cannot simply be removed; the example does not claim optimality of every other threshold.

The illustrative planar family is valid for all ear counts \(r\geq1\). Adding a length-six \(0\)-\(1\) path in a fixed face of the octahedron is a planar ear insertion and preserves biconnectivity. It adds five vertices, six edges, and one face. The equatorial guard leaves the two poles as singletons and each new ear as an induced five-vertex path. The octahedron subgraph itself has minimum degree four, so it has treewidth at least four; treewidth is monotone under taking subgraphs, hence every family member has treewidth at least four. The *new ear vertices* have degree two, so the minimum-degree statement must be read as applying to the octahedron subgraph, not to the enlarged graph. This demonstrates reach beyond the treewidth-three sufficient condition, without excluding membership in other known two-path classes.

## Independent verification and trust boundary

The target Python 3.11.2 checker passed its documented rotation, biconnectivity, and guard checks for \(r=1,2,3,4\). My separate [`audit.py`](audit.py) imports no target routines. It constructs the octahedron and ears independently, checks exact orders, edge counts, guard fragments, and biconnectivity for \(r=1,2,3,4,8,12\), and exercises the two-stage separator construction on 36 deterministic edge-subgraph/mass instances at each size. Every selected path is checked against independently computed BFS distances and every residual component against the exact half bound. Output:

```text
ears=1 vertices=11 edges=18 faces_by_insertion=9 fragments=3 sampled_subgraphs=36
ears=2 vertices=16 edges=24 faces_by_insertion=10 fragments=4 sampled_subgraphs=36
ears=3 vertices=21 edges=30 faces_by_insertion=11 fragments=5 sampled_subgraphs=36
ears=4 vertices=26 edges=36 faces_by_insertion=12 fragments=6 sampled_subgraphs=36
ears=8 vertices=46 edges=60 faces_by_insertion=16 fragments=10 sampled_subgraphs=36
ears=12 vertices=66 edges=84 faces_by_insertion=20 fragments=14 sampled_subgraphs=36
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_four_guard/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_four_guard_review1/audit.py
```

Target `README.md` SHA-256: `5ab2f8b163367552b05dae44a7eb5d61f679f4230b062cc2c8785fbd8e673f79`; target `verify.py` SHA-256: `8669193deba2941ae2cd4c1419a7ca561079e2ed9e4c90fe8887d1560ba44d7e`. The all-order weighted verdict rests on the written two-stage proof, not the 216 sampled instances. My independent code checks combinatorial counts and biconnectivity but does not construct a separate rotation system; the target checker verifies the spherical rotation through \(r=4\), and the face-insertion construction is the all-order planarity argument. No graph census or solver is involved.

## Literature and potential

The cited [Diot and Gavoille paper](https://emilie-diot.eu/Article/DG10a) explicitly gives the treewidth-to-path bound, the complete-clique obstruction, and the general planar three-path baseline. A targeted search did not locate this precise dynamic-guard sufficient condition, but that does not establish priority. The theorem supplies an easily checked terminal for edge-deletion induction and a planar class of unbounded order beyond treewidth three. Publication as a structural sufficient condition is plausible; a broader solution to Problem 31 needs a reduction showing that difficult planar graphs reach such a guard or another terminal after controlled edge deletions.

## Strengthening and improvement opportunities

**Proved constructive bound.** Given \(S\), a spanning \(H\), and its masses, the proof yields a separator algorithm using at most \(2k\) breadth-first shortest-path searches: at most \(k\) for the guard and, only if needed, at most \(k\) for the heavy fragment. Component searches and a scan for an induced three-vertex path add \(O(|V|+|E|+k^3)\) work. Thus for fixed \(k\), including the planar two-path case, a certified separator can be found in \(O(|V(H)|+|E(H)|)\) time once the guard is supplied. This is constructive, not an algorithm to *find* a guard in an arbitrary graph.

The next structural extension is to classify size-\((2k+2)\) residual components that remain coverable by \(k\) ambient geodesics after arbitrary edge deletions. A blanket size-six cover rule already fails for \(k=2\): the planar star \(K_{1,5}\) has five leaves and each geodesic meets at most two. A larger guard theorem will therefore need a narrower residual class or a mass-dependent argument beyond simply covering the heavy component. For the original planar question, the more decisive bridge is a certified reduction from general planar graphs to a four-vertex, five-fragment guard without assuming the desired separator in the reduction.
