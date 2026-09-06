# Origin-only Heule bridges and a bounded H514 family decision

The complete 122-point [published completion frontier](../hadwiger_nelson_heule510_completion_frontier/README.md)
contains exactly **four points with neighbours in both blocks of H510**:
centre indices **170, 436, 1239, 1527**. Each has only one large-block
neighbour, the origin. Together these four points induce a path, and all
four are adjacent to the origin. Thus this selection introduces four new
cross-block edges but no new large-block attachment vertex.

Adding all four to H510 gives a distinct exact support **H514**, with
**514 vertices and 2,526 unit edges**. One frozen, simultaneous family pilot
tested 64 induced 508-vertex graphs; every query was SAT and its colouring
was checked. The pilot reached its specified limit. **H514 is not closed**,
and no five-chromatic or record graph is established.

The compact positive certificates force 484 vertices in any non-four-colourable
subgraph. Exhausting all six-subsets of the other 30 yields **258,914 exact
library residuals**. Existence of a non-four-colourable H514 subgraph on at
most 508 vertices is equivalent to deciding these specified induced
508-vertex graphs. Residual means uncovered by the checked colourings only.

## Fixed selection and exact geometry

H510 uses the increasing union-certificate labels marked `510` in
[`certificate_H510.json`](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json).
All indices below are this H ordering, not the original Heule labels.
Coordinates use the positive-radical basis
`1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)`.
The block L consists of points whose coefficients in positions 2,3,6,7
vanish in both axes; it has 375 vertices. The other 135 form S.

The selection predicate was fixed on all 122 rows in
[`fresh_candidates.json`](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json):
at least one H510 neighbour in L and at least one in S. The preceding census
establishes that this table comprises the points outside U553 and A1111
with at least four H510 neighbours. This pass does not re-enumerate the
whole-plane centre census. Its selection statement is specifically within
that published 122-point table, and it excludes no lower-degree or other-ambient
points or configurations of several points.

The selected points, in new vertex order 510 through 513, are

| H514 index | Centre index | x | y | Complete H510 neighbours |
|---:|---:|---|---|---|
| 510 | 170 | −7/8 | −sqrt(15)/8 | 0,361,417,495,503,509 |
| 511 | 436 | (−7−3sqrt(5))/16 | (7sqrt(3)−sqrt(15))/16 | 0,418,498,506,508 |
| 512 | 1239 | (7−3sqrt(5))/16 | (7sqrt(3)+sqrt(15))/16 | 0,359,362,502 |
| 513 | 1527 | 7/8 | sqrt(15)/8 | 0,358,416,507 |

Their only mutual unit edges are `510–511`, `511–512`, `512–513`.
Their only L neighbours are vertex 0, whose coordinates are exactly zero.
The other attachment neighbours are fifteen distinct S vertices.
The complete H514 graph has 1,920 L edges, 572 S edges, and 34 cross edges;
the new small block has 139 vertices. It includes all geometric unit edges.

[`geometry.json`](geometry.json) records the complete 122-point neighbour
classification and the four selected neighbourhoods. The independent
implementation checks all **62,220 centre-to-H pairs**, compares every
published neighbour list, selects exactly these four, and directly checks
all **131,841 H514 point pairs**. It uses scale 288 to cover every denominator
in the input table; the selected support itself has denominator dividing 96.
All 514 points are distinct, and the added points are outside U553.
Their A1111 exclusion is inherited from the pinned census; that exclusion is
unnecessary for the finite graph and colouring claims here.

## Transported witnesses and frozen pilot

The [accepted H517 closure](../hadwiger_nelson_heule517_whole_decision_review1/README.md)
provides 963 durable colourings in compact source formats. H517 remains
retired from deletion-only search. Here its colourings are restricted to
their first 510 entries, then extended onto the four different points above.
No H517 colouring theorem is assumed to imply an H514 colouring.

For each old row, the producer exhausts all 625 partial colour strings on
the four additions, maximizing retained additions and then choosing the
lexicographically first string with the order `0,1,2,3,.`. It next attempts
greedy restoration of omitted H510 vertices in increasing L then S order.
Every resulting full 514-character colouring is checked. These 963 transported
rows yield an initial 512-set antichain, with 464 singleton cuts.

