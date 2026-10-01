# Negative-edge parity and flat-forced tip gaps

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.
Two written all-real local lemmas for every integer n>=8, with a standalone
exact affine reader. They are unformalized and independently unreviewed.
They establish no new corona count, global Heesch upper bound, exact height
or connected finite-seven example.

## Physical geometry and prerequisites

Axial coordinates (q,r) mean (q+r/2,sqrt(3)r/2) in the Euclidean plane.
The skeleton S_n has counterclockwise corners

    A=(0,-1), B=(n,-1), C0=(n-1,1), D0=(0,1).

Its bottom has n unit chords, its top n-1, and its left two, meeting at
(0,0). The remaining B-to-C0 side is straight of length sqrt(3). On a unit
chord v to v+e, directed counterclockwise in Cartesian coordinates, use the
physical profile

    v+u*e+(s/100)*u^2*(1-u)^2*(e_y,-e_x),  0<=u<=1.

Here s=-1 on the bottom and s=+1 on the top and left. The flat side stays
straight. These profiles define the unmarked connected Jordan disc T_n;
the signs and labels describe its geometry, not additional matching rules.
Displacement is at most1/1600 and endpoint cone deviation at most
arctan(1/675). Scaling the amplitude from zero preserves the simple
prototype boundary. Genuine angles at A,B,C0,D0 are60,90,90,120 degrees;
intermediate labels and other smooth boundary points have180 degrees.

Let R(q,r)=(-r,q+r), J(q,r)=(q+r,-r). A pose(h,k,a,b) denotes R^k J^h
followed by translation(a,b). All additional copies below may initially
have arbitrary real translations, rotations and reflections. Their finite
union may have arbitrary topology. Only explicitly named old copies must
be contained strictly in the interior of that union.

The [atomic unit lemma](../heesch_weighted_matching_obstruction/quartic_realization.md)
forces any coincident open quartic portion to the whole unit, opposite
intrinsic signs, both labelled endpoints and an endpoint-fixed D6 motion.
Finitely many noncoincident algebraic germs cannot cover an incident
analytic boundary interval. The
[finite analytic-star proof and whole-OLD-flat sublemma](../heesch_trapezoid_protected_contact_reduction/proof.md)
therefore apply at a protected old point or flat side. The whole-flat
sublemma needs only its old owner strictly interior; its exclusion of
split contacts uses the
[uniform O,U,L strip obstruction](../heesch_trapezoid_uniform_strip_obstruction/proof.md).
It does not need a further surround of the newly forced flat mate.

For a gap of less than180 degrees at an interior old point, smooth tile
points cannot fit, so all suppliers are genuine corners. The
[necessary small-gap state words](../heesch_trapezoid_single_surround_alignment/proof.md)
use60-degree words(-,+) and(+,-),90-degree words(-,flat) and(+,flat) in both
orders, and the120-degree word(+,+). Adjacent supplier germs must match
with opposite signs. In particular a120-degree gap bounded by two positive
germs has no completion. A single120 corner fails the exterior matches;
two60 corners force an incompatible positive/positive internal seam.
A90 corner leaves30 degrees, smaller than any tile sector.

These are written mathematical dependencies. The reader verifies their
concrete affine uses, not a formalization of arbitrary analytic packings.
The previous [independent review of the protected-contact proof](../heesch_protected_contact_review1/REVIEW.md)
confirms older prerequisites within its stated two-surround scope. That
review does not review the later single-surround result or the present
lemmas. Generic affine arithmetic and physical geometry are credited to
the [earlier positive-run proof and reader](../heesch_trapezoid_positive_run_obstruction/proof.md).

## Lemma 1: negative-edge parity

Put O=(0,0,0,0) and P_a=(1,4,a,-1), with a an integer,0<=a<=n.
P_a's positive left side lies along O's negative-bottom line and covers
the axial interval[a-1,a+1] at height-1, in the opposite CCW direction.

**Claim.** If a finite packing contains O,P_a and O is strictly interior
to its union, then a is odd. P_a and other copies need no interiority.
This statement concerns exactly orientation(1,4). It makes no assertion
for the other mirror(0,5), or that odd offsets actually admit a surround.

At z=(0,-1), O has its60-degree sector in30-degree slots0,1. P_0 has a
regular180-degree positive-left sector in slots6,...,11. Their remaining
120-degree gap slots2,...,5 is bounded by O's positive north unit and
P_0's positive west unit. It has no necessary state word, so a=0 is
impossible with O strictly interior.

For2<=a<=n let x=(a-1,-1). This is a regular labelled point of old O's
negative bottom. O occupies slots0,...,5 and P_a's120-degree D0 corner
occupies slots8,...,11. Their remaining60-degree gap consists of
slots6,7. It is bounded by O's negative west germ and P_a's positive
southwest germ. O's interiority requires exactly one60 corner to fill
it; no other angle or collection of two sectors fits.

The finite analytic-star and atomic-unit lemmas force its endpoint
alignment. The only prototype60 corner is A. The twelve endpoint-fixed
D6 motions yield exactly one filler with positive west and negative
southwest germs:

    P_(a-2)=(1,4,a-2,-1).

Its occurrence, not its interiority, is forced. If a is even, repeat at
the old O labels a-1,a-3,...,1, reaching P_0. All points invoked belong
to strictly interior O. The base contradiction proves the parity rule
by integer induction over the entire stated offset and width domain.

