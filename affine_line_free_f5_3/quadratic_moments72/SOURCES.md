# Dependencies and scope

The named objective is exact `r_5(F_5^3)`. This is Team A researcher 3's
algebraic route. The primary method is centered finite-field moments and
quadratic-form geometry; standard-library exact code audits the finite
calculations.

## Mathematical dependencies

* [Global low-plane reduction](../low_planes72/README.md):
  `bafkreifb7i4346rrz2c5ch5vhs4odx3n57xijazwl6jrgjhdmmijzthaqy`.
  We use the planar upper bound 16 and exclusion of five collinear
  low-plane normals. Its complete original verifier passed locally.
* [No eight-point planes](../no_eight_planes72/THEOREM.md):
  `bafkreiauyfcdpuccibdqvyu6fmaabice6pjk5es4f3pnlwenisiaddyxuy`, h5960.
  This supplies `a_8=0`. Its 1,252 checked lifting proofs, and its
  dependency on the earlier 164 two-eight-plane proofs, are inherited
  premises, not newly reproduced or independently reviewed here.
* [Nine-plane frame](../nine_plane_frame72/THEOREM.md):
  `bafkreidz24r5ootmcelvbeuxsl3sp7ota4ycla343hkjgigmtl6bzl7nn4`, h5954.
  We use `3a_8+a_9>=11` and the BBB normalization. Its exact original
  verifier passed locally. Together with the previous item it gives
  `a_9>=11`.
* [Upper bound 72](../upper_bound72.md):
  `bafkreigdcleaywkrwivj7mewtq4lir55ort2jlkblt6a72m5j5bskscdjq`.
  This supplies the numerical frontier, not a premise of the
  conditional theorem at size 72.

The prepublication refresh supplied the stronger no-eight-plane theorem.
The final proof uses that durable result; intermediate counting
certificates made unnecessary by it are omitted. The new content is the
moment-class exclusion and the dual geometric restrictions, not a claim
to the prior weighted inequality or no-eight-plane exclusion.

## Primary sources inspected live on 2026-09-26

* C. Elsholtz et al., *Maximal line-free sets in F_p^n*, Periodica
  Mathematica Hungarica 90 (2025), 7–21,
  [arXiv:2310.03382v2](https://arxiv.org/html/2310.03382v2),
  [DOI](https://doi.org/10.1007/s10998-024-00617-x).
  This supplies the recognizable extremal problem, prior 70-point
  construction and published upper bound 73. Its incidence framework is
  antecedent work.
* J. Führer and V. Taranchuk, *Large line-free sets and their applications*,
  [arXiv:2403.18611v2](https://arxiv.org/html/2403.18611v2).
  This provides current polynomial-construction context; its general
  line-evasive-set construction is not a premise of this proof.
* S. Kurz, I. Landjev and A. Rousseva, *Classification of (3 mod 5) arcs
  in PG(3,5)*,
  [arXiv:2108.04871v2](https://arxiv.org/abs/2108.04871v2).
  Its classification enters earlier campaign upper-bound work; it is not
  directly used by the centered-moment argument.

No matching moment-class exclusion or associated normal-configuration
theorem was found in the targeted primary search or relevant committed
graph. This is bounded, search-relative novelty evidence, not a priority
claim. Finite-field diagonalization, moment identities and conic polarity
are standard ingredients. The proof and checks are author evidence, not
an independent review or proof-assistant formalization.
