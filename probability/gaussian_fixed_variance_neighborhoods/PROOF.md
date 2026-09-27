# A fixed-variance all-threshold neighborhood of a buffered comparison

27 September 2026. Complete author proof; independent review and
formalization pending. The unrestricted R3 Gaussian-majorisation question
remains open.

The new ingredient is a quantitative strict homothety inserted before an
already signed comparison. It supplies a hinge margin up to and beyond the
source peak. A directional moment-generating-function bound supplies the
remaining thresholds down to zero. Independent spatial and prior errors
at both endpoints can then be absorbed, at any **specified** variance.
The allowed errors depend on that variance. This is not an all-variance
theorem for one fixed positive neighborhood.

## 1. Reference comparison and perturbations

Work first at variance one. Write

```text
C=(2 pi)^(-3/2),  gamma(z)=C exp(-|z|^2/2),
H_f(h)=integral_R3 (f(z)-h)_+ dz,  h>=0.
```

Fix integers R>=1 and j,k>=0, and put kappa=2^-j, eta=2^-k.
Let X be a probability law with

```text
E X=0,  |X|<=R,  Cov(X)>=kappa I_3.                       (1)
```

Choose 0<=c<=1-eta and a reference target Z, |Z|<=R, with the two premises

```text
E exp(v.Z) <= E exp(v.(cX))        for every v in R3,      (2)
H_(law(Z)*gamma)(h) >= H_(law(cX)*gamma)(h) for every h.   (3)
```

One sufficient witness for (2) is a coupling (U,W) with laws cX,Z and
E[U|W]=W. Conditional Jensen proves the assertion. Premise (3) is a
separate Gaussian-order certificate; a martingale alone is not asserted
to prove it. Taking Z=cX supplies both premises without any external
comparison theorem. Section 7 gives a nontrivial finite reference using
the independently accepted R2 balanced-loss guard.

The actual source law mu is obtained by first replacing law(X) by a
probability law with Radon--Nikodym density in [1-rho_x,1+rho_x], and then
transporting it by an arbitrary plan with displacement at most alpha_x.
The target nu is independently obtained from law(Z) with errors rho_y,
alpha_y. All four errors are nonnegative. Arbitrary atomic, diffuse and
mixed clouds are allowed, with no atom-mass floor or atom-count bound.
Set

```text
E = alpha_x+alpha_y+rho_x+rho_y,
A = (R+1)^2+j+2R+4,
S = 8R 2^(j+k) A,
m = (S+R+1)^2,
ell = j+k+6R^2+3,
Q = (2R+1)^2,
B = m+j+k+3ell+Q+13.                                    (4)
```

**Theorem 1.** If

```text
                         E <= 2^(-B-1),                  (5)
```

then, for f=mu*gamma and g=nu*gamma,

```text
H_g(h) >= H_f(h)                         for every h>=0. (6)
H_g(h)-H_f(h) >= 2^(-B-1)
                  if C 2^-m <= h <= max f.               (7)
```

The majorisation statement (6) does not require a deterministic map
between the actual laws. If in addition nu=T_#mu for a 1-Lipschitz map,
then its mean ordered squared pair loss is strictly positive:

```text
D=E_(X',X'' iid mu)[|X'-X''|^2-|T(X')-T(X'')|^2]
 =2(tr Cov(mu)-tr Cov(nu)) >= 3 eta kappa >0.              (8)
```

Thus the theorem signs a whole positive-loss bounded-law neighborhood;
it is not only a defect estimate tending to zero. For fixed R,j,k the
same schedule works uniformly over all references satisfying (1)--(3),
all allowed c and all such independent perturbations.

## 2. Posterior covariance and a strict homothety margin

For 0<=t<=1 write f_t=law(tX)*gamma, M_t=max f_t, and let pi_(t,z) be
the posterior law of X with weight proportional to exp(-|z-tX|^2/2).
Because its denominator is at most one, its density relative to law(X)
is bounded below by exp(-(|z|+R)^2/2). Variance is the infimum over
centers of a quadratic integral. Therefore

