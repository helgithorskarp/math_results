# Literature, status and dependency boundaries

Agent **six-sendov-2**, role **researcher**, 2026-09-30.
This contribution concerns quantitative first-power surplus stability
around two boundary families. Its new collapsed-branch obstruction is
specific to that branch, not a universal optimal first-power margin.

## Primary status

[Tao's August 12, 2026 primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports proofs of Sendov and Phelps--Rodriguez in all degrees.
The [accompanying Lean repository](https://github.com/teorth/sendov/blob/master/README.md)
states the full theorem and describes the formalization. These primary
statements were inspected; no external formalization was rebuilt.
The original assigned degree-nine assertion is therefore covered by the
newer primary proof report, rather than treated as our unresolved target.

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126),
Conjecture 1.2 versus Theorem 1.3 and Corollary 1.4, separates the
conjectural first-power endpoint from the proved quadratic and higher
cases. The quadratic equality class is the boundary binomial only.
Our first-power limiting class also includes \((z-a)(z+a)^8\).
At that collapsed boundary polynomial, the eight reciprocal moduli are
\(1/2\) seven times and \(9/2\) once: their sum is \(8\), while their
squared sum is \(22\). The two equality questions are therefore different.

[Tang--Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
equation (5.1) and Remark 5.1, supplies the classical reciprocal identity
and boundary half-plane argument. Complex factorization, Gauss--Lucas,
Maclaurin/Newton, elementary phase bounds, coefficient norms, integration
and Rouche are inherited tools. Their use is not claimed as new.

The required older audit remains separate:
[Meng's degree-nine claim](https://arxiv.org/abs/1705.07235) displays
v3 dated May 17, 2018, whereas
[arXiv:2609.20256](https://arxiv.org/html/2609.20256) reports the historical
degree-at-most-eight status. This is a status discrepancy, not a refutation.
No independent primary acceptance, withdrawal or refutation record for
the older claim was identified in the bounded audit. The newer all-degree
proof report covers the original assertion independently.

## Published campaign inputs

All reader links below use the default branch; verified commit identities
are recorded separately.

- [Two-family first-power boundary proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
  six-sendov-2, source 437a2d57e99a6c3b61c514b2fee2e5121062f3cc;
  graph bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa,
  height 7220. It supplies the prior boundary method and the cited sharp
  families. The fresh independent review recorded below confirms that
  previous theorem; its verdict does not cover this interior extension.
- [Effective-annulus proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md),
  six-sendov-2, source 4ef7996638ffee0f42d7780e477c2745aeac233e;
  graph bafkreigenk4drh3ixa54mwshdukdnv3xs2f7khffkpc7u2t4rfcmcq34ey,
  height 7184. It supplies the preceding signed-projection/Newton method.
  Its polar variance exclusion is not needed here.
- [Independent unit-circle coefficient refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_boundary_stability_review2/REFINEMENT.md),
  six-reviewer-2, source b75eb0b0235ac9201d8fab7b47433b75df0deeff;
  graph bafkreibn74ptvpnv3pcvw2t74nqwnqpka3trpahj2tfknebxfmth2prowa,
  height 7162. The coefficient mechanism is generalized through projection
  of the marked interior root; its paired-coefficient bound is rederived.
- [Boundary first-power classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
  six-sendov-1, source 728857924504f28020dea5de6590ae3458b7bc90;
  graph bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue,
  height 7152, sections 4 and 7. Classification is known context, also
  recovered at zero parameter here.

The independently published
[variance-gap lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_review2/SATURATION.md),
source 0a6484e56add69854d7016bcefa211aa250afdf1, explains the
collapsed obstruction to a single-family variance conclusion. The present
proof retains that branch instead of assuming a gap. This source is
methodological context, not a new independent review of the present proof.

The fresh [independent two-family boundary review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_review2/README.md),
source a55f2b614c6cab5817f5266274514f725779b00e,
graph bafkreieerxdxucvj5ooynp66r6uxdcxxfrg3j36jtxkmtwt2sxvgdfclfq,
height 7248, confirms the preceding boundary theorem with high confidence.
Its [refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_review2/REFINEMENT.md)
extends boundary radial interpolation to the full small-quadratic-deficit
range. That result retains a boundary marked root. Its discussion expressly
leaves the signed interior two-family bridge as further work; it is neither
a duplicate nor an independent review of the present interior statement.

[The independent effective-annulus review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_review3/README.md),
source 29c68171cdaf7f10dba45be563df63c07f631040,
graph bafkreifhsmxp3bhwlvk4t5xt2o3l5xkgaep2whtnlp6g4j5cgavsel2piq,
height 7218, confirms the previous effective statement and gives a wider
explicit annulus. It expressly leaves nonzero-surplus two-family
stability and a larger effective slope as further work. Its verdict does
not extend to this new theorem.

## Prior-art limit and collaboration boundary

Current bounded primary searches and the pertinent committed graph/source
refresh found no duplicate of the exact interior-surplus statement or
branch-specific coefficient (5). This is not historical-priority evidence.
The older quantitative Sendov annulus literature concerns existence of
one nearby critical point under the original Sendov distance objective.
In particular Chijiwa, Hiroshima Math. J. 41 (2011), 235--273,
DOI 10.32917/hmj/1314204564, still needs full-text comparison: the inspected
publisher request returned a challenge page, not the mathematical article.
No exclusion of that inaccessible source is claimed. The scoped primary
Kasmalkar comparison in the independent review concerns pointwise-distance
hypotheses, not this independent aggregate upper-surplus condition.

The complementary lane's
[collinear and reciprocal-cone proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
source 177818bdbd7e23f16ec46bacfc3077d7a22a8aca,
graph bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4,
height 7212, concerns first-power validity and angular control. The fresh
[independent collinear review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
source 18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d,
graph bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4,
height 7244, confirms it and proves a quadratic phase criterion.
These are context, not premises of our theorem. The necessary bound (6)
is useful input for that lane's local coercivity calculations. General
complex interior phase and the middle annulus remain its separate frontier.
