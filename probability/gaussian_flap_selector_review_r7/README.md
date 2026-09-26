# Counterexample-lane review of the full flap theorem

**Accepted in scope:** researcher 4's full Gaussian majorisation theorem
for the interior-orthocenter, depth-one tetrahedral flap family, with all
weights, all variances, and both arbitrary-radius ball-volume inequalities.
The unrestricted R3 question remains open.

[REVIEW.md](REVIEW.md) checks the new selector motion and gives a factored
positive certificate for its sole exceptional distance derivative. This
retires the entire orthocentric depth-one counterexample family, including
both templates isolated by the earlier R7 reduction.

This is independent team-agent review of the new motion. The reviewer
authored its upstream basis motion and selector reduction; that relationship
and the subsumed unpublished partial exploration are disclosed. The author's
checker and expected record were not read, imported or executed.

From the repository root, with standard-library Python 3.11 or 3.12:

```sh
python3 probability/gaussian_flap_selector_review_r7/verify.py
python3 -O probability/gaussian_flap_selector_review_r7/verify.py
```

The expected status is `R7_SELECTOR_MOTION_REVIEW_EXACT_CHECKS_PASS`.
The compact [EXPECTED.json](EXPECTED.json) is regenerated with `--write`.
Normal CPython 3.11.2 and optimized CPython 3.12.14 checks agree: five
polynomial identities, 72 eligible choices over all 32 sinkless tournaments,
2,025 exact pair derivatives, and nine rejected full-family motion extensions.
Three deliberate formula changes were also rejected. Measured runs took
nine and seven seconds, using under 21 MiB peak memory.
Checks use exact rational coordinates and algebraic extensions, with no
numerical integral, float, solver or external package. The written proof
and cited Gaussian/volume theorems remain explicit trust boundaries.

Reviewed original: [PROOF.md](../gaussian_flap_selector_motion/PROOF.md),
commit `19d42da48e5262580c4178c47a5937cbfe39f1ff`.
[INPUTS.json](INPUTS.json) pins the reviewed proof and upstream source bytes.
This is not external human peer review, formalization, or a priority claim.
