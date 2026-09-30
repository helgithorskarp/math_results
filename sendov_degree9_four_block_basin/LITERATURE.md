# Literature, dependencies and research boundary

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
The human's current Sendov-family brief is the problem source.
One primary approach, algebraic structure, is used with exact computer
algebra and Python research-code tools. No worker or review was delegated.

## Current primary status

Live primary sources were reopened on 2026-09-30.
[Tao's August 12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and the [primary Lean repository](https://github.com/teorth/sendov/blob/master/README.md)
report all-degree Sendov and Phelps–Rodriguez results.
The historical ordinary degree-nine assertion is therefore covered by
the newer proof report. This author performed no rebuild or full audit
of that external formalization.

[Zhang, September 2026](https://arxiv.org/html/2609.19126),
Conjecture1.2, leaves exponent one conjectural; Theorem1.3 proves exponent
two, with only regular-binomial equality, and Corollary1.4 gives
exponents at least two. The current degree-nine obligation remains
\(\sum_{j=1}^8|a-\zeta_j|^{-1}\ge8\) for arbitrary complex
disk-root polynomials. A fourth-order Taylor coefficient of that
first-power sum is not a reciprocal fourth-power theorem.

[Tang–Zhang v3](https://arxiv.org/html/2508.10341v3),
Conjecture1.10, is the earlier endpoint formulation. Its companion
matrix and sharp negative-order upper estimates are predecessors of
the general angular machinery, not new identities here.
The present proof instead differentiates the explicit polynomial and
desingularizes its residual quartic; no matrix-theorem input is required.

The historical [Meng 2017 degree-nine claim](https://arxiv.org/abs/1705.07235)
and [the older explicit large-degree manuscript](https://arxiv.org/html/2609.20256),
which reports the classical verified low-degree range through eight,
were reopened. Those reports record a historical status discrepancy;
they do not establish either acceptance or refutation of Meng's proof.
The active current frontier follows the newer primary status above.

[Miller, Seeking a quadratic refinement of Sendov's conjecture](https://arxiv.org/html/2506.12951v1)
studies a nearest-critical-distance refinement as the marked radius
approaches one. Our reciprocal-sum baseline basin concerns a collapsed
original-root cluster and a moving marked radius near five eighths.
The functional, base point and quantified neighborhood differ.
Bounded live searches for Sendov/collapsed/quartic/first-power stability
found no exact duplicate of the scalar sextic optimizer in the inspected
primary material. This is a limited novelty comparison, not a priority claim.

## Precise campaign reuse

The new [proof](PROOF.md) gives a stand-alone direct coefficient
derivation, its joint analytic interpretation, a scalar optimization,
and the exact loss from nonlinear phase-mean drift at fixed first slopes.
Earlier campaign results are credited predictions and comparisons:

| Input | Exact source and graph | Scope reused |
| --- | --- | --- |
| [Three-block theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_block_basin/PROOF.md) | a753c5239339dff40dac378b2cee633e7b89e54c; bafkreihdibwm7xjjrvjw5e3vhhyaluvnzhywgiayfstt6fvt76j3oexzzm,7500 | The u0 endpoint, varying-radius predecessor and basin definition. The author's Laurent kernel is adapted openly. |
| [Two-block review](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_block_quartic_review1/REVIEW.md) | 823da55eaa6088dfa0168f57da2157ca0b01fd11; bafkreig7yesgssknqm3ot3egoa44fajqduxkumrlisjoawk2nqsg6i4xzy,7446 | Credited u1 constant3328/75, optimized only within two blocks. |
| [Nonlinear two-block review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_two_block_review3/PROOF.md) | 4de653093173ec7ec24de738ea297f9f829e0c1a; bafkreicye5w4llvutfwvsbe46hv7vhnbeukaejjevzpy6ldyxli5q3xqsq,7462 | Prior second-jet weighted-mean loss and nonlinear limit for two blocks. Section6 extends that mechanism to the fixed four-block first slopes with four independent phase jets. |
| [Angular functional](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md) | 57dd686588ddf1874ebb2e52f1a9aac898cc2df8; bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne,7432 | Predicts cutoff coefficients and spectral weights. Direct quartic arithmetic reproduces this profile. |
| [Energy optimizer](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_optimizer/PROOF.md) | 71a2f9f201bc9fa7e32237bdd14feef5ff8c3f8f; bafkreibyx62xasxzcqheejib64y3i4dr462rjc4bjoerumtthypw6rqcdi,7472 | Maximizes K, whereas the present radius objective maximizes mu2*K. |
| [Angular independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md) | b587355b8bf25a09fee12cdca1e8596712f49941; bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu,7496 | Confirms7432/7472 including the collision/uniformity bridge, and sharpens their near-maximizer geometry. No verdict on this new result. |
| [Quartic stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_quartic_stability/PROOF.md) | fe5f093e012430f54554e83e9fe1eba39524f999; bafkreihspazdbffjge3vs3zevwt5zvwpfukkyr5ih6hzrbst2pwrlfv5fm,7348 | Earlier sufficient basin and square-root exponent, with a coarse universal coefficient. This work sharpens an upper obstruction. |
| [First-power boundary classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md) | 728857924504f28020dea5de6590ae3458b7bc90; bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue,7152 | Regular-binomial and opposite-collapsed equality families at a unit marked zero, distinct from quadratic equality. |
| [Two-family boundary stability](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md) | 437a2d57e99a6c3b61c514b2fee2e5121062f3cc; bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa,7220 | Regular/collapsed quantitative boundary context; this result stays in the interior collapsed lane. |

No earlier graph claim is silently promoted to a theorem about arbitrary
original-root paths. In particular, the angular energy optimum does not
automatically become the sharp radius-basin coefficient.

## Complementary lane and durable input

Researcher **six-sendov-1** owns the critical-reciprocal phase/radius
lane. Its [near-balanced origin-gap proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_origin_gap/PROOF.md),
source b3c2e98504f243383d4cf6e25287e0cfdaf4dfbc, graph
bafkreibx6rmuyl6c67qexb34aat5qawet2kvrwiqpr5ledhieusvecusfe,7478,
has been [independently confirmed with a fiftyfold wider radial strip](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_review2/REVIEW.md),
source a6f8a8b31b024d74164cee14b9f9d0ac97385662, graph
bafkreifeml4esrswaxfgyrdlfp3ylx6unlpfxaunjenvvbekpvxc6ydy2a,7506.
The fresh [actual-mean gap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md),
source 2893f22afbf54942a4d41455d6f1a503fb1c3535, extends polar forcing
across its full two-value radial range and gives a polar-feasible
comparison obstruction; its origin bridge remains open. Its committed
graph is bafkreigcprveajqf7doe6bmwbwt5lypodawzds4keugmdxzhk3jaeewvdi,
height 7518, read in the preclaim refresh.
These are contributions in critical-reciprocal coordinates, rather than
the original-root four-block curve (1). None is a premise of this proof.

The four-block coefficient and its algebraic optimizer are durable
original-root inputs for any later all-path reduction. Researcher
**six-sendov-3** adds the independent broader original-root/interior-motion
lane under the latest human contract. A preclaim source refresh found its
[full-motion theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_motion_quartic/PROOF.md),
source 25cba219635a3265d7f896359f144940d3a07f7a; the complete proof was
read. It reports the sharp energy-normalized collapsed quartic and its
extremal motion conditions over arbitrary disk motions at fixed a=5/8,
using the independently reviewed angular input. Independent review of
that extension is pending. It already covers the fixed-cutoff part
of our four-phase second-jet corollary. We credit the overlap and make
no new general-motion claim. Our direct Vieta derivation also permits
second-order marked-radius movement; the main distinct contribution
is the joint varying-radius displacement crossing and algebraic optimum
within the 3+3+1+1 curve. We retain collapsed angular/basin ownership and
coordinate through artifacts and the orchestrator.

## Remaining boundary

The new constant is exact within the specified conjugate-symmetric
3+3+1+1 curve. Its four-phase jet lemma also rules out increasing the
quartic deficit by second phase jets at those fixed first slopes.
Establishing the optimal universal root basin still requires displacement
optimization over unrestricted angular profiles and a joint moving-radius
reduction for paths outside this local profile and inward disk motion,
or another proof that they cannot give a stronger obstruction. The
fixed-cutoff full-motion energy theorem now supplies a pertinent reported
input for that next bridge, with review pending. The first-power endpoint is a separate
global inequality. The baseline at the cutoff is128/13, above8;
the local negative quartic gap does not refute that endpoint.
No general equality classification, universal phase bridge, full basin
optimum, external formalization rebuild or review of this result is claimed.
