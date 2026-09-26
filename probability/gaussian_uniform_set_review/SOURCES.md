# Sources and review boundary

* The reviewed [uniform lattice-set proof](../gaussian_uniform_set_reduction/PROOF.md)
  is by researcher 3. Commit `748304ec455b7c233da6931cbfed763105949a36`
  includes the original reduction and the subsequent interaction identity.
  Its core Theorem 1 first appeared in commit
  `15a8c5e52802c9ad14cd1a24f4cede0e2d1a1c3e`.
  The exact input is pinned in [INPUTS.json](INPUTS.json). This review accepts
  Theorem 1 and identity (12), with their stated quantifiers, without changing
  the proof. It does not claim authorship or historical novelty of them.
* Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
  arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), Conjecture 1.1.
  This remains the sole campaign problem. Its planar and pressure-class
  theorems are not used to infer the missing three-dimensional hinge sign.
* M. Kirszbraun, *Über die zusammenziehende und Lipschitzsche Transformationen*,
  Fundamenta Mathematicae 22 (1934), 77--108,
  [publisher record](https://impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/22/0/93089/uber-die-zusammenziehende-und-lipschitzsche-transformationen).
  The classical extension theorem is the explicit external premise relating
  support contractions to full-space maps. No global volume property of the
  extension is supplied or used. Other approximation and Gaussian estimates
  are derived directly in the review.
* The [isometric-reference proof](../gaussian_isometric_reference/PROOF.md),
  source `3a70618cd4611e258dcd275bdf45a139fd44e459`, was authored by this
  reviewer, researcher 5. The reduction's optional corollary invoking it is
  excluded from independent acceptance. The reference theorem's pending review
  status remains unchanged. Correcting the researcher number in the reduction's
  SOURCES.md is a bibliographic repair only.
* The earlier [shift-interaction obstruction](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md)
  distinguishes arbitrary grouped packets from identical rigid packets.
  It is context for the sign boundary, not a proof premise of the reviewed
  equivalence. Its unfavorable interaction is compensated by conditional gaps;
  the latter are exactly zero in the new reduced class.

Primary literature and bounded team source/graph context were refreshed on
26 September 2026. The later contact-flux review, cap classes and lift-regularity
boundary have their own scopes. None is an input to the accepted equivalence.
There is no claim to independently review every upstream team result.

The author checker was not imported or replayed. No test output is counted as
evidence for the universal approximation. The two commands in README verify
only this packet's integrity and the precise reviewed input. There is no
omitted numerical dataset, solver artifact or large certificate.
