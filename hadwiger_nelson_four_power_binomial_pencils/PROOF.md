# Homogeneous A5 pencils cannot concur

This package studies the fixed-scale plane point set

    A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
    T = {0,1,omega},  omega = (1+i sqrt(3))/2.

The 243 digit labels may coincide. A unit event is the equation that an
Eisenstein-unit coefficient displacement has squared modulus one. Coefficients
belong to `{0} union {six Eisenstein units}`, modulo a common unit multiplier.
Reduction modulo 2 identifies the Eisenstein integers with F4. A *homogeneous
full pencil* consists of the five projective directions of a rank-two subspace
of F4^4, with constant coefficient zero. A monomial direction is excluded from
the interface: all nonconstant monomial unit events have the same physical
unit-circle locus.

## 1. Statements and scope

**Four-position binomial theorem (exact computer-assisted).** Every full
homogeneous pencil using all four nonconstant positions and containing a
binomial direction is nonconcurrent, for every choice of its Eisenstein-unit
lifts. This holds even after independently complexifying the coordinates x,y
in the equations for z=x+i sqrt(3)y.

There are exactly 189 such pencils and 387,072 lifted five-equation systems.
The complete class contains the 162 retained homogeneous binomial pencils
in the pinned h4195 residual and also the 27 intrinsic members excluded before
that frontier. None of the latter is assumed excluded in this computation.
The initial asymmetric residual pencil is h4195 index 412 (intrinsic index 2):

    ((0,0,1,1),0), ((1,1,0,2),0), ((1,1,1,3),0),
    ((1,1,2,0),0), ((1,1,3,1),0).

Its six D3 images have distinct residual indices
412,1008,710,416,1012,714. No symmetry quotient or parameter chamber is used.

**Homogeneous-pencil corollary.** No full homogeneous pencil of five
nonmonomial A5 unit events is simultaneously active at any physical complex
radix z. This combines the present 189-pencil theorem with the previously
proved 54 four-position no-binomial pencils and 36 three-position pencils.
Thus all 279 intrinsic homogeneous nonmonomial pencils, with 502,272 raw
lifts, are physically excluded. The prior three-position theorem is a physical
result; the corollary does not upgrade it to a complex-affine statement.

The theorem concerns these exact radix powers 1,2,3,4 and their fixed unit
scale. It is not a theorem about arbitrary four input vectors or arbitrary
exponent quadruples. It does not exclude nonhomogeneous pencils or every
higher-cardinality cover. Additional active events cannot make an impossible
homogeneous five-section subsystem possible, but other cover types remain.
It neither closes A5 nor constructs a five-chromatic graph or improves the
published 509-vertex record.

## 2. Intrinsic finite classification

Write a rank-two generator matrix with four columns in F4^2. A nonzero row
combination vanishes on precisely one projective column direction. If all
four positions occur and there is no monomial direction, no column is zero
and no projective column direction occurs three times. A binomial occurs
exactly when a column direction is repeated twice. Therefore the possible
multiplicity partitions are (2,1,1) and (2,2).

For (2,1,1), choose the repeated direction in 5 ways, the two singleton
directions in C(4,2) ways, the positions in 4!/2! ways, and independently
scale each column in 3^4 ways. The result is 29,160 ordered generator
matrices. For (2,2), the count is C(5,2)*6*3^4=4,860. Every rank-two row
space has |GL(2,4)|=(16-1)(16-4)=180 ordered bases. There are consequently
162 and 27 pencils, respectively. Their support profiles are (2,3,3,4,4)
and (2,2,4,4,4).

Each nonzero F4 coefficient has two unit lifts differing by sign. After
normalizing the first nonzero coefficient by common unit row scaling, a
support-s direction has 2^(s-1) distinct lifts. Both profiles have total
support 16, so each pencil has 2^(16-5)=2,048 lifted systems.

`interface.py` independently enumerates all 357 rank-two RREF spaces in
F4^4 and selects the stated property. `classification.py` uses only the
Python standard library and directly enumerates the projective columns.
The two methods agree entrywise on all 189 pencils. `RESIDUAL.json` retains
the literal 162 h4195 indices and signatures; optional `--residual` verifies
its exact intersection with the pinned historical export. The intrinsic
classification does not depend on any residual count or conservative
allowance.

