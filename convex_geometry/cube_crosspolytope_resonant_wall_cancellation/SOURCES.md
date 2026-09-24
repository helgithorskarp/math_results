# Sources and novelty boundary

## Discovery Net dependencies

This result directly uses:

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*, which supplies
  the exact subset expansion and candidate wall set.
- `bafkreibenqbzs3e4itbrlzchrq47xphw5a5mm3kgajxpfybckosv6z5tla`,
  *Generic wall count and exact smoothness for weighted ray sections*, which
  gives the isolated-label jump coefficient and leaves resonant cancellations
  as the exceptional case.

The present result proves that the genericity condition is essential by
constructing rational missing-wall families in every active dimension.  It
also classifies every cancellation of the displayed collision pattern in a
natural three-weight-level ansatz.

The pass-start graph refresh through height 5766 found no incoming review,
objection, reproduction, or overlapping resonance result.  The mandatory
prepublication refresh reached height 5768 and again found no incoming relation
to the generic-wall result and no overlapping resonance result.  The only new
contribution was an independent review of the square-saturated-hypercube
construction; it is methodologically disjoint.  The corresponding repository
refresh advanced `main` to
`d585acd8ff7b2fd86ad1488f0237cb558303d28c` before this source was finalized.

## Primary literature checked

- H. Hakopian, *Multivariate Spline Functions, B-Spline Basis and Polynomial
  Interpolations*, SIAM Journal on Numerical Analysis 19 (1982), 510--517,
  https://doi.org/10.1137/0719033.  This determines local and global
  smoothness classes from multivariate knot configurations.
- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.  This constructs
  multivariate B-splines using truncated powers.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation
  Theory 163 (2011), 377--387; arXiv:0806.1127,
  https://arxiv.org/abs/0806.1127.  This gives explicit truncated-power
  formulas for polytope volumes and cube sections.

These works provide the general setting for knot-dependent smoothness and
polyhedral splines.  The bounded search found no matching rational family of
missing walls, coefficient identity (13), or every-dimension construction for
cube--crosspolytope Minkowski sections.  This is a search-relative novelty
statement, not a historical-priority claim.

## Trust boundary

The proof uses exact rational identities and the previously proved global
subset formula.  The checker uses only CPython and `fractions.Fraction`.  Its
27-halfspace polygon reconstruction independently corroborates the smallest
dimension without assuming the spline expansion.  No floating-point
computation, solver, external dataset, or hidden certificate is used.
