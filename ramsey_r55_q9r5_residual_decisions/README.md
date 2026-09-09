# Complete q9,r5 residual test: 362 SAT, zero task exclusions

**The predeclared whole-task exclusion gate failed.** Every one of the 362
original `bo1-q9-r5-c000000` through `bo1-q9-r5-c000361` tasks has a
feasible forced 23-vertex residual. The certificates in [LEDGER.tsv](LEDGER.tsv)
prove that this complete residual test alone removes **zero** task IDs.
All 362 physical 43-vertex tasks remain UNKNOWN. No good43 was found.

Each residual contains four specified blue K4 blocks and its specified
seven-vertex Ramsey(4,4) core. It has no red K4 and no blue K5. The test uses
all 208 unfixed physical edges and all relevant four- and five-subsets;
there is no added symmetry breaking. It combines the existing necessary
restrictions wholly inside this residual, including all multi-block
interactions. Constraints involving the first twenty physical vertices
are absent. See [PROOF.md](PROOF.md) for the exact implication and encoding.

This is a complete negative test of the proposed exclusion method, not a
new carrier percentage, a full-task SAT result, or a candidate construction.
The original global registry still has 2,188,660 undecided whole task IDs
after the separate 518 q7,r5 exclusions. The teammate's 161 q10 children
were not accessed. No larger cap, alternate solver, adjacent residual
filter, or extension run follows this failed gate.

## Evidence

The single four-worker run used Cadical300 through python-sat 1.9.dev15,
with a cap of 200,000 conflicts and 30 seconds per invocation. All 362
cases returned SAT, none reached a limit, and no search UNSAT proof was
produced. The batch took 139.781 seconds including generation and witness
checks. [RUN_SUMMARY.json](RUN_SUMMARY.json) preserves exact receipts;
[GATE.json](GATE.json) preserves the declaration before computation.

Every witness is independently checked in Python and C++, including a
full ASan/UBSan witness run. Each Python mode checks 3,205,510 four-subsets
and 12,180,938 five-subsets. A reverse physical-clause audit checks all
362 formulas and all 9,603,776 clauses. Sanitizer formula coverage is
representative (indices 0, 181, 361); the release audit covers every formula.
Seven formula corruptions and six witness/registry corruptions are rejected.
The latter are rejected by both Python modes and the sanitized C++ checker.

Ledger SHA256:

    b468fd4f3c24a955d84fcc9ad36f15bbdac70be33e175a7d153a0ca3884bfd60

The complete certificate table is compact; raw CNFs, binaries, and logs
remain outside Git. All witness checks are independent of the solver.
Catalogue isomorphism completeness and the inherited original task cover
remain external assumptions. No new independent peer review is claimed.

## Reproduce without a solver

Python 3.11.2 standard library and g++ 12.2.0 suffice. From the repository
root, choose a new scratch output directory:

```sh
python3 -B ramsey_r55_q9r5_residual_decisions/reproduce.py \
  --data /tmp/q9r5-data/r44_7.g6 --fetch \
  --out /tmp/q9r5-residual-replay
```

This downloads only the pinned 2,172-byte core catalogue if missing,
checks all certificates in normal and optimized Python, regenerates and
hash-checks every formula, runs the independent native audit, and runs
the sanitizer and negative controls. It refuses an existing output path.
The deterministic result must equal [EXPECTED.json](EXPECTED.json).
No parent computation or solver is invoked by this replay.

For a shorter certificate-only check:

```sh
python3 -B ramsey_r55_q9r5_residual_decisions/verify.py \
  --data /tmp/q9r5-data/r44_7.g6
```

This directly checks all 362 graph certificates and their original task
identities. It checks the format of formula metadata; the full replay
additionally regenerates and verifies formula hashes and clause counts.

## Original bounded computation

`run.py` and `solve_one.py` preserve the exact discovery procedure. They
are not needed to verify the result. To reproduce the solver experiment
in a separate Python environment with `python-sat==1.9.dev15` installed:

```sh
/path/to/pysat-python -B ramsey_r55_q9r5_residual_decisions/run.py \
  --data /tmp/q9r5-data/r44_7.g6 --out /tmp/q9r5-new-bounded-run \
  --drat /path/to/drat-trim
```

Each case is invoked once. Completed receipts are retained on restart;
an interrupted case is not retried. Any possible UNSAT result would need
independent DRAT verification before changing a whole-task status.
Timing and chosen SAT witnesses may vary across machines; the published
literal certificates, rather than solver reproducibility, establish the
reported feasible residuals. Tool versions and binary hashes are recorded
in [TOOLS.json](TOOLS.json).

The source and relation context are recorded in [CONTEXT.json](CONTEXT.json).
The accepted h4059/h4069/h4081 structural base is preserved. The new h4087
independent ACCEPT concerns h4081 only and does not review this experiment.
