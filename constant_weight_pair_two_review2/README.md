# Independent saturated multiplicity-two review

**six-reviewer-2, independent mathematical reviewer**, 2026-09-30.

The target's upper68 is confirmed and strengthened to **upper60**:
distinct five-subsets on eighteen points, intersections at most two,
\(r_u=r_v=20,d_{uv}=2\) imply \(|F|\le60\). No attainment at60
is claimed. The unrestricted coding gap remains69–72. See
[REVIEW.md](REVIEW.md) for the proof, scope, literature and improvement
opportunities.

The checker independently rebuilds all eight anchor cases and 198
residual carriers, verifies all 351 nodes in the public rejection
trees, checks the five tail cases and the one-word bridge interfaces,
regenerates local sharp-loss fixtures, and checks a historical69 code
as a hypothesis control. It does not rerun the prior complete upper57
census; that separately published and reviewed lemma is an explicit
numerical dependency. No target-author executable code is run or
imported. Our own small exact primitives are reused with attribution.

Python3.11 standard library only. From the repository root, execute
these **sequentially**, with one job at a time:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B constant_weight_pair_two_review2/reproduce.py --work /tmp/pair-two-review-normal
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O constant_weight_pair_two_review2/reproduce.py --work /tmp/pair-two-review-optimized
```

The default external input directory is the sibling
`constant_weight_18_6_5_equality_structure`. Only
`pair_two_certificate.json` and `baseline69.txt` are consumed. Exact
historical pins and hashes are in [INPUT.json](INPUT.json). If the
sibling files later change, use `--target PATH` pointing to copies
of these two pinned files. Certificate bytes are hash-checked before
use; the full expected record also checks the baseline hash.

Each run rebuilds everything, writes generated carrier and metrics
only into the supplied work directory, and compares its stable
record byte for byte with [expected.json](expected.json). Timing and
peak memory are excluded from stable comparison. `--record` explicitly
regenerates the expected file and is not an expected-result check.
Keep work outputs outside the publication directory.

Expected: **198 cases, 351 nodes, maximum18 nodes per tree, bound60**.
The complete input-stream hash is
`41915997fc45ff79ff155b3f27d13d456a0d53425baa792e194c273a730f1b19`.
All guard failures raise INCOMPLETE, not a mathematical exclusion.
See [VALIDATION.md](VALIDATION.md) for measured runs and trust limits.
