# First unsigned beta test: an exact asymmetric flap certificate

The [author proof](PROOF.md) and rational interval calculation establish
`b_(7,0)>=0` on a specified squared-distance region around an asymmetric
orthocentric sixteen-site flap, for **every probability weight vector**.
At publication this was the first entry not supplied by R2's universal
seven-column theorem. A subsequent [universal kernel certificate](../gaussian_seven_factor_kernel/PROOF.md)
now signs this entry for every bounded R3 contraction at the author-proof
level. This packet's larger pattern margins and source are preserved;
independent review of those numerical margins is pending.

Separately, R4's [full orthocentric-flap theorem](../gaussian_flap_selector_motion/PROOF.md),
[accepted by R7](../gaussian_flap_selector_review_r7/REVIEW.md), covers every
variance and threshold and both KP volume inequalities on the exact flap
family. The unrestricted Gaussian-majorisation question remains open.

The centre is the tetrahedron `(0,0,1), (2,0,-1), (-1,3,-1), (-1,-1,-1)`.
Each source and target squared distance divided by the variance may differ
from its centre value by at most `1/100`, within the orthocentric flap
family. All 32 surviving labelled selectors from R7's reduction are
certified; its other 32 have a known R5 contracting motion. This covers
arbitrary directed flap masses, not just one orientation or balanced weights.

For a selected ten-site contraction the sharper lower bound is
`Q7/1000 + Q8/100 + Q9/30`, where the `Qd` are the explicit replica-pattern
probabilities in the proof. The certificate checks 92,480 occurrences of
47,936 different coefficients, with all other patterns pruned analytically.
Its exact interval stream is hashed and regenerated locally.

From the repository root, with standard-library CPython 3.11 or 3.12:

```sh
python3 probability/gaussian_flap_beta_certificate/certificate.py --check
python3 probability/gaussian_flap_beta_certificate/verify.py --check
python3 -O probability/gaussian_flap_beta_certificate/certificate.py --check
python3 -O probability/gaussian_flap_beta_certificate/verify.py --check
```

The exhaustive certificate takes about 70 seconds on one CPU on the
author's host. It keeps caches in memory and writes no large result file.
`--write` regenerates compact expected records. `verify.py` uses a separate
alternating-series enclosure at the three weakest tuples and audits
coverage and repeated-label multiplicities. Author tests are not independent
mathematical acceptance. [INPUTS.json](INPUTS.json) records durable dependencies.

For R2/R3 consumers: retain this as a quantitative benchmark on the
radius-six compact frontier, including all weight faces. Its explicit
pattern bounds are not replaced by the weaker global distance-loss margin.
The selected ten-site cells allow contractions that need not be exact flaps.
No full all-threshold cover of the compact frontier is claimed by this packet.
