# Exact analytic degree-nine first-power boundary minimizer

Actual author **six-sendov-3**, role **researcher**.

[PROOF.md](PROOF.md) proves that, for every sufficiently small positive
eta, the unique monic degree-nine disk-root polynomial marked at1-eta
minimizing the reciprocal first-power sum is a real analytic curve. Its
derivative has six coincident real critical points and one conjugate pair;
exactly four original roots are on the unit circle. A positive radial-slack
penalty and twelve-coordinate quadratic gap hold around the exact
minimizer, without an asymptotic truncation error. The collar is
existential. Independent review of this extension is pending.
An implicit family saturating the four active root constraints proves
the small-imaginary eta^2 error is optimal on fifth excess-budget classes;
more generally it proves the corresponding rates for every fixed q>=3.

From the repository root, CPython3.11+, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-sendov-3/analytic-boundary/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-3/analytic-boundary/verify.py
```

Both pass **61 exact checks**, reject **eight mathematically damaged
identities**, and match the complete [expected.json](expected.json).
The exact record hash is recorded in [provenance.json](provenance.json).
Missing, malformed and mathematically altered fixtures reject in both
modes. `--fixture PATH` selects a copied record. `--write` regenerates a
development record and is not independent validation of changed evidence.

The finite computation verifies the leading generic anchored polynomial,
the four-normal root/slack Jacobian, all nine leading original-root
radials, active root curvature, exact dual identities and the complete
twelve-variable finite tangent Hessian. It uses exact rational arithmetic
in a cubic number field and quadratic Gaussian extensions; all embedding
signs have rational brackets. The local arithmetic kernel is credited in
[algebra.py](algebra.py); no prior checker or fixture is imported at runtime.

The analytic root maps, divisibility/parity, implicit inversions, uniform
negative slack derivatives, Hessian continuation, complete competitor
coverage and symmetry are ordinary written mathematics, outside a formal
kernel. [LITERATURE.md](LITERATURE.md) specifies the reviewed premises,
Miller's prior repeated-critical-point family, complementary campaign
work and the open scope. [provenance.json](provenance.json) records final
validation and baseline attribution; [SHA256SUMS](SHA256SUMS) covers the
compact source packet. One local mathematical job with native threads1
suffices. No solver, numerical optimizer, resource increase, effective
collar or global first-power proof is claimed.
