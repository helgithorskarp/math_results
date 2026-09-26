# Sources and mathematical scope

The sole problem source is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, 13 September 2026; checked live on 26 September 2026.
Conjecture 1.1 asks for Gaussian density majorisation under every
1-Lipschitz map. Theorem 1.2 settles dimension two; the full three-dimensional
case is the shared target. The paper also supplies context for the classical
Kirszbraun extension theorem used to turn a finite contraction into a global map.

## Prior results used or tested

1. [Simplicial-cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md),
   researcher 7, source commit
   `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`.
   Graph `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`,
   committed at height 6042.
   PROOF.md SHA256:
   `6495916425b70062986e55beef5e472f4d2deacfe93bd46f92ea365521713842`.
   Its Theorem D already proves the anchored nine-point map has no continuous
   contraction in five dimensions. We reproduce that short obstruction and
   use its general simplicial-cone theorem only for the restricted minimality
   observation. Neither geometric result is claimed anew.

2. [Common-target convex decomposition](../gaussian_majorisation_common_target/PROOF.md),
   researcher 8, source commit
   `3ad6ed0be174d1292b250efcad734d03eed01af5`.
   Graph `bafkreiefowbrpgnu2cjyyuyig4y2gzk5zdchubp3xqpcgu2rzzpy5fe25m`,
   committed at height 6052.
   PROOF.md SHA256:
   `9dd5d85334d1c8cc6b574c79fef16380fa5716f8a3cf7d8d98b3ccca7f5e375c`.
   Theorem B proves injective finite targets give no enlargement by exact
   deterministic common-output mixtures, and explicitly applies it to the
   binary-weighted nine-point map. This publication arrived during our final
   refresh and was read before publication. Our Lemma 1 credits and repeats
   it; the new result is the quantitative approximate-output obstruction and
   the simultaneous covariance obstruction for an open set of asymmetric
   weights. The positive tetrahedral-ray theorem merges twelve ray atoms to
   six and is not contradicted.

3. [Eventual Gaussian majorisation endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
   researcher 5, source commit
   `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`.
   Graph `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`,
   committed at height 6032.
   PROOF.md SHA256:
   `9adbd6c07b271a12252b13c35d76835a2d6edc0592f3dd7285a2d950c9ba330f`.
   Corollary 3 gives a sufficient martingale convex-order criterion after
   separate isometries. Our covariance certificate excludes that hypothesis
   for the displayed family. It does not refute the corollary or decide its
   more general spherical-gap criterion. The endpoint subsequently received
   an [independent accepting review](../gaussian_majorisation_eventual_endpoint_review2/README.md)
   in commit `c750676fd6e164db43c0891c0093ebed2a49c356`; that review is not
   a review of the present packet.

4. [Rank-five Gaussian cancellation](../gaussian_majorisation_rank_abel/PROOF.md),
   researcher 6, source commit
   `f7c122d6a5ade217930d63da27e67f9a9e55a539`;
   graph `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
   This gives the standard paired-rank lifting comparison. The rank-five
   permutation attaining our mass separation is a genuinely available
   comparison map, not merely a formal mass permutation.

The covariances, Sylvester inertia test, eigenvalue min-max principle,
and strict-convexity identity are standard. No novelty is claimed for those
tools. The construction uses them to produce an exact simultaneous obstruction
with explicit open weight range and approximate-output separation. No search
has established historical priority for an asymmetric nine-atom example.

The full Gaussian inequality for the example remains undecided. No finite
moment check is a premise, and no new ball-volume comparison follows here.
The proof is an author proof awaiting independent review, not a formalization.
