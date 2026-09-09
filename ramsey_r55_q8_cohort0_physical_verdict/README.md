# First physical solver gate on q8,r8 cohort 0

This package exercises the existing positive cohort 0 from h4149/h4161,
covering 2,184 original task IDs. It splits the complete physical43 input
into four exhaustive sign choices on edges {0,41} and {1,37}. The exact
decomposition, proof admission, imported-premise boundary and stopping rule
are in [PROTOCOL.md](PROTOCOL.md).

**Measured outcome: UNKNOWN on all four leaves.** They used 400,008 conflicts
and 245.8481 seconds of solver wall time in total. There were zero certified
leaf closures, zero original-task exclusions, and zero candidates. All 2,184
original members remain UNKNOWN. VERDICT.json records every call and input
hash. The prior global administrative counts remain 518 exclusions and
2,188,660 UNKNOWN original task IDs.

The solver/proof interface was tested before the four target calls, and the
mixed-premise admission control passed with zero catalog matches. Those
controls do not establish target feasibility or infeasibility. The largest
per-call peak RSS was 408,752 KiB. All partial target DRAT traces are retained
as unfinished artifacts and were not presented as UNSAT certificates.
The completed gate is parked without a retry, deeper split, changed budget,
alternative backend, or neighboring cohort. No good43 was established.

The source uses Python3.11 standard libraries on Linux, the pinned CaDiCaL
sc2021 executable, and the pinned drat-trim checker in DEPENDENCIES.json.
The parent h4149 and h4161 source directories must match their full manifests.
The solver's `--plain` setting disables internal preprocessing; only
independently checked RUP proofs are imported. Binary hashes are verified
before solver calls. No q10 input is consumed.

## Reproduction

From the repository root, let PARENT_INPUTS be an h4149 run directory with
the exact q8-r8.cnf and cores.u64le files. UNIT_CERT is h4161's public
branch-certificate.json. POSITIVE_INPUT is the h4161 frozen/reproduced
positive-000.cnf input, SHA-256
326d54a4a9b2abb26c5865536c7bb42d20696c5a59c6c8e1a0d1477465f21c67.
The h4149/h4161 READMEs document regeneration of those prerequisites.
Use fresh scratch directories outside the repository:

```sh
python3 -O -B ramsey_r55_q8_cohort0_physical_verdict/gate.py controls \
  PARENT_INPUTS UNIT_CERT /tmp/r55-q8-verdict-controls
python3 -O -B ramsey_r55_q8_cohort0_physical_verdict/gate.py prepare \
  PARENT_INPUTS POSITIVE_INPUT /tmp/r55-q8-verdict
python3 -O -B ramsey_r55_q8_cohort0_physical_verdict/audit.py \
  PARENT_INPUTS POSITIVE_INPUT /tmp/r55-q8-verdict /tmp/r55-q8-verdict-controls
python3 -O -B ramsey_r55_q8_cohort0_physical_verdict/gate.py execute \
  PARENT_INPUTS UNIT_CERT /tmp/r55-q8-verdict --controls /tmp/r55-q8-verdict-controls
```

The last command makes the four budgeted target calls. Do not use it to
restart a partially executed gate: execution and leaf STARTED markers cause
it to refuse duplicate work. Reconcile any existing writer and receipts
first. The declared budget is fixed for this experiment; reproducing its
setup does not authorize a larger or adjacent search campaign.

The four target CNFs total 273,571,364 bytes. Full formulas, logs, binary
proof traces and scratch checkpoints are kept outside Git. Public artifacts
contain source, exact input hashes, compact controls and the measured verdict.
No target UNSAT claim may be made from an UNKNOWN call's partial trace.
