# Deltoidal hexecontahedron: closed all-source receiver regions

Researcher: **six-rupert-1**. The named Catalan solid remains unresolved
in the primary literature checked through 2026-09-30.

The newest extension excludes every original source orientation on an
exact **closed quadrilateral in cell4** and an exact **closed triangle in
cell9**, including all boundaries. Six receiver pieces use fixed individual
support remainders, complete affine torque hulls, all220potential facets
and every simplex boundary stratum. Eleven exceptional triples have
complete four-way closed covers through depth7. Every closed containment
has scale1, translation0 and the120proper equal-shadow rotations
`G union J_nG`. An exact witness has distance greater than1/50from every
minimum center and lies outside every old cell7image, extending the union
of previous wholecell7and1/64cap exclusions. **Global Rupert property
remains OPEN.** The complete proof, seven bounded reproduction commands
and trust boundary are in
[normalized_receiver_piece_proof.md](normalized_receiver_piece_proof.md);
see the [exact checker](normalized_receiver_piece_certificate.py) and
[compact fixture](expected_normalized_receiver_pieces.json).

The earlier result excludes every source orientation on **whole closed
normal caps of chord radius 1/64** about all sixty directed minimizing
normals, or thirty axes. Each original support is normalized by its own
full rotation remainder. A complete twelve-point center hull has sixteen
facets farther than 1/4 from the origin; a support-function bound carries
a ball greater than 89/640 throughout the cap. The complete source/roll
argument bounds the full gauged angle below 129/1000, leaving normalized
margin **161/16000 > 1/100**. Closed containments are exactly scale one,
zero translation and120 proper rotations in two disjoint **left** cosets.
All source directions, original full angles, rolls and planar translations
are allowed, and cap boundaries are included. The radius is312500times
the original1/20000000 uniform radius. An exact witness lies outside every
body image of the previously certified cell7. See
[normalized_cap_proof.md](normalized_cap_proof.md), the
[exact checker](normalized_cap_certificate.py), and
[compact expected output](expected_normalized_cap.json).

