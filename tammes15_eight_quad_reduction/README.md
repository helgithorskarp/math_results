# Thirteen necessary auxiliary types in the eight-quadrilateral Tammes-15 branch

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
deficit lies at two zero-triangle degree fours.
The necessary cover now has **14 degree/deficit profiles** and
**13 colored auxiliary types**, across three deficit distributions.

The [original proof](PROOF.md) uses spherical diagonal lengths, four-point
Gram rank, the two-point intersection of contact planes with the sphere,
and the sides of an embedded cycle. The hand proof is complete and
author-audited; independent review is pending. The exact checker audits
arithmetic identities, strict rational margins, and the finite auxiliary
cover. The refinements use contact-star incidence, the rhombus angle
involution and exact angle inequalities. The latest two polynomial signs
have 158 positive rational Bernstein coefficients. These checks
do not certify the geometric arguments in
a proof assistant. The original proof and checker remain unchanged, with
their earlier 35-profile/18-type claims; the two-five files retain 29/17.
The one-five files retain 23/16, and the boundary-patch files give 14/13.

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
(cd tammes15_eight_quad_reduction && sha256sum -c SHA256SUMS)
```

The current deterministic JSON gives all nine initial deficit distributions,
the three survivors, each of the 14 degree profiles with its permissible
colored auxiliary codes, and the nine newly removed profiles. Two-zero-triangle
profiles with n3=0,1 have only the empty H code. Earlier
JSON outputs retain the 35-profile, 29-profile and 23-profile stages.
Codes enumerate unordered pairs in lexicographic
order and minimize over permutations preserving vertex colors. A second
enumeration by partitions into paths and a possible four-cycle compares
every colored graph type with the exhaustive edge-mask enumeration.
There are at most four auxiliary vertices and at most 64 masks per
distribution. Cover enumeration takes well under a second; polynomial
certificate verification also takes only seconds, using one thread.
These computations are not searches over spherical embeddings.

Primary context and dependencies appear in the four proof files. The current
Cohn table still lists the fifteen-point cosine approximately
`0.592605902926` without an optimality
asterisk, and its coordinate bytes were refreshed before this work. The
prescribed 29-contact completion and its new
[thirteen-vertex, twenty-four-contact core](../tammes15_contact_pattern_obstruction/CONTACT_CORE.md)
and its [cyclic companion](../tammes15_contact_pattern_obstruction/CYCLIC_CORE.md)
by six-tammes-2 are complementary, and are citations rather than premises.
No historical-priority claim is made.
