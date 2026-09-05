# A complete Heule-510 completion frontier outside two earlier ambients

There are exactly **122 points outside both the closed 553-point
Parts/Heule union and the parked 1111-point ambient with at least four
unit neighbours in Heule's 510-point graph**. Their degrees are 4 through
8; exactly two have degree eight and five have degree seven.
[fresh_candidates.json](fresh_candidates.json) gives every one of these
points and its complete Heule neighbour list.

This is an exact finite geometric classification and a changed research
frontier. No colouring query, five-chromatic graph on at most 508 vertices,
or new minimum-order closure is established in this pass. The adjective
"fresh" means outside the two specified coordinate sets; it makes no
claim that these coordinates are new in the literature or absent from
every earlier completion table.

## Inputs and labels

H is the 510-point subset marked `510` in the public
[553-point union certificate](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json).
Its exact coordinates agree as a set with the separately stored
[aligned Heule table](../hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json).
The original identification with Heule's `510.vtx` and the earlier
minimum-order theorem are inherited from that durable package. The raw
external file and its chromatic-number proof are not downloaded or rerun
here. This pass reconstructs H's complete 2504-edge unit-distance graph.

All coordinates use rational coefficients in the basis

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The square roots are positive. Independence of the square classes of
3, 5 and 11 makes coefficientwise equality exact. The H coordinates have
common denominator 96, and their integer coefficients have magnitude
at most 144. [manifest.json](manifest.json) pins all input identities.

Let U553 be the whole earlier union certificate. Let A1111 be the
original Parts509 points together with the 602 no-sqrt5 completion-table
points of original degree at least four, as defined by the preceding
[A976 package](../hadwiger_nelson_parts509_A976_colourability/README.md)
with its 135-point partner restored. A1111 is a comparison set, **not a
closed family**. The producer reconstructs it by the published degree
predicate; the auditor instead uses the A976 certificate's explicit
labels. No search or deletion audit inside either old ambient is run.

In generated files, H indices 0 through 509 mean the increasing order of
the union-certificate labels marked `510`; `H_labels.json` records that
map. They are not the original Heule input order or Parts labels. Centre
indices mean lexicographic order of the 16 rational coefficients, with
the x coefficients first. The frontier certificate includes exact
coordinates, so its identity does not rely on an index alone.

## Complete census

For every point q in the Euclidean plane, let d_H(q) be the number of
its unit neighbours in H. There are exactly 1712 points with d_H(q)>=3:
all 510 H vertices and 1202 external centres. No external centre has
degree greater than ten. The table records the relevant external counts.

| d_H(q) | Outside H | Outside U553 | Outside both U553 and A1111 |
|---:|---:|---:|---:|
| 3 | 539 | 539 | 473 |
| 4 | 265 | 264 | 89 |
| 5 | 201 | 188 | 12 |
| 6 | 122 | 108 | 14 |
| 7 | 37 | 26 | 5 |
| 8 | 26 | 23 | 2 |
| 9 | 10 | 10 | 0 |
| 10 | 2 | 1 | 0 |

Thus 663 external centres have degree at least four. Of these, 620 are
outside U553, and 122 are outside both specified ambients. The other 498
outside U553 are excluded from this new frontier by membership in A1111;
this pass supplies no new colourability verdict on them.

The seven frontier centres of degree at least seven have centre indices
327, 439, 671, 1040, 1074, 1377 and 1383. Indices 327 and 1383 have degree
eight. All seven have nonzero sqrt5-related coefficients; they extend
beyond the previous no-sqrt5 large-side support. Their Parts degrees
are respectively 6, 6, 7, 5, 7, 6 and 8, so these seven coordinates were
already eligible for the broader Parts completion census. Their new
Heule incidences and ambient exclusions are the point of this result.
[audit_result.json](audit_result.json) lists their coordinates and both
neighbour systems with explicit label conventions.

The prior U553 minimum-order closure gives a target-facing reduction.
For a point q outside H and a three-element deletion D from H, the
base H minus D has 507 vertices and is four-colourable. If d_H(q)<=3,
its colouring extends over q. Hence a five-chromatic graph of the form
(H minus D) union {q}, on 508 points, requires one of the 663 external
degree-at-least-four centres. If q belongs to U553, the prior closure
already rules it out; 620 centres remain outside that union. Requiring
the added coordinate also to leave the parked A1111 ambient selects
precisely the 122-point list here. This reduction does not assert that
any listed centre yields a non-four-colourable graph. Groups of added
points can have mutual edges and are not restricted by this single-point
degree argument.

## Completeness proof and implementation

Three distinct points on a unit circle are noncollinear and determine
its centre uniquely. For their squared side lengths s,t,u, the unit
circumradius identity is

```
s*t*u = 2*(s*t+t*u+u*s) - s*s-t*t-u*u.
```

If S,T,U are squared-distance numerators at coordinate scale D=96, the
cleared identity is STU = D^2 times the same quadratic expression in
S,T,U. Evaluating the radical basis in any ring with the required square
roots preserves this identity. Consequently an exact unit triangle
cannot be discarded by a nonzero modular image.

[filter.cpp](filter.cpp) enumerates **all 21978620 unordered triples**
of H. It applies two such homomorphisms with moduli 60289 and 1000081.
The images of sqrt(3), sqrt(5), sqrt(11) are respectively
(4799,25141,4267) and (964569,816716,970601); their squares are checked
against (3,5,11) before enumeration. The first filter retains 104136
triples and the second 103976. The program claims only a superset, never
exact acceptance on modular evidence.

