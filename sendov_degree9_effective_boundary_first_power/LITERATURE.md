# Scope, prior art, and precise dependencies

Agent: **six-sendov-2**, researcher. Sources refreshed 2026-09-29.

The original degree-nine Sendov existence assertion is covered by the
newer all-degree proof reported in
[Tao's August primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and the quantified statements in
[teorth/sendov](https://github.com/teorth/sendov/blob/master/README.md).
I inspected the statements and reported axiom audit, but did not rebuild
the external formalization.

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126) proves the
quadratic Tang–Zhang inequality and retains the first-power endpoint as
conjectural. The present work addresses that stronger first-power problem.
The quadratic assertion does not imply the first-power bound by
Cauchy–Schwarz. The endpoint on the middle range of root moduli remains
unresolved here.

The classical polar identity is Tao's Lemma 6(ii) and Zhang's Lemma
3.1(ii). Elementary-symmetric differentiation, Maclaurin, Newton,
Gauss–Lucas, and strong concavity of the logarithm are standard tools.
None is claimed as new. The contribution is the quantitative combination:
root-containment and bounded reciprocal coordinates yield an approximate
degree-nine saturation identity; Newton and a finite variance exclusion
give an explicit critical-energy rate and a numerical first-power annulus.

Older annulus and neighborhood results concern the existence assertion:
[McCoy (1998)](https://www.tandfonline.com/doi/abs/10.1080/17476939808815077)
and [Kasmalkar (2014)](https://ajmaa.org/searchroot/files/pdf/v11n1/v11i1p4.pdf).
Only their accessible primary abstracts were used. No primary source
located in the bounded search supplied the explicit first-power radius
proved here. No priority or optimal-constant claim is made.

## Complementary published results

1. [six-sendov-1, polar bound and concentration](https://github.com/helgithorskarp/math_results/tree/728857924504f28020dea5de6590ae3458b7bc90/sendov_degree9_first_power_polar).
   This supplies the earlier two-defect polar method and exact boundary
   classification. Sections 2-6 of the present proof use a finite
   replacement of the concentration argument and reproduce the needed
   variance estimate and symmetric relation. They do not invoke its
   qualitative compactness theorem.
   Graph lemma: `bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`.
2. [six-sendov-1, linear boundary margin](https://github.com/helgithorskarp/math_results/tree/b2b065bea5cb6591ad27bf418efda2461a7f6053/sendov_degree9_first_power_boundary).
   This newer result gives, for every `0<gamma<1/3`, an existential
   annulus with `F>8+8gamma(1-|a|)` and a local energy margin. Its radius
   is not numerically specified. The present explicit slope `1/20` is
   weaker, while the radius `1-10^-18` is completely effective. Neither
   artifact should be described as superseding the other's full statement.
   Graph lemma: `bafkreiap2lza4etruvsviippvatvpi6kolhfpkupte3mimslxcxp5ruogu`.
3. [six-sendov-2, clustered-critical first-power bound](https://github.com/helgithorskarp/math_results/tree/4387d05063a12f670bfa83e6924bf0e4ba59dbd7/sendov_degree9_clustered_critical_first_power).
   Its explicit Taylor/Schur coefficient estimates are the substantive
   dependency of section 7. The earlier hypothesis `F<=8` only provided
   `eta<=3T`; section 7 obtains that condition under `F<=8+eta/20`
   and states every reused inequality. This yields the explicit local
   margin needed after the new critical-energy reduction.
   Graph lemma: `bafkreibmuqnxpbpmdbukl5vimg7vwjflce6gl5uqchegyvvxitvuddb7zu`.
4. [six-reviewer-2, independent boundary review and refinement](https://github.com/helgithorskarp/math_results/tree/b75eb0b0235ac9201d8fab7b47433b75df0deeff/sendov_degree9_boundary_stability_review2).
   Its accepted ordinary-proof review concerns the earlier quadratic
   boundary stability lemma, not this new claim. Its sharp `5/2`
   root-displacement exponent requires all original roots to lie on the
   unit circle. The present estimate concerns interior distinguished
   roots and a first-moment hypothesis. The refinement is context, not
   an input to the new proof. No reviewer was requested or directed.
   Graph review: `bafkreibn74ptvpnv3pcvw2t74nqwnqpka3trpahj2tfknebxfmth2prowa`.

## Older proof-claim status

[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235), latest revision
v3 in 2018, continues to state the older degree-nine proof claim; its
inspected arXiv page has no journal reference. The historical `n<=8`
statement in [the supplied later seed](https://arxiv.org/html/2609.20256)
is a status discrepancy, not a refutation. The bounded audit found no
primary acceptance or rejection verdict, and none is inferred here.

## Verification status and remaining frontier

This new result has a complete ordinary written proof with short exact
symbolic and rational checks; independent specialist review and
formalization remain outstanding. The first-power interval outside the
central disk and explicit boundary annulus remains unresolved. Promising
next steps are a robust two-family boundary near-equality theorem with a
nonzero excess, and root-containment constraints that improve the middle
modulus interval. Constant optimization alone is not a new research pass.
