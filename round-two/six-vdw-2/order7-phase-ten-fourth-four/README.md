# Exact-ten H7 fourth-selection and whole-run restriction

six-vdw-2, researcher. Read [PROOF.md](PROOF.md) for all quantifiers, complete
coverage, ordinary bridges and limitations. This author-checked scoped
result leaves the3704 witness and whole exact-ten family open.

Clone the public repository so all SOURCE_PINS.json relative dependencies
are present. Python3.11.2, PySAT1.8.dev24/six1.17.0 and CaDiCaL195 were used
for the original bounded proof proposals. The strict checker and phase
consequence verifier use exact Python integers. Build the pinned drat-trim
source as specified by the geometric-cut companion README; keep native
threads one. From this directory, using the actual un-resolved solver venv:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /path/to/solver-env/bin/python reproduce.py --work /tmp/h7-fourth4 --converter /path/to/drat-trim
/path/to/solver-env/bin/python guards.py --work /tmp/h7-fourth4 --output /tmp/h7-fourth4-guards
python3 phase_consequences.py
python3 -O phase_consequences.py
```

Work/output directories must be fresh. Native proposal caps are unchanged;
incomplete stages prove no exclusion and are never automatically retried.
A reader with candidate CNF/LRAT files can supply --certificate-cache DIR,
using head/<stem>.cnf and head/<stem>.lrat. Candidates are untrusted and must
match full generated input bytes, then pass all strict proof checks. The
publication run used this path without new native search after the private
UNKNOWN. Explicit --resume only replays already checked positive proofs;
it refuses identical bounded failures.

Both Python modes check the complete literal field definitions, counter,
all44 TWO clauses, six omitted-parent inclusions, new complete12 failure
cover, all proof steps and whole PHASE_EXPECTED.json. SHA256SUMS and
SOURCE_PINS.json check entire source bytes before helper execution; digests
identify data and do not replace mathematical checks. EXPECTED.csv is a
compact reproducibility fixture, not a proof corpus. Full generated proofs,
CNFs, logs, binaries and private signed receipts remain outside Git.

Trust includes exact Python arithmetic/runtime and the published source,
plus the ordinary proof of parent premises, transport, coverage, counter
semantics and run consequences. Independent algorithms by the same author
are not external-person review or proof-assistant formalization. The next
length-six ten-head reduction is a plan, not a computed exclusion.
