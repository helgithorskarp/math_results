# All-radius localization of the Gaussian hinge curve at fixed covariance

Complete author proof, 27 September 2026. Independent review pending.
The unrestricted three-dimensional majorisation conjecture remains open.

The contribution is an explicit **all-radius, loss-proportional functional
modulus**, and consequently a whole-curve version of the accepted paired
cubature at every bounded radius. A positive covariance floor replaces the
small-radius hypothesis of the earlier functional estimate. This is not a
new signed map class. The constants below are deliberately conservative;
the resulting general certification budgets are not practical enumeration
bounds.

## 1. Statement and normalization

Let X have any bounded probability law in R3, let Y=T(X) for a contraction
on its support, and let s>0. Define

```
C_s=(2 pi s)^(-3/2), f=law(X)*gamma_s, g=law(Y)*gamma_s,
H(u)=integral(g-C_s u)_+ - integral(f-C_s u)_+, 0<=u<=1,
d=E[|X-X'|^2-|Y-Y'|^2]/s.
```

Primes denote independent copies. Suppose, for an integer R>=1 and a
positive number kappa,

```
|X-E X| <= R sqrt(s),       Cov(X)/s >= kappa I_3.       (1)
```

There is no atom-count, atom-mass, or positive loss lower bound. These
are hypotheses on the ACTUAL law, not an auxiliary full-rank measure.
Put

```
Lambda=1+4R^2/kappa,
T0=4(2R+3)^3 Lambda 2^(296R^2).
```

For each integer L>=0 define rational or integer constants

```
a=2^(-L), c=ceil(sqrt(2(L+1))), B=2R+c,
r=32B^2-1,                 K_L=56 B^3 2^(3L) Lambda.  (2)
```

**Theorem 1.** The following inequalities hold:

```
|H(u)| <= d T0 sqrt(u),                              0<=u<=1;       (3)
|H(u)-H(v)| <= d K_L |u-v|^(1/r),                    a<=u,v<=1;     (4)
|H(u)-H(v)| <= d[2T0 2^(-L/2)+K_L |u-v|^(1/r)],      0<=u,v<=1.    (5)
```

Thus the infimum of the right-hand bracket in (5) over L is a modulus
tending to zero with |u-v|. This assertion is uniform over all laws and
contractions satisfying (1), at arbitrary R. At d=0, H is identically zero;
no division by d is made.

In the accepted notation let P_N be the Bernstein--Durrmeyer reconstruction
of H from its beta row b_(N,k). Then

```
||P_N-H||_infinity <= d E_(N,L),
E_(N,L)=2T0 2^(-L/2)+K_L (N+2)^(-1/(2r)).             (6)
```

The infimum over L and N is zero. For fixed R,kappa and prescribed relative
error, N can therefore be fixed independently of how small d is.

**Theorem 2 (loss-independent sparse-measure transfer).** For every integer
q>=2, choose the accepted same-pair cubature nu on at most

```
M_q=2 binom(2q+3,3)-1
```

original source--target pairs, preserving both marginal moments through
degree 2q. It preserves the mean, covariance, centered radius bound, and d.
For every N,L,

```
||H_mu-H_nu||_infinity <= d[2E_(N,L)+B_(N,q)(R^2)],    (7)
```

where B_(N,q) is exactly the rational beta-row error in the accepted
[loss-cubature theorem](../gaussian_prior_localization/LOSS_CUBATURE.md).
First increasing L, then N, then q makes the bracket arbitrarily small.
This extends its whole-curve transfer beyond R^2/s<=1/2, under (1).
It does not improve the older covariance-free small-radius modulus.

For every zeta>0, any adverse margin H_mu(u)<=-2d zeta has a finite same-pair
witness H_nu(u)<=-d zeta with an atom budget depending only on R,kappa,zeta.
This is relative localization of an actual adverse sign; it is not a
positive-error argument for zero defect.

## 2. Procrustes geometry and the straight interpolation

Scale by sqrt(s), so s=1. Center X and Y independently and rotate Y by
orthogonal Procrustes alignment. Let h=Y-X, M=E|h|^2, and

```
Delta=|X-X'|^2-|Y-Y'|^2 >=0,    D=E Delta=d.
```

