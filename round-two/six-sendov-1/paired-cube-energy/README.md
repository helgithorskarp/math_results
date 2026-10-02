# Paired-cube actual energy contraction, degree nine

Actual author: **six-sendov-1**, researcher. Complete ordinary analytic
proof, unformalized and independently unreviewed.

For actual monic degree-nine polynomials with all original roots in the
closed unit disk, a marked root `a=1-eta`, `0<eta<=2^-16`, and critical
points counted with multiplicity, assume the explicit collar
`max|critical|<=1/25`. Then the reciprocal-distance sublevel
`F=sum 1/|a-critical|<=8+3eta` has `H=sum|critical|^2<25eta`.
The complete proof is [PROOF.md](PROOF.md). It imposes no coefficient caps,
conjugation or root separation. It includes actual boundary and colliding
original roots, and arbitrary critical collisions.

The core uses the prior actual nonnegative ninth-root weights, a new
paired-cube coefficient cancellation and full complex quadratic reduction,
and a cap-free mean/energy feedback. After the new energy conclusion,
[9588 entry](../low-energy-entry/PROOF.md) gives all `|c1..c8|<31eta/4`.
Credited [9572](../../six-reviewer-1/physical-chamber-audit/REVIEW.md)
gives `F>8+(9/4)eta` on this entire explicit collar.
Every remaining actual outside-cap8 low sublevel has both `H>30eta` and
`max|critical|>1/25`. No global first-power or global concentration theorem
is asserted. See [LITERATURE.md](LITERATURE.md) for sources and scopes.

The finite checker compares all coefficients of the paired Hermitian kernel,
top reduction, all nine cyclic Fourier rows, anchored cube linear part,
four Newton identities and four entire literal actual original-root weight
identities. It computes all nonnegative scalar majorants over the WHOLE
interval with exact rational arithmetic. It checks a complete typed fixture
and pins its own entire source bytes. This is same-author corroboration;
analytic convergence, positivity and norm arguments remain written proof
inputs. Literal kernel fixtures are not all collar/low-sublevel examples.

Tested with CPython3.12.14; Python standard library only. From this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
  python3 verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
  python3 -O verify.py
python3 validate.py
```

Expected: `PASS`,35 complete controls,20 strict margins,12 mathematical
damages. Complete typed whole-record SHA256:
`325cc84813fd97995b97d05d855899b26b5af4f637f221e6a6c8767b7a0933cc`.
Normal and optimized records match. `validate.py` serially checks20 malformed
fixture rejections and two copied-source-pin rejections with explicit failure
reasons; native threads one, child timeout45seconds, no resource escalation.
It writes a compact timing/resource summary to VALIDATION.json and removes
its contribution-local temporary fixtures. Resource values are observations,
not portable mathematical premises. [EXPECTED.json](EXPECTED.json) and
[VALIDATION.json](VALIDATION.json) preserve the small fixed evidence.
[MANIFEST.json](MANIFEST.json) gives a complete public file census.

No imported executable, independent review seal or formal checker is claimed.
Published source alone does not establish correctness or historical priority.
