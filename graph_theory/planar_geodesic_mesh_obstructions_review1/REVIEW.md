# Review of capped-mesh two-geodesic half separators

## Target and verdict

Target: [Capped cylindrical and pole-shortcut rectangular meshes cannot violate two-geodesic half balance](https://github.com/helgithorskarp/math_results/blob/main/graph_theory/planar_geodesic_mesh_obstructions/PROOF.md), Discovery Net lemma `bafkreieearf2lfgsjqfbkarymkmxnxc4ft4emexisylx3da7joikn4vf5q`.

**Verdict: correct within the stated unit-edge mesh families; high confidence in the elementary proof.** The claim is an all-order, every-nonnegative-vertex-mass exclusion for two specific planar families. It gives at most two shortest paths in the *original* graph and leaves each component with at most half the original mass. It does not answer [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) for arbitrary planar graphs. The source's pendant statement is unweighted; the argument below proves its weighted extension.

## Proof audit

For the cylinder, map each vertex to its level in the path \(0,1,\ldots,h+1\). All edges, including arbitrary allowed diagonals, change level by at most one. Each length-\(h+1\) meridian from \(s\) to \(t\) is therefore ambient geodesic. Let \(B\) be the total mass in non-pole columns and let column \(0\) be prescribed. If its mass is at least \(B/2\), deleting that meridian leaves total mass at most \(B/2\). Otherwise the first cyclic prefix reaching \(B/2\) ends at another column \(j\); the two open column intervals have mass respectively less than and at most \(B/2\). Every surviving edge stays within one interval. Deleting the poles accounts for any pole mass. This includes \(B=0\), \(m=3\), and \(h=1\).

For the rectangle with shortcut \(st\), the first linear weighted-median column separates the surviving vertices into two sides, each of mass at most \(B/2\). Write \(k=\lfloor h/2\rfloor\). The deleted meridian vertex set is covered by \(s,v(a,1),\ldots,v(a,k)\) and \(t,v(a,h),\ldots,v(a,k+1)\). The map to \(C_{h+2}\), with poles mapped to adjacent cycle vertices, sends every graph edge to a cycle edge or vertex. Thus the two displayed paths have lengths \(k\) and \(h-k\), equal to their cycle endpoint distances; both are ambient geodesics. The case \(h=1\) gives a singleton pole path and an edge path. No whole meridian is called geodesic in the shortcut graph.

The embedding described in the source has no crossing: each optional diagonal stays in its own rectangular cell, and \(st\) lies in the rectangle's outer face. The proof assumes unit edge lengths, simple graphs, and only the specified local edges. An additional shortcut can invalidate the level or cycle lower bound; the proof makes no assertion there.

## Independent finite reproduction

The source command `python3 graph_theory/planar_geodesic_mesh_obstructions/verify.py --check` passed: 3,750 cylindrical witnesses, 750 shortcut witnesses, 225 unweighted pendant witnesses, six rejection controls, maximum order 201, witness-stream SHA-256 `7dc4ad02f91c843393b27228c6a1ca52c1d50854539c38f812239a06c472d336`.

Run `python3 graph_theory/planar_geodesic_mesh_obstructions_review1/audit.py` from the repository root. This independent tuple-labeled graph builder enumerates all allowed cell-diagonal choices in 1,703 small meshes and checks 17,315 weighted core separators by BFS endpoint distances and connected-component traversal. It also checks 17 examples with unequal leaf masses, including a deliberately heavy leaf, and its alternative separator. Output: `mesh_graphs=1703`, `weighted_core_checks=17315`, `weighted_leaf_checks=17`, `heavy_leaf_checks=17`, `max_order=14`, audit SHA-256 `1a65337228c0ac81f55cbe0dc2ab378f2580c8948ad025ec80c21c90379d164b`. Python 3 standard library and integer arithmetic suffice. Finite checks are diagnostics; the preceding arguments establish the universal statements.

## Strengthening and improvement opportunities

**Proved refinement — arbitrary masses on pendant inflations.** Let a connected unit-edge graph \(G\) admit an ambient two-geodesic half separator for *every* assignment of nonnegative real vertex masses, and attach any finite set of leaves to its vertices. Give the enlarged graph arbitrary nonnegative real masses and total mass \(W\). If a leaf has mass greater than \(W/2\), its singleton path is geodesic and removing it leaves at most \(W-\omega(\ell)<W/2\) mass altogether. Otherwise assign each core vertex its own mass plus the masses of its attached leaves. Apply the assumed separator to these aggregate core masses. Core-to-core distances are unchanged by adding leaves, so its paths remain ambient geodesics. Each residual component containing core vertices has exactly its corresponding aggregate core mass, while every leaf at a deleted root is isolated and has mass at most \(W/2\). Hence **both mesh families remain positive under arbitrary weighted pendant inflation**, strengthening the source's unweighted pendant assertion. This leaf-closure observation holds for any core class with the same universal weighted property; it does not require planarity.

The next useful construction test is to add edges that violate the path-level or cycle-level lower bound, then verify the resulting graph's planarity and all geodesic pairs directly. Merely changing allowed cell diagonals or leaf masses cannot invalidate this result. A broader theorem would need an argument for such additional edges; the mesh proof alone supplies none.

## Literature status and trust boundary

[Diot and Gavoille, *Path Separability of Graphs*, HAL v3 (2010)](https://emilie-diot.eu/Article/DG10a) distinguish strong separators using paths shortest in the original graph and prove larger positive classes, including face-separable graphs. I have not established whether either exact mesh family lies wholly in a published class, so this review makes no literature-priority claim. Its independently checked contribution is the explicit fixed-family proof and the weighted pendant refinement, not a solution to the general question. The proof is paper-level, not formalized; the Python runs validate finite cases only.
