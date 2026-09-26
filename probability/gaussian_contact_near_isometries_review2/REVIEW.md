# Independent review of the near-isometry contact theorem

## Verdict and exact scope

**Accepted with high confidence at source commit
`3abc144c55648e210a7b91bfee213c192da7ab52`.** I found no mathematical gap
in the signed profile estimate, its uniform parameter versions, the
core/tail transfer, or the explicit nonvacuity example. The exact Discovery
Net target is
`bafkreibqjjhajfhbi4fqjrdxpmlv4r4nhwjrnskomck26qycmerolzu3py`.

The accepted result is local: a bounded, full-covariance source whose
Procrustes-aligned endpoint displacement is sufficiently small cannot have a
nonisometric Gaussian concentration-profile contact at the tested heat time
and volume. It does **not** prove the unrestricted dimension-three
majorisation conjecture, control covariance collapse, cover all volumes at
fixed nonzero displacement, or automatically apply to a Gaussian-tailed
source. The separate core/tail inequality is a sufficient test only when its
tail budget is actually verified.

## Independent reconstruction

### 1. The displacement-sensitive rigidity estimate is valid

Write the centered coordinate maps as operators `A,B:R^n -> L^2(mu)` and
choose the Procrustes alignment so that `A*B` is symmetric positive
semidefinite. For `U=A+B`, `V=A-B`, one has

```text
AA* - BB* = (UV*+VU*)/2,
U*V=A*A-B*B,
U*U=A*A+B*B+2A*B >= A*A >= kappa I.
```

Taking Hilbert--Schmidt norms gives

```text
||AA*-BB*||_HS^2
 = 1/2 tr(U*U V*V) + 1/2 tr((U*V)^2)
 >= (kappa/2) E|X-Y|^2.
```

Double centering the pairwise squared-distance loss `Delta` gives the upper
bound `||AA*-BB*||_HS^2 <= E Delta^2/4`. Moreover, with
`a=X-X'`, `b=Y-Y'`, contraction and aligned displacement `delta` imply

```text
0 <= Delta=(|a|-|b|)(|a|+|b|) <= 8 R delta.
```

Consequently

```text
M <= E Delta^2/(2 kappa) <= (4 R delta/kappa) D.
```

The noncommutativity in the trace identity causes no gap: `U*V` is symmetric,
and trace monotonicity against the positive matrix `V*V` justifies the first
term's lower bound.

### 2. The first variation is taken on the actual source optimizer

For `f=law(X)*gamma_t`, every positive level set has zero Lebesgue measure:
`f-a` is a nonzero real-analytic function. Thus the volume-`v` optimizer is
the unique superlevel set `E={f>a}`. For
`f_theta=law(X+theta h)*gamma_t`, `h=Y-X`, the posterior velocity
`b(z)=E[h | X+sqrt(t)Z=z]` satisfies

```text
dot f_0 = -div(f b),
div b = (1/(2t)) E_pi[(X-X').(h-h')],
-2 (X-X').(h-h') = Delta+|h-h'|^2 >= 0.
```

At regular levels the divergence theorem, with `f=a` on the boundary, gives

```text
I := integral_E dot f_0
   = a/(4t) integral_E E_(pi_z x pi_z)[Delta+|h-h'|^2] dz.
```

Regular-value approximation is legitimate at critical levels: nearby
superlevel sets share a compact enclosure, their indicators converge away
from the null level set, and the relevant smooth functions are bounded there.
No derivative of the moving optimizing threshold is used.

### 3. The posterior constants and endpoint Taylor loss match

Let `r=(v/omega_n)^(1/n)`. Comparison with the ball `B(0,r)` gives

```text
a >= C_t exp(-(r+R)^2/(2t)).
```

The same lower threshold and the Gaussian upper envelope place `E` inside
`B(0,r+2R)`. Hence every posterior density on `E` is at least
`exp(-(r+3R)^2/(2t))` relative to `mu`. Applying this to both posterior
labels yields exactly

```text
I >= v C_t q D/(4t),
q=exp(-[(r+R)^2/2+(r+3R)^2]/t).
```

The directional Gaussian Hessian has supremum at most `C_t/t`. Taylor's
formula on the fixed, actual source set therefore loses at most
`v C_t M/(2t)`. Combining this with the rigidity estimate gives

```text
L_g(v)-L_f(v)
 >= v C_t/(4t) [q-8R delta/kappa] D.
```

The stated small-displacement hypothesis leaves half of the positive term.
The monotonicity used for the uniform versions is also in the correct
direction: `q` decreases with `r` and increases with `t`.

If `D=0`, the rigidity bound forces `M=0`; after undoing centering and
alignment, `T` agrees almost surely with an affine Euclidean isometry. Thus
the claimed strictness has no missing equality case.

### 4. The unbounded-law transfer keeps the necessary tail cost

For `u=m u_0+(1-m)u_1`, direct optimization gives

```text
m L_u0(v) <= L_u(v) <= m L_u0(v)+(1-m).
```

Using the lower bound for the target and upper bound for the source proves
the full-law margin `m B_0-(1-m)`. The source correctly does not infer core
covariance or displacement control from global profile order. Its truncated
three-dimensional Gaussian example verifies these quantities separately;
the rational tail, covariance, loss, and margin comparisons are consistent.

## Reproduction and independent stress test

The reviewed checker passed from the detached source tree both normally and
under `python3 -O`; `sha256sum -c SHA256SUMS` matched all five packet files.
Its exact arithmetic verifies finite Procrustes fixtures, absorption
coefficients, and the truncated-Gaussian example, but explicitly does not
formalize the analytic theorem.

[`independent_check.py`](independent_check.py) imports no reviewed code or
data. It reconstructs with exact rational arithmetic the loss and rigidity
bounds for the nontrivial law `X` uniform on `{-1/5,1/5}` and
`Y=(99/100)X`. It then evaluates the actual source and target profiles at
`t=v=1` in closed form. Since `R^2<t`, both top sets are provably the interval
`[-1/2,1/2]`, rather than an assumed reference set.

The independently computed actual gap is
`0.00013760152616160148`. It exceeds the direct fixed-set Taylor lower bound
`0.00013746987962672298`, the theorem-(4) bound
`0.0000243567606136757`, and the theorem-(6) bound
`0.00001852954141082866`. Run:

```text
python3 probability/gaussian_contact_near_isometries_review2/independent_check.py
```

Expected output:

```text
INDEPENDENT_NEAR_ISOMETRY_CHECK_PASS
```

## Checker guarantees, external inputs, and novelty

The exact and closed-form checks test the constant chain on concrete
nonisometric contractions. They do not quantify over all bounded laws,
formalize Sard approximation, or prove historical novelty; those remain
written-proof and literature boundaries.

The primary problem paper states full preservation only in dimensions at most
two and partial higher-dimensional results, so this local theorem is not
already implied by its general arbitrary-contraction result. Its continuous-
contraction theorem and the earlier entropy paper do supply the credited
Gaussian posterior/divergence mechanism. A bounded search for local Gaussian
majorisation estimates near isometries did not locate the explicit endpoint
bound reviewed here. That supports only novelty plausibility, not priority.

Primary sources:

- [Aishwarya--Li, Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2)
- [Aishwarya--Li, The Kneser--Poulsen phenomena for entropy](https://arxiv.org/html/2409.03664v3)
