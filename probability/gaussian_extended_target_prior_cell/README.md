# A full prior simplex with extended targets

The [proof](PROOF.md) certifies every Gaussian threshold at variance one
for a fifteen-dimensional simplex of weights on the accepted deep-flap
coordinate cell. Each of its sixteen component masses is at least
`15/256`; source and target components can be arbitrary diffuse laws in
their corresponding coordinate boxes.

The target density changes with the prior. A common supporting plane for
its hinge reduces the whole simplex to **two vertex types**, without
assuming convexity of a difference of hinges. Exact middle bounds below
`-1/256` on `[1/512,9/32]`, a new weighted radial cover, and a source-peak
bound close all thresholds.

The anchored coordinate-and-weight cell has **105 parameters** and lies
in the unchanged rational frontier. Its denominator-7104 slice contains
`3427492026504451783224489079` labelled priors; none are enumerated.
This is an author proof awaiting independent review. It extends the
[accepted equal-prior cell](../gaussian_deep_flap_cell/ACCEPTANCE.md),
not an all-variance or Kneser--Poulsen theorem. Unrestricted majorisation
and the global defect bound `D<=7/50` are unchanged.

With standard-library CPython 3.11+, run from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected: `EXTENDED_TARGET_PRIOR_CELL_PASS`. [EXPECTED.json](EXPECTED.json)
stores compact bounds and stream hashes; [INPUTS.json](INPUTS.json) pins
ten dependencies. A full run takes about four minutes and 350 MB on the
author's host. `--progress` prints bounded progress. Floating root
proposals are accepted only after exact outward exponential checks.

The universal convexity, symmetry, quadrature and tail arguments remain
written mathematics. The new certificate does not inherit independent
acceptance merely from its reviewed prerequisites. [SOURCES.md](SOURCES.md)
records those boundaries and attribution.
