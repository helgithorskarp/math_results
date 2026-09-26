# Sources, dependencies, and scope

1. Gautam Aishwarya and Dongbin Li,
   [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
   arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), 13 September 2026.
   This is the sole problem source. Its established one-dimensional comparison
   is used for the endpoint statement. The Gaussian replica identity, the
   standard lift, and Gaussian marginalisation are prior work.
2. Daniel Azagra, Erwan Le Gruyer, and Carlos Mudarra,
   [Kirszbraun's theorem via an explicit formula,
   arXiv:1810.10288v3](https://arxiv.org/abs/1810.10288v3).
   The general encoding lemma uses the classical Hilbert-space Lipschitz
   extension theorem. The explicit certified construction instead has its
   own globally defined coordinatewise piecewise-linear extension.
3. Team B analytic lane,
   [Exact Hankel certificates and aligned common-noise transport obstruction](../gaussian_majorisation_hankel_transport/PROOF.md),
   graph `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`,
   source commit `6f51c67737051a61290c070c9fb960e1da83b75b`.
   This supplies the integrated criterion and the existing rational bounds
   implementation. Its artificial Dirac-measure obstruction did not show
   failure for a measure actually arising from a contraction. The present
   result addresses admissible *instantaneous* measures; it does not refute
   the integrated conjecture.
4. Team B geometric lane,
   [Paired-rank reduction and half-order obstruction](../gaussian_majorisation_rank_abel/PROOF.md),
   graph `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
   Its retained half-order comparison and cancellation obstruction concern
   the endpoint difference. The result here identifies a different failure:
   inverse-marginalisation energy need not be monotone along an actual lift.
5. Team B adversarial lane,
   [Sharp relative Gaussian moment gaps](../gaussian_contraction_moment_gaps/PROOF.md),
   graph `bafkreibvtztcjy7u65knymr77p6txb2g2cteukcfsb6c5o7yh5lhi4ymna`.
   The positive sample-variance representation remains valid in this example.
   Its scalar monotonicity does not assert the false Hankel condition tested
   here. This pass did not duplicate endpoint cloud searches.
6. Team B functional bridge lane,
   [PC2 and entropy bridge obstruction](../gaussian_majorisation_bridge_barrier/PROOF.md),
   graph `bafkreiahtwafewpeuhfbid57md6jtcbwrxn222ryy53ypafsmr4maoed3e`.
   Its counterexamples do not have contracting inputs. In contrast, the
   present pointwise obstruction uses an explicit contraction, but concerns
   an intermediate six-dimensional test rather than endpoint majorisation.
7. Team B's new prepublication refresh result,
   [Convex quartic comparisons at large variance](../gaussian_contraction_high_noise_quartics/PROOF.md),
   graph `bafkreig737fhqpda2iz657ruh6clkymbesvt2a53sw4suywpqb7obwgkay`,
   committed at height `5978`. It proves endpoint comparisons for every convex
   quartic when `s >= (17/15) R^2`, and for every fixed Hankel level at an
   explicit sufficiently large variance. Our input radius is enormous at
   variance one, so the new example is outside that sufficient regime.
   More fundamentally, its endpoint order holds anyway; the present failure
   concerns a pointwise lift inequality. The new result is complementary,
   not contradicted or duplicated.

The preceding covariance-free rigidity proof remains preserved and
independently accepted:
[proof](../gaussian_contraction_covariance_free/PROOF.md) and
[audit](../gaussian_majorisation_bridge_barrier/AUDIT.md), graph acceptance
`bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`.
It provides distance-to-isometry control, not the false instantaneous sign.

The original paper and current team sources were inspected before publication.
The final substantive refresh included graph height `5979` and the new
high-variance proof above. The adversarial lane's ongoing symmetric-flap
quartic certificate was also noted as in progress; no uncommitted result is
used as a premise here.
No independent mathematical review of the new proof is claimed. The novelty
claim is restricted to this explicit failed bridge and its encoding mechanism;
standard Gaussian integration, tensorisation, and extension results are not
claimed as new. No Kneser--Poulsen consequence is obtained here.
