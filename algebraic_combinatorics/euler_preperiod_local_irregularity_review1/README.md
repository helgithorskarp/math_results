# Independent review: local Euler preperiod irregularity

This directory independently reviews the four-class theorem for modular
three-zero runs in the Euler up/down numbers and proves a companion exact
classification of modular consecutive-zero pairs.

The checker uses only the Python standard library.  From the repository
root, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  algebraic_combinatorics/euler_preperiod_local_irregularity_review1/verify_independent.py \
  | diff -u \
  algebraic_combinatorics/euler_preperiod_local_irregularity_review1/EXPECTED_OUTPUT.txt -

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  algebraic_combinatorics/euler_preperiod_local_irregularity_review1/verify_independent.py \
  | diff -u \
  algebraic_combinatorics/euler_preperiod_local_irregularity_review1/EXPECTED_OUTPUT.txt -

sha256sum -c \
  algebraic_combinatorics/euler_preperiod_local_irregularity_review1/SHA256SUMS
```

Expected: both diffs are silent and every manifest entry prints `OK`.
Runtime is about 20 seconds per checker invocation on the publication host.

Files:

- `REVIEW.md`: verdict, complete premise audit, pair theorem, limitations,
  and literature assessment;
- `verify_independent.py`: exact independent checker;
- `EXPECTED_OUTPUT.txt`: deterministic record;
- `SHA256SUMS`: integrity manifest.

The computation is corroborative.  Universal correctness rests on the
algebraic case split in `REVIEW.md`, not on extrapolation from the finite
range.
