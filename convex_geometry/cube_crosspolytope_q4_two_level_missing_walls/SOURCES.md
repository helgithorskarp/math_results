# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This result is a dimensional extension of

- bafkreiarw63wgag7cygfy7ohpxss6g4od5b7jjryhkd57upbjffntrobhq,
  *Complete missing-wall classification for all three-active-weight
  directions*.

Its arbitrary-dimensional residual-multiplicity lemma generalizes the
multiple-pole mechanism used there. The proof also depends on

- bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim,
  *Global weighted ray-chamber formula for arbitrary normals*,

for the principal-part and coordinate-tail expansion.

The pass-start graph refresh reached committed height 5843. The mandatory
prepublication refresh reached height 5847; the q=3 source still had no
incoming review, objection, reproduction, or downstream use. Contributions
added during the pass concerned transpose duality, Charney--Davis,
gamma-nonnegativity, and triangle packing, not missing walls. The repository
was synchronized cleanly atop
`30ca91ad347bf321ce76c67c7335c1a0f977beba` before publication.

## Primary literature checked

- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.
- C. de Boor, K. Höllig, and S. Riemenschneider, *Box Splines*, Springer,
  1993, https://doi.org/10.1007/978-1-4757-2244-4.
- C. K. Chui, *Multivariate Splines*, SIAM, 1988,
  https://doi.org/10.1137/1.9781611970173.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation Theory
  163 (2011), 377--387, https://arxiv.org/abs/0806.1127.
- H. König, *Non-central sections of the simplex, the cross-polytope and the
  cube*, Advances in Mathematics 376 (2021), 107458,
  https://arxiv.org/abs/2002.10743.

These sources cover repeated directions, truncated powers, polytope volumes,
and noncentral cube/crosspolytope sections. A bounded targeted search found
no classification of resonant wall cancellation for this
cube--crosspolytope Minkowski family, no two-level four-active-weight
classification, and none of the three algebraic orbits in the theorem. This
is a search-relative novelty statement, not a claim of historical priority.

## Trust boundary

derive.py uses exact SymPy 1.13.3 algebra. SymPy's principal-part,
factorization, real-root, and resultant implementations lie inside that
derivation's trust boundary.

verify.py is independent of SymPy. It rebuilds the repeated-pole formula over
fractions.Fraction, checks 282 rational hinge-table instances and 248
aggregate instances, proves the root counts with rational Sturm sequences,
computes the obstruction resultant by integer Bareiss elimination, and
reconstructs seven exact sections directly from the original 81 halfspaces.
The finite rational checks do not by themselves prove the displayed
rational-function identities; the handwritten algebraic proof and symbolic
derivation supply that step. Neither script uses floating-point decisions,
random choices, an optimizer, an external dataset, or a hidden certificate.
