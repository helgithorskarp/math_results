# Exact positive-face exclusion for Gaussian counterexample searches

The two-scale 16-site polar family has exactly **208 maximal support faces
of paired affine rank at most five**, for every invertible polar matrix and
every pair of distinct positive radii. These are known-positive Gaussian
cores. The classification and exact distance to their union reveal a search
boundary missed by the earlier ten isometric-face constraints.

The [author proof](PROOF.md) also consumes researcher 6's existing
[quantitative hinge margin](../gaussian_axial_cone_rotations/HINGE_MARGIN.md):
if a core has mass `q=1-epsilon` and certified hinge margin `b` at threshold
`a/q`, the full actual hinge gap is at least `q*b-epsilon`. This gives an
explicit uniform exclusion region, without any restriction on the remainder
law's support extent or atom count. It does not settle the full conjecture.

The faces have sizes 6, 7, 8 and 12, with counts 64, 96, 36 and 12. Their
distance `delta_5` is the minimum mass outside any certified mask. Its maximum
over weights is exactly `1/4`, attained by uniform weights. The constraint
`delta_5 >= eta` consists of 208 linear inequalities. A positive reserve
keeps a search away from these faces; it does not certify a negative or
positive Gaussian sign.

An exact all-positive-weight example has isometric reserve `1501/4000`, both
scale masses `1/2`, and rank-five reserve only `1/4000`. The
[compact historical packets](PACKETS.json) have still smaller reserves:

| Preserved packet | Exact rank-five reserve | Closest face size |
| --- | --- | ---: |
| first_negative | 72519/800000000 | 7 |
| identity_0 | 5000977000635028709/125000000000000000000000 | 12 |
| identity_3 | 80024163133280024167/2000000000002000000000000 | 12 |
| minimum_logged_gap | 673758340/1000000000001 | 12 |
| strongest_negative | 8000099/200000000000 | 12 |

Their historical names describe discovery bookkeeping. **None has a
certified negative sign.** Previous fresh floating checks reversed the
retained apparent negatives. This packet performs no Gaussian integration
and infers no full hinge sign from proximity. The
[exact audit](PACKET_AUDIT.json) records the full rank, core rank, distance
loss and centered radius for each reconstructed rational configuration.

Run from this directory with standard-library CPython 3.11 or 3.12:

```sh
python3 certify.py
python3 check_matroid.py
python3 audit_packets.py
python3 check_controls.py
python3 -O certify.py
python3 -O check_matroid.py
python3 -O audit_packets.py
python3 -O check_controls.py
sha256sum -c SHA256SUMS
```

Expected: 208 faces; all rational constant checks pass; all ten imported
isometric faces are contained; all 8008 six-subsets are examined, 5344 are
independent; five packet audits and four damage controls pass. Each program
takes only a few seconds on a single CPU. `certify.py --write` regenerates
the compact certificate; the normal mode checks it without modifying it.

`certify.py` constructs symbolic normals in the formal reciprocal radii.
`check_matroid.py` independently enumerates hyperplane closures at radii
1 and 2 modulo 65537; a Hadamard bound makes its ranks exact over the
rationals. It compares every mask, not just counts. Universality in radii
comes from the written classification, not from the one finite instance.
Both programs are author code; agreement is not independent peer review.

The analytic margin is an explicit dependency on Theorem H, not a new
geometric result of this lane. The mathematical proof and its analytic
premises are not formalized. There is no new Kneser--Poulsen consequence,
claim of historical priority, or certificate for the historical candidates'
signs. The [handoff](HANDOFF.md) specifies exactly what the finite and
counterexample lanes can use.
