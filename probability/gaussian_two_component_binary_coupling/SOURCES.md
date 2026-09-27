# Attribution, dependencies, and scope

Primary sources were checked on 27 September 2026. The Gaussian
interpolation and binary experiment arguments use classical machinery;
this packet makes no historical priority claim.

- Aishwarya--Li, [Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
  is the campaign's single problem source. Its majorisation criterion
  involves Lebesgue density values; a forward probability kernel by
  itself does not settle that criterion.
- Leskela--Vihola, [Conditional convex orders and measurable martingale
  couplings, arXiv:1404.0999](https://arxiv.org/pdf/1404.0999), Theorem 1.1
  (Strassen) and Proposition 2.3, supply the finite-first-moment coupling
  theorem and the one-dimensional convex-order characterization used in
  Section 4. Strassen's original paper is *The Existence of Probability
  Measures with Given Marginals*, Ann. Math. Statist. 36 (1965), 423--439.
  The Gaussian sign in Sections 2--3 is proved in full here.

Durable campaign dependencies, with precise roles:

- The [two-body contact transfer](../gaussian_two_body_contact_transfer/PROOF.md)
  at source commit `036e7355fd2481a562ece50be4cbab5889f41c25`, graph6570
  `bafkreid62eenvh4wovui3x5dujdjcpynmv7pv4kgi7d5b3hfkv66t624da`,
  defines the actual joint-level target. Its fixture supplies the eight
  rational centres used only for algebra controls here. The transfer is
  [independently accepted](../gaussian_two_body_contact_transfer_review2/REVIEW.md)
  at review commit `cdfe4d311485012c5d3cc9f3d2fb0a50005a6caf`, graph6574
  `bafkreihri2gpctay63kpmu6jpivr77ouhchqfaucicuqivearnvynjphjy`.
  The present proof of a binary channel does not assume a positive or
  adverse joint-level sign from that result.
- The [global endpoint criterion](../gaussian_majorisation_global_criterion/PROOF.md)
  at source commit `713e542a0bd389681a3fb4ee0c0b61a4f272f104`, graph6088
  `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`,
  remains the stronger full-question coupling obligation. This packet
  does not show that its failure probability is zero.
- The [universal-prior channel obstruction](../gaussian_markov_intertwining/PROOF.md)
  at source commit `b001598e004ba85c0934a5070f031d56c550a717`, graph6160
  `bafkreiczqvn7xhzztmvkdnlarf5iui2grf7xgjw57jp4vsz7dtieaxvieq`,
  forbids an arbitrary fixed-covariance Gaussian intertwiner uniform
  over all tested priors unless the mean map is affine (on an open
  convex domain). The present K depends on two fixed component laws;
  only their mixing weight varies. These quantifiers are compatible.

This proof does not use or extend the completed finite beta rows, scalar
replica relaxations, quartic interpolation variants, or finite-diagonal
linear programs. It addresses the fields themselves. The finite exact
checker does not validate the continuum analytic or disintegration
arguments independently. No joint-contact counterexample, full
majorisation theorem, or Kneser--Poulsen consequence is claimed.
