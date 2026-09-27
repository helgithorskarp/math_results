# Sources, prior comparison and trust

The sole target is the full R3 majorisation problem in Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2).
No claim of resolution or historical priority is made.

## Classical geometric input

U. Brehm, [*Extensions of distance reducing mappings to piecewise congruent
mappings on R^m*](https://link.springer.com/article/10.1007/BF01917587),
J. Geometry16 (1981),187--193, is the extension theorem used by the accepted
finite-interval reduction. A. Petrunin and A. Yashinski's
[*Lectures on piecewise distance-preserving maps*](https://arxiv.org/pdf/1405.6606)
give its construction and discuss higher dimensions in the final remarks.
The papers were checked on27 September2026. No new extension theorem,
triangulation bound, or reflection-state algorithm is asserted here.

## Campaign dependencies and precursors

- R5's [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
  graph6112 `bafkreievpgikszwz2kggan4dnfbbhvtvjohiycou6xuhlsqpxjvvxrhaai`,
  source138993ba3ec2efde720c789a2a3d887c9c417c69. The whole-curve hinge
  interaction bound and remote-atom idea are prior work. The present
  construction replaces that atom by a uniformly weighted tetrahedron
  specifically to retain a covariance floor during later factorization.
- The accepted [indecomposable reduction](../gaussian_indecomposable_contractions/PROOF.md),
  graph6164 `bafkreihtkvrmyjs4cswetyjge4rpwvppjunbtmd4tnrw3o65cwvfa5wyey`,
  source4518e569424cbac04083e6cb9497cc97991cf301, and its
  [accepting review](../gaussian_indecomposable_contractions_review2/REVIEW.md),
  graph6188 `bafkreifbrvpx4z32sbzb4ipdejnfrlvdxgshekcw2xn7mcytnrutxunt54`,
  sourced853d267d429b0f502ccf9989d93a724f3b027d6. Its finite full interval,
  saturation and auxiliary positive-mass steps are used, with a pinned
  root-mass modification. None of its existing computations is replayed.
- R7's [finite-symmetry reduction](../gaussian_finite_symmetry_reduction/PROOF.md),
  graph6584 `bafkreidmmkru236kcu5scluw5jvsajb2k2536vzmblcnl7kb2anw2mp7fy`,
  source4524b3674ab752dfdf5f4cb695e68ac122798f08. It gives a complete
  compact isotropic class retaining the full supremal absolute defect.
  Its [accepting review](../gaussian_finite_symmetry_reduction_review2/REVIEW.md)
  is graph6600 `bafkreiggr2dmh2jfbb6sgdytulc7yo26rgpwmlyw37vhvljl2k3b5vq5z4`.
  It is related prior work, not an analytic premise here.
  We retain a fixed weighted root instead of symmetry, and keep its
  geometry through full-distance-interval factorization.
- R4's [endpoint-block classification](../gaussian_endpoint_block_classification/PROOF.md),
  graph6582 `bafkreiflr2ixigpozmgycnoix7k5knbijnmazeu2osk52mdzaxhml2gqti`,
  sourceca59f324d587ecdc878318b5c99c673c1f395d0b, is the predecessor.
  Its adverse gap/ordered-loss selection is elementary additive
  telescoping. The new result applies it on a full indecomposable chain
  with a covariance guard that cannot disappear. The old ten-point
  positive input is reused solely as a geometric fixture. Its
  [accepting review](../gaussian_endpoint_block_classification_review2/REVIEW.md)
  is graph6586 `bafkreieopltgzvsw3newmylow37stsfiyxvmolwwikdd2oyuupfkoafq74`.
- R3's [all-radius loss-relative localization](../gaussian_all_radius_loss_localization/PROOF.md),
  graph6576 `bafkreibivrqpvaay3jjrqcg3ezx4u64efeszvrtcyr6k5jtlh4lexfghqm`,
  source1104fcce0bfcf2d9cb16f70daa45c361f54c977c, and its
  [accepting review](../gaussian_all_radius_loss_localization_review2/REVIEW.md),
  graph6578 `bafkreidli7x7h2uqouhy2hqylp3h3vo6qfjlimawtlpw5f6vhy5rc3eazq`,
  source24fce7dc389c0e634549ba50d12076ebde570d3a. The new root inequalities
  provide actual hypotheses for its existing error schedules, at every
  chain step. No new analytic estimate or signed sample margin is claimed.

## What changes and what does not

The proposed contribution is the simultaneous complete frontier: universal
fixed tetrahedron, nonvanishing fixed masses, one fixed support ball,
permanent positive covariance, and indecomposability. The norm inequality
from the four root distances is what carries these guards through a
full interval. The adverse-gap-to-loss lower bound is independent of
the potentially enormous factorization length.

This is a concrete change to the geometric inputs required by a finite
sign oracle, not a claim that that oracle has positive output. Variance
can tend to zero. Unbounded mesh size, missing signed margins, and the
unrestricted question remain. No cap/flap catalogue, R5 barrier, reviewer
replay, or new positive Gaussian/Kneser--Poulsen class is part of the work.

`DEPENDENCIES.json` records the exact source bytes inspected. Those pins
are provenance, not independent correctness evidence. Exact rational
checks validate the compact controls and transplant hypotheses, not the
classical extension theorem, the Gaussian integral limit, or an actual
negative value. Both the new proof and its scope require independent review.
