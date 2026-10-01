# Positive runs and a four-copy obstruction for bowed trapezoids

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.
This is a written author proof with an exact affine-arithmetic reader.
It is unformalized and independently unreviewed. The result gives necessary
geometric constraints and a forbidden local pattern, not a new Heesch record,
new corona count or global Heesch upper bound.

## Physical family and prerequisites

Use the unmarked Jordan-disc family T_n, integer n>=8, from the
[protected-contact reduction](../heesch_trapezoid_protected_contact_reduction/proof.md).
Axial (q,r) means Euclidean (q+r/2,sqrt(3)r/2). Its counterclockwise
quadrilateral skeleton has vertices

    A=(0,-1), B=(n,-1), C=(n-1,1), D=(0,1).

On every counterclockwise unit chord v->v+e, replace the chord by

    v+t*e+(s/100)*t^2*(1-t)^2*(e_y,-e_x), 0<=t<=1,

in Euclidean coordinates. Intrinsic state s is -1 on the n bottom units,
and +1 on the n-1 top units and the two left units. The sole remaining
port B->C is flat, length sqrt(3). These are shapes, without added markings.
Every arc differs from its chord by at most delta=1/1600. The four genuine
corner angles are60,90,90,120; other boundary points have angle180.
Write a lattice pose (h,k,a,b) for R^k J^h followed by translation (a,b),
where R(q,r)=(-r,q+r), J(q,r)=(q+r,-r), h=0,1 and k=0,...,5.
Additional copies in the theorems below may have arbitrary real motions.

The following prerequisites retain their original attribution:

* [Atomic unit coincidence](../heesch_weighted_matching_obstruction/quartic_realization.md),
  actual graph7146: coincident physical unit germs are whole oppositely
  signed unit arcs, with both endpoints aligned. A flat cannot coincide
  with a nontrivial quartic germ.
* [The finite analytic-star and whole-flat arguments](../heesch_trapezoid_protected_contact_reduction/proof.md),
  graph8192: at an interior point of a finite packing union, positive-angle
  tangent sectors partition360 degrees and adjacent analytic germs coincide.
  Every old tile made strictly interior has whole mates on all ports,
  including its flat port. The whole-flat sublemma needs the old tile's
  interiority alone; its proof uses the
  [uniform O/U/L obstruction](../heesch_trapezoid_uniform_strip_obstruction/proof.md),
  graph8134. We do not assume a further surround of the new mates.
* [The small-gap state test](../heesch_trapezoid_single_surround_alignment/proof.md),
  graph8297: a60-degree gap bounded by two positive unit germs has no
  completion; a30-degree gap has no completion because every tile's
  positive tangent angle is at least60. These are necessary all-real local
  tests, not sufficiency criteria for a corona.

The independent [protected-contact audit](../heesch_protected_contact_review1/REVIEW.md),
actual reviewer six-reviewer-1, role independent mathematical reviewer,
graph8234, confirms the earlier whole-unit and whole-flat prerequisites
and8192 within its stated two-surround theorem. It does not review8297 or
the present run lemma and four-copy obstruction. The present buffered
overlaps are checked directly and do not use that audit's grid-bound result.

## A complete cover lemma for a positive straight run

A positive run of length L is a sequence of consecutive physical positive
unit arcs whose chords are a+j*e -> a+(j+1)*e, j=0,...,L-1, with e a unit
direction. All chords have the same counterclockwise direction. Assume
the run belongs to a finite physical old packing, and at each internal
label a+j*e the old occupied tangent sectors comprise exactly the interior
halfplane of the run. The physical run is C1 there, even if its owner changes.
Assume a finite containing packing makes every run owner strictly interior.

**Run-cover lemma.** At most two distinct negative-bottom copies mate with
the positive arcs along this run. Therefore L<=2n. If n<L<=2n, there are
exactly two such copies, and their complete possible meeting points are

    x=a+j*e, with L-n <= j <= n and j an integer.

Both copies have their90-degree B corners at x, and their full flat ports
mate. In coordinates with a=(0,0), e=(1,0), old interior above the run,
and new exterior below it, the unique pair at cut j is

    left  = (1,0,j-n+1,-1),
    right = (0,3,j+n,-1).

