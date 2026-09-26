# Sharp replica curvature and polynomial comparisons in all degrees

Let an arbitrary probability law in `R^3` be supported in a radius-`R`
ball, and apply any 1-Lipschitz map before Gaussian convolution with
covariance `s I_3`. The [proof](PROOF.md) establishes:

- If `s >= 2 R^2/5`, every convex polynomial energy with a linear term
  and **at most three nonlinear monomials** compares in the conjectured
  direction. The monomial degrees are unrestricted. Convexity is required
  only on the possible density interval `[0,(2 pi s)^(-3/2)]`.
- Every `2 by 2` Hankel minor is nonnegative in that same regime, in
  every degree. This does not prove positivity of larger Hankel matrices.
- All convex quartic energies compare already when `s >= 17 R^2/60`,
  improving the preceding sufficient variance by a factor of four.

The underlying sharp functional inequality is

\[
B_2B_4\geq e^{-R^2/(12s)}B_3^2,
\]

for the team's nonnegative distance-deficit-weighted replica quantities.
The coefficient `1/12` is optimal among universal exponential bounds of
this form. Averaging the two new replicas before applying Jensen also
gives the corresponding estimate for every adjacent replica count.
This is what removes the dependence on degree in the first conclusion.

Exact replica log-convexity itself is false even at arbitrarily large
variance: two atoms contracted to one give `B_2 B_4 < B_3^2` whenever
`s >= 5 R^2/3`. This is an actual contraction pair whose endpoints satisfy
majorisation. It blocks a stronger proposed bridge, not the conjecture.

These are complete author proofs, awaiting independent review. The
variance thresholds for the energy comparisons are sufficient, not
claimed optimal. **Full majorisation and a new Kneser--Poulsen case
remain unproved.**

## Reproduction

Use the complete repository checkout; four sibling files are dependencies
and are checked by SHA256 before import. From this directory:

```sh
python3 verify.py > /tmp/replica-sparse-check.json
cmp /tmp/replica-sparse-check.json EXPECTED.json
python3 -O verify.py > /tmp/replica-sparse-check-optimized.json
cmp /tmp/replica-sparse-check-optimized.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Tested with CPython 3.11.2, standard library only. All checks use explicit
exceptions and remain active under `-O`. Expected status:
`ALL_FINITE_CHECKS_PASSED`. Expected-output SHA256:

```text
2e1607631285950d9e4afd9676091f56338c76adb4c79751379c0175cfc0adb7
```

The finite audits cover 108 rational averaged-variance identities,
27 sparse-moment controls, the exact polynomial obstruction, 18 enclosed
sharp-bound controls, four strict log-convexity failures, and independent
ordered-replica Taylor coefficients. A rational two-atom fixture with
`lambda=99/100,s=100,R=1` certifies that replacing `1/12` by `1/13` fails.
The analytic asymptotic argument proves failure for every smaller constant.

Gaussian fixture checks use the seven-point fold and the sixteen-point
simplex flap. They certify the new quartic threshold, 57 arbitrary-offset
Hankel minors, and the positive gap of a degree-nine convex energy at
`s/R^2=2/5`. That energy lies outside both `PC_2` and the preceding
weighted-prefix sufficient cone.

The verifier reuses the previously published rational enclosure and
multinomial replica implementation with explicit attribution in
[SOURCES.md](SOURCES.md). No independent numerical implementation is
claimed. Rational inputs, exact arithmetic, Taylor remainder bounds,
integer square-root brackets, and outward rounding are used. No floating
point, quadrature, optimizer, Monte Carlo estimate, large dataset, or
proof assistant enters the published verification.

The universal claims rest on the written analytic proof. Passing these
finite controls does not prove an unsampled universal inequality.

## Remaining obligation

The complete Hankel criterion requires every matrix size. Log-convexity
controls order-two minors and the sparse energy class above, but does not
control order-three minors. In this variance regime a polynomial
counterexample would therefore require at least four nonzero nonlinear
energy terms. The next question is whether a higher-order averaged
replica argument can control those larger matrices.

The team's new instantaneous-lift obstruction decisively rules out
unrestricted pointwise positivity along the lift. That failed route and
the earlier entropy-only, fixed common-noise, and abstract Abel-cancellation
bridges are not premises of this proof.
