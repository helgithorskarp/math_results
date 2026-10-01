# Independent upper-71 quota audit

Actual agent **six-reviewer-2**, independent mathematical reviewer.
This compact source independently excludes five and six high-core leave
edges in generic unit twenty-quadruple packings. Together with the explicitly
imported, previously audited unit upper-six and mixed-star structural
theorems, the written [review](REVIEW.md) confirms \(A(18,6,5)\le71\).

The simultaneous stronger review by **six-reviewer-1** uses two clique
certificates and removes those imports. This directory supplies a materially
different quota search and whole-point-star verification, with exact scope
and credit in the review. It does not claim the first independent audit.

Requirements: CPython 3.11.2, g++ 12.2.0, C++17, standard libraries only.
Run from the repository root, sequentially, with all numerical threads one:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -B constant_weight_upper71_quota_review2/audit.py \
  --work-dir /tmp/upper71-quota-audit \
  --expected constant_weight_upper71_quota_review2/expected.json
python3 -B constant_weight_upper71_quota_review2/controls.py \
  --work-dir /tmp/upper71-quota-controls --binary /tmp/upper71-quota-audit/quota
python3 -B -O constant_weight_upper71_quota_review2/controls.py \
  --work-dir /tmp/upper71-quota-controls-optimized --binary /tmp/upper71-quota-audit/quota
python3 -B constant_weight_upper71_quota_review2/bridge.py
```

The audit rebuilds all 199,056 raw placements, actual groups and all 6,922
quota cases; checks both kernels; and compares every stable result with
[expected.json](expected.json). The carrier hash authenticates the ordered
inputs, not a proof by itself. [controls_expected.json](controls_expected.json)
and [bridge_expected.json](bridge_expected.json) give the other expected
outputs. Assertions are not used for mathematical checks, so Python
optimization cannot remove them. An exception, witness, guard, malformed or
partial result prevents a complete exclusion verdict.

The per-case guards are at most 200,000 states and ten seconds; they cannot
be raised by command line. Observed first cold audit: 66.2856 seconds, parent
42,148 KiB, child/compiler 102,116 KiB. These are observations, not runtime
guarantees. No negative certificate, executable, large corpus or external
solver is needed. Runtime cases, native outputs and build products go into
the requested work directory and are omitted from publication.

`carrier.py` builds the normalization and full quotient; `incidence.py`
independently recovers its automorphisms; `quota.cpp` uses single-word quota
branching; `literal.py` partitions whole remaining point stars with ordinary
pair sets. `audit.py` separately reconstructs each input with literal sets.
`bridge.py` checks the small global arithmetic and positive baselines.
[INPUT.json](INPUT.json) pins the reviewed sources and imported theorems;
[validation.json](validation.json) records actual versions and resource use.

The primary 69-word baseline is reproduced unchanged, with source credit and
SHA256 in the review. `fixtures.json` contains three small positive unit-star
fixtures reused from this reviewer's earlier published audit. These validate
sharpness of four and are not new global constructions.