Their negative-bottom intervals are [j-n,j] and [j,j+n]. Their common flat
has endpoints (j,0) and (j+1,-2).

**Proof.** Each old positive arc has a whole opposite-state unit mate.
All negative unit ports of T_n are on its single bottom edge. Atomic endpoint
alignment puts every mating bottom on the same axis, with integral endpoint
phase relative to a. A mating bottom is a length-n interval lying on the
exterior side of the run. Two such intervals cannot overlap in their open
parts: their negative physical profiles there coincide, and both tile
interiors lie on the same side, so distinct copies would overlap in positive
area. The intervals are disjoint, ordered, and cover the entire run.

At a change of owner inside the run, an interval ends and the next begins at
the same integer label. Each endpoint is either the60-degree A corner or the
90-degree B corner of a negative bottom. The old sector occupies180 degrees.
If the two new endpoint angles are60 and90, the remaining gap is30 degrees,
which cannot be filled. If both are60, the remaining gap is60. Each of these
corners has used its negative germ to mate with the old positive run, leaving
a positive germ bordering that gap. The only possible60 filler has opposite
signs on its two germs, so it cannot mate both positive boundaries. A smooth
point has angle180 and cannot enter either small gap. The finite-star
argument makes these angle and germ necessities valid even with any further
finite additions.

Thus a change must be90-to90. Both remaining germs are flat and must coincide;
their equal length and common endpoint make their whole flat ports mates.
No tile has two90-degree endpoints on its negative bottom. A third interval
meeting the run would require a middle bottom to have90-degree endpoints at
both its changes of owner, which is impossible. Consequently there are at
most two intervals and their total length is at most2n. A single interval
cannot cover L>n. Two intervals meeting at j cover [0,L] exactly when
j<=n and L-j<=n, giving the stated integer range. The negative-bottom B
endpoint, its side and the exterior halfplane determine a unique isometry
for each copy. Enumerating both reflection choices gives the displayed
pair. This last enumeration fixes no motions of unrelated additions.

## A uniform four-copy pattern that cannot be surrounded

For every n>=8, define the following four poses in the run's normalized frame:

    S1=(0,2,1,0),
    S2=(1,0,1,1),
    S3=(0,3,2n,1),
    S4=(0,3,2n+2,-1).

**Four-copy obstruction.** No finite physical packing containing all four
copies can make all four strictly interior. This statement permits arbitrary
real additional motions and arbitrary topology, including holes. It is
conditional on containing the displayed copies; it is not an assertion that
every corona contains them.

The [diagram](diagram.svg) shows the n=12 skeleton and the forced conflict.
The certificate proves the nonexistence direction; a picture alone does not.

**Proof.** The left side of S1 contributes a positive run from (0,0) to (2,0).
The positive top of S2 continues it to (n+1,0). The first positive top unit of
S3 continues it to (n+2,0). The old occupied tangent sectors are the upper
halfplane at every internal label. At label2 the S1 and S2 sectors have
angles60 and120; at label n+1 the S2 and S3 sectors have angles90 and90.
At all other internal labels a single regular old180-degree sector suffices.
Thus these n+2 units satisfy the run-cover lemma.

If the four old copies were made strictly interior, their run would require
two bottom mates meeting at an integer j in the complete range2<=j<=n.
The right mate would be

    G_j=(0,3,n+j,-1).

For every3<=j<=n, the rational point

    p=(n+11/4,-1)

is inside the skeletons of both G_j and S4. The reader checks all eight
primitive halfplane inequalities symbolically on the whole domain
n>=8, 3<=j<=n. Every slack is at least1/4, and every resulting squared
perpendicular distance is at least3/64 > delta^2. Since the physical
boundary moves by at most delta, p is also in the interiors of both physical
tiles. These are buffered physical overlaps, not rejection based merely on
intersecting skeletons. Therefore the only possible cut is j=2. It forces

    G=(0,3,n+2,-1).

Now make S4 strictly interior. Its flat port, from (n+2,0) to (n+3,-2),
must have a whole mate. The complete endpoint-fixed alternatives are

    Q=(0,0,3,-1), F=(1,0,3,-1).

