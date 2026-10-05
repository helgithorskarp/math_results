# Independent all-count block audit

Agent six-reviewer-5 / independent mathematical reviewer. Source publication
and actual graph commitment are verified separately. The
all-count scoped verdict and proved small-pool / exact-window refinements
are in [REVIEW.md](REVIEW.md); the self-contained ordinary proof is in
[PROOF.md](PROOF.md). Numerical q19 attainment is not audited here.

CPython 3.12.14 standard library only. The checker uses arbitrary-precision
integers, Fraction and a tested-prime modular determinant. No author
certificate, table, program or external math package is an input.

Run from this directory with one thread per native library:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -B validate.py
```

For publication integrity without repeating mathematics, run
`python3 -B publish_check.py`. EDITORIAL.json records the exact reversible
publication edits; the mathematical checker, validator, proof and complete
record are byte-identical to the private seal.

The mathematical validator checks all primary sealed bytes before executing the checker.
It then checks the ENTIRE RECORD.json in normal and optimized modes,
and requires six distinct live semantic damages to fail in each mode.
Its mathematical children are serial and each has a fixed 45-second
guard. An interruption, timeout, failure or resource limit is not a
nonexistence result. The test-count cases do not prove all-count or
continuous-real statements; the ordinary proof does that.

For a raw fresh deterministic record run `python3 -B check.py` without
arguments. A single declared damage argument deliberately exercises a
rejection gate. An unknown mode is an error. RECORD.json is generated
by this independent checker and is not an author EXPECTED-file input.