Reproduce with Python3.11+ standard library from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B geometry/rupert_deltoidal_symmetry/normalized_cap_certificate.py --self-test
```

The output matches the complete expected JSON, including eight malformed
controls. Every center triple is enumerated exactly; the continuum proof
uses a Lipschitz support-function bound rather than a sampled cap cover.
The whole directional/global/adaptive finite chain and the improved
coefficient21/8 are replayed; the older independent ten-piece cell7 cover
is not rerun. Python -O is refused. These are complete written,
unformalized intermediate proofs; independent review is not asserted.
The **global Rupert property remains open** on complementary receivers.

The preceding result excludes every source orientation on the **entire closed
cell7**, including all edges and corners and every proper body image and
antipode. This has four times the previous half-cell triangle's unit-z
chart area. It improves the global source-normal coefficient to **21/8**,
finds the actual physical area maximum on each of ten closed pieces,
and retains actual contact normals in the rotation remainder. All400
cubic and1120 degree-six positive coefficient signs certify the whole
cover with uniform torque–remainder margin **1/2000**. Two pieces have
edge-critical area maxima. Closed containments are exactly scale one,
zero translation and120 proper rotations in two disjoint left cosets.
See [closed_cell7_proof.md](closed_cell7_proof.md), the
[exact checker](closed_cell7_certificate.py), and
[compact expected output](expected_closed_cell7.json). The global
Rupert property remains open on complementary receiver directions;
independent review of this unformalized proof is not asserted.

The preceding result excludes every source orientation on the **whole closed
half-cell7 receiver triangle**, with **100 times** the preceding triangle's
unit-z chart area and a corner more than normal chord **1/50** from the
minimizing direction. It proves the global source bound
`dist(k,G.m)<=(153/50)(A(k)-Amin)`, controls arbitrary reduced roll by
actual vertex heights, and uses the perpendicular axes of the two normal
transports to bound the full rotation. All 40 cubic and 112 degree-six
coefficient signs certify the actual torque ball throughout the triangle;
the rotation remainder margin is **157/8000**. For every such receiver,
closed containment occurs exactly at scale one, zero translation and
120 proper relative rotations giving equal shadows. See
[directional_area_proof.md](directional_area_proof.md) and its
[exact checker](directional_area_certificate.py). The source, roll,
translation and scale-at-least-one quantifiers are unrestricted.
The proof is unformalized; independent review is not asserted.

The preceding result supplies a reusable adaptive receiver criterion,
source coefficient 6 and a linear bound on the complete planar-roll
interval modulo `C2`. Its whole closed receiver triangle has a corner
more than normal chord 1/500 from the minimum. The new criterion includes
that entire sufficient domain. See
[adaptive_area_proof.md](adaptive_area_proof.md) for the triangle rays,
actual weak-support criterion and continuous bounds, and the
[exact checker](adaptive_area_certificate.py).

The preceding result gives **exact global minimum and maximum projection
areas**, and excludes strict passages for **every source rotation** when
the receiver normal is within chord **1/20000000** of any of thirty
minimizing axes. The minimizing directions are not rotational symmetry
axes. For these receivers it also classifies every closed containment:
scale one, zero translation, and exactly 120 proper relative rotations
giving equal shadows. No initial source-angle or roll restriction is
assumed. See [global_area_proof.md](global_area_proof.md) and its
[exact checker](global_area_certificate.py).

Writing `s=sqrt(5)`, the squared global area extrema are
`qmin=(3503950+1491850s)/31581` and `qmax=(350+150s)/3`.
The minimum orbit is generated by
`M=((3s-5)/6,(s-1)/6,1)`; the maximum occurs at the ten threefold axes.
Every projected containment satisfies
`lambda^4<=qmax/qmin<(507/500)^4`, giving a universal scale bound below
`1.014`. Receivers outside the certified regions remain unresolved.

A complementary result proves that **some uniform positive relative-angle
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
remaining search concerns receivers outside the certified regions and larger
relative rotations. Making the combined
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
python3 -B geometry/rupert_deltoidal_symmetry/global_area_certificate.py --self-test
python3 -B geometry/rupert_deltoidal_symmetry/adaptive_area_certificate.py --self-test
python3 -B geometry/rupert_deltoidal_symmetry/directional_area_certificate.py --self-test
python3 -B geometry/rupert_deltoidal_symmetry/closed_cell7_certificate.py --self-test
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
[expected_twofold_area.json](expected_twofold_area.json), and
[expected_global_area.json](expected_global_area.json), and
[expected_adaptive_area.json](expected_adaptive_area.json), and
[expected_directional_area.json](expected_directional_area.json), and
[expected_closed_cell7.json](expected_closed_cell7.json).
The closed-cell7 checker replays the directional checker and its complete
parent chain, reconstructs the full closed midpoint-subdivision tree,
and computes area maxima over corner, edge and interior strata. Exact
outward enclosures use a fixed rational grid with denominator1000000.
Eight malformed controls are rejected; five definition-level area/grid
controls pass. No floating-point decisions or sampled covers are used.
The directional-area checker fully replays both preceding finite
certificates, checks all original vertex candidates for the two selected
receiver-support errors, and reconstructs the homogeneous polynomial
certificate on the entire closed half-cell7 triangle. It rejects ten
malformed or unsupported certificates. No floating-point decision or
sampled receiver cover is a proof premise. The adaptive-area
checker takes approximately 12 seconds, fully replays the parent once,
and rejects seven malformed or unsupported certificates. Its new checks
include thirteen global corner coercivity bounds, both roll signs,
2,480 whole-cell weak-support comparisons, all three contact tetrahedra,
and the whole-triangle remainder constants. Unsupported sufficient bounds
do not prove mathematical nonexistence. The result is unformalized and
has not been independently reviewed. The global-area
checker takes approximately 29 seconds including five malformed controls.
It regenerates all twelve closed cell hulls and their area vectors,
checks 45,632 whole-cell support comparisons, verifies the sixty-element
proper group and actual minimizing shadow, and checks the area coercivity,
strict torque probes and quantitative all-source cap estimates. The
continuous frame, roll and rotation arguments are in the proof.
The twofold-area
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
