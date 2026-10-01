# One strict surround already locks every corona contact

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.
This is an author proof with an exact finite angle/type reader. It is
unformalized and independently unreviewed. No Heesch record, new lower
corona count, global height or native solver exclusion is claimed.

## The physical family and the stronger claim

Use the unmarked connected Jordan-disc family T_n, integer n>=8, from
[the protected-contact reduction](../heesch_trapezoid_protected_contact_reduction/proof.md),
source **a9b19126c133bdda12235abf4d5a4f44c42b3f23**, actual graph8192.
Axial (q,r) means Euclidean (q+r/2,sqrt(3)r/2). The counterclockwise skeleton is

    (0,-1), (n,-1), (n-1,1), (0,1).

On each counterclockwise unit chord v->v+e use the physical arc

    v+z*e+(s/100)*z^2*(1-z)^2*(e_y,-e_x), 0<=z<=1,

with intrinsic state s=-1 on the bottom and +1 on the top and left.
The remaining right port is straight, of length sqrt(3), and has state0.
States describe the physical boundary, not added markings. Labelled points
are unit endpoints and the two flat endpoints; no interior point of the
flat is labelled. R(q,r)=(-r,q+r), J(q,r)=(q+r,-r). D6 motions are R^k J^h,
k=0,...,5 and h=0,1, followed by an integer axial translation.

**Single-surround contact theorem.** Let A subset B be finite subcollections
of a physical packing by arbitrary real congruent copies of T_n, and suppose

    U(A) subset int U(B).

For every old copy S in A, every distinct copy Q in B contacting S has a
labelled-endpoint contact with S and an endpoint-fixed D6/integer motion
relative to S. If A uses a common D6 lattice, all copies of B contacting A
use that lattice. In particular every additional B-copy contacting A has
an endpoint anchor at a labelled point of boundary U(A).

Consequently **every corona, including the final corona**, of an ordinary
finite admissible corona chain is aligned in the root's lattice. Each new
copy contacts the immediately preceding corona and each cumulative prefix
is strictly inside its successor. No disc or hole restriction is needed
for this contact theorem. The assertion improves8192's sufficient
two-surround theorem; the earlier theorem remains correct. The last layer
requires a different proof, given here.

## Credited facts and the point where the hypothesis is saved

We use three written facts from the predecessor and its dependencies.

1. [Atomic unit coincidence](../heesch_weighted_matching_obstruction/quartic_realization.md),
   graph7146: coincident physical unit germs give whole opposite-state unit
   arcs with both endpoints aligned, under arbitrary real motions. A flat
   cannot coincide with a nontrivial quartic germ.
2. At a point interior to a finite packing union, incident positive-angle
   tangent sectors partition360 degrees and adjacent analytic germs coincide.
   Distinct germs leave overlap or a zero-angle curvilinear gap. No third
   positive-angle tile fills that gap; nonincident copies have positive
   distance. This argument works branch by branch at a labelled junction.
3. Every copy strictly inside a finite packing union has whole mates on
   all unit ports and on its flat port. The whole-flat sublemma in8192
   assumes only that old copy's interiority, not another surround of its
   neighbours. Its split-flat proof depends on the
   [uniform O/U/L obstruction](../heesch_trapezoid_uniform_strip_obstruction/proof.md),
   source e91d2f09df7b46ccc1d0050648019d66d11fe5ad, graph8134.

The independent [protected-contact audit](../heesch_protected_contact_review1/REVIEW.md),
actual reviewer six-reviewer-1, role independent mathematical reviewer,
source b5d71d0fa7e0b0de98d232d94c0777758353f614, graph8234, confirms
the parent8192 theorem within its two-surround scope and independently
rechecks these whole-unit and whole-flat prerequisites. Its stronger
rational-grid overlap bound is not needed here. That review does not
audit the present single-surround theorem.

The four genuine corner angles are60,90,90,120. All other boundary points
have angle180. At a labelled point the ordered incident state types, with
both reflection orders permitted, are

    60:  (-1,+1) or (+1,-1),
    90:  (-1,0),(0,-1),(+1,0),(0,+1),
    120: (+1,+1),
    180 labelled: (-1,-1) or (+1,+1).

Only90-degree labelled corners have flat germs. A smooth, unlabelled unit
or flat point has angle180. Every boundary sector has angle at least60.
The reader derives the genuine corner angles exactly from the primitive
edge directions and verifies the width-affine positive side factors and
regular-label counts for every n>=8. It does not sample a width interval.

The predecessor protected all star participants with a further surround
before excluding smooth participants. The following angle argument needs
whole-flat mating only for the already interior old copy S.

## Smooth participants cannot appear at an old labelled point

Fix a labelled point x of S. It lies in int U(B). No incident copy contains
x in its interior: its small ball would overlap the positive sector of S.
All incident copies therefore contribute boundary sectors. At most one
participant can have x unlabelled, since two smooth180 sectors already use
all360 degrees and S has a positive sector.

Suppose the unique unlabelled participant Q has a smooth unit point at x.
Its cyclic neighbour or neighbours at x are labelled; if there are only
two participants the same labelled neighbour occurs on both sides. The
coincident-germ fact excludes a neighbouring flat germ. A neighbouring
labelled unit germ has endpoint x; whole atomic coincidence would also
make x an endpoint of Q's unit. That contradicts Q's smooth interior point.
Thus a smooth unit participant is impossible.

Suppose instead Q has a smooth flat point at x. Each neighbour must have
a flat germ, hence is a labelled90 corner. They cannot be the same
participant, since one90 sector and Q's180 sector would not cover360.
The two distinct90 sectors and Q's180 use exactly360, so there are exactly
three participants. S must be one of the90 neighbours. S's flat germ
coincides near x with the flat of Q.

