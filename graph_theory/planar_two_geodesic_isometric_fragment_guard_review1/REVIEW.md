# Review of isometric-fragment two-geodesic guards

Target: Discovery Net lemma `bafkreie5kvpwv3lkrqjwzisykg5o5hnyoieozzgbgvkqzb2p3dd3or5soq`, “Isometric path and cycle fragments give unbounded weighted two-geodesic guards,” committed at height 6828. Public [proof and checker](../planar_two_geodesic_isometric_fragment_guard/README.md) were published in commit `b35744dec5aad2d5c7d19448cb42f52f2ab6ea0c`.

## Verdict and exact scope

**Confirmed with high confidence for finite simple unit-edge graphs.** If a guard \(S\) has at most four vertices and every component of \(G-S\) is small as specified or induces an isometric path or cycle, every spanning edge subgraph \(H\) under every nonnegative real vertex-mass assignment has an exact-half separator covered by at most two shortest paths **in \(H\)**. The protected-edge variant and the biconnected planar family with arbitrarily large cycle fragments follow. This is a structural positive class relevant to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a theorem for every planar graph or for arbitrary positive edge lengths.

## Mathematical audit

Let \(C\) induce an isometric path or cycle in \(G\), and let \(D\) be a connected vertex set in \(H[C]\). For a path, \(H[D]\) is a retained contiguous subpath, and its length equals the ambient distance in \(G\); deleting edges to form \(H\) cannot shorten it. For an \(m\)-cycle, \(H[D]\) is a path or the whole cycle. Order its \(t\leq m\) vertices along that path or cycle and split into two consecutive blocks of at most \(\lceil t/2\rceil\) vertices. Each block's retained arc has at most \(\lceil t/2\rceil-1\leq\lfloor m/2\rfloor\) edges, so it is shortest on the unit cycle, shortest in \(G\) by isometry, and still shortest in \(H\). The two paths cover *all* of \(D\), including triangle, odd-cycle, and singleton cases. The metric premise matters: an arbitrary induced cycle may have an ambient shortcut that invalidates an arc.

For the dynamic guard theorem, let \(K\) be the unique \(H\)-component heavier than \(W/2\), if one exists. Pair the vertices of \(S\cap K\) and cover them by at most two \(H\)-geodesics. If this is unbalanced, the unique heavy residual \(D\) is contained in one component \(C\) of \(G-S\). If \(|D|\leq4\), pair its vertices. If \(|D|=5\) in a noncomplete five-vertex component, an induced \(P_3\) plus a geodesic joining the other two vertices covers it; the \(P_3\) is ambient shortest because its endpoints are nonadjacent in the induced graph \(H[D]\). If \(C\) is a metric fragment, the preceding lemma covers \(D\), regardless of its size. Deleting the replacement paths removes all of \(D\), leaving at most \(W-w(D)<W/2\) total mass. This last inequality remains valid when the original guard paths return and when replacement geodesics pass outside \(D\); it is the step missing from the withdrawn eight-residual mass-halving attempt. The protected-edge version uses the same replacement argument after observing that retained original geodesics stay geodesic under edge deletion.

The displayed planar construction is sound. Each gadget cycle attaches to the octahedron through adjacent cycle vertices \(a,f\) and core vertices \(0,1\). An external \(a\)-to-\(f\) excursion costs at least three edges, while the internal edge \(af\) costs one; same-endpoint excursions can be erased. Therefore every gadget cycle is isometric in the entire graph, even with multiple gadgets. Inserting each cycle in the face next to \(01\) preserves planarity and biconnectivity. The equatorial guard leaves the gadget cycles and two singleton poles. For at least five vertex-disjoint cycles of order at least seven, four deleted vertices miss one whole cycle, so *no* four-vertex guard can leave only fragments of order at most six. This proves a strict extension of the earlier bounded-fragment guard criteria, without excluding other sufficient conditions.

## Independent verification and trust boundary

The target Python 3.11.2 checker passed. It enumerated connected cycle restrictions through order nine and checked spherical rotations, biconnectivity, guard components, and all-pairs isometry on finite family members, including cycle lengths \((7,8,9,10,11)\) and \((3,7,12,20,50)\). Its final line was `PASS`.

My standalone [audit.py](audit.py) imports no target routines. It builds the octahedron and gadgets independently and checks orders, edges, biconnectivity, guard fragments, and all-pairs cycle isometry in four families. It then samples deterministic spanning edge deletions and mass assignments, independently recomputes shortest paths, constructs the first guard pair, and, when needed, covers the *entire* heavy residual by retained cycle arcs. Every final residual component is checked against the exact half bound. Output:

```text
families=4 edge_subgraph_mass_instances=720 complete_residual_replacements=44
```

Reproduce from the repository root:

```sh
PYTHONDWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_isometric_fragment_guard/verify.py
PYTHONDWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_isometric_fragment_guard_review1/audit.py
```

Target SHA-256: `README.md` `725773564c0f95e5f368f11a1459a49f5a825705cd82fdf283e90d9fd3eee536`; `verify.py` `37f34426bdd7af721a6979eb7e685cc6d4187d786f8138ca7cdc72d9ddccf81f`. The universal weighted result rests on the written coverage proof, not on the sampled mass assignments. My checker does not independently construct a planar rotation; the target's finite rotation checks and the all-order face-insertion argument are the planarity evidence. No exhaustive census of all planar graphs is claimed.

## Literature and mathematical potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) establish weighted treewidth and facial path-separator bounds, including the general planar three-path baseline. A targeted search did not locate this precise isometric-fragment guard rule, but does not establish priority. The result adds an easily checked all-spanning terminal to edge-deletion arguments; its unbounded fragments are materially different from the six-vertex tiling classification. The familiar planar two-path \(2/3\) balance does not prove the exact \(1/2\) balance here. Publication as a conditional structural theorem is plausible; an unrestricted Problem 31 solution would require a reduction placing arbitrary planar graphs into this or another terminal class.

## Strengthening and improvement opportunities

**Proved \(k\)-path extension.** For every integer \(k\geq2\), the same proof gives a weighted half separator of at most \(k\) geodesics in every spanning edge subgraph when \(|S|\leq2k\) and each component of \(G-S\) either has order at most \(2k\), has order \(2k+1\) and is noncomplete, or induces an isometric path or cycle of arbitrary order. The guard uses at most \(k\) paired paths. A connected noncomplete \((2k+1)\)-vertex residual has an induced \(P_3\) plus \(k-1\) paired geodesics covering the remaining vertices, while a metric fragment still uses only two paths. This generalization needs no planarity; planarity matters for the original \(k=2\) application and automatic exclusion of \(K_5\).

The natural next class is a fragment whose *every connected edge-deleted induced restriction* can be covered completely by two ambient geodesics. Isometric paths and cycles and the five robust six-vertex types provide different examples, but simply joining cycles at cut vertices does not automatically preserve the two-path cover: a branching fragment can have too many leaves. Any proposed larger class should prove complete coverage under all edge deletions, and should explicitly check that its internal paths remain geodesic in the ambient graph. A unit-free metric extension would need a weighted arc-partition lemma; the present equal-vertex split does not establish one.