For the corollary, a pencil with an unused position and no monomial must
use exactly three positions. Its three nonzero columns have distinct
projective directions. There are 36 such row spaces. With all four columns
nonzero, the remaining multiplicity pattern (1,1,1,1) gives the previous 54
no-binomial pencils. These disjoint possibilities exhaust the 279 spaces.
The 36 three-position pencils have 128 lifts apiece; hence the total lift
count in the corollary is 36*128+(54+189)*2048=502,272.

## 3. Exact norm equations and finite anchor coverage

A coordinate pair (a,b) denotes a+i sqrt(3)b, and its squared norm is
**a^2+3b^2**. Every displacement polynomial and unit event is regenerated
from the accepted h4105 architecture. The complete event inventory has
2,797 distinct curves, including the unit circle. Its canonical hash is
pinned. Each of the other 2,796 events has its projective F4 signature and
belongs to exactly one lift bucket.

For each pencil, order the five buckets by (size, ascending curve-ID list)
and take every pair from the first two buckets. There are 1,404 distinct
anchor pairs: eight for each of the 162 support-(2,3,3,4,4) pencils and four
for each of the 27 support-(2,2,4,4,4) pencils. Every concurrent full pencil
must occur in one of these intersections. No admissibility prefilter,
reflection restriction, real-root filter or inherited pair exclusion is used.

The producer changes coordinates by u=x+2y, retaining y. This is an
invertible rational linear change, x=u-2y. For each pair f,g it computes
Res_y(f(u-2y,y),g(u-2y,y)), factors this polynomial over Q, and computes a
fiber gcd over each irreducible quotient field. A nonrational fiber must
have a linear equation for y; otherwise generation fails explicitly. Each
rational exceptional u-fiber is factored separately in y, including all its
irreducible factors. All fibers in the selected domain are supported by this
procedure. Coordinates are restored to physical x,y before storage.

Components are represented by a primitive irreducible q(s) with positive
leading coefficient and reduced rational polynomials x(s),y(s). Rational
points use q=s. Otherwise either x+2y=s, or x+2y is rational and y=s.
These canonical separating forms make different records disjoint: sharing
one coordinate pair forces the same minimal polynomial and the same reduced
coordinate polynomials. Every embedding of a degree-d field gives a distinct
complex coordinate pair.

## 4. Independent completeness audit without solving nonlinear fibers

The checker works in the original x,y coordinates. It computes the
**unshifted** resultant R(x)=Res_y(f,g). A nonzero resultant guarantees that
every affine common zero projects to a root of R. For each irreducible
factor q_x, let K=Q[x]/(q_x), and compute

    h(y) = gcd(f(x,y),g(x,y)) in K[y].

