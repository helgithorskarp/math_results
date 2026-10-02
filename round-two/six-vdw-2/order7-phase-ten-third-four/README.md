# Exact-ten phase third-selection bound four

six-vdw-2, researcher. In the H7/F617 seven-AP-free field model, every selected
adjacent run start at exact selected phase count ten has its third selection
at offset 2..4, for either selected value. [PROOF.md](PROOF.md) gives the
quantifiers and complete heterogeneous eight-case cover. Phase endpoints
10/34 and the interval [1,3704] target remain unresolved.

Use a checkout containing the sibling sources. The eighteen helper/premise
files in `SOURCE_PINS.json` are checked before mathematical imports. No
campaign state, ledger or signing key is needed. The environment recorded is
Python 3.11.2, python-sat 1.8.dev24, six 1.17.0 and CaDiCaL195. The converter
is drat-trim commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, source SHA256
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee.
Download the source URL in `SOURCE_PINS.json` and compile `drat-trim` beside
`drat-trim.c`. Preserve the actual venv interpreter path; resolving its symlink
can lose the installed solver environment.

From this directory, using fresh private output directories:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
/absolute/venv/bin/python reproduce.py \
  --work /private/scratch/third-four-check \
  --converter /private/tools/drat-trim
/absolute/venv/bin/python guards.py \
  --checked-work /private/scratch/third-four-check \
  --work /private/scratch/third-four-guards
```

The serial driver generates all eight models and independently audits both
definitions and heterogeneous counters normally and under Python -O before
native proposals. It converts each positive proposal and strictly checks its
RUP trace in both modes. Native stages use 50000 requested conflicts/30 seconds,
conversion uses 25 internal/30 external seconds, strict checks 30 seconds per
mode, and definition stages 55 seconds. It stops at the first incomplete case.
Resume accepts already checked positives only, with unchanged inputs and new
exact replays. Identical native failures are never retried.

Success is `EXACT_H7_PHASE10_ADJACENT_THIRD_INDEX_AT_MOST4` with eight checked
cases. Recorded traces total 105264 additions, 526799 deletions and 1893203
hints per mode. Fresh valid traces can differ in bytes and counts; their
strict checks remain necessary. Generated models and proof corpora stay in
private scratch rather than Git.

With `--certificate-cache PATH`, independently supplied candidate traces are
read from `PATH/head/STEM.cnf` and `PATH/head/STEM.lrat`. The CNF must match the
fresh reconstruction and the candidate LRAT must match the fixture; both
strict replays still follow. The recorded public-source validation used this
route, with cached traces explicitly untrusted, to avoid redundant native work.

The separate auditor, ordinary reductions, pinned premises and RUP kernel
define the trust boundary. External independent review and formalization are
not claimed. [VALIDATION.md](VALIDATION.md) and [VERIFICATION.json](VERIFICATION.json)
record source checks and rejection controls.
