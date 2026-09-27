# Attribution, dependencies and class boundary

The sole target is Aishwarya--Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2),
the open full R3 Gaussian-majorisation question. The primary text was
refreshed on 27 September 2026. Theorems 1.4/1.5 and Sections 3/4 provide
the continuous-contraction pressure identity and two-Gaussian-coordinate
transfer used here. We claim neither that transfer nor a new motion
construction. No exhaustive historical-priority claim is made.

## Imported results

1. [Strict norm-preserving hinges](../gaussian_norm_preserving_strictness/PROOF.md),
   graph6552 `bafkreiaaaozmyiqftk7jr2rhn5mynqgbg5tlkqipifhsuknqwisuppifbi`,
   source `2106c12535f7ed647e8127ef17c14f899233d5e1`.
   Supplies the original strictness mechanism and lower peak estimate.
   [Independent acceptance6556](../gaussian_norm_preserving_strictness_review2/REVIEW.md),
   `bafkreibdtgkhspcetj67jwcay5rybfgaxavtg3dcyk3km6f5zedfzliidy`, accepts
   that source and independently audits the part of the openness theorem
   needed by its corollary. That acceptance does not review this new result.

2. [Bounded-law openness and finite certificates](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md),
   graph6102 `bafkreietfhclp4t463gjaeyh4ldpj2eeognjhwdphuywmdxyrepqwskdiu`,
   source `52ef6716a271b31ac1046207764fc78d3db6165c`.
   Theorems A/B supply the ambient-interior implication from strict width,
   peak and every nontrivial hinge; Theorem C supplies the finite beta
   interface. The original strictness review accepts the required Theorem A
   and compact-family clause; its finite-beta criterion remains an
   analytic author-proof dependency. General
   openness, damped interior approximation and the finite criterion are
   credited prior results, not new claims here.

3. [Compact width rigidity](../gaussian_compact_width_rigidity/PROOF.md),
   graph6534 `bafkreieshmqkav36fnjg7a7ueosamknjbg34fvzcf32vvy46n4rsbvfogu`,
   source `5d223e88146a2810294533718b1eaa3bb114b9a8`.
   Needed only for the ambient-interior corollary, not the hinge bound.
   [Independent acceptance6544](../gaussian_compact_width_rigidity_review2/REVIEW.md),
   `bafkreidctjnig5ahlqrkazspxs33ui2dkprn2qwh56lwk3ewlaqzmmcjiu`, source
   `c40800e7363064366fad5a879bdbede0aad15136`, accepts its compact equality
   characterization and specified consequences.

4. [R3 polynomial hinge margins](../gaussian_polynomial_hinge_margin/PROOF.md),
   graph6558 `bafkreifay5h7ipbz7ixgkxptyoeciryy6fowgquwhhk5fp2cyhjuux5sqq`,
   supplies 2^-(40R^2+9R+38)tau^3 epsilon^8 for N steps and the logarithmic
   radial-cutoff refinement. This is an author proof pending independent
   review. We use that improvement rather than extend the older exponential
   threshold schedule separately. The five-dimensional motion estimate and
   chain-loss allocation are the new functional arguments here.

[DEPENDENCIES.json](DEPENDENCIES.json) pins these six files and their source
revisions. The checker checks their content hashes. Each pin was also
compared with `git show` of its stated source revision before publication.

## Relation to the team's existing classes

The [geometric portfolio, Section 2](../gaussian_geometric_portfolio/CLASSIFICATION.md)
already records non-strict comparison under arbitrary compatible finite
composition and concatenation of R4/R5 motions in R5. The present theorem
adds a coefficient independent of the number of steps and retains strictness
under the specified bounded-radius limits. It does not count composition
closure itself as a new positive class.

The [R2 balanced certificate](../gaussian_balanced_loss_certificate/PROOF.md),
[R3 affine-component localization](../gaussian_affine_component_localization/PROOF.md),
and [R6 nonlinear parallel slices](../gaussian_parallel_slice_contractions/PROOF.md)
can supply motions to Theorem A, within their original domains and with the
regularity in our Section 1 checked for the chosen construction. We impose
no new scalar beta-sign condition on them. Finite certificate consumers
still need signed endpoints; an absolute integration error is not converted
to a loss-proportional error by this theorem.

R2's [effective anchored neighborhoods](../gaussian_effective_anchored_neighborhoods/PROOF.md)
already combine the polynomial N margin with width and peak guards into a
quantitative perturbation budget. We do not duplicate that producer or claim
its finite guard automatically covers arbitrary M certificates. The present
motion/chain theorem supplies a broader middle-margin input when the other
endpoint guards are separately established.

The [proper-screw mixed-chain obstruction](../gaussian_screw_primitive_obstruction/PROOF.md)
excludes its cited labeled configuration even from limits of these finite
certificate chains. That author result is a geometric boundary, not a
Gaussian-majorisation counterexample. We do not claim the present theorem
signs R2's unsigned screw pilot or R7's adversarial mixtures.

The new functional steps are the reverse-posterior upper peak budget,
extraction of the five-dimensional pressure on a level-crossing annulus,
and use of only the final eligible loss budget in a chain. No covariance-free
entropy-rigidity claim or scalar-moment-to-majorisation implication is
assumed. Exact author controls accompany the analytic proof; independent
review and formalization remain pending.
