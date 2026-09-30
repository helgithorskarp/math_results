# Deltoidal hexecontahedron: a uniform strict small-angle gap

Researcher: **six-rupert-1**. The named Catalan solid remains unresolved
in the primary literature checked through 2026-09-30.

The strongest result proves that **some uniform positive relative-angle
bound excludes strict passages for every receiver direction**, allowing
both directions to vary, arbitrary translations, and scales at least one.
[twofold_area_proof.md](twofold_area_proof.md) closes the remaining fifteen
twofold axes using twelve unequal-radius singleton supports and an exact
projection-area formula. At those axes the receiver caps have chord radius
**1/200**, with full relative rotation angles at most **1/200 radians**.
The combined global bound is existential; no numerical value is computed.
The global Rupert property remains unresolved.

The previous exact reduction at the 30-axis orbit left **one oriented
rotation-axis ray** at each representative: the corresponding body mirror
normal. Two of its three incident receiver cells were also excluded.
[contact_family_proof.md](contact_family_proof.md) proves this with two
three-contact polynomial stresses, without assuming a rate at which
the receiver approaches the exceptional direction.

The preceding mirror-branch certificate closes that remaining branch. An axial vertex and
its two neighboring support edges force the axial drift to be at most
1/1000 of the deviation from the mirror axis. The full polynomial stress
weights then have positive lower bounds. Reflection covers both signs
in an explicit parameter box of radius 1/10000000. Compactness gives
positive receiver and angle neighborhoods at all 30 orbit directions;
numerical sizes of those geometric caps are not computed.

That proof additionally constructs a two-parameter family of nontrivial
**proper closed containments** with angles tending to zero and exactly
sixteen permanent vertex-edge contacts. The optimal closed scale is one;
the family supplies no strict passage. It shows why uniform exclusion of
closed containment cannot extend across the second exceptional orbit.

The earlier 45-axis exceptional representatives are `(0,0,1)` and `(1,phi,1+3phi)`, where
`phi=(1+sqrt(5))/2`. At each of their 45 orbit axes, a maximum-radius vertex
projects to full radius, which excludes that exact fixed inner view for
every receiver. The neighborhood bounds outside these axes are pointwise;
compact sets avoiding the 45 axes admit a uniform positive bound excluding
even closed containment for nonzero relative angles. The mirror-branch
result left only fifteen axes, now closed by the twofold-area proof.
Every fixed inner orientation is also excluded from arbitrarily small
reverse passages; [stable_proof.md](stable_proof.md) supplies that proof.

The earlier result covers **every fixed outer orientation**: for each
direction `u`, some `epsilon(u)>0` excludes every nonzero relative rotation
through at most `epsilon(u)`, for any translation. Together the results
show that the solid is neither locally Rupert nor locally reverse Rupert
in Scott's two distinct definitions. See
[orientation_proof.md](orientation_proof.md) for the fixed-outer theorem.

The fixed-outer certificate partitions a reflection chamber into twelve
direction cells and sixteen triangles. Four contact gradients on each triangle
give a positive equilibrium through homogeneous cubic determinants.
The checker verifies all 640 nonnegative coefficients, all 11,904 support
comparisons, and every boundary direction. The earlier twofold contact
certificate supplies the one exceptional corner.

The stable certificate adds strict exposure probes throughout all polygon
interiors, all 25 open boundary edges, and 12 nonexceptional nodes. Its
28,792 exposure comparisons and 400 nonnegative binary cubic coefficients
are exact. Perturbing weak contacts into those strict probes makes the
torque obstruction persist in a receiver neighborhood. At the exceptional
axes the unique-vertex probe cone degenerates, as separately checked.

A complementary restricted result is an exact optimum for passing its
fivefold shadow into its threefold shadow:

$$\frac4{\sqrt{10+2\sqrt5}+\sqrt3(5\sqrt5-11)}
 \in(0.971679451840,0.971679451841).$$

Together with exact area, circumradius, and inradius inequalities, this
excludes all nine ordered pairs of exact symmetry-axis projections.
For the six pairs of different orders, it also excludes perturbing
each axis by at most **1/1000 radians**, with any planar rotation or
translation. Inner directions perpendicular to any maximum-radius
vertex are excluded regardless of the outer direction.

An additional exact contact certificate excludes every nonzero
relative rotation of angle at most **1/10 radians** when the outer
orientation is fixed at any of these three symmetry axes. It includes
a reusable positive-combination criterion for proving a local
obstruction at other fixed projections.

This is an intermediate result about restricted passages. It gives
neither a passage nor a global non-Rupert proof for the solid. The
remaining search concerns larger relative rotations. Making the combined
global angle gap numerical is also open; the named question remains unresolved.

Read [proof.md](proof.md) for the analytic proof and precise scope.
[verify.py](verify.py) checks the geometric input, exact hulls, invariant
formulas, rational inequalities, and decimal enclosure using only
standard Python arithmetic in $\mathbb Q(\sqrt5)$.

From the repository root:

```sh
python3 geometry/rupert_deltoidal_symmetry/verify.py
python3 geometry/rupert_deltoidal_symmetry/local_certificate.py
python3 -B geometry/rupert_deltoidal_symmetry/orientation_certificate.py --self-test
python3 -B geometry/rupert_deltoidal_symmetry/stable_certificate.py --self-test
python3 -B geometry/rupert_deltoidal_symmetry/contact_family_certificate.py --self-test
python3 -B geometry/rupert_deltoidal_symmetry/frontier_certificate.py
python3 -B geometry/rupert_deltoidal_symmetry/stress_limit_certificate.py
python3 -B geometry/rupert_deltoidal_symmetry/mirror_branch_certificate.py
python3 -B geometry/rupert_deltoidal_symmetry/twofold_area_certificate.py --self-test
```

Python 3.11 or later; no third-party packages. Verified with Python
3.11.2. Expected outputs are [expected.json](expected.json),
[expected_local.json](expected_local.json),
[expected_orientation.json](expected_orientation.json), and
[expected_stable.json](expected_stable.json),
[expected_contact_family.json](expected_contact_family.json),
[expected_frontier.json](expected_frontier.json), and
[expected_stress_limit.json](expected_stress_limit.json), and
[expected_mirror_branch.json](expected_mirror_branch.json), and
[expected_twofold_area.json](expected_twofold_area.json). The twofold-area
checker regenerates both complete hulls, whole-cell supports, the local
area formula and scalar constants, and rejects three malformed controls.
The mirror-branch checker takes about one second and replays full polynomial
ideal decompositions, exact coefficient bounds and the prior stress check.
The contact-family
checker verifies 744 cubic gap polynomials over an entire parameter rectangle,
using 11,904 exact tensor Bernstein coefficients, and rejects three malformed
controls. The limiting-stress checker replays the full polynomial cofactor
identities, exact divisibility and leading-coefficient signs; it imports no
CAS transcript. The stable checker rechecks
the orientation certificate and takes approximately 19 seconds, including
four malformed-certificate rejection tests. The two older
checkers take approximately one second each; the orientation checker,
including four malformed-certificate rejection tests, takes a few seconds.
Each uses one process; the checker
does not load a solver or BLAS. Output comparisons are regression
checks; the mathematical proof is the argument and exact inequalities.

Coordinates are generated in the script from
[McCooey's standard model](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt).
There are no external input files or omitted large artifacts. The trust
boundary and primary literature are listed in the proof. Novelty is
limited to the formula and exclusion certificates not found in the
bounded primary sources searched; no priority claim is made.
