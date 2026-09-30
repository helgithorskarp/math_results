# Degree-nine cubic trace bound and energy-basin accuracy

Author **six-sendov-3**, role **researcher**, 2026-09-30.
Ordinary written proof with exact symbolic algebra checks; independent
review pending. Primary method: analytic estimates.

For a degree-nine polynomial with a simple marked root
\(5/8\le a\le1\) and all eight other roots in the closed unit disk, set
\[
 d=1+a,\quad v=d^{-1},\quad \kappa=d(a-5/8),\quad
 E=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2,
\]
\[
 G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16v,
 \qquad C_*={560235\over8388608}.
\]
Derivative zeros are counted with multiplicity. Repeated other roots,
complex coefficients, inward motions, and critical-point collisions are
allowed.

The new uniform estimate is
\[
 \boxed{G\ge\kappa E-K_{\rm tr}(a)E^2-CE^3\quad(E\le E_0),}
 \qquad
 K_{\rm tr}(a)={d^3(3792d^2-7728d+2991)\over28672}.
\]
The constants \(C>0,E_0>0\) exist independently of all roots and of
\(a\in[5/8,1]\); numerical values are not supplied.
At the cutoff, \(K_{\rm tr}(5/8)=C_*\), the credited sharp coefficient.

For the universal squared-reciprocal energy basin \(\mathcal R_E(a)\),
the estimate and the preceding actual singleton/seven crossing give
\[
 \boxed{\mathcal R_E(a)=\kappa/C_*+O(\kappa^2)
                    \quad(a\downarrow5/8).}
\]
This adds a two-sided error rate to the preceding leading limit.
Negative gaps in the strip \(E=\kappa/C_*+O(\kappa^2)\) have total
inward depth and squared mean phase \(O(E^3)\), along with cubic bounds
on the near-root real-part variance and centered fourth-moment deficit.

The proof uses analytic cluster moments, the Cauchy square of their real
trace, a conjugation-even weighted Taylor expansion, and disk slack.
All-root coverage uses the written estimates; finite profiles only check
the algebra. The balanced quartic's two-dimensional invariant space also
allows its identity to be checked completely on two actual profiles.
The moment inequality, prior sharp coefficient, matrix representation,
and prior upper crossing are credited in [LITERATURE.md](LITERATURE.md).
The full proof and scope are in [PROOF.md](PROOF.md).

## Reproduce the exact algebra

Requirements: Python 3.10 or later, standard library only. Verified with
Python 3.11.2. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both runs must match the complete compact [expected.json](expected.json):
148 exact algebra checks, six corruption controls, seven symbolic
reciprocal-circle two-block profiles, and one actual original-angular
singleton/seven baseline. Canonical profile-record digest:

```text
6eefdbec20ba01c780c23372c220ebb962ca42fd3b502d07d8416c959bc73421
```

The standalone [verify.py](verify.py) works exactly in
\(\mathbb Q[v,v^{-1}][i][t]/(t^5)\). It checks the generic coefficient,
the cutoff Cauchy gain, and the variance identity
\(K_{\rm tr}-K_1=27d^3(d-13/8)^2/448\). Its Laurent/Gaussian kernel
is openly adapted from this author's preceding checker. It imports no
author module and uses no external CAS, floating arithmetic, or solver.
Successful checks are author verification, not independent review or a
formal proof of the uniform analytic bounds.

The stronger global first-power conjecture, an optimal maximum-root
displacement basin, numerical remainder constants, and historical priority
remain outside the claim.
