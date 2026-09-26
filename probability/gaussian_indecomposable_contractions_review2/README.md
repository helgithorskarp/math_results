# Review 2: indecomposable Gaussian-contraction reduction

This directory independently reviews the proof at source commit
`4518e569424cbac04083e6cb9497cc97991cf301`, graph target
`bafkreihtkvrmyjs4cswetyjge4rpwvppjunbtmd4tnrw3o65cwvfa5wyey`.

**Verdict:** accepted with high confidence as an exact reduction to
indecomposable finite contractions fixing a tetrahedron, including the two
ball-volume reductions. This is not acceptance of the still-open Gaussian
sign on the reduced class or of the full dimension-three conjecture.

The mathematical audit is in [REVIEW.md](REVIEW.md). The independent checker
reconstructs the four complete fixture intervals from labelled squared
distances and checks the all-depth regular-simplex flap identities without
importing the reviewed packet.

Run from the repository root with standard-library CPython 3.11 or later:

```sh
python3 probability/gaussian_indecomposable_contractions_review2/independent_check.py
python3 -O probability/gaussian_indecomposable_contractions_review2/independent_check.py
sha256sum -c probability/gaussian_indecomposable_contractions_review2/SHA256SUMS
```

Expected output from each Python invocation:

```text
PASS: independent interval counts 4,2,2,2 and saturated chains 2,1,1,1
PASS: exact all-depth simplex-flap coefficient and synchronization identities
```

The checker certifies only the exact fixtures and displayed flap algebra.
Brehm extension and the universal reduction are externally sourced and
written-proof obligations, respectively; no Gaussian integral or unknown sign
is computed.