The frozen [`plan.json`](plan.json) then allows at most **64 native graph
queries**, each limited to **100,000 conflicts**, and 4 GiB address space.
A SAT omission master has 514 Boolean omission variables, an at-least-six
threshold encoding, and one clause `OR(v in D) not omit(v)` for every checked
positive cut D. Each master query is limited to 100,000 conflicts. A model's
first six omitted indices give an uncovered 508-vertex candidate, because
every subset of a cut-avoiding omission set also avoids the cuts.

The full candidate oracle uses 2,570 variables and 10,619 clauses. Colour
variables have index `4v+c+1` and activation variables `2057+v`. Each activation
guards a four-colour at-least-one clause; every unit edge supplies four binary
colour inequalities. The final clause is `not a(0) or x(0,0)`, and all 514
activation literals are assumed in every query. At-most-one colour clauses
are unnecessary: adjacent nonempty true-colour sets are disjoint, so choosing
one true colour at each selected vertex gives a proper colouring. Conversely
every proper colouring, after palette normalization at vertex 0 if retained,
gives a model. No intact-L profile restriction is imposed.

All 64 graph queries and all 65 master queries returned SAT. Every candidate
colouring was decoded, checked, greedily extended over omitted L then S
vertices, and checked again before adding its positive cut. There was no
UNKNOWN, negative target, proof trace, or limit extension. The run took
**10.0317 seconds**, peak RSS **40,040 KiB**, using python-sat 1.8.dev24 and
CaDiCaL 1.9.5. This is a bounded search transcript, not an exhaustive
four-colourability decision on all candidates.

The deterministic master selected six L omissions in every one of the 64
queries. This bias matters: the exact residual family below spans all seven
block compositions. Another unchanged master run would not by itself establish
a new family-level mechanism.

## Positive certificate and exact residual reduction

The final public [`certificate.json`](certificate.json), **21,769 bytes**,
contains 491 transport recipes and 25 complete native colour strings. A
transport recipe is `[source_index, tail, fills]`: restrict that source row to
its first 510 entries, append the four-character tail, then fill the listed
previously omitted H vertices. Source indices run through the inherited
groups in order: 526 prior rows, 202 final small rows, 86 two-large rows,
108 three-large rows, 33 four-large rows, and eight whole-H517 rows.
Every recipe is decoded into a full colouring and checked directly on H514.
Native rows additionally state their exact dot positions and original query
index. No solver answer is needed to trust a verified positive row.

These 516 omission sets form an inclusion antichain of **484 singletons,
31 pairs and one triple**. A colouring of H514-D colours every subgraph
omitting D; hence any non-four-colourable subgraph must intersect each D.
The singleton sets force 358 L and 126 S vertices. The only possible omitted
vertices of such a subgraph are

```
46,59,65,108,152,210,214,219,236,257,294,301,313,321,331,
344,371,398,433,436,439,448,449,466,497,500,510,511,512,513.
```

All 32 non-singleton cuts lie in this 30-vertex set. Of its
`binomial(30,6)=593,775` six-subsets, 334,861 contain a certified cut and
258,914 do not. The complete residual histogram is

| L omissions | S omissions | Residual six-subsets |
|---:|---:|---:|
| 0 | 6 | 246 |
| 1 | 5 | 4,701 |
| 2 | 4 | 29,436 |
| 3 | 3 | 77,966 |
| 4 | 2 | 92,272 |
| 5 | 1 | 46,483 |
| 6 | 0 | 7,810 |

Any non-four-colourable subgraph on at most 508 vertices retains the 484
forced vertices and omits at least six others. Choose six of its omissions.
They must be one of these residuals, and the subgraph lies in the corresponding
induced 508-vertex graph. Conversely any non-four-colourable graph in that
residual family is itself a target-order subgraph. This proves the exact
reduction, including edge-deleted graphs, without asserting uncolourability
of any residual. The first residual is `46,108,152,210,219,294`; it was not
queried within the frozen pilot.

The local frontier is 6,074,339 bytes, consisting of lexicographic increasing
six-tuples of global H514 indices, comma-separated decimal ASCII without
spaces and with one LF per row. Its SHA-256 is

```
6098161a878f17d4eb0f102124e1ea193543d15e4120c1ca0269a28baf0e6c80
```

The exhaustive dump stays local. [`census.json`](census.json) gives compact
counts, examples and its digest, and the source regenerates every tuple.

