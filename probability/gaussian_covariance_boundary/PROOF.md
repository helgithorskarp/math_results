# Covariance-boundary signs at arbitrary radius and threshold

27 September 2026. Complete author proof, pending independent review.
The full dimension-three majorisation question remains open.

This gives a uniform signed neighborhood of either marginal's covariance-
degenerate boundary on every bounded, positive-loss, positive-threshold slab.
The law, map, atom count and weights may all vary. It complements the
[effective small-loss theorem](../gaussian_effective_mean_loss/PROOF.md),
which requires a positive covariance floor. Their simultaneous zero-loss,
zero-covariance corner is **not** closed by combining them.

R2's concurrent [covariance-collapse guard](../gaussian_covariance_collapse_guard/PROOF.md)
already uses source/target plane projection and proves the stronger covariance
cutoff `2^-86 D^2` when the normalized radius is at most `1/2` and the
threshold floor is `1/64`. Those projection and boundary-exclusion mechanisms
are credited, not claimed new here. This packet supplies a complementary
all-radius, arbitrary-positive-threshold estimate. Its target-peak argument
retains a margin through the ACTUAL source peak, with a weaker covariance
cutoff of order `D^10`. It does not improve or imply R2's sharper guard.
The geometric comparison and quantitative motion margin are also credited
inputs. No projected map needs to be computed for the exact certificate.

## 1. Uniform theorem and finite-frontier consequence

Work at Gaussian variance one. Let

```
C=(2 pi)^(-3/2), gamma(z)=C exp(-|z|^2/2),
E X=0, |X|<=R, Y=T(X), T:R^3 -> R^3 1-Lipschitz,
D=E[|X-X'|^2-|Y-Y'|^2],
f=law(X)*gamma, g=law(Y)*gamma,
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+.
```

Primes denote independent copies. Source centering is harmless; target
translation does not affect a hinge. Take integers

```
R>=1, m>=1, k>=0,
q=ceil(sqrt(2(m+1))),
B=31+47R^2+2(2R+q)^2+5k,
L=2B+4.                                                   (1)
```

**Theorem 1.** Suppose `D>=2^-k` and, for some unit vector `e`, either

```
Var(e.X) <= 2^-L  OR  Var(e.Y) <= 2^-L.                 (2)
```

Then

```
H(u)>=0                         for EVERY u>=2^-m,        (3)
H(u)>=2^(-B-1)     if 2^-m<=u<=||f||_infinity/C.          (4)
```

In particular this is a strict actual-hinge margin throughout every
potentially adverse threshold in that interval. No covariance lower bound,
minimum mass, finite support, or small maximum displacement is assumed.
The integer radius can be any upper bound; rounding a real bound up only
makes the certificate more conservative.

Since `D<=2R^2`, (4) also gives the uniform normalized margin

```
H(u)/D >= 2^(-B-2)/R^2.                                 (5)
```

**Corollary 2 (interior covariance for an adverse input).** Within the
slab `|X|<=R`, `D>=2^-k`, `u>=2^-m`, any input with `H(u)<0` must have

```
Cov(X) > 2^-L I_3  AND  Cov(Y) > 2^-L I_3.             (6)
```

Thus the whole covariance-degenerate boundary of each such compact search
is excluded with a known number, rather than a qualitative continuity
argument. This does not assert a positive sign on the remaining interior.

At covariance `s I_3`, use coordinates divided by `sqrt(s)`, loss `D_raw/s`
and directional variance `Var(e.X_raw)/s`. The hinge itself is unchanged
under the corresponding spatial change of variables and normalized
threshold `C_s u`. No uniform assertion as `s` tends to zero is made.

For example, `R=1,m=6,k=1` gives `B=155,L=314`: normalized mean loss at
least `1/2` and either marginal's directional variance at most `2^-314` imply all
hinges above `1/64` are nonnegative, with margin at least `2^-156` through
the source peak. These are sufficient constants, not optimal ones.

## 2. Credited plane projections and retained loss

### 2.1 Source covariance

Let `P=I-e e^T` and put

```
X0=PX, Y0=T(PX), lambda=E|X-X0|^2, eta=sqrt(lambda),
D0=E[|X0-X0'|^2-|Y0-Y0'|^2].                            (7)
```

If the map was initially given only on the source support, first choose
one classical Kirszbraun extension. Only its 1-Lipschitz property is used;
no particular extension needs to be found or supplied to the certificate.
After translating the image by `T(0)`, all of `Y,Y0` have norm at most R.
Also `E X0=0`, `|X0|<=R`, and `E|Y-Y0|^2<=lambda`.

For any coupled square-integrable vectors U,V, write `Var` for the trace
of covariance. The triangle inequality in centered L2 gives

