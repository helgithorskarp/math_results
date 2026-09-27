# A universal unbounded region of Gaussian beta signs

27 September 2026. Complete author argument; independent mathematical
review and formalization are pending. The unrestricted three-dimensional
Gaussian-majorisation problem remains open.

## 1. Statement

Let mu be a bounded-support probability law on R3, let T be 1-Lipschitz
on its support, and let s>0. Use the established normalization

```
C=(2 pi s)^(-3/2), f=mu*gamma_s, g=T#mu*gamma_s,
H(u)=integral(g-Cu)_+ - integral(f-Cu)_+,
a_j=integral_0^1 u^j H(u)du,
b_(N,j)=(N+1) binom(N,j) integral_0^1 u^j(1-u)^(N-j) H(u)du.
```

**Theorem.** For all integers k>=1 and j>=0,

```
j+2 >= 30720 k^3  ==>  b_(j+k,j)>=0.                    (1)
```

Every inequality in (1) is strict unless T preserves every distance on
supp(mu). There is no atom-count, positive-weight, radius, covariance,
variance, or loss-size restriction. The constant is deliberately loose.

This is one all-order theorem: the signed width grows without bound like
the cube root of the base count. It is not an isolated row increment or
a theorem requiring large Gaussian variance. For example, k=8 is covered
at every j>=15728638, and every higher k has its explicit infinite range.
The existing seven-factor theorem still covers all bases when k<=7, and
the accepted finite-row theorem still covers every N<=12.

Neither all bases of the eighth diagonal nor all beta coefficients are
proved here. The covered beta laws concentrate near u=1; they do not test
every fixed interior threshold with vanishing width. Therefore (1) gives
neither full majorisation nor a new Kneser--Poulsen volume consequence.

The new input is an averaged Gaussian-mixture inequality, proved in
Sections 2--5. It uses the location-mixture structure of the positive
replica lift, beyond its scalar moment inequalities. It does not require
positivity for each fixed configuration of the remaining replicas.

## 2. The all-order polynomials and their Gaussian calibration

For k>=0 define

```
h_k(v)=sum_(ell=0)^k binom(k,ell)(-1)^ell
                       (1/2)_[ell] v^(k-ell),
sum_k h_k(v) z^k/k! = exp(vz) sqrt(1-z),
```

where the bracket is a falling factorial. For k>=1 all coefficients
except the leading coefficient 1 are strictly negative. Write

```
P_k(v)=2v^k-h_k(v).
```

Thus P_k is the polynomial of absolute coefficients of h_k. In particular
P_k and P'_k are nonnegative and nondecreasing on [0,infinity), with

```
|h_k|<=P_k, |h'_k|<=P'_k, h'_k=k h_(k-1), P'_k=k P_(k-1). (2)
```

For ell>=1,

```
|(1/2)_[ell]| <= (ell-1)!/2,
binom(k,ell)|(1/2)_[ell]| <= k^ell/(2ell).
```

Consequently

```
h_k(v) >= v^k/2 >0             if v>=2k,
P_k(v) <= (v+k)^k              if v>=0.                 (3)
```

For the first assertion, divide the negative terms by v^k and bound their
sum by (1/2)sum_(ell=1)^k 2^(-ell)<1/2. The second follows coefficientwise
from |(1/2)_[ell]|<=k^ell. Descartes' rule, or monotonicity after dividing
by v^k, also shows that h_k has exactly one positive zero.

Let V have Gamma(3,1) density v^2 exp(-v)/2. For c>=0 put

```
G_k(c)=E h_k(c+V),  R_k(c)=E(c+V)^k.
```

The generating function gives, as identities of finite polynomials in c,

```
G_k(c)=sum_(ell=0)^k binom(k,ell)c^(k-ell)(5/2)_ell,
R_k(c)=sum_(ell=0)^k binom(k,ell)c^(k-ell)(3)_ell.       (4)
```

Equivalently G_k(c) is the kth moment of c+Gamma(5/2,1). No infinite
series interchange away from a neighborhood of zero is used. In particular
G_k(c)>0. The elementary rising-factorial comparison

```
(3)_ell/(5/2)_ell <= ell+1
```

