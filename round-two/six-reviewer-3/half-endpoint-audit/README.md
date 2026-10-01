# Independent half-endpoint audit

Actual reviewer **six-reviewer-3**, independent mathematical reviewer.
[REVIEW.md](REVIEW.md) confirms Sendov claim9033 in its explicit inherited
boundary-minimum scope, independently reconstructs its negative first curvature,
and proves two refinements: the half-bound fails in every positive excess budget,
and the five-dimensional centered-real Hessian sector has first correction
\(\ell=-4441/540+(7046/135)c-(2288/45)c^2<0\).

The budget can be super-polynomial or discontinuous. A matching finite-radius
lower stability constant, an effective collar and the full first-power
conjecture remain unresolved. Analytic arguments are ordinary written proofs,
not formal kernel checks.

Python 3.11+ standard library only; audited with CPython3.12.14. From repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B round-two/six-reviewer-3/half-endpoint-audit/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B -O round-two/six-reviewer-3/half-endpoint-audit/audit.py
```

Both must print:

```text
PASS 137 exact checks; 13 damages rejected; full-record SHA256 71f9e789fbe8e99a5e11277bf38d7b9a14927e76aa09fe5899b66f5a71e93c0c
```

[exact.py](exact.py) uses extended polynomial Euclid and flat sparse jets.
[audit.py](audit.py) uses a rational unit-circle parametrization and literal
critical factors. Neither imports researcher code. [EXPECTED.json](EXPECTED.json)
contains the complete independent record; checking uses explicit exceptions
and canonical JSON, including types, in normal and optimized Python.

To fetch hash-bound original source and five inherited prose inputs and perform
both original/independent normal and optimized replays with all nine complete
mathematical fields compared:

```bash
python3 -I -B round-two/six-reviewer-3/half-endpoint-audit/replay.py
```

This requires network access to public GitHub source, writes only a temporary
directory, and uses one sequential mathematical process with a fixed20-second
guard per run. Add `--fixture-damages` to repeat missing/malformed/altered external
fixture controls in both modes. These controls already completed in the recorded
validation. The original checker must pass70 checks/eight damages and full-record
SHA256 `f91b1d9c36f2475cecfdb7053afd8357381fd1bbbbb47a01208345c9443d4ddd`.

[INPUTS.json](INPUTS.json) binds all15 public input files to commits/hashes;
[VALIDATION.json](VALIDATION.json) records completed runs and full field comparisons.
[SHA256SUMS](SHA256SUMS) binds the public package apart from itself. Finite algebra
checks do not establish global competitor coverage or analytic remainder bounds;
those are explicitly separated in the complete review.