```
|Var(U)-Var(V)|
 <= (sqrt(Var(U))+sqrt(Var(V))) sqrt(Var(U-V)).           (8)
```

Consequently `|Var(Y)-Var(Y0)|<=2R eta`, while
`Var(X)-Var(X0)=lambda`. Since mean pair loss is twice the difference
of the two variances,

```
|D-D0| <= 2lambda+4R eta <= 6R eta.                     (9)
```

The last step uses `eta<=R`. In particular, if
`eta<=2^-k/(12R)`, then `D0>=2^(-k-1)>0`.

The projected pair has a continuous contracting motion in R5: identify
the plane with R2 and use

```
F_t(x)=(sqrt(1-t) PX, sqrt(t)[T(PX)-T(0)]) in R2 x R3.
```

Its pair distances squared are `(1-t)|PX-PX'|^2+t|Y0-Y0'|^2`.
Append a rigid rotation at the endpoint if needed to use the common
three-dimensional coordinate subspace. The anchor 0 is part of the same
motion and every center stays within distance R of its moving anchor.
Thus the existing R5 motion comparison and its quantitative hinge margin
apply to these reference laws, including diffuse laws and collisions.
This low-dimensional positive comparison is prior work, not a new class.

### 2.2 Target covariance

Instead suppose `lambda=Var(e.Y)` satisfies (2). Translate Y by its mean,
which changes none of the quantities of interest, so that EY=0, and put

```
X0=X, Y0=PY, eta=sqrt(lambda).
```

Here `E|Y-Y0|^2=lambda`. Projection is contractive, so `X -> Y0` is
an actual contraction and

```
D0=D+2lambda >= D.                                     (9a)
```

The reference motion is now the R3-plus-R2 lift
`F_t(x)=(sqrt(1-t)x,sqrt(t)PTx)`, using the translated map T.
Include the anchor x=0 and subtract its moving position. Each center
then stays within R of the anchor, because `|P(Tx-T0)|<=|x|<=R`.
At the endpoint, a rigid rotation identifies the target plane with the
original R3. Translations and this rotation change neither peaks nor hinges.

For this case the approximation bounds below are stronger: `f=f0`,
`||g-g0||_1<=eta`, `F=F0`, and `|H-H0|<=eta`. Both cases therefore
satisfy the common bounds (10), have a centered reference source in B_R,
and obey `D0>=2^(-k-1)` under the side conditions (19).

## 3. Endpoint approximation and a uniform peak gap

Write `f0=law(X0)*gamma`, `g0=law(Y0)*gamma`, and let `F,F0,G0` be the
maxima of `f,f0,g0`, respectively. Gaussian translation bounds give

```
||f-f0||_1 <= eta,       ||g-g0||_1 <= eta,
||f-f0||_infinity <= C eta,
|H(u)-H0(u)| <= 2eta,   F<=F0+C eta,                    (10)
```

where `H0` is the favorable reference hinge. Indeed,
`||partial_e gamma||_1=sqrt(2/pi)<1` and
`||grad gamma||_infinity=C/sqrt(e)<C`. Integrate the translation bounds
over the common labels and use Cauchy--Schwarz. The map `a -> (a-h)_+`
is 1-Lipschitz, which proves the hinge estimate. All bounds are global
and uniform in the threshold.

The source-posterior peak inequality from the earlier rigidity result is
particularly useful here. We recall its short proof and normalization.
Let z maximize f0, and give labels posterior density
`gamma(z-X0)/F0`. Then `E_posterior X0=z`. If
`v=E_posterior Y0`, Jensen's inequality yields

```
g0(v)/F0 >= exp(E_(posterior x posterior) Delta0 / 4),
Delta0=|X0-X0'|^2-|Y0-Y0'|^2>=0.                       (11)
```

This follows by taking the expectation of
`exp((|z-X0|^2-|v-Y0|^2)/2)`; the difference of posterior variances
equals half its posterior mean pair loss. The mode z lies in the convex
hull of the source, so `|z|<=R`. Since `F0<=C`, the posterior density
relative to the original labels is at least `exp(-2R^2)`.
Also `F0>=f0(0)>=C exp(-R^2/2)`. Therefore

```
G0-F0 >= (C/4) exp(-9R^2/2) D0.                        (12)
```

This is a credited posterior inequality, not an inference from entropy
ordering alone. Put

```
Z=k+4+9R^2, zeta=2^-Z.                                 (13)
```

Since `e<4`, `exp(-9R^2/2)>=2^(-9R^2)`. If `D0>=2^(-k-1)` and
`eta<=zeta`, equations (10)--(12) give

```
G0 >= F+C zeta.                                        (14)
```

This separates the reference target peak from the ACTUAL source peak,
which is needed to cover all possibly adverse high thresholds uniformly.

## 4. Consume the target-peak motion margin

