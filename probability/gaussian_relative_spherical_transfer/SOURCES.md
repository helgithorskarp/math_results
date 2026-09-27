# Dependencies and scope

Sole problem source: G. Aishwarya and D. Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2). The unrestricted
bounded-law dimension-three majorisation question remains open.

- The [spherical-tail theorem](../gaussian_majorisation_spherical_tail/PROOF.md),
  original6002, `bafkreiakfdyplrgs5zveoa2ocaggbrq4ptyrkfdq5efhatguxxntp7u7pi`,
  source `740f95368f291816672c96ae1e71a06a9186519d`, gives the absolute
  approximation error and identifies its limit. That limit identification
  is used here after a separate estimate retaining the actual pair loss.
- The [coarea/high-noise theorem](../gaussian_majorisation_high_noise_window/PROOF.md),
  original6008, `bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q`,
  gives the six-dimensional Abel representation and the signed upper range.
  [Review6301](../gaussian_small_radius_defect_review_frontier/REVIEW.md),
  `bafkreidb3jx7u4uxhnydsjllidgofa72hzgsstellnwkh4lrm4veeb6v7e`, accepted
  that normalization and Theorem A. No use is made of unreviewed Theorems B
  or C from that older packet.
- The [loss-normalized continuity proof](../gaussian_loss_normalized_hinges/PROOF.md),
  original6325, `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`,
  source `a68810063b8ad53dda046c68552a14e76f8d3f07`, provides the modal
  derivative bound used in equation (22). Its quantitative estimates were
  independently accepted by [review6333](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md),
  `bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4`.
- The [replica/Hankel identity](../gaussian_majorisation_hankel_transport/PROOF.md),
  original5962, `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`,
  underlies the coarea normalization and the zero-loss conclusion. The
  present proof always retains integration over the entire interpolation.

The [eventual-endpoint theorem](../gaussian_majorisation_eventual_endpoint/PROOF.md),
original6032, `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`,
source `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`, already converts a
uniform positive spherical gap on the full parameter ray into all-threshold
majorisation at high variance. We do not claim that implication as new.
The new bound keeps the loss factor on a compact parameter interval; a
loss-normalized margin then yields a variance budget independent of that
loss. Its separate tail premise must actually overlap. It does not improve
the older absolute error uniformly at all spherical parameters.

The [dominant-atom middle theorem](../gaussian_uniform_dominant_atom_window/PROOF.md),
original6349, `bafkreihlsbbnbcpgyx5aelqr5mnh7tozv4amt7f5qmkpqrhxeqd4yde32m`,
source `a86e9ef2f7a4a3951e8d2214c2c4a52b9bf045d0`, is preserved. Its actual
unit-variance sign uses a dominant mass; the present error estimate works
for arbitrary priors under a high-variance radius condition, and requires
a spherical sign premise for a sign conclusion. Neither result is being
silently substituted for the other's hypotheses.

The [exposed-edge tail certificate](../gaussian_exposed_edge_tail/PROOF.md),
original6351, `bafkreibyr7gg4woewmiwtysdpppsv4dvxkmwkwh2wgyteerkv4uhcds65i`,
and the [compact frontier endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md)
are potential tail inputs. No overlap with them is established here.
R2's [deep-flap cell](../gaussian_deep_flap_cell/PROOF.md) and R3's
[prior/measure cell](../gaussian_frontier_prior_cell/PROOF.md) have separate
actual sign covers; this packet neither recertifies nor enlarges those cells.
R7's [signed-radial comparison](../gaussian_signed_radial_tail_exclusion/PROOF.md)
supplies a spherical sign on its class, not automatically the uniform
margin and overlapping physical tail required here.

At the prepublication refresh, R3's [loss-proportional cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
original6364, `bafkreicuyedmct5zhkt5cxba2nkvgel3tkursxckgxcryd45ed53khps5e`,
supplied a complementary approximation preserving D exactly. It is not a
premise of this proof. Its absolute-hinge error cannot be used as an error
for B_s without division by `4pi lambda s^2 b_s`; the present theorem uses
that relative normalization throughout.

The new proof remains an unformalized author proof. Acceptance of its older
dependencies is not a review of the new radial comparison or relative error.
The exact standard-library checker is supplementary. It needs no private
ledger, numerical quadrature, external solver, or large dataset. No historical
priority beyond the inspected sources is asserted.
