# Barycentric triangle packing as a characteristic systole

Let `T` be a finite connected closed triangulated surface, with `f` triangular
facets, and let `G` be the graph of its barycentric subdivision. Write `nu(G)`
for maximum **edge-disjoint** triangle packing and `tau(G)` for minimum
graph-edge triangle covering.

The exact deficit has the following topological description:

```text
tau(G) = tau*(G) = nu*(G) = 3f,
tau(G) - nu(G) = min{|X| : X is a mod-2 edge cycle, [X] = PD(w1(T))}.
```

For the real projective plane this is its ordinary edgewidth `s`, the length
of a shortest noncontractible graph cycle. Consequently:

* `nu(G) = 3f - s`, with an explicit polynomial algorithm returning an optimal
  packing, a shortest essential cycle, and an optimal cover.
* `tau(G) / nu(G) <= 10/9`, with equality **exactly for six-vertex projective
  plane triangulations** (`f=10`, `tau=30`, `nu=27`).
* `tau(G)-nu(G) <= sqrt(2f+4)`. The square-root order, and the corresponding
  `f^(-1/2)` relative gap, cannot be improved uniformly.

[PROOF.md](PROOF.md) proves the claims. The packing/orientation identity is
prior campaign work; the characteristic-class interpretation, its constructive
projective-plane application, and the sharp constant are the present result.
Shortest-cycle algorithms, the external systolic bound, and the small flag
complex classification are prior literature. See [SOURCES.md](SOURCES.md).
No priority claim is made beyond the sources searched.

This is a theorem with an ordinary mathematical proof and exact corroborating
code, not a formalized proof or a new exhaustive classification. The sharp
constant uses Katzman/Adamaszek's published classification through eleven
vertices; this package checks its four supplied records, not its completeness.
The formula for a general surface uses the **specified characteristic class**:
on the supplied Klein bottle the gap is four although an essential triangle
exists. On the torus the gap is zero.

Run from this directory with CPython 3.11 or later; no dependencies or network:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

The checker independently compares homology-cover optimization with exhaustive
orientation supports on small inputs; reconstructs and verifies literal
packings; checks the four imported graphs; and tests sphere, torus, Klein
bottle, malformed inputs, and all two-variable binary linear systems.
[expected.json](expected.json) includes compact cycles, cocycles, and packing
witnesses. The six-vertex and midpoint-refined projective planes have
`(f,s,nu,tau)=(10,3,27,30)` and `(40,5,115,120)` respectively.

A source countercheck matters here: the standard midpoint-refined
hemicosahedron has an essential five-cycle. Thus the `3k` value stated for
this grid family in the introduction of Liu–Pelsmajer's manuscript fails at
`k=2`. We provide its exact certificate and use a separate elementary argument
for the order-sharpness result. This does not refute their general upper bound.

Scope stops at closed abstract simplicial surfaces and this projective-plane
optimization theorem. There is no claim here about arbitrary graphs, complexes
with singularities or boundary, or a faster general surface algorithm.
