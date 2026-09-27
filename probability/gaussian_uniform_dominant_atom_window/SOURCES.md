# Sources, dependencies, and the uniformity gain

The sole problem source is G. Aishwarya and D. Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The full bounded-law dimension-three majorisation question is unresolved.
This packet claims a finite threshold window, not a resolution.

- The [replica/Hankel proof](../gaussian_majorisation_hankel_transport/PROOF.md),
  original5962, `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`,
  supplies the exact moment identity at arbitrary support radius. This
  identity is the starting point for the local two-primitive inversion.
- The [high-noise coarea proof](../gaussian_majorisation_high_noise_window/PROOF.md),
  original6008, `bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q`,
  introduced the weighted radial coarea and half-derivative mechanism.
  Its Theorem A and normalization were independently accepted in
  [review6301](../gaussian_small_radius_defect_review_frontier/REVIEW.md),
  `bafkreidb3jx7u4uxhnydsjllidgofa72hzgsstellnwkh4lrm4veeb6v7e`.
  The global radius hypothesis from that theorem is not assumed here.
- The [loss-proportional continuity proof](../gaussian_loss_normalized_hinges/PROOF.md),
  original6325, `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`,
  source `a68810063b8ad53dda046c68552a14e76f8d3f07`,
  retained the loss factor in derivatives of the actual coarea curve.
  Its first-derivative identity is used here. The present result replaces
  an unsigned interpolation budget by an actual positive angular estimate
  in a uniformly specified dominant-prior region.
  The source estimates and the conditional certificate implications were
  independently accepted by [review6333](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md),
  `bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4`.
  That review does not cover the present new local inversion or sign.
- The [small-mass theorem](../gaussian_majorisation_small_mass/PROOF.md),
  original5984, `bafkreihtnp3ptickdr4nhikxkarcr3v4uwocvhde5lcj3mx2fhmk7b7jge`,
  source `5f0f1852d71dc61b7edfa1871cbc6a06673a4c27`,
  already proved positivity above any fixed threshold floor for fixed
  rare law, map and variance, and a logarithmic-square escape window.
  Its Section 1 explicitly excludes uniformity over those data. Its
  spherical second-variation argument identifies the zero-radial-loss
  case. We credit those facts; the present contribution is the explicit
  budget uniform over all radius-bounded packets and contractions, with
  a margin normalized by the actual pair loss.

The finite certificate context is R3's
[paired cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
and [signed endpoints](../gaussian_prior_localization/SIGNED_ENDPOINTS.md),
originals6212 and6287:
`bafkreia425hkp6pibvmb4dqein5ybdlxy4kkeywfmuqd3gd6mkptjll4rq` and
`bafkreidzywknhi3khr65enmniumcplrqltn7r6igpo3degnh6unhijkii4`.
Our middle certificate does not require these reductions for its proof,
does not cover all their cells, and supplies no automatic overlap with
their lower-threshold cutoff. R2's separate
[rational cell](../gaussian_frontier_middle_cell/PROOF.md), original6311,
`bafkreif25s5jph7vfopsnlkpodlal5ng56tfzsyomy62pktnhhqwhytchm`, already has a
full threshold cover for its specified weights and boxes; it is not the
result proved or enlarged in this packet.

At the prepublication refresh, R3's [prior/measure cell](../gaussian_frontier_prior_cell/PROOF.md),
original6335, `bafkreidsn7klheuvguoiqbidjjinu4xj56lltx6cjybhly7oju45r5fbva`,
had extended that cell to a six-dimensional prior simplex with six positive
outer mass floors. R2's [deep-flap cell](../gaussian_deep_flap_cell/PROOF.md),
original6341, `bafkreidewnncabhfdz4rugy7wqmrcl6hnuyqyj6d2vbehj7vdji3mkdt7m`,
gave a separate all-threshold certificate on a sixteen-site coordinate box.
Those are distinct regions and are not used in this proof. R6's
[convex-core theorem](../gaussian_radial_contractions/CONVEX_CORES.md),
original6331, `bafkreifktf3exjltqmj5gnt5wvhpqe2za3cbb7rkdnlt3ha774is52k2j4`,
instead gives all-variance majorisation and both Kneser--Poulsen inequalities
for its specified maps. No containment in or exclusion from that entire
geometric class is asserted here.

The [scalar-defect theorem](../gaussian_majorisation_scalar_defect/PROOF.md)
is used only to explain the rank-six control's exclusion of that specific
sufficient criterion. No classification of all positive map classes is
claimed. The finite contraction itself is checked directly; a global
extension uses the usual Kirszbraun premise when that formulation is desired.

All of these are durable team sources. Their status must not be confused
with external peer review. The new mathematical argument remains an author
proof awaiting independent review. The exact checker is supplementary,
requires no private ledger or large artifact, and does not formalize
Gaussian integration, continuum quantifiers, coarea or polynomial-moment
uniqueness. No historical priority beyond the inspected sources is asserted.
