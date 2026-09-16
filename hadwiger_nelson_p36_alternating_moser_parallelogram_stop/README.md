# Alternating-Moser four-P36 parallelogram is exactly three-chromatic

This package freezes and exactly decides one translated, nonconcurrent union
of four 127-point triangular patches for the Hadwiger--Nelson record search.
It produces no five-chromatic graph and does not improve the 509-point record.

Put

```text
omega = (1+i*sqrt(3))/2,
rho   = (5+i*sqrt(11))/6,
P36   = {a+b*omega : a^2+a*b+b^2 <= 36},
v     = 6*(1+rho) = 11+i*sqrt(11),
w     = omega^2*v.
```

The one topology frozen before chromatic testing is

```text
Q0 = P36,
Q1 = v + rho*P36,
Q2 = v+w + P36,
Q3 = w + rho*P36.
```

Thus the patch centres form a parallelogram and the two exact orientations
alternate.  This is not a concurrent/radial union and is not a cyclic
quarter-turn collar.

## Exact outcome

The 508 formal labels collision-merge to **504 physical points**.  There are
exactly four double collisions, one on every edge of the patch-contact cycle:

```text
Q0(-6+6*omega) = Q3( 6-6*omega)
Q0( 6)         = Q1(-6)
Q1(-6+6*omega) = Q2( 6-6*omega)
Q2(-6)         = Q3( 6)
```

No point has multiplicity three or four.  Exact all-pairs reconstruction
finds **1,368 unit edges**, precisely the merged union of the four sets of 342
patch edges: there is no additional old--old cross-patch unit edge.

The patch-contact graph is a four-cycle.  Both it and the complete 504-point
physical graph are connected and have no articulation vertex or bridge, so
the declared nonseparability gate passes.  However, iterative deletion of
vertices of degree at most three removes all 504 vertices.  The four-core is
empty, so the required all-four-patch four-core admission gate fails.

The complete graph is in fact exactly **three-chromatic**.  On every formal
patch occurrence use

```text
colour(a+b*omega) = a-b mod 3.
```

Every triangular-lattice unit step changes this residue.  All eight labels in
the four collision pairs have residue zero, so the formula descends to the
physical quotient and colours every reconstructed edge.  The three points
`0, 1, omega` in `Q0` form a unit triangle, proving the matching lower bound.

This literal complete decision is the mandated stop.  It retires only the
displayed alternating-Moser parallelogram.  No anchor, translation, contact
cell, phase, or orientation variant was tested after the frozen topology
failed the four-core gate.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```sh
tmp=$(mktemp)
python3 -B hadwiger_nelson_p36_alternating_moser_parallelogram_stop/produce.py --out "$tmp"
cmp "$tmp" hadwiger_nelson_p36_alternating_moser_parallelogram_stop/certificate.json
rm "$tmp"
python3 -B hadwiger_nelson_p36_alternating_moser_parallelogram_stop/verify.py
python3 -O -B hadwiger_nelson_p36_alternating_moser_parallelogram_stop/verify.py
(cd hadwiger_nelson_p36_alternating_moser_parallelogram_stop && sha256sum -c SHA256SUMS)
```

The producer uses rational arithmetic in the basis
`(1,sqrt(3),sqrt(11),sqrt(33))` and checks every physical pair.  The verifier
imports no producer or parent code.  It independently expands every coordinate
as eight integer coefficients with common denominator 12, reconstructs all
126,756 squared distances, collisions, inherited edges, connectivity,
articulations, bridges, the deterministic four-core peeling, the residue word,
and the source triangle.  Eight malformed certificates are rejected.  No
floating-point predicate or SAT result is a premise.

Canonical commitments are:

```text
points      d3e60e263baf2f5bd8fdb3c009cf2b086a40df4b76183f412d6569574494e41a
edges       7123ed27a60b9907e6461dd030426517125f5744d519a5e56fb39ce6279e16ad
certificate 379dd011d3565c4507a7eca63a0c2f74997bf46fcb10657254c31a48d08ab60d
```

These are exact author-side computations, not independent review or a
proof-assistant formalization.

## Scope and context

The reviewed concurrent theorem covers every four-`P36` placement with a
common physical point, and the reviewed quarter-turn theorem covers its exact
cyclic collar family.  Those results were rejection boundaries, not premises
of this graph decision.  The present translated alternating-orientation union
lies outside both geometric definitions, but it fails for the simpler reason
that its complete contacts add nothing beyond four cyclic vertex gluings.

Parts's strict 509-point/2,442-edge construction remains the supported
unrestricted vertex record.  This package is a scoped negative construction
result only.
