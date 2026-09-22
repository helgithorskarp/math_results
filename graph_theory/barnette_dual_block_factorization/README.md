# Barnette dual block factorization

This directory proves that Hamilton cycles of a Barnette graph containing one
fixed edge-color perfect matching factor exactly over the blocks of the
corresponding bicolored dual.

Each non-bridge block contributes the number of ways to delete
non-articulation green faces so that the block becomes a tree.  The product
of those local counts is the exact global number.  For a cactus dual this
simplifies to a closed product: count the degree-two green vertices in each
cycle block.  The proof is a planar boundary bijection followed by a
block-cut decomposition.

Files:

- `THEOREM.md` — complete proof, constructive algorithm, and scope.
- `SOURCES.md` — primary literature and novelty boundary.
- `verify.py` — exact standard-library audit of both product formulas.
- `expected.json` — pinned deterministic output.
- `run_checks.sh` — reproduction entry point.
- `SHA256SUMS` — source manifest.

Reproduce with Python 3.11 or later:

```bash
./run_checks.sh
```

The universal result is the written proof.  The checker audits the finite
combinatorial conventions only.
