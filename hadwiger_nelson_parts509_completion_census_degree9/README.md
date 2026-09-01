# Exact completion-center census and degree-9 replacement closure for Parts 509

## Results and scope

Let `P` be the 509 algebraic points in Jaan Parts's record construction, and
write

\[
d_P(q)=|\{p\in P:\|p-q\|_2=1\}|.
\]

The exact census in this directory establishes that there are exactly 1,667
points `q` in the plane with `d_P(q) >= 3`.  Of these, 509 are themselves
Parts vertices and 1,158 are external points.  The complete degree census is:

| degree | all centers | Parts vertices | external centers |
|---:|---:|---:|---:|
| 3 | 461 | 0 | 461 |
| 4 | 328 | 6 | 322 |
| 5 | 222 | 42 | 180 |
| 6 | 175 | 56 | 119 |
| 7 | 91 | 62 | 29 |
| 8 | 72 | 45 | 27 |
| 9 | 56 | 40 | 16 |
| 10 | 73 | 69 | 4 |
| 11 | 50 | 50 | 0 |
| 12 | 61 | 61 | 0 |
| 13 | 28 | 28 | 0 |
| 14 | 15 | 15 | 0 |
| 15 | 14 | 14 | 0 |
| 16 | 6 | 6 | 0 |
| 17 | 4 | 4 | 0 |
| 18 | 4 | 4 | 0 |
| 22 | 6 | 6 | 0 |
| 36 | 1 | 1 | 0 |

Consequently an external point has at most ten unit neighbors in `P`.  Exactly
four attain ten; they are the four points treated in the earlier
`hadwiger_nelson_parts509_degree10_replacements` contribution.  There are
exactly sixteen external degree-9 points.

For every one of those sixteen degree-9 points `q` and every two-element set
`D` of Parts vertices, a compact certificate gives a proper four-coloring of
the **strict** unit-distance graph on

\[
(P\setminus D)\cup\{q\}.
\]

This closes

\[
16\binom{509}{2}=2,068,576
\]

degree-9 two-delete/one-add candidates on 508 vertices.  Combining this result
with the earlier degree-10 certificate closes all

\[
20\binom{509}{2}=2,585,720
\]

such candidates whose added point has at least nine unit neighbors in `P`.

This is a finite negative local search, not a graph with fewer than 509
vertices and not a proof that the record is globally minimal.  It does not
cover the 677 external centers of degrees 4 through 8, points introduced in
groups, coordinate perturbations, or constructions outside the Parts point
set.

## A finite reduction for every one-point replacement

The census reduces the continuous choice of one added point to a finite list.
If `d_P(q) <= 3`, then after deleting any two Parts vertices, any proper
four-coloring of a one-vertex deletion of the Parts graph restricts to the
remaining base graph and leaves a color available for `q`.  Thus a
non-four-colorable graph of the form `(P-D)+q` would require `d_P(q) >= 4`.

Every point with at least three unit neighbors occurs in the exact census, so
only the 697 external centers of degrees 4 through 10 can possibly yield a
508-vertex one-point replacement.  The degree-9 and degree-10 certificates
close 20 of these, leaving 677 exact geometric candidates of degrees 4 through
8.  This reduction does not assert that any of the remaining candidates works.

## Why the center list is complete

Three distinct points on a unit circle are noncollinear and determine their
circle center uniquely.  If their squared side lengths are `s`, `t`, and `u`,
then their circumradius is one exactly when

\[
stu=4st-(s+t-u)^2.
\]

All Parts coordinates lie in
`Q(sqrt(3),sqrt(5),sqrt(11))`.  `points.tsv` writes every coordinate as sixteen
integer coefficients in the eight-element squarefree-radical basis, with
common scale 96.  `verify_centers.py` checks this file against the original
coordinate expressions, then checks every one of the 1,667 listed centers
against all 509 vertices with rational multiquadratic arithmetic.  It performs
848,503 exact incidence decisions and confirms that the listed degrees,
neighbor sets, existing-vertex markers, and histograms agree.

Independently, `count_unit_circumcircles.cpp` evaluates the circumradius
identity on all

\[
\binom{509}{3}=21,849,334
\]

triples.  Two finite-field homomorphisms are sound rejection filters: an exact
zero maps to zero, so a nonzero residue can reject a triple without losing a
solution.  Every survivor is rechecked coefficient-by-coefficient over the
integers.  It finds exactly 95,406 unit-circumcircle triples.  The manifest
independently satisfies

\[
\sum_q \binom{d_P(q)}3=95,406.
\]

Distinct centers cannot account for the same triple, so equality of these two
counts proves that the manifest is complete.  The floating-point clustering in
`generate_manifest.py` is therefore outside the completeness trust boundary;
it is only a way to propose the manifest that the exact checks certify.

The C++ integer-width bound is explicit.  Scaled coordinate coefficients have
absolute value at most 144, so difference coefficients are at most 288.  A
squared-distance coefficient is at most

\[
B=2\cdot8\cdot165\cdot288^2=218,972,160.
\]

A field product coefficient is bounded by `1320` times the product of the two
input coefficient bounds.  The full scaled circumradius identity is therefore
bounded in absolute value by

