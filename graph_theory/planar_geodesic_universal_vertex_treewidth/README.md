# Two geodesic half separators from a universal vertex

**Prior work:** Diot and Gavoille's 2010 Proposition 1(1) already covers
this corollary via its general treewidth-three theorem. See [PROOF.md](PROOF.md)
for the explicit specialization and citation. This note does not claim a
new path-separability class.

This contribution addresses the unweighted half-balance question in
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

**Theorem.** If a finite simple graph `G` has a universal vertex `u` and
`tw(G-u) <= k`, then for every nonnegative vertex weighting, a union of at
most `ceil((k+2)/2)` shortest paths in the original graph leaves components
of at most half the total weight. In particular, **two shortest paths suffice
for every planar graph with a universal vertex**, at every order, because
deleting that vertex leaves an outerplanar graph of treewidth at most two.

The mechanism is explicit. A centroid bag in a width-`k` tree decomposition
of `G-u` balances the remaining vertex weights and contains at most `k+1`
vertices. One path is an edge from `u` to a bag vertex. Pair the other bag
vertices: an adjacent pair is covered by its edge, and a nonadjacent pair
by the geodesic through `u`. [PROOF.md](PROOF.md) gives the full argument.

The bound of two is sharp even in the planar class: `K_2 join P_{n-2}`
needs two for every `n >= 7`. Those maximal planar graphs also have no
half-balanced facial border, so this class extends beyond the
face-separable family proved in
[Diot–Gavoille (2009)](https://dept-info.labri.fr/~gavoille/article/DG09a).
No literature priority claim is made.

## Reproduction and trust boundary

The theorem is proved in [PROOF.md](PROOF.md); its proof needs no software or
generated data. A finite sanity check independently enumerates the twelve
labeled graphs formed by joining a universal vertex to at most three
vertices, and tests the sharp family at orders 7 through 12. With Python
3.11.2 or later and no external packages, run:

```bash
python3 verify.py
```

Expected output:

```json
{"local_failures": 0, "local_labeled_cases": 12, "one_path_sharp_orders": [7, 8, 9, 10, 11, 12]}
```

The finite check confirms only the local path-cover cases and small sharp
examples. It is not used to justify the weighted centroid argument, the
outerplanar treewidth bound, or the claim for arbitrary order.
