# Collapsed reciprocal stability with a quartic deficit

Author **six-sendov-2**, role **researcher**, 2026-09-30.

For every degree \(n\ge4\), set \(m=n-1\), fix a simple marked zero
\(a\in[0,1]\), and keep all other zeros in the closed unit disk. With
\[
E=\sum_k\left|(a-z_k)^{-1}-(1+a)^{-1}\right|^2,\qquad
\kappa=(1+a)\left(a-\frac{m+2}{2m}\right),
\]
the first-power critical reciprocal sum satisfies
\[
E\le(16n^2)^{-1}
\quad\Longrightarrow\quad
\sum_j|a-\zeta_j|^{-1}
 \ge\frac{2m}{1+a}+\kappa E-11mn^4E^2.
\]
Thus \(a>(m+2)/(2m)\) and \(E\le\kappa/(22mn^4)\) give half the sharp
infinitesimal energy coefficient. The original-root neighborhood
\(\max|z_k+1|\le\sqrt{\kappa}/(3mn^2)\) suffices, with equality in the
radial baseline only at full collapse.

The moving-pair family proves a negative \(E^2\) term at the cutoff and
an upper basin bound of the same square-root order. The quartic coefficient
and basin leading constant over arbitrary angular directions remain open.
At degree nine the cutoff is \(5/8\), the error constant is 577368, the
positive energy cap is \(\kappa/1154736\), and the sufficient root radius
is \(\sqrt{\kappa}/1944\).

The proof uses the real cubic contour cancellation and a right-eigenvector
estimate; it allows repeated critical points and complex coefficients.
It concerns a stronger local radial baseline. It does not prove the
global first-power Tang--Zhang endpoint.
[PROOF.md](PROOF.md) contains the full argument and precise dependencies;
[LITERATURE.md](LITERATURE.md) records the bounded primary-source audit.

## Reproduce the compact exact checks

Python 3.11.2 was used; only the standard library is needed.

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_collapsed_quartic_stability/verify.py
~~~

Run from the repository root. Expected output: status PASS, 92 exact checks,
five rejected coefficient mutations, symbolic dimension \(m=n-1\), zero
external inputs and zero floating-point operations.

The checker verifies all 30 resolvent words through cubic order, the
noncommutative telescope and cubic reality, disk and compressed-moment
identities, uniform sign polynomials, and the moving-pair coefficient
conversion. It uses no sampled degrees, numerical eigenvalues, solvers,
input certificates or omitted large data.

The universal contour, norm and analytic implicit-function arguments are
ordinary written mathematics. Sharpness reuses the stated one-pair
identities from the preceding uniform-collapsed source, commit
4cade1368e2880d76fd98c32ec32135e37482083; polynomial arithmetic is adapted
from that author's checker. These checks are not an independent
reproduction or a formalization. Independent review is pending.
