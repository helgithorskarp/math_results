# Every target-sized residue hyperplane section of de Grey's graph is four-colourable

For the exact 1,581-point construction and coefficient projection defined below,
**every affine residue hyperplane selecting at most 508 vertices induces a
four-colourable unit-distance graph**. Every subgraph of each such selection is
also four-colourable. This closes the complete specified extraction family and
finds no record improvement.

There are 9,840 affine hyperplanes in the residue space. Exactly **2,118** select
at most 508 points, giving **2,100 distinct supports**. There are **32 sections of
order exactly 508**. The decision uses one colouring of the full graph with a
bridge endpoint removed and 120 short positive words. It does not classify
arbitrary target-sized subsets, other residue projections, or other moduli.

## Exact source construction

The source is the construction in Section 6 of
[de Grey, arXiv:1804.02385v2](https://arxiv.org/html/1804.02385v2).
[seeds.json](seeds.json) transcribes the 39 displayed points as integer rows
(a,b,c,d) meaning

```
((a+b*sqrt(33))/12, (c*sqrt(3)+d*sqrt(11))/12).
```

Let Sb be the union of their images under all rotations through multiples of
60 degrees and reflection in the x-axis; it has 397 points. Put

```
Sa = Sb minus {(-1/3,0),(1/3,0)},
r  = (7+i*sqrt(15))/8,
Y  = Sa union r*Sb,
s  = (31+3*i*sqrt(7))/32,
G  = Y union {-2+s*(z+2) : z in Y}.
```

Thus Sa has 395 points, Y has 791, and G has 1,581. Both r and s have norm one.
They place equal-radius linking points at unit distance: their real parts are
respectively 1-1/(2*2^2) and 1-1/(2*4^2). The outer copies share the point -2.
The strict unit-distance graph on G has **7,877 edges**, checked here from all
point pairs. This package needs no chromatic lower-bound assertion from the
paper; it independently reconstructs the literal point set and uses positive
colourings only.

Coordinates lie in Q(sqrt(3),sqrt(5),sqrt(11),sqrt(7)), with common scale 3072.
The coefficient order for each of x and y is the following squarefree-radicand
order, with positive square roots:

```
1,3,5,15,11,33,55,165,7,21,35,105,77,231,385,1155.
```

Vertices are labelled by lexicographic order of the 32 integer coefficients,
x first and then y. The endpoint (2,0) is label 1580.

## Residue projection and exhaustive family

In this fixed coordinate frame, the nonzero x-coefficient columns have
radicands and common divisors as follows.

| Radicand R_j | 1 | 5 | 33 | 165 | 21 | 105 | 77 | 385 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Column gcd g_j | 1 | 3 | 1 | 1 | 3 | 3 | 3 | 9 |

Write each x-coordinate uniquely as

```
x(p) = (1/3072) * sum_j g_j*c_j(p)*sqrt(R_j),   c_j(p) integral,
f(p) = (c_0(p),...,c_7(p)) modulo 3 in F_3^8.
```

The gcds are recomputed across the complete source; no coefficient truncation
or rounding is used. There are 205 distinct residue vectors. This projection
is an explicit arithmetic selection rule, not a claim that the number field
maps to F_3 or that physical lines are being intersected.

For every nonzero normal a in F_3^8 and b in F_3, select

```
S(a,b) = {p in G : a dot f(p) = b}.
```

Normalize a by making its first nonzero coordinate 1. Each affine hyperplane
has exactly one such description, since multiplying both a and b by 2 is the
only other nonzero scalar choice. Hence there are (3^8-1)/2 = 3,280 normals and
3*3,280 = **9,840 hyperplanes**. Every one is enumerated before the vertex-order
predicate is applied.

| Level b | Admissible hyperplanes | Distinct supports | Orders |
|---|---:|---:|---|
| 0 | 138 | 120 | 487 through 505 |
| 1 or 2 combined | 1,980 | 1,980 | 129 through 508 |
| All | 2,118 | 2,100 | 129 through 508 |

Distinct hyperplanes can have the same intersection with this finite source.
The 18 duplicate descriptions all occur at level zero. All 32 sections with
508 vertices have nonzero level. The proof checks descriptions and supports;
no heuristic sample, cutoff prefix, or unresolved case is substituted for the
complete candidate space.

## Positive certificate

The residue of the endpoint (2,0) is zero. The supplied `base_word` properly
colours **all of G except this one endpoint**. Therefore every nonzero-level
section inherits a four-colouring, even when its order exceeds 508. This part
requires only checking the word and the endpoint's zero residue.

Each of the remaining 120 distinct target-sized zero-level supports has an
entry `{normal,word}`. The eight-character normal specifies its defining
zero-level equation; the word assigns colours `0123` to selected vertices in
increasing global label order. Duplicated supports are rejected even if their
normal strings differ. The verifier requires equality between the certified
support set and the entire computed zero-level target family.

The base word has 7,870 checked edge inequalities. The exception words have
125,276, for **133,146 independently checked inequalities** in total. The
certificate contains no SAT proof or unverified negative verdict. Its
65,327 bytes have SHA-256

```
b4ff0d1a41f3353be1777247a6606191c1b2876acb4fec9888b8e272e64fb067
```

## Independent geometry and enumeration

[geometry.py](geometry.py) constructs the points with integer coefficient
vectors, an iterative sixfold orbit, and bit-indexed radical multiplication.
For the edge census it first tests the exact constant coefficient of the
squared distance, then all remaining coefficients. The constant coefficient
is a necessary equality, not a bound on the physical distance. There are 8,689
survivors of that first test and 7,877 exact edges.

[verify.py](verify.py) imports no producer or solver code. It reconstructs the
seed orbit using twelve explicit orthogonal matrices, rational coefficients,
and dictionaries indexed by actual squarefree radicands; multiplication uses
gcd reduction. It independently builds both affine unions and every coordinate.

For all **1,248,990 unordered pairs**, the auditor first evaluates the scaled
integer radical expressions modulo 2269, with roots of (3,5,11,7) equal to
(931,158,418,1063). It checks all four root identities. These define a
homomorphism from the integer radical ring; denominators have already been
cleared. Any exact unit pair must pass. The auditor then expands the squared
distance exactly for all 8,350 survivors, accepting precisely the 7,877 edges.
Modular equality never certifies an edge. Independence of the four prime square
classes makes the final rational coefficient comparisons exact.

For sections, the producer enumerates every ternary normal and filters on its
leading digit, then evaluates it on residue fibres. The auditor instead
chooses the leading nonzero position and enumerates all tails; it evaluates
each normal directly on every vertex. It confirms every hyperplane, every
cardinality, the complete exception set, and all final colourings.

This is author-run independent checking, not independent-author peer review
or formal proof-assistant verification. The trust boundary comprises the
explicit seed transcription and construction formulas, finite enumerations,
ordinary Python exact arithmetic, and the directly checked positive words.
The reported five-chromatic lower bound for the full source is not imported.

## Reproduction and controls

Python 3.11 or later and its standard library suffice; no external graph file
or network access is required after obtaining this package.

```bash
python3 -B verify.py --check-expected
python3 -B controls.py
python3 -O -B verify.py --check-expected
python3 -O -B controls.py
sha256sum -c SHA256SUMS
```

[expected.json](expected.json) pins the deterministic audit report. Coordinate
and sorted `u v` edge streams, each with a newline after every row, have hashes

```
coordinates 40b27b53176a846efe80a1f40ce685b7aaf89d6f3988969da112caa9c493c5e3
edges      a20b27f728af08a9aaacbc60cbaa4ef095f62e4c47ef8ab87dcc0c0233b04675
```

[controls.py](controls.py) reconstructs all affine hyperplanes in dimensions
one, two and three by spanning every affine basis, independently of normal
vectors. It gets 3,12,39 hyperplanes. It then exhausts all 512 subsets of F_3^2
and every applicable vertex threshold, giving 2,816 cases, including empty
fixtures and duplicate finite intersections. Further checks cover 256 radical
basis products, equality of both full point/edge/section reconstructions, and
18 invalid-input rejections, including a wrong modular root and duplicate
support under another equation. Normal and optimized verifier and control
reports agree; details are in [controls_expected.json](controls_expected.json).

Optional discovery uses `python-sat==1.9.dev15` and CaDiCaL195:

```bash
python -B generate.py --out /scratch/degrey-residue-regeneration
```

The output directory must not already exist. This regenerated the certificate
byte for byte in 6.74 seconds. One 791-vertex half query used 14,556 conflicts;
all 120 exception queries were SAT with at most 26 conflicts each. Each query
had the same fixed 200,000-conflict budget. There were no UNKNOWN outcomes or
budget increases. The independent verifier took 7.08 seconds with peak child
RSS 32,176 KiB in the recorded Python 3.11.2 environment. Source and compact
proof data are committed; exploratory tables and logs stay outside Git.

## Campaign boundary

The 2026-09-07T02:23Z coordination instruction was read. This is an arithmetic
extraction mechanism on a distinct exact source, separate from the retired
Parts compression, Haugland metric-ball, and Heule catalogue-block families.
The E477 classification's new independent acceptance and the teammate's G372
and generalized Mycielski transfer results were read as separate context; none
is a mathematical premise. A scoped prepublication graph refresh through
height 3658 found no overlapping new result. The late Mycielski source was
inspected before publication.

The complete residue-hyperplane gate is retired. No new modulus, coordinate
projection, codimension, or later major phase is started here. Arbitrary
<=508-vertex subsets and the overall five-chromatic record target remain open.
No priority claim is made for the original construction or residue-selection
heuristic.
