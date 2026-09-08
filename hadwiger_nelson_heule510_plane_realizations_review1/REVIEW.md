# Independent review of h3945 H510 realization classification

**Verdict: ACCEPT for the stated near-injective geometric classification.**

This reviews Discovery Net h3945,
`bafkreia5oxkhc3sjykhvvl2fqkksrd3ple4ci4rcyn6x6z4ixjkj7y6dqq`, at exact
source commit `70bd2363ee5505770eb54d3fd089a640d2c6a653`. Let H510 denote the fixed
labelled graph with 510 vertices and 2,504 unit edges. Every map from its
vertices to the real Euclidean plane that preserves those edge lengths and
has at least 508 distinct images actually has 510 images. After a global
Euclidean isometry, its coordinates are one of the four arrays obtained from
the archived drawing by independently changing the signs of `sqrt(5)` and
`sqrt(11)`.

Thus no identification quotient of H510 with 508 or 509 vertices has an
injective planar unit-distance realization. If such a 508-image realization
existed, non-four-colourability of H510 would descend to its image graph, so it
would meet the campaign target. The classification is negative: it constructs
no graph, changes no record, and says nothing about maps with at most 507
images or modified source graphs.

## Exact source graph

The pinned inputs have SHA-256 values

```text
aligned_510.json  84456269b4acb9fa911164f7148eb227e5f30835f03d8cb5d46d6f9602fd8e5b
union_510.json    19d360e5d460ecf1abc6d8e0084046de5e33a05c6c9ff1dff7d26d4ba5e298d9
```

Coordinates lie in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The square classes of 3, 5, and 11 are independent, so coefficient comparison
in this basis is exact. The reviewer parses the 510 coordinate pairs using
`Fraction`, proves they are distinct, and computes squared distances for all
129,795 unordered pairs. Exactly 2,504 are unit pairs, and the resulting edge
list agrees entry-for-entry with the restriction of the pinned 553-point
strict union graph. This is stronger than merely checking the declared edges.

The current public upstream `510.vtx` has 510 lines and SHA-256
`66defa1743e64073776ed4c6a2e9c496abbd4628bf7d973dcc07cf834ce35b37`,
matching the identity pinned by the sibling alignment package. The geometric
theorem below needs only the exact labelled graph. Its known
non-four-colourability is imported for the target consequence and was not
re-proved in this milestone.

## Rhombus reduction and image-loss coverage

Suppose four source vertices form a `K2,2`, with opposite pairs `{a,b}` and
`{c,d}`. If neither opposite pair collides under a realization, the four
images are distinct. The images of `c,d` are then the two intersections of
the unit circles centred at the images of `a,b`; their common midpoint gives

```text
p_a + p_b = p_c + p_d.
```

A cross-part collision cannot occur because each cross pair is a source edge.
The exact graph has 3,953 canonical rhombi and no pair with more than two
common neighbours. Therefore a colliding source pair invalidates at most one
rhombus equation.

A partition of 510 vertices into at least 508 images has only three possible
nontrivial forms: one colliding pair, two disjoint colliding pairs, or one
colliding triple. The corresponding invalid-row sets have sizes at most one,
two, and three respectively.

Let `L` be the 3,953-by-510 rational rhombus matrix. All rows annihilate the
constant column and the eight rational coordinate columns `K`. The reviewer
checks these nine columns are independent modulo the independently chosen
prime 1,000,000,009. It generates 32 independently ordered row bases at that
prime; each contains 501 rows of modular rank 501. Hence `rank_Q(L)=501`: the
bases give the lower bound, while the nine exact kernel columns give the
matching upper bound.

The 32 bases avoid every single invalid row. They avoid every invalid row pair
except

```text
{1625,3008}  and  {1647,3016}.
```

For each pair, the two opposite sides of each rhombus give four possible
collision choices. The reviewer reconstructs all eight quotient graphs and
finds five distinct quotient vertices spanning a `K2,3` in each. Such a graph
cannot be realized by distinct plane points at unit distance: two distinct
unit circles have at most two intersections.

For a colliding triple, three rows can fail only when its three source pairs
form a triangle in the opposition graph. The independently enumerated census
has 31,582 triangles. All but two are avoided by one of the 32 bases, and each
of the two exceptions contains one of the already impossible row pairs.
Therefore every realization with at least 508 images satisfies an intact
rank-501 basis.

## Parameterization and direct orientation exhaustion

