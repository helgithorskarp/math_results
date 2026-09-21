# Iterated Mycielski clique complexes: an exact Stirling wedge law

For every finite connected K4-free graph G with at least two vertices, we
compute the homotopy type of its ordinary Mycielski iterates:

    Cl(M^k G) ≃ Cl(G) ∨ R_k circles ∨ Q_k two-spheres.

Both multiplicities have explicit nonnegative Stirling-number formulas in
six elementary statistics of G. This yields the exact asphericity boundary:

- The first iterate is aspherical iff every vertex link is a forest.
- The second is aspherical iff every edge belongs to at most one triangle.
- Every fixed iterate k>=3 is aspherical iff G is triangle-free.

Every positive case collapses to a graph, as does every simplicial subcomplex.
The bound three is sharp already for G=K3, whose third iterate is a wedge of
56 circles and six two-spheres. This is an abstract clique-complex theorem;
it does not resolve Whitehead's general conjecture.

Read [PROOF.md](PROOF.md) for the complete universal argument and
[SOURCES.md](SOURCES.md) for attribution and the literature boundary.

Reproduce from this directory with CPython 3.11+, standard library only:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands compare every field with `expected.json` and print
`status: pass`. `python3 verify.py --emit` regenerates the compact output.
The audit covers 709 connected K4-free labelled graphs, direct chain ranks,
legal collapse traces, all three failure times, a torsion-sensitive fixture,
and a K4 control that demonstrates why the dimension hypothesis is needed.

`construct.py` exposes `statistics(n, edges)`, `wedge_counts(stats, k)`,
`first_failure(stats)`, and `mycielski(n, edges)`. Edges are canonical pairs
0<=u<v<n; loops, duplicate edges, disconnected and non-K4-free inputs are
rejected. `collapse_trace` supplies triangle/free-edge removals when the
peeling procedure succeeds; failure is not a general asphericity verdict.

The finite audit corroborates the written homotopy proof. It is not an
independent review, formalization, or inference of arbitrary homotopy type
from Betti numbers. No solver, floating point, external data or unpublished
certificate is required.
