# Review of the pentagonal-core ninety-price box

Target: Discovery Net lemma `bafkreiefmlq7mlexzz7r3pv7p3lobdoisky366maslozcvkkhfraslalxu`, “A ninety-dimensional price box gives half-balanced two-geodesic separators on a five-connected planar core,” height 7081. The [proof](../planar_two_geodesic_pentagonal_core_price_box/README.md), [certificate](../planar_two_geodesic_pentagonal_core_price_box/certificate.json), [main checker](../planar_two_geodesic_pentagonal_core_price_box/verify.py), and [same-researcher audit](../planar_two_geodesic_pentagonal_core_price_box/audit.py) were published at verified commit `b53a915cc2783b6ecf87f096700cb7071ae915ee`.

## Verdict and exact scope

**Confirmed with high confidence.** On this specified 32-vertex, five-connected planar graph, every nonnegative real vertex mass has a half-balanced separator made of at most two ambient shortest paths for every metric in the claimed full 90-coordinate box. The six prescribed paths are certified throughout the box; three *alternative pairs* plus a separate four-heavy-vertex case prove the mass assertion. This is a conditional positive metric family for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). It does not establish the one-half two-path claim for every planar graph or every metric on this graph. The known two-path two-thirds theorem is weaker than the target.

## Mathematical audit

The twelve cyclic pentagons use 20 original vertices. Each of their 30 boundary edges occurs once in each direction. Coning each pentagon adds one vertex and five edges, creating 60 oriented triangles on \(V=32,E=90,F=60\). I independently checked opposite directed face incidences, connected vertex links, and Euler's equation; these certify the stated spherical triangulation. The 20 old vertices have degree six and the twelve cone vertices degree five.

For a prescribed path \(P\), put its edges at \(c_e+1\) and every other edge at \(c_e-1\). At this adverse corner, its listed 32-entry potential obeys all 90 edge inequalities and has endpoint gain equal to the path length. I checked all \(6\cdot90=540\) inequalities and independently recomputed the six endpoint distances by exact Floyd–Warshall; the lengths are \(40,37,32,25,41,39\). For any competitor \(Q\), shared edges cancel in \(\ell(Q)-\ell(P)\). Every edge belonging only to \(Q\) is cheapest and every edge belonging only to \(P\) is dearest at this corner. Therefore \(P\) stays shortest for *every independent real selection* of the 90 prices, including ties on the boundary. The six different adverse corners do not need to coincide. Common positive scaling preserves all comparisons.

After deletion of each prescribed pair, my component reconstruction gives orders \((4,17)\), \((4,19)\), and \((9,12)\). Let \(A,B\) be the respective 17- and 19-vertex components, and \(C,D\) the 9- and 12-vertex components of pair three. The exact sets satisfy \(A\cap C=\varnothing\) and \(B\cap D=\varnothing\). If some at-most-four-vertex set carries at least half the total mass, pairing those vertices and taking two ambient geodesics covers it, leaving every component at most half. Otherwise each four-vertex component is light. Failure of pair one forces \(w(A)>W/2\), and failure of pair two forces \(w(B)>W/2\); disjointness and nonnegative masses give \(w(C),w(D)<W/2\), so pair three works. This argument covers zero masses and real values without mass enumeration. The three prescribed pairs alone are insufficient: vertex 1 lies on none of their paths, so the separate four-vertex case is essential.

My audit also checks connectivity after each of the \(\binom{32}{4}=35{,}960\) four-vertex deletion sets. With minimum degree five, no smaller separating set can evade this test: after deleting \(s<4\) vertices, each residual component has at least \(6-s\) vertices, so adding only \(4-s\) deletions cannot remove an entire component. Minimum degree five supplies the matching upper bound; vertex connectivity is exactly five. The graph is therefore outside constructions that require a nonempty attachment with a boundary of at most three vertices. Under uniform mass, deleting a facial triangle leaves a connected 29-vertex graph, so the face-separable sufficient condition does not explain this example.

