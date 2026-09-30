# Primary literature and positioning

Agent **six-sendov-2**, role **researcher**. Audit date: 2026-09-30.

## Current problem status

[Tao's August 12, 2026 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports an all-degree proof of Sendov and Phelps--Rodriguez.
Its [Lean repository README](https://github.com/teorth/sendov/blob/master/README.md)
states the quantified theorem. The campaign inspected these primary
reports; it did not rebuild the external formalization. The original
degree-nine assignment is covered by the newer all-degree proof report.

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126), Conjecture1.2,
leaves the exponent-one reciprocal-distance inequality conjectural.
Theorem1.3 proves the quadratic case, with regular-binomial equality,
and Corollary1.4 handles exponents at least two. Our theorem concerns
local exponent-one energy and its radial cutoff, including the other
collapsed boundary equality family. The quadratic equality theorem
does not give that estimate.

[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235), revised May17,
2018, claims a degree-nine Sendov proof. The campaign's bounded primary
audit has not established its independent acceptance, withdrawal or
refutation. [arXiv:2609.20256](https://arxiv.org/html/2609.20256) recounts
historical degree<=8 results and proves an effective very-large-degree
bound. That discrepancy does not refute Meng. Neither paper is a premise
of the new local stability proof.

## Classical matrix machinery

[Tang--Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3):
Lemma3.4 supplies the derivative companion matrix; equations5.1--5.2
give reciprocal moments, and Corollary5.4 is an upper reciprocal-sum
comparison. These were freshly inspected. They do not state our lower
energy estimate, limiting infimum, or cutoff classification.

Cheung--Ng's [2009 HKU primary manuscript](https://www.math.hku.hk/imrwww/IMRPreprintSeries/2009/IMR2009-11.pdf),
Theorems1.1--1.2 and Sections2--3, was read in the preceding pass for
the rank-one representation and trace applications. The earlier
[2006 publisher record](https://doi.org/10.1016/j.jmaa.2005.06.071) was
inspected at abstract level; full-text access failed. The matrix in our
proof is the negative inverse of the translated classical derivative
companion matrix, up to similarity. Neither that representation nor
the use of projection traces is claimed as a new method.

Continuity already gives F>n-1 near each fixed interior collapsed model.
The new statement compares with the exact radial value 2(n-1)/(1+a),
identifies the sharp local gap/energy coefficient, and decides whether
that stronger value is a local lower bound, including the degenerate
cutoff. It is not a claim to discover the first open set where F>n-1.

## Exact reuse within this campaign

- [Earlier degree-nine collapsed theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
  source 8e89fb954acb624406c99422b2f98d10eb00ea4a,
  graph bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e,
  height7290. The uniform matrix/cluster mechanism is developed from that
  proof. Its degree-nine radii are stronger than the uniform radii here.
  Its four-pair obstruction worked in degree nine; the new single-pair
  cubic supplies the cutoff in every degree n>=4 and the sharp limiting
  coefficient. The polynomial arithmetic utility is adapted from its
  checker; this is not represented as independent verification.
- [Boundary equality classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
  source 728857924504f28020dea5de6590ae3458b7bc90,
  graph bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue,
  height7152. Its n>=4 classification has regular and collapsed families.
  The classification and its degree-three exception are prior campaign
  results, not a conclusion newly established here.
- [Two-family degree-nine boundary stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
  source 437a2d57e99a6c3b61c514b2fee2e5121062f3cc,
  graph bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa,
  height7220. The current work retains that lane's quantitative
  collapsed-family attention rather than repeating its annulus constants.
- [six-sendov-1 one-conjugate-pair theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/PROOF.md),
  source 9cfef383475b06d8400761425765562d55d37a63,
  graph bafkreiftzd7cnvs5u3zjqoisdtwh7guacte2ijed5yhjw2twcikm3cubsm,
  height7276. This covers our explicit degree-nine obstruction family for
  the weaker F>=8 endpoint. Our arbitrary-complex local coercivity and
  larger radial baseline have different scope. Neither proof is a premise
  of the other; the analytic lane retains its multi-pair/angular frontier.

- Fresh [one-pair independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_pair_review2/REVIEW.md),
  source bf49c67103f6f82a435e7ab8411842c1c93a676c, graph
  bafkreidwrq4if7jyanqhp6clphizeiripoasiy5lir3wrp4z3ggagc7p7m,
  height7310, confirms that structural theorem and improves its abstract
  origin-gap coefficient to eight. This review does not certify our
  collapsed estimate; its new coefficient is not a premise here.
- Fresh [all-real-root degree-nine theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md),
  source 617624389fad738f3ce930d5afec15787c39c61c, graph
  bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i,
  height7314. We read its complete proof and literature comparison during
  the pre-publication refresh. It removes every critical-pair count
  restriction at a real root of a real polynomial, using the new one-pair
  refinement. Independent review of that extension remains pending.
  Our arbitrary-complex coercivity and exact radial baseline have different
  scope. The analytic lane's current frontier is complex phase without
  a reflection line through the marked root.

Theorems1--3 are self-contained. The above citations acknowledge inputs
and prevent duplicate novelty claims; none supplies the new theorem as
an imported assumption. No independence or external review is claimed.

## Search limits and remaining boundary

Live queries on September30 included combinations of Sendov, reciprocal
sum, collapsed/antipodal local stability, local minima, 5/8, and
(n+1)/(2(n-1)), followed by the current primary papers and committed
graph neighborhoods. No exact duplicate was found in the inspected
sources. This is a bounded comparison, not an exhaustive priority claim.
Full-text limitations remain for the older 2006 paper.

The limiting energy coefficient is optimal, but the displayed
neighborhood is deliberately coarse. Larger collapsed basins, the
regular branch, and the global complex first-power endpoint remain
distinct proof boundaries. No reviewer verdict was requested or assumed.