Because an intact basis has a nine-dimensional kernel with basis `[1|K]`, a
translation taking vertex 0 to the origin gives

```text
p_v = K_v (A,B,C,D,E,F,G,H),       A,...,H in C.
```

This does not assume that the new coordinates lie in the archived number
field; the eight parameters are arbitrary plane vectors, represented as
complex numbers.

The 2,504 edges yield exactly 36 rational parameter directions, up to sign.
The reviewer derives, without the submitted certificate, exactly twelve
disjoint identities

```text
v_i + s v_j = r v_k,       s,r in {-1,+1},
```

partitioning all directions. Since all three evaluated vectors have unit
length, with `t=i*sqrt(3)` one necessarily has

```text
v_j = (-s/2 + epsilon*t/2) v_i,    epsilon in {-1,+1}.
```

Rather than validating the submitted 36-prefix cover, the reviewer enumerates
all 4,096 complete sign words. A finite-field extension modulo 1,000,000,097
is used only to propose candidate forced equalities. Every equality counted
toward image loss is then checked as an exact row-space consequence over
`Q(t)`; any word for which the screen does not produce three exact losses is
fully censused over `Q(t)`. Exactly 4,094 words force at least three image
losses, hence at most 507 images. Exactly two are lossless.

For the two survivors, direct exact row reduction gives rank four and one of

```text
E = sigma*t*A,  F = sigma*t*B,
G = sigma*t*C/3,  H = sigma*t*D/3,    sigma in {-1,+1}.
```

The four displayed relations are independent, so membership in the rank-four
row space proves equality of the kernels. Reflection exchanges the two signs.
After taking `sigma=+1`, rotation normalizes the unit vector `A` to 1. The two
unit directions `(C+t)/6` and `(C-t)/6` imply that `C` is real and `C^2=33`.

## Independent polynomial elimination

Write

```text
B=b+t*y,  D=d+t*z,  C=c,  c^2=33,
```

with real `b,y,d,z`. The reviewer independently expands all 36 squared-unit
equations as polynomials over `Q(c)`. Thirteen monomials occur, and their
coefficient matrix has rank seven. Exact row-space reduction, without using
the submitted 21 combination terms, proves that the following four
polynomials lie in the span:

```text
b^2 + 3*y^2 - 5,   y,   z,   d-c*b.
```

Consequently `y=z=0`, `b=+/-sqrt(5)`, `c=+/-sqrt(33)`, and `d=bc`. These four
sign choices are precisely the sign changes of `sqrt(5)` and `sqrt(11)` in
the archived coordinates. The reviewer explicitly matches the normalized
parameter columns to those four Galois arrays, checks 510 distinct points in
each, and performs all 10,016 source-edge incidence checks exactly.

## Reproduction and controls

The submitted 51,226-byte certificate has SHA-256
`13aab3ef8e66770536ed4c064b41f3631ecab9b631148d7145e66d25087a0759`.
Its manifest passes. The source verifier and its 15 malformed-certificate
controls pass in normal and optimized modes, and its deterministic producer
regenerates the certificate byte-for-byte in about 37 seconds.

The independent audit uses neither the certificate's bases nor its
orientation/polynomial witnesses. Its normal and optimized outputs agree
byte-for-byte, with SHA-256
`7a76efe0b2aec9229f2a571fac6f039c62e5dd9faee67bd87ac2b673dc5eed4d`.
Reviewer controls exercise 5,000 exact quadratic-field cases, 625
finite-field-extension cases, row-space membership and nonmembership,
multiquadratic norms, and direction normalization. The complete sequential
replay takes about seven minutes under CPython 3.11 and ends with
`REPRODUCED_ACCEPT_REVIEW_H3945`.

## Scope and trust boundary

This accepts the classification for maps with at least 508 images. It does not
classify maps with at most 507 images, modified graphs, or constructions not
obtained as H510 quotients. It supplies no sub-509 graph and does not improve
the record.

No SAT solver, approximate coordinate test, private search output, or omitted
large proof object enters the geometric proof. Residual trust includes the
elementary equal-circle and Euclidean-normalization arguments, independence
of the multiquadratic basis, the pinned source alignment, both source and
reviewer implementations, Python integer and `Fraction` semantics, SHA-256,
the operating system, and hardware. The source graph's five-chromatic status
is imported from the published H510 construction and prior certified work; it
is needed only to interpret a hypothetical 508-image quotient as a campaign
breakthrough. This is a computer-assisted proof review, not proof-assistant
formalization.