## Independent checking and reproduction

[`verify.py`](verify.py) imports neither the producer nor a SAT package.
It uses the hash-pinned reviewer-owned integer radical arithmetic and original
witness decoder, reconstructs the new geometry independently, and checks all
516 public colourings (**1,298,057 edge inequalities**). It rederives the
antichain and forced vertices, directly enumerates all six-subsets using set
containment, and compares **every residual entry** with a separate bit-mask
backtracking enumeration that prunes forbidden partial selections. The two
streams match, including order and termination. All 256 hypergraphs on three
vertices at all four ranks pass against direct enumeration: **1,024 controls**.

The optional native audit also checks all 963 transported colourings
(2,421,086 inequalities), all 64 native colourings (159,997 inequalities),
every query's eligibility and positive cut, all retained provenance and
subsumption, and the actual full graph, activation CNF and final omission
formula entry by entry. It does not rely on replaying the solver's branching.
The full audit took **19.4711 seconds**, including 3.5910 seconds for the
two complete residual enumerations and comparison.

From the repository root, Python 3.11.2 and standard library only:

```bash
python3 -B hadwiger_nelson_heule514_interface/verify.py --out /tmp/h514-verified
```

The output directory must be new; omit `--out` to check the complete census
without saving the large frontier. Expected fields are `family_closed=false`,
`forced_vertices=484`, and census residual 258914.

To reproduce the bounded discovery, use a Python environment with
`python-sat==1.8.dev24` and new output directories:

```bash
python3 -B hadwiger_nelson_heule514_interface/run.py --work /tmp/h514-pilot
python3 -B hadwiger_nelson_heule514_interface/verify.py --work /tmp/h514-pilot
```

The master uses a backward prefix-threshold encoding. Its auxiliary variables
say that a prefix can certify at least j omissions; the implications require
either a previous same-threshold certificate or the current omitted variable,
and, for j greater than one, either that same-threshold certificate or a
previous lower-threshold certificate. Requiring the final threshold six
therefore forces at least six omissions. Conversely setting auxiliaries to
the true prefix counts satisfies the clauses. The final master has 3,583
variables and 6,141 clauses. Its SAT status is also witnessed simply by the
displayed residual six-tuple. No negative solver certificate is asserted.

The trust boundary is exact source coordinates and the radical basis,
Python integer and Fraction arithmetic, faithful witness decoding, complete
finite loops, and the restriction argument. The frontier's previous
whole-plane completeness and A1111 exclusion are inherited from the cited
census. This is author-run computer-assisted evidence; the accepted review
of the reused H517 foundation does not review the new H514 result.

## Decision and handoff

The bounded pilot is complete and its family remains open. The mixed-neighbour
predicate produced only origin attachments, and the master sampled only one
block composition. These facts support **no unchanged runtime extension** and
no new deletion-stratum ladder. The exact frontier and formulas are preserved
for reassessment; no background process or unfinished proof remains.

If this support is retained, the next distinct mechanism should first derive
the complete list-colouring extension relation of the four-vertex path joined
to the origin, including optional path vertices. Vertex 0 is forced by the
checked certificates, so its normalized colour leaves three available colours
on each retained new vertex. The complete local relation has a bounded domain
of 16 path-selection masks and `8^4` possible colour-list tuples. Such a
projection would apply across every residual block composition. It has not
been computed here, and this suggestion is not an assertion that it will
close H514 or yield a record.

H517's full closure received independent acceptance at Discovery Net height
3178, source `b4af1d9056c56e76a7af7bd148c43afe4c7bf5b1`, and remains retired.
The initial shared refresh reached 3179. HN-3's separate geometric lane,
the parked HN-1 census, H574 deletion closure and timed-out QBF configurations
are not resumed by this work.

The final relevant graph refresh reached height 3181. HN-3's new
[483-point two-triangle sum](../hadwiger_nelson_heptagon_two_triangle_sum/README.md),
source `e87584f7e73ffc951ee2d8d9325b7b551885cdfd`, height 3180, was inspected.
Its symbolic extension preserves every colouring of its fixed eleven-point
host, so that support and all its subgraphs are four-colourable. It concerns
different exact factors and supplies no premise here. No new overlapping
H514 work or objection to the reused H517 closure appeared in the refresh.
