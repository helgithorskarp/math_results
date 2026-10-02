# Exact-ten phase selections after two backgrounds

six-vdw-2, researcher. In the H7/F617 seven-AP-free field model, every
selected run-start pair at exact selected phase count ten, followed by two
backgrounds, has selection 4 and at least one of selections 5 or 6. Both
selected values and every cyclic start are covered. [PROOF.md](PROOF.md)
gives the full hypotheses and complete twelve-case reduction. The third
selection bound remains four; phase endpoints and [1,3704] remain open.

Use a checkout containing the sibling sources. Nineteen helper/premise files
in `SOURCE_PINS.json` are checked before mathematical imports. No campaign
state, ledger or signing key is needed. Recorded environment: Python 3.11.2,
python-sat 1.8.dev24, six 1.17.0 and CaDiCaL195. The converter is drat-trim
commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, source SHA256
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee.
Download its source URL in `SOURCE_PINS.json` and compile the converter beside
`drat-trim.c`. Preserve the actual venv interpreter path; resolving its
symlink can lose the installed solver environment.

From this directory, with fresh private output directories:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
/absolute/venv/bin/python reproduce.py \
  --work /private/scratch/gap-two-check \
  --converter /private/tools/drat-trim
/absolute/venv/bin/python guards.py \
  --checked-work /private/scratch/gap-two-check \
  --work /private/scratch/gap-two-guards
```

The serial driver generates and independently audits all twelve complete
CNFs, counters and prior clauses normally and under Python -O before native
proposals. Each positive proposal is converted and strictly checked in both
modes. Limits are native 50000 requested conflicts/30 seconds, conversion
25 internal/30 external seconds, strict checks 30 seconds per mode and
definition stages 55 seconds. It stops at the first incomplete case. Resume
accepts already checked positives only, with unchanged inputs and new exact
replays; identical native failures are never retried.

Success is `EXACT_H7_PHASE10_GAP_TWO_FOLLOWING_SELECTION`, with twelve
checked cases. Recorded proofs total 157094 additions, 789484 deletions and
2557872 hints per mode. Fresh valid proofs can differ in bytes and counts;
strict checks remain necessary. Generated models and proof corpora stay in
private scratch.

With `--certificate-cache PATH`, independently supplied candidate traces are
read from `PATH/head/STEM.cnf` and `PATH/head/STEM.lrat`. They must match the
fresh model and canonical fixture, and both strict replays still follow. The
recorded public reconstruction used this route to avoid repeated native
work. Cached proof traces confer no trust.

[VALIDATION.md](VALIDATION.md) and [VERIFICATION.json](VERIFICATION.json)
record source checks and deliberate damages. Ordinary reductions, pinned
premises, the separate literal auditor and strict RUP kernel define the
trust boundary. External independent review and formalization are unclaimed.
