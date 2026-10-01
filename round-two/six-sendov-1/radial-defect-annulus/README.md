# Radial defect and degree-nine first-power annulus

Actual author: **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with explicitly cited mathematical dependencies;
independent review of this extension pending. The full first-power endpoint
remains open here.

[PROOF.md](PROOF.md) proves a new radius-sensitive real origin gap. For
eight radii r with r_j >= 1/(1+a), sum r_j <= 8 and 0 <= a <= 1, let

    O_a(r) = 9 integral_0^1 product_j(1-at r_j) dt,
    y_j = (1+a)r_j - 1,
    D_a(r) = 2a e_2(y) - e_3(y) >= 0.

Then

    (1+a)^8 [O_a(r) - product r_j] >= 8(1-a^9) + 5D_a(r).

Combined with the previously published quadratic phase estimate, this gives
an explicit shape-dependent phase criterion. A finite variance/spread bridge
and the previously published polar-mean and mean-tube lemmas then exclude the
joint polar/origin/critical-disk system throughout

    1 - 10^(-10) <= a < 1.

Consequently every degree-nine disk-root polynomial has strict critical
reciprocal sum greater than eight at every marked root in this annulus.
Critical multiplicities are arbitrary; collisions give infinity.
There is no stated linear margin or claim that this annulus is optimal.
The prior narrower effective annulus keeps credit for its stronger margin.
[LITERATURE.md](LITERATURE.md) records the dependencies and neighboring work.

Reproduce from the repository root using CPython 3.10+ and its standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/radial-defect-annulus/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/radial-defect-annulus/verify.py

Expected: PASS, all 636 Bernstein coefficients reconstructed in two algebraic
routes and fully inverted; 590 positive, 46 zero, minimum positive 7/4;
17 full polar-prefactor coefficients, 15 finite rational comparisons,
six damaged fixtures rejected, and an unsupported penalty certificate rejected.
Canonical coefficient SHA256:

    dbc01b552f13ae0747d667c9bf732211f95c967350b43864e23ae879ce5f73be

The default checker only reads the compact [expected.json](expected.json),
which contains every rational coefficient. An explicit `--emit` regenerates it.
There are no external code or data imports, floating-point proof inputs,
solvers, large certificates, or omitted computations. The checker verifies
finite polynomial identities and rational comparisons. The minimizer reduction,
Maclaurin/log-concavity arguments, complex Taylor bound, communication identities
and inherited mean-tube lemma remain ordinary mathematical proof obligations.
Author checks are neither independent review nor machine formalization.
