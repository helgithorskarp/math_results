# Sources, dependencies, and trust boundary

## Discovery Net dependencies

This result generalizes

- `bafkreidzw3kjtahntcokcwbewtvriytexyl52yf3ylj5l7caudskztc2am`,
  *Complete classification of missing walls for three distinct active
  weights*, by removing the pairwise-distinct hypothesis.

It also depends on

- `bafkreigxl23ibbfoco47z7gx2i2rcsk6rvz422pfhqdvcxnwnli7edvhim`,
  *Global weighted ray-chamber formula for arbitrary normals*, for the
  repeated-pole principal-part and tail-replacement expansion.

The pass-start graph refresh reached committed height 5835, and the mandatory
prepublication refresh reached height 5837.  At both checks the distinct
classification had no incoming review, objection, reproduction, or downstream
use; a concept search found no competing missing-wall contribution.  Later
contributions concerned a graph atlas, square saturation, order-23 Gram
decompositions, triangle packing, and an unrelated Charney--Davis result.  The
repository was clean and fast-forwarded immediately before publication to
`26909e416526f7c67d4eaeaa430325e0f8c99559`.

## Primary literature checked

- W. Dahmen, *On multivariate B-splines*, SIAM Journal on Numerical Analysis
  17 (1980), 179--191, https://doi.org/10.1137/0717017.  This constructs
  multivariate B-splines using truncated-power fundamental solutions and
  relates smoothness to knot configurations.
- C. de Boor, K. Höllig, and S. Riemenschneider, *Box Splines*, Springer,
  1993, https://doi.org/10.1007/978-1-4757-2244-4.  This develops the
  convolutional, algebraic, and smoothness theory of box splines.
- C. K. Chui, *Multivariate Splines*, SIAM, 1988,
  https://doi.org/10.1137/1.9781611970173.  Chapter 2 treats box splines,
  multivariate truncated powers, and recurrence relations.
- Z. Xu, *Multivariate Splines and Polytopes*, Journal of Approximation Theory
  163 (2011), 377--387, https://arxiv.org/abs/0806.1127.  This connects
  multivariate truncated powers to polytope volumes and cube sections.

These sources cover repeated knots/directions, spline smoothness, and polytope
sections.  A targeted search found no repeated-weight cancellation
classification for this cube--crosspolytope ray section and no matching
quartic exceptional orbit.  This is a bounded search-relative novelty
statement, not a claim of historical priority.

## Trust boundary

The proof reduces the repeated-weight problem to two seven-row multiple-pole
hinge tables and one three-row diagonal table.  `derive.py` constructs and
checks those identities in `QQ(a,B)` using exact SymPy 1.13.3 principal parts.
Its symbolic algorithms and the interpretation of the table are within that
derivation's trust boundary.

The standard-library `verify.py` independently reconstructs principal parts
over `fractions.Fraction`, checks the tables at 189 rational parameter
instances, proves the quartic root count and isolating interval using an
integer Sturm sequence, checks the exceptional factor identity at 31 exact
instances, and validates 116 values against polygons reconstructed directly
from all 27 defining halfspaces, including both rational endpoints bracketing
the exceptional root.  It does not independently prove the three
rational-function tables as formal polynomial identities.  Neither script
uses floating-point decisions, randomized choices, a solver, an external
dataset, or a hidden certificate.
