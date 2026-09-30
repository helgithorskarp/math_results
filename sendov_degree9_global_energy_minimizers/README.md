# Exact degree-nine fixed-energy minimizers and analytic basin

Actual author **six-sendov-3**, role **researcher**, 2026-09-30.
Complete ordinary written author proof with exact algebra controls.
**Independent review of this extension is pending.**

For a degree-nine polynomial with a simple marked root \(a\), set
\[
v=(1+a)^{-1},\quad E=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2,\quad
F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad G=F-16v.
\]
All original roots lie in the closed unit disk, and all algebraic
multiplicities are counted.

For each finite \(B>0\), at all sufficiently small positive energies
\(e\) with \(5/8\le a\le5/8+B e\), the **global minimum over the full
disk-root energy level** is attained exactly at the analytic stationary
one-plus-seven branch
\[
(z-a)(z+e^{i(7t+m)})(z+e^{i(-t+m)})^7
\]
and its conjugate, up to root permutation and polynomial scalar.
Here \(E=e\), \(t^2=e/(56v^4)+O(e^2)\), and
\[
m=t^3w(a,e),\qquad
w(a,e)=\frac{392a^2-413a+140}{20(1+a)^2}+O(e).
\]
The common mean is the actual stationary one, not just its cubic
approximation.

The new completeness bridge proves a uniform local domain:
seven-root split at most \(\epsilon t^2\), mean error at most
\(\epsilon t^3\), total inward depth at most \(\epsilon t^6\).
A full seven-point holomorphic trace plus one scalar norm defect has
fixed-energy excess divisible by \(t^6\), jointly analytically in
the scaled variables. Its positive limiting Hessian and inward
gradients give coercivity on a fixed scaled box. The independently
reviewed sextic concentration rates put every global minimizer in
that box, completing the classification.

Consequently the universal energy basin for \(G\ge0\), near \(a=5/8\),
is **exactly the analytic crossing of this branch from the right**, with
\[
\mathcal R_E(a)=\kappa/C_*+\Gamma\kappa^2+O(\kappa^3),\quad
\kappa=(1+a)(a-5/8),\quad
C_*=560235/8388608,\quad
\Gamma=2965647537471488/20111391661725.
\]
Both displayed coefficients were previously established and reviewed.
The exact analytic identification and stronger remainder are new
to this contribution. [PROOF.md](PROOF.md) gives hypotheses, dependencies,
the uniform bridge and global completeness.

The signed crossing curve extends analytically across \(a=5/8\).
The actual basin equals zero on the left, so its two-sided description
is \(\mathcal R_E(a)=\max\{0,e_c(a)\}\); it has a corner at the cutoff.
The analyticity statement concerns its right-hand restriction.

This is a local marked-radius and small-energy classification.
The constants and energy cutoff are existential. It does not establish
the unrestricted first-power inequality \(F\ge8\), arbitrary-energy
classification, an effective numerical neighborhood, or historical priority.
[LITERATURE.md](LITERATURE.md) separates classical methods, direct
premises, independently reviewed inputs and complementary team work.

## Exact reproduction

Python 3.10+ standard library only, tested with **Python 3.11.2**.
From this directory, run the two commands sequentially:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both compare the complete required [expected.json](expected.json),
including every compact profile field. Expected summary: **66 exact
identities**, **six complete scaled-profile records**, **six internal
corruption controls**, record SHA-256
**89750ea71c04b6dde42e551c16a58ac5fa6b415d94865614ae52335f645cb754**.
The fixture includes the full records, rather than aggregate counts alone.

The normal and optimized runs took 60.6 and 26.3 seconds under the
observed shared-host load, with peak child memory under 23 MiB.
Separate optimized runs rejected missing, malformed and altered fixtures.
All numerical thread counts were one; runs were sequential.

Arithmetic is rational Laurent polynomials in formal positive
\(V=(1+a)^{-1}\), Gaussian coefficients, and order-eight formal jets
in \(t\). The actual energy is solved through degree eight. The far
root is solved implicitly at its simple positive background. The
simple near root is solved after forming the divided characteristic
polynomial before truncation, avoiding a loss of seven input orders.
Holomorphic near traces follow from exact Newton identities; scalar
support coefficients follow from the explicit primitive derivative.
Only support coefficients through degree six and near-root changes
through degree four are reported. Degree-eight input suffices for these
claims; no higher output coefficient is evidence.

Six profiles cover positive/negative cubic mean shifts, paired and
unequal seven-root angular splits, a combined motion, and independent
inward depths. The checker also verifies the full leading compression
basis and the zero-sum linear expectation. Its leading profile excess
is \(5V^3y^2+L(V)\|x\|^2+2V^2\sum r_j\); the ordinary analytic proof
requires only its positive quadratic/linear derivatives, not inference
of a universal polynomial from these finite profiles.

The kernel openly adapts this author's preceding local-minimum checker.
It imports no campaign code, CAS, numerical library, solver, corpus,
or floating proof input. These are author checks, not independent review.
The divided-contour uniformity, degree completeness, analytic divisibility,
coercivity, reviewed concentration, coordinate bridge, compactness and
basin crossing remain ordinary written mathematics outside a formal kernel.
Missing, malformed and altered required fixtures must fail, including
under optimized Python. No search or solver outcome supplies a theorem.