```text
1320^2 B^3 + 9216 (4*1320 B^2 + 1320*(3B)^2)
= 18,294,255,895,343,551,074,571,124,736,000 < 2^104,
```

well inside signed 128-bit arithmetic.

## Replacement certificate

The previously certified Parts vertex-deletion rows settle 2,059,140 of the
2,068,576 degree-9 instances: after restricting a row by the second deletion,
the neighbors of the new point omit a color.  The remaining 9,436 instances
occur on 8,415 deleted pairs.

`certificate.bin` contains 9,199 proper coloring witnesses; one witness can
cover several degree-9 points for the same deleted pair.  Its 16-byte header is
followed by fixed 132-byte records:

- two little-endian 16-bit deleted vertex indices;
- 510 two-bit colors packed into 128 bytes, including the added point as
  vertex 509.

The primary and independent solver-free verifiers both replay 22,271,691
retained base-edge inequalities, check the added-point neighborhood condition,
and confirm that every residual instance is covered.  MiniSat generated the
committed witnesses but is not trusted by the result.

## Fast verification

Use CPython 3.11 or newer and a C++20 compiler.  Keep environments and compiled
outputs under `/scratch`.

```bash
python3 -m venv /scratch/parts509-census-venv
/scratch/parts509-census-venv/bin/pip install -r requirements.txt

/scratch/parts509-census-venv/bin/python verify_centers.py \
  points.tsv centers.json

g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra \
  count_unit_circumcircles.cpp \
  -o /scratch/count_unit_circumcircles
/scratch/count_unit_circumcircles points.tsv

/scratch/parts509-census-venv/bin/python \
  degree9_replacements.py verify certificate.bin
/scratch/parts509-census-venv/bin/python \
  independent_check.py certificate.bin
```

Expected center-verifier summary:

```text
all_checks=true
centers_with_at_least_three_neighbors=1667
external_centers=1158
external_maximum_unit_neighbors=10
external_maximizers=4
external_degree_9_centers=16
exact_incidence_checks=848503
unit_circle_triples_accounted_for=95406
```

Expected exhaustive-counter summary:

```text
all_checks=true
vertices=509
triples_checked=21849334
first_modular_filter_survivors=95566
second_modular_filter_survivors=95406
exact_unit_circumcircle_triples=95406
```

Both replacement verifiers should report:

```text
all_checks=true
candidate_points=16
two_deletion_instances=2068576
instances_covered_by_prior_deletion_rows=2059140
residual_instances=9436
certificate_records=9199
retained_edge_inequality_checks=22271691
```

## Regeneration

Regenerate the numerical proposal followed by exact center reconstruction:

```bash
/scratch/parts509-census-venv/bin/python generate_manifest.py \
  /scratch/centers-regenerated.json \
  --points-output /scratch/points-regenerated.tsv
cmp centers.json /scratch/centers-regenerated.json
cmp points.tsv /scratch/points-regenerated.tsv
```

Regenerate the degree-9 coloring witnesses:

```bash
/scratch/parts509-census-venv/bin/python degree9_replacements.py generate \
  /scratch/degree9-certificate-regenerated.bin \
  --solver minisat22
/scratch/parts509-census-venv/bin/python degree9_replacements.py verify \
  /scratch/degree9-certificate-regenerated.bin
```

SAT solvers can return different valid colorings, so a regenerated certificate
need not have the committed byte hash.

## Hashes

```text
points.tsv
  f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50
centers.json
  47867a68f8fec9dc84dd69f04465cdad2e69fb68bcbb08e95ae4b91b16d92d9c
certificate.bin
  a75644d0bd7701900f1eb62af83965b552b445ad8e9cb62d92837c2d9172ff0b
```

## Trust boundary and provenance

- The coordinate-source bridge trusts the published input, CPython
  `fractions.Fraction`, SymPy 1.14.0 parsing/denesting, and the sibling
  `parts509.py` parser.  Once `points.tsv` is checked, the C++ census uses only
  integer arithmetic.
- Census completeness trusts the circumradius identity, uniqueness of a circle
  through three noncollinear points, the small C++ implementation, the stated
  signed-128-bit bound, and the compiler.  Finite-field evaluations only reject
  candidates; every accepted triple receives a full exact check.
- Replacement colorability trusts the exact center-neighborhood manifest, the
  strict 2,442-edge manifest, the earlier 509 deletion-coloring certificate,
  and the two direct witness checkers.  The SAT solver is outside the
  verification boundary.
- No proof-assistant formalization was performed.

Primary construction source: Jaan Parts, *Graph minimization, focusing on the
example of 5-chromatic unit-distance graphs in the plane*, *Geombinatorics*
29(4) (2020), 137–166, <https://arxiv.org/abs/2010.12665>.

The complete center census was also obtained concurrently by a distinct exact
pair-intersection approach; this directory's exhaustive triple counter is an
independent completeness mechanism.  No novelty or priority claim is made for
the census.  The degree-9 two-delete closure extends the committed degree-10
subsearch, but targeted literature and graph searches do not establish
priority for that finite computation.
