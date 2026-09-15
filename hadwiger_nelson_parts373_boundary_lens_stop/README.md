# The complete Parts373 boundary-lens replacement is four-chromatic

The frozen Parts373 receiver now has an exact failed replacement certificate.
Add **every plane point at unit distance from at least two of its 23 marked
boundary points**, all at once. After exact collision merging with the host,
the complete strict unit-distance graph has **488 points and 2,200 edges**.
A literal proper four-colouring extends the first published full host word.
An embedded Moser spindle proves that the chromatic number is exactly four.

Thus this replacement does not meet the receiving demand. More generally,
**no replacement for this frozen receiver can succeed if every new point has
at least two unit neighbours among these 23 pins**: every such support is a
subset of this same four-colourable graph. This is a scoped physical class
exclusion, not a sub-509 candidate, a global HN bound, or a claim that all host
patterns extend.

## Named receiver and exact replacement

The input is R1's [complete Parts373 receiving relation](../hadwiger_nelson_parts373_receiver_relation/README.md),
source commit `0fdb37bb7772a835307f904403589ba1d4676f20`:

- H consists of original Parts labels 0,...,373 except 310: 373 points.
- The frozen receiving boundary is
  `B=[0,150,169,243,244,245,287,296,344,345,346,357,358,359,360,361,362,363,364,365,366,367,368]`.
- The complete unrestricted host relation has 468 global colour orbits.
- The replacement allowance is 135 distinct new points, for at most 508 total.

For each unordered pair a,b in B, set s=|b-a|^2. The replacement contains both
common unit neighbours when 0<s<4, the midpoint when s=4, and no point when
s>4. Exact coordinates of the two roots are

    (a+b)/2 +/- i(b-a)/2 * sqrt((4-s)/s).

All square roots are positive real roots. We take every pair and both signs,
merge physical collisions, retain all of H, and reconstruct **every** unit
pair. This is one simultaneous operation; no iterative closure or selection
from a larger host is used.

The initial rationale was to couple the receiver's deleted rainbow-star
constraint with its small-side boundary constraints through shared physical
vertices and new--new contacts. No chromatic gain was assumed from contact
counts. The exact cap check precedes the full chromatic verification.

| Exact census | Value |
|---|---:|
| Boundary pairs | 253 |
| Secant / tangent / disjoint circle pairs | 81 / 24 / 148 |
| Generated lens occurrences | 186 |
| Added distinct points outside H | 115 |
| Complete merged support | 488 |
| Complete unit edges | 2,200 |
| Old / old--new / new--new edges | 1,856 / 308 / 36 |
| All merged pairs checked | 118,828 |

Every possible numerical equality is settled algebraically. These are exact
physical counts, not conservative colour-group or possible-edge counts.

## Surviving receiving word

The supplied full four-colour word restricts on the original B to

    01200021231303000000303

and agrees on all 373 host vertices with the first row of R1's table. Its 115
new colours are checked against the complete reconstructed graph. A single
surviving word is sufficient to retire this replacement; no further host
patterns were tested and no full replacement-relation census is claimed.

The true host interface of this replacement has **80 vertices**, including
**58 outside B**. Therefore the old 23-pin table alone would be insufficient
for a relation-only composition decision. We instead check the **entire
488-point colouring directly**, including every incidental contact. There is
no inference of compatibility from an incomplete boundary.

Seven host vertices with original labels `[0,149,152,312,151,154,314]` induce
the eleven-edge Moser spindle. Exhausting its 2,187 three-colour assignments
proves the lower bound four. Recolouring the first vertex with colour 4 also
gives a directly checked proper five-colour word, but supplies no non-four
signal and does not make the graph a candidate.

## Reproduce

Python 3.11 or later; standard library only. From this directory:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B verify.py --bits 192
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The checker regenerates every exact point formula, collision and edge without
a solver, floating-point package, or sibling code import. `certificate.json`
contains the literal word, marked lower-bound witness and expected geometry
hashes. `points.tsv` is the byte-pinned exact source file from the receiver.
The normal, optimized and 192-bit runs agree. Controls reject three damaged
certificates and check false square-root signs and dependent-radical identities.

The exact algebra works over K=Q(sqrt3,sqrt11) with one extra positive root
per point. Rational directed intervals reject noncontacts; every remaining
collision and unit equality is decided by a signed algebraic squaring
identity. No small residual or interval containing zero is accepted as an
equality. [PROOF.md](PROOF.md) states the branch and completeness arguments.

Canonical compact-JSON hashes:

- Complete edges: `800eaa425b8ba5371a93b7370a18c632ef562d0c967481be7acdd49e6d22441f`.
- Ordered point formulas: `10e010eeb24478d67b17a2b2fc5e860ca26e962aa24593e0d59b7db800e994e4`.
- All lens routes: `e01a98146d5f70aba9595648e9523e237d5f59e90d28de193e6b1fac9c29a1e6`.

The floating selector and initial SAT model are preserved in authorized
scratch. They are not proof premises: the published word is checked directly
against the exact complete physical graph. R1's negative completeness and
parent proofs are contextual dependencies, not needed to certify this
surviving extension. This is author-side verification, not autonomous
independent review or formalization.

## Stop and scope

This source is banked at the first surviving host word. Deleting points from
this complete support cannot help, since the colouring restricts to every
subset. A successful answer to the same receiver must use at least one new
point with at most one B-contact. That necessary condition is **not** a reason
to start a one-contact sweep, add another layer, fill the unused 20-point
allowance, change boundary pins, or widen this operation.

The receiver remains valid and available for a genuinely different physical
replacement. G19, Parts a=8, old completion pools and other registered closed
families remain dormant. No global exclusion is asserted.

[Parts's paper](https://arxiv.org/abs/2010.12665) supplies the 509-point/2,442-edge
unrestricted record. [Haugland v4](https://arxiv.org/html/2608.04542v4) still
calls 509 current; its separate 2,131-point construction is spindle-free work.
The present four-chromatic graph changes neither benchmark.