The credited [target-peak theorem H2](../gaussian_axial_cone_rotations/HINGE_MARGIN.md)
states that a reference contraction with the R5 motion and radius bound R
satisfies, for `0<h<M<=G0`,

```
H(g0,h)-H(f0,h)
 >= K(R,(M+h)/2,h)
       min{D0, 4 exp(-R^2) log(2M/(M+h))},               (15)

K(R,a,h)=A ((a-h)/C)^4
       exp(-(2R+sqrt(2 log(2C/h)))^2),
A=exp(5/2)/(96 sqrt(2pi)).
```

It follows from the primary paper's Stieltjes pressure identity in R5,
a uniform radial shell estimate, and two-coordinate Gaussian
marginalization. Its proof includes critical levels and only continuous
contracting motions. Its source-peak version alone would not justify
the argument here. The precise dependency and author-review boundary
are recorded in SOURCES.md.

For `2^-m<=u<=F/C`, put `h=Cu` and `M=G0`. By (14),
`M-h>=C zeta`. Also `M<=C`, and hence

```
log(2M/(M+h))
 =-log(1-(M-h)/(2M)) >= (M-h)/(2M) >= zeta/2.            (16)
```

Because `D0>=2^(-k-1)` and `zeta<=2^(-k-4)`, the minimum in (15)
is at least `exp(-R^2) zeta`. Moreover `A>2^-7` (use `e>2` and
`sqrt(2pi)<3`), and `sqrt(2 log(2/u))<=q` because `log 2<1`.
Thus (15) implies

```
H0(u) >= 2^-11 zeta^5
          exp(-R^2-(2R+q)^2)
       >= 2^(-11-5Z-2R^2-2(2R+q)^2)=2^-B.              (17)
```

All rounding directions in this lower bound use `e<4`. The factor
`zeta^5` accounts for both the fourth power in the shell margin and the
terminal amount of loss; it is not optimized.

## 5. Close every side condition

Hypothesis (2) gives `eta<=2^(-B-2)`. The integer formulas show

```
B+2>=Z,
B+2-k>=4R^2,          12R<=2^(4R^2) for integer R>=1.  (18)
```

For the last inequality, `12R<=16^R` follows by induction, and
`16^R<=16^(R^2)`. Consequently

```
eta <= min{zeta, 2^-k/(12R), 2^-B/4}.                  (19)
```

Equations (9), (14) and (17) are all applicable. Finally (10) gives
`H(u)>=2^-B-2eta>=2^(-B-1)` whenever `2^-m<=u<=F/C`.
For `u>F/C`, the actual source hinge is zero, so `H(u)>=0` directly.
This proves (3)--(4), including all thresholds above one. Bound (5)
uses `D=2(Var(X)-Var(Y))<=2R^2`. The contrapositive applied to a minimum
eigenvector of either marginal gives (6). QED.

## 6. Exact certificate and the remaining corner

[certificate.py](certificate.py) emits only the integer exponents in (1).
For finite rational data it accepts a marginal `side` (source or target),
a nonzero rational direction n and
checks the centered directional variance

```
sum_i p_i (n.(z_i-mean z))^2 / (s |n|^2),
where z=x for side=source and z=y for side=target,
```

against `2^-L`. No eigenvector approximation, projected target, extension
algorithm, or Gaussian integration is required. The source radius, every
active pair contraction and the exact mean-loss floor are also checked.
Floats and malformed inputs are rejected; a failed sufficient guard is
`UNRESOLVED`. Dyadic comparisons use integer bit lengths, so the code
does not construct enormous denominators just to describe a guard.

An exactly planar marginal already gives full majorisation by the credited R5
lift, and zero mean loss already gives a rigid endpoint pair. The checker
reports those known branches separately from the new positive-width guard.

R3's existing paired cubature retaining marginal degree-two moments and
original sites preserves the radius, covariance and mean loss entering
this theorem for either marginal. The same supplied direction remains a certificate. No
additional mixed moments or mass bounds are needed. This is a direct
consumer of that interface, not a new cubature construction or a claim
that a uniform rule for diffuse inputs has been computed.

On each slab with a fixed positive loss floor and threshold floor, the
normalized sign margin (5) is independent of how close the covariance is
to collapse. The slab may therefore be restricted to the explicit positive
covariance floor (6) when searching for an adverse input. R2 can use the
guard before computing moments or hinges.

When D and the smallest covariance eigenvalue both tend to zero, the
current guard has width of order `D^10` at fixed radius and threshold.
The accepted small-loss theorem has its own covariance-dependent cutoff.
These inequalities do not cover every joint approach to that corner.
Nor does either supply the uniform low-threshold overlap required for
full majorisation. No unrestricted theorem, new Kneser--Poulsen case,
or practical complete enumeration follows from this result.
