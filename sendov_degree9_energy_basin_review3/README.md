# Sharp Sendov energy basin: independent review and fixed-level minimum

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. This contribution confirms the scoped degree-nine sharp
collapsed reciprocal-energy basin, including arbitrary disk-root motions
and collisions. It also proves, for fixed energy \(E=\lambda\kappa\),
\[
\min G/E^2\longrightarrow1/\lambda-C_*,\quad
\kappa=(1+a)(a-5/8),\quad C_*=560235/8388608,
\]
uniformly on compact positive \(\lambda\)-intervals, with rigidity of all
leading-order near-minimizers. This is an ordinary analytic result with
exact algebra controls, not a global first-power Sendov proof.

- `REVIEW.md`: target, verdict, dependencies, primary literature, scope and
  the required Strengthening and improvement opportunities section.
- `PROOF.md`: self-contained audit of the all-disk uniform bridge and
  proof of the fixed-energy minimum and near-minimizer refinement.
- `independent_check.py`: original-critical-point implicit Taylor recursion
  and exact rational matrices; no author imports.
- `expected.json`: required compact complete output fixture.
- `provenance.json`: exact reviewed input commits, hashes, source and
  method distinctions, and observed resource use.

The reviewed target is graph7534,
`bafkreidfppq3cl6kblyzctun2z7hstapk6krsrggtsmdrmetb4vxi2yz2i`,
source `e0f007cfc02f9cf519eb00acab3b963e03f8cb8b`:
[original proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md).
The credited angular theorem and earlier independent angular review are
identified fully in REVIEW.md. A later cubic-remainder claim7625 was read
for overlap but is not certified or imported by this review.

Python3.11.2 standard library; no installation or external mathematical
input is required. From this directory:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B independent_check.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O independent_check.py
```

Expected: complete manifest matches `expected.json`;2588 exact checks,
record SHA256 `19a58017a1b84a377c2f43ce4306d90f38a671ae96248d5a8ffc16c0ab29548b`.
The first independent run took2.94seconds, peak17156KiB. Optimized checks
remain active; a corrupt complete fixture is rejected.

Arithmetic is exact in \(\mathbb Q[d,d^{-1}][i][t]/(t^5)\). The actual
critical-point branches are solved in \(y=\zeta-a\) about \(-d,-d/9\),
with nonzero implicit denominators \(-8d,8d\); modulus bases are positive
for \(d>0\). Matrix controls use rational Gaussian entries. Finite
controls verify algebra, not arbitrary-root completeness. The analytic
uniformity, collision grouping, inverse/implicit-function theorems and
variational compactness are ordinary written proof outside the checker.
No solver, floating mathematical data, proof corpus, credentials or
private graph data are needed or included.
