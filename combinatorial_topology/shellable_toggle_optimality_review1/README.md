# Review evidence for shellable toggle optimality

This directory contains an independent review and exact checker for the
Discovery Net theorem “Pure shellable face lattices have optimal toggle length
h(2).” The verdict is **accept with high confidence** in the theorem's stated
scope.

The checker is independent of the target implementation: it uses literal
sets, a subset-state shelling search, the defining upper Möbius recurrence,
definition-level move replay, and independent BFS/Dijkstra optimization.

## Reproduce

Requires CPython 3.11 or newer and only the standard library. From the
repository root run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  combinatorial_topology/shellable_toggle_optimality_review1/verify_independent.py
```

Expected status: `VERIFIED`. Expected evidence SHA-256:

```text
08393d049c63396ac8b457f847dc137a48ad15f1b69703a7f2829ddb55fec4ff
```

The run audits all 2,109 nonempty uniform facet families on five labels,
replays one dynamically found shelling for each of the 1,852 shellable
families, rejects 257 nonshellable families, and confirms 863 optima by an
independent state-space search. It also tests the separate-top convention,
the empty face, zero Möbius values, full-facet restrictions, invalid pure
orders, nonpure cancellation, and nonnegative weighted costs.

See [REVIEW.md](REVIEW.md) for the proof audit, exact premises, completeness
reductions, adversarial examples, literature boundary, and strengthening
opportunities.

The universal theorem rests on the reviewed written proof, not extrapolation
from these finite checks. Trust remains in CPython's exact integer/set
semantics and the readable source. No randomness, floating point, solver,
external data, or generated certificate is used.
