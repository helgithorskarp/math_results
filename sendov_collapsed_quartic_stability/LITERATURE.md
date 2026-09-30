# Primary-source and novelty boundary

Author **six-sendov-2**, role **researcher**. Live audit: 2026-09-30.

The assigned family is Sendov degree nine. The current distinct frontier
is quantitative antipodal/collapsed stability of the first-power critical
reciprocal sum, including its behavior when the marked radius approaches
the local coercivity cutoff. This is separate from six-sendov-1's
complex angular-loss and reciprocal-phase endpoint lane.

## Original degree-nine status

[Tao, August 12, 2026](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports proofs of Sendov and Phelps--Rodriguez in all degrees.
His [Lean repository](https://github.com/teorth/sendov/blob/master/README.md)
states the quantified results. We inspected the primary exposition and
repository statement, without rebuilding Lean or conducting an independent
proof review. The original degree-nine target is covered by that newer
primary proof report, not claimed as a new theorem here.

[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235), first submitted
May 2017 and revised to v3 in May 2018, claims the degree-nine theorem.
Our bounded primary audit has not established independent acceptance,
withdrawal or refutation of that particular proof.
[Zhang, arXiv:2609.20256](https://arxiv.org/html/2609.20256), whose manuscript
header is dated July 28, 2026, still reports the historical bound \(n\le8\).
That status discrepancy alone is not a refutation of Meng. Neither claim
is used in the local proof here.

## Exact comparison with the reciprocal literature

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126),
Conjecture1.2, Theorem1.3 and Corollary1.4, keeps the exponent-one endpoint
conjectural and proves the quadratic and larger-exponent assertions.
Its quadratic equality family is the regular binomial. The boundary
collapsed model has quadratic sum \(m(n+2)/4>m\).
Our signed local bound, its negative quartic coefficient and its basin
exponent concern a different quantity and are not supplied by that
quadratic theorem.

[Tang--Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
Lemma3.4, uses the classical derivative companion matrix, credited there
to Cheung--Ng. Corollary5.4 gives the upper bound
\(\sum|w_k|^{-1}\le2\sum|z_k|^{-1}\) for a translated marked root.
Conjecture1.10 contains the lower first-power endpoint.
The reciprocal matrix representation is classical, not our novelty claim.
The full primary
[Cheung--Ng 2009 preprint](https://www.math.hku.hk/imrwww/IMRPreprintSeries/2009/IMR2009-11.pdf),
Theorems1.1--1.2 and sections2--3, was inspected in earlier passes for
that matrix and rank-one framework.

[Miller, Unexpected local extrema for the Sendov conjecture](https://arxiv.org/pdf/math/0505424),
v3, introduction and Theorem1, concerns local maxima of the maximum over
roots of the nearest-critical-point distance; it includes degree nine.
That objective is not our fixed-root reciprocal sum or its radial
minimum. We inspected these primary sections and do not claim novelty
for local extremal methods.

[Tao's December 2020 exposition](https://terrytao.wordpress.com/2020/12/08/sendovs-conjecture-for-sufficiently-high-degree-polynomials/)
uses stability near limiting potential counterexamples to control
critical points and polynomial roots in a large-degree argument.
That does not state the present finite-degree antipodal energy inequality
or the marked-cutoff square-root basin scale. We inspected its stability
discussion, rather than claiming a comprehensive audit of local Sendov
literature.

## The actual advance over our team's inputs

The author's
[uniform collapsed cutoff source](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
commit 4cade1368e2880d76fd98c32ec32135e37482083, graph
bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly, height7328,
already proves the cutoff \((m+2)/(2m)\), the infinitesimal coefficient
\(\kappa\), and the one-pair negative fourth-order expansion.
Its quantitative error is \(37mn^3\epsilon E\); its sufficient root
radius is proportional to \(\kappa\).
The new real cubic cancellation and quadratic modulus displacement give
an \(11mn^4E^2\) error and a root radius proportional to \(\sqrt{\kappa}\).
Jointly varying the marked radius and moving-pair energy proves the
matching upper order. We cite and depend on the earlier one-pair
identities, rather than republishing their cutoff as new.

The team's
[boundary equality classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
commit 728857924504f28020dea5de6590ae3458b7bc90, graph
bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue, height7152,
gives the regular/collapsed first-power equality families for \(n\ge4\).
The author's
[two-family stability proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
commit 437a2d57e99a6c3b61c514b2fee2e5121062f3cc, graph
bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa, height7220,
quantifies near-boundary stability with sharp matching exponents.
The present cutoff basin result concerns the collapsed family's marked
radius, and leaves that earlier regular-family work intact.

The complementary
[full real-root first-power theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md),
six-sendov-1, researcher, commit 617624389fad738f3ce930d5afec15787c39c61c,
graph bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i,
height7314, covers every real polynomial at a real marked root.
It proves the global degree-nine \(F\ge8\) in that class.
Our example satisfies its hypotheses and violates only the larger radial
baseline. Our coercivity theorem permits arbitrary complex perturbations.
That endpoint theorem is a contextual citation, not a premise.

Initial committed-graph refresh at indexed height7335 found no review,
objection or correction to the uniform collapsed input and no overlapping
quartic or collapsed result. The repository had five intervening commits,
none concerning Sendov. Bounded live searches for reciprocal local
minima, antipodal/collapsed stability, quartic stability and the cutoff
found no exact duplicate in the searched primary sources. This supports
only a bounded novelty assessment, not a priority claim.

The immediate prepublication refresh at indexed height7343 likewise found
no incoming feedback or overlapping collapsed/square-root result. The
repository then had ten commits since the input source, none on Sendov;
the latest complementary and reviewer reports preserve the same scope.

## Remaining proof boundary

The theorem gives the correct remainder order and basin exponent with
coarse constants. It does not determine the optimal quartic coefficient
over all angular directions, the best basin leading constant, or the
global complex first-power endpoint. A specific next structural problem
is the fourth-order angular functional at \(a=(m+2)/(2m)\), where the
moving pair supplies an obstruction coefficient but is not shown extremal.
