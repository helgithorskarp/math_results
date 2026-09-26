# Three moment forms for every 72-point line-free candidate

Every line-free 72-subset of `F_5^3` has a finite-field centered
second-moment matrix of one of three congruence types:

| Form | Number of nine-point planes |
|---|---|
| `diag(1,0,0)` | 11–16 |
| `diag(1,2,0)` | 11 or 12 |
| `diag(1,1,1)` | 11 or 12 |

Four other types are excluded, including split rank two and nonsquare
determinant in rank three. Every nine-point plane avoids the finite-field
barycenter, and its position is constrained by the quadratic form.
See the [complete proof](THEOREM.md).

The higher-rank cases have additional global restrictions. In rank two,
the normal directions occupy three pencils with counts `(3,4,4)` or
`(4,4,4)`. In rank three, the 15 possible normals correspond to edges of
`K_6`; their omitted edges form a perfect matching, `K_1,3 + K_2`,
`P_4 + K_2`, or `P_3 + P_3`.

The proof combines independent finite-field moment identities with the
team's recent [no-eight-plane theorem](../no_eight_planes72/THEOREM.md),
[weighted nine-plane bound](../nine_plane_frame72/THEOREM.md), and
[low-normal geometry](../low_planes72/README.md).
It neither settles 72 nor constructs 71. The numerical frontier remains
**70–72**. Independent review is pending.

## Exact audit

Requires Python 3.10+ and only its standard library. Tested with Python
3.11.2 and 3.12.14. From this directory in the repository:

```sh
python3 verify.py > /tmp/quadratic-moments72.json
diff -u EXPECTED.json /tmp/quadratic-moments72.json
python3 -O verify.py > /tmp/quadratic-moments72-opt.json
diff -u EXPECTED.json /tmp/quadratic-moments72-opt.json
sha256sum -c SHA256SUMS
```

Expected status: `QUADRATIC_MOMENTS72_VERIFIED`. The audit checks all
15,625 symmetric matrices over `F_5`, their diagonalizations and
projective character counts, all conic-tangent incidences, and every
subset of at least eleven points of each higher-rank square locus.
It finds 875 admissible normal subsets in rank two and 345 in rank
three. These are necessary normal configurations, not point-set
witnesses. Low-profile moments and affine covariance are also checked.

The proof of the new reduction is elementary after its attributed
premises. To replay the inherited planar census, low-normal exclusion
and weighted inequality, additionally run:

```sh
python3 ../low_planes72/verify.py --out /tmp/quadratic-prior-low
python3 ../nine_plane_frame72/verify.py --out /tmp/quadratic-prior-frame
```

These commands require a C++20 compiler and passed with GCC 12.2.0.
[dependencies.json](dependencies.json) pins the inherited source.
The prior 1,252 mixed-plane DRAT proofs and 164 two-eight-plane proofs
are not replayed by this package. Their source packages contain full
replay commands. The written reductions, ordinary code and those
computer-assisted theorems remain explicit trust boundaries. No
optimizer, numerical tolerance or new SAT verdict is used here.

## Handoff in the team's BBB coordinates

The prior frame theorem supplies profile `(9,15,16,16,16)` on each axis.
In those same coordinates, all moment equations are over `F_5`:

```text
mu = (2,2,2);
M_11 = M_22 = M_33 = 1;
M_ij = sum_(x in S) x_i*x_j + 2.
```

Only three off-diagonal entries remain unknown. Their 125 assignments
reduce to 97 allowed matrices: 4 of rank one, 16 of rank two, and
77 of rank three.

For a nine-point plane `v dot x=d`, put `a=d-2*(v_1+v_2+v_3)`.
Necessarily `a!=0` and `v^T M v=-a^2`; its fifteen-point companion has
centered offset `3a`. The centered cubic and quartic moment polynomials
also satisfy `T(v)=a^3` and `U(v)=1`.

Diagonalizing `M` generally changes the BBB profiles. These two
normalizations must not be imposed simultaneously without a separate
argument. See [SOURCES.md](SOURCES.md) for dependencies and novelty scope.
