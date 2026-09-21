# Independent review: equivariant total-graph fixed spaces

This directory independently reviews
[`total_graph_fixed_points`](https://github.com/helgithorskarp/math_results/tree/e269dc5b33ae06567ecdedae95dea59c8b335b87/combinatorial_topology/total_graph_fixed_points).

**Verdict: ACCEPT, high confidence.** The explicit core deformation,
equivariant attachment replacement, reduced-permutation sphere action,
subgroup fixed-space formula, and integral orientation signs are correct.

[REVIEW.md](REVIEW.md) enumerates the human premises, tests adversarial
smallest examples, separates finite corroboration from the universal proof,
and records three consequences: an equivariant cofiber splitting, a
componentwise fundamental-group formula, and a fixed-point Euler formula.

## Reproduce

CPython 3.11 or newer and the standard library suffice.

```bash
cd combinatorial_topology/total_graph_fixed_points_review1
PYTHONDONTWRITEBYTECODE=1 python3 verify_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

The deterministic checker uses exact finite-set, integer-chain, and binary
linear-algebra operations. It has no solver, floating point, randomness,
network input, third-party dependency, external dataset, or omitted
certificate. A full run takes about fifteen seconds on the review host.

## Files

- `REVIEW.md`: verdict, complete proof-premise audit, refinements, caveats.
- `verify_independent.py`: exhaustive independent checker.
- `expected.json`: frozen compact evidence.
- `SOURCES.md`: primary source and search boundary.
- `SHA256SUMS`: integrity manifest.

