# Independent review: prime-index Ehrhart Fourier criterion

This directory independently reviews the prime-index local Fourier formula
for the first potentially varying Ehrhart coefficient.  It also proves a
codimension-two character cancellation at `p=5`.

From the repository root, using CPython 3.11+ and only its standard library:

```bash
DIR=polyhedral_combinatorics/prime_index_ehrhart_fourier_review1
PYTHONDONTWRITEBYTECODE=1 python3 "$DIR/verify_independent.py" \
  | diff -u "$DIR/EXPECTED_OUTPUT.txt" -
PYTHONDONTWRITEBYTECODE=1 python3 -O "$DIR/verify_independent.py" \
  | diff -u "$DIR/EXPECTED_OUTPUT.txt" -
(cd "$DIR" && sha256sum -c SHA256SUMS)
```

Expected: both diffs are silent and every manifest entry prints `OK`.
Each checker run takes about 25 seconds on the publication host.

Files:

- `REVIEW.md`: verdict, complete premise audit, proved refinement, literature
  boundary, and remaining geometric problem;
- `verify_independent.py`: exact checker based on finite cyclotomic reciprocal
  sums and direct four-face parallelogram counts;
- `EXPECTED_OUTPUT.txt`: deterministic compact record;
- `SHA256SUMS`: source-integrity manifest.

The finite checks corroborate the proof.  Universal correctness rests on the
human-audited local cone and Euler--Maclaurin reductions in `REVIEW.md`.
