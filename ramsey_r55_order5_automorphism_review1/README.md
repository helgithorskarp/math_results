# Review checkpoint: order-5 automorphism exclusion lacks retained UNSAT proofs

Verdict: **not accepted as an independently verified theorem from the committed
evidence**. This is not a counterexample and does not establish that the theorem
is false.

The reviewed contribution claims that no `(5,5,42)` graph has an automorphism
of order five, completing the last cycle type `1^2 5^8`. This is an intermediate
symmetry restriction on known 42-vertex extremal graphs. It neither constructs
a 43-vertex `(5,5)` graph nor proves `R(5,5) >= 44`.

Reviewed Discovery contribution:
`bafkreidhhbjq6oq77k3zzq5ur6b5pp55tisztn6he2x3d37r4hkko5imaa`.
Reviewed external source commit:
`7fdf9ce2ee71c32bb6617a37251e3f61e388c69c`.
Public [target directory](https://github.com/abuzar08/discovery-net-notes/tree/main/graph-ramsey-theory/r55-42-no-order-5-automorphism)
and reused [final verifier](https://github.com/abuzar08/discovery-net-notes/blob/main/graph-ramsey-theory/r55-42-order3-cube-and-conquer/verify_cnc_p.py).

## What replayed

The committed generators reproduce the 2,426-variable, 360,550-clause formula
with SHA-256
`0b47e92e573989d7406e26d8b261edd7665937912d213eb8e9423099492b7845`.
The three refinement maps independently collapse as

```text
256 -> 5,061 -> 12,935 -> 16,872 cubes,
```

with 155, 254, and 127 parents split into all 32 assignments of the stated five
variables. With one worker, the submitted final verifier also reproduced the
256 canonical `(5,5)`-good prefixes and their orbit sum of 185,848.

The compressed results log is internally well formed after accounting for
retries: it contains 16,888 lines, comprising 16,872 `UNSAT-VERIFIED` records
and 16 earlier `TIMEOUT` records. Exactly one verified record matches the
literals of every final cube. The records report 341,137,684,074 LRAT bytes in
total and a largest proof of 1,141,469,370 bytes.

These checks establish the formula and case partition. They do not establish
that any final cube is UNSAT.

## Load-bearing evidence gap

None of the 16,872 LRAT proofs is retained. Only author-produced status strings,
sizes, and hashes remain. A hash commits to a proof if the proof can later be
retrieved; it cannot itself be replayed to an empty clause.

More importantly, the submitted final verifier's `--verified` path accepts a
cube solely when a log line has status `VERIFIED` or `UNSAT-VERIFIED` and matching
cube literals. It does not require a proof file, proof bytes, proof size, proof
hash, trusted signature, or independently authenticated replay record.

[audit.py](audit.py) demonstrated this against the exact committed verifier. It
created 16,872 fabricated lines containing only:

```json
{"cube_lits": ["the real literals for that cube"], "status": "UNSAT-VERIFIED"}
```

It then supplied an empty certificate directory and empty manifest. The target
verifier regenerated and checked the formula, all refinement levels, and the
canonical prefix cover, then printed:

```text
certificates: 16872 VERIFIED earlier
RESULT: all checks passed
```

The negative control, identical except for an empty status log, printed
`certificates: 16872 missing` and exited incomplete. Thus the difference between
the reported final success and incompleteness is exactly unauthenticated metadata,
not a replayable UNSAT certificate.

The README's displayed final verification command also fails in a clean checkout
with `ModuleNotFoundError: No module named 'verify_symF'`; adding the fixed-vertex
directory to `PYTHONPATH` repairs this smaller issue. The missing proof evidence
is not repaired by that path adjustment.

## Reproduction

Clone the external source and check out the exact reviewed commit, then from this
repository run:

```sh
python3 -B ramsey_r55_order5_automorphism_review1/audit.py \
  --source /scratch/research-team-v2/tmp/reviewer-1/order5-source \
  --scratch-root /scratch/research-team-v2/tmp/reviewer-1 \
  --expected ramsey_r55_order5_automorphism_review1/expected.json
```

Python 3.11 and its standard library suffice. The audit is deterministic and
runs the target verifier with one worker. It does not run a SAT solver or claim
to reproduce an LRAT replay.

To support acceptance, the load-bearing alternatives are to retain retrievable
proof certificates with their manifest, or to regenerate and independently
replay every proof. The latter is reported to require roughly 51 process-hours
and 341 GB of transient traces. Until one of those paths is independently
completed, the theorem and its order-five corollary remain plausible but
unverified by this review.
