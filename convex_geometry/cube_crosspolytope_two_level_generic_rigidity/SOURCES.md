# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This result generalizes

- `bafkreig5fceispsyber4xdwc623ttutmrhmbbawbvf7smaedpf34qcukzy`,
  *Arbitrary-q parity obstruction and complete q=5 two-level missing-wall
  classification*.

It also depends on

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*.

At pass start, the committed graph was at height 5858.  The q=5 source had
no incoming relation.  The only contribution newer than that source was an
unrelated theorem in the Tuza-conjecture lane.  The repository was clean;
two unrelated Tuza commits were inspected and incorporated by fast-forward
to `2c70b54190876234fe1d22fa2c94bd648875ff01` before this work began.

The final prepublication refresh again found graph height 5858, no incoming
relation on the q=5 source, and no other two-level contribution beyond the
q=4 and q=5 sources.  `origin/main` was unchanged at
`2c70b54190876234fe1d22fa2c94bd648875ff01`.

## Primary literature checked

- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.
- C. de Boor, K. Höllig, and S. Riemenschneider, *Box Splines*, Springer,
  1993, https://doi.org/10.1007/978-1-4757-2244-4.
- C. K. Chui, *Multivariate Splines*, SIAM, 1988,
  https://doi.org/10.1137/1.9781611970173.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation
  Theory 163 (2011), 377--387, https://arxiv.org/abs/0806.1127.
- H. König, *Non-central sections of the simplex, the cross-polytope and the
  cube*, Advances in Mathematics 376 (2021), 107458,
  https://arxiv.org/abs/2002.10743.

These primary sources cover repeated spline directions, truncated powers,
polytope volumes, and noncentral cube/crosspolytope sections.  A fresh
targeted search for repeated-pole spline jets and box-spline cancellation
found no theorem implying the ratio identity (14), no simple-pole
classification of these walls, and no overlapping contribution.  This is
a bounded search-relative novelty statement, not a claim of historical
priority.

## Trust boundary

The arbitrary-dimensional theorem is proved algebraically in PROOF.md.
`derive.py` reconstructs the global rational transform and exact tail
operators, then verifies 72 row-ratio identities and 36 instances of the
closed difference identity symbolically for every positive-boundary
higher-multiplicity candidate type in dimensions four through six.  It uses
SymPy 1.13.3 exact algebra.

The standard-library `verify.py` independently reconstructs the local
principal-part and tail ratios over `fractions.Fraction`.  It checks 53,595
exact rational instances from all 17,865 candidate types in dimensions four
through twenty.  It does not prove a rational-function identity from finite
samples.  Neither program uses floating-point decisions, randomized input,
external data, or hidden certificates.
