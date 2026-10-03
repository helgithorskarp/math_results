# Separation-only leading-mass and two-moment bounds

Actual **six-sendov-2**, researcher. Complete ordinary author proof,
**unformalized and independently unreviewed** at publication.

For eight **distinct real** original coordinates with balance0, squared norm1,
adjacent gaps>=specified delta in(0,1], at angular stationarity of exactly
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
the actual mass interpolant has

\[
 |p_5|\ge10^{-3936}\delta^{10400},\qquad
 \mu_3^2+\mu_5^2\ge(57600/4549)10^{-747976}\delta^{1977140}.
\]

This removes the supplied |p5|>=tau hypothesis from the two-moment estimate
[9952](../joint-moment-coercivity/PROOF.md). The constants are deliberately
coarse. No stationary-profile existence, collision continuation, physical H
estimate or complex first-power endpoint is asserted.

The [complete proof](PROOF.md) combines quantitative unscaled degree drop,
an actual stationary heat gap, the separation-only asymmetry margin
[10000](../quantitative-stationary-asymmetry/PROOF.md), and a six-root box
obstruction to the quadratic resonance. Projected coefficients are only used
in polynomial residual estimates and are never assumed to represent feasible
roots or positive masses. All exceptional factors remain in the proof.

From the repository root, with CPython3.10+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/leading-mass-separation-floor/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/leading-mass-separation-floor/verify.py
```

[verify.py](verify.py) regenerates the **entire** typed mathematical record
[expected.json](expected.json), using exact rational arithmetic:

* All13 residual rows,181 terms, complete Q/O/K/rho/Newton maps, and all13
  unscaled p5 difference quotients.
* All34 polynomial identities, the full projected quartic map, and every one
  of the six backward resonance inverse coefficients.
* All23 sufficient monomial comparisons on0<e<=M^-50,M>=100, and every scalar.
* Five damaged mathematical inputs reject without relying on expected.json.

Canonical whole-record SHA256:
`98eccc29981554fe0fea426e410d6f849ea2d70e12c2a8bfe7714c4e03a73423`.
An altered last coefficient of the full K5 row is a useful external fixture
rejection check. The ordinary universal root, heat and norm implications are
written in PROOF.md; code execution is not formal verification. Sparse Fraction
arithmetic and quotient-adjoint kernels adapt this same author's9496; no peer
implementation is imported and no independent review is implied.

There is no CAS runtime requirement, numerical root finder, solver, external
data or large certificate. Exact checks were developed with CPython3.12.14.
Native threads1, one serial mathematical child, fixed50-second guards;
normal/O checks took0.628517/0.806823seconds, with peak22512KiB. Older stopped global
searches remain incomplete and are not mathematical nonexistence premises.

Optional [compare_cas.py](compare_cas.py), with SymPy1.14.0, performs a
same-author alternate exact comparison of all10 full maps and all84 coefficient
polynomials. It uses SymPy polynomial long division and a logarithmic generating
series for the Newton traces. No portable checker or prior proof engine is
imported. This corroboration is neither independent review nor a formal proof:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-sendov-2/leading-mass-separation-floor/compare_cas.py
```

For inputs, current primary status and credit, see [LITERATURE.md](LITERATURE.md).
Independent [REVIEW9994](../../six-reviewer-5/joint-coercivity-audit/REVIEW.md)
confirms9952 relative to its dependencies and retains sharper constants; that
verdict does not review this new proof.
