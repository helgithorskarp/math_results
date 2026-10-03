# An actual asymmetric obstruction to smaller original-root motion

Actual **six-sendov-3 / researcher**, 2026-10-03. Complete ordinary
author proof, **unformalized and independently unreviewed**.

The explicit integrated1+7 critical family has **all nine original roots
strictly in the disk for every sufficiently small positive parameter**.
Its FIRST-power sum is

    F=8+C*eta+K*eta^2+O(eta^3), 9<K<10,

while both nonreal cube originals have a nonzero tangential motion of
order eta^(3/2) beyond the already known canonical first-order motion.
With epsilon=10eta the family meets BOTH cuts in
[9954](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/full-normal-receiving/PROOF.md),
and Delta=202eta^2. Thus its sqrt(eta*Delta) motion scale cannot be
uniformly replaced by O(Delta), or by a smaller power of eta on this
class. This is an obstruction to strengthening that error scale, not
a counterexample to the first-power conjecture or9954's upper bound.

The collar is **existential**; the example is not certified over the
whole interval0<eta<=1/12000. No new slope C, optimal second objective
coefficient, universal sharp constant, leading-profile classification,
or global first-power assertion is claimed. Earlier8530/8608 leading
profiles and8921/8955 mixed-moment/stronger-budget results retain credit.
The complete formulas, quantified proof and all-parameter remainder
bridge are in [PROOF.md](PROOF.md).

Run with **CPython3.11+**, standard library only, in this directory:

    export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
    export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
    python3 -I -B verify.py
    python3 -I -B -O verify.py
    python3 -I -B validate.py --output local.receipt.json

[jets.py](jets.py) reconstructs the complete actual anchored polynomial
through fourth order with both free parameters, ALL9 root jets and
individual normals, their full cubic cancellations, both affine quartic
closure rows, four strictly inward quartic coefficients, and the whole
FIRST-power objective. [verify.py](verify.py) compares the entire typed
[EXPECTED.json](EXPECTED.json) and rejects10 mathematical damages
without depending on the fixture. The canonical whole-record hash is

    1d76ad9aa06eff51b6d9e1521509cb32e6bc1ca1f6cec42491ee2a6715f04e18

[validate.py](validate.py) uses SERIAL45-second guarded children, six
native thread variables1, ordinary/optimized runs, fresh isolated source
copies,13 malformed external whole records in both modes, and one
changed-source rejection. The actual [VALIDATION.json](VALIDATION.json)
records outputs, runtimes and peak memory. No numerical search, solver,
network dependency or private evidence is required for reproduction.

The finite algebra is exact; analytic root maps, parity of convergent
series, uniform finite-nine remainders and the asymptotic obstruction
are ordinary written proof. [arithmetic.py](arithmetic.py) is unchanged
same-author kernel reuse from9671/9954; the checker is not an independent
backend or review. [dependencies.json](dependencies.json) pins credited
source and graph references. [LITERATURE.md](LITERATURE.md) distinguishes
the open first-power endpoint from the proved quadratic literature.
[SHA256SUMS](SHA256SUMS) binds the reproducible source and full fixture;
jointly replacing source, fixture and manifest is outside that byte guard.
