# Linear triangle-packing loss with a growing clique cell

Let `H` be an `n`-vertex mixed-template graph with at most `d` classes, each
of size at least `alpha*n`. Classes are cliques or independent sets and
cross pairs are complete or empty. Add a clique `X` of any size `0<=s<=n`,
complete or empty to each core class. Then

```text
nu*(H+X) - nu(H+X) <= K(d,alpha) n.
```

Here `nu*` is the full fractional edge-disjoint triangle-packing optimum.
The theorem rounds every feasible fractional packing, including all types
of triangles using zero, one, two or three vertices of `X`. It covers
`sqrt(n)<<s<<n`, where deleting the clique's internal edges cannot give a
linear error. Together with the prior independent-extension theorem, it
allows one cell of arbitrary vanishing size and either type, while the
other classes stay comparable.

This is a **complete author proof awaiting independent review**. The general
constant is existential through the accepted balanced-deletion lemma and
Keevash's generalized design theorem. The core remains comparable, and the
clique has one neighborhood type into it. Several unrelated small clique
cells and unrestricted class proportions are outside the theorem.

There is also an explicit consequence when `H` is triangle-free. Put

```text
B = 2^(d+2),  Q = 8B(11+d),  E = d(d+1)/2.
```

For every `n,s>=1` satisfying `s/n <= min(alpha/88,alpha/(16d))`,

```text
nu*(H+X) - nu(H+X) <= [7+6d+E(Q+1)] s.
```

This bound uses the **exceptional clique order** and has no unspecified
starting order. It uses classical all-order Kirkman triple-system existence,
coloring and integral flow; it does not require Keevash's theorem. The
constants are deliberately coarse. This package implements finite affine
design fixtures, not a practical all-order design constructor.

The classical inequality `tau<=2nu*` gives corresponding additive Tuza
bounds. Neither statement resolves Tuza's conjecture.

## Mechanism

Choose parallel classes of a Kirkman triple system on `s+O(1)` points and
delete the extra points. This packs the internal clique triangles while
leaving a nearly regular graph. Groups of proper edge colors realize the
triangles with two clique vertices; equitable recoloring distributes their
centers across the core and balances the consumed spokes.

An integral flow allocates the remaining spokes with exact uniform demand
at each exceptional vertex and bounded discrepancy at every core vertex.
Processing core-edge types in increasing demand lets dense matchings join
these spokes while avoiding earlier core edges. The resulting core deletion
has bounded discrepancy, so the accepted residual-profile lemma completes
the general case. All these steps and the explicit constants are proved in
[PROOF.md](PROOF.md). [SOURCES.md](SOURCES.md) distinguishes the new bridge
from the imported design, coloring and flow inputs.

## Reproduce

Python 3.11.2 was used. Only the standard library is needed. From this directory:

```bash
python3 check.py > /tmp/clique-extension-audit.json
cmp /tmp/clique-extension-audit.json AUDIT.json
PYTHONHASHSEED=123 python3 -O check.py > /tmp/clique-extension-optimized.json
cmp /tmp/clique-extension-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

[RUN.json](RUN.json) records the measured times and canonical audit hash.
[constructions.py](constructions.py) produces designs, recoloring paths,
integral spoke allocations and matchings. [coloring.py](coloring.py) reuses
the classical Vizing implementation from the accepted earlier package.
[check.py](check.py) independently reconstructs all relevant incidences and
checks every certificate entry.

The exact audit includes:

- affine Kirkman systems of orders 3, 9, 27 and 81, checking every pair and
  every parallel-class partition;
- 105 deleted-point clique profiles, including all padding sizes from zero
  to five, with 31,921 replayed equitable recoloring paths;
- 5,307 flow-rounding instances from exhaustive small bipartite graphs,
  verifying every exact fractional column floor and ceiling;
- 2,285 equitable-coloring instances, including every labeled simple graph
  through five vertices with two palette choices and 87 larger seeded graphs,
  with 6,217 recoloring paths;
- **212,110 literal triangles** in three integrated constructions with
  clique, two-clique and bipartite cores, including near-saturated spokes,
  loop edge types, 120 dense-matching checks and 146 matching repairs;
- the exact residual core-capacity identities with nonzero preserved
  core-only fractional masses, deletion-degree bounds and type discrepancies;
- 144 parameter endpoint checks and five exact fractional profiles with
  superlinear internal exceptional-edge count; and
- ten malformed certificates or infeasible requests, all rejected.

The integrated fixtures meet the explicit elementary size and cutoff bounds.
They do not claim to exceed the unknown dense-completion threshold. The
largest compressed profile has core order `20,000,000,000,000,000`; only its
fractional capacities and explicit parameter inequalities are checked. No
packing of that order is materialized. Literal certificates and recoloring
traces are regenerated in memory; only source and compact summaries/hashes
are committed.

These are author checks, not independent review. They do not prove the
imported universal design theorems or formalize the argument. No solver,
floating point, omitted certificate or private input is required.
