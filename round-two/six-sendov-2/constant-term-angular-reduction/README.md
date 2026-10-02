# Feasible constant-term / six-moment angular reduction

Author: **six-sendov-2**, researcher. Ordinary proof plus exact finite
certificates; unformalized and independently unreviewed.

For a balanced real-rooted degree-eight auxiliary polynomial with seven
distinct criticals, all nonnegative mass vectors with its fixed six coupling
moments are realized by constant-term shifts. Their feasible interval is exact.
The fiber optimum is the six-moment least-squares value plus an explicit
clipping penalty. It reduces the global angular search to collision profiles
or positive centered eight-root profiles; six explicit coefficient equations
describe first-order stationarity of the latter.

An exact eight-root example with angular quotient above24.53 has an
infeasible unconstrained center with two nonreal roots. Clipping and singleton
examples prevent incorrectly dropping feasibility. This does not prove the
global angular maximum or the complex degree-nine first-power conjecture.
The classical constant-term method and least squares retain their prior credit.

Read [PROOF.md](PROOF.md) for all quantifiers, normalization and degenerate
cases, and [LITERATURE.md](LITERATURE.md) for predecessor and literature scope.
No predecessor code, CAS, solver or external certificate is required.

From the repository root, using **CPython3.11 standard library**:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 50s python3 -I -B round-two/six-sendov-2/constant-term-angular-reduction/verify.py --expected round-two/six-sendov-2/constant-term-angular-reduction/expected.json

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 50s python3 -I -B -O round-two/six-sendov-2/constant-term-angular-reduction/verify.py --expected round-two/six-sendov-2/constant-term-angular-reduction/expected.json

Run these commands sequentially. Every fixture field is compared, including
exact rational coefficients, all critical-root enclosures and all formal
coefficient derivatives; assertions are not used for mathematical checks.
Expected summary:

    status=checked
    records=8
    simple_critical_profiles=6
    mathematical_negative_controls=6
    record_sha256=d10fc8928eb11f398e56159285b707a869a7c36ade2c714cfbec2fc7f3587d10

Runtime/RSS fields vary. Native mathematics threads are one. The checker uses
exact rational polynomial/Sturm arithmetic, full seven-dimensional compression,
quotient-ring residue traces and independent first-order dual/root-motion
derivations. Its 36 first-variation comparisons are exact algebra, not finite
differences. Mathematical predicates use no floating point.

The universal real-rootedness/realization/variational proofs in PROOF.md remain
ordinary mathematics. Finite controls corroborate those proofs and do not
enumerate the remaining global strata. Formal coefficient derivatives at
collision examples do not assert two-sided legal root perturbations there.

The checked fixture can be regenerated explicitly:

    python3 -I -B round-two/six-sendov-2/constant-term-angular-reduction/verify.py --write-fixture /tmp/constant-term-angular-fixture.json

Compare the complete JSON or its canonical hash; the output path is chosen
explicitly. Generated scratch and private reports are excluded from publication.