## Lemma 2: a flat mate forces an impossible tip gap

For t=0 or t=1 put

    O=(0,0,0,0), C=(0,1,-1,-2n+t), D=(0,1,1,-2n+t).

**Claim.** No finite packing containing O,C,D makes both O and C strictly
interior to its union. D and all other copies need no interiority.

C's flat side goes from(0,-n+t-1) to(-2,-n+t). Strict interiority of C
forces a whole flat mate by the old-flat sublemma. Matching the complete
side, its endpoint direction and either hand gives exactly

    Q=(0,4,-1,t-1), F=(1,4,-1,t-1).

Q's first positive top unit goes from(0,-n+t-1) to(0,-n+t). D's first
positive top unit reverses the same chord. Both profiles bow toward the
other skeleton, so they create physical interior overlap. At the common
chord midpoint(0,-n+t-1/2), every other primitive side inequality of both
skeletons has slack at least1/2 for every n>=8. Primitive side norms are
1 or sqrt(3), so other-side distances are at least1/4, far above the
profile displacement1/1600. The overlap cannot be removed by other
prototype sides. Thus Q is excluded and F must occur.

At z=(0,t-1), F's60-degree A corner occupies slots6,7. For t=0, O has
slots0,1; for t=1, O has its regular180-degree left sector in
slots8,9,10,11,0,1. Both cases leave the contiguous120-degree sector
slots2,...,5 bounded by O's positive north germ and F's positive west
germ. Its necessary word list is empty. Because z belongs to the
strictly interior O, this gap must be filled in the same packing, a
contradiction. F never requires its own surround. This proves the claim.

No native prerequisite propagation, provider pool or solver was used in
either proof. The full flat census has only two motions; the forced60
corner census tests all twelve motions. A common arbitrary Euclidean
isometry transports either lemma.

## Reproduction and concrete scope

From repository root, ordinary CPython3.11+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B heesch_trapezoid_tip_propagation/check.py --expected heesch_trapezoid_tip_propagation/expected.json
```

[certificate.json](certificate.json) contains the literal domains and two
n=12 fixtures. [check.py](check.py) imports no earlier executable, solver,
constructor, native formula, trace, private corpus or external file.
The affine class and polygon/star primitives are adapted with attribution
from the preceding public reader; this is same-author exact checking,
not independent peer review. Python with `-O` is explicitly rejected.
Six malformed controls change the amplitude, parity induction, allowed
flat-offset range, blocker position or actual-frame pose; all reject.

Each coordinate has the form c+a*n+b*j with exact rational coefficients.
Primitive side directions are derived and checked constant on n>=8 with
positive side lengths. For the parity step2<=j<=n, a scalar-affine
inequality is minimized at j=2 or j=n. Its resulting expression c+m*n
must have m>=0 and c+8m>0. This proves the active-halfplane sector identities
throughout the full domain. Each flat case has only width n; every asserted
side slack has nonnegative n coefficient and passes at n=8. These are
domain proofs, not samples of widths or offsets. The remaining even-offset
induction and analytic-star/flat completeness are the written arguments
above. [expected.json](expected.json) gives the deterministic output.

The parity fixture O,P_2 is a physical two-copy disc packing with two
whole interfaces,48 exposed ports, nonincident squared distance3/4 and
ray separation30 degrees. The flat t=0 fixture O,C,D has ten whole
interfaces,58 exposed ports and the same margins; it has two disc
components. Both are nonvacuous packings, not coronas. The reader checks
skeleton separation, all shared whole opposite-sign chords, complete
boundary cycles, every nonincident edge distance and the incident rays.
The [earlier bounded-deformation proof](../heesch_trapezoid_four_coronas/proof.md)
transfers these networks to the actual curved geometry.

The flat fixture's frame(0,4,47,-16) gives

    O=(0,4,47,-16), C=(0,5,23,9), D=(0,5,23,7).

The [diagram](diagram.svg) shows the n=12 skeletons and both flat alternatives;
the proof uses exact profiles and the reader, not the picture. An old
prefix containing these three poses cannot admit a further strict
surround. A particular privately checked four-prefix motivated this
application, but that private witness is not an input or dependency
of either public lemma, and no fifth or new lower corona bound is claimed.

Each lemma supplies a necessary forbidden-pattern clause when selected
copies will need a future surround. Enumeration of occurrences in a
finite pool is a separate question from complete arbitrary-real corona
enumeration. Native UNSAT, resource guards and failure to find a new
prefix prove no global tile height here.

## Prior work and remaining frontier

The earlier n=8 root-tip catalogue excluded smooth matches at one
specified root port. Its [four-corona source](../heesch_trapezoid_four_coronas/proof.md)
also contains other fixed-width local obstructions. Lemma1 records the
entire width/offset induction in a specified mirror; Lemma2 combines
the later whole-old-flat fact with one protected old tip. The earlier
uniform strip and positive-run four-copy lemmas remain distinct
credited patterns. No exhaustive historical-priority assertion is made.

[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and the
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/) supply the disc/final-hole
corona conventions and bounded-size polyform census.
[Kaplan2025](https://arxiv.org/html/2509.12216v1) reports connected-disc finite
examples through six, crediting Bašić2021. These primary pages were refreshed
live for this pass; they are not an exhaustive2026 novelty census. Known
disconnected arbitrary-height constructions and hyperbolic results do not
solve the connected Euclidean-disc target, which remains open in this work.
