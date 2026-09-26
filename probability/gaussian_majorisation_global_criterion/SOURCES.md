# Primary attribution and durable team inputs

Literature and bounded Team B neighbourhood refreshed on 2026-09-26.
This is a synthesis with a quantitative global certificate, not a claim
to invent stochastic order, Hausdorff moments or positive approximation.

## Primary literature

* Gautam Aishwarya and Dongbin Li, [Gaussian Convolution, Internal Energies, and
  the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  The sole problem source. Lemma 3.2 uses stochastic order of sampled
  density values and disintegration; Theorem 1.4 supplies such couplings
  for continuous contractions. Theorem 1.5 explains two-Gaussian-coordinate
  marginalisation; Theorems 1.8 and 5.1 give volume consequences, with
  the latter already treating variable radii by exponential weights.
  Our proof spells out the uniform-variable identity and
  the exact nonzero coupling defect rather than asserting a new coupling
  principle.
* Persi Diaconis and David Freedman, [The Markov Moment Problem and de
  Finetti's Theorem: Part I](https://www.stat.berkeley.edu/users/freedman/631.pdf),
  manuscript dated 15 June 2003. Theorem 1 and Lemma 1 recall the classical
  Hausdorff nonnegative finite-difference criterion. Our beta tests are
  precisely those differences for the existing hinge moments.
* Jian-Guo Liu and Robert L. Pego, [On generating functions of Hausdorff
  moment sequences](https://arxiv.org/html/1401.8052), introduction,
  equations (1)--(2). Another primary source for complete monotonicity
  of finite positive measures on `[0,1]`. We use no later generating
  function characterization or lemma affected by its appended corrigendum.
* Elena E. Berdysheva, Nira Dyn, Elza Farkhi and Alona Mokhov,
  [Metric Approximation of Set-Valued Functions of Bounded Variation by
  Integral Operators](https://link.springer.com/article/10.1007/s00365-024-09681-5),
  Constructive Approximation 61 (2025), 347--377, Section 5.1.
  This primary article records the classical Bernstein--Durrmeyer kernel
  used here. We derive the particular second moment and the Gaussian
  support bound directly. No set-valued approximation result is needed.

## Reused mathematical source

Direct reader links and precise implication boundaries are in
[DEPENDENCIES.md](DEPENDENCIES.md). These commits record the input
versions; links intentionally use readable branch paths.

| Input | Source commit |
|---|---|
| Complete hinge/Hankel reduction | `6f51c67737051a61290c070c9fb960e1da83b75b` |
| Local-lift obstruction | `c363e6b2e9db8cdb18b7a6ad787446f305712e92` |
| Paired-rank and Abel reduction | `f7c122d6a5ade217930d63da27e67f9a9e55a539` |
| Scalar-defect motion | `a8c8a21bde0eb356cf1fc302e3f9b13f1e9b113e` |
| Simplicial cone reflection | `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7` |
| Axial cone rotation | `984e1edaaf7f02bf4572c80754edff1e296fdd19` |
| Axial finite strong-composition obstruction | `8e8cb2a62e575adbf0ec3ff74e681ee9688f1768` |
| Uniform nonlinear axial robustness | `a63bee4157117a2d2abb2a358119dfd57ebb5a9d` |
| Damped cone reflection | `57ff1129224b92a88404817b164bf8c17bd2ecd1` |
| All-variance square-cone density orbits | `241e48a3c393b659ad90fbe5db145a6f58395d6e` |
| Compact-variance spatial-cloud stability | `b48c5ca31f3c573f2ffe6874944de83bc1a92710` |
| Bounded-law interior and finite positive certificates | `52ef6716a271b31ac1046207764fc78d3db6165c` |
| Paired-layer all-variance completion | `465f892ad569fe12fb2634395c21bc7025abff41` |
| Fixed-core relabelling | `e78d73bcae9a21f1344e74166153abe308bf51e9` |
| Common-target gluing | `3ad6ed0be174d1292b250efcad734d03eed01af5` |
| Common-target independent acceptance | `193f0e8fbf34bba8db0ef54d2aa87efa75de7034` |
| Sparse Hankel hierarchy | `c8df5163dd314544b4f2a611483ab192349a8119` |
| High-noise hinge window | `42fef5f197d9e601db9d1f637b84c4d6215a3039` |
| Spherical tail | `78b38b8cd6caab0e8ef8a7e0efa88b0d1da05f6f` |
| Eventual completion | `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6` |
| Eventual completion independent acceptance | `c750676fd6e164db43c0891c0093ebed2a49c356` |
| Asymmetric eventual certificate | `733f2f1ffeec6a97089fbdaa5bd89aa997da2240` |
| Atomic bridge obstruction | `d05dd54b551a5a14329cfbe31f8b66c13cc0e217` |
| Atomic obstruction independent acceptance | `b89f9f31a95637f92f7235a5693d2edbc5e530f6` |
| Covariance-free entropy rigidity | `a264d277a51683479424060972dafb44123db597` |
| Covariance-free independent acceptance and unsigned hinge bound | `fc25eff113b59c72fa820def81698e914a80d15b` |
| Signed tail-deficit obstruction | `54372e691479d94f8c4a6ee9a7c3a7ab4ffdac3d` |

The written proofs in this packet are self-contained for the global
criterion. Motion claims and the nine-point separation use the credited
team results at their stated status; their inclusion here is not a new
independent review. No priority or general-conjecture resolution is claimed.

## Geometric-endpoint annex

[GEOMETRIC_LIMIT.md](GEOMETRIC_LIMIT.md) specializes the primary Theorem 5.1
to one logarithmic weight path and gives the exact defect scale using our
global criterion. The variable-radius transfer itself is existing work.
The new finite classification concerns the particular coefficient cones
defined in the [square-cone orbit source](../gaussian_majorisation_square_cone_orbits/PROOF.md),
commit `241e48a3c393b659ad90fbe5db145a6f58395d6e`. Its original compact order
certificate is a hash-checked input to the annex audit, not an omitted
dataset. Four exact cone vectors prove attainability; eleven retained
inequalities prove necessity for all finite logarithmic profiles.

The relabelling explanation uses the already available
[paired-rank/coordinate-preserving mechanism](../gaussian_majorisation_rank_abel/PROOF.md)
and the primary planar majorisation theorem. It is included to establish
that the extracted radius family is not a new geometric consequence.
The refreshed [axial-cone scope statement](../gaussian_axial_cone_rotations/SCOPE.md),
commit `79f59b8ab07215fea46a00e8ca57381393d19f67`, also emphasizes the
distinction between new weighted Gaussian comparisons and new volume cases.
This annex does not classify alternative finite orders, arbitrary positive
weight families, or all valid Kneser--Poulsen radius assignments.

The prepublication refresh also incorporates the
[spatial-cloud stability proof](../gaussian_majorisation_open_stability/PROOF.md)
and [paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md)
at the commits recorded above. They supply additional exact-zero classes
in the dependency map, with their stated variance and weight quantifiers.
The annex explains the radius-matching scope of their immediate geometric
endpoints. They are author proofs awaiting review, not new premises of our
fixed-cone classification or independently accepted results here.

## Fixed-atom reduction and refreshed obligations

[ANCHOR_REDUCTION.md](ANCHOR_REDUCTION.md) is an analytic reduction of
the entire open question, using the same global defect. It combines an
explicit contractive anchor extension with the elementary nonnegative
hinge interaction and a Gaussian half-space overlap estimate. The
result is uniform over every threshold. The conditional near-Gaussian
consequences use standard mixture entropy, Gaussian translation, and
coupling identities derived there. These ingredients, and the standard
Kirszbraun extension, carry no priority claim. No counterexample is
assumed or constructed, and no new positive Kneser--Poulsen class is
claimed. The reduction requires no external computational certificate.

The prepublication refresh incorporates three durable advances:

* [Axial finite compositions](../gaussian_axial_cone_rotations/COMPOSITIONS.md):
  all finite aligned strong-coordinate chains are excluded on the stated
  rigid anchored class. This does not constrain post-convolution couplings.
* [Axial nonlinear robustness](../gaussian_axial_cone_rotations/ROBUSTNESS.md):
  a reserved scaling gives one domain-wide bound for nonlinear endpoint
  perturbations, all weights and variances, and arbitrary radii. Its
  geometric input is retained; this source does not cover arbitrary
  remote rare packets solely by their small probabilities.
* [Bounded-law stability](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md):
  strict mean-support and peak gaps and strict hinges describe the exact
  product `W_infinity` interior. Its finite positive moment certificate
  has signed endpoint and localization premises. The fixed-atom
  reduction explicitly records why neither a law-dependent neighborhood
  nor convergence in weaker distances supplies the unrestricted sign.

These author proofs are cited at their stated status, not independently
reviewed here. Their source commits are recorded in the table. The
paired-layer all-variance completion retains its separate spatial and
weight hypotheses. New private searches and finite positive moment
tables from the counterexample lane are not mathematical dependencies.
The fixed-atom reduction leaves the original arbitrary-weight square-cone
origin-adjunction question open; its remote-atom error tending to zero
does not imply positive comparison at finite separation.

The retained covariance-free theorem has an
[independent acceptance](../gaussian_majorisation_bridge_barrier/AUDIT.md)
in graph contribution `bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`
at height 5952. Its quantitative hinge consequence is unsigned. The
separate energy-only obstruction in that packet is not what this audit
accepted, and the audit does not establish the present fixed-atom proof.
