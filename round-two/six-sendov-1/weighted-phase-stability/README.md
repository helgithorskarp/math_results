# Weighted phase stability and an explicit first-power annulus

Actual author: **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite algebra checks. Independent
review of this extension is pending; the analytic bridges are unformalized.

[PROOF.md](PROOF.md) proves the factor envelope

    |1-tau r| <= (1-tau/2)^(3/2-r),   0<=tau<=1, r>=1/2.

For eight complex q, radii r=|q|>=1/2 and sum r<=8, define

    O_a(q) = 9 integral_0^1 product_j(1-at q_j) dt,
    epsilon = sum_j |q_j-r_j|,
    Delta = sum_j (r_j-Re q_j).

The proof gives an all-phase exponential estimate and an adaptive rational
estimate with exact degree-four coefficient polynomials. For epsilon<=1/100,
the resulting weighted phase inequality is

    Re O_a(q) >= O_a(r) - (3/2)Delta - (30/49)epsilon^2.

It implies an unweighted coefficient207/98 on the same small-phase domain.
With r_j>=1/(1+a), a<1 and Delta<=(1-a)/41, it also implies
an explicit positive origin excess369(1-a)/64288.

Combined with the published radial-defect, polar-mean and mean-tube lemmas,
the weighted bound excludes the relaxed origin/polar/critical-disk system on

    1 - 10^(-7) <= a < 1.

Consequently every degree-nine disk-root polynomial has critical reciprocal
sum strictly greater than eight at every marked root in that annulus.
Critical multiplicities are arbitrary; collisions give infinity. The annulus
inherits the mean-tube lemma's ordinary author proof, still independently
unreviewed. No global first-power endpoint, optimal width or linear surplus
for the unconditional polynomial annulus is asserted. The conditional phase
criterion's origin margin is a different quantity.
[LITERATURE.md](LITERATURE.md) identifies all dependencies and prior work.

From the repository root, use CPython3.10+ and the standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/weighted-phase-stability/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/weighted-phase-stability/verify.py

Expected: PASS, four exact positive-cubic coefficients, two full integral
coefficient routes, fifteen Bernstein controls on three complete cells with
full inverses, the exact derivative factorization, fourteen rational
comparisons, and five damaged fixtures rejected. The complete rational fixture
is [expected.json](expected.json), with canonical record SHA256

    8ce61ad314c6ce78f0309f0d72634f7d087e6557a4cac283356757fb916374bf

Default runs only read that file; `--emit`
explicitly regenerates it. No external code/data, floating-point proof input,
solver or omitted certificate is needed.

The checker verifies finite algebra and constants. Logarithm/product bounds,
the complex segment, Taylor integration, communication identities and
inherited analytic lemmas remain ordinary written mathematics. Author checks
are neither independent review nor proof-assistant formalization.
