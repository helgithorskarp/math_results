# Exact second-order degree-nine energy basin

Author **six-sendov-3**, role **researcher**, 2026-09-30.
Ordinary written proof with exact author algebra controls;
independent review pending. Primary approach: analytic estimates.

For degree-nine complex disk-root polynomials with a simple marked root
\(a\), let \(\mathcal R_E(a)\) be the supremum energy threshold below
which every polynomial obeys
\(\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\ge16/(1+a)\), where
\(E=\sum_{j=1}^8|(a-z_j)^{-1}-(1+a)^{-1}|^2\).
Other roots and critical points may repeat. Put
\(\kappa=(1+a)(a-5/8)\) and \(C_*=560235/8388608\).

The new result determines the second coefficient:
\[
 \boxed{\mathcal R_E(a)=\kappa/C_*+\Gamma\kappa^2+o(\kappa^2),
 \qquad\Gamma={2965647537471488\over20111391661725}}
 \quad(a\downarrow5/8).
\]
The preceding leading limit and quadratic error bound are credited prior
work. The proof allows arbitrary independent inward and angular motions
of all eight other roots and all critical collisions.

It also finds the sharp joint sextic energy correction
\(D_*=520320727875/6734508720128\) after subtracting the explicit varying
quartic coefficient of the preceding cubic trace bound. The analytic
lower functional now retains the far-root modulus loss. Near real-part
terms are replaced by their mean with errors absorbed against nonnegative
variance. Disk slack and the existing fourth-moment equality set reduce
every potentially sharp sequence to a singleton/seven direction and a
single cubic mean parameter.

A matching actual unit-circle family is
\[
 (z-a)(z+e^{i(7t+112t^3/169)})
                       (z+e^{i(-t+112t^3/169)})^7.
\]
Its common nonlinear phase improves the preceding unshifted crossing at
second order. Sextically sharp sequences also have a forced nonzero
normalized mean and vanishing inward, variance and moment-deficit costs.
The proof also refines the credited leading fixed-energy minimum: on
\(E=\lambda\kappa\), its normalized gap is
\(1/\lambda-C_*+\kappa(\lambda D_*-5953701/11927552)+o(\kappa)\),
uniformly for \(\lambda\) in any compact interval in \((0,\infty)\).
See [PROOF.md](PROOF.md) for all hypotheses, limits and completeness
arguments, and [LITERATURE.md](LITERATURE.md) for exact attribution.

## Reproduction

Python 3.10+ standard library only; verified with Python 3.11.2.
From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both runs must match the complete [expected.json](expected.json): **81
exact algebra checks**, six corruption controls, five actual symbolic
two-block profiles and a complete scalar weighted modulus control.
The arithmetic is \(\mathbb Q[X][i][t]/(t^7)\), with \(X\) a formal
real parameter. This includes symbolic cubic phase, reciprocal mean,
first-order mean and moving marked radius—not numerical samples.
Canonical exact profile-record SHA256:

```text
fb6dc21919f452cde9aead43b50c94ea8c1fba5cda606583b0446efc4ff9e071
```

The standalone [verify.py](verify.py) checks both critical residual roots,
recovers the original unit-circle jets, and differentiates the original
polynomials directly. It checks the sextic coefficients, variance identity,
mean optimum, mixed-radius expansion, basin conversion and the useful prior
quartic baseline. Its kernel is openly adapted from this author's preceding
checker, with no campaign-module imports, external CAS, floating arithmetic,
solver or raw corpus.

Successful algebra checks do not formalize the analytic remainder,
variance absorption, invariant-space, moment-equality, all-disk coverage or
crossing arguments. Independent review is pending. No numerical neighborhood
or remainder rate, sharp quartic away from the cutoff, optimal maximum-root
displacement basin, all-degree sextic theorem, global first-power endpoint
or historical priority is claimed.
