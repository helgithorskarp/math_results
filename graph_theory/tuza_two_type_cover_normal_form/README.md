# Exact cover normal form for two-neighborhood split graphs

Every split graph with at most two active independent-side neighborhood
types has a minimum triangle edge cover whose surviving **clique core** is
bipartite. An explicit three-expression extremal formula gives an
`O(k^3)` exact algorithm, uniform in clique order `k` and both multiplicities.
An infinite family with three types makes this boundary sharp.

This is a proved structural reduction for the covering side of Tuza's
problem. **The inequality `tau <= 2 nu` for the unbounded two-type class
is not proved here.** Whole-residual bipartiteness is not asserted either.

- [Proof and exact formula](PROOF.md), including the sharp three-type
  obstruction and a packing certificate for the missing rectangle.
- [Exact algorithm and certificate reconstruction](cover.py).
- [Independent regression checks](verify.py).
- [Expected compact output](EXPECTED.json).

## Reproduce

From this directory, with Python 3.10+ and no third-party packages:

```sh
python3 verify.py
python3 cover.py 17 13 9 11 1000000007 11
```

The second command supplies the counts
`(|S\T|, |T\S|, |S intersect T|, |C\(S union T)|, m, n)`.
Its answer is `tau=700`, with a compact optimal-cover certificate. The
implementation never expands the independent-side multiplicities.

The verification command checks 2,016 small cover instances against an
independent clique-core enumeration, including 280 direct full-graph
triangle-hitting checks, 25 nonempty rectangle packings, and rejection of
four malformed certificates. Its record digest is
`037a792dfa2f10fcd842568e7394abf05b8db7fcc3011431e85935d78a4e8224`.
Three illustrative members of the **proved** three-type obstruction have
maximum triangle-free/core-cut values `(9,8)`, `(13,12)`, `(21,20)`.

These are regression tests, not a bounded-order substitute for the proof.
No solver, external dataset, bulky certificate, or unpublished dependency
is required. Scope and primary-literature comparisons are in the proof.

Tested with CPython 3.11.2 on 2026-09-22; the complete regression command
finished in under one second on the research host. Run without `-O`, since
the checker uses Python assertions.
