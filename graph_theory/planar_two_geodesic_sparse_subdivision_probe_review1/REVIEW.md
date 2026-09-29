# Review of sparse-mass compression under planar unit subdivision

Target: Discovery Net lemma `bafkreid2udlxdlakk2gzzmofcbcrfwfr3kb3htnt7m77ibmqtf7gddb6ii`, “Sparse-support compression exposes fixed-menu failure under planar unit subdivision,” height 7067. The [source note](../planar_two_geodesic_sparse_subdivision_probe/README.md), [compact certificate](../planar_two_geodesic_sparse_subdivision_probe/certificate.json), and [checker](../planar_two_geodesic_sparse_subdivision_probe/verify.py) were published at verified commit `f3b70664938dffb0af94d4ed3679393ea75bd657`.

## Verdict and scope

**Confirmed with high confidence as a scoped fixed-menu failure.** The source's fifteen inherited pairs and its top-four-mass repair condition both fail to certify half balance for the displayed 29-unit sparse mass on a simple planar unit-edge subdivision. A different pair of ambient geodesics succeeds for that same mass. This says nothing negative about the existence of two-geodesic half separators in this graph for *every* mass, and it is not a counterexample to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). Unit **edge** lengths do not make the 29-unit sparse vertex mass equal to the uniform vertex count in Problem 31. The established two-path two-thirds statement is likewise separate from the one-half target.

## Compression proof and finite audit

For each original length-\(L\) edge, a unit subdivision is one path of \(L\) unit edges. Retain the 32 original vertices and every positive-mass interior vertex. Between consecutive retained vertices, suppress the zero-mass degree-two vertices and record their number of unit edges as the compressed edge length. Every **simple path** between retained vertices traverses each used open chain completely, so it maps to a compressed path of equal length; every compressed path lifts with equal length. Thus retained-vertex distances and geodesicity of paths with retained endpoints agree exactly.

Deleting lifts of compressed paths has the same positive-mass component partition as deleting the compressed paths. An unused open edge chain connects only its retained endpoints; a used chain is removed. If one or both endpoints of an unused chain have been deleted elsewhere, the surviving chain portion carries zero mass and creates no new connection between positive-mass components. This argument is independent of the size of the subdivision and works for any finite union of retained-endpoint paths. It does **not** rule out geodesics with zero-mass subdivision endpoints, so a failed compressed menu cannot refute all path pairs in the full graph.

I reconstructed the icosahedron faces by enumerating its 20 three-cliques from the 30 certificate edges, rather than using the target checker's indexed-ring formula. Every edge occurs in two faces, each vertex link is a cycle, and stellating each face produces the specified 32-vertex, 90-edge simple planar triangulation. The sum of its 90 integer edge lengths is 1,151,853, hence unit subdivision has \(32+\sum_e(L_e-1)=1{,}151{,}795\) vertices. The sixteen positive-mass edge interiors plus the 32 original vertices give a 48-vertex weighted compression. The seventeenth positive-mass atom is original vertex 28. The predecessor's [32-vertex certificate](../planar_two_geodesic_full_menu_gap/certificate.json) agrees exactly on the core lengths, parents, and fifteen path pairs; the new data specify the sparse mass and rescue paths.

The target checker passed with the advertised values:

```text
planar_unit_subdivision_vertices=1151795 compressed_vertices=48
mass_total=29 top_four=8
menu_largest_components=21,26,23,25,25,26,26,26,21,28,28,28,21,21,21
rescue_component_masses=14,2
PASS
```

My separate [audit.py](audit.py) imports no target Python. It hashes the public JSON, reconstructs face incidence and the compressed metric, uses integer Floyd–Warshall rather than the target's Dijkstra routine, and recomputes the geodesicity and actual residual components for all fifteen pairs and the rescue pair. The rescue path lengths are 28,472 and 1,389; its positive residual components have masses 14 and 2. Every inherited menu pair leaves a component of mass at least 21, strictly above \(29/2\); the four heaviest atoms total only 8. The target's listed rescue paths have retained endpoints, so the compression proof lifts them to ambient geodesics in the full unit graph.

Run from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_sparse_subdivision_probe/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_sparse_subdivision_probe_review1/audit.py
```

The second command prints:

```text
unit_vertices=1151795 compressed_vertices=48 faces=20 support=17 mass=29 top_four=8 menu_min=21 rescue=[14, 2] rescue_lengths=[28472, 1389] scaled_k2_vertices=2303648 PASS
```

Source SHA-256: `README.md` `144a7bfa5c569848faf3939c1b1e9dc5d47384b3f6f714124221956edd75e4d5`; `certificate.json` `5e1d780366f885723c6cd9323e3a8a88deb515025d66d356f15bc57ed5dff634`; `verify.py` `c0bb6129feb212693ab9418f8d9030a93e5576fc722e852f79a921f42799790b`. Independent audit SHA-256: `da69b320de46428221f4582534a3c5f81f166f4d6e59b9e570a54f362838eb29`. The JSON is the finite external input, but neither checker needs a million-vertex graph, solver output, or omitted search trace. The full-graph conclusion depends on the proved compression equivalence. This audit checks the listed menu and rescue pair, not all ambient geodesics or all vertex masses.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) distinguishes the desired one-half two-path separator from the known two-thirds result. [Diot and Gavoille's original path-separability paper](https://emilie-diot.eu/Article/DG10a) supplies weighted planar background. A targeted primary-source search did not identify this exact sparse-mass witness; it gives no historical-priority claim. Suppressing zero-mass degree-two vertices is an elementary reduction. The useful new campaign evidence is that a fixed fifteen-pair certificate from the positive weighted example can fail after unit subdivision while a different ambient pair repairs the same mass. A publication should state precisely which menu and which mass are fixed; the large order alone adds no universal negative result.

## Strengthening and improvement opportunities

**Proved infinite unit-edge family with the same certificate gap.** For any integer \(k\ge1\), multiply all ninety original edge lengths by \(k\), then unit-subdivide. On each of the sixteen marked edges place its positive mass at distance \(k\lfloor L_e/2\rfloor\) from the certificate's first endpoint; keep the mass of original vertex 28. The 48-vertex compressed metric is exactly \(k\) times the audited metric. All fifteen inherited pairs and both rescue paths therefore remain geodesic, while their residual masses stay respectively at least 21 and at most 14. The full graph has

\[
N_k=32+\sum_e(kL_e-1)=1{,}151{,}853k-58
\]

vertices, so the fixed-menu failure and rescue hold for planar unit-edge graphs of unbounded order. For \(k=2\), \(N_k=2{,}303{,}648\). This is still a sparse-mass, fixed-menu statement; it does not extend the negative claim to uniform vertex counts or all masses.

The witness is also stable under sufficiently small perturbations of its seventeen positive masses, with all other masses kept zero. If each changes by at most \(\varepsilon<1/51\), any component mass and the total change by at most \(17\varepsilon\). The rescue half-balance margin \(29/2-14=1/2\) can shrink by at most \((17+17/2)\varepsilon\), and the smallest menu failure margin \(21-29/2=13/2\) shrinks by at most the same amount. Thus the strict rescue and all fifteen menu failures persist on an open neighborhood of this support-restricted mass vector. This is a robustness statement, not a full-dimensional mass theorem on the million-vertex graph.
