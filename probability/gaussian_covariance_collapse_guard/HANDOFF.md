# Positive-loss covariance boundary for the R2/R3/R8 spine

Keep the normalization `d=E pair_squared_distance_loss/s`, with
`Sigma_X=Cov(X)/s`, `Sigma_Y=Cov(Y)/s`. The new author proof assumes
centered source radius at most `sqrt(s)/2`. It awaits independent review.

Its exact certificate tests whether either matrix

```
Sigma_X - 2^-86 d^2 I,
Sigma_Y - 2^-86 d^2 I
```

fails to be positive definite. Such a failure gives an integer direction
with nonpositive quadratic form. The whole interval `[1/64,1/2]` then
has margin `2^-42 d`, and the accepted high-noise window joins above it.
This is a uniform family theorem, not a sample-grid conclusion.

In a putative negative-middle search with d>=d0>0, both covariance
matrices must exceed `2^-86 d0^2 I`. Thus a fixed positive-loss region
has an explicit full-rank margin before requesting expensive Gaussian
moments or subdivision. A general sign in that remaining region is still
needed. If covariance and loss vanish together, the bound need not remove
the limit; no complete cover of that joint boundary is claimed.

The accepted R3 [effective mean-loss theorem](../gaussian_effective_mean_loss/HANDOFF.md)
signs sufficiently small d with a source covariance floor. The new
covariance test works at positive loss and has a different hypothesis.
It does not replace the accepted quartic-loss test or R8's functional
modulus and reconstruction error. In particular, none supplies a uniform
low-threshold tail reaching zero.

After contractivity has been checked, only marginal means and second
moments are required. The accepted same-pair degree-two cubature preserves
these, the source radius and contraction, on at most 19 original pairs.
For the degree-2q Taylor/Jackson interface its usual
`2 binom(2q+3,3)-1` budget remains unchanged. There are no extra mixed
features. This is an exact existence/preservation statement; independent
rounding, an effective diffuse integration oracle and a common rule for
all points in a parameter cell are not asserted.

The source projection in the proof uses a Kirszbraun extension and then
`(PX,T(PX))`. The checker need not compute that extension: its existence
is an analytic premise with a uniform estimate. Reusing the old targets
as labels of PX would generally invalidate contractivity. Target
projection instead uses `(X,P(TX-E TX))` directly.

Finite-input geometry and certificates can be replayed using guard.py
and verify.py. A parameter-cell proof must verify the radius, contraction,
and covariance inequality on the whole cell, by exact algebra or validated
enclosures. Checking the guard at its center or finitely many arbitrary
samples does not suffice.
