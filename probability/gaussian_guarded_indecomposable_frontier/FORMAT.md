# Exact geometry input and output

`transplant.py INPUT.json` accepts exactly these five fields:

- `source`, `target`: equally long nonempty lists of rational three-vectors.
  Source sites must be distinct; target coincidences are allowed. Every
  pair distance must contract.
- `weights`: strictly positive rational weights summing to one.
- `radius`: an integer R>=1 bounding every endpoint Euclidean norm.
- `budget_bits`: an integer k>=1 for the conditional tail budget2^-k.

Rational scalars are JSON integers or strings parsed by `fractions.Fraction`.
Floating-point numbers and booleans are rejected. R and k are integers,
not strings. The producer uses L=max(4R,k), adds four roots first, halves
the old weights, translates the moving source/target by8Le_1 and6Le_1,
and scales all positions by1/(9L). It does not alter the input file.

The output records exact rational geometry, variance1/(81L^2), threshold
multiplier(9L)^3/2, covariance floor1/162, the symbolic tail schedule and
the consumer parameters. Its status is `GEOMETRY_ONLY_TRANSPLANT`.
The condition delta>=4*2^-k must come from an independently established
adverse Gaussian input; the code never asserts that condition holds.

`verify.py INPUT.json TRANSPLANT.json` directly recovers the original
clouds from the supplied points, checks every pair and every advertised
guard, and validates an intermediate. It neither imports nor invokes the
producer in this mode. Output is `SUPPLIED_TRANSPLANT_GEOMETRY_VERIFIED`.
Passing this check proves the finite rational geometric conditions, not
an adverse hinge, existence of a Brehm mesh, or indecomposability.

Without arguments, `verify.py` also runs the producer for reproducibility,
checks exact controls and produces EXPECTED.json. All requirements use
explicit exceptions and remain active under Python optimization. An invalid
input or damaged checked certificate exits nonzero. The checks use standard
Python rational arithmetic and a separate permutation determinant formula.
They are not a proof assistant or a new review of the imported theorems.
