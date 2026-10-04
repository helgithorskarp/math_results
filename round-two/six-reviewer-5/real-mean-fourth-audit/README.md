# Independent balanced real-mean audit

**six-reviewer-5 / independent mathematical reviewer.** This source
independently audits the complete new LEMMA10280 explicit degree-nine
construction and its coupled real repair class. It proves sharp
square-root mean-gap and linear repair stability in that class.
[REVIEW.md](REVIEW.md) states the verdict, exact limits and provenance;
[PROOF.md](PROOF.md) gives all constants, reductions and ordinary analytic
bridges. The proof remains unformalized. Universal fourth optimality and
global reciprocal FIRST are not proved.

## Reproduction

Standard-library Python only. Tested interpreters and actual run details
are recorded in [VALIDATION.json](VALIDATION.json). Six complete positive
replays and30 intended rejections passed; each retained a fixed45-second
guard, serial children and one native thread. From any full or
relocated source-only copy, with no parent executable or fixture:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
python3 -I -B verify.py

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
python3 -I -B -O verify.py
```

Expected: `complete=true`, `whole_rows=21`, eighteen whole original
root/normal jets, canonical record 66066 bytes, SHA256
`bfc97c056ed8c23ca6809ae96146426c996b427853611d5bcb31071d1018347d`.
Every source file is sealed before mathematical imports. The entire
freshly regenerated record is compared with [FRESH-BASE.json](FRESH-BASE.json),
including all field coordinates and symbolic coefficients. A hash or
aggregate count does not replace those proof checks.

The complete validation suite uses serial children and a fixed
45-second guard; give it a fresh directory outside the source:

```sh
python3 -I -B validate.py --scratch /tmp/mean-audit-new \
  --summary /tmp/mean-audit-summary.json
```

An optional `--second-python /path/to/python` performs two further complete
interpreter replays. `--record /tmp/record.json` on verify saves the whole
regenerated record outside the source. No generated corpus is required.
Timeout or interruption is incomplete verification, never a negative
mathematical result.

## Files and boundaries

[algebra.py](algebra.py) and [signs.py](signs.py) openly adapt our own
10246 cyclotomic/jet and rational sign framework. [audit.py](audit.py)
reconstructs the mean family, complete original/scalar jets, both actual
normal columns, dual and cone. [derive.py](derive.py) builds the whole
21-row record. [verify.py](verify.py) checks source closure, strict types
and every field; [validate.py](validate.py) exercises mathematical,
whole-fixture and preimport-source defects under normal and optimized
modes. All current author code, EXPECTED and validation were excluded.

[DEPENDENCIES.json](DEPENDENCIES.json) and
[PROVENANCE.json](PROVENANCE.json) identify written inputs and explicit
prior reuse. There is no external runtime mathematical input. Compactness,
IFT, collar, remainder and little-o decoding arguments are ordinary
mathematics, not a formal certificate. The other reviewer's concurrent
fifth-order derivative remains a separate scope; our private control was
preserved without a duplicate derivative publication.
