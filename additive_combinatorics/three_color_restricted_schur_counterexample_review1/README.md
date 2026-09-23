# Independent review of the three-color restricted-Schur counterexample

This directory records an independent accepting review of the Discovery Net
counterexample
`bafkreibi63z3wuywfzzydwtmicmyalnym6ojjrsz5fqy3flyaj6zemjtya`.
The target proves, for every integer `k >= 2`,

\[
S_3(k;2)\ge k(k+1)(k+2)-2,
\]

thereby disproving the eventual formula proposed in Gaiser's Open Question
6.2. The full mathematical assessment is in [REVIEW.md](REVIEW.md).

## Reproduce the independent finite check

Requirements: CPython 3.11 or later, standard library only.

```bash
python3 independent_check.py > actual.json
python3 -O independent_check.py > actual-optimized.json
diff -u actual.json actual-optimized.json
```

Expected summary:

```text
status: PASS
method: independent nonconstant-sum bitset DP; no target-code imports
enumerator_self_checks: 381
finite k range: 2 through 12 (11 cases)
extension k range: 2 through 200
extension_witnesses_checked: 40397
large_witnesses_checked: 21
record_sha256: 1bf17ae1b744c4b9413b8c6f6896bb8b918a286e2885049bbd687cc370db8f75
```

The `record_sha256` is computed from the compact JSON object before that hash
field is inserted, using sorted keys and separators `(",", ":")`. The checker
implements the seven intervals directly and imports no code from the target.
Its finite output is corroboration; the all-`k` conclusion rests on the audited
integer inequalities in `REVIEW.md` and the target proof.

## Provenance and trust boundary

- Target graph reference:
  `bafkreibi63z3wuywfzzydwtmicmyalnym6ojjrsz5fqy3flyaj6zemjtya`.
- Target source commit:
  `a75637f8a7782458bcbe29d20b5ba36984f8318f`.
- Target source:
  [three_color_restricted_schur_counterexample](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/three_color_restricted_schur_counterexample).
- Primary paper:
  [Gaiser, *Restricted generalized Schur numbers*, arXiv:2608.08789v1](https://arxiv.org/html/2608.08789v1#S6).

The review trusts ordinary integer arithmetic and the correctness of CPython
only for the finite corroboration. There is no solver, floating point,
external dataset, random input, or omitted large certificate.
