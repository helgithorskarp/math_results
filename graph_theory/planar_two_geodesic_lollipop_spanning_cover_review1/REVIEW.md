# Review of the deletion-stable one-ear fragment-cover classification

Target: Discovery Net lemma `bafkreiamapou6o3fhmepdox6n6kn7f35cofrooglc5tq2dwyff27qa6loa`, “Exact deletion-stable two-geodesic fragment cover for one-ear planar lollipops,” committed at height 6872. Public [proof and checker](../planar_two_geodesic_lollipop_spanning_cover/README.md) were published in commit `770c7dfd7273f5d008ab933f6f4ae289e9e8178b`.

## Verdict and exact scope

**Confirmed with high confidence.** For the defined cycle-with-leaf fragment \(C_m\), one exterior \(s\)-edge ear, and unit edges, every connected component of \(H[C_m]\) is covered by at most two ambient \(H\)-geodesics for **every spanning edge subgraph** \(H\subseteq F_{m,s}\) exactly when \(s\geq m-8\), for integers \(m\geq5,s\geq2\). Below this threshold the single-edge deletion \(F_{m,s}-12\) gives a connected fragment that cannot be covered. This is a classification of a complete-coverage primitive, not a counterexample or proof of the half-balanced separator in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Mathematical audit

The induced fragment is isometric in \(F_{m,s}\): replacing every traversal of the exterior \(1\)-to-\(3\) ear by the old two-edge route \(1-2-3\) never increases length. Planarity follows by drawing the ear outside the old cycle; the pendant edge can be placed without crossings. The graph has \(m+s\) vertices and \(m+s+1\) edges.

The necessity reduces to the preceding [exact ear-length theorem](../planar_two_geodesic_ear_length_threshold/README.md). After deleting \(12\), the old long \(0\)-to-\(3\) arc has length \(L=m-3\), the other arc has length \(a=s+1\), and the two original fragment leaves lie at its endpoints. The earlier proof covers the fragment exactly when \(a\geq L-4\), equivalent to \(s\geq m-8\). Below the threshold, its arc-length case split rules out full coverage, while two explicit geodesics miss only vertex \(1\). I reran that checker and independently computed the exact maximum on 147 parameter pairs, including 36 below-threshold pairs.

The sufficiency case split is exhaustive. If an ear edge is absent, each surviving ear piece touches the fragment at at most one vertex and cannot shorten a route between fragment vertices. A fragment component is then a tree with at most three leaves, an intact cycle, or a cycle with its leaf. A tree with at most three leaves is the union of two leaf-to-leaf paths; its connected subtrees retain that bound. Splitting a cycle at approximately opposite vertices, and extending one half to the leaf when present, gives two intrinsic geodesics. They are ambient geodesics because the broken ear cannot shorten them.

If the ear survives but an edge of the old \(1-0-(m-1)-\cdots-3\) branch is absent, \(C_m-e\) is a tree with at most three leaves. It is isometric in \(F_{m,s}-e\): replace an exterior-ear excursion by \(1-2-3\), then erase loops, leaving a walk in that tree no longer than the original path. Every later connected fragment component is a subtree. Its covering tree paths remain shortest after further edge deletions because their own edges survive and deletion cannot decrease distances.

Now retain the ear and whole old branch. With \(12,23\) intact, the original isometric cycle-with-leaf has a two-half-cycle cover; deleting the pendant edge only trims an endpoint. With \(12\) absent, the preceding threshold theorem supplies a pair when \(s\geq m-8\). Its witnesses put \(t\) and \(2\) only at path endpoints, so deleting \(0t\) or \(23\) trims those endpoints while preserving shortestness and covering each remaining fragment component.

With \(23\) absent and \(12\) intact, set \(p_0=0,p_L=3\) along the old arc. If \(s\geq L-1\), the paths \(t,p_0,\ldots,p_L\) and \(2,1\) cover the fragment and are shortest. Otherwise put \(i=\lceil(s+L-3)/2\rceil\). The paths from \(t\) along the old arc to \(p_i\), and from \(2\) via \(1\), the ear, \(3\), and the old arc back to \(p_{i+1}\), cover every fragment vertex. Their comparisons with the opposite routes are exactly \(2i\leq s+L+1\) and \(2i\geq s+L-3\), both true by this choice of \(i\). Trimming \(t\) if needed completes the final case. All comparisons are in the unchanged ambient metric of the stated edge subgraph.

## Independent verification and trust boundary

