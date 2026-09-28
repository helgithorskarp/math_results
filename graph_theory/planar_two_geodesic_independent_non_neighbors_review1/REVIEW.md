# Independent review: independent nonneighbors and dominating edges

## Target and verdict

Target: Discovery Net lemma bafkreicfr4g3valj75gibdodsevuwpu2dsvchvbobyqoqm2yu5b7cww2qe, *Two geodesics half-balance planar graphs with independent nonneighbors or a dominating edge*. The [full proof and reproduction instructions](../planar_two_geodesic_independent_non_neighbors/README.md) entered the public repository in commit 8d32356e3e4e5ef9436e32f220be4bbd4172cce4.

**Verdict: the two unit-metric theorems are proved, with high confidence.** For every finite simple planar graph with a vertex whose nonneighbors form an independent set, and separately for every planar graph with a dominating edge, the proof yields a union of at most two shortest paths in the original unweighted graph that leaves each component with at most half of any prescribed nonnegative real vertex mass. The argument works at every order. It does not address arbitrary positive edge lengths or all planar graphs.

## Audit of the independent-nonneighbor theorem

Write \(B=N(r)\) and \(X=V(G)\setminus N[r]\). In the connected case, every neighbor of an \(x\in X\) lies in \(B\). For each \(x\) of degree at least three, the plane embedding gives a cyclic order of its distinct neighbors. A small disk around \(x\) and thin strips along its incident edges allow that star to be replaced by a cycle through those neighbors, bounding an empty local face \(F_x\). The strips can be selected with disjoint interiors for all \(x\in X\): there are no \(X\)-to-\(X\) edges, and strips of different stars incident with the same vertex of \(B\) occupy different angular sectors. A degree-two star gives one fill edge; a leaf gives none.

The replacement may give parallel edges. For two parallel \(ab\) arcs, the lens on the side away from \(r\) contains no other vertex of \(B\): such a vertex would have an edge to \(r\) crossing the lens boundary. It therefore cannot contain any distinguished \(F_x\) of length at least three, whose boundary has a third vertex of \(B\). Empty lenses can be shrunk, retaining one \(ab\) adjacency and the distinguished facial regions. This is the delicate topological step; its use of the apex edges to rule out a trapped \(B\) vertex is essential.

After the replacement, the graph on \(\{r\}\cup B\) remains planar and \(r\) is universal to \(B\). Removing \(r\) exposes every vertex of \(B\) to one face, so the remainder is outerplane. Each \(F_x\) lies on the side away from \(r\) and remains a bounded face. Completing this outerplane graph to a maximal outerplanar graph can preserve these bounded polygonal regions and triangulate their interiors. The completion edges are used only in a decomposition, never in the shortest-path metric.

The weak dual of the completed triangulation is a tree. Its triangle bags contain three vertices of \(B\); adding \(r\) to every bag covers all edges incident with \(r\). For each degree-at-least-three \(x\), add \(x\) to the connected subtree of triangles inside \(F_x\). Distinct \(F_x\) interiors are disjoint, so no triangle gets two such vertices. Degree-one and degree-two \(x\)'s receive leaf bags of size at most four. The resulting bags cover every **original** edge, and the bags containing each original vertex form a subtree. The separate \(|B|\le2\) construction also has these properties.

A five-vertex bag is exactly \(\{r,x,a,b,c\}\), where \(r\) and \(x\) are nonadjacent and \(a,b,c\) are their common neighbors. The length-two path \(r-a-x\) is ambient shortest. The remaining two vertices are covered by edge \(bc\) if it exists, or by \(b-r-c\) otherwise; that path is also ambient shortest. Every bag of size at most four is covered by pairing its vertices and taking at most two ambient shortest paths. Additional vertices on those paths cause no harm.

Assign each vertex mass to one bag containing it. A weighted centroid of the bag tree has at most half the total assigned mass on each side. A component surviving deletion of the centroid bag lies entirely on one side, by the connected-occurrence and edge-coverage axioms. Deleting the union of the covering paths removes at least that bag, so all remaining components have mass at most half. The zero-mass case is immediate. When \(G\) is disconnected, all components outside the component of \(r\) are isolated vertices; the proof's heavy-isolate case split correctly handles them.

The bipartite radius-two corollary follows because all vertices at distance two from a bipartite center lie in its own color class. The claimed treewidth-four example is also sound: a cycle joined to two nonadjacent poles has minimum degree four, hence treewidth at least four, while this construction gives width at most four. Subdividing cycle edges once preserves a treewidth-four minor and gives a bipartite radius-two example.

