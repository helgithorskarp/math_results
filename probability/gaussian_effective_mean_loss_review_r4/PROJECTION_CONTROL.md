# An independent projection control for the effective mean-loss mechanism

27 September 2026. A separately derived, coarser analytic control of the
effective mean-loss mechanism. R3's concurrently published slicing theorem
supplies a stronger cutoff and is the primary result; see [REVIEW.md](REVIEW.md).
This proof is supplementary author mathematics, not independently accepted.
It makes the cutoff in R8's uniform mean-loss theorem explicit. The alternative step repairs the background separately for each rare
move by projection onto its bisector halfspace. Quantitative polarization
then signs that move on the **actual** source top set. The constants are
deliberately very conservative; no feasible global enumeration is claimed.
See [SOURCES.md](SOURCES.md) for attribution and the precise research boundary.

## 1. Statement and normalization

Let `m>=2` be an integer. Let `X` have any probability law on `R^3` with

```text
E X=0,       |X|<=m,       Cov(X)>=m^(-1) I_3.             (1)
```

Let `T` be 1-Lipschitz on the source support. Center its image and choose
an orthogonal Procrustes alignment, writing the result as `Y`. Thus
`E Y=0` and `A=E[XY^T]` is symmetric positive semidefinite. Set

```text
h=Y-X,  M=E|h|^2,
Delta(x,z)=|x-z|^2-|Y(x)-Y(z)|^2>=0,  D=E Delta(X,X').    (2)
```

Primes mean independent copies. Write `C=(2 pi)^(-3/2)`,
`gamma(z)=C exp(-|z|^2/2)`, `f=law(X)*gamma`, `g=law(Y)*gamma`, and
`E_f(v)={f>a_f(v)}` for the source top set of volume `v`.

**Theorem.** If

```text
0 < D <= 2^(-65536 m^2),
```

then, simultaneously for every `0<v<=m`,

```text
integral_(E_f(v)) (g-f) >= 2^(-8193 m^2) v D.            (3)
```

For `D=0`, `Y=X` almost surely. In particular (3) gives the same lower
bound for `L_g(v)-L_f(v)`, where `L_p(v)=sup_(|E|=v) integral_E p`.
It also gives that lower bound for
`H(u)=integral(g-Cu)_+-integral(f-Cu)_+` whenever
`v=|{f>Cu}|` belongs to `(0,m]`. An empty source superlevel already
gives `H(u)>=0`.

There is no atom-count assumption, minimum mass, maximum-displacement
smallness assumption, or regular-level assumption. The positive covariance
floor, radius bound, unit variance, and bounded source volume are actual
hypotheses. In particular this does not prove unrestricted majorisation,
all-threshold order, or a new Kneser--Poulsen theorem.

For prescribed `R,kappa,V>0`, choose any integer
`m>=max(2,R,1/kappa,V)`. At variance `s I_3`, first divide coordinates
by `sqrt(s)` and volume by `s^(3/2)`: the guard applies to `D/s` and
the margin becomes `2^(-8193m^2) (v/s^(3/2))(D/s)`.

An entirely rational high-threshold guard is available. If `|X|<=R`
and `h_0>=0` is an integer, every nonempty `{f>Cu}` with `u>=2^(-h_0)`
has volume at most `(16/3)(R+h_0+1)^3`. Indeed it lies in the ball of
radius `R+sqrt(2 h_0 log 2)<=R+h_0+1`, and `pi<4`.
Enlarging `m` to this bound signs the whole interval `[2^(-h_0),1]`.
A uniform low-threshold sign is a separate obligation.

## 2. Credited rigidity and bulk estimates

