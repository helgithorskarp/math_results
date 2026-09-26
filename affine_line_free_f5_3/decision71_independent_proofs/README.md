# Independent formula audit and stock proof replay

This package checks the remaining software boundary of the author's
[exact-value proof](../decision71/README.md). It independently reconstructs
the whole input formula for each of the 109,676 quotient representatives
and can freshly check every binary DRAT proof with unmodified DRAT-trim.
It imports no author point-model or evidence module.

**Independent acceptance of the exact value 70 remains pending.** The
recorded all-input audit and the native proof replay are distinct checks.
See [REVIEW.md](REVIEW.md), [INPUT_AUDIT.json](INPUT_AUDIT.json), and
[PROOF_PROGRESS.json](PROOF_PROGRESS.json) for their precise scopes.
A matching digest is evidence identity, not an UNSAT proof.

The [earlier geometric review](../decision71_geometry_audit/REVIEW.md)
already accepts the complete equivalence between a 71-point line-free
set and a model of one of these formulas. Its mathematical implementation
and inputs are unchanged; [SOURCE_BRIDGE.json](SOURCE_BRIDGE.json) records
the exact comparison. This package addresses all exported formula bytes
and the new global proof obligation.

## Software and checker

The review code needs only Python's standard library. Tested with Python
3.11.2, Linux, and GCC 12.2.0; `run_bounded.py` uses POSIX file locking.
The author regeneration pipeline separately needs Python-SAT 1.9.dev15
with CaDiCaL 1.9.5; it was tested here using Python 3.12.14.

Run from this directory. Keep generated data outside the repository.

```sh
R5_REVIEW_TMP=/tmp/r5-independent-review
mkdir -p "$R5_REVIEW_TMP"
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c \
  -o "$R5_REVIEW_TMP/drat-trim.c"
sha256sum "$R5_REVIEW_TMP/drat-trim.c"
gcc -std=gnu99 -O2 "$R5_REVIEW_TMP/drat-trim.c" -o "$R5_REVIEW_TMP/drat-trim"
```

The required source SHA256 is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
No allocation patch is applied. The review's executable SHA256 is recorded
in the validation data; another compiler may produce a different binary.
Each invocation must exit zero and print a complete `s VERIFIED` line.
A timeout, failure, missing case, or incomplete range is never acceptance.

## Regenerate independently checkable evidence

First reproduce the complete quotient domain using the public author
pipeline, as reviewed in `decision71_geometry_audit`:

```sh
python3 -m venv "$R5_REVIEW_TMP/venv"
"$R5_REVIEW_TMP/venv/bin/python" -m pip install -r ../decision71/requirements.txt
"$R5_REVIEW_TMP/venv/bin/python" ../decision71/verify.py \
  --out "$R5_REVIEW_TMP/reduction"
"$R5_REVIEW_TMP/venv/bin/python" ../decision71/replay.py \
  --domain "$R5_REVIEW_TMP/reduction/orbits.json" \
  --out "$R5_REVIEW_TMP/generated" --drat-trim "$R5_REVIEW_TMP/drat-trim"
```

These commands generate roughly 20 GB of proof traces plus formulas and
metadata. None of that generated corpus is included in Git. Domain SHA256:
`02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2`.

Fresh proof traces can legitimately differ from the archived ones. This
occurred in our hardest-case control, index 20750: both traces verify for
the same independently reconstructed CNF. To check regenerated evidence,
without requiring historical proof bytes, run:

```sh
python3 check_regenerated.py \
  --domain "$R5_REVIEW_TMP/reduction/orbits.json" \
  --corpus "$R5_REVIEW_TMP/generated" \
  --checker "$R5_REVIEW_TMP/drat-trim" \
  --checker-source "$R5_REVIEW_TMP/drat-trim.c" \
  --out "$R5_REVIEW_TMP/regenerated_review.json"
```

