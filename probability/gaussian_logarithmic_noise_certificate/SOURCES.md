# Attribution, dependencies and the remaining sign boundary

The named target is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
Their Conjecture1.1 asks for the full convex-energy comparison; Theorem1.3
proves the dimension-dependent pressure-class comparison, and Section1.3
explains the all-variance/full-energy hypotheses for geometric consequences.
Our finite-degree, high-noise result does not satisfy those KP hypotheses.

The Legendre orthogonality and integral formulas are classical, not new:
[NIST DLMF, Section18.3](https://dlmf.nist.gov/18.3) and
[Section18.10](https://dlmf.nist.gov/18.10). The proof gives the particular
reproducing bound and extrapolation calculation explicitly; the checker
also expands the Laplace integral by even cosine moments. The elementary
Chebyshev cosine coefficient and recurrence bounds are included in the proof.
Targeted live literature and repository searches did not supply a previously
stated logarithmic variance-degree theorem for this contraction problem.
This is not a historical priority determination.

Every repository file below has a byte hash and freshly resolved file commit
in [INPUTS.json](INPUTS.json). Review status is stated separately from those
byte-level pins.

- [High-noise window and interior estimate](../gaussian_majorisation_high_noise_window/PROOF.md),
  original6008 `bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q`,
  source42fef5f197d9e601db9d1f637b84c4d6215a3039.
  The signed window and normalized coarea/Abel bridge were independently
  audited in the [small-radius review](../gaussian_small_radius_defect_review_frontier/REVIEW.md),
  6301 `bafkreidb3jx7u4uxhnydsjllidgofa72hzgsstellnwkh4lrm4veeb6v7e`.
  That review expressly did not accept the separate quantitative interior
  theorem. The derivation needed here is repeated in PROOF Section2 and
  remains part of this new author's proof, not an independent review claim.

- [Exponential small-radius defect](../gaussian_majorisation_high_noise_window/SMALL_RADIUS_DEFECT.md),
  original6279 `bafkreicadnrjyx7f6nhq6ftzlthcsop7xuof7uq7zccaar7z26gdr63p3e`,
  accepted6301. The dyadic cutoff is reused. An absolute defect alone does
  not give our strictly signed cone when distance loss tends to zero.

- [R8 loss-dependent hinge modulus](../gaussian_loss_normalized_hinges/PROOF.md),
  original6325 `bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24`,
  sourcea68810063b8ad53dda046c68552a14e76f8d3f07;
  [acceptance6333](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md)
  `bafkreieyqbx7j34qcop5tdz46qgtub5jcvo3rz3cxzdc6d4uspcshm6uo4`.
  Its factor d in the tail modulus is essential. No all-radius extension
  of its strong-convexity premise is made here.

- [R3 loss-proportional paired cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
  original6364 `bafkreicuyedmct5zhkt5cxba2nkvgel3tkursxckgxcryd45ed53khps5e`,
  sourceafacddeb257993b31ee118ff92e7360a7870cbc6;
  [acceptance6380](../gaussian_loss_cubature_review2/REVIEW.md)
  `bafkreia62tjvdimerupjq35kmi27cdxsknhqy4sg6bzhoiuatovvrwdluu`.
  Its Taylor remainder and exact preservation of both marginal moments and
  d give our signed finite functional. The correct fetched review-source SHA
  is99d165ea308026e7c3241f90ac2fe984cc16fec9, as recorded by correction6382
  `bafkreid4y3p2jc6hgxotdnkxfuiraih7i3dnonaynzh7njemucyuon2mv4`;
  the discrepant longer hash in the original review body is not reused.

- [Earlier finite-Hankel/high-noise quartic theorem](../gaussian_contraction_high_noise_quartics/PROOF.md),
  original5978 `bafkreig737fhqpda2iz657ruh6clkymbesvt2a53sw4suywpqb7obwgkay`.
  Our logarithmic variance dependence improves the large-degree sufficient
  schedule and covers the whole nonnegative polynomial-curvature cone. It
  does not improve that source's much sharper degree-four variance cutoff,
  and no optimality is claimed for either schedule.

- [R8 Jackson reconstruction](../gaussian_jackson_certification/PROOF.md),
  original6398 `bafkreif2rlkhwmh3eh5s64iowgjy2anli6al5ewqppglnqqm76adex263m`.
  This supplies the current R2/R3/R8 reconstruction frontier. It is context,
  not a premise of the signed theorem here; independent acceptance is not
  assumed. The new result supplies a uniform signed finite cone rather than
  another reconstruction operator or a standalone positive cell.

The concurrently published
[R3 loss-moment middle guard](../gaussian_loss_moment_middle/PROOF.md) was
inspected before publication. It uses a covariance floor and a small ratio
of second to first pair-loss moments to sign an entire middle hinge
interval; its cubature adds ten mixed features. Our theorem has no such
covariance or loss-ratio restriction, and signs the full nonnegative
polynomial-curvature cone through a radius-dependent degree. It does not
sign the remaining hinges. The two statements have different scopes;
neither one is assumed as a premise of the other.

The finite calibration reuses the already accepted R2 deep-flap coordinates
at a smaller scale. Its established positivity is not new evidence for this
universal theorem. The production moment code extracts only the useful
marginal generating-function calculation from an unpublished R2 draft;
that draft's weaker reconstruction operator remains parked and is not
published or used here.

No claim is made about new beta strips, an unrestricted quartic inequality,
the remaining middle sign at arbitrary radius, or any new KP class. The
accepted global defect estimate and the unrestricted rational frontier remain
unchanged. Full dimension-three Gaussian majorisation remains open.
