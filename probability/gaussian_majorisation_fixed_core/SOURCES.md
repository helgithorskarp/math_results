# Sources, attribution, and scope

Checked 26 September 2026. The human-named problem source remains
Aishwarya--Li; the other papers are proof inputs or comparison context.

## Primary inputs

1. Gautam Aishwarya and Dongbin Li,
   [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/abs/2609.07041),
   arXiv:2609.07041v2, revised 13 September 2026. The source remained v2
   on the final prepublication check. Theorem 1.2 is the planar Gaussian
   comparison used in the fibre argument. Remark 1.9 supplies the optional
   single-full-support-measure route to equal-radius neighbourhoods.
   [Full text](https://arxiv.org/html/2609.07041v2).
2. Karoly Bezdek and Robert Connelly,
   [Pushing disks apart—the Kneser--Poulsen conjecture in the plane](https://arxiv.org/pdf/math/0108098),
   J. Reine Angew. Math. 553 (2002), 221–236.
   Corollary 1 gives planar union and intersection comparison for arbitrary
   radii. Corollary 3 already covers contractions whose displacements lie
   in one two-dimensional subspace. These are **prior results**, not new
   contributions of this packet. The new part is constructing such an
   alternative map while preserving the fixed core and target data.
3. Holun Cheng, Ser Peow Tan, and Yidan Zheng,
   [On continuous expansions of configurations of points in Euclidean space](https://arxiv.org/pdf/1107.0140),
   arXiv:1107.0140. Section 2 defines the simplex flaps and Theorem 2.1
   proves their labelled nonliftability below twice the original dimension.
   Scaling their tetrahedron and reversing the depth-one expansion gives
   equation (13) of our proof. Their ordered labels matter, including
   coincident target points. They credit the earlier Belk--Connelly
   construction. The configuration and nonliftability are not new here.

Kirszbraun extension and the Lebesgue density theorem are standard external
theorems used in the written proof. The elementary tangent-ball argument
spells out the boundary-measure step in the compact ball-union extension.

## Team dependencies and distinctions

- [Balanced twelve-ray Gaussian majorisation](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_ray_relabelling/PROOF.md),
  researcher 7. This supplies the strategy of changing a contraction while
  preserving its output law. Its particular map cannot fix a tetrahedral
  core. Our core-preserving map and five radial-measure constraints are
  different; neither full measure class contains the other.
- [Paired-rank reduction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_rank_abel/PROOF.md),
  our earlier contribution. Its rank-five theorem gives another proof after
  the new rematching. The present Gaussian proof instead uses the primary
  planar theorem directly and makes conditioning explicit.
- [Nested hulls and small rare mass](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_nested_hulls/PROOF.md),
  our preceding contribution. The new class has arbitrary core mass and
  every variance, but imposes measure balances. The old binary-weight
  obstruction to deterministic rematching remains outside this class.
- [Spherical-tail reduction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_spherical_tail/PROOF.md),
  researcher 5. It supplies a counterexample criterion, not a premise of
  the present proof. No spherical-tail search is duplicated here.
- [Sparse-energy comparisons](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_replica_curvature_sparse_energies/PROOF.md)
  and [high-noise hinge window](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_high_noise_window/PROOF.md),
  researcher 8. The latter arrived during this pass and was read before
  publication. Its universal high-variance threshold window and spherical
  range are complementary to the present all-threshold geometric class.
  These results are not proof premises here.

Immediately before the source push, two additional commits were read:
the [sparse Hankel hierarchy](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_sparse_hankel_hierarchy/PROOF.md)
gives every principal block of size $N$ at $s\ge24NR^2$, uniformly in its
indices, and the [independent replica review](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_replica_curvature_sparse_energies_review2/README.md)
accepts the earlier sparse-energy result with high confidence. Neither
settles the low-variance geometric comparison or changes the present proof.

The current shared graph and durable reports were checked at entry and
before publication, with no overlapping fixed-core contribution found.
The repository supplies the public mathematical source for the team
dependencies, including those whose graph submissions were initially
pending. Graph acceptance is not treated as proof validation.

## Novelty audit and remaining question

The primary texts above, the earlier team proofs, and targeted searches
combining Kneser--Poulsen or Gaussian majorisation with fixed core,
tetrahedron, cuboctahedron, octahedron, flaps, and relabelling were inspected.
No matching fixed-core construction or stated additive/maximum balance
class was located. The specific construction and corollaries are **new to
these searched sources**; this is a bounded novelty audit, not a priority
claim or a comprehensive literature classification.

The new all-radius result follows established planar geometry after a new
explicit change of target labels. It does not bypass planar Kneser--Poulsen,
prove the original labelled motion possible, settle all flap depths, allow
arbitrary unbalanced Gaussian masses, or settle general unequal radii.
The full dimension-three Gaussian majorisation problem remains open.
