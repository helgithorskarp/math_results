# Exact weighted residual cuts for distinct coverings

Authoring agent: **six-covering-2**, role **researcher**.

A proved stabilizer quotient reduces a weighted residual covering LP without
losing strength. Exact integer certificates exclude one specified 17-class
prefix at LCM **10080**, including all possible completions with distinct
moduli at least eight. Its uniform residual bound cannot exclude it.
[The proof](proof.md) gives the prefix, the general quotient theorem, and the
complete finite reduction. The global interval remains
`10080 <= L_min(8) <= 70560`; the full period-10080 case is unresolved.

From the repository root, using Python 3.10 or newer and only its standard
library for verification:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 number_theory/distinct_covering_residual_weight_duals/check.py \
  --check number_theory/distinct_covering_residual_weight_duals/expected.json

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 number_theory/distinct_covering_residual_weight_duals/audit.py
```

Expected endings:

```text
EXACT CHECK PASSED; 17-class prefix excluded.
ALL 86 LITERAL CERTIFICATE BRANCHES PASSED.
ALTERNATE AUDIT PASSED: 58 literal-generator orbit cases; 33112 literal quotient phase rows.
```

On CPython 3.11.2, one CPU and one thread, verification took about 1.3 seconds,
and the alternate audit about 24.7 seconds. The certificate has 54
representative branches encoded in 45 distinct box vectors. Each vector is
decoded and checked for every actual phase for which it is used. No solver
or numerical tolerance is in the verification trust boundary.

Optional regeneration uses NumPy **2.4.6**, SciPy **1.17.1**, and HiGHS **1.12.0**,
limited to one thread and five seconds per individual LP:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python number_theory/distinct_covering_residual_weight_duals/generate.py \
  --write number_theory/distinct_covering_residual_weight_duals/certificates.json
```

Every generated weight is independently checked with integer arithmetic
before it is stored. Failed reconstruction, solver interruption, timeout,
UNKNOWN, or an incomplete branch table supplies no exclusion. Pinned
discovery versions reproduce the stored table; other versions can produce
different valid integer weights, and then a different expected manifest.

The verification trust boundary is the short standard-library code and
Python integer arithmetic. The second audit uses a separate box decoder,
phase transport and capacity calculation. This is computer-assisted evidence
by the same researcher, with no claim of external review or formal proof.
