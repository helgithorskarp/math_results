# Sources, dependencies, and scope

The sole problem source is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, revised 13 September 2026 and checked live on
26 September 2026. Conjecture 1.1 is the target. Theorem 1.2, which gives
full planar majorisation, is the analytic input to the fibre proof.
Kirszbraun's Euclidean Lipschitz extension theorem is the other standard
external theorem used. The hinge characterization, Jensen inequality,
Tonelli, and the tree-flow estimate are proved or explained in the text.

## Direct team dependency

Researcher 6's [fixed-core rematching](../gaussian_majorisation_fixed_core/PROOF.md)
constructs the coordinate-preserving map, identifies its common fixed
tetrahedral core, proves full comparison under a different set of five
exact balance identities, and rules out a single core-fixing rank-five
realization for uniform rays. Its proof was read in full. We use its map
and the planar-fibre argument, give the three cyclic versions explicitly,
and repeat the short geometric and analytic verifications so the new
convex-decomposition argument can be checked locally.

- Source commit: `e78d73bcae9a21f1344e74166153abe308bf51e9`.
- PROOF.md SHA256:
  `3d27c688021345da8a58132370e5610b2dd4718ad859b395defbfaddcb8b04ce`.
- Committed graph reference:
  `bafkreih4dtcjm33xgje4uavijwtb4rsytcvo3axlaritcx2zmha3j43gre`, height 6026.

The original uniform law does not satisfy that paper's five balances.
Our three source components do not individually need to retain their
original `S`-images: their coordinate-preserving images instead all equal
the original uniform law's target. This common-target convex decomposition
is the new bridge. The neighborhood of unequal weights follows from
strict positivity of the uniform splitting and connectivity of its
incidence graph, with an explicit L1 estimate.

## Results extended or distinguished

1. Researcher 5's
   [eventual-variance endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md)
   proves all thresholds at sufficiently high variance under a spherical
   gap condition. Its arbitrary tetrahedron-background application uses
   uniform flaps at one radius. The present theorem removes that variance
   restriction for this application, permits arbitrary bounded radial
   laws, and allows a full-dimensional set of unequal weights. Its general
   spherical-gap and martingale criteria are separate results, not
   superseded or used as proof premises here.
   Commit: `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`.
   PROOF.md SHA256:
   `9adbd6c07b271a12252b13c35d76835a2d6edc0592f3dd7285a2d950c9ba330f`.
   Graph: `bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`,
   height 6032.
2. Researcher 7's
   [balanced-ray theorem](../gaussian_ray_relabelling/PROOF.md)
   already proves the unanchored uniform case at every variance, using a
   single alternative matching. Its map cannot fix the tetrahedral core.
   Commit: `4ae1468058b90d7d8c9040153dc68853cc39cba1`.
   Graph: `bafkreiayrirznkna2pchblkswn3y73kyakolixti5zzacaejxotdgibtfu`,
   height 5998.
3. The earlier
   [nested-hull theorem](../gaussian_majorisation_nested_hulls/PROOF.md)
   has small perturbing mass around an origin atom at each fixed variance.
   No such origin atom or small mass is assumed here. The new result still
   requires the displayed geometric support and weight condition.
4. Our [sparse Hankel hierarchy](../gaussian_sparse_hankel_hierarchy/PROOF.md)
   controls every principal size-N block when `s >= 24 N R^2`, for `N>=3`,
   for arbitrary bounded contractions. It remains preserved at commit
   `c8df5163dd314544b4f2a611483ab192349a8119`, graph
   `bafkreih5ygxepusexo3w53mvz6sjww4tir4gsjenwieqs6bnttybpu6lca`, height 6010.
   The new geometric class has every order and every variance at once.
   No moment-limit argument from the hierarchy is used here.
5. Our [replica-curvature theorem](../gaussian_replica_curvature_sparse_energies/PROOF.md)
   has received an [independent accepting review](../gaussian_replica_curvature_sparse_energies_review2/README.md)
   at commit `0a8dd763bb1069cc1d9ae889950b32f577555642`, graph
   `bafkreia7yvpc2u26ovjpwdfblycgbsg2zd3vdcqab2ehjzx57v2x62oy34`, height 6020.
   This review concerns that earlier result, not the present theorem.
   The [covariance-free entropy audit](../gaussian_majorisation_bridge_barrier/README.md)
   and its obstruction to energy-only majorisation inference also remain
   preserved; they are not replaced by assuming entropy controls hinges.

During the final refresh, researcher 7 published
[simplicial-cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md),
commit `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`, graph
`bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`, height 6042.
Its proof was read. It settles all dual-basis central flips using an
explicit five-dimensional motion and supplies a nine-point nonsimplicial
obstruction. The latter is a direct dependency of our Theorem B's
nine-point corollary: injective finite contractions admit no enlargement
by pre-Gaussian common-target mixtures of deterministic maps, so its
binary-weighted fixture cannot be addressed by such mixtures of
five-dimensionally liftable contractions. The geometric nonliftability
is credited to researcher 7; the finite-mixture rigidity proof is given
here. This dependency does not enter Theorem A.
Its PROOF.md SHA256 is
`6495916425b70062986e55beef5e472f4d2deacfe93bd46f92ea365521713842`.

## Literature and trust boundary

The primary manuscript, the relevant committed neighborhood, the latest
bounded teammate reports, and all intervening Team B source commits were
inspected before publication. Searches combining Gaussian majorisation,
contractions, mixtures, common targets, and tetrahedral flaps did not
locate this explicit three-source decomposition. This is a bounded audit,
not a historical-priority claim. Convexity of the set of densities
majorised by one fixed density is elementary and is not claimed new.

The support-level equal- and unequal-radius results in the fixed-core
paper are prior team results. Adding this Gaussian weight class supplies
no new KP conclusion for the same supports. The full conjecture and
arbitrary unequal ray weights remain open. Infeasibility of our particular
splitting equations does not refute majorisation, as the point-mass
control demonstrates exactly.

All source links name real files on the authorized repository's `main`
branch. Commits and file hashes identify the versions read. The graph
uses `proof_attempt` for this complete but not independently reviewed
author proof. Publication, finite checking, and graph commitment are
not treated as mathematical peer review.
