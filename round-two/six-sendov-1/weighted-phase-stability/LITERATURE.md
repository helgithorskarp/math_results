# Primary problem, dependencies and nearby phase estimates

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

## Primary status

[Teng Zhang, Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126),
Conjecture1.2, keeps the first-power endpoint conjectural; Theorem1.3 proves
the quadratic case. Lemma3.1 gives the origin and polar communication identities
used in the polynomial interpretation here. Its centered estimates under a
second-moment bound do not supply a first-power-failure premise.
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
Lemma6 and Conjecture19, describes the same stronger family. Ordinary Sendov
is reported resolved and is not the assigned open target.

The current primary manuscript and candidate-specific searches were refreshed
on1October2026 before publication. Searches included Sendov/Tang--Zhang first
power, weighted phase, and factor/product bounds. No relevant duplicate primary
result was located in this bounded comparison. No exhaustive historical-priority
or optimal-constant assertion is made for the elementary envelope.

## Explicit mathematical dependencies

1. [Radial Newton-defect theorem and finite polar variance cap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/radial-defect-annulus/PROOF.md),
   six-sendov-1 researcher, source de423eaba9288fcbcfa79a86bbf15f2fcded183a,
   graph8656, bafkreiasy3xkvn4kiqqbbjkjngd2aba7d6iwrtkspv67y3jry3ztb446hi.
   It proves (1+a)^8[O_a(r)-product r]>=8(1-a^9)+5D_a(r),
   D_a(r)=2a e2((1+a)r-1)-e3((1+a)r-1), and the finite variance cap
   v<=80001923/79997600 for1-a<=10^-6 under the joint polar/disk channels.
   These are premises of the new annulus, not results reconstructed by this
   directory's checker. Its previous unconditional annulus width is10^-10.
   Independent review of8656 is pending at the major-claim refresh.

2. [General polar mean gap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/general-polar-mean/PROOF.md),
   six-sendov-1 researcher, source935ec2f52affd0968be4649b89abbd42f691e633,
   graph8533, bafkreidm3pbjbv5tzj34fehpdi2njyutz7xgczubba2yn4twlg54xb7mhq.
   Under sum|q|<=8 and|C_a(q)|>=1 it gives
   Re mean(q)>a+(2/5)(1-a)/[a(1+a)]. This supplies the phase budget.
   [Independent review8598](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/polar-mean-audit/REVIEW.md),
   six-reviewer-1 reviewer, source de7a5141938c8afcc66b6a634b6f8db66f57d95d,
   bafkreifujsxvfmyhj3nvqh2wwwa72aouhmvhbap3kflw32ccwzuduvlyoy,
   confirms8533 and improves its coefficient to47/100. The new annulus uses
   the author's2/5 coefficient. Review8598 does not audit the mean-tube lemma.

3. [Arbitrary-multiplicity mean-tube origin bound](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/near-mean-origin/PROOF.md),
   six-sendov-1 researcher, source ea4b182f83e061cb289ca5df9bda9d1aef99f0cf,
   graph8591, bafkreihwayklo5hnhvaltdla4km5aoromcdsyi5g5pdlf62z72hi4ij6pe.
   For a>=511/512, sum|q|<=8, Re m>=a and max|q/m-1|<=1/32,
   it gives N_a(q)>1 with explicit radial/angular coercivity. The new annulus
   uses this lemma in its small-spread branch. Its ordinary author proof is
   independently unreviewed at this checkpoint.

## Earlier phase and angular mechanisms

[Collinear-critical origin theorem7212](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
source177818bdbd7e23f16ec46bacfc3077d7a22a8aca,
bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4,
contains the real minimizing-profile reduction and unpenalized origin gap.
[Independent review7244](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
six-reviewer-3 reviewer, source18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d,
bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4,
proves the quadratic phase estimate and the real gap>=9(1-a)/32 used in
the conditional angular criterion. Its multiaffine Taylor argument is credited.
The new small-phase coefficient207/98 applies only when epsilon<=1/100;
review7244's global phase estimate retains its broader phase domain.

[Weighted signed angular budget7254](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md),
six-sendov-1 researcher, source7eb0bac3d54294930118ac2ac0aa37cdb73b52b1,
bafkreibmpkev3bekc2s2eixm3vprwycinocfzv4i6idhyzmvspedckjcae,
already proves a signed subset-phase obstruction and Delta<=(1-a)/2400
sufficient criterion, with no small-phase premise. Weighted angular budgets
and quadratic phase order are prior mechanisms. The new ingredient here is
the one-factor exponential envelope, its exact subset-budget consequence,
and the resulting all-phase exponential and small-phase Taylor estimates.
These prove the new conditional Delta<=(1-a)/41 region with an explicit
origin margin, and pay for a wider unconditional joint-channel annulus.

## Complementary boundary work

[Prior effective-annulus theorem7184](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md)
and [review7218](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_review3/README.md)
retain their linear reciprocal-sum margin on narrower effective collars.
[Sharp second-order theorem8619](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md)
is independently confirmed by [review8684](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md).
[Quantitative profile stability8668](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/profile-stability/PROOF.md)
is a separate, currently independently unreviewed extension with existential
constants. These boundary results are complementary citations, not inputs
to the weighted-phase proof or effective annulus. Review8684 cites8656 as
context; it does not audit8656 or this extension.

The full complex degree-nine first-power endpoint, a substantially larger
unconditional middle range, optimal constants and a numerical sharp-boundary
annulus remain unresolved here. No reviewer target or verdict was requested.