An identically zero gcd would signal a whole vertical fiber and is rejected.
A constant gcd contributes no common point. Otherwise the number of distinct
y-roots over each embedding of K is

    m = deg(h) - deg(gcd(h,h')).

Characteristic zero makes the square-free part separable, so this fiber
contains exactly deg(q_x)*m distinct complex points. This calculation handles
nonlinear, nonrational fibers directly; it does not discard them or require
factorization over K.

For every component claimed on the pair, the checker substitutes its exact
coordinates into the original f and g. It also identifies its unique
q_x projection factor by exact substitution. The sum of component degrees
assigned to that factor must equal deg(q_x)*m. Because all claimed points
solve both equations and are disjoint by the canonical separating forms,
equality proves complete coverage. Every component must belong to at least
one pair, and every listed pair is audited.

This audit differs from the producer's shifted fiber solution: it never
solves the nonlinear unshifted fibers. It shares exact arithmetic libraries
and the initial norm equations. `fiber_controls.py` checks y^2=x, x^2=2,
then repeats the first equation as (y^2-x)^2. Both have four distinct complex
points although their raw fiber degrees differ. Missing and duplicated
components are rejected.

## 5. Concurrency, actual points and colourings

Every component is substituted into **all** 2,797 original event equations.
For every pencil and every component of each of its anchor pairs, at least
one whole bucket has no active curve. Hence every choice of one lift from
each of the five buckets fails to concur. This is a complete algebraic
statement, including components with no real embedding.

For physical graphs, q(s) is also checked irreducible and its real embeddings
are counted exactly. At every real embedding the coordinate polynomials are
real, so z=x+i sqrt(3)y is an actual plane parameter. Equality of algebraic
coordinates and unit-distance relations are constant across embeddings of
one irreducible component. Thus one exact field computation describes the
graph at every real root of that component.

The producer constructs every one of the 243 digit points, merges exact
coincidences, and obtains the complete edge union from the event ownership
inventory. The verifier examines **every pair of physical points**. It evaluates the
squared norm directly on the coordinate difference, with the following exact
cache. Choose one digit-label representative of each physical point. A formal
displacement has coefficients a+b*omega. Its first nonzero coefficient u+v*omega
is an Eisenstein unit; multiplying the entire row by its conjugate sends each
coefficient to

    (a*(u+v)+b*v) + (-a*v+b*u)*omega.

Rows with the same normalized result differ by a common unit rotation, so
their squared norms agree for every radix. One direct norm evaluation per
class therefore decides every pair in that class. This uses no event curve
or edge-owner table and remains valid through collisions. In an injective
243-point graph it reduces 29,403 norm evaluations to 2,801 while still
examining all 29,403 pairs. `--literal-distances` disables this cache for a
complete direct replay. Selected algebraic and collision fixtures compare
the two complete edge lists entrywise.

The checker compares the complete edge and collision maps with the producer's
hashes. Distinct original digit labels are never mistaken for distinct
physical vertices.

Positive three-colourings have the form sum(w_j*t_j) modulo 3, with t_j=0,1,2
for the digits 0,1,omega. The first weight is 1. The search permits zero
weights off the unit circle. The verifier checks both descent through every
collision and propriety on every unit edge; the search itself is not a
chromatic certificate. The surviving physical triangle 0,1,omega proves the
matching lower bound of three. The certified scope is the complete anchor
parameter envelope, not the entire A5 parameter plane.

## 6. Verified physical and algebraic counts

The full verifier passes with 1,539 distinct complex component records and
2,956 pair-component incidences. Exactly 1,469 components have real embeddings,
giving 4,320 distinct actual plane parameters; the other 70 components have no
real embedding. There are zero complex-affine full-pencil concurrences.
The independent unshifted audit covers 69 nonlinear nonrational fibers across
57 pairs, all represented in the completed point table.

All 4,320 complete physical graphs have chromatic number exactly three.
There are 4,120 injective parameters and 200 collision parameters, 188 of the
latter off the unit circle. The 12 circle parameters are exactly z^12=1 and
have graphs on 21, 27 or 84 physical points. The complete size distribution,
with 27 (vertex-count, edge-count) types, is in `EXPECTED.json`.
Exactly 3,996 parameters have two active event curves and the other 324 have
more, up to 811. All are included, without a generic-position assumption.

Fourteen positional weight vectors suffice. Thirty-six parameters use a zero
weight: 24 yield 129-point/195-edge graphs, six yield 162-point/189-edge graphs,
and six yield 162-point/219-edge graphs. For one representative of each of
these three types, the controls check all 81 normalized weight vectors:
exactly three work, and none is all nonzero. This is a statement about the
displayed positional witness family, not a chromatic lower-bound claim about
arbitrary colourings. Positive full graph witnesses and the fixed triangle
establish the exact chromatic decision.

## 7. Dependencies and trust

The homogeneous-pencil corollary uses the public proofs
`hadwiger_nelson_homogeneous_three_power_pencils/PROOF.md` and
`hadwiger_nelson_four_power_no_binomial_pencils/PROOF.md`. Both have received
independent acceptances. Their substantive mathematical commits and the
review sources are pinned in CONTEXT.json. The current 189-pencil theorem
and physical anchor analysis do not depend on those exclusion conclusions.

The written reductions are not formalized. CPython, SymPy and python-flint,
exact polynomial factorization, fiber Euclid, real-root counting, and the
imported norm/coordinate helper source remain trust boundaries. The distinct
author algorithms and controls are author validation, not independent-author
review of this new result. The earlier 57 unsupported unshifted pairs are
preserved as a documented failed representation; the completed shifted
computation and unshifted cardinality audit cover them explicitly.

No global quotient or allowance from h4117/h4175/h4177 is used or repaired.
The stale Discovery Net ledger is reported separately from accepted
broadcasts. Complete local root tables remain reproducible generated data
and are not committed to the repository.
