# Sources and evidence boundary

* Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
  arXiv:2609.07041v2. The named problem is the all-hinge comparison for
  arbitrary bounded laws and 1-Lipschitz maps in dimension three.
* Ulrich Brehm, *Extensions of distance reducing mappings to piecewise
  congruent mappings*, Journal of Geometry 16 (1981), 187--193,
  [DOI 10.1007/BF01917587](https://link.springer.com/article/10.1007/BF01917587).
  The geometric extension is classical. The publisher's abstract was
  checked; the full original article was not available through that page.
* Anton Petrunin and Allan Yashinski,
  [Lectures on piecewise distance-preserving maps](https://arxiv.org/abs/1405.6606),
  arXiv:1405.6606, Lecture 2 and final remarks. The accessible proof was
  read, including its statement that Brehm extension holds in all dimensions.
* Kristian Bredies, Jonathan Chirinos Rodriguez, Emanuele Naldi,
  [On extreme points and representer theorems for the Lipschitz unit ball on finite metric spaces](https://link.springer.com/article/10.1007/s00013-024-01978-y),
  Archiv der Mathematik 122 (2024), 651--658, Theorems 2.2--2.3.
  Tight-graph extremality and the finite representer theorem are prior
  results. We do not infer hinge minimization from their convex decomposition.
* Holun Cheng, Ser Peow Tan, Yidan Zheng,
  [On continuous expansions of configurations of points in Euclidean space](https://arxiv.org/abs/1107.0140),
  Theorem 2.1 and equations (5)--(7). This supplies the simplex-flap
  geometry and nonliftability, with the original expansion reversed.
  The paper credits the independently constructed Belk--Connelly example.
  The checker here supplies neither a new construction nor a new proof
  of nonliftability.

The team's [paired-rank package](../gaussian_majorisation_rank_abel/README.md)
already records the finite witness reduction and the same 16-label flap.
Its source commit is `f7c122d6a5ade217930d63da27e67f9a9e55a539`;
graph contribution `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
The present checker generates the flap directly rather than importing that
package. Keeping output labels distinct is essential even when positions
coincide.

The team refresh included the fixed-atom reduction (graph height 6112),
axial robustness (6104), transverse matrix paths (6118), paired layers
(6100), ordered weights (6114), and researcher 7's completed negative
search report. These provide context, not premises of this proof. The
new reduction does not replace any hypothesis in those positive results.

Before publication, remote main was refreshed through
`007ec4fddd5566a57106a7b0464b34fa8d7ad8f2`. The additional inspected work
included [common-set transfer and diffuse optimizer localization](../gaussian_prior_localization/README.md),
[heat-profile comparison](../gaussian_majorisation_heat_profiles/README.md),
[finite orthogonal averaging obstruction](../gaussian_majorisation_finite_orbit_obstruction/README.md),
and the updated global and stability dependency handoffs. These are
complementary reductions or proof-method boundaries, not premises of
the mesh construction. In particular finite approximation of a strict
violation does not assert finite attainment of an optimized prior.

The contribution is the explicit all-hinge violation transfer to a rigid
mesh, its uniform-mass variant, and the finite fold-consistency formulation.
These are applications and consequences of the cited classical geometry;
no priority claim is made. The inspected sources did not contain this
specific combined formulation for the Gaussian question.

The universal statements are written analytic arguments. Exact rational
calculation checks the finite controls only. No finite computation here
proves the original conjecture or rules out every compatible fold pattern.
