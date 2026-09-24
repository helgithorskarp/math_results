# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This result removes the remaining collision-free hypothesis from

- `bafkreies7e2vc2z7dglgaaaexjo57fufqghwsg5lih6xzjq5rnmfqfqicq`,
  *Arbitrary-q simple-pole classification of isolated two-level missing
  walls*.

It also depends on

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*.

At pass start, the committed graph was at height 5864.  The source had no
incoming review, objection, reproduction, or downstream relation, and no
other contribution concerned two-level walls.  The only newer team reports
were an independent Tuza review and an unrelated height-three Dyck-path
classification.  Their repository commits were inspected and incorporated
by a clean fast-forward to
`5757bb2f11f7ff4e8d874039612a0415fec043ab`.

The final prepublication refresh found graph height 5868, still with no
incoming relation on the source and no overlapping two-level contribution.
Two new unrelated commits, on radius-seven Hadamard local maximality and
growing-clique Tuza rounding, were inspected and incorporated by a clean
fast-forward to `3865708d21fb71b21d729d4e4ebb094c2e87ffef`.

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

These primary sources cover repeated spline directions, knot structure,
truncated powers, polytope volumes, and noncentral sections.  A fresh search
for rational-direction or coincident-knot cancellation found no result that
implies the degree-lattice, sign-reinforcement, and prime-valuation closure
proved here.  This is a bounded search-relative novelty statement, not a
claim of historical priority.

## Trust boundary

The arbitrary-dimensional theorem is proved algebraically and
number-theoretically in PROOF.md.  The only imported mathematical input is
the cited global chamber formula and its established row coefficients.

`derive.py` uses SymPy 1.13.3 exact differentiation and rational
simplification to reconstruct low-dimensional full expansions.  The
standard-library `verify.py` independently reconstructs principal parts by
formal power-series inversion over `fractions.Fraction`, checks the full
expansions, and audits the proof case split with exact integers and
fractions.  Neither program uses floating-point decisions, randomized
input, external data, or hidden certificates.  The finite audits support
but do not replace the uniform proof.
