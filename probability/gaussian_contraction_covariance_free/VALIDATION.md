# Exact corroboration and analytic trust boundaries

The program was run with CPython 3.11.2 in ordinary and optimized (`-O`)
modes. Both exit successfully and produce identical `EXPECTED.json` bytes.
An instrumented run took 3.7 seconds and approximately 15 MB maximum resident
memory; runtime is descriptive, not a correctness premise.

## What is checked

- 36 sparse coordinate-folding configurations in dimensions 1 through 6,
  at three rational masses and two radii. Pair distances, centered
  cross-covariance, Procrustes error, and the ratio approaching the sharp
  constant are computed directly from all labeled points.
- All 95 contractions of the four input points `(-1,-1/3,1/2,1)` into the
  five-point half-integral grid in `[-1,1]`, with weights `(1,2,3,4)/10`.
  Their one-dimensional optimal alignment errors are calculated exactly.
- Six two-dimensional configurations, including nonlinear folds, rank
  loss, a rational rotation, and an isometry. The checker uses the exact
  two-by-two singular-value identity for Procrustes error and direct
  double-centering of the squared-distance arrays.
- Nine noncommuting positive matrix-square-root pairs, plus an orthogonal
  rank-one equality case for Powers–Stormer. Positivity is checked by
  principal minors; the trace norm of the self-adjoint two-by-two
  difference is handled algebraically, without eigensolver calls.
- Fifteen formal exponential-polynomial identities: dimensions 1, 2, 3
  and integer orders 2, 3, 4, 8, 9. The checker independently computes the
  coefficients of the defining replica integral through `epsilon^2`.
- Forty-two finite entropy comparisons at integer orders, comprising
  forty strict cases and two exact isometry identities. All forty strict
  margins have positive certified rational lower bounds.
- 1,125 one-center overlap controls, including the fractional orders
  `1/4,1/2,3/4,3/2,5/2,9/2`. These are exact checks of the Gaussian
  product formula, not a verification of arbitrary fractional mixtures.
- Nine malformed inputs are rejected, including noncontractions, invalid
  probabilities/radii, invalid sparse parameters, reversed intervals,
  negative square roots, and inadmissible exponential/logarithm arguments.

## Independent replica representation

For an integer `k>=2` and a finite mixture with centers `x_i` and weights
`p_i`, completing the square gives

```text
integral f^k / integral phi_0^k
  = sum_(i_1,...,i_k) p_(i_1)...p_(i_k)
      exp(-(sum_j |x_(i_j)|^2 - |sum_j x_(i_j)|^2/k)/(2s)).
```

The checker groups tuples by their multiplicity vector, using the exact
multinomial coefficient. For the sparse family the weights are polynomials
in `epsilon`; truncating at degree two discards precisely the terms with
more than two nonzero-center labels. Exponentials are kept as formal terms
indexed by rational exponents. Agreement of coefficient dictionaries is
exact algebraic equality, independent of numerical evaluations. This
representation is different from the parity-and-differentiation derivation
in the proof, but both were authored for this contribution; it is not an
independent peer review.

## Enclosure policy

All endpoints are `fractions.Fraction` values. There is no binary
floating-point step and no adaptive precision increase.

- For positive `x<130`, `exp(x)` is bounded using the sum through degree
  128 and a geometric tail starting with degree 129; successive omitted
  term ratios are at most `x/130<1`. Negative arguments use reciprocals.
- For `log(x)`, put `t=(x-1)/(x+1)` and require `|t|<=3/4`. The first 160
  terms of `2 sum t^(2j+1)/(2j+1)` are retained. The omitted absolute tail
  is at most `2(3/4)^321/[321(1-(3/4)^2)]`.
- Exponential endpoints and retained logarithm operations are rounded
  outward onto the rational grid with denominator `10^40`. Logarithm
  inputs are first enclosed on that grid; monotonicity encloses the
  logarithm of the whole input interval. Every accumulated rounding error
  is included by interval arithmetic.
- Square roots use integer square roots to enclose the answer on the
  same `10^-40` grid; rational perfect squares are returned exactly.
- Printed certificates are additionally rounded outward to the
  `10^-18` grid. The strict comparisons use the narrower internal
  endpoints, not a decimal approximation of them.

Each finite entropy certificate encloses both the actual gap and the
claimed lower bound; its displayed positive margin certifies that finite
case. No parameter subdivision or infinite-family coverage is inferred.
The standard library's arbitrary-precision arithmetic and the explicit
finite Gaussian integral formula are the computational trust boundary.

## What remains mathematical rather than computational

The all-order overlap lemma, the lifted dissipation identity, the SVD/trace
argument, and the Taylor and mode expansions are established in `PROOF.md`.
Finite agreement does not prove them. In particular, the checker does not
claim interval quadrature for arbitrary fractional mixtures, verification
of a noncompact truncation argument, or proof-assistant certification.
Independent review of this extension remains pending.
