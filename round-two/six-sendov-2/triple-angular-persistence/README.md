# Triple-pair angular persistence

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) proves that the previously isolated triple-pair
angular equality profile at
\(a_3=(3\sqrt{29}-11)/16\) persists as the **complete global optimizer**
on an existential nonzero interval on both sides. It supplies uniform
quadratic root-distance stability, the sharp local constant \(32/21\),
and the exact second-order value and formal-square gap. The proof drops
collision weights to form an analytic upper bound, proves a strictly
negative full tangent Hessian, uses symmetry to attain the upper bound,
and promotes local uniqueness to global uniqueness by compactness.

Two additional results have deliberately narrower scope:

* Full tangent Hessian formulas give a certified **local** stability band
  \(21/136\le r\le161/1000\), or
  \(-208/9\le R\le-1129232/148877\). Global optimality on that whole
  explicit band is not established.
* On the entire symmetric triple family, the sharp inequality is
  \(\eta\ge1-(208/9)(X-1/8)\). Its nonuniform equality profile is
  \(r=21/136,t=5/136\). This is not proved for all balanced root vectors.

A cubic-discriminant calculation also extends the formal equality
polynomial's four-real/four-nonreal obstruction throughout the physical
radius range below \(a_3\). These angular results do not settle the
degree-nine first-power Tang--Zhang conjecture. The full-disk asymptotic
corollary credits its separate analytic reduction.

Run the standalone checker with CPython 3.11 or later, no packages:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Expected result for both commands:

```json
{"checks":34,"damage_controls":4,"record_sha256":"6c9210212480f7c435480d9e3adfd9f96bf74b3a079b8a05ab8fd9657af94488","status":"all exact checks passed"}
```

`verify.py` implements exact arithmetic in
\(\mathbb Q(r)[\mu]/(\mu^2-(3/8-2r))\), with polynomial gcd reduction.
It derives the active-weight Taylor coefficients from the polynomial
and its derivative, checks the universal Hessian formulas, separately
checks the equality-point Hessian by the spectral ODE and compressed
matrix traces, and verifies the full Bernstein and restricted-comparison
identities. It does not perform floating root approximation. All fixture
comparisons and damage controls remain active under `python3 -O`.
`--expected PATH` permits checking an independently copied fixture;
`--write-expected` is a maintainer regeneration option, not the normal
verification command.

The checker validates exact algebraic subclaims. The analytic arguments
and external inputs remain ordinary unformalized mathematics, and no
independent review of this artifact is asserted. Exact dependencies and
primary status are listed in [LITERATURE.md](LITERATURE.md).
