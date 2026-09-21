# Independent review: denominator-five profile cancellation

This directory independently reviews the denominator-five Ehrhart-collapse
octagons and proves a six-facet refinement realizing the same four local
profiles.

From the repository root, using CPython 3.11+ and only its standard library:

```bash
DIR=polyhedral_combinatorics/prime5_ehrhart_profile_cancellation_review1
PYTHONDONTWRITEBYTECODE=1 python3 "$DIR/verify_independent.py" \
  | diff -u "$DIR/EXPECTED_OUTPUT.txt" -
PYTHONDONTWRITEBYTECODE=1 python3 -O "$DIR/verify_independent.py" \
  | diff -u "$DIR/EXPECTED_OUTPUT.txt" -
(cd "$DIR" && sha256sum -c SHA256SUMS)
```

Expected: both diffs are silent and every manifest entry prints `OK`.

Files:

- `REVIEW.md`: verdict, premise audit, complete proof of the six-facet
  refinement, literature boundary, and remaining minimality problem;
- `verify_independent.py`: exact checker that imports no target source or
  fixture;
- `EXPECTED_OUTPUT.txt`: deterministic compact record;
- `SHA256SUMS`: source-integrity manifest.

The finite calculations corroborate the result. Universal correctness rests
on the human-audited fan, face, and local-Fourier reductions in `REVIEW.md`.
