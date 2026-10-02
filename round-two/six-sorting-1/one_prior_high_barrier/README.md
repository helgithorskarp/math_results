# Thirteen-input L4, one preceding HIGH equal merge

Executing agent: **six-sorting-1, researcher**. The scoped result is in
[PROOF.md](PROOF.md). No size-44 sorting network is constructed and the
unrestricted 44..45 gap is unchanged. This source excludes arbitrary-depth
standard completions in the exactly-one-prior-HIGH-merge singleton branch
of the literal prefix `B23;L4`.

From this directory, using CPython 3.11 or later and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 run.py
```

The runner uses one child at a time and a 55-second limit on each finite
stage. It regenerates all source data and runs each independent scalar
checker both normally and with `-O`. Expected final status:
`ALL_ONE_PRIOR_HIGH_PREMISES_AND5613_NESTED_EXCLUSIONS_VERIFIED_NORMAL_AND_O`.
Expected counts: 762 preparation functions, 501 minimum-lock exclusions,
261 retained functions, 2,044 rejected heads, 5,613 complete fronts and
25,630 selected outer witnesses. The smallest strict selected mass is
`17729624997888 > 2^44`.

Reproduction takes several minutes on one core. Generated arrays and
receipts are kept in ignored `work/`; they are omitted from publication.
The compact summary is [certificate.json](certificate.json), with source
pins in [source-manifest.json](source-manifest.json). Hashes record
reproduction and are never substituted for complete cube/function checks.

The producer uses packed Boolean columns, original-domain activity
projection and canonical weighted tail pairings. Separate scalar checkers
enumerate the full five-variable closure without a length limit, reconstruct
all original cubes and full carrier functions, enumerate every tail event
order, and compute inner anchors with heap `1+max` merges. They import
only `numeric.py`, which imports no producer or sibling. Exact inherited
primitives and mathematical credits appear in
[SOURCE-CREDITS.md](SOURCE-CREDITS.md).

Imported facts: `S(11)>=35`, `S(7)>=16`, `S(6)>=12`, `S(5)>=9`, the
general pruning/standardization, nested and anchored bounds. Their large
published lower-bound corpora are not replayed. Threshold equivalence,
commutation and the minimum-lock induction are written ordinary proofs,
not proof-assistant theorems. This is same-author algorithmic checking;
no external-person verdict is claimed. No timeout, partial enumeration
or unsuccessful heuristic search establishes mathematical nonexistence.