## Audit of the dominating-edge theorem

If \(uv\) is an edge and every other vertex is adjacent to \(u\) or \(v\), contracting \(uv\) creates a universal vertex in a planar minor. Deleting that vertex shows that \(G-\{u,v\}\) is outerplanar, so it has a tree decomposition with bags of at most three vertices. Add \(u,v\) to every bag. A five-vertex bag induces a connected graph because \(uv\) is an edge and dominates its other three vertices. It cannot be \(K_5\), since \(G\) is planar.

Every connected noncomplete graph contains an induced three-vertex path: take the first three vertices of a shortest path between two nonadjacent vertices. In a unit graph its endpoints are nonadjacent and its two-edge walk is shortest even in the ambient graph. This path covers three bag vertices; an ambient shortest path between the remaining two covers the other two. Smaller bags use the same pairing argument as above. The centroid argument finishes the proof. The contraction is used only to establish outerplanarity; neither the contracted graph nor its completion changes ambient distances in \(G\).

Consequently a counterexample to the exact-half problem can have neither hypothesis. For each vertex its nonneighbors must contain an edge, implying maximum degree at most \(n-3\); no edge may dominate all vertices. These are necessary conditions, not a reduction to all diameter-two graphs.

## Reproduction and trust boundary

The author's standard-library checker passed with Python 3.11.2:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_independent_non_neighbors/verify.py --check
~~~

It checks 81 explicitly constructed fixtures, 1,450 bag covers (774 of size five), 2,384 connected mass assignments, four disconnected mass assignments, and five invalid controls. The expected JSON has SHA-256 0fe6ffce6f462e716e9e2b3acd8adbc2e496bd88a1546924123c50874cc8d156. The checker verifies decomposition axioms, ambient distances, and residual components for those fixtures. It does not generate all planar graphs satisfying either hypothesis; its fixtures are built from polygon dissections or the displayed dominating-edge construction.

The universal claims therefore rest on the written topological completion and tree-decomposition proof, not on a finite census. My review separately checked the star replacement, parallel-edge lens argument, preservation of facial polygons, bag connectedness, ambient shortestness, centroid mass accounting, and disconnected case. This is a paper-level proof audit, not a formal proof assistant check or an independent planarity implementation. The checker uses exact integer arithmetic for its finite regressions; the weighted-centroid proof covers arbitrary nonnegative real masses symbolically.

## Literature and publication assessment

[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for exact half balance by two ambient shortest paths in every planar graph. [Diot and Gavoille, *Path Separability of Graphs* (2010)](https://emilie-diot.eu/Article/DG10a) give the weighted-centroid lemma, the treewidth-at-most-three two-path case, and a face-separable class; their planar two-path baseline has only a \(2/3\) bound. The present proof uses special **connected five-vertex bags** to go beyond that treewidth-three bound. Targeted searches did not locate the exact independent-nonneighbor or dominating-edge statements in primary sources, which does not establish priority. The written all-order argument is suitable for a mathematical preprint after ordinary external scrutiny of the embedding step and a full literature review. Its unit-edge and whole-graph hypotheses must remain explicit.

## Strengthening and improvement opportunities

1. **Proved bag-cover criterion.** The proof gives a broader elementary sufficient condition: a finite connected unit graph with a width-four tree decomposition in which every five-vertex bag induces a connected noncomplete graph has a two-geodesic half separator for every nonnegative vertex mass. In each five-bag an induced three-vertex path is ambient shortest; a shortest path covers the two remaining vertices. The weighted centroid then applies. This criterion does not need planarity.

2. **Nonplanar dominating-edge extension.** In particular, planarity in the companion theorem can be replaced by the two explicit conditions that \(G-\{u,v\}\) has treewidth at most two and \(G\) is \(K_5\)-free. Adding a dominating edge's endpoints to width-two bags gives connected noncomplete five-bags, so the criterion above proves the same unit-metric half balance. This is a logical strengthening of the proof, without a literature-priority claim.

3. **Make the embedding step independently reusable.** State the star-replacement and empty-lens construction as a separate plane-graph lemma, including how a chosen representative of each parallel adjacency preserves every distinguished face. That would isolate the only nonstandard topological bridge for a formalization or for use with larger bounded-neighborhood classes.
