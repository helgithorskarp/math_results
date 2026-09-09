# Exact incidence exclusions for the complete radix architecture

Put E=Z[omega], where omega=(1+i sqrt(3))/2, let U be its six units, and
let D={0} union U. The architecture is

    A5(z) = {sum(a_j z^j, j=0,...,4): a_j in {0,1,omega}}.

An active displacement row d in D^5 has |sum d_j z^j|=1. The 2,796
nonmonomial rows, normalized by a common unit, have the original h4105
curve IDs. Circle ID 342 collects the four nonconstant monomial events.
The constant monomial is always unit and is treated as true.

**Theorem.** Every injective physical member avoids the 182,396 event
conjunctions generated below: 5,976 pairs and 176,420 triples. Every
non-four-colourable physical member also avoids all 8,376 constant-offset
pairs. Their union gives 184,796 distinct forbidden conjunctions for a
possible counterexample, valid regardless of how many other curves are
active. This does not assert closure of the eight-active gate or produce a
record graph.

## Collision dictionary

Every nonzero row in D^5 is a difference of two distinct digit labels,
coordinate by coordinate, since D=T-T. Thus injectivity is equivalent to
requiring P_d(z) != 0 for every nonzero row d. The exact pair inventory
checks this dictionary: all 29,403 unordered label pairs give 2,801 unit-
normalized nonzero rows. In particular, every nonzero polynomial mentioned
below with coefficients in D and degree at most four gives an actual label
collision when it vanishes.

## Six-phase pencils

Take two nonzero rows p,q in D^5 with disjoint supports, and write
P=P_p(z), Q=P_q(z). The six polynomials

    P + u Q,  u in U,

still have coefficients in D, and give six distinct nonmonomial events.
An injective realization has P != 0 and Q != 0.

**Three phases.** If three distinct values of u give |P+uQ|=1, the three
distinct points P+uQ lie both on the circle with centre P and radius |Q|
and on the unit circle with centre zero. The phase centres are noncollinear;
the checker verifies the twenty exact determinants. Two distinct circles
meet in at most two points, so their centres agree and P=0. This contradicts
injectivity. Consequently at most two events of any such pencil can be
active.

Equivalently, subtracting the three squared-norm equations gives two
independent real linear equations in P conjugate(Q), forcing that product
to vanish. This also covers all degeneracies without a numerical tolerance.

**Unit triangle.** If |P|=|Q|=|P+uQ|=1, the ratio P/(uQ) is one of the
two Eisenstein units with real part -1/2. Hence P-vQ=0 for a unit v.
Disjoint supports ensure that P-vQ is a nonzero D-polynomial, again a
label collision. Thus an endpoint pair and any one pencil event cannot
all be active in an injective member.

**An endpoint and two nonadjacent phases.** Suppose |P|=1 and
|P+uQ|=|P+vQ|=1. If |u-v|=2, the parallelogram identity gives |Q|=0.
If |u-v|=sqrt(3), subtracting |P|^2 from the other two equations gives

    Re((P/Q) conjugate(u)) = Re((P/Q) conjugate(v)) = -1/2.

Their unique solution is P/Q=-(u+v). Since |u+v|=1 in this case, the
result is another D-polynomial collision. The checker verifies this unit
identity for all relevant pairs. The same argument applies when |Q|=1,
after multiplying each phase event by its inverse phase and exchanging P,Q.
Adjacent phases, with |u-v|=1, are not excluded by this rule.

Each rule is a conjunction of two or three event IDs after substituting
the always-unit constant monomial. Conjunctions containing the circle
monomial are omitted, because the candidate frontier is off-circle. Every
conjunction that remains nevertheless forces a collision whenever its
listed equations hold; adding further active curves cannot remove that
collision.

## Completeness and exact counts

The producer splits each normalized nonmonomial row into all unordered
nonempty support partitions, retaining the least occupied position in its
first part, then varies all six relative phases. It deduplicates the sorted
six-event sets.

The independent checker takes a different route: it separately normalizes
every nonzero row, and enumerates every unordered pair with disjoint
supports. There are exactly

    (13^5 - 2*7^5 + 1)/(2*6^2) = 4690

such pairs. At each position a disjoint ordered pair has 13 choices: both
zero, a unit in p, or a unit in q. Subtract the two cases where one whole
row is zero and restore the doubly-zero case. The two independent unit
actions are free, and exchanging nonempty disjoint supports has no fixed
point. The checker verifies that all 4,690 pencils have distinct six-event
sets, and both algorithms obtain exactly the same set hashes.

Applying every rule to every pencil and removing duplicate conjunctions
gives 182,396 distinct sets: 5,976 pairs and 176,420 triples. These are
sufficient exclusions, not a claim that every impossible incidence has
been enumerated or that each listed set is inclusion-minimal.

## Constant-offset pairs

For an additional non-four-colourability exclusion, normalize a row by
its nonzero tail (coefficients of z,...,z^4). Its constant term is then an
element a of D. In any fixed tail bundle, two distinct events have the form

    |P(z)+a| = |P(z)+b| = 1,  a != b in D.

If one offset is zero, the other is a unit and the two circle intersections
give P(z) an Eisenstein-unit value. If both offsets are units, the
intersections are P(z)=0 and P(z)=-a-b; in the antipodal case they coincide
at zero. In every case P(z) lies in E. Since P has degree between one and
four with unit leading coefficient, z satisfies a monic E-polynomial of
degree at most four. The accepted h4119 paired-residue theorem therefore
three-colours the entire physical graph, including possible collisions.

Consequently a possible counterexample can activate at most one curve in
each tail bundle. There are (7^4-1)/6=400 bundles: four monomial tails have
six retained curves, and the other 396 have seven. This yields

    4*C(6,2) + 396*C(7,2) = 8376

forbidden pairs. The union with the phase-pencil conjunctions has 184,796
members. This second rule asserts three-colourability, not impossibility
of a physical realization. Its distinction from the collision-only rule
is preserved in the exported interface.

## Use and verification boundary

`produce.py` uses the original h4105 geometry implementation. `verify.py`
uses the direct label-pair inventory from the independently replayed h4151
checker, then enumerates separately normalized disjoint row pairs. Neither
path reads a private input export. Their complete canonical interface
exports agree byte for byte. The phase and offset proofs above use exact
unit identities, elementary circle geometry, and the imported h4119 theorem;
they are not proof-assistant formalized. No SAT, CAS, root approximation,
or floating-point computation is needed for this result.

The running eight-active search motivated these constraints but is not a
premise of this theorem. An incomplete SAT cover, a solver timing, or an
abstract graph does not establish a physical chromatic result.
