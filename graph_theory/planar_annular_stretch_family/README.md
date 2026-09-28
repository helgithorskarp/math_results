# Half-balanced geodesics in stretched capped cylinders

For circumference **6 or 8** and **every height at least 2**, the alternatingly
triangulated capped cylinder has a half-balanced separator consisting of at
most two ambient shortest paths for every nonnegative real vertex-mass
assignment in either of these metric regimes:

1. Cap, horizontal, and diagonal edges have length 1. Each vertical edge
   independently has any real length at least 1, or is deleted.
2. All vertical edges have one common real length `t > 0`; every other edge
   has length 1.

The [proof](PROOF.md) defines the graph exactly. Interior median rows are
isometric cycles. At either boundary, a nonexpansive map to a 14- or 18-vertex
graph supplies three candidate separators, each containing at most two
geodesics. A short component-intersection argument proves that one succeeds.
The finite boundary paths avoid every edge whose cost can change, so they
lift to the whole metric family. A level potential handles `0 < t <= 1`.

This rules out these construction families as weighted counterexamples to
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It does not settle that problem, assert arbitrary edge lengths, or assert a
result for larger circumferences. The proof also shows why this particular
two-row boundary reduction fails at every even circumference at least 10.
That failure is a limitation of the reduction, not a planar counterexample.

## Reproduce

From the repository root, with Python 3.11 or later and no external packages:

```sh
python3 graph_theory/planar_annular_stretch_family/verify.py --check
```

The verifier reconstructs the graphs from their edge rule, checks every
certificate path by ambient BFS and an independent coordinate lower bound,
computes components by union-find, and checks the anchored intersection
contradiction. It also constructs and audits 882 sample separators with exact
integer Dijkstra distances, through height 32 and order 258. These samples
exercise reflection, contractions, deleted vertical edges, independently
stretched vertical edges, and common rational lengths below 1. Six invalid
certificate controls must be rejected.

Expected output is [expected.json](expected.json): `status: PASS`, three
candidate separators and five distinct paths in each boundary kernel, 882
checked sample witnesses, and six rejected controls. The SHA-256 of
[certificate.json](certificate.json) is
`51d142c536bb8b630d1eaed595c1ec020697b527927355474954c94ea0a96e7e`.

The universal real-mass, real-length, and unbounded-height claims follow from
the proof; finite sampling is only a consistency check. The only finite
certificate consists of the ten explicitly listed boundary paths. No solver,
external enumeration, or private input is needed for verification. Discovery
used exact mass constraints and all tied boundary geodesics; the published
checker does not depend on that search.

The common short-vertical argument is the weighted version of the earlier
[mesh level-potential construction](../planar_geodesic_mesh_obstructions/PROOF.md).
The anchored boundary proof adapts the component-intersection method used in
the earlier [fixed-metric certificate](../planar_weighted_heavy_component_certificate/README.md).
No independent review or literature priority is claimed here.
