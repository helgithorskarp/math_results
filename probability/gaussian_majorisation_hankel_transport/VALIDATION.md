# Validation and trust boundaries

Environment: CPython 3.11.2, standard library only. The normal interpreter
and `python3 -O` reproduce identical bytes in `EXPECTED.json`:

```text
25f2d42cd53b0ec6f5d4cb720b5a8e169903f1bd63c27ba4580b827408231a19
```

The output status is `VERIFIED_REDUCTION_CONTROLS`. This status applies
to the finite checks below, not to the open majorisation conjecture.

## Exact checks

- Eighteen exact comparisons between a multinomial-count expansion and
  literal ordered replicas, totaling 4,898 ordered tuples. The two
  implementations produce the same rational coefficient/exponent maps
  before any transcendental evaluation.
- Five supplied Gaussian polynomial controls: a three-atom fold,
  tetrahedron collapse, seven-point coordinate fold, asymmetric fold,
  and translated isometry. Four supplied gaps are certified positive;
  the isometry cancels to exactly zero before interval evaluation.
- The seven-point example has joined affine rank six, checked by exact
  rational elimination. This is a control for the checker, not a new
  class theorem; coordinate folds have known majorisation comparisons.
- Nine certified, strictly positive lower bounds for the row-condition
  violation, each of which applies to **all** orthogonal alignments by
  the written theorem. Forty-five individual rotation-parameter values
  are checked separately. The fold moment identity and centered geometry
  are also checked independently in these nine cases.
- The abstract Dirac-measure obstruction to the square-root multiplier
  is certified negative. This measure is not asserted to be an admissible
  lifted deficit measure.
- A classical rational step-density pair gives a negative order-five
  Hankel quadratic form even though all nine tested moment entries are
  positive. Its gap is computed both from moments and by exact integration
  of its piecewise-linear hinge curve:
  `-1442909906179/1089174528000000000000`.
  This is a **non-Gaussian negative control**, not a contraction
  counterexample. Eight exact partial sums verify the standard catalyst.
- Fourteen invalid-input or domain/workload cases are rejected, including
  an expansive labelled map, inconsistent coincident inputs, floating-point
  coordinates, zero variance, and division through zero.

## Rational enclosures

`bounds.py` uses `fractions.Fraction` endpoints throughout. Addition and
multiplication propagate the full endpoint interval; reciprocal intervals
are used only when zero is excluded. Decimal-denominator rounding takes
the lower floor and upper ceiling, so it is always outward.

For `exp(x)`, `x<=0`, reduce `-x` by repeated halving to `r<=1/2`.
Use `N=2*digits+16` Taylor terms for `exp(r)`. If `b_N` is an upper
bound for the last retained term, the omitted tail is at most

```text
b_N * r/(N+1) / (1-r/(N+2)).
```

Successive omitted-term ratios are at most `r/(N+2)`. Every retained
term, partial sum and squaring is rounded outward at
`digits+20+number_of_squarings` decimal digits. Square the enclosure back
to `exp(-x)`, reciprocate, and round outward at the requested precision.
This has no floating-point underflow. An enclosure may include zero when
the value is too small for the chosen precision; it then does not justify
a strict sign. Precision changes width, never enclosure validity.

The factor `sqrt(k)` is enclosed by integer square root at denominator
`10^digits`, with exact treatment of integer squares. Checks of exponential
addition and square-root squaring supply sanity controls. They are not
substitutes for the series-remainder and integer-root proofs.

`certify.py` validates every pairwise squared-distance inequality using
rationals. It then groups the two replica expansions by exact exponents,
subtracting equal terms **before** enclosing exponentials. This avoids
spurious losses on pairs whose distances agree exactly, an issue identified
in the adversarial team's floating-point exploration. Signed coefficients
are propagated with interval arithmetic. The decision uses the full
requested-precision interval, not the shorter moment intervals displayed
for readability.

## Limits

The proof is not formalized. The program does not enumerate all measures,
all contractions, all polynomial degrees, or all precision levels. It is
a finite witness checker plus compact reproduction controls. Its default
workload cap is 250,000 multinomial states, and its precision setting is
restricted to 10--1,000 digits. These operational bounds do not enter the
mathematical certificate-completeness theorem.

No solver, random seed, external dataset, empirical quadrature, eigenvalue
sign inferred from floating point, or large certificate is trusted. The
written proof and classical Kirszbraun theorem carry the universal claims.
New independent mathematical review of this contribution is pending.
