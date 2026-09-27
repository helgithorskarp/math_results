# Sources, scope and trust

The named problem is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1 in dimension three. The primary manuscript was checked live
on 27 September 2026. It establishes full comparison in dimensions at most
two and higher-dimensional partial energy comparisons; the full R3 target
remains open. Nothing here supplies the small-variance limit needed for a
new Kneser--Poulsen consequence.

The required accepted analytic input is the
[spherical-gap endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
source `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`, graph6032
`bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`, with
[independent acceptance](../gaussian_majorisation_eventual_endpoint_review2/README.md),
source `c750676fd6e164db43c0891c0093ebed2a49c356`, graph6048
`bafkreih6v5ttck5sx6ivw5xrvn7oqzvmuqylrfyohzvpek3k7bm6ohbbli`.
The review directly audits both consumed analytic inputs, the
[spherical-tail estimate](../gaussian_majorisation_spherical_tail/PROOF.md)
and [high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md).
They are not re-audited by this packet's exact checker.

The earlier [dilated-martingale certificate](../gaussian_dilated_martingale_certificate/PROOF.md),
source `63f42fa6f5173c69391c08b40af53a470663221a`, graph6464, supplies
the immediately preceding frontier. Its elementary source-scatter estimate
is restated in full here. Its independent acceptance was pending at the
entry refresh. The new proof replaces its extra coupling premise by a
uniform pairwise Lipschitz condition and subsumes its covariance/damping
corollary, not its whole general martingale theorem. A mid-pass refresh
then found [independent acceptance at6480](../gaussian_dilated_martingale_review/REVIEW.md),
review source `2f8e01ccd26751dade844412ed1f298021e68607`. That acceptance
does not extend to this new spherical comparison without a new review.

The [same-pair cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
source `7c5bd936a9f22e1eeb03ac2775ee711295458a8c`, graph6212/6218,
and [loss cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
source `afacddeb257993b31ee118ff92e7360a7870cbc6`, graph6364/6380,
give the accepted finite-atomic handoff. Seven consumed or closely
related source files are content-pinned in [INPUTS.json](INPUTS.json).

The earlier [asymmetric atomic bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md),
graph6058, already showed that covariance eigenvalues obstruct martingale
witnesses after arbitrary independent endpoint isometries. The thin-source
control uses that same elementary necessary condition; it is not a new
obstruction method. The [rank-six conditional-kernel obstruction](../gaussian_conditional_kernel_obstruction/PROOF.md)
at6267/6289 remains separate from the spherical comparison proved here.

The campaign refresh records independent acceptance of the all-radius
covariance-boundary result6454/6466, the moving small-loss defect6450/6460
and complete beta row6452/6470. The meridian theorem6468 is now accepted6474;
Coxeter6462 and screw-motion6456 have different geometric hypotheses.
The new two-body screw obstruction6472 and beta-row-twelve supplement6476
remain at their own review status. None is a premise here. R7's latest
search report supplied no rigorous negative. Prior accepted middle,
modulus and zero-loss results are preserved.

R3's concurrent [endpoint-join obstruction](../gaussian_endpoint_join_obstruction/PROOF.md),
source `e3503fef13c51da2b8da4f4d44337c6c75b163d7`, graph6478, rules out
joining its accepted tiny-loss window with the existing mass/mean-support
tail schedule. The present spherical gap does not use that cloud schedule,
but its strong-contraction high-variance family is also disjoint from that
normalized small-loss slab. The algebraic compatibility check in HANDOFF
prevents reading this theorem as a repair of the blocked join.

The final source refresh also found R8's
[uniform small-target theorem](../gaussian_uniform_small_target/PROOF.md),
source `da4a4317929a40c2d60453d1ac7309a2408a2c9c`.
It allows arbitrary endpoint laws at every specified variance, assuming a
positive source covariance floor and a much smaller variance-dependent
target radius. The current theorem instead permits all source covariances
and all maps with a fixed global Lipschitz bound, at the displayed large
variances. Its frame argument and sufficient condition differ from R8's
directional-mass tail and point-target perturbation. Neither theorem is
claimed to subsume the other's full statement.

Symmetrization, log/cosh convexity, rotation invariance, Jensen, Gaussian
translation invariance and Kirszbraun extension are classical tools. A
bounded graph and source search found no prior statement of the uniform
spherical bound in this packet; historical priority has not been established.
The finite folded calibration is already positive by known low-rank
compositions and is included only to verify a strict extension of certificate
scope. No new example classification is claimed.

Code guarantees exact finite pair inequalities, moment/radius reconstruction,
variance budgets, covariance separation and provenance. It does not prove
the universal frame integration or the imported Gaussian endpoint by formal
verification. No solver, numerical quadrature, floating-point sign, private
dataset or omitted large certificate is needed.
