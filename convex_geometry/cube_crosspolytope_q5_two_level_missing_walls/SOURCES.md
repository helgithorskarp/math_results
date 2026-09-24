# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This contribution generalizes the structural mechanism and continues the
two-level classification from

- bafkreieywkmdh2hewoxfv3fqninexkkmd7bjfghwactc4fckq7vvnw5kbi,
  *Complete two-level missing-wall classification for four active
  coordinates*.

It also depends on

- bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim,
  *Global weighted ray-chamber formula for arbitrary normals*.

At pass start, the committed graph was at height 5853. The q=4 source had
no incoming review, objection, reproduction, downstream use, or competing
missing-wall contribution. The repository was clean and synchronized at
commit 1dd0cb3b6f1b2dc221569df3936e8b5c14336737.

The mandatory prepublication refresh remained at height 5853 with no new
relation on the source and no overlapping graph contribution. Two unrelated
repository additions reviewed gamma-nonnegativity and audited an FC(4,9)
classification; they were incorporated by a clean fast-forward to
1cb417dc57df23718297b2a0ca0c9020d58d0265.

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

These primary sources cover repeated spline directions, truncated powers,
polytope volumes, and noncentral cube/crosspolytope sections. Targeted
searches found no arbitrary-\(q\) parity obstruction for these resonant walls
and no five-active-weight two-level classification. This is a bounded
search-relative novelty statement, not a claim of historical priority.

## Trust boundary

The arbitrary-\(q\) coefficient identity is proved algebraically in
PROOF.md. derive.py also checks it in all 42 positive resonance types for
\(q=3,4,5\), then proves the dimension-five symbolic identities using exact
SymPy 1.13.3 operations. SymPy factorization, root isolation, and resultant
algorithms lie inside that derivation's trust boundary.

The standard-library verify.py independently reconstructs the expansion over
fractions.Fraction, tests the closed identity at 673 exact rational
instances, proves all six root certificates with rational Sturm sequences,
computes the three resultants using integer Bareiss elimination, and repeats
the special-collision census. It does not independently prove the
rational-function identities from finitely many samples. Neither program
uses floating-point decisions, randomized choices, external data, or hidden
certificates.
