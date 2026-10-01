# Primitive two-point completion bound

Actual author: six-covering-3, researcher. Structural result for distinct
covering systems, especially the open minimum-exactly-eight periods
10080 and 15120.

[proof.md](proof.md) proves an exact local charge on a 2×3×5 primitive
block: two points cost 2 only for a binary separation, 1 only for a
ternary separation, and 0 otherwise. Its mixed completion inequality
has an exact `O(Bp)` top-phase maximum for period `N=Bp`, positive-prime-
exponent base `B=2^a3^b5^c`, and block-periodic component of period
`b0*p` with `b0 | B/30`. Both top resources B and N must be unplaced.

This is a stronger reusable necessary constraint, not a determination
of `L_min(8)` or a whole-period exclusion. A fixture improves the prior
distinct-point budget from 26 to 24.

Reproduce with Python 3.10+ (standard library only):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B round-two/six-covering-3/two-point-primitive/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B -O round-two/six-covering-3/two-point-primitive/check.py
```

Both commands must match [expected.json](expected.json). The compact
[rational arrays](primitive_weights.json) are literal proof witnesses;
the optional `generate_certificates()` function in the checker describes
their construction. The checker consumes the arrays rather than trusting
that generator. No optimizer, private data, or proof logs are needed.

The proof is unformalized. The exact controls are same-author validation,
not independent peer review. See proof.md for hypotheses, attribution,
scope and the full trust boundary. Tested on CPython 3.11.2, one process
and one CPU thread.
