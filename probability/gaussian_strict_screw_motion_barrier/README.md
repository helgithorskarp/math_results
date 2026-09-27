# A concrete strict contraction requiring six motion dimensions

The [author proof](PROOF.md) gives an explicit neighborhood of the
existing 24-site screw in which no prescribed matching has a continuous
contracting motion in R5. Each endpoint's squared-distance matrix may
change by up to **2^-136**, entrywise. No preserved pair, rigid perturbed
group, or preferred endpoint frame is required.

The [rational witness](WITNESS.json) is the original source P with target
`(1-2^-145)Q`. Every one of its 276 pairs contracts strictly, with exact
Lipschitz constant `1-2^-145`, yet its minimum motion dimension is six.
Its augmented anchor matrix also has rank8, excluding the single
norm-preserving primitive. This is not a Gaussian-majorisation
counterexample or a quantitative exclusion of arbitrary mixed chains.

R7 had already proved an existential open neighborhood for a stronger
composition obstruction. The increment here is a numerical rational
radius for the R5-motion component and an explicit strict control. The
bound is intentionally conservative; no historical priority is claimed.
Independent acceptance is pending, and unrestricted R3 majorisation
remains open.

Reproduce from the repository root with CPython3.11 and its standard
library; no solver or numerical library is needed:

```bash
python3 -B probability/gaussian_strict_screw_motion_barrier/verify.py
python3 -O -B probability/gaussian_strict_screw_motion_barrier/verify.py
python3 -B probability/gaussian_strict_screw_motion_barrier/verify.py probability/gaussian_strict_screw_motion_barrier/WITNESS.json
```

The first two commands compare exact output to [EXPECTED.json](EXPECTED.json)
and return `STRICT_SCREW_R5_BARRIER_PASS`, in under one second locally.
The third returns `NO_R5_MOTION` for the strict witness. No old motion
checker is imported or run. [INPUTS.json](INPUTS.json) pins three public
reference files; a repository checkout supplies those relative inputs.
[SHA256SUMS](SHA256SUMS) records this package's file hashes.

For another rational candidate, use the witness schema: one object with
`sites`, containing all 24 reference labels exactly once, each with
three-coordinate `source` and `target` lists. Coordinates must be integers
or rational strings. Site order is immaterial. The consumer checks
endpoint contraction and the two squared-distance bounds and returns
`NO_R5_MOTION` or `NOT_CERTIFIED`. The latter does not assert that a motion
exists. Input and target may be independently rotated, reflected or
translated.

Finite validation includes two scatter floors, sixteen exact constant
guards, direct polynomial expansion of the Gram determinant, three
malformed inputs, independent endpoint frames, and known R3-positive
controls outside the negative guard. The strict witness is reconstructed
from the old fixture and one exact scale factor. Polar alignment,
continuity and the universal perturbation bounds remain written
mathematics, not a proof-assistant or independent-review result.

[HANDOFF.md](HANDOFF.md) gives the reusable obstruction and its limits.
[SOURCES.md](SOURCES.md) credits the original construction, the qualitative
closure result and primary literature. The tiny strictness gap is an
exact-arithmetic control, not a numerically resolved Gaussian sign.
