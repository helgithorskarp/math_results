# All near-injective planar realizations of Heule's H510 graph

Let **H510** be Marijn Heule's 510-vertex, 2,504-edge five-chromatic
unit-distance graph in the exact labelled form pinned below. A realization is
any map

\[
p:V(H510)\longrightarrow \mathbb R^2
\]

that sends every source edge to a pair at distance exactly one. The map need
not be injective, its coordinates may lie outside the source number field,
and source nonedges may become unit pairs.

**Exact computer-assisted classification.** Every realization of H510 with at
least **508 distinct images** has 510 distinct images. Up to a global Euclidean
isometry, it is one of the four labelled drawings obtained from the archived
H510 coordinates by independently changing the signs of `sqrt(5)` and
`sqrt(11)`. Thus H510 has no planar unit-distance quotient with exactly 508 or
509 images.

A realizable 508-image quotient would inherit non-four-colourability from
H510: any four-colouring of the quotient would lift to H510. It would therefore
meet the target order. The complete family is negative, so this result does
not improve the 509-vertex record. Realizations with at most 507 images,
modified source graphs, and constructions unrelated to H510 remain open.

The earlier [fixed 553-point union theorem](../hadwiger_nelson_parts509_heule_union_minimum/README.md)
only excludes small five-chromatic subgraphs inside one exact Parts/Heule
coordinate union. This classification permits arbitrary real coordinates and
arbitrary extra unit pairs. It uses planar rhombus identities and exact
algebra, without a colouring solver or a finite target host.

## A rank certificate that survives two image losses

Four distinct points forming a unit `K2,2`, with opposite pairs `{a,b}` and
`{c,d}`, obey

\[
p_a+p_b=p_c+p_d.
\]

The two points in either pair are the two distinct intersections of unit
circles centred at the other pair. The identity can fail if an opposite pair
coincides. Also, two distinct unit circles have at most two intersections, so
an injective planar unit-distance graph cannot contain `K2,3`.

The checker reconstructs H510 in its original labels from the pinned aligned
coordinate table and exact 553-point union. It checks all 2,504 source edges
at distance one and enumerates **3,953** canonical source rhombi. No source
pair has more than two common neighbours. Let `L` be the rational matrix with
one row `e_a+e_b-e_c-e_d` for each rhombus.

The certificate supplies 20 independently ordered sets of 501 rows. Each has
rank 501 modulo the checked prime 1,000,000,007. The archived coordinate
columns give nine independent kernel vectors, including translation, so
`rank(L)=501` over characteristic zero and the full kernel has dimension nine.

A realization with at least 508 images can have one colliding pair, two
disjoint colliding pairs, or one colliding triple. A colliding pair invalidates
at most one rhombus row. Thus the invalid-row set has size at most two in the
first two cases. A colliding triple can invalidate at most three rows, one for
each pair in the triple.

For every rhombus row, at least one of the 20 certified bases avoids it. For
every pair of rows, some basis avoids both except for exactly two row pairs:

```text
{1625, 3008}    {1647, 3016}
```

Each row has two possible opposite-pair collisions. The checker exhausts the
four choices for each exceptional row pair. All **eight** quotient graphs
contain an explicit `K2,3`, so none can be realized by distinct points in the
plane. This covers disjoint pairs as well as pairs sharing a vertex, where the
identifications generate a triple.

For completeness, the checker enumerates the opposition graph whose edges are
vertex pairs occurring opposite in a rhombus. Its **31,582** triangles are
exactly the possible three-row invalidation patterns from a colliding triple.
Only

```text
vertices {56,139,353}: rows {1625,1637,3008}
vertices {57,144,352}: rows {1647,1659,3016}
```

meet every supplied basis. Each contains one of the two exceptional row pairs
already excluded by its checked `K2,3`. Therefore some intact rank-501 basis
holds in every realization with at least 508 images.

Coordinates use the ordered multiquadratic basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Flattening x followed by y leaves precisely columns
`[0,2,5,7,9,11,12,14]`. Call the resulting rational 510-by-8 matrix `K`.
Every entry has denominator dividing 96. The checker verifies `L K=0` and
that `[1 | K]` has rank nine modulo the same prime. After translating vertex
0 to the origin, every eligible realization therefore has the form

```text
p_v = K_v * (A,B,C,D,E,F,G,H),       A,...,H in C = R^2.
```

This is a consequence of the intact rank certificate. It does not assume that
a new realization preserves the archived coordinates.

## Exhausting the triangle orientations

The 2,504 edges determine **36** distinct rational direction vectors in these
eight parameters, up to sign. The checker verifies a source edge for every
direction. They split into twelve triads with identities