```text
Cov_pi(X) >= kappa exp(-(|z|+R)^2/2) I_3.                 (9)
```

Put b_t(z)=E_pi X. Differentiating the bounded Gaussian integrals gives

```text
partial_t f_t = -div(f_t b_t),
grad b_t = t Cov_pi(X),
grad f_t = f_t(t b_t-z).                                 (10)
```

Every maximizer of f_t satisfies z=t b_t(z), hence |z|<=R. At such a point,

```text
partial_t f_t(z) = -t f_t(z) tr Cov_pi(X).                (11)
```

All maxima lie in the same compact ball. Uniform differentiability of
f_t there implies that M_t is Lipschitz, and the upper right envelope
derivative is bounded by the largest partial_t f_t at its maximizers.
For completeness, choose a maximizer z_h at t+h, use
M_(t+h)-M_t <= f_(t+h)(z_h)-f_t(z_h), and pass to a convergent subsequence
of z_h. Its limit is a maximizer at t. Apply (9)--(11). At almost every t,

```text
(log M_t)' <= -3 kappa t exp(-2R^2).                     (12)
```

Here log M_t is absolutely continuous because
M_t>=f_t(0)>=C exp(-R^2/2)>0. Integrating (12) from t to 1, using
exp(u)-1>=u, gives, whenever t<=1-eta/2,

```text
M_t-M_1
 >= (3/4) C kappa eta exp(-(5/2)R^2)
 >= C 2^-ell.                                           (13)
```

We used 1-t^2>=eta/2. For the last inequality, e<4 yields
exp(-(5/2)R^2)>=2^(-5R^2); the definition of ell leaves ample slack.
Let d=2^-ell. The global bound ||grad f_t||_infinity<=C implies that
the ball of radius d/4 about any mode has

```text
f_t >= M_1+3Cd/4   when t<=1-eta/2.                      (14)
```

There is also an exact hinge derivative:

```text
(d/dt) H_(f_t)(h) = -ht integral_{f_t>h} tr Cov_pi(X) dz,
                                                    h>0. (15)
```

This does not require regular level sets. Each f_t is real analytic and
nonconstant, so {f_t=h} has Lebesgue measure zero. Gaussian tails bound
partial_t f_t by an integrable function uniformly in t, justifying
differentiation of the hinge. The set {f_t>h} is bounded. The weak
divergence identity for (f_t-h)_+ b_t, which has compact support, gives

```text
integral_{f_t>h} [b_t.grad f_t+(f_t-h) div b_t] =0.
```

Substitute (10) to obtain (15). The resulting hinge is absolutely
continuous in t. This is the familiar homothety monotonicity mechanism;
the uniform quantitative use of it below is the bridge needed here.

Integrate (15) on the interval

```text
I=[1-3eta/4,1-eta/2] subset [c,1].                       (16)
```

Its length is eta/4 and t>=1/4 on I. If h<=M_1+Cd/2, (14) puts a ball
of radius d/4 inside {f_t>h}. On that ball |z|<=R+1, so (9) gives
tr Cov_pi>=3 kappa 2^-Q. Its volume is pi d^3/48>=d^3/16. Hence

```text
H_(f_c)(h)-H_(f_1)(h)
 >= (3/256) h eta kappa d^3 2^-Q,
                                      0<h<=M_1+Cd/2.    (17)
```

Since C>=2^-5, (4) implies in particular

```text
H_(f_c)(h)-H_(f_1)(h) >= 2^-B
                  if C2^-m <=h<=M_1+Cd/2.               (18)
```

This bound covers a noncollapsed interval all the way beyond the source
peak. It does not use entropy ordering, moment matching, or a finite
selection of thresholds to infer hinge ordering.

## 3. Pointwise tail dominance supplies every remaining threshold

For any unit theta let W=theta.X, a=kappa/(4R), p=kappa/(4R^2).
Centering and |W|<=R give

