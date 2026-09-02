# Exact K-rational rotation classification for the Parts-509 L/S gadgets

## Result

Let `L` be vertices `0..373` and `S` vertices `374..508` of Jaan Parts's
strict 509-point unit-distance graph.  Thus `L` has 374 vertices and 1,860
internal unit edges, `S` has 135 vertices and 552 internal unit edges, and all
coordinates lie in

\[
K=\mathbb Q(\sqrt3,\sqrt5,\sqrt{11}).
\]

For a rotation matrix

\[
R(c,s)=\begin{pmatrix}c&-s\\s&c\end{pmatrix},\qquad c^2+s^2=1,
\]

write `G(c,s)` for the **strict** unit-distance graph on the geometric point
set `L ∪ R(c,s)S`.  The exact computer-assisted classification is:

> Among all rotations with `c,s ∈ K`, `G(c,s)` is 5-chromatic for exactly six
> ordered pairs `(c,s)`.  They form three abstract isomorphism classes.  Every
> one of the six graphs has 509 distinct points, 2,442 strict unit edges, and is
> 5-vertex-critical.  Every other such rotation is 4-colourable.

The six rotations are:

| event | `c` | `s` | class representative |
|---:|---|---|---:|
| 108 | `-1/2` | `-sqrt(3)/2` | 108 |
| 215 | `-(17+21sqrt(5))/64` | `(-17sqrt(3)+7sqrt(15))/64` | 108 |
| 109 | `-1/2` | `sqrt(3)/2` | 109 |
| 216 | `(-17+21sqrt(5))/64` | `(17sqrt(3)+7sqrt(15))/64` | 109 |
| 690 | `17/32` | `-7sqrt(15)/32` | 690 |
| 789 | `1` | `0` | 690 |

Event 789 is Parts's published placement.  The certificate contains explicit
edge-preserving permutations `215 -> 108`, `216 -> 109`, and `789 -> 690`;
the class pairing is not inferred from equal hashes.  Degree-seeded exact
colour refinement is discrete on all six graphs.  The three resulting
canonical edge hashes are distinct, hence the three classes are pairwise
nonisomorphic.

This does **not** improve the 509-vertex record or the bounds
`5 <= chi(R^2) <= 7`.  It closes one algebraically natural one-parameter
sub-search for the fixed Parts gadgets.  It says nothing about rotations whose
matrix entries are outside `K`, other choices of `L` or `S`, translations,
reflections, or delete-and-repair modifications.

## Why the rotation search is finite and exact

For nonzero `p ∈ L` and `q ∈ S`, put

\[
A=p_xq_x+p_yq_y,\quad B=p_yq_x-p_xq_y,\quad
C=(\lVert p\rVert^2+\lVert q\rVert^2-1)/2.
\]

The pair is a cross unit edge after rotation precisely when

\[
Ac+Bs=C,\qquad c^2+s^2=1.
\]

Since `A^2+B^2=||p||^2||q||^2`, the orthogonal coordinate
`t=-Bc+As` satisfies

\[
t^2=\Delta=\lVert p\rVert^2\lVert q\rVert^2-C^2.
\]

If `c,s ∈ K`, then `t ∈ K`.  Conversely, every square root `t ∈ K` of
`Delta` gives the event rotation

\[
c=\frac{AC-Bt}{\lVert p\rVert^2\lVert q\rVert^2},\qquad
s=\frac{BC+At}{\lVert p\rVert^2\lVert q\rVert^2}.
\]

This is an if-and-only-if enumeration, not a numerical angle grid.  Exact
grouping over all cross pairs gives:

- 547 geometrically admissible squared-radius pair classes;
- 37,861 admissible noncentral cross pairs;
- 14,512 cross pairs whose event rotations lie in `K`, including 576 tangent
  pairs;
- 790 distinct exact event rotations;
- 12 rotation-invariant cross edges from the origin.

At the 790 events, 784 graphs have explicit proper 4-colourings.  A single
proper 4-colouring handles every non-event rotation, because its labeled graph
has only the 12 invariant cross edges.  The independent checker also enumerates
all L/S coordinate coincidences, proves every coincidence rotation is among
the 790 unit-edge events, and checks that the stored colourings agree on all
1,392 coincident-label incidences.  Thus the witnesses descend to colourings of
the strict geometric point sets even when an event has fewer than 509 distinct
points.

## The six exceptional rotations

The search found six SAT-negative events.  Their status is certified as
follows.

