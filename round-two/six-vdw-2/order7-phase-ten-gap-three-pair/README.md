# Pair-following necessity for a three-background phase gap

six-vdw-2, researcher. In the exact-ten H7/F617 phase scope, a selected run of
length two followed by three background phases must be followed by another
selected run of length at least two. [PROOF.md](PROOF.md) states the quantified
field hypotheses and complete fourteen-case counterexample cover. Third-index
five, phase endpoints 10/34 and the interval [1,3704] target remain unresolved.

Use a checkout of this repository containing the sibling sources. All seventeen
inherited helper/premise files in `SOURCE_PINS.json` are byte-checked before
mathematical imports. `SHA256SUMS` pins the compact contribution. No ledger,
signing key or campaign state is needed to reproduce the proof.

The recorded environment is Python 3.11.2, python-sat 1.8.dev24, six 1.17.0 and
CaDiCaL195. The converter is drat-trim commit
2e3b2dc0ecf938addbd779d42877b6ed69d9a985, source SHA256
d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee.
Download the URL in `SOURCE_PINS.json`; compile `drat-trim` beside `drat-trim.c`.
Preserve the actual virtual-environment interpreter path rather than resolving
its symlink and losing the installed solver environment.

From this directory, using fresh private output directories:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
/absolute/venv/bin/python reproduce.py \
  --work /private/scratch/gap-three-pair-check \
  --converter /private/tools/drat-trim
/absolute/venv/bin/python guards.py \
  --checked-work /private/scratch/gap-three-pair-check \
  --work /private/scratch/gap-three-pair-guards
```

The serial driver generates and independently audits all fourteen canonical
models in normal and optimized Python before native proposals, conversion and
both strict RUP replays. Native stages use 50000 requested conflicts/30 seconds;
conversion uses 25 internal/30 external seconds; strict checks use 30 seconds
per mode; definition stages use 55 seconds. It stops on the first incomplete
case, which gives no exclusion. Resume is only for already checked positives
with unchanged inputs and another exact replay; identical native failures are
not retried.

Success has status `EXACT_H7_PHASE10_GAP_THREE_FORCES_PAIR` and fourteen exact
cases. The recorded proof streams give 181697 additions, 918244 deletions and
2914862 hints per Python mode. Other valid fresh traces may differ in bytes or
counts; both strict checks remain necessary. Models and proof corpora stay in
private scratch rather than Git.

For independently supplied candidate traces, `--certificate-cache PATH`
expects `PATH/head/STEM.cnf` and `PATH/head/STEM.lrat`. The CNF must equal the
freshly reconstructed model and the candidate LRAT must match the fixture hash;
the driver then strictly replays it in both modes. Cache presence confers no
trust. The recorded source validation used this route to avoid redundant native
work. Its fixture excludes both ell=6 cases; the privately attempted `(6,0)`
UNKNOWN supplies no proof, and the whole third-index-five class is not excluded.

Trust remains in the written finite cover, cited premises, separate literal
auditor and positive-only RUP checker, Python and execution. Same-author
algorithmic independence does not assert another person's review or formalization.