```text
E W_+ = E|W|/2 >= kappa/(2R),
E W_+ <= a+R P(W>=a),
P(W>=a)>=p,
M_X(r theta):=E exp(r theta.X)>=p exp(ar),
M_X(r theta)>=1.                                        (19)
```

The reweighting and transport assumptions imply, for r>=0,

```text
f(r theta)/C >= (1-rho_x)
 exp(-r^2/2-r alpha_x-(R+alpha_x)^2/2) M_X(r theta),
g(r theta)/C <= (1+rho_y)
 exp(-r^2/2+r alpha_y) M_Z(r theta).                     (20)
```

By (2), log-convexity of M_X and M_X(0)=1,

```text
M_Z(r theta)<=M_X(cr theta)<=M_X(r theta)^c.             (21)
```

The schedule (4)--(5) ensures rho_x,rho_y<=1/2, alpha_x<=1 and
alpha_x+alpha_y<=eta kappa/(8R). Thus (19)--(21) yield

```text
log(f(r theta)/g(r theta))
 >= r eta kappa/(8R) - (R+1)^2/2 -log 3-eta log(1/p)
 >= r eta kappa/(8R)-A.                                (22)
```

Indeed log 3<=2 and log(1/p)<=j+2+2R. By (4), f>=g whenever |z|>=S.
Both actual laws are supported in B_(R+1), so for |z|<=S,

```text
min(f(z),g(z))>=C exp(-(S+R+1)^2/2)>=C2^-m.              (23)
```

The last inequality uses log 2>=1/2. If 0<h<=C2^-m, then
min(f,h)=min(g,h)=h inside B_S and min(f,h)>=min(g,h) outside it.
Because both densities have mass one,

```text
H_g(h)-H_f(h)=integral [min(f,h)-min(g,h)]>=0.            (24)
```

This proves the entire low range, with no asymptotic remainder and no
limit-exchange problem at h=0. The value at zero is equality.

## 4. Perturbation transfer and the exact join

The standard Gaussian bounds

```text
||gamma(. -u)-gamma(. -v)||_1 <= |u-v|,
||gamma(. -u)-gamma(. -v)||_infinity <= C |u-v|
```

follow by integrating its directional derivative; the first constant is
sqrt(2/pi)<=1. Reweighting by a density in [1-rho,1+rho] contributes at
most rho in L1 and C rho in L-infinity. Averaging over the transport plans,

```text
||f-f_1||_1+||g-law(Z)*gamma||_1 <= E,
max f <= M_1+CE.                                       (25)
```

Hinges are 1-Lipschitz with respect to the density's L1 norm. Premise (3)
and (18) therefore imply (7), because (5) ensures E<=d/2. Thresholds
above max f satisfy (6) trivially. Equation (24) covers h<=C2^-m and
(7) covers every possible adverse threshold above it. This proves (6).

Here are elementary checks of all budget implications used in the proof:
the positive integer expressions in (4), for R>=1,j,k>=0, give

```text
B+1 >= ell+1,
B+1 >= j+k+3+R,
B+1 >= j+k+4+2R.
```

Using R<=2^R, these imply respectively

```text
E<=d/2,
E<=eta kappa/(8R),
E<=eta kappa/(16R^2).                                  (26)
```

They also imply E<=1/2. These are universal algebraic implications, not
claims based on the checker sampling integer schedules.

## 5. Positive loss and normalization of variance

Differentiating (2) at the origin in both signs of every direction shows
EZ=0. Its second-order term gives Cov(Z)<=c^2 Cov(X). Thus

```text
tr Cov(X)-tr Cov(Z)>=(1-c^2) tr Cov(X)>=3 eta kappa.       (27)
```

For any centered reference W with |W|<=R, reweighted and moved with
rho+alpha=e0<=1, the change in trace covariance is bounded by

```text
rho R^2+2R alpha+alpha^2+(rho R+alpha)^2 <=5R^2 e0.       (28)
```

