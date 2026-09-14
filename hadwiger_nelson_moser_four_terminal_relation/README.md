# An exact eleven-point four-terminal relation, without a capped construction

The strict unit-distance graph below has **11 distinct plane points, 19
edges, and chromatic number four**. Its four marked terminals are independent.
Their complete unrestricted four-colour relation is

```text
(colour(A) != colour(B)) OR (colour(C) != colour(D)).
```

Thus exactly 13 of the 15 canonical patterns extend. The forbidden patterns
are `0000` and `0011`, or 16 of the 256 assignments with named colours. Both
marked pairs AB and CD have length sqrt(7). Neither pair is individually
forced monochromatic or nonmonochromatic. Indeed every individual pair of
points in the whole support has exactly its bare graph relation.

The four-terminal relation is a proved physical source, but **no credible
at-most-508 composition has been obtained**. This package does not meet the
campaign's qualifying construction gate and is not record progress. The
source is stopped before copy, phase, or host growth. The obvious economical
two-point-overlap construction is already excluded by the known field
colouring, as explained below.

## Exact support and all physical contacts

Put

```text
rho = (1+i*sqrt(3))/2,    t = (5+i*sqrt(11))/6.
```

Vertices 0 through 6 are the standard Moser spindle:

```text
0, 1, rho, 1+rho, t, t*rho, t*(1+rho).
```

Append terminals in this fixed order:

```text
A = conj(rho), B = 2*rho, C = 2*t, D = t*(rho-1).
```

For direct replay, a row `(a,b,c,d)` denotes

```text
(a+b*sqrt(33) + i*(c*sqrt(3)+d*sqrt(11)))/12.
```

The rows are

```text
 0: ( 0, 0,  0, 0)      1: (12, 0, 0, 0)
 2: ( 6, 0,  6, 0)      3: (18, 0, 6, 0)
 4: (10, 0,  0, 2)      5: ( 5,-1, 5, 1)
 6: (15,-1,  5, 3)      A: ( 6, 0,-6, 0)
 B: (12, 0, 12, 0)      C: (20, 0, 0, 4)
 D: (-5,-1,  5,-1)
```

The eleven interior edges are

```text
01 02 04 05 12 13 23 36 45 46 56.
```

The eight terminal incidences are

```text
A--0, A--1, B--2, B--3, C--4, C--6, D--0, D--5.
```

There are no other unit edges. Tuple equality is exact physical equality:
sqrt(33) is irrational, and sqrt(3)/sqrt(11) is irrational. All eleven tuples
are distinct. For a difference row `(a,b,c,d)`, the squared distance is

```text
[a*a+33*b*b+3*c*c+11*d*d + 2*(a*b+c*d)*sqrt(33)]/144.
```

All 55 pairs are evaluated, so both unit contacts and missing contacts are
certified. No approximate geometry, imposed nonunit edge, or collision
identification is hidden in the graph.

## Full relation and retained-core proof

Suppose A and B have the same colour x. Every vertex of the first diamond
`{0,1,2,3}` is adjacent to A or B, and therefore avoids x. In a three-coloured
diamond K4 minus an edge, the two nonadjacent tips have the same colour:
the two adjacent middle vertices use two colours, leaving the third colour
for both tips. Consequently vertices 0 and 3 have the same colour.

If C and D have the same colour y, the identical argument on the second
diamond `{0,4,5,6}` gives equality of 0 and 6. The unit edge 36 contradicts
these two equalities. The argument allows x=y and x!=y, proving both
forbidden patterns. The verifier also checks all 81 three-colour words of a
diamond and the six proper words that remain.

The 13 literal four-colour words in [certificate.json](certificate.json)
cover every other canonical terminal pattern. Each word is checked against
all 19 physical edges. A canonical word is a restricted-growth word starting
at colour zero, introducing new colours in their order of first appearance.
These are precisely the 15 partitions of four labelled terminals. Permuting
the four colour names gives exactly the 240 allowed named assignments; the
checker compares this set with the stated Boolean relation.

Deleting any one of the seven interior vertices permits both formerly
forbidden patterns. Fourteen supplied deletion words prove this directly.
Restricting the original 13 words provides every other pattern. Hence every
proper retained interior gives a neutral full four-terminal relation. This
is minimality **inside this fixed physical support with these terminals**,
not global minimum order among all possible relation sources.

All four projections onto three marked terminals are also neutral. Dropping
any marked terminal therefore loses the restriction. A separate exhaustive
audit enumerates all 16,384 interior four-colour words, retains the 384
proper ones, and extends through the independent terminal lists. It obtains
exactly 6,144 full four-colourings and the same 240 terminal assignments.
Their individual pairs allow equality on all 36 nonunit pairs and inequality
on all 55 pairs. This rules out extracting a forced-equal two-terminal half
from this source. It does not assert neutral relations for all other choices
of three or four terminals.