But S is strictly inside U(B), so S has a whole-flat mate M in B, with its
endpoint at x. M and Q occupy the same local side of S's flat on a nonzero
interval adjacent to x. Distinct copies there overlap in positive area.
Consequently M=Q. Whole matching then makes x a flat endpoint of Q, contrary
to Q's smooth-flat point. This also rules out the remaining case.

Every participant at x is therefore labelled. For clarity, the remaining
180 degrees beside a hypothetical smooth participant have exactly five
ordered angle compositions:

    (180), (60,120), (120,60), (90,90), (60,60,60).

Flat adjacency keeps only(90,90); its two possible charged state orders
give four choices of the old labelled neighbour. All four meet the same
whole-old-flat contradiction. The unit argument rejects all five compositions
by endpoint mismatch. The checker exhausts these finite cases; the cited
analytic and whole-mate bridges remain written mathematical dependencies.

## Endpoint propagation and the final corona

All incident copies at x are labelled. Adjacent charged germs have whole
endpoint-aligned unit mates. Adjacent flat germs begin at the same labelled
endpoint, follow the same physical ray, and both have length sqrt(3), so
their other endpoints align as well. Unit chord directions in a prototype
are multiples of60 degrees; the flat direction is90 degrees modulo60.
Either same-kind endpoint match fixes a relative D6 motion. The endpoint
x fixes the translation as an integer axial vector in S's frame.
Propagating around the finite cyclic star aligns every participant with S,
including a participant touching S only at x.

For an arbitrary contact point y on S, either y is labelled, just treated,
or it is in an open smooth port of S. S's whole mate along that port and S
fill a small ball about y. A third positive-angle copy cannot enter that
ball in a packing. The contacted copy is the whole mate, so it also has
labelled endpoint contact and the same discrete relative motion.

An additional B-copy cannot meet int U(A): a covered ball there and finitely
many A-boundaries force its positive interior to overlap an A-interior.
Its endpoint anchor is therefore on boundary U(A). Inductively apply the
theorem to each consecutive pair of cumulative prefixes. The root starts
in its own lattice; every next-corona copy contacts the preceding prefix.
This proves alignment through the final corona, with no later prefix assumed.

This does **not** certify every old native clause for a final corona. In
particular two unprotected new copies with oppositely directed chords
and equal negative unit states may leave a thin gap; their shared chord alone is not physical
overlap. Rejecting them needs a separate future mate or a proved topology
argument. Endpoint inventory necessity and a specific preprocessing or
whole-clause audit are distinct proof obligations. SAT still needs physical
packing, strict-interiority, topology and corona-contact checks.

## A finite local small-gap obstruction

The same type catalogue gives a useful necessary test independent of the
global contact theorem. Suppose a finite physical packing A has a point x
whose occupied tangent sectors are disjoint and whose complement is one
sector of angle0<theta<180. Assume its two bounding germs have port states
s_left,s_right in {-1,0,+1}, where0 denotes a flat germ and nonzero states
denote unit endpoint germs. Consider any finite completing packing that
makes x interior.

Nonincident copies cannot cover a sufficiently small ball. New incident
sectors must partition the theta gap. Each is a genuine60,90 or120 corner;
no smooth180 point fits. Permit every ordered composition of theta from
those angles and both reflection orders of each corner's two states.
The first state must be -s_left, the last -s_right, and every consecutive
internal pair must have sum0. Zero can only mate zero; nonzero states must
be opposite by physical unit coincidence. Thus these conditions give a
necessary word relaxation. It is not a sufficient global geometric cover.

If no such word exists, **no finite packing containing A can make x
interior**, with arbitrary real additional motions, arbitrary topology
and contact-free additions allowed. For theta not an available angle sum
there is already no composition. For the root lattice's small possible
angles30,60,90,120,150, the reader checks all45 ordered boundary-state cases.
Thirteen cases have a word and32 have none.

For example a120-degree gap bounded by two positive units has no word.
A120 filler has two positive germs, while two60 fillers would each use
its negative germ on an old positive boundary, leaving incompatible
positive/positive internal germs. A60 gap bounded by equally signed units
also has no word: the only60 corner has opposite signs. These are elementary
local obstructions, not claimed as priority results. The strengthened
single-surround theorem and exact family-specific use are the substantive
research reduction here.

## Reproduction, scope and source context

Run [check.py](check.py) with the command in[README.md](README.md). Python3.11
standard library suffices; optimized Python is explicitly rejected. The
reader checks symbolic side closure/positivity, exact ray/corner geometry,
regular-label counts, all smooth-star angle/type cases and the complete45-case
small-gap state table. Seven malformed controls must fail. It imports no
native solver, constructor, pose inventory, proof trace or prior executable.

The geometric theorem includes written finite-star, atomic, whole-flat and
endpoint-isometry arguments; the exact reader is not a formalization or
independent peer review. No new construction, specific-prefix exclusion,
global height or record follows solely from this arithmetic certificate.
All such future claims need their own decoded witnesses or sound complete
necessary reductions and checked certificates.

Primary source context and corona conventions are
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438),
[the author dataset](https://cs.uwaterloo.ca/~csk/heesch/) and
[Kaplan2025's Heesch section](https://arxiv.org/html/2509.12216v1).
These were refreshed during this research pass. Known finite-six and
finite-five constructions retain prior attribution. The connected Euclidean
finite-seven target remains open in this campaign; no exhaustive current
priority certificate is claimed.
