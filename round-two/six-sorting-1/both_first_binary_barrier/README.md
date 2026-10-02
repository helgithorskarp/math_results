# A conditional binary barrier for changed thirteen-input B23

Agent **six-sorting-1**, role **researcher**. This packet proves that after
either remaining canonical LOW26 front, the first strict HIGH pair-mass
increase cannot be binary at total size 44. Its audited commutation argument
also proves that a size-at-most-44 completion of the literal B23 must have
a singleton first strict increase on at least one side. Arbitrary comparator
depth and preparation length are covered.

The [proof](PROOF.md) gives the literal prefix, definitions and logical bridges.
There is no size-44 construction or complete B23/global exclusion. The
[current table](https://bertdobbelaere.github.io/sorting_networks.html), checked
2026-10-02, still lists the unrestricted thirteen-input interval 44..45.

Python 3.11+ and its standard library suffice. The copied producer helpers
are local, hash-pinned and credited in [SOURCE-CREDITS.md](SOURCE-CREDITS.md).
The standalone checker imports no sibling implementation or producer.
From the repository root, run the jobs sequentially:

```sh
timeout 55s env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-sorting-1/both_first_binary_barrier/generate.py --output /tmp/b23-both-binary-certificate.json
timeout 55s env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-sorting-1/both_first_binary_barrier/verify.py --certificate /tmp/b23-both-binary-certificate.json
timeout 55s env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-sorting-1/both_first_binary_barrier/verify.py --certificate /tmp/b23-both-binary-certificate.json
```

The 55-second wrapper is an operational limit, not a mathematical cutoff.
An interrupted or incomplete invocation establishes no exclusion.
Commands also work from another directory with absolute script paths.

Expected statuses: `BOTH_FIRST_BINARY_CERTIFICATE_REGENERATED` and
`BOTH_FIRST_BINARY_CERTIFICATE_VERIFIED`. Both checker modes reconstruct
three LOW and 45 HIGH genealogies, all 90 linked conditional fronts, 582
whole original-domain occurrences and 449 distinct seven-input inner words.
Each selected root mass is greater than `2^44`; the minimum is
`18691697672192=(17/16)*2^44`. All 15 deliberate damages must reject.
[expected.json](expected.json) contains the complete finite output without
variable wall time or RSS.

The deterministic 40232-byte certificate has SHA256
`cce7383fbe1e0401ef9c7dbbe9fc176a7603c34ca2148de1ea12a099ee4d6f5d`.
Normal/optimized producers have identical bytes, and normal/optimized
checker finite fields agree. Full generated images, exploratory scans,
logs and proof corpora are unnecessary for reproduction and stay private.

Written thresholding, standardization, ordinary/nested transport and
live-support commutation bridges remain unformalized. The small size bounds
are imported from primary literature. Different algorithms were authored and
executed by the same researcher; no external review verdict is claimed.
