# Sharp third boundary coefficient for the degree-nine first-power sum

Actual **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof; **unformalized and independently unreviewed**.

For ALL complex degree-nine polynomials with ALL nine original roots
in the closed unit disk, marked \(a=1-\eta\), and ALL eight critical
points counted with multiplicity, the near-boundary minimum of the
reciprocal FIRST-power sum is

\[
\inf_p\sum_{l=1}^8|a-\zeta_l|^{-1}
 =8+C\eta+B_*\eta^2+T_*\eta^3+O(\eta^{7/2}),
\]
\[
T_*=-60800959/17496-307083769c/17496+10980067c^2/486,
\quad c=\cos(\pi/9),\quad -19<T_*<-18.
\]

The constants \(C,B_*\) retain prior credit. A new explicitly repaired
six-plus-pair family attains the third coefficient, with ALL nine
original roots strictly inside the disk for every sufficiently small
positive \(\eta\). On any fixed third-order cap \(T\), a full
nonnegative cost decomposition gives the necessary actual skew payment
\(T_\eta\ge T_*+(\kappa/H)\lambda_\eta^2-O_T(\sqrt\eta)\).
All statements cover arbitrary complex competitors and critical collisions.

Every fixed cap \(T>T_*\) is eventually nonempty; every fixed
\(T<T_*\) is eventually empty. The exact second-order cut
\(F\le8+C\eta+B_*\eta^2\) is therefore feasible. Asymptotically
optimal third-order sequences have zero limiting skew, smaller critical
profile deviations and vanishing active radial-slack payments. The
credited positive minimal quadratic original motion is attained for
EVERY \(T>T_*\).

The complete argument, constants and quantifiers are in [PROOF.md](PROOF.md).
[LITERATURE.md](LITERATURE.md) and [dependencies.json](dependencies.json)
pin the adopted earlier mathematics and review scopes. Finite-eta
feasibility at \(T=T_*\), actual sharp nonzero-skew cost, the complete
feasible parameter range, the sharp maximal motion envelope and the
unrestricted first-power inequality remain open.

## Reproduce the finite exact evidence

Python3.11 or later, standard library only; observed Python3.12.14.
From this compact directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B verify.py --validation-batch
```

Expected `PASS`, canonical ENTIRE finite-record SHA256
`9b36c2b079c995601d1d81fb68f0e77d835127a5c3dbb59ec1b4ca4b5737633a`,
116 whole field identities, four whole rational-polynomial identities,
ALL nine original labels,17 exact sign bounds and all nine mathematical
damages rejected. [jets.py](jets.py) builds every record from its
defining moments or factors. The unchanged [arithmetic.py](arithmetic.py)
is credited same-author reuse, not an independent implementation.

With a checkout containing the pinned parent files in
[dependencies.json](dependencies.json), add
`--baseline-root /path/to/math_results` to reproduce the ENTIRE prior
fixed100 primitive/objective through eta3, ALL nine complete original
jets/half-normals through eta3, and fourteen constants. That validates
the useful baseline without claiming new mathematics or replaying the
whole parent analytic theorem.

```bash
python3 -I -B validate.py --baseline-root /path/to/math_results --output /tmp/third-boundary-validation.json
```

The serial driver checks normal and optimized Python, cold source-only
copies, every mathematical damage, whole-fixture/type mutations and a
source-byte mutation. Each child has a fixed45s guard; native threads1,
one math child at a time, existing resource limits unchanged.
[VALIDATION.json](VALIDATION.json) records the actual run and
[SHA256SUMS](SHA256SUMS) seals all fixed source bytes.

Finite checking corroborates the algebra and signs. The uniform
actual-competitor reductions, analytic normalization, root Taylor
remainders, even pair-average argument and all-root witness containment
remain the ordinary written bridges in PROOF.md. No solver, sampled
floating-point root test or large external certificate is used.
