# Independent acceptance: moving Gaussian sign window and flat adverse defect

## Verdict

**Accept for correctness in the stated scope.** For a centered contraction
at Gaussian variance `s`, suppose the source radius is at most `sqrt(s)/2`
and `Cov(X)/s >= 2^-15 I`. For every integer `m>=4`, the reviewed proof
correctly establishes

```text
d <= 2^-(44m+208)
  => H(u)>=0 for every u>=exp(-m^2/2),
     Def<=2^20 d exp(-m^2/4).
```

Thus with `m=max(4,ceil(sqrt(3(b+20))))`, the loss cutoff
`d<=2^-(44m+208)` gives `Def<=2^-b d`. More generally, at every fixed
source radius and positive covariance floor, the adverse defect is bounded
uniformly by `B_R exp(-c(log(a/d))^2)` and is therefore smaller than every
fixed power of `d` as `d` tends to zero.

The exact target is Discovery Net artifact
`bafkreidezctu4ybxubgdhubtveuj2px4qo4djtumcjhgxjhtpkezkunjka` at source
commit `abeedd6fee24a92e4ce58bdd9be7591a83f07f29`. Nine target files are
content-pinned in `TARGET_INPUTS.json`. The author checker passes under
normal and optimized CPython 3.11.2 and reproduces record SHA-256
`01e4794d90e5612b9f9cfa68c1396652700daeaabe4321f477dd4b028817449d`.

This is not a zero-defect theorem for any fixed positive loss. It does not
remove the covariance floor, sign the remaining low thresholds, settle the
positive-loss interior, or establish the full dimension-three frontier.
Historical novelty was not exhaustively checked.

## Threshold-sensitive estimates

For `u=exp(-S^2/2)` and the actual source top set `E={f>Cu}`, the Gaussian
envelopes give `B(0,S-R) subset E subset B(0,S+R)`. Cancelling the common
Gaussian factor in the posterior ratio correctly yields

```text
exp(-2RS-(5/2)R^2) <= r_z(x)
                     <= exp(2RS+(5/2)R^2).
```

At a component endpoint the separate absolute kernel floor is `Cu W`, not
merely `C W`. Keeping these two floors distinct is essential. The accepted
interval-component score argument then gives

```text
[k_E(y)-k_E(x)]/|E| >= Cu W^2 q/4.
```

This applies component by component without convexity. Along any bounded
line slice the Gaussian mixture is real analytic and nonconstant, so a
positive level has finitely many roots. The endpoint and posterior estimates
are uniform over arbitrary bounded laws, including diffuse laws.

For the Taylor remainder, the full-space Gaussian Hessian integrates to
zero. Since `E` contains `B(0,S-R)`, every point of its complement is at
least `q=S-3R>=1` from any Taylor point in `B(0,2R)`. Radial integration by
parts gives

```text
integral_q^infinity (r^4+r^2)e^(-r^2/2)dr
 <= (q^3+4q+4/q)e^(-q^2/2)
 <= 9S^3 u exp(3RS).
```

Dividing by the inner-ball volume produces `3375/64<64`, hence
`|partial_ee k_E|<=Cu|E| 64exp(3RS)`. This retains the threshold factor
needed to cancel `Cu|E|` in the normalized core estimate; no boundary
gradient or convex-superlevel hypothesis is introduced.

## Seven-budget assembly

The source proof correctly transports the accepted Procrustes and
conditional-alignment estimates. With `M<=K0d`, the first five cutoff terms
respectively enforce global alignment, rare mass at most `1/2`, conditional
covariance, the rare half-space bound, and one-label loss retention. The
core Taylor estimate becomes

```text
(W^2/4)d_GG - K1 delta d
  - A L^2 alpha^2 - K2 alpha sqrt(K0d),
```

while rare labels contribute `(W^2/8)(d_JG+d_JJ)`. With
`c=W^2/16` these coefficients retain all of
`d=d_GG+2d_GJ+d_JJ`. The choices `K1 delta=c/4` and the final two loss
budgets bound the remaining errors by `cd/8` each, leaving the claimed
positive margin `cd/2`.

At `R=1/2`, `kappa=2^-15`, the dyadic choices give the seven negative
exponents

```text
44, 14m+83, 14m+98, 22m+124,
7m+47, 35m+219, 44m+208.
```

The last dominates for every `m>=3`. For `m>=4` this cutoff also invokes
the independently accepted fixed window above `1/64`; that window overlaps
the new annulus because `1/64<exp(-25/8)`. No unsigned gap remains above
the moving endpoint.

## Whole-curve and every-radius bounds

The independently accepted R8 modulus gives
`|H(u)-H(v)|<=K d sqrt(|u-v|)`. Under `R<=1/2`, the reviewed elementary
bounds give `K<1016064<2^20`. Since any adverse value lies below the moving
endpoint and `H(0)=0`, this proves the stated whole-curve defect estimate.
The square-root schedule and `log(2)<3/4` then imply `Def<=2^-b d`.

For arbitrary fixed `R,kappa>0`, direct substitution gives exponential
pairs `(a_i,b_i)` equal to

```text
(0,0),(14,10),(14,10),(22,20),(7,5),(35,25),(44,40).
```

All seven cutoff terms therefore exceed a common positive coefficient times
`exp(-44Rm-40R^2)`. The generic target tail estimate follows from
`g(z)<=C exp(-(|z|-2R)_+^2/2)` and exact radial moments, giving

```text
integral min(g,Cu) <=
  [4+8R+8R^2+(8/3)R^3] sqrt(u).
```

Choosing `m=log(a/d)/(44R)` proves the log-squared bound and its uniform
`o(d^p)` consequence. The constants depend on the fixed radius and
covariance floor, as the theorem states.

## Independent exact evidence and trust boundary

`independent_check.py` imports no target module. It reconstructs the seven
dyadic budgets for nine values of `m`, proves the linear dominance check for
all `m>=3`, reproduces all six published relative-error schedules, checks
the symbolic every-radius envelope and radial coefficients, and evaluates
the eight-site calibration directly from all 28 pair distances and all
source covariance principal minors. It also tests a compressed `10^200`-bit
request without materializing its loss denominator.

Reproduce from this directory with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

The expected status is `INDEPENDENT_SMALL_LOSS_DEFECT_REVIEW_PASS`.
The canonical review record has SHA-256
`91ae356240abb5ae26a79a8208f38ec37cca3d6ad177b996a2fbc8335d51c443`.
The posterior/score identity, analytic slicing, kernel differentiation,
regular-value passage, Procrustes rigidity, conditional alignment, and R8
loss modulus remain reviewed written mathematics rather than proof-assistant
output. The checker guarantees the exact constants, schedules, finite-family
geometry, and packet provenance only.