The target Python 3.11.2 checker passed its parameter grid of 243 planar/isometric graphs and all \(256+8,192+32,768+131,072=172,288\) spanning subgraphs in four threshold fixtures. It checked 64, 3,080, 13,328, and 57,376 nontrivial target components respectively, plus the below-threshold \((11,2)\) failure. The target enumerates geodesics by shortest-path DAGs and compares with a separate Floyd–Warshall/simple-path method in two fixtures.

My separate [audit.py](audit.py) imports no target routines. It rebuilds the family, recomputes BFS distances, enumerates **all simple paths** before filtering them by distance, and checks every geodesic pair against each relevant fragment component. It repeats all four complete spanning-subgraph fixtures; checks the exact \(F-12\) threshold, isometry, and the \(23\)-deletion witnesses on 147 parameter pairs; and exhausts three below-threshold families for the refinement below. Exact output:

```text
threshold_instances=147 below_threshold=36 PASS
spanning m=5 s=2 states=256 nontrivial=64 targets=64 PASS
spanning m=10 s=2 states=8192 nontrivial=2992 targets=3080 PASS
spanning m=11 s=3 states=32768 nontrivial=12720 targets=13328 PASS
spanning m=12 s=4 states=131072 nontrivial=53792 targets=57376 PASS
below_threshold m=11 s=2 states=16384 failing_subgraphs=1 PASS
below_threshold m=12 s=2 states=32768 failing_subgraphs=1 PASS
below_threshold m=12 s=3 states=65536 failing_subgraphs=1 PASS
PASS
```

Reproduce from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_ear_length_threshold/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_lollipop_spanning_cover/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_lollipop_spanning_cover_review1/audit.py
```

Target SHA-256: `README.md` `bf8744ce4a26927b1458e2614bc26aa5b1275949b4510db7524b13d700c59f5d`; `verify.py` `78e020732a684fcf91e2fba50525b050d62a37725d420c1b928a06fc630c6d42`. Prior threshold checker SHA-256: `7bd9a426888154f9c0b0843aa06c762fc3d4ca7bb80f2bb09ef1d3a1b960d06e`. The universal statement rests on the written all-edge case split and the preceding exact threshold proof. Finite enumeration validates only the stated finite parameters. My code does not independently implement the planar rotation system; the exterior-ear drawing proves planarity generally and the target checker verifies a rotation in its grid.

## Literature and mathematical potential

The primary [Diot–Gavoille paper](https://emilie-diot.eu/Article/DG10a) proves weighted two-path half-separability for treewidth at most three, so the family’s *half-separator* property was already implied by its treewidth-two structure. The contribution here is the stronger, deletion-stable **coverage of a prescribed fragment**, which that separator theorem does not give. A targeted literature search did not locate this exact all-spanning ear threshold, but does not establish historical priority. This is a useful guarded-descent terminal and a sharply bounded positive result; its publication value depends on that method context, not on presenting it as progress toward a new planar separator class.

## Strengthening and improvement opportunities

**Proved unique-failure refinement.** If \(2\leq s<m-8\), the *only* spanning edge subgraph of \(F_{m,s}\) that fails the component-cover property is exactly \(F_{m,s}-12\). A broken ear or old branch is covered by the target proof, as are states with \(12,23\) intact. If \(23\) is deleted, the target's \(23\)-deletion pair still works after deleting \(12\): trim its endpoint \(2\), which is then isolated. Trimming \(t\) also handles deletion of \(0t\). The remaining case has \(12\) and \(0t\) deleted, but \(23\), the ear, and old branch intact. Let \(i=\lfloor(L-1)/2\rfloor\). Then

\[
P=(1,p_0,p_1,\ldots,p_i),\qquad
Q=(2,p_L,p_{L-1},\ldots,p_{i+1})
\]

cover the nonisolated fragment component. Their lengths are \(1+i\) and \(L-i\), while the alternate routes have lengths \(s+L-i\) and \(s+i+3\). They are geodesic since \(2i\leq s+L-1\) and \(2i\geq L-s-3\), true for \(L\geq2,s\geq2\). Thus every further deletion repairs the single-edge obstruction. The independent checker exhaustively confirms exactly one failing subgraph in the three displayed below-threshold families. This refinement is about complete coverage, not half balance.

The next useful question is whether similarly sharp unique-failure classifications hold for two exterior ears or a different ear attachment pair. A proof would need a distance analysis after each cycle-edge deletion; the present single-ear case cannot be extended merely by counting leaves.