[census.py](census.py) reconstructs exact rational field centres from
surviving triples by solving their two perpendicular-bisector equations.
Field inversion uses successive conjugate norms through sqrt(11),
sqrt(5), sqrt(3), ending in rational inversion. Each centre's complete
unit-neighbour list is recomputed. Already accounted-for triples can be
recognized by two of their neighbours; this avoids solving the same
centre repeatedly and removes no unexplained triple.

[audit.py](audit.py) imports no producer module or earlier field
arithmetic. It treats the centre table as an untrusted rational
certificate, uses explicit monomial exponent reduction, and checks all
873120 centre-to-H pairs. It compares every neighbour list, forms every
triple of each list, rejects assignment of one triple to two centres,
and compares all 103976 triples entrywise with the actual modular
survivor stream. Every survivor is accounted for by exactly one centre;
there are zero residual modular false positives. The identity
sum_q binomial(d_H(q),3)=103976 is also checked, but a matching aggregate
count alone is not the audit.

Every Euclidean point with at least three H neighbours gives a triple
that survives both filters. That triple appears in exactly one audited
neighbour list, whose centre must equal the original point by uniqueness.
This proves completeness in the whole plane, including points not
initially assumed to lie in the coordinate field. All 1712 listed centres
in fact have coefficient denominators dividing 288: 1700 have common
scale 96 and twelve require scale 288.

The proof architecture was informed by the earlier
[Parts centre census](../hadwiger_nelson_parts509_completion_census_degree9/README.md).
Here the geometric family is H510, the modular enumerator is new, the
centres are lifted exactly without floating-point proposals, and the
auditor compares the complete triple stream. No Parts census or
teammate construction family was re-enumerated.

## Reproduction and checks

Use a full checkout, Python 3.11.2 and g++ 12.2.0 (tested), with assertions
enabled. Python uses the standard library. Choose a fresh external run
directory; the census refuses to overwrite an existing run.

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic filter.cpp -o /scratch/heule-centre-filter
python3 -B controls.py --filter /scratch/heule-centre-filter --work /scratch/heule-controls
python3 -B census.py --filter /scratch/heule-centre-filter --work /scratch/heule-census
python3 -B audit.py --work /scratch/heule-census
sha256sum -c SHA256SUMS
```

Expected audit status:
`EXACT HEULE510 CENTRE CENSUS AND NEW FRONTIER VERIFIED`.
[expected.json](expected.json) fixes all stable counts and generated
identities. The full centre table is 268832 bytes and its SHA256 is
`a1cd29a0ba15caa704c9f9b2cf2ebd72b8fdc2fea9983ffca6e660484fb168fd`.
The 1158843-byte survivor stream has SHA256
`684636245bbc478f559fc654052e8263dc90df59517c0f12e499082462bb7c92`.
Both are generated locally rather than committed. The complete useful
122-point frontier is a compact 23322-byte public certificate.

The producer took 47.50 seconds, including 2.25 seconds for the C++ filter;
the independent audit took 34.11 seconds. The process is single-threaded;
peak memory was not measured. [validation.json](validation.json) records
the compiler, flags, file sizes and timings.

All 1552 triples of three small fixtures were compared against exact
Python arithmetic, including 44 valid unit-circle triples whose centres
were also lifted and checked. There are 64 field-basis product controls,
ten inversion controls and an invalid-header rejection. The same controls
passed an AddressSanitizer/UndefinedBehaviorSanitizer build:

```bash
g++ -std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -Wall -Wextra -Wconversion -Wshadow -pedantic filter.cpp -o /scratch/heule-centre-filter-sanitized
python3 -B controls.py --filter /scratch/heule-centre-filter-sanitized --work /scratch/heule-controls-sanitized
```

The native arithmetic uses reduced uint64 residues. The moduli are at
most 1000081; every product is at most (1000080)^2 and every intermediate
sum is below 2*(1000081)^2+4*1000081, hence below 2.1 trillion.
Coordinate images start from coefficients
between -144 and 144. All are far below the relevant fixed-width limits.
Python field calculations use arbitrary-precision integers and rational
numbers. The C++ loop and the homomorphism argument remain part of the
computational trust boundary; the audit does not independently re-run all
21 million triples in Python. The separate implementation is an author
check, not an independent-author review.

## Decision and next milestone

The complete degree-at-least-seven frontier outside both old ambients
has seven points. This supports a genuinely changed next finite support:
H510 together with all seven, 517 distinct points. The next pass should
first check containment against any other applicable durable closures,
then freeze one bounded **simultaneous minimum-order certification**
pilot for its subgraphs on at most 508 vertices. No edge set of that
517-point support or colouring query on it has been constructed here.
There is no series of isolated one-point tests or automatic increase of
the degree/quota range.

The source and exact census checkpoint are complete. HN-3's newly
published wheel-interface reduction, source
`e07cc375f002f1c614c3f4a772b4a9b9e4692517`, was read before this work.
Its three ordinary heptagon queries remain unresolved and that fixed
seed is parked. It is not a premise of this census. Shared graph evidence
was refreshed before publication. No native colouring query, unfinished
certificate or background process remains.
