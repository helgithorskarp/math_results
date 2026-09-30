# Independent two-STS(9) review

**six-reviewer-1, independent reviewer**, 2026-09-30.

Read [REVIEW.md](REVIEW.md) for the confirmed scope, complete finite coverage,
and improved capped certificates of maximal lower-slack rank. The target is
`bafkreigbat7eropwjyin2bydiwxu42mg2vrebvturxsd26szqirisc6l3e`, source
commit `4b419710be5c9d15b78649707728e26e915dca96`.

From this directory, using Python 3.11+ and no external packages:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Both checker commands output [expected.json](expected.json). The checker
regenerates every STS(9) by completing whole point stars, verifies 840 explicit
normalization witnesses, reconstructs the complete 192-system disjoint
cohort and its 144/48 orbits, and independently expands each rational table.
It checks both bounds and ranks by integer fraction-free elimination.

[source_certificates.json](source_certificates.json) is copied unchanged
from six-downset-2's `two9_certificates.json` at the reviewed commit. Its
317 rational orbit weights are untrusted data, validated by the independent
decoder and matrix checker. No researcher code or large matrix/census data
is imported.

Original matrices have bound/upper-slack ranks `(60,69)`. The independent
refinement `(1023 Q + P)/1024`, with the explicitly reconstructed ordinary
partition Gram matrix `P`, has ranks `(61,69)` in both cases. Its products
attain `70^k-9k`, maximal for every `k>=1`, and their only maximum intersecting
families are the `9k` coordinate stars. These infinite statements use the
complete kernel and tensor proofs in the review, not finite extrapolation.

The original source verifier separately reproduced at its pinned commit with
`python3 spectral_downsets_steiner_triples/verify_two9.py --check`. That replay
is not required by this independent entry point.
