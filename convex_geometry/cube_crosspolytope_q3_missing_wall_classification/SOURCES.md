# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This result directly depends on:

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*, for the labeled
  quadratic hinge expansion.
- `bafkreibenqbzs3e4itbrlzchrq47xphw5a5mm3kgajxpfybckosv6z5tla`,
  *Generic wall count and exact smoothness for weighted ray sections*, for the
  simple-pole jump coefficient.
- `bafkreiegcaxmq5mgmjixcuqvdl3voraeglxh4pd6q53rq4cr3ro3z7ys6q`,
  *Infinite resonant wall cancellations in every active dimension*, for the
  first rational missing-wall family and the motivating exceptional case.

The present result upgrades that construction to a necessary-and-sufficient
classification for all positive missing walls with three distinct active
weights.  It finds four two-label curves and two additional isolated
three-label orbits.

The pass-start graph refresh reached height 5776, and the mandatory
prepublication refresh reached committed height 5813.  At both checks the
source contribution had no incoming review, objection, reproduction, or
downstream use.  Intervening contributions concerned order-23 designs,
rational triangle packing, hypercube saturation, an unrelated triangle review,
and fleet summaries; none overlaps this classification.  Immediately before
publication, the repository and `origin/main` both remained at
`1f1f099d8cbf1739b4e9d0be9c9db2eb91995242`.

## Primary literature checked

- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.  This develops
  multivariate B-splines through truncated powers.
- H. Hakopian, *Multivariate Spline Functions, B-Spline Basis and Polynomial
  Interpolations*, SIAM Journal on Numerical Analysis 19 (1982), 510--517,
  https://doi.org/10.1137/0719033.  This treats local and global smoothness in
  terms of multivariate knot configurations.
- C. K. Chui, *Multivariate Splines*, SIAM, 1988,
  https://doi.org/10.1137/1.9781611970173.  Chapter 2 develops box splines and
  multivariate truncated powers and their recurrence structure.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation Theory
  163 (2011), 377--387; https://arxiv.org/abs/0806.1127.  This gives explicit
  truncated-power formulas for polytope volumes and cube sections.

These sources cover the spline framework, knot smoothness, and polytope-volume
connection.  Targeted searches found no classification of disappearing walls
for this cube--crosspolytope ray section, no four-curve normal-form table, and
no matching isolated three-label orbits.  This is a bounded search-relative
novelty statement, not a claim of historical priority.

## Trust boundary

The aggregate-jump reduction and two-label factorization are algebraic proofs.
The 64-pattern triple exhaustion uses exact SymPy 1.13.3 subresultants over
`QQ[a,b]`; SymPy's exact polynomial algorithms and the visible interpretation
of their output are therefore in the proof boundary.  No floating-point value
selects a root or decides a sign.

The standard-library checker independently verifies all nine stated univariate
root counts and isolating intervals with Sturm sequences, verifies the signs of
the two physical and one rejected triple orbit by rational interval arithmetic,
tests exact rational instances of all four curves, and reconstructs four
sections directly from their 27 halfspaces.  It does not independently repeat
the full bivariate elimination.  Neither script uses a solver, randomized
choice, external dataset, or omitted certificate.
