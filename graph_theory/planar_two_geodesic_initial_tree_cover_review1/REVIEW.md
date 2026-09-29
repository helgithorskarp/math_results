# Review of deletion-stable internal covers of induced trees

Target: Discovery Net lemma `bafkreigemzegkicd3tsa2irk7bceyhqekrx7mqcu5f5hkcdrxrwxl3rcem`, “An intact internal geodesic cover of an induced tree persists through every edge deletion,” height 6986. The [proof and family checker](../planar_two_geodesic_initial_tree_cover/README.md) were published at verified source commit `dc9bfa6693d2133c7d0ea3c944ef09daf5a5cb27`.

## Verdict and exact scope

**Confirmed with high confidence.** An induced tree has a deletion-stable internal cover by at most \(k\) ambient geodesics exactly when the intact tree already has one. The same paths, restricted to a connected surviving vertex set, are valid witnesses. No planarity or tree isometry is needed for this equivalence. The four-vertex guard corollary and the explicit unbounded planar family follow under their stated hypotheses. These are sufficient classes bearing on [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a solution for arbitrary planar graphs. The established two-path two-thirds balance statement has a different threshold from the one-half target here.

## Mathematical audit

Let \(P\) be one original internal \(G\)-geodesic and \(D\) a connected vertex set of \(H[T]\), where \(H\) is obtained by deleting edges. Since \(T\) is induced, \(H[T]\) is a forest using only tree edges. The unique \(T\)-path between any two vertices of \(D\) survives and stays in \(D\), so \(D\) is convex in \(T\). The intersection \(P\cap D\) is therefore empty or a single contiguous subpath whose edges survive in \(H\). Any subpath of a \(G\)-geodesic remains a \(G\)-geodesic. Deleting edges cannot reduce the distance between its endpoints, while the retained subpath still provides an \(H\) route of the same length, so it is also an ambient \(H\)-geodesic. Intersecting each of the \(k\) intact paths with \(D\) covers \(D\). The converse takes \(H=G\) and \(D=V(T)\). This proves the exact quantifiers, not merely the finite examples.

The leaf observation is sound: a leaf of a tree can occur on an internal tree path only as an endpoint, so \(k\) paths cover at most \(2k\) leaves. For \(k=2\), checking all internal tree paths whose lengths equal their **full ambient** endpoint distances, including singletons, gives an exact finite cover test for a specified tree. This test is weaker than requiring the tree to be isometric, which would make every internal path geodesic.

In the displayed family, deleting the four equatorial guard vertices leaves the two octahedral poles as singletons and one ten-vertex induced tree per gadget. Each tree has nine edges and four leaves. The two internal same-side leaf-pair paths each have length four, cover the whole tree, and attain ambient endpoint distance four. But one selected opposite-side leaf pair has internal tree distance five and ambient distance three through the guard edge \(0\!-!1\), proving nonisometry. The graph has \(6+10r\) vertices and \(12+13r\) edges. An all-order planar embedding places the \(r\) parallel \(0\)-to-\(1\) gadget spines in disjoint strips inside one octahedral face; the four arms and the two leaf-to-guard links of each gadget fit beside that spine within its strip. Euler's formula then gives \(8+3r\) faces. The published rotation checker confirms the embedding on finite instances, but the all-order assertion uses this strip construction.

The guard implication uses the previously reviewed heavy-component descent. First cover the four guard vertices by two ambient geodesics. A heavy residual lies within a single component of \(G-S\), and after edge deletion it is a connected vertex set of that component's surviving induced tree, or has at most four vertices. The tree theorem supplies two paths covering the entire heavy residual. Replacing the initial pair with them removes the heavy mass, leaving less than half the total mass outside. In a unit-edge planar host, the separate five-vertex rule extends the small residual allowance. The protected-edge version is also valid: a retained original geodesic remains geodesic after deletion, and residual components can only split before the same heavy-component replacement.

## Independent reproduction and trust boundary

The target [verify.py](../planar_two_geodesic_initial_tree_cover/verify.py) passed its published \(r=1,2,5\) family checks and 8,192 one-gadget deletion profiles. I also exercised its rotation construction at \(r=10,25\); its face and Euler checks passed. My standalone [audit.py](audit.py) imports no target code. It builds the octahedron and gadgets directly from the edge description, recomputes ambient distances by BFS, enumerates eligible internal geodesic pairs, verifies nonisometry and residual trees, and independently checks all 8,192 masks of the 13 gadget and attachment edges while holding the octahedron fixed. The 45,056 surviving tree components are all covered by restrictions of the same two original paths. Exact output:

```text
families=[(1, 16, 25, 11), (2, 26, 38, 14), (5, 56, 77, 23)] deletion_masks=8192 residual_components=45056 noninduced_hamiltonian_paths=4 nonisometric=PASS two_internal_geodesics=PASS
```

The last count concerns the explicit noninduced boundary example below. Reproduce from the repository root with Python 3.11 or later, standard library only, assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_initial_tree_cover/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_initial_tree_cover_review1/audit.py
```

Target SHA-256: `README.md` `9168dc74ebb1266fa3f97668af757d9d1c68122e0396d64d725b8eae5756e152`; `verify.py` `30205a082a70e4f29442d3b882ec4d68d54aafb9d0f0c964b72941745eb73c35`. The finite checks validate these unit-edge instances and deletion masks. The arbitrary-order, arbitrary-positive-length theorem rests on the written tree-convexity proof. My audit does not reconstruct the planar rotation; planarity for all \(r\) rests on the explicit strip embedding, supported by the target's rotation checks.

## Literature and mathematical potential

The official [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for two shortest paths at one-half balance. [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give broader structural path-separability results, including treewidth-based classes and a weighted planar three-path bound. A targeted search did not locate this exact induced-tree intersection formulation; that is not historical-priority evidence. Relative to the committed graph, it replaces a global isometry hypothesis on each tree terminal by the strictly weaker, directly checkable existence of two covering geodesics. The proof is elementary but useful as a reusable reduction; the planar family shows the new hypothesis has genuinely nonisometric cases. It would fit naturally as a lemma in a larger separator argument rather than as a stand-alone resolution of the open question.

## Strengthening and improvement opportunities

**Proved selected-tree extension and sharp boundary.** The pure deletion-stability equivalence does not need \(T\) to be induced if \(D\) is defined as a connected vertex set in the **surviving selected tree-edge forest** \((V(T),E(T)\cap E(H))\). Convexity and path restriction hold exactly as above, even if \(G[V(T)]\) has chords. One cannot simply drop inducedness while keeping \(D\) connected in \(H[V(T)]\): take the unit path \(T=0-1-2-3-4\) and add chords \(0-3\), \(1-4\), each of length three. The intact tree path has length four and is a \(G\)-geodesic. Delete tree edge \(2-3\) but retain the chords. All five vertices remain connected in \(H[V(T)]\), yet none of its four Hamiltonian paths is an \(H\)-geodesic; thus no single internal \(H\)-geodesic covers them. The independent audit checks every such path. The selected-edge forest instead has components \(\{0,1,2\}\) and \(\{3,4\}\), each covered by a restricted original geodesic. This specifies exactly where the induced hypothesis enters the target theorem and guard use.

**Nonnegative metrics.** The pure tree-intersection theorem also extends to nonnegative edge lengths, with geodesics understood as simple minimum-cost paths. Tree convexity, subpath optimality, and monotonicity of distances under deletion require no strict positivity. This does not by itself extend the separate unit-edge five-vertex planar rule or remove the induced-tree condition from the guard corollary.