This independently reconstructs every formula and freshly checks every
trace. A complete execution must report `verified: 109676` and
`complete_family: true`. This driver does not reuse saved checks.
Its `--start` and `--stop` options are for diagnostic ranges, which are
incomplete unless they cover the entire domain in that invocation.
The recorded new-trace test in this package covers only index 20750;
we do not claim a completed fresh-generation run.

## Replay the archived original corpus with checkpoints

The following route is for an available copy of the original corpus.
Set `R5_ORIGINAL_CORPUS` to its root. These checks deliberately bind the
original proof hashes as well as the input family. They may reject a
different valid regenerated trace; use the preceding driver for that case.

```sh
python3 audit_inputs.py \
  --domain "$R5_REVIEW_TMP/reduction/orbits.json" \
  --manifest ../decision71/CERTIFICATES.json --corpus "$R5_ORIGINAL_CORPUS" \
  --out "$R5_REVIEW_TMP/input_audit.json" --workers 8
python3 check_saved.py \
  --domain "$R5_REVIEW_TMP/reduction/orbits.json" \
  --manifest ../decision71/CERTIFICATES.json --corpus "$R5_ORIGINAL_CORPUS" \
  --checker "$R5_REVIEW_TMP/drat-trim" --checker-source "$R5_REVIEW_TMP/drat-trim.c" \
  --out "$R5_REVIEW_TMP/pilot" --pilot --known70 ../known70.json
python3 run_bounded.py \
  --domain "$R5_REVIEW_TMP/reduction/orbits.json" \
  --manifest ../decision71/CERTIFICATES.json --corpus "$R5_ORIGINAL_CORPUS" \
  --checker "$R5_REVIEW_TMP/drat-trim" --checker-source "$R5_REVIEW_TMP/drat-trim.c" \
  --out "$R5_REVIEW_TMP/stock_replay" --seconds 1200
```

Repeat the last command to resume. It waits for four workers on disjoint
half-open intervals `[0,27419)`, `[27419,54838)`, `[54838,82257)`, and
`[82257,109676)`. A worker stops at a durable 25-case boundary after its
runtime limit; completed 1,000-case or boundary blocks must match the
public ordered digests. Resumption checks the frozen runner, checker,
source, domain, manifest, case order and actual inputs. Start with an
empty review directory for a new independent replay: local checkpoints
are trusted operational records of earlier reviewer executions.

`INCOMPLETE_DURABLE_CHECKPOINT` is not a proof verdict. The driver invokes
the complete summary only after all 112 blocks are present; that summary
then validates exact coverage, every block and all twenty type counts.
Only `COMPLETE_INDEPENDENT_STOCK_PROOF_REPLAY_VERIFIED` establishes that
the entire archived family passed this native proof replay.

Keep the supervising command alive until its bounded run finishes.
An agent execution session may end at a turn boundary; process survival
across a controller rest is not assumed. Atomic checkpoints preserve
finished work, with at most 25 completed cases per worker lost on abrupt
interruption between checkpoint writes.

The complete serial reference audit, in `audit_inputs_reference.py`, and
the eight-thread audit both passed and agree in every mathematical output.
The reference source is retained for comparison; `--workers 1` also runs
the current audit with one I/O worker. Neither input audit invokes DRAT.

## Controls and trust

The pilot covers all twenty types, partition boundaries and the hardest
author case. It directly checks a genuine 70-point line-free set and its
gauged satisfying assignment. Empty proofs, false empty-clause assertions,
an UNSAT trace applied to that satisfiable formula, damaged completed
blocks, and damaged partial checkpoints must be rejected. An actual
two-process stop/resume test verifies that saved cases are preserved and
not counted again as fresh checks. See [VALIDATION.json](VALIDATION.json).

The trust boundary remains the written reduction, exact ordinary program
execution, Python, the compiled unmodified DRAT-trim implementation, and
the runtime/hardware. This is not proof-assistant verification. The SAT
solver supplies traces; its verdict is not an acceptance premise.