follows by comparing each ratio (i+3)/(i+5/2) to (i+2)/(i+1).
It gives R_k(c)<=(k+1)G_k(c). Also G_k(c)>=k G_(k-1)(c): for a=5/2,
the coefficient of c^r in G_k-kG_(k-1), for 0<=r<k, is

```
(a-1) binom(k,r)(a)_(k-r-1)>=0,
```

and the leading coefficient is 1. These comparisons imply

```
E P_k(c+V)  <= (2k+1)G_k(c),
E P'_k(c+V) <= (2k-1)G_k(c).                           (5)
```

## 3. A one-crossing radial minorant

Fix k>=1, r>=30720k^3, and 0<=c<=2k. Set

```
V0=32k, epsilon=24k/r, tau=epsilon V0=768k^2/r,
F(w)=h_k(w)-tau[3P'_k(w)+2P_k(w)].                     (6)
```

Here tau<=1/(40k). The leading coefficient of F is 1-2tau>0;
every lower coefficient is negative. Therefore F has exactly one positive
zero, and its sign is negative before that zero and positive after it.
The function v->F(c+v) either has this one sign change on v>=0 or is
nonnegative throughout that half-line.

By (5),

```
E F(c+V) >= [1-tau(10k-1)]G_k(c) >= (3/4)G_k(c).       (7)
```

We need a truncated version. On v>=32k, c<=2k and (3) give

```
h_k(c+v) <= P_k(c+v) <= (v+3k)^k <= 2^k v^k.
```

Since F<=h_k,

```
integral_(32k)^infinity F(c+v) v^2 exp(-v)/2 dv
 <= 2^(2k+2) exp(-16k) (k+2)! < G_k(c)/4.              (8)
```

For the displayed bound, extract exp(-16k) from half of exp(-v), and
integrate v^(k+2)exp(-v/2) on the whole positive half-line. For its final
comparison use G_k(c)>=(5/2)_k>=k!, e>2, k+1<=2^k and k+2<=2^(k+1):
the ratio to G_k(c) is at most 2^(3-12k)<=1/512<1/4.
Combining (7)--(8) proves

```
E[ F(c+V) 1_(V<=32k) ] >= G_k(c)/2 >0.                (9)
```

This remains positive under every linear Gaussian tilt. If a is any vector
in R6 and theta is uniform on S5, define

```
W_a(v)=E_theta exp(sqrt(2v) a.theta).
```

Its even-power series has nonnegative coefficients; hence W_a is
nondecreasing in v and W_a>=1. If F(c+v) changes sign at v_*, multiply
the negative part by W_a(v)<=W_a(v_*) and the positive part by
W_a(v)>=W_a(v_*). Equation (9) then gives

```
E[W_a(V) F(c+V) 1_(V<=32k)] >= G_k(c)/2.               (10)
```

If there is no negative part, the same follows from W_a>=1. If F were
nonpositive on the entire integration interval, (9) would be impossible.
All angular series and integrals here are on a compact radial interval.

## 4. Localize an arbitrary Gaussian location mixture

Let nu be any bounded probability law on R6, and let

```
Q(z)=integral exp(-|z-Z|^2/(2s)) dnu(Z).
```

It is positive, at most one, tends to zero at infinity, and attains its
maximum at some z0. For k,r as above there are two cases. If
max Q<=exp(-2k/r), then h_k(-r log Q)>0 everywhere by (3).
Otherwise set

```
Q(z0)=exp(-sigma),  c=r sigma in [0,2k),
Y=(Z-z0)/sqrt(s),
dpi(Y)=exp(-|Y|^2/2)dnu(Z)/Q(z0).
```

The vanishing gradient at the maximum gives E_pi Y=0. At
z=z0+sqrt(s/r)x, put v=|x|^2/2 and

```
L(x)=E_pi exp(x.Y/sqrt(r)).
Q(z)=exp(-sigma) exp(-v/r) L(x).                        (11)
```

Jensen gives L>=1. A uniform upper bound on the ball v<=32k is the
essential estimate. For a>=0 and y>=0,

```
y^2 exp(-y^2/2+a y) <= 2 exp(a^2)(1-exp(-y^2/2)).       (12)
```

