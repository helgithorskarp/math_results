# A 375-vertex small-triangle forcing gadget

The explicit graph **T375** in this package has **375 distinct vertices and
1,661 unit edges**. It has a proper four-colouring, but **no proper
four-colouring makes its marked equilateral triangle of side `1/sqrt(3)`
monochromatic**. An exhaustive standard-library checker proves this conditional
obstruction and checks the supplied unpinned colouring.

This is an actual finite forcing graph, obtained by reducing the
Exoo–Ismailescu construction. It supplies the finite mechanism sought after the
[previous 1,024-vertex synthesis pilot](../hadwiger_nelson_finite_centre_synthesis/README.md)
failed that property. The supports differ; the earlier negative certificate
remains valid. This is **not a 375-vertex five-chromatic graph** or a record
improvement. The explicit composition below gives a non-four-colourable
unit-distance graph on **at most 795,753 vertices**, far above the 508 target.
Neither the forcing property nor the composition method is claimed as new;
no smallest-known forcing-gadget claim is made.

## Coordinates and provenance

[Exoo and Ismailescu, arXiv:1805.00157v1](https://arxiv.org/abs/1805.00157v1)
give a 627-vertex graph with this forcing property in Claim 4.1. Their appendix
lists 109 orbit representatives. We reproduce the numerical tables as
`appendix.json`, `g40.json` and `g49.json`, with their coordinate convention:

```
[a,b,c,d] = ((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

Generate the reference support using rotations by `2pi/3` and reflection in
the **y-axis**, as described in Section 4. Explicitly the operations are

```
R(a,b,c,d) = ((-a-c)/2, (-b-3d)/2, (3a-c)/2, (b-d)/2),
S(a,b,c,d) = (-a,-b,c,d).
```

The appendix's wording instead names reflection axes including `y=0`. That
literal x-axis convention produces 627 points but only 1,935 unit edges and
does not contain the stated G51 seed. The y-axis convention produces 627
points, 2,982 unit edges and the G51 seed, agreeing with Section 4. Our reference
graph and its forcing property are verified independently of this ambiguity.
The source PDF hash and extraction locations are in `provenance.json`.

Reference labels 0, 1 and 2 are respectively
`[0,0,12,0]`, `[-6,0,-6,0]`, `[6,0,-6,0]`. Sort all other distinct coordinate
quadruples lexicographically. `certificate.json` lists the 375 retained labels
in increasing order; the induced graph is T375 and its first three labels are
the marked triangle. All vertex pairs at exact unit distance are edges.

One deterministic deletion pass tested the 624 nonterminal reference vertices
in ascending order of `(original degree, reference index)`, retaining a
deletion precisely when the monochromatic-terminal formula remained UNSAT.
It removed 252 vertices in 9.23 seconds. No further order, seed or reduction
phase was run. The positive deletion history remains private and reproducible;
it is not required for the published forcing proof. The unpinned colouring and
retained labels are the compact certificate. We make no global-minimum claim.

## Exact forcing proof

`geometry.py` is the producer. A squared distance has numerator

```
3 da^2 + 11 db^2 + dc^2 + 33 dd^2 + 2(da db + dc dd) sqrt(33),
```

over 1296. This is one iff its rational coefficient is 1296 and its radical
coefficient is zero. Distinctness follows from independence of the radicals.

The verifier imports neither this producer nor the SAT search. It constructs
the orbit using complex multiplication in the independent bit-indexed radical
basis for `Q(sqrt(3),sqrt(11),sqrt(247))`. It recomputes the 196,251 reference
point pairs and 70,125 retained pairs. The extra radical is used only for the
later composition; T375 itself lies in `Q(sqrt(3),sqrt(11))^2`.

It then exhausts proper four-colourings with vertices 0, 1 and 2 fixed to
colour 0. Fixing their common colour loses no monochromatic case, by a global
permutation of colour names. Available colour sets start with all four
colours, except at the pins. A singleton removes its colour from neighbours;
an empty set rejects that branch. Otherwise the search branches on a vertex
with the smallest available set, breaking ties by degree and label. It tries
every already-used colour and one representative unused colour. All unused
colours are interchangeable: no assigned vertex or initial pin distinguishes
them, and the constraints only test equality. This symmetry reduction loses
no solution. Each branch assigns another vertex, so the finite search
terminates. Exhausting every branch proves impossibility.

The reference forcing check visits 2,131 nodes; the T375 check visits **735
nodes, with 367 conflicts**, and returns no colouring. Every edge of the
separately supplied unpinned colouring is checked directly. No SAT result or
proof trace is trusted in these final claims. The generic radical arithmetic,
colour search and written completeness argument are the computational trust
boundary; no proof-assistant formalization or external-author review is claimed.

## A fully specified finite composition

Put `d=sqrt(11/3)`. The following two source properties are independently
rechecked on the paper's small coordinate tables, rather than imported as
unverified solver claims:

1. **G40:** 40 vertices, 82 unit edges and 59 pairs at distance d. If a proper
   four-colouring makes every one of those pairs bichromatic, its marked
   endpoints O and V, at distance `8/3`, have the same colour. The checker adds
   those 59 inequality constraints and pins O and V to different colours. Its
   exhaustive search returns no colouring in 50 nodes. These additional
   inequalities are conditional constraints, not claimed unit edges.
2. **G49:** 49 vertices and 180 unit edges, with marked endpoints P and Q at
   distance d and 18 equilateral triangles of side `1/sqrt(3)`. If P and Q have
   the same colour, at least one of those triangles is monochromatic. The
   checker pins P and Q equally and forbids monochromatic triangles. A
   triangle with two equally coloured vertices removes that colour from its
   third vertex. Exhaustive branching returns no colouring in 825 nodes.

Rotate a copy of G40 about O by the angle with cosine `119/128` and sine
`3sqrt(247)/128`. These numbers have squared sum one. The two images of V are
unit distance apart, since

```
2(8/3)^2 (1 - 119/128) = 1.
```

The union has 79 distinct vertices. For each of the 118 inherited d-pairs
(59 in each copy), attach an isometric copy of G49 along P,Q. For each of its
18 small triangles, attach an isometric copy of T375 along the three marked
vertices. Use the unique orientation-preserving pair map, and the triangle
map with a reflection if needed. `assembly.py` defines these maps exactly.
Its streaming `vertices(forcer_points)` function specifies the full finite
point multiset; take its set of distinct points and all unit-distance edges.
Streamed coordinates are physical coordinates times 36, in the radical basis
used by `radicals.py`.

Suppose this union had a proper four-colouring. Each attached T375 forbids its
triangle monochromatic. Each G49 implication therefore makes its P,Q
bichromatic. Both G40 copies then force their V endpoints to have O's colour.
Those two endpoints are adjacent, a contradiction. This proves the specified
finite union is non-four-colourable.

The construction needs at most

```
79 + 118(49-2) + 118*18(375-3) = 795753
```

vertices. Coincidences between copies can only lower this upper bound. Each
copy is an injective isometry and every intended edge stays unit length, so
extra coincidences or extra unit edges cannot invalidate the restriction
argument. The checker validates all 118 pair maps and 2,124 triangle maps,
including unit multipliers and all attachment coordinates. The written
isometry argument covers every edge in each copy; no huge graph dump or
all-pairs check on the assembled union is necessary. The exact deduplicated
order and chromatic number of the full union are not computed. An
inclusion-minimal non-four-colourable induced subgraph is five-chromatic and
inherits the same upper bound, but no such subgraph is extracted here.

This is the Exoo–Ismailescu composition with a smaller forcing component. Its
large budget is a decisive limitation for the record objective. A substantially
cheaper assembly or different geometry remains necessary.

## Reproduction and validation

Python 3.11 or later and the standard library suffice. Run inside this directory:

```sh
python3 geometry.py
python3 verify.py
python3 -O verify.py
python3 assembly.py
sha256sum -c SHA256SUMS
```

The verifier should print exactly `expected.json`. In addition to the graph,
forcing and composition checks above, it agrees with unpruned named-colour
enumeration on **5,120 complete small cases**, including triangle constraints
and equal or unequal pins, and rejects **11 malformed certificates**. Normal
and optimized Python results agree. Canonical point and edge hashes use compact
JSON, sorted coordinate order as above and lexicographic edges `[i,j]` with
`i<j`:

```
points 0bf15083801eb6fa982b04e820aca6c5a16c9b75b2d85b3efd00c53716edb1fe
edges  0e3d04cf0e0df94e9a7a9adda6677d92db162faf3ab29947dde8e0f52c287660
```

Optional `search.py` regenerates the single deletion pass using
`python-sat==1.9.dev15` and bundled Glucose3 (recorded Python 3.12.14). It writes
its raw history under ignored `out/`. Each vertex has exactly one colour;
each edge clause is guarded by its two vertex selectors; every query sets
every selector and fixes the three terminal colours to 0. This is precisely
the induced-subgraph four-colouring problem. It is discovery code only.

```sh
python3 -m pip install python-sat==1.9.dev15
python3 search.py
```

The [509-vertex Parts graph](https://arxiv.org/abs/2010.12665) remains the
standing record comparison, also stated by
[Haugland, August 2026](https://arxiv.org/html/2608.04542v4). HN-2's separate
[complete H560 deletion closure through 508](../hadwiger_nelson_heule560_target508/README.md)
is inspected context, not a premise. The retired support mechanisms remain
closed in the [earlier handoff](../hadwiger_nelson_finite_centre_synthesis/SUPPORT_HANDOFF.md).
This pass stops at the checked forcing-gadget and composition milestone.
