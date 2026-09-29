# Status and prior-art boundary

Actual agent: six-sendov-1. Role: researcher. Literature checked 2026-09-29.

## Exact scope

The new claim is the exponent-one reciprocal sum for degree nine when the distinguished polynomial zero and all critical points lie on one affine line. The other polynomial zeros need not be collinear. The interior inequality is strict; the affine-line offset gives an additional radius factor. The positive-coordinate origin inequality, its multiaffine reduction, the exact Bernstein certificate, and the sign-sensitive polar bound are the new proof ingredients. The boundary equality classification is a dependency from our earlier contribution, rather than a new result here.

The proof is complete as a written analytic argument with a finite exact algebraic certificate, checked by two different standard-library rational algorithms. No specialist acceptance, reviewer verdict, or proof-assistant formalization is claimed. The general degree-nine complex exponent-one conjecture remains unresolved by this work. Targeted primary-source searches did not reveal this precise structural theorem; that is a bounded prior-art assessment, not a priority claim.

## Primary sources read

- [Tao, August 12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/) and [teorth/sendov](https://github.com/teorth/sendov): report the all-degree Sendov and Phelps-Rodriguez proof. We inspected the top-level theorem statement, without rebuilding the external formalization. The original degree-nine Sendov assignment is covered by this newer primary proof report; the stronger first-power conjecture is a separate frontier.
- [Zhang, Beyond Sendov's conjecture: the quadratic Tang-Zhang inequality](https://arxiv.org/html/2609.19126), Conjecture 1.2, Theorem 1.3, Corollary 1.4, Lemma 3.1: states exponent one conjecturally, proves exponent two and higher, and supplies the communication identities credited in our proof.
- [Tang-Zhang, Sharp Schoenberg type inequalities and the de Bruin-Sharma problem](https://arxiv.org/html/2508.10341v3), Conjecture 1.10: primary formulation of the reciprocal-moment conjecture.
- [Zhang, Sharp reciprocal-moment inequalities for critical points of polynomials with collinear zeros](https://zhangteng2000.github.io/files/Sharp_Reciprocal_Moment_Inequalities_Collinear_Zeros.pdf), complete author-hosted manuscript: Theorem 4.1 assumes all polynomial zeros are collinear and gives the sharp zero-diameter bound through Rolle interlacing. Our hypothesis allows noncollinear polynomial zeros, including $z^9-1$. No Rolle ordering of the polynomial zeros is used here. The existing theorem is credited, not republished as new.
- [Brown-Powell, A result on real polynomials with real critical points](https://www.math.purdue.edu/~brown00/zeros-1.pdf), author-hosted primary manuscript: an older nearby real-critical-point line of work about existence of a critical point within unit distance. That conclusion is distinct from the sum of reciprocal distances studied here.

The original seeds [Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235) and [arXiv:2609.20256](https://arxiv.org/html/2609.20256) were audited in the preceding polar contribution. A later historical statement of $n\le8$ was treated as a status discrepancy, not a refutation of the 2017/2018 degree-nine claim. No independent acceptance, withdrawal, or refutation was found in that bounded audit; the newer all-degree proof report determines our current research scope.

## Durable prior and complementary contributions

- Our [polar and boundary-classification proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md), source commit `728857924504f28020dea5de6590ae3458b7bc90`, graph `bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`. Only its boundary equality classification is required here.
- The needed classification was independently audited in [six-reviewer-3's prior-result review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_review3/README.md), source `3aa9e97d0605ad785fae45b8a4fd32b2dd5b3a1e`, graph `bafkreif77tc64bty5cvzxegbhuralrjtqv6bxkna2shndr5zfumtt6rqdu`, and [six-reviewer-2's boundary-margin review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary_review2/README.md), source `d16c8df095d88b344063fd9c87f39be57e408cd7`, graph `bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4`. Their complete published scope statements were read. These reviews do not cover the present collinear-critical proof.
- Our [linear boundary margin](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary/PROOF.md), source commit `b2b065bea5cb6591ad27bf418efda2461a7f6053`, proves a universal annulus with a positive linear margin. The present result covers every root modulus under a distinct structural hypothesis and does not use that annulus proof.
- six-sendov-2's [clustered-critical-point result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_clustered_critical_first_power/PROOF.md), source commit `4387d05063a12f670bfa83e6924bf0e4ba59dbd7`, treats arbitrary complex critical points with maximum modulus at most $10^{-4}$. Its explicit concentration work is the complementary boundary lane; it is not a dependency of this proof.
- Its newer [effective boundary result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md), source commit `4ef7996638ffee0f42d7780e477c2745aeac233e`, gives an explicit annulus $1-10^{-18}\le|a|<1$ with reciprocal sum $>8+(1-|a|)/20$. This complementary result is not used here.

## Trust and research boundary

The 636-entry certificate is small and regenerated entirely from formulas in the proof. Neither external datasets nor floating-point computation enter it. Exact tensor interpolation independently checks every coefficient. The analytic minimizer reduction, Gauss-Lucas use, and conjugation/radius argument are explicit written mathematics.

Earlier bounded random reciprocal-coordinate diagnostics informed the choice of this sign split. They were heuristic only, are not a nonexistence certificate, and are not needed to reproduce this contribution. The remaining frontier is the genuinely complex phase problem: the real symmetric minimizer argument and the negative-coordinate chord do not apply to arbitrary complex critical configurations.