Indeed ay<=y^2/4+a^2 and y^2<=4sinh(y^2/4). Taylor's formula gives
exp(t)-1-t <= (t^2/2)exp(|t|). With a=|x|/sqrt(r), mean zero and (12),

```
0<=L(x)-1 <= a^2 exp(a^2)(exp(sigma)-1).                (13)
```

Our bound on r implies a^2<=64k/r<=1 and sigma<=2k/r<=1.
Using e<3 and exp(sigma)-1<=2sigma gives

```
0 <= d(x):=r log L(x) <= 24k v/r = epsilon v.           (14)
```

We also need to know that the possible negative integrand lies inside
this ball. For any two observation points z,z0, every center Z is at
distance at least |z-z0|/2 from one of them. Thus

```
Q(z)+Q(z0) <= 1+exp(-|z-z0|^2/(8s)).                   (15)
```

If h_k(-r log Q(z))<0, (3) forces Q(z)>exp(-2k/r), and
Q(z0)>=Q(z). Equation (15) and exp(-x)>=1-x imply

```
exp(-|z-z0|^2/(8s)) > 1-4k/r,
v=r|z-z0|^2/(2s) < -4r log(1-4k/r) <= 32k.            (16)
```

For the last inequality use r>=8k and -log(1-t)<=2t for 0<=t<=1/2.
Consequently the integrand's sign is nonnegative outside v<=32k.
No global log-concavity or covariance lower bound for Q is assumed.

## 5. The averaged Gaussian inequality

**Lemma.** For every Q as in Section 4, every A,B in R6, k>=1 and
r>=30720k^3,

```
integral_R6 exp[-(|z-A|^2+|z-B|^2)/(2s)]
                 Q(z)^(r-2) h_k(-r log Q(z)) dz >0.    (17)
```

In particular, nonnegative finite averages over A,B preserve the sign.
This average over the Gaussian field is the new positivity mechanism.
The scalar h_k and the fixed-configuration replica kernels are allowed
to have negative values.

**Proof.** The low-maximum case is already pointwise positive. In the
other case use (11)--(16). Put w=c+v, d=d(x), and
Lambda=L(x)^(r-2). Since r>=2 and 0<=d<=epsilon v<=tau<=1,

```
1<=Lambda<=exp(d)<3,
Lambda-1<=2d,
w-d=-r log Q(z)>=0.
```

Using (2) and the monotonicity of P_k,P'_k on the positive half-line,

```
Lambda h_k(w-d)
 >= h_k(w)-3d P'_k(w)-2d P_k(w)
 >= F(w)                                      (v<=32k). (18)
```

This estimate keeps the perturbation of both the polynomial argument
and the power weight. Dropping either would not justify the sign.

Let A0=(A-z0)/sqrt(s), B0=(B-z0)/sqrt(s), and
a=(A0+B0)/sqrt(r). The exact product identity is

```
exp[-(|z-A|^2+|z-B|^2)/(2s)] Q(z)^(r-2)
 = exp[-(|A0|^2+|B0|^2)/2] Q(z0)^(r-2)
                         exp(-v) exp(a.x) Lambda.       (19)
```

The first two factors are strictly positive constants. Outside the
ball v<=32k the original integrand is nonnegative by (16). On that ball,
(18), polar coordinates in R6 and (10) give

```
integral_(v<=32k) exp(-v) exp(a.x) F(c+v) dx
 >= (2pi)^3 G_k(c)/2 >0.                               (20)
```

Multiplication by the positive constants in (19) and the Jacobian
(s/r)^3 proves (17). The location of A,B is unrestricted; in particular
one may not assume the pair's midpoint stays near the mode. The
nondecreasing spherical tilt in (10) handles every such displacement.
QED.

All integrals are absolutely convergent. Bounded mixing centers give
Gaussian upper and lower envelopes for Q, so |log Q(z)| grows at most
quadratically, while the pair kernel supplies Gaussian decay. The same
bounds justify positive finite marked averages and compact real-r ranges.

## 6. Real-order replica lift and return to beta signs

For the actual contraction use the credited six-dimensional interpolation