```text
v_i + s*v_j = r*v_k,       s,r in {-1,+1}.
```

Writing `t=i*sqrt(3)`, unit lengths give the exhaustive alternative

```text
v_j = (-s/2 + epsilon*t/2)*v_i,       epsilon in {-1,+1}.
```

The certificate partitions all 4,096 sign words into 36 disjoint prefixes.
For each of 34 rejected prefixes, the checker proves three vertex equalities
as exact row-space consequences over `Q(t)` and recomputes that their generated
partition loses at least three images. Such a branch has at most 507 images.
The equality-partition check matters because three distinct pair equalities
can form a triangle and lose only two images.

The two surviving prefixes are complete words. Each equation matrix has rank
four, and its kernel is exactly one of

```text
E = sigma*t*A,  F = sigma*t*B,
G = sigma*t*C/3,  H = sigma*t*D/3,       sigma in {-1,+1}.
```

Reflection lets us take `sigma=+1`, and rotation makes the unit direction
`A=1`. The unit directions `(C+E)/6` and `(C-E)/6` then force `C` to be real
with `C^2=33`.

Write `B=b+t*y` and `D=d+t*z`, with real variables `b,y,d,z`, and substitute

```text
(A,B,C,D,E,F,G,H) =
(1, b+t*y, c, d+t*z, t, t*(b+t*y), t*c/3, t*(d+t*z)/3),
c^2 = 33.
```

The checker expands `|v|^2-1` for all 36 directions as polynomials over
`Q(c)`. Twenty-one nonzero certified combination terms give the four exact
identities

```text
b^2 + 3*y^2 - 5 = 0,
y = 0,
z = 0,
d - c*b = 0.
```

Hence `b=+/-sqrt(5)`, `c=+/-sqrt(33)`, and `d=bc`. The four sign choices are
exactly the stated Galois-conjugate drawings. The checker constructs all four,
checks 510 distinct points in each, and checks all 10,016 source-edge
incidences across them.

## Reproduction

Python 3.11 or later and its standard library suffice. Keep the two sibling
inputs at the paths and hashes in `inputs.json`. From this directory run:

```sh
python3 -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

`verify.py` is independent of the producer and prints `expected.json`. It
reconstructs the graph and rhombi, checks all rank bases and collision
exceptions, expands the complete orientation-prefix cover, verifies the
polynomial combinations, and rebuilds the four realizations. The 51,226-byte
certificate has SHA-256

```text
13aab3ef8e66770536ed4c064b41f3631ecab9b631148d7145e66d25087a0759
```

Optional deterministic discovery replay:

```sh
python3 -B generate.py --out /tmp/h510-plane-realizations
cmp certificate.json /tmp/h510-plane-realizations/certificate.json
python3 -B verify.py --certificate /tmp/h510-plane-realizations/certificate.json
```

The recorded producer replay took about 37 seconds and the verifier about two
seconds under CPython. Runtime is descriptive. Normal and optimized verifier
and control outputs agree byte for byte. `controls.py` compares 11,250
quadratic-field operations with rational arithmetic, checks ordinary and
degenerate diamonds, exhausts the equality-partition control, and rejects 15
mutations distributed across all certificate layers.

## Scope and trust boundary

The source coordinates and graph are the pinned identity-aligned copy of
Heule's public `510.vtx` construction in the sibling Parts/Heule certificate.
That sibling result records H510's 510 vertices, 2,504 exact unit edges, and
five-chromatic source status. This package independently checks coordinate
identity, source distinctness, and all source edge lengths. It does not rerun
the source non-four-colourability proof because the geometric classification
does not use colouring.

The proof trusts the two pinned input hashes, the usual Euclidean facts about
two-circle intersections, Python integer arithmetic, and the finite checks in
`verify.py`. Modular rank 501 is only a lower bound in characteristic zero;
the nine explicitly checked independent kernel columns supply the matching
upper bound. The orientation and polynomial stages use normalized exact
quadratic arithmetic. No approximate roots, numerical tolerance, SAT solver,
or external finite host enters the classification. No proof-assistant
formalization or external review is claimed.

The complementary [Parts-509 near-injective classification](../hadwiger_nelson_parts509_plane_realizations/README.md)
allows only one image loss and has a different source graph and rank-resilience
certificate. The present two-loss H510 theorem reuses its general rhombus and
orientation idea, with a new collision partition argument, two genuine rank
cocircuits, eight quotient obstructions, and a complete triple-collision
census.

## Source

Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic Number
5*, Geombinatorics 28 (2018), arXiv:1805.12181; public data in
`github.com/marijnheule/CNP-SAT` (`510.vtx`, source SHA-256 pinned by the sibling
certificate).
