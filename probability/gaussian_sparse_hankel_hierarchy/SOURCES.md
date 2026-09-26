# Sources, novelty boundary, and team dependencies

The single problem source is
[Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1 for bounded probability measures in dimension three.
It was rechecked live on 26 September 2026; v2, dated 13 September 2026,
remained current. The source's replica formula and continuous-lifting
framework are prior work. The all-threshold, small-variance hypothesis
required for the geometric implication is still missing here.

## Direct mathematical dependencies

- [The exact Hankel reduction](../gaussian_majorisation_hankel_transport/PROOF.md),
  graph `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm`,
  source `6f51c67737051a61290c070c9fb960e1da83b75b`, identifies the
  hinge moments and the full hierarchy of square-curvature polynomial
  certificates. The universal equivalence is credited there, not here.
- [The signed high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md),
  source `42fef5f197d9e601db9d1f637b84c4d6215a3039`, supplies the exact
  weighted-coarea half-derivative identity and quantitative positive
  window. Its graph broadcast reference is
  `bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q`,
  still uncommitted at this pass's initial height-5995 query. The inspected
  public proof is the mathematical dependency; graph commitment is not
  assumed. Our Section 2 rechecks the necessary normalization and derives
  the new global absolute estimate proportional to the same deficit.
- [Sharp replica curvature and sparse energies](../gaussian_replica_curvature_sparse_energies/PROOF.md),
  graph `bafkreigxtycueb6re2fvuohmmqw3er5l76jddrbhbyv2nqexhj6w7x356y`,
  source `5586f0d772d6b7861bd73207901e183690f4d22b`, proves order-two
  positivity and supplies the zero-deficit case. Its optimal raw-replica
  curvature loss remains preserved. Order-two signs alone are insufficient
  for the present conclusion; the weighted tail information is new input.
- [The earlier finite-level theorem](../gaussian_contraction_high_noise_quartics/PROOF.md),
  graph `bafkreig737fhqpda2iz657ruh6clkymbesvt2a53sw4suywpqb7obwgkay`,
  source `a68f3a7c2d3e1c2141d43d2ea00eca76635ba964`, gives exponentially
  growing sufficient constants for consecutive blocks (12015 at order
  three). The new theorem gives a linear bound and arbitrary index sets;
  it is not merely a new entry in that earlier finite table.

## Approximation-theory context

Sparse polynomials `sum c_i u^(k_i)` and their exponential-coordinate
forms are classical Müntz polynomials/Dirichlet sums. Remez-type control
for such spaces is established literature; see the primary source
[Borwein--Erdelyi, Müntz spaces and Remez inequalities, arXiv:math/9501225](https://arxiv.org/abs/math/9501225),
and their author-hosted
[Generalizations of Müntz's theorem via a Remez-type inequality for Müntz spaces](https://www.cecm.sfu.ca/~pborwein/PAPERS/P107.pdf).
Our one-sided finite-dimensional bound is proved by elementary Newton
interpolation, with its hypotheses and constants explicit. We neither
claim a new general Remez principle nor invoke a theorem for a different
exponent class as a premise. The contribution is the quantified bridge
from the signed Gaussian window to every finite principal Hankel order.
The literature check does not establish historical priority.

## Teammate awareness and closed routes

The newest reports and source commits from researchers 5--7 were inspected
at pass start. Researcher 5's spherical-tail/ball-hull reduction,
researcher 6's full small-mass nested-hull theorem, and researcher 7's
balanced twelve-ray relabelling theorem are recorded in the preceding
window package and retained here as settled complementary scopes.
No optimal-transport construction, independent generic internal-energy
route, or counterexample search is duplicated by this pass.

The actual instantaneous-lift obstruction
(`bafkreifseyjs3jimzu7yvo3lpfd3555dmnf5q6hraqdonaldti3nqjgxqy`) remains
respected: the only sign used is the proved restricted window. Outside
it we bound the absolute value. Entropy rigidity and abstract Abel
positivity are not used to infer a missing sign.

## Computational trust boundary

The checker imports only the standard library and
`gaussian_majorisation_hankel_transport/bounds.py`, pinned to SHA256
`60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7`.
This is credited reused interval code. New exact Newton interpolation
and binomial moment calculations audit different parts of the argument.
Finite homothety examples are positive controls, not evidence of a
previously unknown full Gaussian class. The abstract negative determinant
is from the prior replica-curvature package and is only a checker control.

All universal statements are analytic author proofs awaiting independent
review, including the source-window dependency. No proof-assistant or
independent peer-validation claim is made.
