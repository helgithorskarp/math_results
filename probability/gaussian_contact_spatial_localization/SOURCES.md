# Sources and claim boundary

Primary literature refreshed on 27 September 2026:

- [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2):
  the named dimension-three majorisation question and Theorem 5.1's
  Gaussian-to-variable-radius Kneser--Poulsen implication. We do not claim
  a new implication or a solution of the open question.
- [Erik Carlsson--John Carlsson, Alpha shapes in kernel density estimation,
  arXiv:2303.12213v3](https://arxiv.org/html/2303.12213v3): Theorem 1(2),
  Lemma 1 and equation (3.9) give the Gaussian ball envelope and posterior
  centres. Section 3.2 samples posterior centres for finite alpha complexes;
  the introduction also discusses spatial discretization. Those ideas and
  their extension beyond finite priors are credited antecedents. The
  present bound is a deterministic uniform covering estimate tied to an
  adverse contact margin and a finite counterexample conversion. No
  priority claim for ball envelopes, posterior sampling or generic covering
  methods is made.

Durable team dependencies; exact file digests and last-change commits are
in [INPUTS.json](INPUTS.json):

- [R7 contact transfer](../gaussian_two_body_contact_transfer/PROOF.md),
  source 036e7355fd2481a562ece50be4cbab5889f41c25, graph height 6570,
  bafkreid62eenvh4wovui3x5dujdjcpynmv7pv4kgi7d5b3hfkv66t624da.
  Sections 3, 5 and 6 supply the whole-hull contraction, quantitative
  ball-to-Gaussian error and the earlier atom-dependent finite cover.
- [R2 independent acceptance](../gaussian_two_body_contact_transfer_review2/REVIEW.md),
  source cdfe4d311485012c5d3cc9f3d2fb0a50005a6caf, graph height 6574,
  bafkreihri2gpctay63kpmu6jpivr77ouhchqfaucicuqivearnvynjphjy.
  Acceptance covers the conditional transfer, not a found adverse datum.
- [R3 all-radius localization, Section 3](../gaussian_all_radius_loss_localization/PROOF.md),
  source 1104fcce0bfcf2d9cb16f70daa45c361f54c977c, graph height 6576,
  bafkreibivrqpvaay3jjrqcg3ezx4u64efeszvrtcyr6k5jtlh4lexfghqm.
  Its elementary critical-level strip lemma is used, with the proof repeated
  in the present Section 3. Neither its covariance hypothesis nor its full
  loss-relative theorem is used here.
- [R2 independent localization acceptance](../gaussian_all_radius_loss_localization_review2/REVIEW.md),
  source 24fce7dc389c0e634549ba50d12076ebde570d3a, graph height 6578,
  bafkreidli7x7h2uqouhy2hqylp3h3vo6qfjlimawtlpw5f6vhy5rc3eazq.
  The review explicitly audits the strip lemma's quantile separation,
  Lagrange coefficients, Gaussian remainder and critical-level passage.

The full problem node is height 5950,
bafkreifx5vhi7azxuu4chant6r4c7vvgjsypwdoob4ug7ea2nmzctlsrhu.
The new result improves a concrete atom/rounding bound for a conditional
adverse witness. It establishes no new positive Gaussian or ball-union
sign. The source laws need not have a finite representation, but evaluating
their posterior integrals is an external constructive obligation.