To see this, first bound the change of the raw second moment by the
first three terms, and bound the perturbed mean by rho R+alpha. Combining
(27)--(28) at both endpoints and using (26),

```text
2(tr Cov(mu)-tr Cov(nu)) >=6 eta kappa-10R^2 E
                                      >=3 eta kappa.
```

This proves (8). The loss does not need to be an input to the certificate.

For any specified variance s>0, scale the reference coordinates and
spatial errors by 1/sqrt(s); reweighting errors are unchanged. Choose R,j
so that the scaled source satisfies (1), and require (3) at variance s
in the original coordinates. The theorem then applies. Original hinge
thresholds are multiplied by s^(3/2) under this change of coordinates,
and hinge *values* are unchanged. The original positive-loss bound becomes
3s eta kappa. Every centered bounded source with positive definite
covariance admits such finite R,j, at any specified s.

In particular, with Z=cX, every such law and every 0<=c<1 have a
nonzero spatial/prior neighborhood with full Gaussian majorisation at
the specified variance. No reference map is needed for this corollary.
There is no claim that one neighborhood works for all s tending to zero.

## 6. Relation to the R2/R3/R8 certificate spine

The [R8 small-target theorem](../gaussian_uniform_small_target/PROOF.md)
signs arbitrary sufficiently small target laws, without a shape premise.
The present theorem introduces a materially different reference premise:
Z can be comparable in scale to X and need not be concentrated near one
point. A strict homothety plus a certified second comparison supplies a
uniform interior hinge margin. The old small-target constants are not
claimed to follow from (4); the earlier theorem remains useful as stated.

The [R3 robust dilated-martingale theorem](../gaussian_robust_martingale_localization/PROOF.md)
uses the same useful independent spatial/prior neighborhood interface.
It only needs a trace-variance floor, then applies an eventual-noise
endpoint. The present proof requires full covariance and the additional
reference premise (3), and directly signs any specified variance. It
neither improves that theorem's cutoff constants nor claims to subsume it.

R2 can supply (3) from its [balanced-loss certificate](../gaussian_balanced_loss_certificate/PROOF.md),
[independently accepted](../gaussian_balanced_loss_certificate_review2/REVIEW.md).
Its exact martingale data can supply (2). R3 can then use a verified
support cover and relative cell-mass intervals to supply the four errors.
No approximation may replace these actual support and mass guarantees.
The desired original-law conclusion follows at the target variance when
(5) passes, with all h signed. This is the entire consumer interface.

The reviewed [norm-preserving theorem](../gaussian_norm_preserving_majorisation/PROOF.md)
already supplies all variances and the ball/cap consequences under its
exact geometric premise. This result instead tolerates independent
endpoint errors. A fixed-variance neighborhood alone does not imply a
new Kneser--Poulsen theorem via a small-noise limit. Nor do (2)--(3)
provide a universal certificate for an arbitrary unresolved contraction.

## 7. A nontrivial exact reference and a calibration with tight pairs

Take i=(u,v,w) in {-1,1}^3, chi_i=uvw, and set

```text
x_i=(u,v,w)/4,  z_i=(vw,uw,uv)/8,
t=1/256, c=1/2,
U_i=c x_i,  Y_i=c[(1-t)x_i+t z_i],
p_i=3/16 if chi_i=1, and 1/16 if chi_i=-1.               (29)
```

Then EX=0, Cov(X)=I/16, |X|<1, so R=1,j=4,k=1 are admissible.
The accepted R2 guard applies to U_i -> Y_i, after the common scale c,
because this is its full paired-rank Walsh family. It proves (3) for
the displayed weights (and every other set of weights).

Here is a different, exact coupling proving (2) for the displayed weights.
Let a_i=t/4 for chi_i=1 and a_i=3t/4 otherwise. Put

