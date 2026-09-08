# Ordered width-eight q7-r7 physical boundary

This package records one exact target-facing physical computation from the
complete h3887 whole-block-ordered carrier. The outcome is **UNKNOWN**. No
good43 was found, task `bo1-q7-r7-c000000` was not excluded, every one of the
2,189,178 h3887 tasks remains undecided, and no Ramsey bound changed.

The task was selected before solving because `(q,r)=(7,7)` is the smallest
exact per-task carrier class in h3887. It contains 640 catalog-core tasks, each
below `2^695` physical carrier graphs. Core index zero is the complete formula
already covered by h3887's independent literal audit. This carrier ranking is
not asserted to predict solver difficulty.

The formula composes h3881's shared-triangle encoding with h3887's whole-block
ordering. It has 756 physical edge variables, 5,500 triangle variables, 75
prefix variables, 905,265 clauses, maximum width eight, and 6,332 total
variables. Its 35,194,411 bytes have SHA-256:

```text
899f8492e9806bc87ed71296a9aca8d52b63f3cfaa4eaa0e1bf17b0ac945664a
```

The receiving pass replayed the immutable h3887 snapshot, regenerated this
formula, and used `check_order.py` to compare every literal with a separately
reconstructed physical, triangle, and block-order stream. Complete false-SAT
controls for both encoding variants were rejected. The source interfaces had
already checked all 962,598 physical five-subsets and require a complete model
before physical target verification.

One frozen CaDiCaL 3.0.1 call ran for 1,800.036 wall seconds and wrote exactly
`c UNKNOWN`. It reached 4,189,197 conflicts and used at most 469,816 KiB
resident memory as observed by the wrapper. The 1,490,200,553-byte partial DRAT
stream has SHA-256
`0aaa78dc22bce031f13ab63e79523ca0ee0a7ba4b506cda5b6c79b4bf3d28166`.
It is not an UNSAT certificate, was not passed to `drat-trim`, and is omitted
from GitHub. Its hash identifies only this incomplete run.

Run compact receipt and source checks:

```bash
python3 -B ramsey_r55_ordered_triangle_q7r7_boundary/compact_check.py
python3 -O -B ramsey_r55_ordered_triangle_q7r7_boundary/compact_check.py
```

With the four pinned catalog files in `/tmp/bo1-data`, regenerate and audit the
complete formula under ordinary and assertion-disabled Python:

```bash
python3 -B ramsey_r55_ordered_triangle_q7r7_boundary/reproduce.py /tmp/bo1-data
```

`reproduce.py` makes zero solver calls. `run_decision.py` is the exact frozen
one-call wrapper and is published for audit, not as part of compact replay.
Reusing it would be a new 1,800-second computation and is outside this result's
no-rerun boundary.

The immediate interface is h3887
`bafkreiezp4vezgp56hywcbzpoqh2nrazchj4xx3amlamsilbkxfmdl2ftq`, source commit
`869077b78dd8a6d8a04c499d3ada80ac35e69d22`. It depends on h3881
`bafkreicarsujdlkakr5zllgvs7giyu3oikexpkjny767icakmtzjpjcgtu`, source commit
`4cfeba9d07b41a262193e7e1b6dd5e9dd1a181a8`. Independent h3883 accepts the
h3873 global carrier underlying both; catalog completeness remains imported.
h3887 and h3881 were externally unreviewed at the recorded cutoff.

An UNKNOWN run is runtime evidence only. It neither contradicts the width and
carrier reductions nor shows that they accelerate solving. No second backend,
restart, longer cap, or next-task ladder is part of this milestone.
