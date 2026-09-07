# One capped circumcentre-discovery trajectory from EI G79

The saved output has **508 distinct plane points and 2,561 strict unit edges**.
An independent exact checker verifies a proper four-colouring. No graph
requiring five colours was found. This is one bounded discovery experiment,
not a classification of the source field or of circumcentre growth.

The preset discovery budget was one trajectory from 79 to at most 508 points,
100,000 SAT conflicts per query and 500,000 over the trajectory. All 430
prefix queries returned SAT; no UNKNOWN or UNSAT occurred. The run used
9,033 conflicts and 22.74 seconds. It stopped at the original vertex cap.
There was no extra orientation, restart, enlarged cap, or exhaustive closure.
A validation replay repeated the identical trajectory without adding candidates.

## Source and coordinates

The source is G79 from Section 2 of
[Exoo and Ismailescu, arXiv:1805.00157v1](https://arxiv.org/pdf/1805.00157).
`seed40.json` transcribes their 40 coefficient rows `[a,b,c,d]`, representing

```
((a sqrt3+b sqrt11)/36, (c+d sqrt33)/36).
```

We rotate all points by minus pi/2, which preserves all distances, then append
the nonzero points of the copy rotated by
`rho=(119+3i sqrt247)/128`. The resulting 79 points have exactly 165 unit
edges and 118 pairs at distance `sqrt(11/3)`, as independently reconstructed.
The latter pairs motivate this source but **never become SAT edges**.
The final saved colour word makes 24 of those auxiliary pairs monochromatic;
this is compatible with its being a proper unit-distance colouring.

All exact calculations remain in the degree-eight field

```
K=Q(r,s,t), r=i sqrt3, s=i sqrt11, t=i sqrt247.
```

The square classes of -3, -11, and -247 are independent over Q, so the eight
monomials `1,r,s,rs,t,rt,st,rst` form a basis and the specified physical
embedding is injective. A point has eight rational coefficients in this
order. The first 40 points are `(c-ar-bs-drs)/36` in these coordinates.

## Discovery rule and exact acceptance

Maintain numerical intersections of pairs of unit circles centred at selected
points. An intersection becomes a proposal when at least three selected
points are numerically at distance one from it. Rank proposals by

```
(number of distinct neighbour colours,
 number of neighbours,
 -squared distance from origin,
 -rounded real coordinate,
 -rounded imaginary coordinate).
```

Choose the lexicographic maximum. Coordinates are rounded after multiplication
by `10^8`; the proposal contact test is `abs(distance_squared-1)<10^-7`.
Distances squared at most `10^-16` are skipped when forming circle pairs.
Numerical proposal discovery is heuristic: missing proposals, roundoff, and
deduplication are not completeness premises.

Before accepting a proposal, construct the circumcentre of a triple of its
neighbours by exact field arithmetic. For translated neighbours `u=b-a` and
`v=c-a`, its complex coordinate is

```
z=a+(|u|^2 v-|v|^2 u)/(conj(u)v-conj(v)u).
```

Reject collinear triples, nonunit circumradii, and repeated exact points.
Every accepted point must be exactly unit distance from all three defining
centres. Recompute **all** its exact unit contacts before inserting its SAT
constraints. The full final graph is therefore strictly induced, irrespective
of numerical proposal errors or contacts absent from the proposal pool.

The saved trajectory adds 429 exact circumcentres. Of these, 375 obstruct
the immediately preceding colour word by meeting all four colours; the solver
finds another word in each case. There were 278 rejected numerical proposals,
which may include repeated exact positions or unusable defining triples.
Those counts describe the run and imply no chromatic lower bound.

SAT uses four one-hot variables per vertex, a nonempty colour domain,
at-most-one colour clauses, and colour inequalities for every exact unit
edge. Only the first vertex's colour is pinned; colour renaming justifies
this symmetry restriction. There are no auxiliary-distance inequalities or
assumed monochromatic pairs or triangles.

## Independent verification and compact evidence

`certificate.json` contains 429 triples of previously constructed vertex
indices and one 508-symbol proper four-colouring. The checker reconstructs
all points from this construction history; no generated coordinate file or
solver proof is required for the saved upper bound.

The producer uses FLINT rationals in the complex tensor field, inverts via
successive field conjugations, and tests edges by `z conj(z)=1`.
The checker instead uses real Cartesian coordinates in
`Q(sqrt3,sqrt11,sqrt247)`, solves rational linear systems for field inverses,
and solves the two real circumcentre equations. It uses only Python's
standard library and imports no producer, FLINT, NumPy, or SAT code.

For its final all-pairs audit, write a difference with common denominator D as

```
x=(a-d sqrt33-f sqrt741-g sqrt2717)/D,
y=(b sqrt3+c sqrt11+e sqrt247-h sqrt8151)/D.
```

The squared distance is `(A+B sqrt33+C sqrt741+E sqrt2717)/D^2`, where

```
A=a^2+3b^2+11c^2+33d^2+247e^2+741f^2+2717g^2+8151h^2
B=2(-ad+247fg+bc-247eh)
C=2(-af+11dg+be-11ch)
E=2(-ag+3df+ce-3bh).
```

Thus an edge is equivalent to `(A,B,C,E)=(D^2,0,0,0)`. All 128,778 unordered
point pairs are checked exactly. The checker verifies distinctness, all 429
unit-radius constructions, all 2,561 edges and the colour word. It rejects
five deliberate certificate corruptions and checks a nonunit squared norm
with rational coefficient one and nonzero irrational coefficient. Optional
coordinate comparison checks every coefficient against producer output.
The independent audit took 3.65 seconds.

The final word also certifies every one of the 430 queried induced prefixes.
The mathematical upper-bound claim trusts exact rational/integer arithmetic
and the checker; it does not trust floating-point proposals or SAT verdicts.
We do not determine the exact chromatic number or claim external peer review.

## Reproduction

From the repository root, with CPython 3.11.2 and its standard library:

```sh
python3 hadwiger_nelson_ei79_circumcenter_pilot/verify.py --certificate hadwiger_nelson_ei79_circumcenter_pilot/certificate.json
```

The expected output is in `EXPECTED.json`. Optional discovery requires
`python-flint==0.8.0`, `numpy==2.4.6`, and `python-sat==1.9.dev15`
(CaDiCaL 1.9.5):

```sh
python3 hadwiger_nelson_ei79_circumcenter_pilot/pilot.py --work /tmp/hn-ei79-circumcentres
python3 hadwiger_nelson_ei79_circumcenter_pilot/verify.py --certificate /tmp/hn-ei79-circumcentres/certificate.json --producer-points /tmp/hn-ei79-circumcentres/points.json
```

The recorded validation replay matched every non-timing certificate field,
all rational coordinates, and the final word. Runtime fields vary. Different
numerical or solver versions may change the heuristic trajectory; the saved
certificate remains independently checkable.

If an invocation stops with UNSAT or UNKNOWN, the producer preserves the full
query CNF. A claimed non-four-colourability result would still require an
independently checked refutation. No such result occurred here.

The completed no-signal pilot is frozen. The general target of a five-chromatic
unit-distance graph on at most 508 vertices remains unresolved.
