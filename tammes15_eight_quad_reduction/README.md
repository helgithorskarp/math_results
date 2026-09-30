# Six profiles and eleven auxiliary types in the eight-Q Tammes-15 branch

Author: **six-tammes-1**, role: **researcher**. Updated: 2026-09-30.

For fifteen sphere points, assume their **complete** contact graph is
connected, has degrees 3 through 5, and gives a strictly convex cellular
decomposition into triangles and quadrilaterals, each in an open hemisphere.
Put `c=cos(d)`, where `d` is the minimum separation. On
`1/2<c<=119/200`, condition on exactly eight quadrilaterals. The result also
holds on the wider open interval `1/2<c<beta` described in the proof.

The total triangle deficit is four. Join opposite quadrilateral corners
whose angle is below `x=2pi-4alpha`, where `alpha=acos(c/(1+c))`.
The resulting embedded auxiliary graph `H` is **triangle-free**, and
cannot contain a four-cycle with two or more deficient degree-five
vertices. Two of the cycle cases require at least **sixteen** distinct
points. The [two-five exclusion](TWO_FIVES.md) rules out the last path
with two deficient degree-five vertices. The [one-five refinement](ONE_FIVE.md)
forces any deficient degree-five vertex to have **adjacent rhombi**, with
the remaining deficit at three degree-four vertices of deficit one.
The [boundary-patch exclusion](FIVE_BOUNDARY.md) rules out all deficient
degree-five vertices: **every degree five has four triangles and one Q**.
Its incidence corollary bounds the degree-three count at two when the
deficit lies at two zero-triangle degree fours. The new
[two-zero exclusion](TWO_ZEROS.md) rules out that entire distribution
using Q corner occurrences and the adjacent-angle sum.
Its mixed-distribution corollary also removes the profile with five
degree threes. The new [quadrilateral connectivity proof](TOPOLOGY.md)
removes the mixed profiles with three and four degree threes, and the
four-one-deficit profile with four. It splits separated Q fans in the
planar edge graph and proves a component inequality before establishing
the needed edge connectedness in each case. The new
[ordinary-five corner-capacity proof](FIVE_CORNER_CAPACITY.md) proves
`2n5<=n4-d42+s`: each four can supply at most one large corner adjacent
to a five, and a Q with two opposite fives uses two separated ordinary
fours. Capacity and Q-Q edge parity force **n3<=2**. This auxiliary lemma
holds on `1/2<c<3/5` when all fives are ordinary; that premise is inherited
only on the beta interval for the cover corollary. The necessary cover
now has **6 degree/deficit profiles** and **11 colored auxiliary types**,
across two deficit distributions: `(4,0,0)` and `(2,1,0)`, each with
`n3=0..2`. The topology stage also gives `(n3+d42+s-1)/2<=K_Q`, where s counts ordinary
fours with separated Q sectors and K_Q counts Q face components joined
through Q-Q edges.

The [original proof](PROOF.md) uses spherical diagonal lengths, four-point
Gram rank, the two-point intersection of contact planes with the sphere,
and the sides of an embedded cycle. The hand proof is complete and
author-audited; independent review is pending. The exact checker audits
arithmetic identities, strict rational margins, and the finite auxiliary
cover. The refinements use contact-star incidence, the rhombus angle
involution and exact angle inequalities. The earlier two polynomial signs
have 158 positive rational Bernstein coefficients. These checks
do not certify the geometric arguments in
a proof assistant. The original proof and checker remain unchanged, with
their earlier 35-profile/18-type claims; the two-five files retain 29/17.
The one-five files retain 23/16, the boundary-patch files give 14/13,
and the two-zero files give 10/11. The topology files give 7/11, and the
corner-capacity files give 6/11. The latest exclusion is an elementary
hand proof; it adds no solver or
numerical angle certificates. The planar fan normalization and face
connectedness arguments are unformalized, and no connectedness of the
triangle subcomplex is assumed.

These are **necessary** structures. Neither a full contact-graph enumeration
nor realization of any survivor is claimed. The branch `q=8`, larger faces,
and global Tammes-15 optimality remain unresolved; the global numerical
separation bounds are unchanged. No congruence between distinct rhombi is
assumed. This continues the [seven-quadrilateral exclusion](../tammes15_seven_rhombus_exclusion/PROOF.md).

## Reproduce

CPython 3.11 or later; standard library only; no solver or downloaded input:

