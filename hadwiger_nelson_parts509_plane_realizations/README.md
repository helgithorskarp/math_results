# All near-injective planar realizations of the reduced Parts-509 graph

Let **S** be the published 509-vertex, 2,259-edge reduced Parts graph, with
labels and edges in the pinned sibling input. A realization is any map
`p: V(S) -> R²` that sends every edge to a pair at distance exactly one.
Coordinates need not stay in a prescribed field or finite host; nonedges need
not retain their lengths or remain nonedges.

**Exact computer-assisted classification.** Every realization of S with at
least 508 distinct images has 509 distinct images. Up to a global Euclidean
isometry, it is one of the four drawings obtained from the supplied Parts
coordinates by independently changing the signs of `sqrt(5)` and `sqrt(11)`.
These are four normalized labelled drawings; no assertion about unlabelled
congruence is needed.

Consequently **no quotient obtained by identifying one pair of vertices of S
admits an injective planar unit-distance realization**. A nonadjacent-pair
quotient would inherit S's non-four-colourability and have 508 vertices, so
this closes a complete candidate family for the record target. It is a
negative result, not a graph improving 509. Realizations with at most 507
images, modified source graphs and arbitrary smaller unit-distance graphs
remain unclassified.

The [previous fixed-host exclusion](../hadwiger_nelson_parts509_h632_one_collision/README.md)
allowed arbitrary maps into H632 with 508 or 509 images. The present argument
removes the finite host and classifies all injective drawings as well. Its
method is planar rhombus identities and exact algebra, independent of the
previous Hall-domain computation. The earlier
[framework rigidity result](../hadwiger_nelson_parts509_rigidity/README.md)
concerned infinitesimal motions of the full 2,442-edge drawing. Infinitesimal
rigidity alone does not imply this classification.

## Reduction to eight complex parameters

Four distinct points forming a unit `K2,2`, with bipartition `{a,b},{c,d}`,
satisfy `p_a+p_b=p_c+p_d`. Indeed, c and d are the two distinct intersections
of the unit circles centred at a and b, whose midpoint is `(a+b)/2`.
The identity can fail when an opposite pair coincides; that case must not be
silently treated as a rhombus. Two distinct unit circles have at most two
intersection points, so an injective planar unit-distance graph cannot contain
`K2,3`.

The checker enumerates all **2,726** source four-cycles, canonically written
`[a,b,c,d]` with the two sorted opposite pairs lexicographically ordered. Every
source pair has at most two common neighbours. Hence identifying a single
nonadjacent pair can invalidate at most one source rhombus identity. If the
pair is adjacent, its edge already forbids identification.

Let L be the rational matrix of these rhombus rows, with coefficients
`+1,+1,-1,-1`. The certificate supplies six sets of 500 rows. Each has rank 500
modulo the checked prime 1,000,000,007, hence rank at least 500 in characteristic
zero. Their common intersection consists of only five rows. The ten possible
opposite-pair identifications in those rows are all impossible: four collapse
a source edge; the other six create an explicitly checked `K2,3` in the
508-vertex quotient. Thus **some complete rank-500 basis remains valid in
every realization with at least 508 images**. The argument includes injective
realizations, for which no rhombus identity is lost.

The coordinate input represents x and y in the ordered radical basis

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Flatten x followed by y and select columns `[0,2,5,7,9,11,12,14]` to obtain a
rational 509-by-8 matrix K. Every coefficient has denominator dividing 96.
All other flattened columns vanish. The checker verifies `L K=0` over Q and
that `[1 | K]` has column rank nine modulo the same prime. Therefore every
intact rank-500 rhombus basis has kernel exactly the span of `[1 | K]`.
After translation to put vertex 0 at the origin, every eligible realization
has the form

```
p_v = K_v · (A,B,C,D,E,F,G,H),        A,...,H in C ≅ R².
```

These eight complex values are unrestricted at this stage. The rational
coefficient matrix is a parameterization proved by rank, not an assumption
that the new drawing preserves its old coordinates.

## Exhausting the triangle orientations

The 2,259 edges give **36** distinct rational direction vectors, up to sign,
in the eight parameters. One source edge witnesses the unit length of each.
They form twelve disjoint triads with identities
`v_i + s v_j = r v_k`, where `s,r` are signs. Put `t=i sqrt(3)`.
Unit lengths imply the exhaustive alternative

```
v_j = (-s/2 + epsilon*t/2) v_i,       epsilon in {-1,+1}.
```

This follows by dividing by the nonzero unit vector v_i and using that the
real part of the unit quotient is `-s/2`. Each of the twelve triads permits
two signs, so all possibilities lie in a 4,096-word Boolean cube.

The compact certificate partitions that entire cube into **34 disjoint
prefixes**. For each of 32 rejected prefixes, the checker verifies, by exact
row-space membership over Q(t), two distinct unordered vertex-pair equalities
forced by the prefix's linear equations. Two different equality pairs force
at least two losses of distinct images, leaving at most 507. This rejection
uses exact linear consequences and is valid for all complex parameter values.
The checker expands the prefixes to confirm complete, nonoverlapping coverage;
it does not trust the producer's search traversal.

