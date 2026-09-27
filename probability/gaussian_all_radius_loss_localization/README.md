# All-radius loss-uniform Gaussian localization

[PROOF.md](PROOF.md) gives an explicit whole-curve modulus proportional to
the mean squared-distance loss for **every bounded R3 contraction**, at any
fixed Gaussian variance, under a positive lower bound on the actual source
covariance. It removes the small-radius restriction from the existing
loss-proportional cubature transfer, at the cost of this covariance guard.
No small atom-mass or positive loss floor is needed.

**Status:** complete author proof, independent review pending. No new
Gaussian sign or Kneser--Poulsen theorem is asserted. Full R3 majorisation
remains open, with the accepted global adverse-defect cap unchanged.

Normalize to variance one and assume |X-E X|<=R, Cov(X)>=kappa I, where
R>=1 is an integer and kappa>0. For the favorable normalized hinge gap H
and ordered distance loss D, the main middle estimate is

```
|H(u)-H(v)| <= D K_L |u-v|^(1/r),  2^-L<=u,v<=1,
B=2R+ceil sqrt(2(L+1)), r=32B^2-1,
K_L=56 B^3 2^(3L)(1+4R^2/kappa).
```

An explicit loss-scaled bound at zero joins this to a whole-curve modulus.
Combining it with the accepted paired cubature gives

```
||H_mu-H_nu||_infinity <= D[2E_(N,L)+B_(N,q)(R^2)],
```

with the explicit error tending to zero and at most
`2 binom(2q+3,3)-1` original pairs. The degree and atom budget depend on
R,kappa and relative tolerance, **not on D**. The old marginal moment list
already preserves every added guard. The proof also gives a uniform middle
mesh certificate conditional on positive normalized sample margins.
Writing `A=1+R^2+log2(1+4R^2/kappa)+log2(1/zeta)`, the sufficient degree
and atom count are `2^(O(A^2))`. This is a quasipolynomial accuracy bound
at fixed radius and covariance, with large explicit constants.

The geometric argument aligns the clouds by Procrustes and uses their
straight interpolation without assuming it contracts. A Gaussian derivative
bound and finite interpolation control thin density-level strips, including
critical levels. This converts the established posterior-divergence formula
into an explicit loss-relative functional estimate at large radii.

## Reproduction

From this directory, with CPython 3.11 or later and its standard library:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `ALL_RADIUS_LOSS_LOCALIZATION_CONTROLS_PASS`.
[EXPECTED.json](EXPECTED.json) has SHA256
`8419ae3d4849f9776ab6c101987f74901a927d0807e55ac7a6422adc38e8dfc8`.

The compact controls check 119 interpolation/Gaussian/constant identities,
five direct factorial remainders, 78 reconstruction variance identities,
7,040 straight-path pair identities, vanishing and zero loss, independent
endpoint frames and variance scaling, 15 rejected inputs, and nine source
pins. The accepted strict 24-site screw is used only to verify the new
radius/covariance hypotheses; its Gaussian sign is not tested and its motion
obstruction is not replayed. The universal analytic proof is not formalized.

## Exact consumer and scale of the budget

The standard-library functions `middle_budget(R,kappa,L,eta)` and
`whole_curve_budget(R,kappa,zeta)` in [verify.py](verify.py) accept exact
`fractions.Fraction` parameters and return symbolic schedules. They never
allocate an enormous beta row, cubature support, or integer denominator.
[HANDOFF.md](HANDOFF.md) states the sign obligations.

For example R=2, kappa=1/64 and a=1/16 give Holder exponent 1/2047.
A normalized sample margin 1/256 has the sufficient mesh spacing
`2^-94162`. A global relative error 1/16 is certified by the deliberately
loose schedule `log2(N+2)=2565381840`. These are rigorous finite budgets,
not practical computations or evidence of a newly signed family.

The theorem is uniform on a parameter cell with fixed R,kappa, including
loss tending to zero. It does not control simultaneous covariance collapse.
The original-law low/high signed endpoints remain necessary for an exact
all-threshold certificate. The new positive tail error cannot replace them.