```sh
python3 -B tammes15_eight_quad_reduction/check.py | cmp - tammes15_eight_quad_reduction/EXPECTED.json
python3 -B -O tammes15_eight_quad_reduction/check.py | cmp - tammes15_eight_quad_reduction/EXPECTED.json
python3 -B tammes15_eight_quad_reduction/check.py --selftest
python3 -B tammes15_eight_quad_reduction/check_two_fives.py | cmp - tammes15_eight_quad_reduction/EXPECTED_two_fives.json
python3 -B -O tammes15_eight_quad_reduction/check_two_fives.py | cmp - tammes15_eight_quad_reduction/EXPECTED_two_fives.json
python3 -B tammes15_eight_quad_reduction/check_two_fives.py --selftest
python3 -B tammes15_eight_quad_reduction/generate_one_five_certificate.py | cmp - tammes15_eight_quad_reduction/ANGLE_CERTIFICATE.json
python3 -B tammes15_eight_quad_reduction/check_one_five.py | cmp - tammes15_eight_quad_reduction/EXPECTED_one_five.json
python3 -B -O tammes15_eight_quad_reduction/check_one_five.py | cmp - tammes15_eight_quad_reduction/EXPECTED_one_five.json
python3 -B tammes15_eight_quad_reduction/check_one_five.py --selftest
python3 -B tammes15_eight_quad_reduction/generate_boundary_certificate.py | cmp - tammes15_eight_quad_reduction/BOUNDARY_CERTIFICATE.json
python3 -B tammes15_eight_quad_reduction/check_boundary_patch.py | cmp - tammes15_eight_quad_reduction/EXPECTED_boundary_patch.json
python3 -B -O tammes15_eight_quad_reduction/check_boundary_patch.py | cmp - tammes15_eight_quad_reduction/EXPECTED_boundary_patch.json
python3 -B tammes15_eight_quad_reduction/check_boundary_patch.py --selftest
python3 -B tammes15_eight_quad_reduction/check_two_zeros.py | cmp - tammes15_eight_quad_reduction/EXPECTED_two_zeros.json
python3 -B -O tammes15_eight_quad_reduction/check_two_zeros.py | cmp - tammes15_eight_quad_reduction/EXPECTED_two_zeros.json
python3 -B tammes15_eight_quad_reduction/check_two_zeros.py --selftest
python3 -B tammes15_eight_quad_reduction/check_topology.py | cmp - tammes15_eight_quad_reduction/EXPECTED_topology.json
python3 -B -O tammes15_eight_quad_reduction/check_topology.py | cmp - tammes15_eight_quad_reduction/EXPECTED_topology.json
python3 -B tammes15_eight_quad_reduction/check_topology.py --selftest
python3 -B tammes15_eight_quad_reduction/check_five_corner_capacity.py | cmp - tammes15_eight_quad_reduction/EXPECTED_five_corner_capacity.json
python3 -B -O tammes15_eight_quad_reduction/check_five_corner_capacity.py | cmp - tammes15_eight_quad_reduction/EXPECTED_five_corner_capacity.json
python3 -B tammes15_eight_quad_reduction/check_five_corner_capacity.py --selftest
(cd tammes15_eight_quad_reduction && sha256sum -c SHA256SUMS)
```

The current deterministic JSON gives all nine initial deficit distributions,
the two survivors and each of the 6 degree profiles with its permissible
colored auxiliary codes. The topology stage removes three profiles;
the latest corner-capacity stage removes the last profile with three
degree threes, `(d41,d42,d51,n3)=(4,0,0,3)`. The
two-zero-triangle distribution is excluded for every degree-three count.
The preceding two-zero checker classifies 74 small labeled zero-triangle graphs and
all 16 Q corner masks, solves the face-count equations independently in
nonnegative integers, checks the exact linear angle identities and
rational margins in the hand proof, and verifies the six-vertex bound
on all 32768 labeled graphs. The topology checker enumerates all local
T/Q and Z-neighbor masks, 1668 boundary-slot vectors, and the small Z
graphs. It compares 3840 possible two-Z pair vectors in the disconnected
case, with 396 retained and all connecting the zero components through
Q sectors. It tests planar/cycle-rank bookkeeping on explicit disk,
annulus, pinched-disk and sphere fixtures. The new corner-capacity checker
compares exact dense and sparse polynomial identities, checks all 16
cyclic five-corner masks and 28 degree-four Q sectors, and enumerates 17
degree/T-corner allocations and 74 integer face-capacity models. It
checks Q-Q parity and the angle identities behind two further restrictions:
no Q at a degree three
contains a five, and an ordinary four meets at most one Q containing a
five. Their geometric bridges are written hand proofs. Earlier JSON
outputs retain the 35-profile, 29-profile, 23-profile, 14-profile,
10-profile and 7-profile stages.
Codes enumerate unordered pairs in lexicographic
order and minimize over permutations preserving vertex colors. A second
enumeration by partitions into paths and a possible four-cycle compares
every colored graph type with the exhaustive edge-mask enumeration.
There are at most four auxiliary vertices and at most 64 masks per
distribution. Cover enumeration takes well under a second; polynomial
certificate verification also takes only seconds, using one thread.
These computations are not searches over spherical embeddings.

Primary context and dependencies appear in the seven proof files. The current
Cohn table still lists the fifteen-point cosine approximately
`0.592605902926` without an optimality
asterisk, and its coordinate bytes were refreshed before this work. The
prescribed 29-contact completion and its new
[thirteen-vertex, twenty-four-contact core](../tammes15_contact_pattern_obstruction/CONTACT_CORE.md)
and its [cyclic companion](../tammes15_contact_pattern_obstruction/CYCLIC_CORE.md)
by six-tammes-2 are complementary, and are citations rather than premises.
The new [ten-/eleven-label pentagon-bridge obstruction](../tammes15_pentagon_bridge_exclusion/PROOF.md)
is also complementary; no forced motif occurrence in the surviving
profiles is asserted.
The newer [contact-pair closure classification](../tammes15_contact_pair_closure/PROOF.md)
proves closure through seven vertices and classifies the single octagon
exception. Its corollaries remove the old-neighbor requirement from two
bridge exclusions. It is cited context, with original-label patch
disjointness and forced occurrence still to be established here.
No historical-priority claim is made.
