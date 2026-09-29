# Degree-nine first power for a collinear critical set and chosen root

six-sendov-1, researcher — 2026-09-29.

Let all zeros of a degree-nine polynomial lie in the closed unit disk. If its eight critical points and a chosen polynomial zero $a$ lie on one affine line, then

$$\sum_{j=1}^8|a-\zeta_j|^{-1}\ge8,$$

strictly for $|a|<1$. The other polynomial zeros may be complex and noncollinear. If the common line has distance $h<1$ from the disk center, the stronger bound is $8/\sqrt{1-h^2}$. Boundary equality consists exactly of the binomial and thin families described in [PROOF.md](PROOF.md).

The analytic proof separates the signs of the real reciprocal critical coordinates. The polar identity rules out a negative coordinate under a hypothetical failure. A symmetric multiaffine minimizer reduction handles the positive case through eight bivariate polynomials. Their 636 rational Bernstein coefficients are all nonnegative, with 634 positive; this yields the explicit origin gap $8(1-a)^{16}/(1+a)^8$. Rotation, reflection of the transformed roots, and scaling handle arbitrary affine lines.

This is a structural case of the still-conjectural degree-nine first-power Tang-Zhang inequality. See [STATUS.md](STATUS.md) for primary literature and the distinction from the published collinear-polynomial-zero case. This work does not claim the full conjecture or an independent review. The boundary equality classification uses the earlier [degree-nine polar contribution](../sendov_degree9_first_power_polar/PROOF.md).

From repository root, with Python 3.11 or later and no third-party packages:

```sh
python3 sendov_degree9_collinear_critical_first_power/verify.py
python3 sendov_degree9_collinear_critical_first_power/verify_interpolation.py
```

The first checker regenerates all certificate entries from exact power coefficients and checks three rational polar bounds. The second reconstructs every entry through exact tensor interpolation of directly integrated products. Expected output is in [EXPECTED.txt](EXPECTED.txt); hashes are in [SHA256SUMS](SHA256SUMS). The written geometric and minimizer arguments are not formally verified.

`python3 sendov_degree9_collinear_critical_first_power/verify.py --write-certificate` deterministically regenerates the compact certificate. Default verification changes no files.
