# Complete one-double angular exclusion

Actual **six-sendov-2 / researcher**, 2026-10-04.
For every normalized real eight-vector with first, third and fifth moments
zero, fourth excess (D>0), exactly one original double, and six other
simple originals, the full grouped-mass ratio is **(C<47/2)**.
[PROOF.md](PROOF.md) supplies the ordinary original-root argument and exact
scope. The two new positive-(q_0) caps close the previous remaining fiber;
the real-(q_0) and central cases are credited published inputs.

Status: complete ordinary proof with finite exact certificates, unformalized
and independently unreviewed. No stationary premise. Other multiplicities,
the global angular bound and full complex FIRST endpoint are not resolved
by this contribution.

## Reproduce

Python 3.12.14 and SymPy 1.14.0 were used. The native engine is standard
library only; the CAS engine requires that exact SymPy version. Set all six
native thread controls to one:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
```

From the repository root, run serially, placing complete records outside
the contribution directory:

```bash
python3 -I -B round-two/six-sendov-2/complete-one-double-exclusion/verify.py \
  --expected round-two/six-sendov-2/complete-one-double-exclusion/EXPECTED.json \
  --whole /tmp/one-double-native.json
python3 -I -B round-two/six-sendov-2/complete-one-double-exclusion/compare_cas.py \
  --expected round-two/six-sendov-2/complete-one-double-exclusion/EXPECTED.json \
  --check /tmp/one-double-native.json --whole /tmp/one-double-cas.json
```

The scripts derive the full original octic/sextic/critical quartic,
moments, both full Bezout matrices, all determinant coefficients, the two
new rational caps and all 3,706 exact Bernstein controls. They compare every
coefficient before using compact output as agreement evidence. All
denominators/factor signs and the actual original-root coverage are paid in
the written proof; a formal polynomial box is not an existence certificate.

The 1,501,910-byte canonical mathematical record has SHA256
`a40535cb3e306325983a410f3d988d7201649262387d2a7540f0753cdd70800f`.
It is deliberately omitted from the public source. Each compact engine
regenerates it without ancestor coefficient maps or peer programs.
`EXPECTED.json` is read only after the complete mathematical calculation.

The complete portable validation suite is:

```bash
python3 -I -B round-two/six-sendov-2/complete-one-double-exclusion/validate.py \
  --scratch /tmp/one-double-validation
```

If SymPy is installed in a separate site directory, the validation runner
accepts `--sympy-root /path/to/site-packages` and uses an isolated `runpy`
bootstrap. No campaign files or private mathematical record are required.
Each child is serial, has six native thread settings one, and a fixed
45-second guard. Four complete normal/optimized local/cold records agree;
all eight deliberate source/partition damages reject as intended.
Maximum validation child: 9.938092 seconds; peak child RSS: 70,632 KiB.
No resource limit was increased or hit. Failed/interrupted checks are
incomplete validation, never mathematical nonexistence.

The new defining input [PARTITION.json](PARTITION.json) contains ten small
quartic rectangles; exact cell coverage verifies that their union is the
whole closed root rectangle. The two angular tensors have degrees
(31,8,5), 1,728 controls each, on the licensed positive and negative strips.
The native arithmetic uses integer Berkowitz plus binomial expansion; the
CAS arithmetic uses exact rings plus a subset determinant and direct
composition. Same-author algorithm checks do not constitute independent
review or formal proof.

[DEPENDENCIES.json](DEPENDENCIES.json), [LITERATURE.md](LITERATURE.md) and
[VALIDATION.json](VALIDATION.json) record provenance, mathematical scopes
and compact evidence. Only compact source and evidence are published.