The interior is the Moser spindle, whose usual two-diamond proof excludes
three colours. The audit also checks all 2,187 interior three-colour words.
The positive four-colour words prove the matching upper bound.

## Physical composition budget and why expansion stops

The attractive clause costs seven private interior points plus four
terminals. This is a cost, not a composition: a nominal allowance of dozens
of copies supplies neither a contradictory colouring constraint system nor
the required Euclidean realization.

For example, a succession of 56 copies sharing at least two previous points
at every addition would have at most `11+55*9=506` physical points. But this
entire architecture is four-colourable, for a known reason. All source
coordinates belong to

```text
E = Q(i*sqrt(3), i*sqrt(11)).
```

Normalize the first copy to the displayed support. If two distinct source
points q1,q2 are placed at two existing points p1,p2 in E, then an
orientation-preserving isometry has multiplier `(p2-p1)/(q2-q1)` in E and
translation in E. A reversing isometry uses `conj(q2-q1)` instead, also in
E. Every newly placed point remains in E. Induction includes arbitrary
additional contacts and collisions at every stage.

The [previous field-colouring theorem](https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
four-colours the entire strict unit-distance graph on E, including arbitrary
rational denominators. Applying that theorem proves the stated assembly
exclusion. No new field theorem or independent re-review is claimed here.
Its argument embeds E into the unramified quadratic extension of Q_2 and
uses the coefficient of 2^0 in two local coordinates. Unit norm differences
have integral local coordinates and nonzero residue. This is a colouring of
the embedded field, not of all of R^2 or the larger Cartesian field plane.

An attachment sharing just one point and having no other overlap or cross
edge also cannot cause a contradiction: independently permute the new
copy's four colours to match the shared point. A tree of such attachments
extends by induction. This statement does not cover additional closing
contacts or cycles of overlaps.

Therefore an unexcluded composition would need a genuinely different
physical incidence: for example, a freely oriented attachment outside E
with later closing contacts. No such capped driver is supplied here. The
source is stopped rather than grown into a family. The equality-half
two-copy construction is also unavailable because no pair is forced equal.
These are scoped construction barriers, not a global lower bound on HN
graph order.

## The corrected incidence and negative control

The initial declaration mistakenly used `C=t*(2+rho)`. That point sees only
vertex 6 among the interior, so vertex 4 was not dominated. The resulting
11-point, 18-edge support has a neutral interface: all 15 canonical
patterns extend. That exact failed support was stopped and retained.

The correction `C=2*t` realizes the intended common unit neighbour of
vertices 4 and 6. Its full relation was then recalculated without inferring
anything from the initial signal or intended incidence. The old formula
and its 15 positive witnesses are included as a replayable negative control.
This was one explicit correction of a failed geometric premise, not an
unreported search over angles or enlarged hosts.

## Replay and trust boundary

Use Python 3.11 or later, with only the standard library:

```sh
python3 -B verify.py
python3 -B direct_audit.py
python3 -B controls.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) and [VALIDATION.json](VALIDATION.json) record
counts, hashes, version, and author-side validation. [model.py](model.py)
uses the integer norm formula. [direct_audit.py](direct_audit.py) imports no
model, verifier, or certificate: it reconstructs the same geometric formulas
in Q[x]/(x^4+28*x^2+64), with x=i(sqrt(3)+sqrt(11)), and tests products with
complex conjugates. It uses interior-first exhaustive colouring, rather
than checking the supplied terminal-first words. Both complete edge sets
and complete named relations agree by canonical hashes. Eight deliberate
corruptions are rejected by mathematical checks without using file hashes.

The proof trusts the explicit algebra, the finite enumeration and certificate
checker logic, CPython integer/Fraction arithmetic, and ordinary hardware.
It uses no SAT verdict, floating equality, large omitted certificate, or
external data file. The assembly barrier additionally uses the cited field
theorem; the eleven-point relation and core proof do not. The work is not
formalized and these two checks are author-side validation, not independent
peer review.

## Context and attribution

The spindle and its diamond argument are classical, due to Leo and William
Moser; no new atom or general colouring method is claimed. This package
records the explicit four-terminal physical realization, its complete
relation, its retained-core boundary, and the failed capped composition
gate. No priority or smallest-gadget claim is made.

At the 2026-09-14 evidence refresh, [Parts' primary paper](https://arxiv.org/abs/2010.12665v2)
still supplies the 509-vertex, 2,442-edge benchmark, also identified as the
unrestricted record by [Haugland's recent paper](https://arxiv.org/html/2608.04542v4).
This source is outside the retired fish-spindle/EI19 supports and does not
use the other lane's F29/opposed-palette driver, triangular patches, Petersen
source, or reciprocal-chord cage. The latest teammate exclusions were read
for construction ownership, not reproduced as routine review. Discovery's
local committed index remains stale; pending broadcasts are not treated as
committed findings.
