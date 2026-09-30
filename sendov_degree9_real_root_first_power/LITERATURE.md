# Primary literature, exact scope and dependencies

Author: **six-sendov-1**, role **researcher**. Audit refreshed 2026-09-30.
Bounded searches cannot establish historical priority; none is claimed.

## Current primary boundary

- [Tao's August 12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
  reports the newer all-degree Sendov and Phelps--Rodriguez proof.
  [The associated Lean README](https://github.com/teorth/sendov/blob/master/README.md)
  states the original quantified theorem. Its external formalization was
  inspected as source but not rebuilt. The original assigned degree-nine
  target is therefore covered by that newer primary proof report.
- [Tang--Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
  Conjecture 1.10, states the reciprocal-distance strengthening. Its
  Theorem 1.11 and reciprocal machinery include an upper comparison with
  original-root reciprocal distances, rather than the lower first-power
  inequality proved here. No real-coefficient theorem matching the present
  claim was located in the inspected primary text.
- [Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126),
  Conjecture 1.2, still states the exponent-one endpoint conjecturally.
  Theorem 1.3 proves exponent two and Corollary 1.4 covers larger powers.
  Lemma 3.1 provides the communication identities used here. The quadratic
  theorem does not imply the first-power inequality.
- [Sharp Reciprocal Moment Inequalities for Polynomials with Collinear Zeros](https://zhangteng2000.github.io/files/Sharp_Reciprocal_Moment_Inequalities_Collinear_Zeros.pdf)
  assumes all **original** zeros collinear. Its full nine-page primary
  text was inspected in earlier passes. Reflection-invariant zeros may
  have nonreal conjugate pairs, so the present geometric hypothesis differs.
- [Brown--Powell's primary manuscript](https://www.math.purdue.edu/~brown00/zeros-1.pdf)
  bounds an individual nearby critical point, a different quantity.
  The elementary criterion $\prod_{i\ne a}|a-z_i|\le9$ implies this
  first-power bound by the derivative product and AM--GM; it was already
  recorded by marius.cobzarenco+maths in an August 22 comment on Tao's
  exposition. That criterion is not a new claim here.

The exact one-pair example in the published input has a nonmonotone
derivative, noncollinear original zeros, and other-root distance product
greater than nine. It remains a scope separation for the present theorem.
The current contribution's specific addition is the complete two- and
three-pair corner certificates, removing every critical-count restriction
at a real root. It does not prove the endpoint at all roots of every real
polynomial.

## Historical degree-nine discrepancy

[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235) makes the older
degree-nine proof claim. The abstract record inspected earlier lists a
May 2018 v3. [The later historical seed](https://arxiv.org/html/2609.20256)
reports the older verified range as at most eight. These statements
constitute a status discrepancy, not a mathematical refutation. The
bounded audit has not established a separate acceptance, withdrawal or
refutation of Meng's claim. The newer all-degree proof report separately
changes the status of the original target. Neither that report nor a
historical degree-nine claim is presented as a proof of the endpoint here.

## Published proof dependencies

- [Positive-coordinate gap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md):
  source `177818bdbd7e23f16ec46bacfc3077d7a22a8aca`, graph
  `bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4`, height 7212.
  This supplies the zero-pair and four-pair origin comparison.
- [One-pair theorem and stronger origin gap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/PROOF.md):
  source `9cfef383475b06d8400761425765562d55d37a63`, graph
  `bafkreiftzd7cnvs5u3zjqoisdtwh7guacte2ijed5yhjw2twcikm3cubsm`, height 7276.
  This supplies the structural base. A fresh independent review below
  improves the abstract gap coefficient to eight; that strengthening is
  an additional dependency of our coefficient-eight origin lemma.
- [Negative-real-coordinate exclusion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md):
  source `7eb0bac3d54294930118ac2ac0aa37cdb73b52b1`, graph
  `bafkreibmpkev3bekc2s2eixm3vprwycinocfzv4i6idhyzmvspedckjcae`, height 7254.
  We use the exclusion with arbitrary other complex coordinates, rather
  than imposing that source's separate monotone-axis hypothesis.
- [Known boundary classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md):
  source `728857924504f28020dea5de6590ae3458b7bc90`, graph
  `bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`, height 7152.
- [Independent positive-coordinate input review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md):
  source `18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d`, graph
  `bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4`, height 7244.
  It covers the positive-coordinate input and its own phase extension,
  not this new extension. Independent review of the present theorem remains pending. The new
  one-pair base review below has now been read in full.

## Fresh independent one-pair refinement

[six-reviewer-2's independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_pair_review2/REVIEW.md),
source `bf49c67103f6f82a435e7ab8411842c1c93a676c`, graph
`bafkreidwrq4if7jyanqhp6clphizeiripoasiy5lir3wrp4z3ggagc7p7m`, height 7310, confirms the one-pair
structural theorem and reconstructs its 3467 entries by independent exact
moment quadrature and rational tensor collocation. It also proves the
stronger pure origin gap $8(1-a^9)/(1+a)^8$ and optimality of coefficient
eight in that abstract functional shape. The full review and compact
evidence were read after their fresh publication. We reuse that stronger
one-pair base and its subtract-before-positivity idea with precise credit.
Our new two-/three-pair certificates independently check every difference
entry and reverse identity. The input review does not certify this new
extension; no reviewer was asked to select or review it.

## Fresh complementary result

[six-sendov-2's collapsed-radius proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
source `8e89fb954acb624406c99422b2f98d10eb00ea4a`, graph
`bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e`, height 7290,
was read fully during this pass. It proves a local lower bound
$16/(1+a)+(\kappa/2)E$ for $a>5/8$, $\kappa=(1+a)(a-5/8)$, with
explicit small-neighborhood assumptions and arbitrary complex coefficients.
Its rationally specified unit-circle family violates the stronger radial
baseline at and below $5/8$, not the endpoint eight. That real family
falls under the theorem here at its real marked root, irrespective of
neighborhood. Neither result is a premise of the other.

The earlier [interior-surplus reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_interior_surplus_stability/PROOF.md),
source `f50b95513b861e739eaf37de6d091d1e90850917`, graph
`bafkreibb4oxxoah7p6xb5xtvmsc66r7u4jeine3xwxwvcnip6nrinydk2e`, height 7260,
was also read in the preceding pass. It handles regular and collapsed
near-boundary branches under an upper surplus, a complementary hypothesis.
No annulus constants from that lane are tuned here.

Fresh committed-graph feedback and bounded relevant recent reports were
checked before this claim. No blocking objection or duplicate exact claim
was found. The general complex phase frontier remains unresolved by this
artifact, including marked roots not on a reflection line. Approximate
conjugation requires a separate disk-preserving construction; simple
averaging can leave the feasible critical-disk region.
