# All Gaussian thresholds from a finite Gram certificate

For a finite contraction, let A,B contain the independently centered point
coordinates, `S=A^T A`, `F=||AA^T-BB^T||_F^2`, and delta be the smallest
squared-distance loss. The exact guard

```
S >= k I_3,     k>0,     k delta >= 4F
```

certifies a straight contracting motion after rigid alignment. It proves
Gaussian majorisation at **every variance and every threshold, for every
probability vector on those labels**. The [proof](PROOF.md) derives the
guard from accepted rigidity and credits the known continuous-contraction
comparison theorems.

A uniform corollary covers all configurations of at most 19 active atoms
with centered source radius at most 1/2, source covariance at least
`2^-15 I`, mean squared-distance loss at most `2^-40`, and every pair loss
at least one quarter of the largest. No lower atom-weight bound is needed.
This closes the entire threshold range in that finite parameter sector,
including loss tending to zero. Unbalanced losses remain outside this
corollary; the unrestricted R3 problem remains open.

Run from this directory with standard-library CPython 3.11 or later:

```
python3 -B certificate.py INPUT.json > /tmp/balanced-loss-record.json
python3 -B verify.py INPUT.json /tmp/balanced-loss-record.json
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

The separate checker reconstructs F from double-centered distance losses,
and S from pair differences. Its supplied-record mode does not import the
producer. Expected control marker: `BALANCED_LOSS_ALL_THRESHOLD_PASS`;
about 0.3 seconds and 17 MB on the development host. The producer uses
O(n^2) rational operations and O(n) storage; the checker uses O(n^2)
storage. Rational bit cost depends on the input.

[INPUT.json](INPUT.json) and [CERTIFICATE.json](CERTIFICATE.json) calibrate
the interface with a reflected, translated member of an entire paired-rank
six family. Polynomial identities and positive Bernstein coefficients cover
its full parameter interval; 12 finite controls and 27 damaged/malformed
rejections check implementation boundaries. [EXPECTED.json](EXPECTED.json)
records these outputs. [INPUTS.json](INPUTS.json) pins six durable sources.

Nonisometric failed guards return `UNRESOLVED` or
`UNRESOLVED_SOURCE_RANK`; neither is a negative Gaussian conclusion.
The [handoff](HANDOFF.md) locates the remaining quadratic loss boundary.
Author proof and exact controls are complete; independent review and
historical-priority assessment remain pending.