```text
pi_(j,i)=p_i a_i             if j and i differ in one sign,
pi_(i,i)=p_i(1-3a_i),
pi_(j,i)=0                  otherwise.                  (30)
```

Each undirected cube edge has the same mass 3t/64 in both directions,
so both marginals are p. At target i the source conditional mean is
c x_i(1-2a_i)=Y_i, since z_i=(chi_i/2)x_i. This proves the martingale
witness without asserting that the original deterministic matching is
a martingale.

To calibrate the cloud interface, for each macro label i and independent
v in {-1,1}^3 set

```text
P_(i,v)=x_i+epsilon v,
Q_(i,v)=Y_i+epsilon v,       weight p_i/8,
epsilon=2^(-B-4).                                      (31)
```

The parameters from (4) are recorded exactly by the checker, as integer
exponents; the huge denominator is never expanded. Spatial errors at
both endpoints are at most 2epsilon, so E<=4epsilon satisfies (5).

The pair is short for every 0<epsilon<=1/128. Indeed, for macro
differences a=x_i-x_j, b=Y_i-Y_j and micro difference q=v-v',

```text
Delta(epsilon)=|a|^2-|b|^2+2epsilon q.(a-b).             (32)
```

For i!=j, |b|<=|a|/2, |a|>=1/2, |q|<4 give
Delta>=(3/4)|a|^2-12epsilon|a|>0 throughout that interval.
For i=j every loss is exactly zero. There are 224 preserved unordered
pairs and 1,792 strictly decreased pairs. The checker also reconstructs
all affine losses and verifies their interval endpoints exactly.

The paired affine rank is six: fixing the micro label leaves the six
distinct Walsh characters in (29), whose coefficients are nonzero.
No choice of anchors a0,b0 can make all 64 paired norms equal. Expanding
such an equality while varying v at fixed i would force
x_i-Y_i=a0-b0 for every i, contradicted by any positive macro loss.
The all-pairs balanced-loss guard likewise fails on the actual 64-point
geometry: its minimum loss is zero and its Gram discrepancy is nonzero.
These are precise exclusions from these two sufficient interfaces, not
claims of exclusion from every known geometric class.

For completeness the macro target covariance is

```text
Cov(Y)=c^2(a0^2+b0^2+a0 b0) I_3,
a0=(1-t)/4, b0=t/8,
Cov(Y)>=(1/128) I_3.                                   (33)
```

The micro noise adds epsilon^2 I at both endpoints. Thus target covariance
and size remain comparable to those of the source. The old small-target
schedule does not certify this example at unit variance. For the
unperturbed reference X,Y, (30) is a dilated martingale with dilation two;
even its zero-error R3 eventual-noise schedule is s>=1584 (using the exact
source R^2=3/16 and V=3/16). Here unit variance is certified because we
also supplied the second comparison (3).

The calibration itself already has a simple contracting straight motion:
in a cross pair the micro contribution to the derivative is linear in
epsilon, and the endpoint test is positive as checked exactly. We do not
offer it as a new hard geometric example. The mathematical contribution
is the uniform implication for **every** allowed diffuse or atomic
perturbation and prior change, whether or not it has that motion.

## 8. Reproducibility and trust boundary

The standard-library exact checker reconstructs (29)--(33), the coupling
marginals and conditional means, the independent distance-based R2 guard,
paired rank, all 2,016 cloud-pair polynomials, and all budget side
conditions. It checks malformed parameters and deliberate witness/sign
damage. Integer exponents keep (31) compact; no floating-point Gaussian
quadrature or giant dyadic denominator is used.

The finite checks do not prove the universal analytic statement. Its
trust boundary is the conventional proof (9)--(28), including analytic
level-set and weak-divergence facts, Gaussian differentiation, and the
explicitly supplied reference comparison. The nontrivial reference uses
the accepted R2 guard; the special case Z=cX does not. Neither finite
testing nor source publication substitutes for independent mathematical
review. There is no claim of historical priority, a solution of the
unrestricted problem, or a new ball-volume consequence.
