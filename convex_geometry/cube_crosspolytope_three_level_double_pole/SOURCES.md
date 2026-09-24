# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This result is a sharp object-class extension of

- `bafkreib43rlceghdvayv3kcfyiopcqh6nonrif2a2elolnnf2cdvqf6cbe`,
  *Complete arbitrary-q classification of all two-level missing walls*;
- `bafkreies7e2vc2z7dglgaaaexjo57fufqghwsg5lih6xzjq5rnmfqfqicq`,
  *Arbitrary-q simple-pole classification of isolated two-level missing
  walls*.

It also uses the structural expansion proved in

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*.

At pass start, the committed graph was at height 5872.  The two-level source
had no incoming relation, and no graph contribution treated three-level
missing walls.  The only newer team source was an unrelated 24-vertex
tournament construction.  Its commit was inspected and incorporated by a
clean fast-forward to `68ef11fa9db8888960b769f4647e845f740847ea`.

The final prepublication refresh found graph height 5874, still with no
incoming relation on the source and no overlapping three-level or
double-pole result.  One new, unrelated review of an order-23 Hadamard Gram
tube was inspected and incorporated by a clean fast-forward to
`42ed45758c6d5041a4e2b2de85ab3acc4e66ab8b`.

## Primary literature checked

- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.
- K. Höllig, *Multivariate Splines*, SIAM Journal on Numerical Analysis 19
  (1982), 1013--1031, https://doi.org/10.1137/0719073.
- C. de Boor, K. Höllig, and S. Riemenschneider, *Box Splines*, Springer,
  1993, https://doi.org/10.1007/978-1-4757-2244-4.
- C. K. Chui, *Multivariate Splines*, SIAM, 1988,
  https://doi.org/10.1137/1.9781611970173.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation
  Theory 163 (2011), 377--387, https://arxiv.org/abs/0806.1127.
- H. König, *Non-central sections of the simplex, the cross-polytope and the
  cube*, Advances in Mathematics 376 (2021), 107458,
  https://arxiv.org/abs/2002.10743.
- R. Liu and T. Tkocz, *A note on the extremal noncentral sections of the
  cross-polytope*, 2020, https://arxiv.org/abs/1910.06993.

These primary sources establish the relevant spline, truncated-power,
polytope-volume, and noncentral-section framework.  A fresh targeted search
for repeated directions, coincident knots, cancellation of polynomial
pieces, and weighted noncentral sections found no theorem giving the exact
three-level double-pole cancellation in this directory.  This is a bounded
search-relative novelty statement, not a claim of historical priority.

## Trust boundary

The proof imports the cited global chamber formula and its tail action.  The
general two-jet identity and the exact counterexample are derived in
PROOF.md.  Root existence is an exact Sturm computation; row isolation also
has the elementary inequality proof in Section 4.

`derive.py` uses SymPy 1.13.3 to reconstruct the complete global expansion.
The standard-library `verify.py` independently checks the algebraic root,
coefficient identities, and structural-row isolation using exact rational
arithmetic.  The displayed decimals are explanatory only.
