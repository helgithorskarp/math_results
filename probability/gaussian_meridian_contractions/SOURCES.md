# Sources, attribution and class boundary

Source audit: 27 September 2026. Correctness and historical priority are
separate questions. This author proof has not yet received independent
acceptance.

## Primary mathematical inputs

1. **K. Bezdek and R. Connelly, Pushing disks apart — the Kneser--Poulsen
   conjecture in the plane.** [Version inspected](https://arxiv.org/pdf/math/0108098v1),
   Sections 2-3, Lemma 1 and Theorem 1. The planar leapfrog and the
   R^(n+2)-motion-to-n-dimensional-volume theorem are credited inputs.
   Corollaries 3-5 give the displacement-rank, small-number and partial
   dilation comparisons. Section 2 credits the lifting idea to
   Alexander's earlier work. That original 1985 text was not newly read;
   the attribution here follows Bezdek--Connelly. We do not claim a new
   general leapfrog or ball-volume transfer.

2. **G. Aishwarya and D. Li, Gaussian Convolution, Internal Energies, and
   the Kneser--Poulsen Conjecture.**
   [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
   Theorem 1.4(i)(a) and the paragraph after Theorem 1.5. The sampled-density
   comparison and the sufficiency of at most two auxiliary coordinates
   are explicit antecedents. Formula (9) in our proof spells out that
   existing cancellation. The human-named full dimension-three question
   is the sole problem source; it remains unresolved here.

3. **K. Bezdek and M. Naszodi, The Kneser--Poulsen conjecture for special
   contractions.** [arXiv:1701.05074v4](https://arxiv.org/html/1701.05074v4),
   Section 1.2 and Theorem 1.3. The strong-coordinate theorem is comparison
   context. Our variable normal-eigenvector argument excludes one directly
   aligned strong contraction for the full conical benchmark map. It does
   not exclude finite compositions with changing frames, or all possible
   deductions from that paper.

The proposed contribution is the meridian lift: retain planar leapfrog
coordinates for the meridian displacement while revolving only the
nonincreasing transverse interpolation. The resulting pair decomposition
has two independently nonincreasing terms. This supplies a motion uniformly
for the entire azimuth-preserving class, including coupled two-variable
maps and reversals. The two-dimensional meridian geometry is not a
rotational-symmetry assumption on the input measure.

A bounded targeted search of the primary literature and the committed
team graph found no statement of this entire meridian class. Queries used
meridian/meridional, azimuth, rotational/axisymmetric and cylindrical
contractions together with Kneser--Poulsen. Searches and a short comparison
list cannot establish historical priority or exclude indirect composition
arguments. No claim of first discovery is made.

## Durable team context

* [Radial profiles](../gaussian_radial_contractions/PROOF.md), graph6317,
  `bafkreiequbwj2ms2eev5sydi5exukocl3ycgaryq5bcywqxypf367hgoui`.
  The earlier scalar-radius decomposition suggested separating meridian
  and angular terms. The new theorem includes those radial maps but uses
  two auxiliary coordinates instead of their sharper one. Their source
  and the subsequent convex-core extension are unchanged.

* [Scalar defect](../gaussian_majorisation_scalar_defect/PROOF.md), graph6066,
  `bafkreidpgtehewdn2wn72hfi4c6aoq5bohkdss6dv36o37rjyxg6ndzxlq`.
  The norm-preserving rank-six obstruction and the written Gaussian
  cancellation are credited precedents. The new exact benchmark uses
  that obstruction; the obstruction itself is not newly claimed.

* [Directional normal bundles](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md),
  graph6418, `bafkreidifxh4fbjb7cgjhs6p36ngsrlybpltu4axyiwdwkic7dsogtk574`,
  accepted in [review6424](../gaussian_directional_normal_bundle_review2/REVIEW.md),
  `bafkreibhmuskn3vq7rqrr3ymhd4ju3jwmcabijyfh353fwzp62zvzslehe`.
  Those maps fix a convex core and move on its outward normal rays. Here
  the two meridian outputs can mix both input coordinates. Arbitrary
  angular factors in the normal theorem need not be axisymmetric, so no
  containment of that entire theorem is claimed. The global example (11)
  is not a convex-normal map in the displayed coordinates. The conical
  benchmark (12), considered alone, is a signed normal reflection; it is
  evidence about direct rank/scalar criteria, not the claimed class advance.

* [Axial cones](../gaussian_axial_cone_rotations/PROOF.md), graph6062,
  `bafkreiao6gmik3rvanspc76z6zukxlkk447ylprpkitnt6ht6tmdayl2zy`, and
  [matrix paths](../gaussian_axial_cone_rotations/MATRIX_PATHS.md), graph6118,
  `bafkreigbbgjyf5dy5wbhowdlqdrsc24ykargcfqfc6xzir4lvktnyxzmry`, are
  preserved geometric flagships. Their rigid-cloud relative Gram paths
  differ from the two-variable meridian mechanism. No optimization or
  annex to those packages is added here.

* R4's concurrent [tangential screw construction](../gaussian_tangential_screw_lift/PROOF.md),
  graph6456, `bafkreigfdheebqbnx6pzws2o2ekbzwhj4w4rmqe6w4g6zz6ryp6ufm55p4`,
  supplies a distinct positive geometric handoff: one rigid region makes a
  quarter turn and an axial translation while another is fixed. Its
  rank-one completion permits an azimuth change. It is not a premise of
  the meridian proof and is not subsumed by its azimuth-preserving form.
  Both constructions give full comparisons for arbitrary priors; neither
  classifies general extremal maps or arbitrary screw matchings.

* R1's concurrent [reflection-group orbit alignment](../gaussian_coxeter_alignment/PROOF.md),
  graph6462, `bafkreiap5q7gewx57jgrfkphj2mry345nto6aalsq7q72gg6qxebkvt2di`,
  is an independent algebraic class. It requires uniformity within each
  rotation orbit, and ball radii constant within each such orbit. The
  meridian theorem instead assumes an equivariant map and permits entirely
  arbitrary measures and individual ball radii. No containment is asserted.

The scalar obstruction is used only in the class comparison, and none of
these team theorems is needed as an unproved analytic premise: Sections 2-3
of the new proof give the motion and its cited transfers explicitly.
The team's accepted cap and closed flap theorems are left intact. No
claim of exclusion from every finite composition of accepted classes is
made. The current moment, covariance, contact and small-loss estimates are
not dependencies. This artifact does not take ownership of extremal-map
classification or adversarial counterexample search.

## Reproduction and trust boundary

Run `python3 -B verify.py`, `python3 -B -O verify.py`, and
`sha256sum -c SHA256SUMS` in this directory. CPython 3.11.2 was used;
only standard-library integer and rational arithmetic is required.

The checker expands the universal identity and derivative symbolically,
compares actual coordinates on six exact families, checks affine-in-time
pair derivatives on the whole interval, computes rank determinants for
seven labels and rejects four invalid hypotheses plus two broken motions.
It also detects omission of either auxiliary term in the formal identity.
The record is deterministic and regenerated by `verify.py --emit`.
The written proof, not finite controls, establishes the infinite class,
the measure-level statement, the all-radii conclusion and the comparison
with strong coordinate maps. No private input, solver, quadrature or
omitted large artifact is required. Author computation is not independent
peer review or formal verification.
