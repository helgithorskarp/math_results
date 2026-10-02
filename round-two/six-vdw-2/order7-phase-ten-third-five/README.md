# Third selection within five positions at phase-ten run starts

six-vdw-2, researcher. [PROOF.md](PROOF.md) gives the exact restricted H7/F617
statement: either phase value occurring ten times has a third occurrence within
positions 2..5 of every adjacent-run start. Sixteen fourth-selection cases
exclude the remaining third-index-six class. Phase weights 10/34 and the
interval [1,3704] target remain unresolved.

Use a checkout of this repository containing the sibling source directories.
`SOURCE_PINS.json` checks all sixteen inherited mathematical/helper files before
importing them. `SHA256SUMS` pins the compact contribution. Nothing needs a
private ledger, signing key or campaign state.

The recorded run uses Python 3.11.2, python-sat 1.8.dev24, six 1.17.0 and
CaDiCaL195. The converter source is drat-trim commit
2e3b2dc0ecf938addbd779d42877b6ed69d9a985, SHA256
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee;
its URL is in `SOURCE_PINS.json`. Compile it as `drat-trim` beside `drat-trim.c`.
Keep the actual virtual-environment interpreter path when running; resolving
its symlink can lose the installed solver environment.

From this directory, with a fresh private output directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
/absolute/venv/bin/python reproduce.py \
  --work /private/scratch/third-five-check \
  --converter /private/tools/drat-trim
/absolute/venv/bin/python guards.py \
  --checked-work /private/scratch/third-five-check \
  --work /private/scratch/third-five-guards
```

The driver serially generates and independently audits all sixteen CNFs in
normal and optimized Python before native proposals, conversion and both strict
RUP replays. Every native stage is capped at 50000 requested conflicts/30 seconds;
conversion uses 25 internal/30 external seconds; strict checks use 30 seconds
per mode; definition stages use 55 seconds. It stops on the first incomplete
case, which proves no exclusion. Resume is allowed only for already checked
positives with unchanged inputs and another exact replay; failed native models
are never retried identically.

Successful output has status
`EXACT_H7_PHASE10_ADJACENT_THIRD_INDEX_AT_MOST5` with sixteen exact cases,
197051 additions/1037464 deletions/3222678 hints per Python mode for the recorded
proof bytes. Fresh solver traces may have different byte hashes/counts; the
strict checks remain mandatory. No proof corpus is distributed in Git.

For independently supplied candidate LRAT streams, `--certificate-cache PATH`
expects `PATH/head/STEM.cnf` and `PATH/head/STEM.lrat`. Each supplied CNF must
match the freshly regenerated model and each candidate proof must match the
fixture digest; both strict replays still run. Cache presence confers no trust.
The recorded source validation used this path to avoid repeating native work.

Trust remains in the written finite cover, cited universal premises, separate
literal-clause and positive-only RUP algorithms, Python and execution. This is
same-author algorithmic independence; external peer review and formalization
are not asserted.
