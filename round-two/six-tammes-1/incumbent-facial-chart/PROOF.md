# Physical facial chart of the two credited Tammes-15 incumbents

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Status: exact author-checked incidence audit of known configurations, with two
different geometric checks using a common exact arithmetic layer. Independent
researcher review and formalization remain pending. No new configuration,
global upper bound, global optimality or optimizer-occurrence theorem is asserted.

Let tau denote the credited root of
`13t^5-t^4+6t^3+2t^2-3t-1` in
`(0.59260590292507377809642492233275,0.59260590292507377809642492233276)`.
Use the labelled asymmetric incumbent and the alternative replacing only label14
from the published [completion construction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/thirteen-core-completion/PROOF.md).
The alternative has the published cyclic relabeling; all labels below are the
common completion labels. The known coordinates and their feasibility are prior
mathematics, credited there to Kottwitz and Buddenhagen--Kottwitz.

**Checked conclusion.** Each complete contact graph, embedded by the shorter
great-circle arcs, has30 edges and17 actual faces: **eleven triangles, three
quadrilaterals and three pentagons**. There are three vertices of degree3,
nine of degree4 and three of degree5. Both physically realize, with one coherent
orientation, these nine triangular faces and the following strict pentagonal face:

```
(2,10,1) (2,1,4) (2,4,8) (2,8,13) (1,10,12)
(0,5,11) (0,11,6) (5,0,7) (11,5,9)
P=(12,10,9,5,7).
```

Thus the stronger physical-face hypothesis of
[facial injectivity9562](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g22-facial-injectivity/PROOF.md)
holds for both of the equality completions classified in
[9560](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-equality/PROOF.md).
Neither classification9560 nor injectivity9562 is needed to compute the chart.
This is a direct labelled non-vacuity check, not their reproduction or review.

## The exact chart

The common oriented faces are

```
(0,5,11) (0,7,5) (0,11,6)
(1,2,10) (1,3,4) (1,4,2) (1,10,12)
(1,12,7,3) (2,4,8) (2,8,13) (2,13,9,10)
(5,7,12,10,9) (5,9,11) (6,11,9,13,8).
```

The three additional asymmetric faces are
`(0,6,14)`, `(0,14,3,7)`, `(3,14,6,8,4)`.
The three additional cyclic-alternative faces are
`(0,6,14,3,7)`, `(3,14,4)`, `(4,14,6,8)`.
All seventeen faces in either chart are strictly convex and have an explicit
containing open hemisphere. The incidence data, exact turn signs and full
contact graph are in `FACE_CHART.json`.

## Coordinate and arithmetic boundary

Write physical vectors as `p_i=B v_i`, with
`B^T B=H=(1-tau)Id+tau J` and choose `det(B)>0`. The root bracket gives
`1-tau>0` and `1+2tau>0`, so H is positive definite. Consequently the sign
of each physical triple product is exactly the sign of `det(v_i,v_j,v_k)`.

`check.py` independently reconstructs all fifteen asymmetric coefficient
vectors from the published cross Gram matrix and triangle-reflection sequence.
It compares them to all exact coefficients in the pinned fourteen-point
completion certificate, and uses that certificate's exact alternative14 vector.
Both constructions use the same anchor frame. Their provenance is pinned in
`inputs/PINS.json`; the copied arithmetic and coordinate input are public files,
not private cover or ledger inputs. The native arithmetic was written by
six-tammes-2 and is retained with its attribution. It uses Fraction polynomials
modulo the displayed quintic, checks requested Bezout inverses, and evaluates
nonzero signs by exact rational Horner enclosures in the root bracket. No floating
point or unproved polynomial irreducibility is assumed. CPython/Fraction and this
unformalized arithmetic remain common trust boundaries.

## Why the computed cycles are actual faces

First every one of the105 different-point gaps `p_i.p_j-tau` is checked either
identically zero or strictly negative. Exactly30 are zero in each construction.
This also establishes distinctness, since tau<1. Every contact arc has length
`d=acos(tau)<pi/2`. Such arcs cannot cross: at an interior crossing choose the
nearer endpoint of each arc; their distances to the crossing are at most d/2.
The strict triangle inequality gives distance below d for two distinct great
circles. Collinear overlap likewise creates a different endpoint pair at distance
below d unless the two arcs are identical. Both possibilities contradict the
packing inequalities. No third packing point can lie inside a contact arc,
since its distance to an endpoint would be below d.

At vertex i the outgoing tangent of neighbor j is `p_j-tau p_i` and is nonzero.
The signs used to sort tangent directions around i are
`det(v_i,v_j,v_k)` and `p_j.p_k-tau^2`. Sorting by an explicit reference half
circle and then the triple-product sign is exact, including opposite directions.
The finite algorithm checks that there are no coincident rays. Its result is the
actual cyclic order, for the chosen physical orientation. Starting at a directed
edge `(i,j)`, take at j the predecessor of i in this order. This follows the face
on the left. The actual connected contact graph has no crossings, so the orbits
are precisely its physical facial boundary walks. The checker visits each of
the60 directed arcs once, obtains17 simple cycles, and checks Euler's identity.
Connectivity is also checked in the direct audit.

As a second geometric route, `audit.py` does not import the tangent sorter or
face walker. For each proposed cycle it verifies that the sum of its vertices
has strictly positive dot product with every cycle vertex, giving an explicit
open containing hemisphere. For every directed side, every nonincident cycle
vertex has strictly positive determinant on its inward side. These strict
supports prove that the minor arcs bound a strict convex spherical polygon.
Every other packing point is excluded by at least one strictly violated side
inequality. Every nonadjacent boundary pair is a strict noncontact, so no contact
diagonal divides the polygon. The noncrossing argument therefore makes each
polygon an actual face. All60 directed sides occur exactly once and the count
is17. This directly checks the physical chart using halfspaces, rather than
relying on a second implementation of the same rotation traversal.

For each boundary vertex the determinant of predecessor, vertex and successor
is strictly positive. In the containing hemisphere this is precisely the
strict left-turn condition and makes the facial interior angle less than pi.
In particular P has all five interior angles less than pi. The listed nine
triangles and P all occur with the same orientation in both charts. Cyclic
rotation of the boundary cycle does not change this predicate.

## Scope and next reduction

The profile T11/Q3/P3 is established only for these two exact incumbents.
It corrects a provisional T9/Q7/P1 guess made while planning this face audit;
that guess was never a published theorem or premise. No arbitrary improved
packing is proved to have this profile or to contain the selected faces.
The next useful target is an explicitly bounded contact-map/profile occurrence
reduction, with all cases and degeneracies stated. The physical profile must
not be replaced by a count inferred from a partial graph.

`check.py`, `audit.py` and `controls.py` are compact and require no solver,
large proof corpus or network at reproduction time. The controls reject damaged
face data and coordinates and accept a harmless cyclic rotation, so a file hash
does not substitute for the geometric audit. Full executed validation is recorded
in `VALIDATION.json`.
