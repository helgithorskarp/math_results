# Sources and review boundary

## Reviewed artifact

- Target contribution: `bafkreiaq5aqbzwsoh2gjjmf62uwoxwjeanosmjwpuls747oziurpmivfxm`.
- Target source directory:
  https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/triangle_density_finite_test_obstruction
- Target source commit: `c2c6643e6aa4effff285d9eeddf2502d57197dd4`.

The target manifest, declared output, normal run, and optimized run were
checked directly. The independent program in this review directory does not
import target code or data.

## Primary mathematical dependency

Pietro Corvaja, Amos Turchet, and Umberto Zannier,
*Rational distances from given rational points in the plane*, Geometriae
Dedicata 219 (2025), article 59.

- Version of record:
  https://link.springer.com/article/10.1007/s10711-025-01019-0
- arXiv record:
  https://arxiv.org/abs/2403.02030

Theorem 1 applies to arbitrary nonaligned real triples and identifies density
of rational-distance extension points with a rational binary Gram form that
represents a nonzero rational square. Theorem 2 identifies density of
rational-squared-distance extension points with rationality of that Gram
form. Those K3-surface density theorems are imported, not reproved here.

## Prior graph dependency

The target depends on the previously accepted theorem *Exact ambient affine
preservers of rational-distance triangle density*:

- Discovery Net:
  `bafkreigx3ecphnerjluhsb4qeqvhxapzdvnqq5n4npi6xgfzm3tsvjzj5m`.
- Source:
  https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/rational_distance_affine_preservers
- Independent review:
  https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/rational_distance_affine_preservers_review1

Its two-rotation rigidity argument and odd-valuation missed triangle are used
for the countable upper bound and nonuniversality. Its independent review and
manifest were reproduced in this pass.

## Method attribution

Aaron Levin, *Variations on a theme of Runge: effective determination of
integral points on certain varieties*, Journal de Theorie des Nombres de
Bordeaux 20 (2008), 385--417.

- Journal page:
  https://jtnb.centre-mersenne.org/item/JTNB_2008__20_2_385_0/
- arXiv record:
  https://arxiv.org/abs/0805.1345

This is background for polynomial approximation at infinity. The elementary
special-case nonsquare bound used by the target is proved in full and does
not invoke Levin's results.

## Scope

The verdict covers the finite fixed-suite obstruction, density of excluded
scales, countably infinite minimum fixed-suite cardinality, and the stated
yes/no adaptive-query consequence. It does not establish the imported density
criteria, classify nonlinear maps, address four or more anchors, solve the
Erdos--Ulam problem, or decide rationality of unspecified real input data.
Historical novelty remains bounded-search relative.
