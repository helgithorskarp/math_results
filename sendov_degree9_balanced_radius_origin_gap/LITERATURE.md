# Literature boundary and cited reuse

Author: **six-sendov-1**, role: **researcher**. Checked 2026-09-30.
This records inspected primary sources, not an exhaustive priority survey.

## Original target and first-power endpoint

The ordinary degree-nine Sendov target is covered by the all-degree proof
reported in Tao's
[August 12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and the accompanying
[Lean repository README](https://github.com/teorth/sendov/blob/master/README.md).
The exposed
[conjecture declarations](https://github.com/teorth/sendov/blob/master/Sendov/Conjecture.lean)
include strict interior distance below one. This campaign has not rebuilt
the external formalization or audited its full proof. The communication
identities and the use of centroid, polar, and two origin identities are
explicit in the primary exposition; none is claimed as new here.

The historical
[Meng 2017 degree-nine claim](https://arxiv.org/abs/1705.07235)
and the later
[September degree-≤8 summary](https://arxiv.org/html/2609.20256)
show a discrepancy in reporting. That discrepancy is not a refutation or
a verdict on historical acceptance. The newer all-degree primary proof
report, rather than an inferred rejection of Meng, changes the target's
current research status.

[Zhang's September paper](https://arxiv.org/html/2609.19126)
states the exponent-one Tang–Zhang endpoint as a conjecture and proves its
quadratic case. The earlier
[Tang–Zhang preprint, v3](https://arxiv.org/html/2508.10341v3)
also formulates the first-power lower bound. The theorem in this directory
is an abstract four-plus-four, two-channel inequality. Its polynomial
corollary gives a restricted strict first-power bound; it does not settle
either general conjecture.

The arithmetic–geometric mean polar envelope itself is prior machinery:
Tao Proposition 10(i) and Zhang Lemma 4.1. The new degree-nine calculation
is the explicit bound at mean parameter equal to the marked root,
$F_a(a)\le1-\frac23(1-a^2)^2$, paired with the sharp linear unit-origin
estimate under the polar-forced mean condition. No new general polar
communication identity or arithmetic–geometric mean argument is claimed.

## Exact comparison with campaign inputs

The author's
[two-unit-phase radial-gap proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_phase_radial_gap/PROOF.md)
(source commit `9c9bd0a1e0d8e83d26254461586a82d9d21086c2`;
graph `bafkreic7rctxzow5pjncoiswptyrgloe5jdkk63n7p35yj55sduxgj3nna`)
establishes a different unit-phase comparison with a combined interior
and angular margin, then excludes an absolute neighborhood of radius one.
The present proof instead uses the polar channel to force a stronger mean
real-part condition, proves a sharp linear unit-origin lower bound, and
transports only radial imbalance at any admissible common radius. It does
not replace the earlier combined angular inequality. The polynomial
algebra helpers adapt that source; all new identities and basis
reconstructions are self-contained in this directory.

The author's
[coalesced-phase proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_polar_phase/PROOF.md)
(source `fb4c0ea74c53a248b574653e9e0821cab6e28bc9`;
graph `bafkreiejfnkoglmhxftcl7vlqe2mapisj6ne42ebbodtv4myshphrrdumy`)
motivates phase-based comparisons but treats a narrower one-phase domain.
The new exact monotonicity obstruction explains why a simple origin-only
radial extension of such a bound fails. It does not refute the earlier
unit-radius result.

The author's
[conjugate matching result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_conjugate_matching_phase/PROOF.md)
(source `ffc0d18b793fd5f35138f0930eedfe6efc91d7f5`;
graph `bafkreiaciq5kgrijgxnzra5tw4cx5w5zewtwyavvpfg65mlpenxbwznvuy`)
and its
[independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/REVIEW.md)
(source `c81089846d8614edbb7f7b9fc39e34e72fc5799a`;
graph `bafkreifcnqo5xremuznkbvetsmhqekpzfkkuaognpqpnhlyz2ieb7tpm4u`)
give a separate mismatch-margin criterion for arbitrary reciprocal
multisets. The review strengthens that criterion's denominator from
9000 to 1600. Those results are not proof dependencies of the present
two-phase certificate, and no separation between their polynomial scopes
and the new corollary is claimed.

The complementary six-sendov-2 lane's
[collapsed angular quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
(source `57dd686588ddf1874ebb2e52f1a9aac898cc2df8`;
graph `bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne`)
computes exact balanced original-root angular coefficients at $a=5/8$
and a positive quartic lower bound. Its variables are original-root
perturbations near a collapsed equality family. The present theorem
concerns interior reciprocal critical points and a two-channel radial
imbalance. The unit-origin linear coefficient 2 and polar mean-pressure
estimate may be useful as interior restrictions, but no conversion of the
quartic's perturbation parameters into the present hypotheses is asserted.

The refreshed
[exact angular optimizer](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md)
(source `71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f`;
graph `bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi`)
now closes that angular maximum at $560235/8388608$, with precisely
singleton/seven directions and quantitative near-maximizer geometry.
Its full proof was read. The angular spectral bridge it imports remains
outside independent review; the optimizer gives no unrestricted inward
root-motion or moving-marked-radius theorem.

The fresh
[independent two-block review](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_block_quartic_review1/REVIEW.md)
(source `823da55eaa6088dfa0168f57da2157ca0b01fd11`;
graph `bafkreig7yesgssknqm3ot3egoa44fajqduxkumrlisjoawk2nqsg6i4xzy`)
confirms the earlier two-block coefficient and improves a different
maximum-root basin upper obstruction to squared constant $3328/75$.
The further
[nonlinear two-block lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_review3/PROOF.md)
(source `4de653093173ec7ec24de738ea297f9f829e0c1a`;
graph `bafkreicye5w4llvutfwvsbe46hv7vhnbeukaejjevzpy6ldyxli5q3xqsq`)
proves the exact local constant over independent nonlinear two-phase
approaches in that original-root family. Both complete arguments were
read for scope. Their citations to the author's prior critical-phase
result are context, not confirming verdicts on it or on the present gap.
These three fresh results are complementary inputs, not premises of
the new certificate.

## What remains

No exact duplicate of the present abstract two-channel inequality was
found in the inspected primary material. This is a limited literature
comparison, not a global novelty certification. In particular the
equal-radius polynomial exclusion already follows from the primary
strict-interior Sendov report. The present quantitative functional gap
uses fewer channels and is the object being proposed for independent
checking.

The large radial-imbalance mode is still untreated: the general complex
four-plus-four necessary system and the unrestricted degree-nine
first-power Tang–Zhang endpoint remain unproved by this source. The
natural next question is how the polar-forced mean condition changes
with non-small imbalance, rather than improving the constant (10^6).
