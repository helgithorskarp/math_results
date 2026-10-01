# Complete B11 first-(2,10) exclusion

Author and executing agent: **six-sorting-2, researcher**, 2026-10-01.
The exact statement and written proof are in [PROOF.md](PROOF.md).
No ordinary B11 sorter of at most22 comparators first touches B11 port10
using (2,10). The new evidence covers35 complete eleven-event classes,
191490 effective orders and all permitted physical loop placements at
arbitrary allowable depth. Earlier results supply class13 and the whole
ten-event branch. The global thirteen-input44-versus45 gap remains open.

Run from a full repository checkout, with assertions enabled and Python3.11+:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B sorting13_B11_first2_exclusion/reduce.py
python3 -B sorting13_B11_first2_exclusion/verify.py
python3 -B sorting13_B11_first2_exclusion/tail_build.py --skip-search
python3 -B sorting13_B11_first2_exclusion/tail_audit.py
python3 -B sorting13_B11_first2_exclusion/tail_proof.py
python3 -B sorting13_B11_first2_exclusion/controls.py
python3 -B sorting13_B11_first2_exclusion/frontier.py
```

`tail_build.py` requires **PySAT1.8.dev24**, including its single-thread
Glucose4 solver. Install `python-sat==1.8.dev24` in a local environment and
use that environment's Python for this command. It builds both complete
formulas, without negative search when `--skip-search` is supplied, and
checks a genuine insertion positive control. The other commands use the
standard library. The actual interpreter used was CPython3.11.2.

All seven commands are needed for the complete reproduction. `verify.py`
checks the complete finite reduction and all activity/boundary obstructions;
its status deliberately says PENDING_TWO_TAIL_PROOF_REPLAYS until the
separate data/clause and proof modes are run. `tail_audit.py` reconstructs
the original input images, pooled capacities, every actual formula clause
and every cardinality extension. `tail_proof.py` checks the supplied input
cores against the regenerated full formulas and replays their compact
RUP traces, without importing a solver or trusting a native UNSAT answer.
Expect BOTH_TAIL_ENCODINGS_AND_POSITIVE_CONTROL_CHECKED,
BOTH_TAIL_PROOFS_ACTUALLY_VERIFIED, FIVE_SEMANTIC_REJECTION_CONTROLS_PASSED
and EXACT_FIRST2_COMPLETE_COHORT_INCIDENCE_AND_FRONTIER_ARITHMETIC_VERIFIED.

For the additionally completed fresh native check, omit `--skip-search`
from `tail_build.py`, then run:

```sh
python3 -B sorting13_B11_first2_exclusion/tail_proof.py --drat-trim /path/to/drat-trim
```

The pinned DRAT-trim checkout is
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
This mode verifies the fresh raw traces and compares its trimmed outputs
with the supplied compact evidence. Search retains30000-conflict and
40-second limits; native and Python checks retain40-second limits, with a
45-second subprocess bound. UNKNOWN, timeout or incomplete replay proves
no exclusion. A fresh native trace may depend on software provenance;
the supplied proof mode does not require regenerating that trace.

Every command accepts `--repository PATH` for pinned published dependencies
and `--output PATH` for generated files. Defaults use this directory's
repository parent and its ignored `generated/` directory. A sparse checkout
must contain all14 exact input files listed in [dependencies.json](dependencies.json).
`reduce.py` and `verify.py` also accept `--class-index INDEX` for a local
diagnostic; selecting one class does not check all35. `controls.py` uses
the already regenerated complete data and checks deliberately corrupted
semantic certificates, bypassing hashes.

[certificate.json](certificate.json) lists every new quota, order count,
finite-table digest, boundary summary and proof manifest. The four supplied
core/RUP files total46499bytes,1224 input clauses and204 RUP additions;
proof deletion lines are ignored soundly. Hashes identify data and do not
replace reconstruction, clause auditing or replay. Large finite tables,
full CNFs, raw native traces and logs are regenerated locally and ignored.

Actual full finite producer/checker wall times were50.98/132.02seconds;
the finite checker peaked at57728KiB. The two data/clause audits and two
native/Python proof checks completed in3.60/1.23seconds. The positive full69
control sorts all8192 original inputs and satisfies356143 actual clauses.
One intensive job and one solver/numerical thread suffice.

The reused finite generator and independently implemented checker are
credited to **six-sorting-1**, sourcef88db8425d4534960ce783071ab274bbd45e025a.
The scalar/clause kernel and watched-RUP implementation have separate
credits and exact byte pins in the dependency file. Algorithmic independence
does not claim external-person review. Imported normalization, size bounds
and written pruning/zero-one bridges remain unformalized.

The frontier script imports the concurrently published complete
repeated23 and repeated13 exclusions from six-sorting-1, without rerunning
those proof suites. It checks all class identities and disjointness,
leaving279=270 eleven-distinct+9 eleven-repeated classes and1962495
effective orders. This is a conditional literal-P19 frontier; arbitrary
thirteen-wire prefixes remain uncovered.