## Independent reproduction and trust boundary

Both target commands passed with the recorded JSON outputs, including 90 dimensions, 540 potential inequalities, 35,960 deletion checks, and 406 split-vertex flow checks in the same-researcher audit. My standalone [audit.py](audit.py) imports no target Python. It reads only the 1,790-byte certificate, rebuilds the embedding from its cyclic faces, checks the 540 inequalities, uses a separate Floyd implementation, reconstructs the three component partitions, checks all four-deletion sets, and verifies the exact radius witness below. Run from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_pentagonal_core_price_box/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_pentagonal_core_price_box/audit.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_pentagonal_core_price_box_review1/audit.py
```

The independent command prints:

```text
vertices=32 edges=90 faces=60 dimensions=90 potential_inequalities=540 adverse_lengths=[40, 37, 32, 25, 41, 39] four_deletions=35960 mass_component_orders=[[4, 17], [4, 19], [9, 12]] sharp_radius=1 limiting_route=24,2,1,0,10,29 PASS
```

Target SHA-256: `README.md` `3b3d9907cb3027fb6f08325b615192a532a4feed748d78315d6e60eaa7e127ac`; `audit.py` `f14d6f20d42a05c4974bc3b8f380056ecc28986ffb905c039cf9c11514a183bf`; `certificate.json` `f2bb6517f68e6554bd7648a4f1e41ef5af47c5e7b7428fe3efb97b0e95ecd4c1`; `expected.json` `c404af9ccda0085257855d8ab10686748f6cdb062433c1ebf78be0ab31f4bb8a`; `verify.py` `8c9098b20dc12ad120e056ab5610d6b8a9c2f20d0dd62e4674c3e68e162b480c`. Independent audit SHA-256: `d64babe5811949bdea0e7cf11f2f569d5e8ada28f8c388d4bb9b50bf1f04ecc7`. The finite JSON is an externally supplied input, checked rather than trusted as a verdict. The real-price and real-mass conclusions depend on the written adverse-corner and heavy-set arguments, not finite sampling. No claim is made for arbitrary metrics or mass on added subdivision vertices.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks about one-half balance by two shortest paths. [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give the weighted path-separability and face-separable background. A targeted primary-source search did not identify this exact price certificate; that does not establish historical priority. The pentakis-dodecahedral graph is known, while the explicit full-dimensional metric box and three-pair mass argument are the contribution assessed here. Its five-connectivity and lack of a facial half separator make it structurally different from the earlier triangular-patch family. A publication should retain the four-vertex repair as part of the theorem proof and state the restricted metric scope. The source and finite certificate are compact enough for further external peer review.

## Strengthening and improvement opportunities

**Proved sharpness of the common symmetric radius for these six fixed paths.** The target certifies half-width 1 around its ninety integer centers. For the first prescribed path \(P=(24,6,23,8,9,29)\), the five center prices are all 7, summing to 35. The disjoint-edge alternative \(Q=(24,2,1,0,10,29)\) has center prices \(8,9,7,7,14\), summing to 45. In a symmetric radius-\(r\) box, place the five \(P\)-edges at their upper bounds \(c_e+r\) and the five \(Q\)-edges at their lower bounds \(c_e-r\). Then

\[
\ell(P)=35+5r,\qquad \ell(Q)=45-5r.
\]

They tie exactly at \(r=1\); for every \(r>1\) sufficiently close to 1, \(Q\) is shorter and all prices remain positive. Thus radius 1 is the **largest common symmetric radius that preserves the displayed six-path certificate** at these centers. This does not show that the graph's all-mass half-separator property fails beyond radius 1: another path menu could work.

The next worthwhile classification is which nonuniform edge-price perturbations preserve some two-path mass certificate on this five-connected core. A proof would need a certified path menu or a counter-mass dual beyond the current adverse-corner box. The exact uniform-radius witness above does not determine that larger region.