Neither H nor the hypotheses change. The accepted centered-Gram estimate,
recalled in [R1's first-variation proof](../gaussian_contact_near_isometries/PROOF.md),
is

```
M <= E Delta^2/(2kappa) <= 2R^2 D/kappa.               (8)
```

For completeness, for the centered coordinate operators A,B into L2(mu),
double centering gives F=||AA*-BB*||_HS^2<=E Delta^2/4. Alignment makes A*B
symmetric positive semidefinite. U=A+B,V=A-B satisfy

```
F=(1/2)tr(U*U V*V)+(1/2)tr((U*V)^2) >= (kappa/2)M.
```

Use 0<=Delta<=4R^2 for (8). In particular

```
D+E|h-h'|^2=D+2M <= Lambda D.                        (9)
```

Contraction and centering give |Y|<=E|X-X'|<=2R. The straight interpolation
Z_t=X+t h, 0<=t<=1, therefore stays in B(0,S), S=2R. It is NOT assumed to
be a contracting motion. Define

```
q_t(z)=E exp(-|z-Z_t|^2/2),       f_t=C q_t,
G_t(z)=E_(pi_(t,z) x pi_(t,z)) [Delta+(1-2t)|h-h'|^2],
```

where C=(2pi)^(-3/2) and pi is the Gaussian posterior on the original label
space. The posterior-divergence identity gives the exact formula

```
H(u)=(C u/4) integral_0^1 integral_(q_t>u) G_t(z) dz dt,
                                                    0<u<1.        (10)
```

Indeed dot f_t=-div(f_t v_t), v_t=E_pi h, and
div v_t=(1/2)E_pi,pi (Z_t-Z'_t).(h-h'). The elementary pair identity

```
-2(Z_t-Z'_t).(h-h')=Delta+(1-2t)|h-h'|^2
```

then yields (10) by differentiating the hinge and using f_t=Cu on the
boundary. Positive Gaussian-mixture levels are null: the density is a
nonconstant real-analytic function decaying at infinity. At a critical
level, approximate by regular levels in the divergence theorem; the
superlevel sets are uniformly bounded and the integrands continuous.
Differentiation in t is justified by bounded h and an integrable Gaussian
derivative envelope. The derivative is continuous in t by dominated
convergence and the same null-level property. Integrating from 0 to 1 is
therefore legitimate even when a critical level is crossed.

The coefficient 1-2t changes sign. Formula (10) is used for absolute
estimates, not to infer monotonicity. Its ingredients are credited prior
work; the added argument is uniform control of the change in its domains.

On q_t>=a, kernels are at most one, so

```
|G_t(z)| <= (D+2M)/a^2.                              (11)
```

Everywhere, the lower Gaussian envelope gives the alternative bound

```
|G_t(z)| <= (D+2M) exp(4S|z|+S^2).                   (12)
```

For (12), remove exp(-|z|^2/2) from each kernel. Its posterior denominator
is at least exp(-S|z|-S^2/2), and the pair numerator without the common
factor is at most (D+2M)exp(2S|z|).

## 3. An explicit level-strip volume bound, including critical levels

The following interpolation lemma is independent of contractions and
covariance. Let

```
q(z)=E exp(-|z-Z|^2/2),     |Z|<=S=2R.
```

For a=2^-L and B,r as in (2), and a<=u<=v<=1, put delta=v-u. Then

```
|{z:u<=q(z)<=v}| <= 48B^3 (4delta/a)^(1/r).           (13)
```

The case delta=0 follows from null positive levels. For delta>0, the set
is inside [-B,B]^3 because q(z)<=exp(-(|z|-S)_+^2/2). Fix the other two
coordinates and write Q(x)=q(x,z_2,z_3). This is a positive subprobability
mixture of one-dimensional normalized Gaussian kernels with means in
[-S,S]. At the common point x=B,

```
Q(B)<=exp(-(B-S)^2/2)<=exp(-(L+1))<=a/2.              (14)
```

Let E={x in [-B,B]:u<=Q(x)<=v} have length b>0. Set
m=16B^2 and n=2m=r+1. Choose n points x_0<...<x_r of E by equal quantiles
of its Lebesgue measure. Since this measure has density at most one,

```
|x_i-x_j| >= |i-j| b/r.
```

Endpoints are chosen at the extrema of the compact set; intermediate
quantiles can be chosen in it. Interpolate Q-u at these n points by a
polynomial P of degree at most r. Lagrange's formula implies

```
|P(B)| <= delta (2B r/b)^r sum_(j=0)^r 1/[j!(r-j)!]
        <= delta (12B/b)^r,                          (15)
```

using r!>=(r/e)^r and e<3.

There is a bound on the interpolation remainder which does NOT depend on
the geometry of E. The Gaussian characteristic function gives

```
sup_x |Q^(2m)(x)| <= E G^(2m)=(2m)!/(2^m m!),
```

for a standard normal G; the subprobability mixture preserves the bound.
Thus the real-variable Lagrange remainder at B is at most

```
(2B)^(2m)/(2^m m!)=(2B^2)^m/m!
 <= (6B^2/m)^m=(3/8)^m<=2^-m<=a/4.                  (16)
```

Here m>=L+2 follows from B^2>=2(L+1). But (14) gives
|Q(B)-u|>=a/2, so (15)--(16) imply |P(B)|>=a/4. Rearranging proves
b<=12B(4delta/a)^(1/r). Integrating over [-B,B]^2 proves (13).

This argument supplies a finite explicit exponent without a regular-value
or a level-gradient assumption. It is an elementary interpolation version
of a sublevel/Remez argument, not a claim to invent that general method.

## 4. Middle and low-threshold estimates

Subtract (10) at a<=u<v<=1. Its two domains are nested. On either domain
q_t>=a, so (11), the volume bound 8B^3, and (13) give

```
|H(u)-H(v)|
 <= (C/4)(D+2M)a^-2 B^3[8delta+48(4delta/a)^(1/r)].
```

Since C<1, 0<=delta<=1, a<=1 and r>=1, this is at most

```
14 Lambda D B^3 a^-2 (4delta/a)^(1/r)
 <= 56 Lambda D B^3 a^-3 delta^(1/r).
```

This is (4), including u=v and the endpoint 1 by continuity.

For (3), write ell=-log u. The domain in (10) lies in
B(0,S+sqrt(2ell)). Equations (9),(12) imply, since C pi/3<1,

```
|H(u)|/D <= Lambda (S+sqrt(2ell))^3
                  exp(-ell+5S^2+4S sqrt(2ell)).        (17)
```

This formula is understood after multiplying by D when D=0. The elementary
square/Young bound is 4S sqrt(2ell)<=ell/4+32S^2. Also

```
(S+sqrt(2ell))^3 exp(-ell/4) <= 4(S+3)^3.             (18)
```

For (18), use (x+y)^3<=4(x^3+y^3). The maximum of
(2ell)^(3/2)exp(-ell/4) occurs at ell=6 and is
(12/e)^(3/2)<16, while S^3+16<=(S+3)^3. Consequently (17) is bounded by

```
4 Lambda (S+3)^3 exp(37S^2) sqrt(u)
 <= 4 Lambda (2R+3)^3 2^(296R^2) sqrt(u),
```

using S=2R and e<4. At u=0 both densities have equal mass, so H(0)=0.
This proves (3). For (5), if both thresholds exceed a use (4); if both
are below a use (3); otherwise insert H(a), use (3) twice and (4) once.

The bound (3) is an ABSOLUTE tail estimate. Its positive error is not a
signed low-threshold endpoint theorem.

## 5. Reconstruction and cubature at arbitrary radius

The accepted beta reconstruction satisfies P_N(u)=E H(U), where
J~Bin(N,u) and, conditionally, U~Beta(J+1,N-J+1). Direct evaluation gives

```
E(U-u)^2 <= 1/(N+2).
```

Apply (5) and Jensen to obtain (6). This uses the older reconstruction
only as a convenient explicit consumer; a sharper positive reconstruction
may replace it. No claim is made that its degree is optimal.

The same-pair cubature preserves (1), since it preserves the source mean
and covariance and retains original sites. It preserves D as the trace
of the difference of the two covariance matrices. The existing beta-row
error is

```
B_(N,q)(epsilon)=(N+1)/(4q!) (epsilon/2)^q
 max_(0<=k<=N) binom(N,k)
  sum_(j=0)^(N-k) binom(N-k,j)(k+j+2)^(q-2).
```

Here epsilon=R^2 is allowed: the cubature theorem normalizes the endpoints
around E X and T(E X), using a Euclidean 1-Lipschitz extension when
necessary. The independent target centering used for (8)--(12) does not
alter that radius argument. Its Bernstein basis is nonnegative and sums
to one, so ||P_N(mu)-P_N(nu)||<=D B_(N,q)(R^2). Applying (6) to both laws
proves (7). No mixed moments or added cubature features are needed.

Here is a wholly explicit, generally enormous budget for (7) at relative
error zeta in (0,1]. All logarithmic ceilings can be computed by exact
rational comparisons. Define

```
t=ceil(log2(16T0/zeta)),  L=2t,
p=ceil(log2(8K_L/zeta)),  nu=2r p,  N+2=2^nu,
b=ceil(log2(2/zeta)),
q=(3R^2+b+nu+1)2^nu.                                 (19)
```

Then 2T0 2^(-L/2)<=zeta/8 and K_L(N+2)^(-1/(2r))<=zeta/8,
so E_(N,L)<=zeta/4. The accepted cubature sufficient conditions

```
q>=max(2,3(N+2)R^2,b+2N+ceil(log2(N+1)))
```

hold, and B_(N,q)<=2^-b<=zeta/2. Thus (7) is at most D zeta. The program
records nu and the prefactor of 2^nu in q symbolically; it never allocates
a beta row, enormous integer 2^nu, or the cubature support.

In particular, if

```
A=1+R^2+log2(1+4R^2/kappa)+log2(1/zeta),
```

then L=O(A), B^2=O(A), r=O(A), p=O(A), and nu=O(A^2), with universal
constants. Consequently both coordinate degree 2q and atom cap M_q are
at most `2^(O(A^2))`. At fixed R,kappa this is a quasipolynomial bound in
inverse relative accuracy. It remains independent of D. This growth claim
follows from the displayed schedule; it is not a runtime claim for finding
the cubature or certifying the remaining sign.

This is an effective bound conditional on R,kappa, not an effective
description of an arbitrary diffuse input. Covariance collapse makes the
budget deteriorate. An exactly lower-dimensional source is already a
known positive case through the R5-motion mechanism; this observation does
not provide a uniform extension through the joint small-covariance,
small-loss corner. Independent rational rounding can change D and the
covariance floor and is not covered by (7).

## 6. Exact sign relevance and the remaining endpoint obligation

Suppose original-law arguments sign [0,a0] and [b0,1], with
0<a0<b0<1. Choose L with 2^-L<=a0. Suppose validated sample enclosures on
a mesh of [a0,b0] give H(u_i)>=D eta, eta>0. If its spacing is at most

```
2^(-r J),   J=ceil(log2(2K_L/eta)),                    (20)
```

then (4) gives H>=D eta/2 throughout that interval. Every gap has a sample
endpoint at distance at most the mesh spacing. This is a parameter-uniform
middle certificate for any family with common R,kappa,eta and endpoint
controls; the mesh does not refine solely because D tends to zero.
Zero loss is handled separately by (8).

Alternatively, a sparse-law certificate

```
H_nu(u)>=D[2E_(N,L)+B_(N,q)(R^2)] on [a0,b0]
```

together with ORIGINAL-law signed endpoints signs the whole original
curve by (7). A row polynomial margin D E_(N,L) similarly suffices by (6).
Endpoint signs of nu alone do not suffice. No such new positive margin
for an unrestricted family is supplied here, and no Kneser--Poulsen
consequence is claimed. The full question and the accepted unrestricted
adverse-defect cap 7/50 are unchanged.

## 7. Validation and attribution boundary

The main proof is unformalized analysis. `verify.py` checks exact rational
interpolation coefficients, Gaussian derivative moment factors, the
finite pair identity behind (10), the constant and budget inequalities,
and normalization on finite laws with vanishing/zero loss. It tests
invalid hypotheses and pins the consumed source. It performs no Gaussian
hinge quadrature, solver search, or numerical sign certification.

The posterior-divergence identity and Gram rigidity are established tools,
not new mechanisms claimed here. The beta reconstruction and same-pair
cubature are accepted team dependencies. The added information is their
explicit loss-uniform functional connection at arbitrary bounded radius
under an actual covariance floor. The thin-level interpolation estimate
is supplied in full, so no unproved analytic Remez bound is imported.
