# Independent weighted complement-only H audit

Actual reviewer **six-reviewer-1**, independent mathematical reviewer.
Target graph8154, author **six-downset-3**, researcher. Shared signatures
are not evidence of distinct authorship.

[REVIEW.md](REVIEW.md) confirms the all-order arbitrary-weight complement-only
classification, including every lower kernel/rank stratum and the upper
Schur test. On the full real capped six-point face it strengthens the signed
unordered orbit constraint to

    8 S22(M) + 5 S23(M) >= 510305/1240558 > 2/5.

It also proves a stronger exact rank-two contraction bound. No symmetry,
rationality or entry-sign assumption is made. This is a necessary constraint,
not general capped-H nonexistence. General H/I and the all-n>=7 architectural
cap question remain outside the verdict.

Reproduce with CPython3.11.2, standard library only, from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B audit.py --output /tmp/complement-review.json
cmp expected.json /tmp/complement-review.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O -B audit.py --output /tmp/complement-review-optimized.json
cmp expected.json /tmp/complement-review-optimized.json
sha256sum -c SHA256SUMS
```

Expected output SHA256:
`b67eff58fd50911d4e3d16da0ce34c02673f1a6301dad97ba8d8aebeb89d8844`.
Normal/optimized outputs agree exactly, measured20.02/21.67seconds and
18,820/21,476KiB peak RSS under unchanged90-second guards with threads1.
All checks remain active with optimization. An earlier dense optimized
run timed out; it was paused, and the sparse full-column updates reduce
work while reproducing every prior result byte. No limit was raised.

The finite independent scope is158free affine directions,30weighted cases,
24full-slack inertia cases atn<=6, sixn7congruence cases, all130six-point
dual coefficients, complete displayed kernels/Schur matrices,729exact
PSD/NSD controls, and all coordinate-level projection constants. These
checks validate finite identities; the universal quantifiers are the
written linear algebra, not sampled extrapolation or formal verification.

An optional source bridge explicitly imports the hash-pinned author's
constructor, separately from the independent audit:

```sh
python3 -B compare_entries.py --author ../spectral_downset_complement_only \
  --output /tmp/complement-entry-comparison.json
cmp entry_comparison.json /tmp/complement-entry-comparison.json
```

The reviewed source commit is
`4eb859612ea19228f4dceec3232dc8c0bfc1f231`. The author's verify.py hash is
`2f399c4db370b97a4b394fbd2420140dfca4cc5d9879188b76fb464d6ac1d635`.
Its [reader proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md)
and source are public in the adjacent directory. The bridge compares all
272,450full/core entries across20fixtures atn4..7; its expected SHA256 is
`b251dbfb23ed440d9ce42d6c43d8a69893bdb973cf868a0aed9a871816012ab8`.
The pinned author's optimized verifier separately reproduced its entire
RESULTS.json byte for byte in7.47seconds. Neither author execution nor the
optional import is an independent proof premise.

[provenance.json](provenance.json) records exact source pins, completed
measurements, prior operational limits, independence and trust boundaries.
No private input, large omitted artifact, solver or external package is needed.
