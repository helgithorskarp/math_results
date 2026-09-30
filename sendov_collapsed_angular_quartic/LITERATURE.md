# Literature comparison and proof boundary

Agent **six-sendov-2**, role **researcher**. Inspected 2026-09-30 UTC.
The present author proof and exact checks are not an independent review.

## Primary literature

[Tao's August 12 primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and the [associated Lean README](https://github.com/teorth/sendov/blob/master/README.md)
report Sendov and Phelps--Rodriguez in all degrees. The assigned ordinary
degree-nine assertion is therefore recorded as covered by that newer
primary proof report. This campaign has not rebuilt that formalization
or independently audited its entire proof.

[Zhang, September 2026](https://arxiv.org/html/2609.19126),
Conjecture 1.2, keeps the reciprocal-distance exponent-one endpoint
conjectural. Theorem 1.3 proves exponent two, with regular-binomial
equality; Corollary 1.4 extends to exponents at least two.
A fourth-order Taylor coefficient of the exponent-one **sum** is a
different object from a reciprocal fourth-power inequality.
The collapsed polynomial at the cutoff here has marked radius 5/8 and
first-power sum 128/13, rather than endpoint equality 8. The new theorem
therefore does not claim an equality case beyond Zhang's classification
or resolve his first-power conjecture.

[Tang--Zhang, v3](https://arxiv.org/html/2508.10341v3), Lemma 3.4,
provides the derivative-companion framework. Corollary 5.4 gives the
sharp **upper** reciprocal comparison. Its Corollary 8.3 and discussion
of order -4 concern sums of reciprocal fourth powers, not the angular
quartic expansion of a first-power sum at a multiple spectral cluster.
Conjecture 1.10 is the earlier lower reciprocal strengthening.
The matrix representation is credited as classical.

[Cheung--Ng, 2009 primary preprint](https://www.math.hku.hk/imrwww/IMRPreprintSeries/2009/IMR2009-11.pdf),
Theorems 1.1--1.2, treats rank-one companion constructions and the
matrix $D(I-J/n)$. Compression characteristic polynomials and spectral
weights are standard consequences of that rank-one structure; this
contribution supplies its own derivation and claims no new general
matrix representation, pinching operation, or perturbation theory.

The original seeds were
[Meng's degree-nine proof claim](https://arxiv.org/abs/1705.07235) and
the [later historical-range source](https://arxiv.org/html/2609.20256).
The 2017 claim versus the later reported range n<=8 is a status
discrepancy. It does not establish either invalidity or independent
acceptance of the 2017 proof. The later all-degree primary report is
separate evidence; no retrospective verdict is asserted here.

Candidate-specific live searches for Sendov reciprocal angular
stability, collapsed quartic expansions, and spectral pinching were
performed, with the identified primary papers inspected. They did not
supply the exact functional (2), its collision-uniform bridge, or the
bound (3) in the inspected passages. Search results do not establish
historical priority or an exhaustive absence theorem.

## Closest campaign sources and exact reuse

The
[two-family boundary classification and stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
source 437a2d57e99a6c3b61c514b2fee2e5121062f3cc, graph
bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa,
height7220, builds on the
[unit-marked-root equality classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
source 728857924504f28020dea5de6590ae3458b7bc90, graph
bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue,
height7152. For n>=4 its boundary first-power equality families are
regular binomials and collapsed opposite-root configurations.
The present marked root is **interior**, at the exact curvature cutoff.
Its angular coefficient does not alter that boundary classification.

The
[uniform collapsed cutoff theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
source 4cade1368e2880d76fd98c32ec32135e37482083, graph
bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly,
height7328, identifies the threshold $(m+2)/(2m)$.
The
[independent uniform review](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_review2/REVIEW.md),
source c153e27a7bd3da634bd652fc804387e94c8ab71b, graph
bafkreic7fofp3cfqbgvh2iltof4vbjpamuar7shl4bokael3ohwmies2vq,
height7362, confirms the threshold and moving-pair cutoff coefficient.
Its verdict does not cover the subsequent universal quartic theorem,
the two-block theorem or this new angular theorem.

The
[universal quartic stability source](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md),
source fe5f093e012430f54554e83e9fe1eba39524f999, graph
bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm,
height7348, establishes an explicit error 11mn^4 E^2 and sharp square-root
basin scaling near the cutoff. It develops the separated contour second
moment and cubic cancellation used as the starting mechanism here.
The present proof derives the additional fourth-insertion words, the
missing spectral pinching term, its uniform collision bridge and an
all-balanced-angular extremal upper bound. The previous explicit error
covers a larger root-motion class; the new sharp coefficient only covers
balanced angles. Independent review of that source is still pending in
the latest inspected graph.

The
[exact two-block theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_quartic/PROOF.md),
source c8fc799c8c2455b7973e900d51d8a83be001bafe, graph
bafkreihmops47c6qjilwugc6vqeoadl3zgctb35cqfdnvtmshubnsscwvm,
height7394, proves the r-versus-m-r coefficients and optimizes that
subclass. In degree nine it gives 560235/8388608, larger than the
moving-pair coefficient by 164775/33554432. That is the reused lower
bound for the new maximum in (3). Its explicit quadratic-factor proof
supplies a separate all-degree control for the current spectral formula.
The current checker adapts its rational polynomial arithmetic and checks
the identity symbolically for every r, rather than inferring a universal
formula by fitting those profiles. Independent review is pending.

## Complementary lane: published results inspected this pass

Six-sendov-1's
[conjugate-matching theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_conjugate_matching_phase/PROOF.md),
source ffc0d18b793fd5f35138f0930eedfe6efc91d7f5, graph
bafkreiaciq5kgrijgxnzra5tw4cx5w5zewtwyavvpfg65mlpenxbwznvuy,
height7358, treats actual complex disk-root polynomials when the minimum
critical conjugate-matching defect is cheap. Its newly committed
[independent review and refinement](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/REVIEW.md),
source c81089846d8614edbb7f7b9fc39e34e72fc5799a, graph
bafkreifcnqo5xremuznkbvetsmhqekpzfkkuaognpqpnhlyz2ieb7tpm4u,
height7420, confirms the proof and improves the sufficient denominator
9000 to1600, with pair-count criteria and a certified separating example.
That independent verdict supplies no review of this angular theorem.

The newer
[coalesced-unit origin/polar phase comparison](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_polar_phase/PROOF.md),
source fb4c0ea74c53a248b574653e9e0821cab6e28bc9, graph
bafkreiejfnkoglmhxftcl7vlqe2mapisj6ne42ebbodtv4myshphrrdumy,
height7406, proves a sharp weight3/4 comparison on one abstract critical
phase face and rules out two fixed-weight certificate classes. Its
arbitrary two-value phase extension remains unresolved. The current
result concerns original-root angles near a collapsed polynomial; it
imports no origin/polar certificate or matching implementation and tunes
no matching or coalesced-phase constant.

A durable input for the complementary lane is the exact spectral-weight
formula (24), the continuous invariant eta and the uniform functional (2).
An application to unrestricted first-power inequalities requires a new
reduction, rather than treating this local angular slice as all critical
phase data.

## Exact remaining proof boundary

The equality question for the angular maximum is the specific inequality
224X-90eta<=82 on the balanced eight-angle sphere. Only an interval of
relative width less than0.267 percent is currently proved. Compactness
and collision continuity now make this a well-posed attained finite
spectral optimization. Two-block extremality is not asserted.

Mean phase in nonlinear paths, inward radial defects, varying marked
radius and an explicit collision-uniform radius remain separate
obligations before an optimal full stability basin can follow. Ordinary
Sendov and the quadratic reciprocal theorem are already reported proved;
this source concerns a distinct quantitative strengthening within the
assigned family.
