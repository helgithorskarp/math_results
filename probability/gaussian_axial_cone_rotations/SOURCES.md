# Sources, dependencies, and scope

The sole problem source is the full bounded-input dimension-three
Gaussian-convolution majorisation question in Aishwarya--Li. Primary source
revisions and the committed Team B neighborhood were checked on
26 September 2026 before publication.

The later consolidation in [SCOPE.md](SCOPE.md) keeps the original theorem
and checker intact, proves the reverse class comparison with the standard
orthant, and applies the team's later scalar-defect and common-target
obstructions to the existing fixture. Primary revisions and current Team B
work were refreshed again for that consolidation.

## Primary inputs

- Gautam Aishwarya and Dongbin Li,
  [*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
  Conjecture*, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  The source remains v2, revised 13 September 2026. Conjecture 1.1 is the
  target. Theorem 1.4(i)(a) supplies the density-value order under a continuous
  contraction; equation (17) of our proof converts its five-dimensional
  application into the desired three-dimensional hinges. Theorem 1.8(i)
  supplies the compact equal-radius consequence. The implication from at most
  two auxiliary coordinates is explicitly already stated in the source.
- Karoly Bezdek and Robert Connelly,
  [*Pushing disks apart—the Kneser--Poulsen conjecture in the plane*,
  arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
  Theorem 1 transfers a piecewise-smooth expansion in `R^(n+2)` to union and
  intersection volume comparisons in `R^n` for arbitrary radii. Our motion
  gives its hypothesis. Corollaries 3--5 provide the displacement-dimension,
  small-cardinality, and partial positive-dilation comparisons used to assess
  scope. No claim of novelty is made for this volume implication.
- Karoly Bezdek and Marton Naszodi,
  [*The Kneser--Poulsen conjecture for special contractions*,
  arXiv:1701.05074](https://arxiv.org/abs/1701.05074).
  Section 1.2 defines strong contraction by decreasing every coordinate
  distance; its examples include one-sided coordinate reflections. Our
  finite fixture fails that criterion, including after independent rigid
  alignments. This does not exclude every composition of existing methods.
- Mojzesz D. Kirszbraun,
  [*Über die zusammenziehende und Lipschitzsche Transformationen*,
  Fundamenta Mathematicae 22 (1934), 77--108](https://doi.org/10.4064/fm-22-1-77-108).
  The classical Euclidean extension theorem puts our domain maps in the
  global 1-Lipschitz formulation. The motion and comparisons on their stated
  domains do not require constructing an extension explicitly.

Cauchy's planar perimeter formula is proved in the form needed in Section 1
by polygonal projection and approximation. The bound `pi < 22/7` follows from
the positive rational integral written in Section 5, whose polynomial identity
is checked exactly. Neither constant is inferred from a numerical sample.

## Durable team work inspected

- [Paired affine rank and Gaussian cancellation](../gaussian_majorisation_rank_abel/PROOF.md),
  source commit `f7c122d6a5ade217930d63da27e67f9a9e55a539`, graph
  `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
  Its two-coordinate sampling identity is reproduced in Section 3. Our new
  motion works at paired rank six, so it uses a different sufficient geometry.
- [Simplicial cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md),
  researcher 7, source commit `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`, graph
  `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`.
  Its full proof was read. It contracts two rigid clusters in five dimensions
  when an intermediate simplicial cone exists. The triangle argument in
  Sections 4--5 proves that our circular class includes domains and a finite
  fixture outside every such separator. Section 4.1 now proves reverse
  noncontainment using the standard orthant, allowing every common axis.
  Its nine-point square-cone obstruction remains a
  separate adversarial target, not decided by the theorem here.
- [Fixed-core rematching](../gaussian_majorisation_fixed_core/PROOF.md),
  this lane, source commit `e78d73bcae9a21f1344e74166153abe308bf51e9`, graph
  `bafkreih4dtcjm33xgje4uavijwtb4rsytcvo3axlaritcx2zmha3j43gre`.
  That result fixes a tetrahedral core and changes ray labels to preserve
  selected output laws or decorated unions. Here the original map itself
  moves continuously in four dimensions, with arbitrary weights and radii.
- [Eventual full majorisation from spherical gaps](../gaussian_majorisation_eventual_endpoint/PROOF.md),
  researcher 5, source commit `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`, graph
  `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`.
  This and its fresh
  [independent review](../gaussian_majorisation_eventual_endpoint_review2/README.md),
  source commit `c750676fd6e164db43c0891c0093ebed2a49c356`, were read in full.
  The review accepts the endpoint theorem with high confidence; it does not
  review the present cone theorem. The endpoint's spherical condition and
  large-variance restriction are not premises of this work.
- [Common-target convex decomposition](../gaussian_majorisation_common_target/PROOF.md),
  researcher 8, source commit `3ad6ed0be174d1292b250efcad734d03eed01af5`, graph
  `bafkreiefowbrpgnu2cjyyuyig4y2gzk5zdchubp3xqpcgu2rzzpy5fe25m`.
  The fresh full proof was read before publication. It now treats uniform
  tetrahedral flaps and a neighborhood of unequal weights at every variance,
  with arbitrary fixed core and radial laws. Its injective-target rigidity
  theorem explains a limitation of deterministic source mixtures. Our cone
  fixture is injective; our positive result follows its original labels and
  uses no such mixture. The previously open uniform-flap Gaussian continuation
  of our fixed-core pass is therefore parked as resolved by this source.
- [Atomic bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md),
  researcher 7, source commit `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`, graph
  `bafkreihqcqwjylfikk74mclhloshmpkpap7xdr233z6bu2rw7wryagqx2i`.
  This arrived at the final repository refresh and its full proof was read.
  The nine-point square-cone law has an open set of asymmetric weights
  excluding both martingale certificates and common-target decompositions
  into five-dimensional motions. It also has a quantified obstruction to
  nearby component output weights. These are barriers to those methods, not
  Gaussian counterexamples, and do not affect the present positive motion.
- [Scalar transport-defect budget](../gaussian_majorisation_scalar_defect/PROOF.md),
  researcher 5, source commit `a8c8a21bde0eb356cf1fc302e3f9b13f1e9b113e`, graph
  `bafkreidpgtehewdn2wn72hfi4c6aoq5bohkdss6dv36o37rjyxg6ndzxlq`.
  Section 6 already excludes norm-preserving anchored flips when both
  clusters span three-space. We credit that obstruction, specialize it to
  our fixture, and provide a small matrix certificate. No new scalar
  obstruction theorem is claimed.
- [Damped cone reflections](../gaussian_damped_cone_reflections/PROOF.md),
  this lane, source commit `57ff1129224b92a88404817b164bf8c17bd2ecd1`, graph
  `bafkreif2xczco4rxrlznq6cbvtv3qt6pdbhsce6vkl6ynfvh7h6k6vf3nm`.
  The product-cost criterion contains this axial motion at damping one.
  The wider class uses smaller damping and changes the endpoints. Its
  full exact-dual-cone obstruction to five-dimensional motions is not an
  obstruction throughout the interval between our circular threshold and
  the dual boundary, and is not a Gaussian counterexample.
- [Asymmetric eventual majorisation](../gaussian_asymmetric_eventual_majorisation/PROOF.md),
  researcher 5, source commit `733f2f1ffeec6a97089fbdaa5bd89aa997da2240`, graph
  `bafkreih6hv45oxpx3stcfy7ucq3b7bcdwrexn5kxm6aevahfnvwxd36qom`.
  It gives all hinges for an asymmetric nine-atom law at variance at least
  13200 and a full-dimensional weight neighborhood at variance at least
  16896. It is a different class with a variance threshold and no claimed
  new Kneser--Poulsen consequence. The newly arrived orbit theorem below
  removes those variance restrictions on a larger weight neighborhood.
- [Tail-deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md),
  researcher 8, source commit `54372e691479d94f8c4a6ee9a7c3a7ab4ffdac3d`, graph
  `bafkreidevccw36nby6zvy3vp5ae2j5lzbpji27qctfk4uyiqib7iwhrku4`.
  Its failure of a proposed uniform stability modulus and signed test at
  spherical zeros are limitations of other methods. It supplies no negative
  hinge and imposes no additional assumption here.
- [Square-cone orbit comparison](../gaussian_majorisation_square_cone_orbits/PROOF.md),
  researcher 8, source commit `241e48a3c393b659ad90fbe5db145a6f58395d6e`, graph
  `bafkreicpvcw53nvwenb2uiq7fk5fhuhl6sqcnwgucw5bgrgcjsj6m65lfu`.
  Its full proof was read at the publication refresh. Exact polynomial
  orders on 48 signed permutations and a finite upper-set correlation
  certificate establish all hinges at every variance on the asymmetric
  nine-point weight ball of radius 1/552. A bounded radial extension uses
  explicit cones of directional weights. It compares densities after
  smoothing, preserving the validity of prior center-law and motion
  obstructions. It claims no new Kneser--Poulsen case. This is coordination
  context, not a premise of the axial proof.
- [Global coupling and moment criterion](../gaussian_majorisation_global_criterion/PROOF.md),
  researcher 5, source commit `3177065da9c38e8735e8c1b39c41510e43e4bcde`.
  Its proof and dependency map were read at the final repository refresh.
  The least endpoint density-value coupling failure equals the largest
  failed hinge and the limit of a complete finite-difference hierarchy.
  It incorporates the axial motion as a sufficient zero-failure
  construction, without enlarging its domain or transferring a finite
  positive moment test to full majorisation. It is not a premise here.

The later independent reviews of the
[common-target source](../gaussian_majorisation_common_target_review2/README.md),
source commit `193f0e8fbf34bba8db0ef54d2aa87efa75de7034`, and the
[atomic bridge source](../gaussian_atomic_bridge_obstruction_review1/README.md),
source commit `b89f9f31a95637f92f7235a5693d2edbc5e530f6`, were also inspected.
Neither is a review of the axial theorem. No review or objection to the
axial theorem was present in the committed incoming neighborhood at the
consolidation's initial graph refresh.

The common-target, eventual-variance, and fixed-core results are coordination
context, not analytic assumptions hidden in our proof. The new motion and
separator proof are self-contained. No generic Gaussian cancellation,
instantaneous Hankel positivity, or all-threshold inference from finitely
many energies is assumed.

## Novelty boundary

Targeted live searches covered central reflections, circular or polar cones,
two rigid clusters, low-dimensional contracting motions, rotation criteria,
and Kneser--Poulsen inequalities for special contractions. The three primary
geometric/analytic sources above and the current team sources were inspected.
No identical axial motion, perimeter criterion, or circular-cone threshold
was located. This is a bounded novelty check, not a historical-priority proof.

The asserted advance is the explicit geometric criterion and its full
Gaussian and arbitrary-radius ball consequences. The `2/pi` threshold is
optimal for the stated axial form only. Larger cone domains, other motions,
and the unrestricted dimension-three question are left open. The rational
fixture's exclusion from the listed prior criteria is proved; exhaustive
exclusion of every possible prior method is not asserted.

The consolidation makes a further narrow comparison, not a new positive
subclass: the standard orthant is in the simplicial class but outside this
perimeter criterion under every common axis. A common-target comparison
with forced labels additionally uses distinct positive weights; injectivity
alone does not prevent rematching equal-weight labels. These qualifications
are recorded with proofs in Sections 4.1 and 5.1.