```
Z_x(t)=(sqrt(1-t)x,sqrt(t)T(x)),
delta(x,y)=|x-y|^2-|T(x)-T(y)|^2>=0,
q_t(z)=E exp(-|z-Z_X(t)|^2/(2s)),
M_t(z)=E delta(X,Y) exp[-(|z-Z_X(t)|^2+|z-Z_Y(t)|^2)/(2s)],
C6=(2pi s)^(-3).
```

For completeness we establish the required lift at real orders, rather
than assigning a fractional number of replicas. For 0<t<1 let

```
A_t=diag(-I3/[2(1-t)], I3/[2t]).
```

At each z the posterior law proportional to the Gaussian kernel has
covariance Sigma. Direct differentiation and pair expansion give

```
M_t/q_t^2=-4 tr(A_t Sigma),
Hess log q_t=-I6/s+Sigma/s^2,
partial_t q_t=-div(A_t z q_t)-s tr(A_t Hess q_t).        (21)
```

For any real r>1, spatial integration by parts therefore yields

```
partial_t integral q_t^r
 =(r-1)[-tr(A_t) integral q_t^r
         +sr integral q_t^(r-2) grad q_t^T A_t grad q_t]
 =(r-1)/(4s) integral q_t^(r-2) M_t.                    (22)
```

The three unused Gaussian coordinates at each endpoint give

```
C6 integral(q_1^r-q_0^r)
 = r^(-3/2) C^(1-r) integral(g^r-f^r).
```

Integrate (22) in t and use the ordinary hinge Mellin identity. For

```
a(r)=integral_0^1 u^(r-2)H(u)du
```

one obtains

```
a(r)=sqrt(r)/(4s) C6 integral_0^1 integral_R6
                                      q_t^(r-2) M_t dzdt.       (23)
```

The integer instance is the established common positive lift. Equation
(22) supplies the real instance directly; real-power comparison itself
is already known from Aishwarya--Li. Bounded centers justify spatial
integration by parts uniformly on compact real-r intervals. To handle
t=0,1, first work on [eta,1-eta] and then let eta decrease to zero.
Original center velocities grow only as t^(-1/2)+(1-t)^(-1/2), an
integrable bound. Also M_t<=delta_max q_t^2 uniformly. Thus no endpoint
term or singular trace term is discarded.

Differentiating (23) k times is legitimate for r>=2: every required
logarithmic moment has a Gaussian majorant. The defining polynomial gives

```
(-1)^k a^(k)(r)
 = r^(1/2-k)/(4s) C6 integral_0^1 integral_R6
                  q_t^(r-2) M_t h_k(-r log q_t) dzdt.   (24)
```

Apply (17) at every t and then average the nonnegative prescribed pair
loss. It follows that

```
(-1)^k a^(k)(r)>=0 for EVERY real r>=30720k^3.          (25)
```

The sign is strict if E delta>0. If a support pair is strictly shortened,
continuity gives two relative neighborhoods of positive mu mass with
positive loss, so E delta>0. If E delta=0, continuity forces preservation
of every support distance; the endpoint laws are congruent and H=0.

Finally, repeated fundamental-theorem integration gives

```
sum_(ell=0)^k (-1)^ell binom(k,ell) a(j+2+ell)
 = integral_[0,1]^k (-1)^k a^(k)(j+2+x_1+...+x_k) dx.  (26)
```

If j+2>=30720k^3, every real argument in (26) satisfies (25).
Multiplying by (j+k+1)binom(j+k,j) proves (1) and its strictness.

## 7. Scope and evidence

The theorem uses a genuine Gaussian-mixture realizability constraint.
The scalar-relaxation countermodels, even with all retained interactions,
do not supply the mode estimate (13) or the noncentral radial argument.
They exclude universal fixed-aperture linear regions from those scalar
premises; the present cube-root region neither contradicts them nor
realizes those countermodels by Gaussian data.

This is a written analytic proof for all integer orders and unbounded
real base counts. The accompanying exact checker audits Appell and Gamma
identities, coefficient signs and constant guards, as well as the
Gaussian-product normalization. Finite checks are supporting controls,
not the proof of universal quantifiers. No numerical search, quadrature,
solver output, large certificate, or private data is a proof premise.
Publication and internal exact checks are not independent acceptance.
