# Scope, primary literature and campaign dependencies

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

## Current problem and primary communication identities

The current primary manuscript
[Teng Zhang, Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126),
v1 of 16 September 2026, states the reciprocal-power family as Conjecture 1.2.
The lambda=1 endpoint remains conjectural there; Theorem 1.3 establishes lambda=2.
Its Lemma 3.1 gives the origin and polar communication identities used in the
polynomial interpretation. The second-moment hypothesis in its centered-origin
argument is unavailable under a first-power failure; it is not assumed here.
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
Lemma 6 and Conjecture 19, supplies the same interpretation and the stronger family.
Ordinary Sendov is reported resolved in this literature, and is not the new target.
The primary manuscript was refreshed on 1 October 2026 before this claim.
Bounded candidate-specific live searches found no relevant duplicate primary
source; historical priority is not exhaustively certified.

## Direct inherited mathematical ingredients

1. [General polar mean gap](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/general-polar-mean/PROOF.md),
   six-sendov-1 researcher, source 935ec2f52affd0968be4649b89abbd42f691e633,
   graph 8533, bafkreidm3pbjbv5tzj34fehpdi2njyutz7xgczubba2yn4twlg54xb7mhq.
   For arbitrary complex q with sum|q|<=8, |C_a(q)|>=1 forces
   Re mean(q)>a. This is used in the new annulus's phase and mean geometry.
   [Independent audit and47/100 refinement](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/polar-mean-audit/REVIEW.md),
   six-reviewer-1 reviewer, source de7a5141938c8afcc66b6a634b6f8db66f57d95d,
   graph 8598, bafkreifujsxvfmyhj3nvqh2wwwa72aouhmvhbap3kflw32ccwzuduvlyoy,
   confirms8533 as an ordinary proof. Its stronger retained-denominator mean
   condition is available for future work but is not required here.

2. [Arbitrary-multiplicity mean-tube origin coercivity](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/near-mean-origin/PROOF.md),
   six-sendov-1 researcher, source ea4b182f83e061cb289ca5df9bda9d1aef99f0cf,
   graph 8591, bafkreihwayklo5hnhvaltdla4km5aoromcdsyi5g5pdlf62z72hi4ij6pe.
   For a>=511/512, sum|q|<=8, Re m>=a and max|q/m-1|<=1/32, it gives
   N_a(q)>=1+(1-a)+(7/8)sum(Re eta)^2+(1/32)sum(Im eta)^2>1.
   This excludes the small-spread branch of the new annulus. It remains an
   ordinary author proof pending independent review. Review8598 cites8591
   only as downstream context; it does not audit it.

3. [Collinear-critical theorem and real origin gap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
   six-sendov-1 researcher, source 177818bdbd7e23f16ec46bacfc3077d7a22a8aca,
   graph 7212, bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4.
   Its symmetric multiaffine minimizer reduction and unpenalized gap
   [O_a(r)-product r]>=8(1-a^9)/(1+a)^8 are prior results. The present
   contribution applies that reduction to a new penalized expression and
   independently reconstructs its entire new positivity certificate.
   [Independent collinear review and quadratic phase criterion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
   six-reviewer-3 reviewer, source 18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d,
   graph 7244, bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4,
   proves Re O_a(q)>=O_a(|q|)-K1(sum|q-|q||)^2, with the exact derivative
   constants restated in the new proof. The new contribution credits that
   estimate and adds the Newton-defect term to its sufficient phase criterion.

## Prior concentration, effective annuli and boundary asymptotics

[Boundary classification and polar concentration](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
graph 7152, bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue,
already contains the limiting radial variance budget and both boundary families.
Those are not new claims here. The finite variance bound in the new proof is a
coarse ingredient calculated under its relaxed channels.

[Effective boundary stability and annulus](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md),
six-sendov-2 researcher, source 4ef7996638ffee0f42d7780e477c2745aeac233e,
graph 7184, bafkreigenk4drh3ixa54mwshdukdnv3xs2f7khffkpc7u2t4rfcmcq34ey,
proves F>8+(1-a)/20 for1-a<=10^-18, using actual original-root coefficients,
a finite variance reduction and critical-root concentration.
[Independent effective-annulus review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_review3/README.md),
six-reviewer-3 reviewer, graph 7218,
bafkreifhsmxp3bhwlvk4t5xt2o3l5xkgaep2whtnlp6g4j5cgavsel2piq,
widens that annulus to121*10^-18 with the same slope.
[Another independent effective-annulus audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_review2/README.md)
uses Newton/Maclaurin saturation to shorten an inherited concentration step.
Newton inequalities and concentration by their saturation are classical/inherited
mechanisms. The new expression is the explicit radial origin penalty
2a e2((1+a)r-1)-e3((1+a)r-1), its uniform coefficient five, and its use to
exclude relaxed channels in a larger strict-inequality annulus. No claim
extends the older linear slope to the new larger annulus.

[Sharp boundary slope and critical-profile classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md),
graph 8530, bafkreif2fnypqfvsvaoqkwti2scnayeqedzd3tmeszpiexmbexnckxpdbu,
and [the second-order boundary theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md),
six-sendov-3 researcher, source f8df996dba7bfec1d05eb6731b3b8e667ca8f860,
graph 8619, bafkreicgkxmkaequm4yqqzg2tb7rjna6a245ipqejfri6nwiwjgwcwhrqy,
are complementary asymptotic results. They neither supply nor are needed for
the present effective annulus. The quartic extension remains independently
unreviewed at this checkpoint; no chat statement is a proof premise.

The unrestricted degree-nine complex first-power inequality, extension to
the middle range, sharper shape-dependent phase control, and the strongest
joint-channel relaxation remain unresolved by this contribution.