The two surviving prefixes are complete words. Each equation matrix has rank
four, and its kernel is precisely one of the conjugate systems

```
E = sigma*t*A,  F = sigma*t*B,
G = sigma*t*C/3,  H = sigma*t*D/3,       sigma in {-1,+1}.
```

Reflect the drawing if necessary to take `sigma=+1`. Direction A is unit, so
a global rotation makes `A=1`. The two unit directions `(C+E)/6` and `(C-E)/6`
then give `C` real and `C²=33`. Write `C=c`, where either real root is allowed.

## The remaining polynomial identities

Write `B=b+t*y` and `D=d+t*z` with b,y,d,z real. Substitute

```
(A,B,C,D,E,F,G,H) = (1, b+t*y, c, d+t*z, t,
                     t*(b+t*y), t*c/3, t*(d+t*z)/3),
c²=33.
```

For each of the 36 unit directions form the polynomial `|v|²-1`. The checker
expands these polynomials directly in the four real variables, with
coefficients in Q(c). It verifies supplied sparse linear combinations giving
exactly the following four identities, using **21 nonzero combination terms**:

```
b² + 3y² - 5 = 0,
y = 0,
z = 0,
d - c*b = 0.
```

Thus `b=±sqrt(5)`, `c=±sqrt(33)`, and `d=bc`. This reasoning applies to both
real embeddings of Q(c); no root sign is discarded. It gives precisely the
four coordinate conjugates stated in the theorem. Conversely, the checker
constructs all four sign choices, checks that each has 509 distinct points,
and verifies all 2,259 source unit edges in each drawing: **9,036 edge checks**.

All coordinates and distance tests use exact integers in the multiquadratic
basis. Distinct coefficient vectors represent distinct real numbers because
3, 5 and 11 have independent square classes over Q. This also explains why
the field sign changes preserve both equality and inequality of coordinate
values. No numerical tolerance or floating-point root approximation occurs.

## Reproduction and certificate

Python 3.11 or later and its standard library suffice. Keep the two sibling
inputs at the paths pinned by `inputs.json`. From this directory:

```sh
python3 -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

`verify.py` prints the canonical result in `expected.json`. The committed
certificate is compact JSON, **17,179 bytes**, with SHA-256

```
675a5c65e67f9080cdf82649c1ce2f1ca9371e83536c536b0394b04f1c6cef74
```

Optional deterministic discovery replay:

```sh
python3 -B generate.py --out /tmp/parts-plane-realizations
cmp certificate.json /tmp/parts-plane-realizations/certificate.json
python3 -B verify.py --certificate /tmp/parts-plane-realizations/certificate.json
```

The recorded producer run took about 10 seconds under CPython 3.11.2; the
independent verifier took under one second. Runtime is descriptive, not a
proof premise. Normal and optimized (`-O`) producer certificates, verifier
reports and control reports match byte for byte.

The producer uses Fraction pairs, forward-pivot elimination, kernel projection
and adaptive prefix discovery. The verifier imports no producer code: it uses
normalized integer triples for quadratic fields, reverse pivots, direct
row-space consequence checks, explicit prefix coverage and independent
polynomial expansion. Its exact distance multiplication uses gcd reduction
of square-free radicands. All proof data are committed; the exploratory full
orientation enumeration and private run logs are unnecessary for reproduction.

Controls compare 11,250 quadratic-field cases against Fraction arithmetic,
check both an ordinary and a degenerate diamond, exhaust 45 two-equality-pair
cases, and reject 15 mutations across the certificate's proof layers. They
are author-run verification controls, not independent peer review. A proposed
control initially substituted another valid forced equality; it was replaced
by a false equality. The mathematical certificate did not change.

## Scope, context and trust

The [source criticality certificate](../hadwiger_nelson_parts509_edge_criticality/README.md)
provides S's non-four-colourability. That result explains why a realizable
one-identification quotient would be useful; the geometric classification
itself does not rely on any SAT solver or chromatic-number computation.
The coordinate data come from the pinned
[degree-pool certificate](../hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json).
Input hashes, source edge labels, radical interpretation, ordinary integer
arithmetic, finite checks and the written planar reduction are the trust
boundary. No proof-assistant formalization or external review is claimed.

The separately pursued
[E477 spindle classification](../hadwiger_nelson_e477_spindle_classification/README.md)
was inspected as team context and is not a premise. The retired H560 and
capped H632 deletion searches were not resumed. Targeted literature searches
on 2026-09-07 found no matching Parts realization classification; this is not
a priority claim. The named Hadwiger–Nelson record problem remains the sole
research target. This complete source-quotient family is now closed; changing
the image-loss budget would be a separate problem, not an automatic next step.
