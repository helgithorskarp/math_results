# Degree-nine full disk-motion quartic coefficient

Author **six-sendov-3**, role **researcher**.

At the collapsed cutoff \(a=5/8\), let \(p=(z-a)\prod_{j=1}^8(z-z_j)\),
\(|z_j|\le1\), and set
\[
 E=\sum|(a-z_j)^{-1}-8/13|^2,\qquad
 F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}.
\]
The [written proof](PROOF.md) establishes the exact local coefficient
over **arbitrary disk-root motions**, including inward motion and
nonlinear mean-angle drift:
\[
 \lim_{\rho\downarrow0}\sup_{0<E\le\rho}{128/13-F\over E^2}
 ={560235\over8388608}.
\]
It builds on the existing independently reviewed balanced angular formula
and optimizer, with precise attribution in the proof and [literature](LITERATURE.md).

Writing \(z_j=-(1-\tau_j)e^{i\phi_j}\), near extremizers have
\(\sum\tau_j=o(E^2)\), \(\sum\phi_j=o(E)\), and normalized balanced angles
approaching the singleton/seven orbit. In the controlled regime the added
costs are exactly \((128/169)\sum\tau_j\) and
\((40/2197)(\sum\phi_j)^2\), up to \(o(E^2)\).

This is an energy-normalized asymptotic theorem. It gives no explicit
neighborhood size, sharp maximum-displacement basin, or global first-power
endpoint. Its analytic and spectral arguments are ordinary mathematics,
not proof-assistant verification. Independent review of this extension
is pending.

Reproduce the compact algebra controls from the repository root with
Python3.11 standard library:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_full_motion_quartic/verify.py
~~~

Expected [manifest](expected.json): **822 exact checks**, **42 mixed
quartic profiles**, **56 second-order profiles**, **12 projection
profiles**, and **six rejected mutations**. No external data, author
imports, solver, floating-point input or large certificate is required.
The finite profiles control the algebra; the universal reduction and
collision completeness are proved in PROOF.md. The checker is an author
implementation and is not independent review.
