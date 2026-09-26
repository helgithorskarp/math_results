# Reproduction and evidence boundary

From the repository root:

```sh
python3 probability/gaussian_flap_selector_motion/verify.py
python3 -O probability/gaussian_flap_selector_motion/verify.py
python3 probability/gaussian_flap_selector_motion/verify.py --emit
```

The first two commands recompute all finite controls and require exact
entry-by-entry equality with [EXPECTED.json](EXPECTED.json). The third emits
the deterministic JSON. Invalid arguments and any failed check exit nonzero.
The code uses explicit exceptions, so optimization does not disable checks.
Python 3.11.2 and 3.12.14 were used; there are no third-party dependencies.

Expected ordinary output:

```text
PASS: 32 new sinkless motions + 32 prior sink motions cover all selectors.
PASS: 1440 formal distance pairs, 36 projection checks, 360 endpoint pairs.
PASS: exact identities, common-target/radius controls, full-map rejection.
```

The checker establishes these finite facts:

- In each of the 32 sinkless tournaments, it selects an actual vertex of
  outdegree one and checks all 45 label-pair distance expressions. All 44
  exceptional pairs encountered have exactly the required h_k reserve.
- Direct formal Gram expansion agrees with the displayed distance formulas
  and with a separate physical-coordinate expansion of both endpoints.
- Nine polynomial identities check the norm preservation, mixed Gram
  preservation, concavity calculation, delta identity and positive margin.
- Three rational fixtures, including a regular and two asymmetric shapes,
  check all twelve ordered complementary-plane projections and all 120
  endpoint distances each. Projections and distances are computed directly
  in Fraction coordinates rather than read from the proof's Gram formulas.
- An exact asymmetric selector mixture, with zero masses and deterministic
  choices included, preserves every opposite-pair target mass.
- Max/min radius controls cover zero radii, ties and strict orders.
- For every new selector motion, adding the full-family common-head pair
  produces a varying Gram entry with no contraction reserve. This rejects
  using the new motion directly on all sixteen labels.

The 32 selectors with a sink use the cited prior proof, recalled in
Section 5 of [PROOF.md](PROOF.md). The small enumeration does not replace
the elementary argument that every sinkless four-vertex tournament has
a vertex of outdegree one. No classification search or imported certificate
is required for the new theorem.

The checker's sparse polynomial arithmetic and rational coordinate
calculations are exact Python code, not a proof assistant. They do not
independently establish the universal analytic inference, the external
Aishwarya--Li or Bezdek--Connelly theorems, or the mathematical novelty of
the result. The written proof supplies these bridges. No Gaussian integral,
floating-point sign, external solver or sampled motion is used as a proof.

The compact expected file and its hash are recorded in
[SHA256SUMS](SHA256SUMS). No data download or omitted large artifact is needed.
