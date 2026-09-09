# Complete q8 work through shared assumptions and checked proof joins

This package decomposes the complete 2185424-task q8 registry into **956
pending physical43 cohort jobs**, backed by four shared full formulas.
Each cohort contains 1953--4095 original task IDs. A verified cohort
refutation would close all matching IDs, and complementary physical edge
branches have an executable proof-join interface.

**No original task was excluded and no candidate was found.** All original
q8 tasks remain UNKNOWN. The work-unit count is a decomposition, not a
search-space reduction or measured target-solver speedup. No target solver
was run. Team-r55-1's q10 children and all parked families are untouched.

The [proof](PROOF.md) establishes exact taskwise projection, a partition of
all core assignments, guarded RUP transport and physical branch joins.
[HANDOFF.md](HANDOFF.md) specifies the worker contract and its operational
gate. [EXPECTED.json](EXPECTED.json) pins the four formulas, entire queue
stream and complete cohort partition.

## Solver-free reproduction

Python 3.11.2, g++ 12.2.0, standard libraries only. Start at the repository
root. The pinned h3887 and prerequisite source packages must be present;
their full manifests are checked by the projection comparison.

Use fresh scratch paths outside the checkout. Only the pinned eleven-vertex
Ramsey(4,4) catalog is needed; `--download` obtains and verifies it if absent.

```sh
python3 -O -B ramsey_r55_q8_assumption_queue/reproduce.py \
  /tmp/r55-q8-catalog /tmp/r55-q8-replay --download --sanitizers
```

The replay regenerates four complete bases, dispatches and independently
checks all original task records, constructs and verifies all cohorts,
compares four full projected formulas with the unchanged h3887 encoder,
checks the certificate protocol, and materializes one real complete worker
input. Outputs include REPLAY.json and detailed compact receipts. Existing
output directories are refused. CNFs, binary streams and build products
remain in scratch. This is validation computation, not a target solve.

The catalog contributes 6556272 bytes. The four bases total 269380717 bytes;
the shared core stream is 4370860 bytes, and the complete dispatch stream
is 28410524 bytes. The compact cohort tree is 45306 bytes. The checked sample
worker adds about 66 MB. A persistent SAT worker may need substantially more
memory, and its runtime is not established by this replay.

## Exact interfaces

After reproduction, replace `/tmp/r55-q8-replay` with the output directory:

```sh
python3 -B ramsey_r55_q8_assumption_queue/task_queue.py request \
  bo1-q8-r5-c000000 /tmp/r55-q8-replay
python3 -B ramsey_r55_q8_assumption_queue/cohorts.py \
  /tmp/r55-q8-replay --r 5 --leaf 0
```

The latter returns a worker job with `r`, `core_assumptions` and `edge_cube`.
Save such a job to JSON and use `worker.py materialize` to produce its exact
full43 formula. `worker.py import-lrat`, `join`, `cover` and `target` validate
the proof/model path. The admission routine accepts a cover certificate
with `task_queue.py request ... --certificate FILE`; a task is suppressed
only after full certificate verification.

This implementation accepts positive-hint RUP certificates, including the
RUP subset of LRAT. It rejects RAT-only additions. A solver adapter must
preserve the exact input and clause IDs and supply a supported checked proof.
No performance or adapter compatibility beyond the tested format is claimed.

The four full-base proof controls cover an impossible core pattern absent
from the actual catalog. They therefore verify with an empty task cover.
Their purpose is to test the protocol; they are not new Ramsey exclusions.
The author checks do not substitute for independent review.
