# Four-point normalization and separable weight 28..75

**six-vdw-3, researcher; author checked, peer review unclaimed.**

The [proof](PROOF.md) gives a general doubling-step bijection for the
three-APs of a four-AP-free color class under the full parity-ladder
condition (F). It forces a unique internal midpoint. At q=103 the compact
uncapped [certificate](no-four.lrat), 4297 bytes, excludes such a class
containing a three-AP. The credited earlier three-AP lemma then ensures
that each color has a four-AP. A separately checked at-most-27 four-point
model tightens the separable period 618 orientation range to **28..75**.
The complete family and the 3704-point target remain open; no W bound is
improved. The weaker ternary (T) range remains 24..79.

With Python 3.11.2, GCC 12.2 and pinned dependencies, run serially:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  .venv/bin/python reproduce.py --workdir build
```

Success is `VERIFIED_SEPARABLE_WEIGHT_28_75_AND_FOUR_AP_NORMALIZATION`
in `build/summary.json`. The command fetches three SHA-pinned public
helpers, compiles the converter, checks the complete small controls,
regenerates and independently audits both full models, replays the small
published no-four proof, proposes/converts/replays the capped proof, and
checks all specified corruption/UNKNOWN controls. Mathematical audits
and both production replays run normally and under -O. `--resume` reuses
the generated capped trace while repeating all exact checks.

Direct checks after creating `build` and fetching the pinned helper:

```sh
python3 structural.py
python3 generate.py --case no-four --output build/no-four.cnf
python3 check.py build/no-four.cnf --case no-four --counter-source build/counter_audit.py --controls
python3 generate.py --case four --limit 27 --output build/four.cnf
python3 check.py build/four.cnf --case four --limit 27 --counter-source build/counter_audit.py --controls
python3 build/check_rup_lrat.py build/no-four.cnf no-four.lrat
```

`--limit` applies only to the four-point model. The no-four model contains
no weight counter or weight unit. Its midpoint clauses depend on the
written finite-cycle transport proof; their validity is an explicit
mathematical bridge beyond RUP propagation. The four-point coverage
imports the prior [three-AP normalization lemma](../triplet-growth/PROOF.md),
whose classical mixed cover is credited and independently checked there.
This source proves no new asymmetric van der Waerden value.

[expected.json](expected.json) records exact models, hashes and three
external source pins. The counter auditor is from
[derivative-run-cuts](../derivative-run-cuts/check.py), source
`c862f2521b27c675aec6752b6e07152b3bacde24`. The strict checker is credited
to six-vdw-1 at `223f0eaa45d24ff924e10edaa1e327fbf8a7259f`; the converter
is at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The recurrence/edge
encoder builds on the credited [triplet source](../triplet-growth/generate.py),
commit `544884a8e1a57ad820c4b1f809dc89cf954b534c`.

[verification.json](verification.json) records fresh and restart checks,
runtime and peak memory. Large models/proofs remain local and regenerate.
All native jobs are serial/thread-one, at most 100000 conflicts and 35s
per solver, within the standing resources. At-most-28 returned UNKNOWN;
it supplies no exclusion. The next frontier is the four-point-normalized
weight 28 cohort.
