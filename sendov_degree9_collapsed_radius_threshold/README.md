# Degree-nine collapsed stability: an exact radius threshold

Author **six-sendov-2**, role **researcher**, 2026-09-30.

For a marked real root \(5/8<a\le1\), put
\(u_k=(a-z_k)^{-1}\), \(v=(1+a)^{-1}\),
\(E=\sum|u_k-v|^2\), and \(\kappa=(1+a)(a-5/8)\).
If all roots lie in the closed unit disk and
\(\max|u_k-v|\le\kappa/13000\), the written proof establishes

\[
\sum_{j=1}^8\frac1{|a-\zeta_j|}
 \ge\frac{16}{1+a}+\frac\kappa2E.
\]

The original root condition \(\max|z_k+1|\le\kappa/5000\) suffices.
The baseline equality family is exactly \((z-a)(z+1)^8\).
For every \(0\le a\le5/8\), the explicit unit-circle family
\((z-a)(z^2+2cz+1)^4\), \(99/100\le c<1\), violates that
radial baseline and converges to the collapsed family as \(c\uparrow1\).
Thus \(5/8\) is the exact local threshold for this radial baseline.
Rotation gives the complex marked-root version. The neighborhood constants
are conservative, and the coefficient is half the upper limit imposed by
the exhibited perturbations.

This is a local first-power result with arbitrary complex perturbations;
the unrestricted Tang--Zhang first-power endpoint is not proved.
The original Sendov target is covered by the newer primary proof report.
See [PROOF.md](PROOF.md) for all hypotheses and the optional reduction
excluding the earlier collapsed small-surplus branch when
\(\sigma\le4(1-a)\), and [LITERATURE.md](LITERATURE.md) for comparisons.

## Reproduction and trust boundary

Python **3.11.2** was used; Python 3.10 or later suffices. No packages,
external certificate, solver, floating-point arithmetic, or numerical
eigenvalue computation are needed. From this directory run:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py
```

Expected output is `status: PASS`, **323 exact checks**, zero external
inputs and floating-point operations, and four rejected mutations.
The checks use rational matrices, coefficient comparison of sparse
polynomials over \(\mathbb Q\), and rational inequalities.
They check the finite algebra; the spectral count, contour remainder,
disk interpretation, monotonicity, and scope are ordinary written proofs.
This is not Lean formalization, a global search, or independent peer review.

Source and finite algebra have been checked by the author. Independent
review is pending. No historical priority or optimal neighborhood is claimed.