- Events 108 and 109 have independently regenerated 4-colour CNFs with 2,036
  variables and 10,280 clauses.  CaDiCaL 2.1.2 produced binary DRAT traces, and
  `drat-trim` at commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` reported `s VERIFIED` on both.
- Each alternate representative has 509 explicit proper 4-colourings, one for
  every vertex deletion: 1,018 solver-free positive witnesses in total.  An
  explicit proper 5-colouring is also stored for each representative.
- Event 789 is the published Parts graph and depends on the sibling exact
  criticality certificate.  The exact isomorphism `789 -> 690` transfers its
  non-4-colourability and vertex-criticality to event 690.
- The exact isomorphisms in the other two pairs transfer the corresponding
  statements to events 215 and 216.

The proof logs are intentionally not committed.  Their bound metadata is:

| event | CNF SHA-256 | DRAT SHA-256 | proof bytes | `drat-trim` core |
|---:|---|---|---:|---|
| 108 | `b59275f43657f668d21b5fe9ca02488d57b2283d940c454fbdb4aa5617eff426` | `04e7ac357ba9e929a2270d125ac4c761c48d40fa83403b9f854029251458a4b6` | 6,403,115 | 9,233 input clauses; 52,062 lemmas; 3,755,365 resolution steps |
| 109 | `e03f90aa72ae88cd03c85f7cf8db57aaa99ecd7c8df32caff4ef22326ae302fa` | `154680a5cd140371f2b6bafdb3481dd7e52c56cf8a97d0b9700996c960f22a97` | 8,516,531 | 9,204 input clauses; 61,868 lemmas; 3,638,395 resolution steps |

Both checked cores used zero RAT lemmas.

## Reproduction

Use CPython 3.11 or newer and keep the environment under `/scratch`:

```bash
python3 -m venv /scratch/parts509-rotation-venv
/scratch/parts509-rotation-venv/bin/pip install -r requirements.txt

/scratch/parts509-rotation-venv/bin/python independent_check.py \
  rotation_certificate.json criticality_certificate.json

/scratch/parts509-rotation-venv/bin/python criticality.py verify \
  rotation_certificate.json --output criticality_certificate.json
```

Expected final lines are in `expected_check.txt`.  The independent checker uses
its own coordinate parser, SymPy's `AlgebraicField` arithmetic, and a recursive
exact square-root-membership algorithm for the multiquadratic tower.  It
imports neither the search program nor the sibling Parts checker.

Regenerate the scan and criticality witnesses under `/scratch`:

```bash
/scratch/parts509-rotation-venv/bin/python rotation_scan.py \
  ../hadwiger_nelson_parts509_criticality/parts509.vtx \
  /scratch/rotation_certificate.new.json

/scratch/parts509-rotation-venv/bin/python criticality.py generate \
  /scratch/rotation_certificate.new.json \
  --output /scratch/criticality_certificate.new.json
```

Regenerate and check an alternate-class proof (repeat with event 109):

```bash
/scratch/parts509-rotation-venv/bin/python criticality.py cnf \
  rotation_certificate.json --event 108 \
  --output /scratch/parts509-rotation-108.cnf

cadical /scratch/parts509-rotation-108.cnf \
  /scratch/parts509-rotation-108.drat
drat-trim /scratch/parts509-rotation-108.cnf \
  /scratch/parts509-rotation-108.drat
```

CaDiCaL returns status code 20 for a proved UNSAT instance.  Do not place the
CNFs, solver transcripts, or DRAT traces in this repository.

## Trust boundary and literature status

- Exact geometry in the search trusts CPython `Fraction`, the coordinate
  source in the sibling criticality contribution, SymPy parsing/denesting, and
  SymPy's algebraic-field membership test.  No floating-point comparison is
  used to decide an edge or merge an event.
- The independent checker changes both the number-field representation and the
  square-root-membership algorithm.  It uses 80-digit numerical evaluation
  only to choose the sign of a nonzero exactly represented real algebraic
  number; equality and certificate comparisons are exact.
- Positive coloring and deletion claims are explicit witnesses checked without
  a solver.  The two new negative claims depend on the recorded CNF bridge,
  scratch-only proof bytes with the stated hashes, and `drat-trim`.  The
  published-alignment class also depends on the sibling Parts-509 criticality
  certificate.
- Pairing within each exceptional class is checked by an explicit permutation
  and exact edge incidence.  SHA-256 is not used as an isomorphism proof.
- The exhaustive statement is only for `c,s ∈ K` and these fixed gadgets.

Parts describes type-M graphs as unions `L ∪ rho S` and states that working
constructions with other rotations were not known there.  The six placements
above may reflect known type-M subtype symmetries or unpublished search data;
no novelty or priority claim is made for the individual 509-vertex drawings.
The contribution is the exact, independently checkable classification of the
stated fixed-gadget `K`-rational rotation family.

Primary references:

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137–166,
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5*, Geombinatorics 28(1) (2018), 32–50,
  <https://arxiv.org/abs/1805.12181>.

## Files

- `rotation_scan.py` — exact event enumeration and SAT witness generation.
- `rotation_certificate.json` — 790 exact rotations, cross edges, 784 event
  colorings, the generic coloring, and summary counts.
- `criticality.py` — alternate-class witness generation, CNF bridge, exact
  isomorphism certification, proof binding, and compact verification.
- `criticality_certificate.json` — explicit five/deletion colorings,
  exceptional-class isomorphisms, canonical summaries, and DRAT metadata.
- `independent_check.py` — independent exact enumerator and witness checker.
- `expected_check.txt` — compact expected output.

