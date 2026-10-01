# Quantitative degree-nine boundary profiles

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof; independent review is pending.

This extends the [sharp second-order boundary theorem](../quartic-boundary/PROOF.md).
Its exact constants $C,B_*$ and selected opposed-pair profile retain credit.
The new result gives a uniform cubic-order remainder and a quantitative
joint critical-profile gap.

Write $\eta=1-|a|$ and $F_p(a)=\sum|a-\zeta_j|^{-1}$. After rotating
the marked root to $a=1-\eta$, let $\mathcal D_\eta$ be the Euclidean
distance of $(\Im\zeta/\sqrt\eta,\Re\zeta/\eta)$ from the finite
permutation set of the selected limiting profile.
For every fixed second-order upper budget $F\le8+C\eta+M\eta^2$,

\[
F-8-C\eta-B_*\eta^2
\ge \kappa\eta^2\mathcal D_\eta^2-K_M\eta^3.
\]

The positive coercive coefficient is universal; the collar and error
constant may depend on $M$. These constants are existential.
In particular the radius-wise minimum is
$8+C\eta+B_*\eta^2+O(\eta^3)$.

A bounded third-order surplus forces
$\mathcal D_\eta=O(\sqrt\eta)$: six critical imaginary coordinates
are $O(\eta)$, while the opposed pair is
$\pm\sqrt{H/2}\sqrt\eta+O(\eta)$.
An explicit two-pair disk-root family proves both this profile rate
and the squared-distance penalty exponent are optimal.
No third-order optimal coefficient or full first-power endpoint is claimed.

Read [PROOF.md](PROOF.md) for quantifiers, uniform pair averaging,
the full constrained Hessian, compactness and attaining families.
[LITERATURE.md](LITERATURE.md) records dependencies and claim boundaries.

## Reproduction

Use Python **3.11** standard library only (tested with 3.11.2).
From repository root:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      python3 -I -B round-two/six-sendov-3/profile-stability/verify.py

Expected:

    PASS: 54 exact checks; 4 mutations rejected.
    Complete record SHA256: 5ff07bc8b7780b772ab2ee4133cdf8c2e05037d69eaad42c401ef9a64e2d4c62

The complete [expected.json](expected.json) is required; every record
must match. Normal and optimized Python both pass. Missing, malformed
and altered fixtures reject under optimization. The development option
--emit-fixture prints a replacement fixture to standard output; ordinary
verification writes no files.

The generic eighteen-variable calculation has **2,852 derivative terms**
and **6,256 anchored terms** through sixth square-root order.
It checks conjugation parity, real/imaginary remainder orders and the
full six-variable constrained profile Hessian. A distinct
cubic-field three-variable kernel builds the two-pair derivative and
primitive and checks its complete objective polynomial. Exact active-root
arithmetic, with a degree bound and exact interpolation, certifies the
radial identity for all profile parameters.

The arithmetic kernels extend the previous author checker with attribution;
no prior source is imported. In-place sparse substitution matches every
record from the completed reference implementation. One optimized run
took **9.416 seconds**, maximum RSS **35,496 KiB**, one process/thread.
Normal execution plus three external damage controls took 31.443 seconds
in total, child peak RSS 36,732 KiB. Timings are descriptive.

The checker certifies finite algebra. Uniform root-map derivatives,
pair-average evenness, global profile coercivity, compactness and all-root
containment are ordinary written arguments, not formalized certificates.
No numerical roots, solver, enumeration, external data or large corpus
is a proof input; author validation is not independent review.