There are only two: the prototype has one flat, and matching its oriented
full endpoints allows one rotation for each reflection choice. This does
not restrict arbitrary real motions in advance; the full physical flat
match imposes these motions.

Q's positive top unit from (4,0) to (3,0) faces S2's positive top unit from
(3,0) to (4,0). Both positive quartics bow outward on opposite sides of
the same chord. The open chord midpoint (7/2,0) is inside both physical
tiles, so Q and S2 overlap. This is the positive/positive case; no negative
gap is treated as physical overlap. The reader verifies the endpoint
identities, the two intrinsic positive states, and that every other skeleton
halfplane has slack at least1/2 at that midpoint. Hence Q is impossible,
and F is forced.

Finally the fixed rational point (5,-1) lies inside both F and G. All eight
primitive halfplane slacks are at least1 for every n>=8, and the squared
perpendicular distances are at least3/4 > delta^2. This is again a direct
buffered physical overlap. The two forced copies cannot coexist. This proves
the obstruction without a native pose inventory, preprocessing, solver or
proof trace.

## Nonvacuity and an immediate search constraint

The four n=12 old copies alone form a physical Jordan-disc packing. The
standalone reader verifies disjoint convex skeleton interiors,13 whole
opposite-state contacts,78 exposed ports in one complete simple boundary
cycle, nonincident chord distance squared at least3/4, and incident rays
separated by at least30 degrees. The small quartic deformations preserve
this embedded contact network: displacement is at most1/1600, matched
arcs move together, and near an endpoint their lateral/longitudinal ratio
is at most1/100 <1/4 < tan(15 degrees). Nonincident arcs cannot meet and
distinct incident arcs remain in disjoint15-degree wedges. An ambient
isotopy preserves disjoint interiors and the Jordan boundary. This uses the
same written bounded-deformation principle as the attributed
[four-corona reader](../heesch_trapezoid_four_coronas/README.md), but the present
reader imports no prior executable or data.

With frame R^2 followed by translation (48,-19), this n=12 pattern is

    (0,4,47,-18), (1,2,46,-18), (0,5,23,5), (0,5,23,7).

The reader verifies that frame conversion exactly. These four poses occur
in a privately verified210-copy four-corona prefix with layer counts
1,13,47,73,76. The public theorem and reproduction do not depend on that
private prefix, its SAT construction class or its enumeration. In particular
the prefix cannot have a fifth surround, but this is a specific-prefix
failure; other four-corona prefixes of T_12 remain possible.

For a construction whose selected old copies must admit another surround,
every isometric image of these four poses gives the sound necessary clause

    not S1 or not S2 or not S3 or not S4.

Fixed copies already required in that construction may be omitted from
the clause. This geometric cut can be used before materializing a whole
next-corona inventory. It excludes only a specified pattern and does not
claim a complete obstruction list, an exhaustive corona census or a global
height bound. Similarly the run lemma gives complete local covering pairs,
not a sufficient global corona construction. A candidate surviving these
conditions still needs physical, containment, topology and preceding-corona
contact checks.

## Exact reader and primary-source context

Run `python3 check.py` as described in[README.md](README.md). The reader
uses only Python's standard library. Affine coefficients prove the stated
inequalities for all n>=8 and all3<=j<=n; these are not finite width samples.
It independently derives the12 D6 matrices, the two bottom placements, the
two whole-flat alternatives, the old tangent halfplanes, the overlap margins
and the n=12 positive pattern. Five malformed certificate controls must fail,
and optimized Python is rejected. The finite-star and whole-mating bridges
are credited written lemmas; this reader does not formalize them or provide
independent peer review.

Primary literature and corona conventions remain
[Kaplan2021/2022](https://arxiv.org/abs/2105.09438),
[the author dataset](https://cs.uwaterloo.ca/~csk/heesch/), and
[Kaplan2025's Heesch section](https://arxiv.org/html/2509.12216v1).
Known finite-six and finite-five constructions keep their prior attribution.
The connected Euclidean finite-seven target remains open in this campaign.
