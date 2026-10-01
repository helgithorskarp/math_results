# A depth-free size 12 exclusion for one B11 nine-wire image

Author and executing agent: **six-sorting-2, researcher**. All campaign
signatures share one identity; this attribution identifies the actual worker.

No ordinary nine-wire comparator network with at most 12 gates sorts the 61-row
image associated with ten-event class
`410718871845198803939197429219333`, image 56 of the pinned parent certificate.
All 36 ordinary comparator pairs and all serialized orders are covered. This
excludes one additional ten-event B11 C22 class: **416 necessary classes
remain** (89 ten-distinct,297 eleven-distinct,30 eleven-repeated).

The [proof and complete coverage argument](PROOF.md) use the full thirteen-wire
completion bridge, passage caps, twelve mandatory clamped activity domains,
and the established End Game theorem. The End Game theorem and known small
sorting-network bounds are literature imports, not new results here. The
eleven-event branch is unchanged. GlobalS13 remains 44..45, and arbitrary other
thirteen-wire prefixes are not covered. No 13-gate witness is established.

The CNF has 11598 variables and 125802 clauses. Glucose 4 produced an UNSAT
certificate; both native DRAT and a separate Python RUP implementation actually
verified it. A solver-independent audit reconstructs every non-cardinality
clause and exhaustively checks auxiliary-variable coverage for the cardinality
blocks. Original-input and clamped-domain data are checked by scalar replay.
This is algorithmic independence, not an external reviewer verdict or a
proof-assistant formalization.

The [compact certificate record](certificate.json) gives the exact CNF and
proof hashes and checked counts. The 3.84 MB raw and 2.36 MB trimmed generated
proofs are omitted under the human restriction on publishing large generated
certificates. The following commands regenerate those exact certificates into
an ignored local directory and independently check them. No private input or
private proof file is required to reproduce the result.

Use Python 3.11 and the pinned `python-sat==1.8.dev24`. Glucose 4 is single-threaded;
keep every other numerical library at one thread. Install into a local
environment, then run one CPU job at a time:

```sh
python3 -m venv /tmp/sorting13-proof-env
/tmp/sorting13-proof-env/bin/pip install python-sat==1.8.dev24
git clone https://github.com/marijnheule/drat-trim /tmp/sorting13-drat-trim
git -C /tmp/sorting13-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/sorting13-drat-trim -j1
cd sorting13_B11_image61_depth_free_exclusion
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
/tmp/sorting13-proof-env/bin/python -B build.py
python3 -B audit_data.py generated/target12.cnf
python3 -B audit_encoding.py generated/target12.cnf
python3 -B controls.py generated/target12.cnf
python3 -B check_proof.py generated/target12.cnf --drat-trim /tmp/sorting13-drat-trim/drat-trim
```

Expected final statuses are
`EVERY_CLAUSE_AND_AUXILIARY_COVERAGE_INDEPENDENTLY_AUDITED`,
`NATIVE_DRAT_VERIFIED`, and
`PYTHON_RUP_CORE_AND_FULL_MEMBERSHIP_VERIFIED`, with 26257 core clauses and 7390
RUP additions. The pinned run takes approximately 25 seconds total and below
100 MiB. Each solver/checker call has fixed operational limits. UNKNOWN,
timeout, missing proof, unexpected hashes, or a failed audit establishes no
exclusion; do not increase resource settings as a substitute for completion.

The real positive control is a 36-gate insertion sorter of all nine-wire inputs;
with the 32-gate prefix it sorts every one of 8192 original thirteen-bit inputs
and satisfies 385050 CNF clauses. Generated CNFs, metadata, cores, traces and
native logs stay in `generated/`; only compact source and evidence are tracked.
See [dependencies.json](dependencies.json) for pinned parent files, mathematical
imports, software versions, and explicit credit to six-sorting-1's Python RUP
checker.
