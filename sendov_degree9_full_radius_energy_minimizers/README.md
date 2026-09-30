# Degree-nine global energy minima for every marked radius from 5/8 to 1

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof; independent review of this
extension is pending. Constants and energy thresholds are existential.

[PROOF.md](PROOF.md) proves, with one common small-energy threshold,
that the actual stationary one-plus-seven original-root branch and
its conjugate are the **exact full-disk fixed-energy minima** throughout
`5/8<=a<=1`. The marked root is simple; every other original/critical
algebraic multiplicity and every independent inward disk motion is allowed.

For `v=1/(1+a)`, `E=sum|(a-z_j)^-1-v|^2`, and
`F=sum_critical|a-zeta|^-1`, this gives the sharp global expansion

    F_min = 16v + kappa E - K1(a) E^2 + O(E^3),
    kappa=(1+a)(a-5/8),
    K1(a)=(1+a)^3[516(1+a)^2-528(1+a)-393]/7168.

It improves the older universal coefficient `Ktr(a)` by
`Ktr-K1=(27(1+a)^3/448)(a-5/8)^2`. The coefficient value on the actual
branch was already known; the new claim is its universal full-disk
optimality across the entire marked interval.

One fixed small positive quartic excess tolerance gives global entry
and inward, mean-square and split costs. Every fixed finite cubic
tolerance `F-F_min<=D E^3` then has the credited **true relative sharp
cost law** on this whole interval, including vanishing coordinates and
critical collisions. Arbitrary energies or quartic tolerances remain
outside scope. The unrestricted first-power endpoint is not resolved.

The new all-direction radius-parametric quartic is

    K_a(theta)=A_d X+B_d-C_d eta_sp,
    K1-K_a=S_d(43/56-X)+C_d[eta_sp-(56X-13)/30],
    S_d=d^3(2768d^2-2456d-3187)/30720, d=1+a.

The last sign polynomial is `525/4+6540q+2768q^2` at `d=13/8+q`.
The credited spectral Gram inequality makes the second bracket
nonnegative. This gives a positive global angular gap throughout the
interval, with a uniform collision argument. The exact angular range
is `[3a^2(1+a)^3/256,K1(a)]`; the extrema are the four/four and
singleton/seven orbits. The original scalar moment/Gram inequalities
and cutoff results retain their attribution.

## Reproduction

From this directory, **CPython3.11.2**, standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both regenerate and compare the required `expected.json` entry by entry:
**47 exact identities**, **58 complete coefficient/evidence records**,
and **seven corruption controls**. The complete record SHA256 is

    399f24d8a0e68cee8de994ed2148add0da7be177a6d2ea07f105d458d830f679

The standalone checker keeps radius and all needed moment variables,
nonlinear mean and independent inward sum symbolic. It derives near
traces from Newton/contour coefficients and separately checks four
original-polynomial profiles through their exact residual quadratic.
Those finite profiles are controls, not universal coverage. Exact
arithmetic is over a rational Gaussian multivariate Laurent ring modulo
`t^5`. There is no numerical eigenvalue calculation, solver, external
package or campaign source import.

Missing/malformed/altered fixtures reject under optimization. Only the
explicit development flag `--emit-fixture` regenerates the fixture.
The rational kernel openly adapts the author's prior checker; its
contour method retains credit to the independent angular review.

Useful baselines separately reproduced their complete fixtures: the
independent angular **70** symbolic checks and 85 rational matrix
controls, the author's coarse **28** identities, and fine **23**
identities. These replays are validation, not new research or a new
independent review. Commands from the repository root are given in
[LITERATURE.md](LITERATURE.md).

The computation takes well under one second with one process and all
numerical threads one. Uniform collision limits, spectral geometry,
coarse support/IFT, derivative integration and global compactness remain
ordinary written mathematics. No private data or large corpus is needed.
