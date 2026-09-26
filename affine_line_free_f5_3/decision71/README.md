# Exact decision of the 71-point line-free problem

**Work in progress:** the complete finite reduction is verified; the
109,676 lifting proofs are being checked. No exact value is claimed until
every case has a checked certificate. The established interval is
$70\le r_5(\mathbb F_5^3)\le71$.

The [written reduction](THEOREM.md) covers every hypothetical 71-point
line-free set by 309,611 normalized quotient matrices in 109,676 affine
classes. Two different complete enumerators agree entry by entry. A
second orbit checker applies all 12,000 affine maps to every representative
and verifies disjoint coverage of the complete catalogue. Each lift is
expressed by a direct formula with only the 125 point variables.

The team's [two-low-plane theorem](../low_pair71/README.md) supplies a
15-type cover contained in the fixed 20-type family used here. The
verifier replays its fourteen integer certificates. An alternative,
weaker counting argument within this directory also establishes the
20-type cover. Neither route uses an earlier SAT exclusion or assumes
that a candidate has an affine symmetry.

## Reproduce the reduction

Requires Python 3.10 or later, a C++20 compiler named `g++`, and the pinned
Python-SAT dependency. Tested with Python 3.12.14, Python-SAT 1.9.dev15,
CaDiCaL 1.9.5, and GCC 12.2.0. Run from this directory:

```sh
python3 -m pip install -r requirements.txt
python3 verify.py --out /tmp/decision71-reduction
```

Expected status: `COMPLETE_71_POINT_REDUCTION_VERIFIED`. The generated
`orbits.json` has SHA256
`02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2`.
This command checks the two planar censuses, exact incidence certificates,
both quotient enumerations, the complete affine partition, direct affine
geometry, all 160 fiber-cardinality truth assignments, and three explicit
70-point construction controls. It does not check the lifting proofs.

To check every C++ computation with AddressSanitizer and
UndefinedBehaviorSanitizer, use:

```sh
python3 -O verify.py --sanitize --out /tmp/decision71-sanitize
```

## Generate and check all lifting proofs

Build the official [DRAT-trim](https://github.com/marijnheule/drat-trim)
checker at source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
or use the documented [small-allocation configuration](CHECKER.md).
Then run:

```sh
python3 replay.py --domain /tmp/decision71-reduction/orbits.json \
  --out /tmp/decision71-proofs --drat-trim /path/to/drat-trim
python3 audit.py --domain /tmp/decision71-reduction/orbits.json \
  --proofs /tmp/decision71-proofs --out /tmp/decision71-audit.json
```

The replay must report `verified: 109676` and `complete_family: true`.
Each case needs a separate checker process that exits zero and reports
`s VERIFIED`. A SAT model is saved and checked directly. UNKNOWN,
incomplete coverage, mismatched input, and failed proof checks are never
treated as exclusions. The default conflict budget is 500,000 per case;
raising it is permitted when a different build reaches its limit.

For four processes, partition the cases into these half-open intervals:

| `--start` | `--stop` |
|---:|---:|
| 0 | 27419 |
| 27419 | 54838 |
| 54838 | 82257 |
| 82257 | 109676 |

Use the same output directory with disjoint ranges. Every completed case
is saved atomically. Repeating a range checks saved input and proof hashes
before resuming. Add `--recheck-existing` to invoke the selected proof
checker again on saved traces. A partial range reports incomplete family
coverage; the final audit must cover all indices exactly once.

The audit regenerates every formula from the published source, compares
the input bytes and all saved proof hashes, checks original acceptance
logs, and creates compact ordered block digests. It does not recheck
DRAT inferences; that is the replay's job. Hashes identify evidence and
cannot establish an UNSAT claim by themselves.

For concurrent auditing, run one `audit.py` process for each of the four
intervals above, supplying the matching `--start` and `--stop` values
and a distinct output JSON. The optional `--wait-for-records` flag follows
the producer and waits for each atomic record instead of skipping it.
After all four audits finish, merge them:

```sh
python3 merge_audits.py --domain /tmp/decision71-reduction/orbits.json \
  --out /tmp/decision71-audit.json \
  /tmp/audit0.json /tmp/audit1.json /tmp/audit2.json /tmp/audit3.json
```

Missing or overlapping intervals are rejected. Digest blocks are fixed
relative to these standard four ranges, including their partial final
blocks, so a full serial audit and this merge produce identical ordered
input and proof digests. Reproduction need not match timing fields or
historical proof bytes; all regenerated traces must verify.

Pipeline controls exercise type and process boundaries, resumption,
invalid proofs, damaged records, missing cases, and a budget-one UNKNOWN:

```sh
python3 validate_pipeline.py --domain /tmp/decision71-reduction/orbits.json \
  --out /tmp/decision71-controls --drat-trim /path/to/drat-trim
```

Raw catalogues, formulas, proof traces, checker logs, binaries, and local
checkpoints are generated outside Git. Proof bytes may differ between
solver builds: a new trace must verify against the specified input, but
need not reproduce a historical search trace. The runner flushes and
copies the native binary proof stream before deleting the solver object.

## Scope and dependencies

The trust boundary is the written mathematical reduction, exact integer
certificate checking, exhaustive ordinary C++ and Python programs, direct
CNF semantics, and DRAT-trim. CaDiCaL supplies proof traces; its verdict
alone is never a premise. This is not a proof-assistant formalization.
Independent review of the new 71-point decision is pending.

[SOURCES.md](SOURCES.md) records attribution, mathematical dependencies,
related teammate results, and the distinction between this decision and
the earlier bound. The known 70-point sets are checked directly from
their point lists. No earlier numerical upper bound is needed to deduce
an upper bound of 70 from a complete exclusion of 71 points.
