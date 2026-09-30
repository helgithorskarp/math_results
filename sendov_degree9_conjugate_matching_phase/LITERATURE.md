# Literature boundary, dependencies and complementary scope

Author: **six-sendov-1**, role **researcher**. Refreshed 2026-09-30 UTC.
No historical-priority assertion is made. The searches and primary-text
checks are bounded; an unlocated matching theorem is not proof of absence.

## Current primary boundary

[Tao's August 12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the newer all-degree Sendov and Phelps--Rodriguez proof.
[The associated Lean README](https://github.com/teorth/sendov/blob/master/README.md)
states the quantified original theorem. Source was inspected; neither its
formalization nor its full proof was rebuilt here. The originally assigned
degree-nine Sendov target is covered by that newer primary proof report.

[Tang--Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
Conjecture 1.10, formulates the reciprocal-moment strengthening.
[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126), Conjecture 1.2,
still states the exponent-one endpoint conjecturally; Theorem 1.3 proves
exponent two, with larger powers in Corollary 1.4. Lemma 3.1 gives the
communication identity used in the proof. The quadratic moment theorem
does not imply the first-power bound. These primary texts were opened
again in this pass. No theorem matching the present explicit approximate
conjugation criterion was located in the inspected text or bounded
candidate-specific searches.

The older [Meng degree-nine claim](https://arxiv.org/abs/1705.07235) and
the later [historical seed reporting the older range through eight](https://arxiv.org/html/2609.20256)
remain a status discrepancy, rather than a refutation. The bounded audit
does not settle separate acceptance, withdrawal or refutation of the older
claim. The newer all-degree proof report independently changes the status
of the original target; it does not settle the first-power endpoint.

The [collinear-original-zero manuscript](https://zhangteng2000.github.io/files/Sharp_Reciprocal_Moment_Inequalities_Collinear_Zeros.pdf)
uses original-zero collinearity and Rolle interlacing. The present theorem
permits noncollinear original zeros and complex coefficients without a
reflection axis through the marked root. The exact example in PROOF.md
also has other-root distance product above nine, placing it outside the
elementary product/AM--GM criterion already noted in the August comments
on Tao's exposition. Neither that product criterion nor continuity of
strict cases is a new result here.

## Exact published dependency and existing perturbation mechanism

The essential input is
[the uniform conjugate-symmetric origin lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md),
source `617624389fad738f3ce930d5afec15787c39c61c`, graph
`bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i`, height 7314.
It supplies $G(a)=8(1-a^9)/(1+a)^8$ under the hypothetical reciprocal budget
for positive singletons and any number of conjugate pairs. Its complete
checker was replayed in this pass. Its new two-/three-pair extension remains
independently unreviewed. The negative-real exclusion and affine reflection
conclusion of that artifact are not needed in the present proof.

The coefficient-eight one-pair base used by that input is credited to
[six-reviewer-2's independent refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_pair_review2/REVIEW.md),
source `bf49c67103f6f82a435e7ab8411842c1c93a676c`, graph
`bafkreidwrq4if7jyanqhp6clphizeiripoasiy5lir3wrp4z3ggagc7p7m`, height 7310.
It does not review either later extension.

Crucially, the **quadratic order** of a positive-axis perturbation was
already proved in
[six-reviewer-3's collinear-critical review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
source `18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d`, graph
`bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4`, height 7244.
That proof gives

$$\left(\sum_j|q_j-|q_j||\right)^2\le\frac{1-a}{1250}
\quad\Longrightarrow\quad S_1>8.$$

It observes that first derivatives at a real baseline are real, so taking
the real part removes first-order imaginary errors. We reuse and explicitly
credit that mechanism. The all-singleton specialization of our denominator
9000 is weaker than its denominator 1250; it should not replace that test.
The present addition is a **disk-preserving conjugate-pair lift** and a
grouped quadratic estimate valid around arbitrary conjugate phases. Paired
factors have quadratic real errors even when their individual angles are
large. A naive Cartesian average of reciprocals need not preserve (5),
which is why the explicit identity (8) is necessary.

The prior [angular-loss criterion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md),
source `7eb0bac3d54294930118ac2ac0aa37cdb73b52b1`, graph
`bafkreibmpkev3bekc2s2eixm3vprwycinocfzv4i6idhyzmvspedckjcae`, height 7254,
uses $\sum_j(|q_j|-\Re q_j)\le(1-a)/2400$. The exact example here violates
that sufficient condition and the preceding positive-axis criterion.
This establishes a concrete distinction of hypotheses, not a claim of
global dominance of one sufficient test over every other test.

## Fresh complementary input and remaining boundary

The fully inspected
[uniform collapsed-coercivity proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md)
by **six-sendov-2**, researcher, source
`4cade1368e2880d76fd98c32ec32135e37482083`, graph
`bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly`, height 7328,
proves local coercivity for every degree $n\ge4$, with sharp radius cutoff
$(n+1)/(2(n-1))$ and sharp infinitesimal energy coefficient. Its assumptions
concern proximity to the collapsed family. The present matching criterion
is an interior reciprocal-phase condition and does not require those local
neighborhood assumptions. Neither result is a premise of the other; no
annulus or collapsed-neighborhood constants are tuned here.

A further fresh source,
[quartic collapsed stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
commit `fe5f093e012430f54554e83e9fe1eba39524f999`, was fully read during
the final refresh. For $m=n-1$ it gives
$F\ge2m/(1+a)+\kappa E-11mn^4E^2$ when $E\le1/(16n^2)$,
and the sharp square-root basin order near the collapsed radius cutoff.
That is a stronger local radial baseline with a different energy and
parameter from the present origin-gap matching test. It is a contextual
source citation, not a premise or an independent review.

The cosine lift, its exact disk-feasibility identity, and displacement
bound $(1+\sqrt2)g$ are reusable geometric inputs for that complementary
lane. Their feasibility proof needs neither a radius cutoff nor a small
pair error. The analytic margin still requires the separate matching loss
test. No claim is made that all polynomials satisfy this test.

Recent relevant durable reports, committed graph feedback and repository
changes were refreshed again before this claim. No blocking objection or
duplicate of the exact matching claim was found. The remaining frontier is
the unrestricted complex reciprocal configuration, especially when every
matching has $K_1(a)E+K_2(a)M^2\ge G(a)$. A new estimate or another obstruction
would be needed there. Independent review of the new extension is pending;
no reviewer selection or verdict was requested.
