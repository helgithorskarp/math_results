# A complete common-pair assembly gate for one EI17 realization

Every collection of congruent copies of the exact 17-point realization `P` defined
below, with **two distinct fixed points occurring as vertices in every copy**, has
a four-colourable full unit-distance graph. Reflections, endpoint reversals,
different choices of the two seed vertices, further vertex coincidences, and
unit-distance contacts between different interiors are all included. Consequently
no subgraph of any such assembly can meet the at-most-508 five-chromatic target.
Every nonempty full assembly actually has chromatic number four because it
contains a copy of `P`.

The first completion obtained by adjoining both intersections of the unit circles
about every eligible pair of vertices of `P` is also four-chromatic. It has at most
283 vertices, counting the 17 originals and 266 intersection labels before
coincidences are identified.

These are exact computer-assisted negative construction results. The common-pair
statement covers arbitrary numbers of copies and arbitrary positions of the two
common vertices. It concerns this **one certified realization**, not every
realization of the abstract EI17 graph. Assemblies with only one globally common
vertex, pairwise overlaps with no globally common pair, and other seeds are
outside the theorem. We do not begin a larger circle-completion or same-seed
assembly ladder here. No five-chromatic graph or record improvement is claimed.

## Exact seed and sources

The seed has 17 vertices, the 31 edges in `seed_edges.json`, and coordinates equal
to the unique solution of its unit-edge equations in the following rational box.
Vertices 10 and 16 (zero-based labels throughout this package) are pinned at
`(-1,0)` and `(0,0)`. Each of the other 30 coordinates is within `10^-18` of its
rational midpoint in `seed_midpoint.json`. The definition is exact; decimal
midpoints are not asserted to be the exact embedding.

The edge list and midpoint data are transcribed from Section 1 and Appendix A of
[Silva Filho, arXiv:2607.19995](https://arxiv.org/html/2607.19995). They supply a
numerical starting point only. We establish existence, uniqueness, distinctness,
faithfulness, triangle-freeness and chromatic number independently. No minimal
polynomial, coordinate-field, Galois-group or numerical-certification assertion
from that manuscript is used. The original small triangle-free graphs are due to
Exoo and Ismailescu, *Small Order Triangle-Free 4-Chromatic Unit Distance Graphs*,
Geombinatorics 26(2), 49–64 (2016); see the
[publisher's issue index](https://geombina.uccs.edu/past-issues/volume-xxvi).

The comparison target remains the 509-vertex example in
[Parts, arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also identified as the
record in [Haugland, arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4),
Section 1. These primary sources were checked on 2026-09-07. We make no priority
claim for the common-pair certificate method.

## Reproduce

From this directory, with Python 3.11 or later, no third-party packages:

```sh
python3 verify.py --check-expected
python3 controls.py
python3 -O controls.py
```

`verify.py` verifies the proof, including root existence; it does not run SAT or
read an external graph dataset. The principal expected results are:

| Check | Result |
|---|---:|
| Seed vertices / faithful unit edges | 17 / 31 |
| Free coordinate variables | 30 |
| Source pairs covered | 136 |
| Disjoint groups of squared-distance intervals | 89 |
| Orientations and reflections across all groups | 544 |
| Total frame labels, before coincidences | 9,248 |
| Largest group's labels | 2,108 |
| Frame-label pairs checked | 2,547,824 |
| Circle-completion labels / pairs checked | 283 / 39,903 |
| Eligible pairs of circle centres | 133 |

The 89 groups are a **certified partition into separated interval ranges**.
We do not need or claim that all pair distances inside each group are exactly
equal. Similarly, labels may coincide; we do not use numerical deduplication to
claim exact support sizes or exact edge counts for the assembled graphs.

`fan_certificate.json` contains one group of source pairs and one colour word for
each interval range. For each pair `(i,j)`, enumerate `(reverse,mirror)` in the
order `(false,false), (false,true), (true,false), (true,true)`, followed by seed
vertices 0 through 16. The word has one character `0`, `1`, `2` or `3` per label.
Its file SHA256 is
`063f7db957473b19abbe773cbb74f12d471e46779fba1e118731f8eb56a47d09`.
`circle_word.txt` first colours the seed, then both circle intersections in
lexicographic pair order and sign order `-1,+1`.

`expected.json` gives all 89 group summaries and exact outward margin summaries.
`PROOF.md` explains the general transfer lemma and every enclosure obligation.
`SHA256SUMS` identifies the compact source and certificate files.

## Optional discovery reproduction

With `python-sat==1.9.dev15` (tested with Python 3.12.14, CaDiCaL 1.9.5):

```sh
python search.py --output out
```

This reconstructs the shipped words byte-for-byte in the recorded environment.
The SAT variables are four Boolean colour indicators per numerically deduplicated
vertex. At least one is true, and each numerical edge excludes a common colour;
taking the first true indicator produces a proper colouring. One vertex is pinned
to colour zero. Each query has a 300,000-conflict cap. Floating-point tolerances
`10^-9` for length groups and `10^-8` for point and unit-edge detection only guide
discovery. A SAT result, tolerance grouping, or numerical coincidence is never
proof evidence: the published words are checked against exact enclosures of all
label pairs.

## Validation and trust boundary

`seed.py` proves the root with a rational inverse-Jacobian contraction bound and
checks the inverse identity exactly. Its exhaustive three-colour search visits 84
nodes. A separate method in `controls.py` enumerates all 131,072 vertex masks and
finds that all 1,181 independent sets leave non-bipartite complements, independently
excluding a three-colouring.

`intervals.py` uses integer endpoints over `2^100`, exact integer products, outward
floor/ceiling division, and integer square roots. `verify.py` checks same-colour
pairs exclude squared distance one and different-colour pairs cannot coincide.
The latter condition is essential: it makes the words descend to the actual
geometric union even when two labels represent the same point.

Controls compare 256 pairs of interval fixtures with exact rational arithmetic,
check 33 square-root boundary cases, and reject 12 malformed or corrupted inputs,
including a perturbed seed midpoint, overlapping pair groups, missing/repeated
pairs, unit-distance colour collisions, and differently coloured duplicate
points. Normal and optimized-Python controls have identical results. The final
checker trusts Python integer/Fraction arithmetic and the proved interval formulas;
it uses no floating-point operation, SAT verdict, guessed exact equality, external
binary, or unprovided algebraic input. This is internal validation, not independent
peer review.

Only source and compact certificates are published. Numerical coordinates for
all generated supports, approximate edge lists, exploratory logs and local graph
queries remain private. The earlier E477 and mixed Moser/L10 results are preserved
in their existing directories; this package changes none of them. The teammate's
fixed Parts realization classification is separate context, not a dependency.
