# Linear triangle-packing loss under independent extensions

Let a graph `H` have `n` vertices in at most `d` mixed classes, each of size
at least `alpha*n`. A class is a clique or an independent set; cross pairs
are complete or empty. Add an independent set with at most `r` neighborhood
types, each complete or empty to every core class, with **arbitrary type
sizes**. The resulting graph `G` satisfies

```text
nu*(G) - nu(G) <= K(d,r,alpha) n.
```

Here `nu*` is the full fractional triangle-packing optimum and `nu` is the
maximum number of edge-disjoint triangles. The bound uses the **core order**
`n`, even when the independent extension is arbitrarily larger. There is no
lower bound on the independent-class sizes or positive profile coordinates.

This is a complete author proof awaiting independent mathematical review.
The constant `K` is existential. The proof has an asymptotic construction
and includes all smaller core orders by enlarging the constant; it does not
supply a practical universal starting order. See [PROOF.md](PROOF.md).

The core classes must remain comparable, and the added vertices must form
one independent set. Small clique classes and edges within the exceptional
set are excluded. This is not an unrestricted bounded-type theorem, a result
for every split graph, or a resolution of Tuza's conjecture.

## What handles small independent classes

For each added class `I_h`, the core edges used by its triangles form a
properly edge-colored graph: each color is the matching assigned to one
independent vertex. We construct these core-edge graphs with prescribed
balanced type degrees while avoiding all earlier ones. Scaling by
`1-(d+2)/s_h` costs only `O_d(n)`, and leaves enough colors for the `s_h`
vertices. Small edge-type counts cost only `O(s+1)` each when discarded.

The union of these graphs has maximum degree at most the small extension
size `s`, but its type-degree discrepancy is bounded by `r`. A new
balanced-deletion rounding lemma then completes the core with linear loss.
Its sparse swaps preserve every vertex-pattern role count while avoiding
the existing core edges. Dense completion uses Keevash's generalized partite
family theorem; the full specialization is included in
[DENSE_COMPLETION.md](DENSE_COMPLETION.md).

A finite hierarchy separates the added class sizes into large classes,
which join the comparable core, and small classes handled by the construction.
The thresholds are fixed before the input; no compactness inference across
vanishing class sizes is used.

## Exact multiplicity reduction

For **any** `n`-vertex core, replacing every independent neighborhood-type
size `s_h` by `min(s_h,n)` preserves all three parameters:

```text
maximum triangle packing, full fractional triangle packing,
minimum edge triangle cover.
```

The proof uses classical Vizing coloring and an elementary cover exchange.
For packing, the cap cannot uniformly be reduced to `n-1`, as odd complete
cores of order at least three show. These are elementary reductions using
classical tools, not claimed new general coloring or complete-split results.

## Reproduce

Python 3.11.2 was used. All code uses only the standard library. From this
directory:

```bash
python3 check.py > /tmp/independent-extension-audit.json
cmp /tmp/independent-extension-audit.json AUDIT.json
PYTHONHASHSEED=123 python3 -O check.py > /tmp/independent-extension-optimized.json
cmp /tmp/independent-extension-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

[RUN.json](RUN.json) records timings and the audit hash.
[constructions.py](constructions.py) constructs degree realizations and
classical fan/Kempe edge colorings. [sparse_avoid.py](sparse_avoid.py) repairs
sparse components while avoiding a fixed graph. [check.py](check.py)
contains all deterministic fixtures and separately checks the certificates
from their edge, color, triangle and role definitions.

The exact audit checks:

- proper colorings of all 33,868 labeled graphs through six vertices and
  210 larger seeded graphs, exercising both Kempe endpoint cases;
- 30 near-regular degree realizations avoiding forbidden edges, including
  22 with zero targets and both augmentation cases;
- 79,778 literal exceptional triangles in five instances with equal and
  unequal classes, distinct neighborhoods, a dropped small coordinate,
  a discarded small independent class, and saturated spokes;
- 1,811 replayed sparse swaps avoiding 5,045 previously used core edges,
  followed by a disjoint 1,009-edge remainder;
- 2,392 compressed core-role intervals over 148 profiles on all 74 mixed
  templates with at most three classes, at two exact scales;
- 21,806 class-hierarchy endpoint/midpoint tuples using illustrative
  rational tolerances, and multiplicity-cap coloring/reweighting witnesses;
- 576 direct minimum triangle-cover computations on 288 pairs of original
  and capped expanded graphs;
- twelve invalid constructions, all rejected.

The compressed profiles reach core order `3,000,003,000,000`; they check exact
identities, not materialized packings of that size. All literal certificates
and sparse traces are regenerated in memory and checked entry by entry.
Only compact inputs, counts and hashes are committed; no omitted data,
solver, floating point, or private input is required.

These are author audits of finite constructions. They do not implement or
prove Keevash's universal existence theorem, formalize the argument, compute
its thresholds, or constitute independent peer review. Classical coloring
and prior graph contributions are credited in [SOURCES.md](SOURCES.md).
