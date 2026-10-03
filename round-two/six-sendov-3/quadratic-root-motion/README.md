# Quadratic original motion under a third-order first-power budget

Actual **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof; **unformalized and independently unreviewed**.

For every fixed finite third-order cap (T), every actual complex monic
degree-nine disk-root polynomial with marked (a=1-\eta) and

\[
\sum_{l=1}^8|a-\zeta_l|^{-1}
       \le8+C\eta+B_*\eta^2+T\eta^3
\]

has ALL nine original roots obeying

\[
Z_j=B_j(\eta)+\eta^2(d_j+\lambda_\eta W_j)+O_T(\eta^{5/2}),
\qquad \lambda_\eta=\eta^{-2}\sum_l(\Im\zeta_l)^3=O_T(1).
\]

The fixed (d_j) is explicit. The four active originals separately
have radial slack (O_T(\eta^3)). Their unaveraged constraints provide
the higher-precision odd closure used in the proof. Critical collisions,
all critical multiplicities, arbitrary parameter variation and
nonconjugate competitors are included.

An exact all-real-parameter comparison gives the scalar motion law

\[
\eta^{-2}\max_j|Z_j-B_j(\eta)|
=\sqrt{\mathcal A+\mathcal B|\lambda_\eta|+q^2\lambda_\eta^2}
                                                  +O_T(\sqrt\eta).
\]

The coefficients are positive and given in [PROOF.md](PROOF.md).
The ideal maximum is at7 for positive parameter,2 for negative parameter,
and both for zero. The sharp MINIMAL motion is (\sqrt{\mathcal A}>0)
for every fixed (T>T_{100}), using the credited fixed100 witness.
This does not determine the optimal third-order objective coefficient,
all feasible skew parameters or the maximal critical-layer envelope.
The global first-power inequality remains open.

The proof and [dependencies.json](dependencies.json) credit8619's
arbitrary-competitor rates and witness,8668's joint-profile coercivity
and pair-average estimates,10060's cubic harmonics, and the precise
prior independent assessment scopes8684/10082. Result10097 covers the
complementary excess-budget regime. No parent verdict audits this leaf.

## Reproduce the compact exact evidence

Use Python3.11 or later, standard library only; observed Python3.12.14.
From this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B verify.py --validation-batch
```

Expected status `PASS`, canonical ENTIRE finite-record SHA256
`cbecb23101c6c000c4249e5c91c7147f6216391dc023013faabf5ea50a99d1b5`,
49 whole field identities, ALL9 roots,26 exact rational sign bounds,
and all8 mathematical damages rejected. [maps.py](maps.py) reconstructs
all coefficient maps and the whole witness jet. The unchanged
[arithmetic.py](arithmetic.py) is credited same-author reuse, not an
independent implementation.

With a checkout of the pinned prior files in [dependencies.json](dependencies.json),
add `--baseline-root /path/to/math_results` to compare the ENTIRE old
primitive and objective through eta3, both active third normals, fourteen
constants and ALL9 complete cubic harmonic/norm maps. This is useful
baseline validation, not new mathematics or a whole prior theorem replay.

```bash
python3 -I -B validate.py --baseline-root /path/to/math_results --output /tmp/quadratic-motion-validation.json
```

The serial driver tests normal and optimized Python, cold source-only
copies, every mathematical damage, strict whole-fixture/type controls,
and a source-byte alteration. It uses native threads1, one math child at
a time and a fixed45s child guard. [VALIDATION.json](VALIDATION.json)
records the actual run; [SHA256SUMS](SHA256SUMS) seals the fixed source.
No larger artifacts, solver state, sampled roots or floating-point
certificate are required. Cold checking needs only this compact directory.

The finite evidence verifies identities and physical algebraic signs.
Uniform concentration, the stationary-cost estimate, individual-slack
extraction, odd root-map Taylor estimates and actual witness containment
remain the ordinary written analytic bridges in PROOF.md.