We use the Procrustes and top-set estimates from the accepted
[near-isometry proof](../gaussian_contact_near_isometries/PROOF.md),
and the bulk decomposition of
[R8's mean-loss proof, Sections 4--5](../gaussian_mean_loss_margin/PROOF.md).
Their relevant quantitative details are recalled here; no compactness
cutoff from that proof is assumed.

Double centering the pair-loss kernel and Procrustes alignment give

```text
M <= E Delta^2/(2 kappa) <= (2R^2/kappa)D,
M <= K_0 D,                  K_0=2m^3.                  (4)
```

One way to check the first inequality is to regard the centered coordinates
as operators `U,W:R^3->L^2(mu)`. With `J` the projection off constants,
`UU*-WW*=-(1/2)J Delta J`. Since `U*W` is positive semidefinite,
expansion using `U+W,U-W` gives
`||UU*-WW*||_HS^2 >= (kappa/2)||U-W||_HS^2`.
The bound `0<=Delta<=4R^2` gives the second inequality. Also, on the
source support, `|Y(x)|<=E|x-X|<=2m`.

For `E=E_f(v)`, `0<v<=m`, put `k_E(x)=integral_E gamma(z-x) dz`.
Gaussian derivatives obey `||grad gamma||_infinity<=C` and
`||D^2 gamma||_op,infinity<=C`. Thus `||D^2 k_E||<=Cv`.
Writing `r=(v/(4pi/3))^(1/3)<=m`, Gaussian tail bounds give

```text
a_f(v)>=C exp(-(r+m)^2/2),     E subset B(0,r+2m),
w_0=exp(-(r+3m)^2) <= gamma(z-x)gamma(z-b)/f(z)^2
                   <= w_1=exp((r+m)^2)                  (5)
```

for `z in E` and source centers `x,b`. The pointwise posterior-divergence
identity is

```text
grad k_E(x) = -a_f(v) integral_E integral (x-b)
                 gamma(z-x)gamma(z-b)/f(z)^2 dmu(b) dz. (6)
```

It follows by the divergence theorem applied to `gamma(z-x)/f(z)`.
At a critical level, approximate by regular levels: positive Gaussian
mixture levels are null sets, all the sets stay in a compact ball, and
dominated convergence proves the same identity. No differentiation of the
level or division by `|grad f|` is needed.

Fix `delta>0`. Put `A_delta={|h|<=delta}`, `B_delta=A_delta^c`,
`alpha=mu(B_delta)<=K_0D/delta^2`, and use unnormalized pair integrals
`D_AB=integral_(A x B) Delta dmu dmu`. If

```text
m sqrt(M)<=1/(2m),
alpha<=min(1/2,1/(8m^3)),                               (7)
```

then the bulk estimate is

```text
(1/v) integral_A [k_E(Y(x))-k_E(x)] dmu(x)
 >= c_0 D_AA - K_1 delta D - C L^2 alpha^2
                         - K_2 alpha sqrt(M),           (8)

c_0=(C/4)exp(-18m^2), K_1=16Cm^2,
L=96m^4+6m,           K_2=2mC exp(4m^2).
```

Here is the conditional-alignment detail behind the squared rare-mass
error. Under (7), global `A>=I/(2m)` and the conditional bulk source
covariance is at least `I/(2m)`. The conditional centered cross-covariance
differs from `A` in Frobenius norm by at most `12 alpha m^2`.
Optimality of the conditional orthogonal alignment `Q` gives

```text
||I-Q||_F <= 48 alpha m^3.
```

The conditional means have norms at most `2alpha m,4alpha m`, so
the conditional rigid alignment changes `Y` by at most `L alpha`.
For two bulk points, `Delta<=8m delta`. Apply (4) conditionally and
return to the global alignment, using `1-alpha>=1/2`, to get

```text
M_A=integral_A |h|^2 dmu <= 32m^2 delta D+2L^2 alpha^2.  (9)
```

Symmetrization of (6) on `A x A` yields the nonnegative kernel
`[Delta+|h(x)-h(b)|^2]/4`, which gives `c_0 D_AA` by (5).
The `A x B` term costs at most `K_2 alpha sqrt(M)`.
Taylor's theorem costs at most `(C/2)M_A`, proving (8).

## 3. Projecting the background for a rare move

Fix a source point `x` with `y=Y(x)`, `l=|y-x|>delta`,
`e=(y-x)/l`, and `q=|x|^2-|y|^2`. Let

```text
P={z:q+2z.(y-x)>=0}.
```

For an independent source point `Z` with displacement `h_Z`, contraction
gives the exact identity

```text
0 <= Delta(x,Z)=q+2Z.(y-x)+2(y-Z).h_Z-|h_Z|^2.
```

Since `|y-Z|<=3m`, project `Z` orthogonally onto `P`, writing `Z'`:

```text
eta=E|Z'-Z| <= (3m/l) E|h_Z| <= 3m sqrt(M)/delta.        (10)
```

Indeed the distance projected is `[-q-2Z.(y-x)]_+/(2l)`.
The bisector's distance from the origin is at most `3m/2`; projection
therefore gives `|Z'|<=sqrt(m^2+(3m/2)^2)<2m`.
Set `b=E Z'`. Then `|b|<=eta`. Translate the actual background,
the projected background, `x,y`, and the test set all by `-b`.
In this section only, use `x',y'` for the translated points, and `f,f'`
for the translated actual and projected Gaussian mixtures, respectively.
The integral `k_E(y)-k_E(x)` is unchanged.

Suppose

```text
eta <= 1/(12m^2).                                      (11)
```

The actual centers then lie in `B(0,2m)`, the projected centered centers
and `x',y'` in `B(0,3m)`. Covariance perturbation is at most
`3m eta+eta^2<=1/(2m)`, so the projected covariance is at least
`I/(2m)`. The bisector is now `e.z=-a`, where

```text
q'=|x'|^2-|y'|^2=q+2b.(y-x)=2al,
a_min=1/(6m^2)<=a<=3m.      (12)
```

To prove the lower bound, the projected centered variable
`U=e.(Z'-b)` has mean zero, variance at least `1/(2m)`, and
`-a<=U<=3m`. Averaging `(U+a)(3m-U)>=0` gives
`3ma>=E U^2>=1/(2m)`.

Let `sigma` be reflection in `e.z=-a`. The actual source top set of
volume `v<=m`, after this translation, lies in `B(0,5m)` by the same
tail estimates as (5), since the actual centers have radius at most `2m`.
Consequently `E union sigma(E)` lies in `B(0,11m)`.

## 4. A quantitative polarization margin on the actual top set

Define

```text
c_D=exp(-361m^2/2), c_P=exp(-379m^2), c_G=exp(-361m^2),
tau=a_min c_D/16,
epsilon_f=C a_min c_P tau,       rho=epsilon_f/(16C).
```

Assume, in addition to (11),

```text
eta <= a_min c_P/4.                                    (13)
```

For `u` on the `y'` side of the bisector, put `t=e.u+a>=0`.
For a projected centered center `z`, put `w=e.z+a>=0`.
On `|u|<=16m`, we have `|u_perp-z_perp|<=19m`,
`t<=19m`, `w<=6m`, and `E w=a>=a_min`. The exact Gaussian reflection
formula and `sinh(tw)>=tw` give

```text
f'(u)-f'(sigma u)
 =2C E exp(-(|u_perp-z_perp|^2+t^2+w^2)/2) sinh(tw)
 >=2Ct a_min c_P.                                      (14)
```

The exponent bound used here is `(19^2+19^2+6^2)m^2/2=379m^2`.
The Hessian bound for the Gaussian, applied first along the center
coupling and then along `[u,sigma u]`, gives

```text
|[f-f'](u)-[f-f'](sigma u)| <= 2Ct eta.
```

Thus (13) proves, on the same domain,

```text
f(u)-f(sigma u) >= Ct a_min c_P.                        (15)
```

In particular the actual top set is polarized: on the `y'` halfspace,
`1_E(u)-1_E(sigma u)>=0`. If either indicator is nonzero then
`|u|<=11m`, so (15) applies; outside this region both vanish.

We need a positive amount, uniformly even when `v` tends to zero.
For any `|u|<=16m` and `t=e.u+a`, differentiating the projected density
and using `Ew=a` gives

```text
partial_e f(u) >= C(a_min c_D-max(t,0)-eta).             (16)
```

Indeed the nonnegative `w` contribution has every Gaussian weight at
least `C c_D`; the negative `t` contribution is at least `-C max(t,0)`;
the center coupling changes the derivative by at most `C eta`.
For `t<=8tau`, (13) and `c_P<=c_D` make (16) at least `4C tau`.
Every global mode is in the convex hull of the actual centers, hence in
`B(0,2m)`, by the Gaussian score equation. Its derivative is zero, so
every mode has `t>8tau`.

If `u in B(0,5m)` has `t<=tau`, then

```text
f(u) <= max f-epsilon_f.                               (17)
```

For `t<=-tau`, reflect and use (15) at `sigma u`, which is in
`B(0,11m)`. For `|t|<=tau`, move `u` by `4tau e`.
The segment has `t<=5tau` and lies in `B(0,16m)`; (16) increases
the density by at least `16C tau^2=C a_min c_D tau>=epsilon_f`.

Write `a_f` for the actual top-set level. There are two cases.

* If `a_f>max f-epsilon_f/2`, (17) puts all of `E` in `t>tau`.
  Its reflections have `t<-tau` and are outside `E`. Thus the polarized
  difference of indicators is one on a set of volume `v` with `t>tau`.
* If `a_f<=max f-epsilon_f/2`, start at a global mode and follow the
  ray in direction `e` to infinity. Continuity and decay give a point
  `u_0` with `f(u_0)=a_f+epsilon_f/4`. It lies in `E`, hence in
  `B(0,5m)`, and has `t>8tau`. By (15), its reflection has density
  at most `f(u_0)-8epsilon_f`. The global bound `|grad f|<=C` now
  puts `B(u_0,rho)` inside `E` and its reflection outside `E`.
  This ball has `t>7tau`, since `rho<tau`.

On either positive region, `|u|<=16m`, `|x'|<=3m`, and

```text
gamma(u-y')-gamma(u-x')
 =gamma(u-x') [exp(tl)-1]
 >= C t l exp(-361m^2/2)
 >= C tau c_G q'/(6m).                                 (18)
```

The last step uses `q'=2al<=6ml`. Pairing the two halfspaces gives
the exact integral identity

```text
k_E(y)-k_E(x)
 = integral_(t>0) [1_E(u)-1_E(sigma u)]
                   [gamma(u-y')-gamma(u-x')] du.
```

All its integrands are nonnegative by (15). The two alternatives above
and `v<=m` therefore prove the explicit bound

```text
(k_E(y)-k_E(x))/v >= beta q',
beta=(C tau c_G/(6m)) min(1, (4pi/3)rho^3/m)>0.          (19)
```

This argument neither changes the tested top set nor compares its level
with a perturbed level. It also avoids a unique-mode, nondegenerate-mode,
or quantitative level-set regularity assumption.

## 5. Restoring the actual one-label loss

The actual loss of `x` against an independent label is

```text
q_x=E Delta(x,Z)=q+D/2.
```

Moreover `|q-q'|<=2eta l`. By (11)--(12), this is at most `q'/2`.
If also

```text
D <= delta/(3m^2),                                     (20)
```

then `D/2<=q'/2`, because `q'>=l/(3m^2)>delta/(3m^2)`.
Thus `q_x<=2q'`, and (19), integrated over the rare labels, gives

```text
(1/v) integral_B [k_E(Y(x))-k_E(x)] dmu(x)
 >= (beta/2)(D_BA+D_BB).                               (21)
```

The background projection depended on the rare label; no common repaired
map or common background law is required. Each comparison is on the
same actual source top set and can therefore be integrated.

## 6. Explicit choices and the error budget

Take

```text
c_*=2^(-8192m^2),    delta=2^(-8196m^2),
D <= 2^(-65536m^2).
```

The elementary bounds `e<4`, `1/32<C<1`, `4pi/3>1`, and `m>=2`
give the following safe estimates:

| Quantity | Bound |
|---|---|
| `c_0` | `>=2^(-38m^2)` |
| `K_0,K_1` | `<=2^(2m^2)` |
| `K_2` | `<=2^(9m^2)` |
| `L` | `<=2^(4m^2)` |
| `tau` | `>=2^(-364m^2)` |
| `rho` | `>=2^(-1125m^2)` |
| `beta` | `>=2^(-4466m^2)>=2^(-4608m^2)` |
| `alpha` | `<=2^(-49142m^2)` |
| `eta` from (10) | `<=2^(-24570m^2)` |

For details of the only polynomial absorptions needed, each inequality
`A m^p<=2^(b m^2)` below is true at `m=2`; at each integer increment
the left side grows by at most `(3/2)^p`, whereas the right side grows
by at least `2^(5b)`. This proves every row for all integers `m>=2`:

```text
(A,p,b)=(1,1,1),(2,1,1),(3,1,1),(6,1,2),
        (6,2,2),(12,2,2),(96,2,3),(24,2,3),
        (16,2,2),(2,3,2),(102,4,4).
```

For example `tau=e^(-361m^2/2)/(96m^2)>=2^(-364m^2)`;
`rho=tau e^(-379m^2)/(96m^2)>=2^(-1125m^2)`.
The prefactor of `beta` is at least `2^(-1090m^2)`, and its minimum
factor at least `2^(-3376m^2)`. Also `C/4>2^-7>=2^(-2m^2)`
proves the `c_0` row. All exponents remain symbolic; their enormous
denominators need not be materialized.

The table verifies all side conditions (7), (11), (13), and (20).
For (13), `a_min c_P/4>=2^(-761m^2)`. For (7), use
`m sqrt(M)<=2^(-32766m^2)` and the displayed bound on `alpha`.
For (20), `delta/(3m^2)>=2^(-8198m^2)`.
In particular `c_*<=min(c_0,beta/4)`.

The three errors in (8), divided by `D`, satisfy

```text
K_1 delta                  <= 2^(-8194m^2)  <= c_*/4,
C L^2 alpha^2/D            <= 2^(-32740m^2) <= c_*/8,
K_2 alpha sqrt(M)/D        <= 2^(-16364m^2) <= c_*/8.     (22)
```

For the last two estimates use respectively
`L^2 K_0^2 D/delta^4` and
`K_2 K_0^(3/2) sqrt(D)/delta^2`.
Combining (8), (21), and `D=D_AA+2D_AB+D_BB` now gives

```text
(1/v) integral_E(g-f) >= c_*D-(c_*/2)D
                       >= 2^(-8193m^2)D.
```

The `D_AB` coefficient is retained because `beta/2>=2c_*`.
For `D=0`, (4) gives `M=0`. The profile and hinge conclusions follow
by testing their variational formulas on the actual source top set.
This proves all claims in Section 1. QED.

## 7. Calibration, finite-frontier use, and limitations

The five-point rare fold from R8 is a calibration of the quantifiers,
not a new positive class. Give

```text
(-1,0,0), (-2,1,0), (-2,0,1), (-2,-1,-1)
```

equal total mass `1-alpha` and give `(1,0,0)` mass `alpha`,
`0<alpha<=1/2`. Apply `T(x)=(-|x_1|,x_2,x_3)` and divide coordinates
by six. After centering, the identity is a Procrustes alignment,
radius is at most `1/2`, and covariance is at least `I/384`. Exactly,

```text
D=(7/18)alpha(1-alpha), M=alpha(1-alpha)/9,
ess sup |h|=(1-alpha)/3, E Delta^2/D=13/63.              (23)
```

With `m=384` and any positive `alpha<=2^(-65536m^2)`, the explicit
guard applies. For `u>=1/4`, the source superlevel volume is less than
`(16/3)(5/2)^3=250/3<384`. Thus it supplies an actual computable
choice of the rare mass, while the maximum displacement stays away from
zero and the quartic loss ratio stays above `2^-48`. Both the near-isometry
and quartic-loss sufficient conditions are distinct from this mean-loss
guard. The fold already has majorisation by classical polarization.

For the shared finite frontier, the reusable comparison is a numerical
loss floor: at fixed radius, covariance and source volume, an adverse input
must have `D>2^(-65536m^2)`. This closes the previously non-effective
zero-loss neighborhood even with vanishing atom masses and finite rare
moves. Conditional on this parameter region, the existing positive-loss
cubature/mesh machinery can use the displayed floor without an unknown
compactness modulus. The numerical bound is far too small to assert a
practical search or a completed finite cover.

Covariance collapse, unrestricted volumes (threshold tending to zero),
positive losses beyond this guard, and the complete dimension-three question
remain open. No overlap with a low-threshold endpoint is assumed.

`projection_controls.py` uses exact rational finite fixtures and integer exponent
bookkeeping. It verifies the reflection/projection algebra, polynomial
absorptions, budget, and calibration, with adverse controls. It does not
formalize Gaussian differentiation, level approximation, polarization,
or the universal proof. No quadrature, solver, hidden corpus or large
computation is used, and no independent acceptance is claimed.
