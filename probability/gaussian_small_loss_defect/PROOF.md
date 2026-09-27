# A moving Gaussian sign window and a uniformly flat adverse defect

27 September 2026. Complete author argument; independent review pending.
The full dimension-three majorisation question remains open.

The earlier [effective mean-loss theorem](../gaussian_effective_mean_loss/PROOF.md)
signs a fixed threshold window once mean loss is sufficiently small. Here
the window grows as loss decreases. The new estimates retain the threshold
factor in both interval comparison and the Taylor remainder: posterior
ratios lose only exponentially in the superlevel radius, while the
Gaussian threshold decreases exponentially in its square. This produces
a whole-curve adverse defect smaller than every power of mean loss,
uniformly at fixed radius and positive source covariance floor.

The argument uses R1's accepted rigidity and top-set derivative, R8's
accepted conditional alignment and loss modulus, and R3's previous
interval-component proof, now independently accepted at graph6432.
The new continuation remains pending review; no zero-defect claim is made.

## 1. Normalization and statements

Let gamma(z)=C exp(-|z|^2/2), C=(2 pi)^(-3/2). Independently center a
bounded source law X and its 1-Lipschitz image Y and orthogonally
Procrustes-align Y. Suppose

~~~
|X|<=R, Cov(X)>=kappa I_3, R,kappa>0,
Delta(x,x')=|x-x'|^2-|Y(x)-Y(x')|^2 >=0,
d=E Delta(X,X'), f=law(X)*gamma, g=law(Y)*gamma,
H(u)=integral (g-Cu)_+ - integral (f-Cu)_+,
Def=sup_{0<=u<=1} max(-H(u),0).
~~~

Centering and contraction give |Y|<=2R. The hinge is invariant under
the separate translations and orthogonal alignment. At variance s,
replace R by R/sqrt(s), kappa by kappa/s and raw mean loss by d=loss/s.
The normalized H and Def are unchanged. All results concern that fixed
variance, not every variance simultaneously for a fixed input.

**Explicit normalized theorem.** Suppose R=1/2 and kappa=2^-15 are valid
bounds. For every integer m>=4,

~~~
d<=2^-(44m+208)  implies
H(u)>=0 for all u>=exp(-m^2/2),
Def<=2^20 d exp(-m^2/4).                                  (1)
~~~

Consequently, for an integer b>=0, put

~~~
m=max(4,ceil(sqrt(3(b+20)))), N=44m+208.
d<=2^-N  implies  Def<=2^-b d.                            (2)
~~~

There is no atom-count, minimum-weight, Q/d, or maximum-displacement
hypothesis. The assertions hold for arbitrary bounded probability laws.
For example:

| Relative error bits b | m | Sufficient loss bits N |
|---:|---:|---:|
| 0 | 8 | 560 |
| 32 | 13 | 780 |
| 64 | 16 | 912 |
| 128 | 22 | 1176 |
| 256 | 29 | 1484 |
| 1024 | 56 | 2672 |

The cutoff is conservative. Its O(sqrt(b)) dependence is an error
certificate, not a computational cost bound for a global sign proof.

**Every-radius theorem.** For each fixed R,kappa>0, explicit a>0 and
B_R>0 in Section 6 satisfy, whenever
0<d<=a exp(-44R S0), S0=max(5R,3R+1),

~~~
Def <= B_R exp(-(log(a/d))^2 / (4(44R)^2)).                 (3)
~~~

In particular Def/d^p tends to zero uniformly over the entire class for
every fixed p>0 as d tends to zero. This is a statement about the adverse
part of H, not about |H|, which can remain of order d.

## 2. Three estimates that retain the threshold

Write u=exp(-S^2/2), E={f>Cu}. Gaussian envelopes give

~~~
B(0,S-R) subset E subset B(0,S+R),   S>=R,                 (4)
~~~

where the inner open ball is intended. The posterior density relative
to the source law is

~~~
r_z(x)=exp(z.x-|x|^2/2) / E exp(z.X-|X|^2/2).
~~~

Canceling the common Gaussian factor, rather than bounding numerator
and denominator separately, gives for |z|<=S+R

~~~
W_S<=r_z(x)<=1/W_S,  W_S=exp(-2RS-(5/2)R^2).              (5)
~~~

Indeed the exponent ranges between -R|z|-R^2/2 and R|z|.
At every endpoint z of every interval component of E, |z|<=S+R and

~~~
gamma(z-x)>=C exp(-(S+2R)^2/2)>=Cu W_S   (|x|<=R).         (6)
~~~

The distinction between the posterior floor W_S and the kernel floor
Cu W_S is essential.

The third estimate uses the complement of the top set. Define
k_E(x)=integral_E gamma(z-x) dz. For S>=S0, |x|<=2R, and a unit e,

~~~
|partial_ee k_E(x)| <= Cu |E| A_S,
A_S=64 exp(3RS).                                         (7)
~~~

To prove this, the full-space integral of the Gaussian Hessian is zero,
so integrate over E complement instead. By (4), |z-x|>=q=S-3R>=1 there,
and |partial_ee gamma(v)|<=(|v|^2+1)gamma(v). Integration by parts and
the elementary Gaussian tail bound give

~~~
integral_q^infinity (r^4+r^2) exp(-r^2/2) dr
 <=(q^3+4q+4/q) exp(-q^2/2)
 <=9 S^3 u exp(3RS).
~~~

Thus the Hessian is at most 36 pi C S^3 u exp(3RS). Meanwhile
|E|>=(4pi/3)(4S/5)^3, since S>=5R. The ratio of these geometric
constants is 3375/64<64, proving (7). Differentiation occurs in the
kernel with E fixed; no regularity of its boundary is required.

## 3. Uniform annular-window lemma

Fix any real m>=S0 and choose bounds

~~~
0<W<=exp(-2Rm-(5/2)R^2), A>=64 exp(3Rm),
K0>=2R^2/kappa, L>=96R^3/kappa+6R,
K1>=16AR/kappa, K2>=2R/W^2,
c=W^2/16, delta=c/(4K1).
~~~

Define

~~~
d_tail = min {
 kappa^2/(4R^2 K0),
 delta^2/(2K0),
 kappa delta^2/(8R^2 K0),
 W^4 kappa^2 delta^2/(144R^4 K0),
 2kappa delta/R,
 c delta^4/(8 A L^2 K0^2),
 c^2 delta^4/(64 K2^2 K0^3)
}.                                                       (8)
~~~

**Lemma.** If 0<d<=d_tail, then for every S in [S0,m], with
u=exp(-S^2/2) and the actual source top set E,

~~~
integral_E(g-f) >= (Cu |E| c/2)d,
H(u) >= (Cu |E| c/2)d >=0.                               (9)
~~~

Here E is nonempty by (4). We give the argument to expose precisely
where the earlier fixed-threshold proof changes.

Put h=Y-X and M=E|h|^2. Accepted Procrustes rigidity gives M<=K0 d.
Split into G={|h|<=delta}, J=G complement, alpha=mu(J)<=K0d/delta^2.
The first three entries of (8) ensure the conditions of R8's
conditional-alignment estimate:

~~~
R sqrt(M)<=kappa/2, alpha<=min(1/2,kappa/(8R^2)),
M_G=integral_G |h|^2 dmu
 <=(32R/kappa)delta d+2 L^2 alpha^2.                      (10)
~~~

For a rare label x with y=Y(x), l=|y-x|>delta, e=(y-x)/l,
midpoint z0=(x+y)/2, set

~~~
zeta(Z)=(Z-z0).e, m0=E zeta=q/(2l), q=|x|^2-|y|^2,
eta=E (zeta)_-.
~~~

The earlier contraction and covariance calculations give

~~~
eta<=3R sqrt(M)/l, m0>=kappa/R-2eta.
~~~

The fourth entry of (8) therefore implies
eta<=W^2 m0/2, m0>=kappa/(2R), and q>=kappa delta/R.
On any line parallel to e, each interval component of E has equal
endpoint densities. The score identity and (5) imply that its midpoint,
in the zeta coordinate, is at least W m0/2. The Gaussian interval
comparison in the earlier proof now uses endpoint floor Cu W from (6),
rather than Cw. It gives

~~~
[k_E(y)-k_E(x)]/|E| >= Cu W^2 q/4.
~~~

For clarity, if the component has center b>=Wm0/2 and length 2r,
its kernel-integral difference is bounded below by
2r(Cu W) b l. Summing components gives the displayed inequality.
A positive Gaussian-mixture level has finitely many roots on each
bounded line interval: it is real analytic and not identically
constant. Thus disconnected slices are covered as well.

The exact one-label mean loss is q_x=E_Z Delta(x,Z)=q+d/2.
The fifth entry of (8) gives q>=q_x/2, and hence the rare contribution,
after division by Cu |E|, is at least

~~~
(W^2/8)(d_JG+d_JJ),                                     (11)
~~~

where pair losses are unnormalized.

For the core, use the accepted actual-top-set identity

~~~
grad k_E(x)=-Cu integral_E integral (x-z) r_v(x)r_v(z) dmu(z) dv.
~~~

Symmetrization over G x G and contraction give the favorable
coefficient W^2 d_GG/4 after division by Cu |E|.
The G x J term has absolute value at most
K2 alpha sqrt(M), using (5). All Taylor segments lie in B(0,2R),
so (7) bounds the remainder by A M_G/2. By (10), the core contribution
is therefore at least

~~~
(W^2/4)d_GG-K1 delta d-A L^2 alpha^2-K2 alpha sqrt(M).      (12)
~~~

The derivative identity at critical levels is justified by the
regular-value approximation in the accepted source: Gaussian-mixture
positive levels have zero Lebesgue measure and nearby top sets share
a compact containing ball. The interval comparison and (7) themselves
do not require this approximation.

Since d=d_GG+2d_GJ+d_JJ and d_GJ=d_JG, (11)--(12) have favorable
coefficient at least c d. Now K1 delta=c/4, and the final two entries
of (8) bound the two remaining errors by c d/8 each. This proves (9).
Testing the target hinge on E proves its stated inequality.

## 4. Exact dyadic specialization and joining the windows

Take R=1/2, kappa=2^-15, S0=5/2. For integer m>=3 use

~~~
W=2^-(2m+2), A=2^(3m+6), K0=2^14, L=2^19,
K1=2^(3m+24), K2=2^(4m+4),
c=2^-(4m+8), delta=2^-(7m+34).                            (13)
~~~

The elementary bounds e<4 and 5/8<1 give the required W and A
inequalities. Also 96R^3/kappa+6R=393219<2^19.
The seven entries of (8) are bounded below by dyadic numbers with
negative exponents, in order,

~~~
44, 14m+83, 14m+98, 22m+124, 7m+47, 35m+219, 44m+208.     (14)
~~~

The last is largest for every m>=3. The sixth and seventh use equality
with the enlarged L; the fourth uses 9<16. All these algebraic
inequalities are checked in the exact certificate.

For m>=4, 44m+208>=384>360. The previous effective theorem therefore
signs all u>=1/64. The new annular-window lemma signs

~~~
exp(-m^2/2)<=u<=exp(-25/8).
~~~

These intervals overlap: log 2>2/3 implies log64>4>25/8, hence
1/64<exp(-25/8). This proves the moving sign window in (1), with no
unsigned middle gap. For d=0, rigidity gives H identically zero.
For u>1 both hinges vanish.

## 5. Joining R8's loss modulus

At R<=1/2, the accepted loss modulus states
|H(u)-H(v)|<=K_epsilon d sqrt(|u-v|), epsilon=R^2<=1/4.
As H(0)=0, it suffices to bound K_epsilon. In its notation set
k_noise=1-epsilon and c_epsilon=4sqrt(2epsilon/k_noise).
Then

~~~
k_noise^-3<3, c_epsilon<=10/3,
5epsilon+c_epsilon^2/2<=245/36<7,
(4+sqrt(2pi))/(16sqrt(pi))<1/4,
(c_epsilon+2)^2<=256/9,
4+c_epsilon(c_epsilon+2)<=196/9.
~~~

The square-root bounds follow from 3<pi<22/7, sqrt(pi)>5/3 and
sqrt(2pi)<8/3. With e<3 these give

~~~
K_epsilon < (1/4)*3*3^7*(256/9)*(196/9)=1016064<2^20.
~~~

By Section 4, any adverse value occurs below exp(-m^2/2). The modulus
therefore proves the second part of (1). Finally log2<3/4 and
m^2>=3(b+20) imply 2^20 exp(-m^2/4)<=2^-b, proving (2).

This uses the accepted modulus for the actual hinge curve, not a
polynomial surrogate. The new exponential tail sign and the accepted
modulus together control every threshold. They do not sign every
threshold.

## 6. Fixed arbitrary radius: defect smaller than every power

The annular-window estimate has a linear, not quadratic, loss exponent
in m. To display all constants, set

~~~
K0=2R^2/kappa, L=96R^3/kappa+6R, J=2^16 R/kappa,
W=exp(-2Rm-(5/2)R^2), A=64 exp(3Rm),
K1=16AR/kappa, K2=2R/W^2, c=W^2/16,
delta=J^-1 exp(-7Rm-5R^2).
~~~

The seven terms in (8) are exactly A_i exp(-a_i Rm-b_i R^2):

| i | A_i | a_i | b_i |
|---:|---|---:|---:|
| 1 | kappa^2/(4R^2 K0) | 0 | 0 |
| 2 | 1/(2K0 J^2) | 14 | 10 |
| 3 | kappa/(8R^2 K0 J^2) | 14 | 10 |
| 4 | kappa^2/(144R^4 K0 J^2) | 22 | 20 |
| 5 | 2kappa/(R J) | 7 | 5 |
| 6 | 1/(8192 L^2 K0^2 J^4) | 35 | 25 |
| 7 | 1/(65536 R^2 K0^3 J^4) | 44 | 40 |

Put A0=min_i A_i. Then d_tail>=A0 exp(-44Rm-40R^2).
Let D0 be the earlier effective cutoff, formula (1) of the
[fixed-window proof](../gaussian_effective_mean_loss/PROOF.md), evaluated at

~~~
t0=exp(-S0^2/2), B=R+S0, w=exp(-(S0+2R)^2/2).
~~~

This is an explicit positive number. Set

~~~
a=min(1,D0,A0 exp(-40R^2))>0.                             (15)
~~~

For every m>=S0, d<=a exp(-44Rm) signs all
u>=exp(-m^2/2): the old and new windows meet exactly at t0.

A generic all-radius tail estimate suffices for the remaining thresholds.
Since the centered target is in B(0,2R),

~~~
g(z)<=C exp(-(|z|-2R)_+^2/2),
min(g,Cu)<=sqrt(Cu)*sqrt(g).
~~~

Direct radial integration gives

~~~
integral min(g,Cu)
 <=4pi C sqrt(u) [8R^3/3+8R+(2+4R^2)sqrt(pi)]
 <=B_R sqrt(u), B_R=4+8R+8R^2+(8/3)R^3.                 (16)
~~~

Here 4pi C=sqrt(2/pi)<1 and sqrt(pi)<2.
The radial integral uses integral_0^infinity exp(-v^2/4)=sqrt(pi),
integral v exp(-v^2/4)=2, and integral v^2 exp(-v^2/4)=2sqrt(pi).
Equal mass gives H=integral min(f,Cu)-integral min(g,Cu), so
-H<=integral min(g,Cu).

For 0<d<=a exp(-44R S0), choose m=log(a/d)/(44R).
Combining (16) with the signed window proves (3).
Writing Ld=log(a/d), the logarithm of its ratio to d^p is bounded by
a constant plus p Ld-Ld^2/[4(44R)^2], which tends to negative infinity.
This also proves the stated uniformity. If R^2<=1/2, the accepted
loss modulus replaces the prefactor B_R by K_(R^2) d.

## 7. Certification and limits

The executable normalized guard depends only on the source radius,
source covariance and marginal second moments:
d=2(tr Cov(X)-tr Cov(Y)). It thus applies unchanged to any finite law
obtained by degree-two paired cubature, at most 19 original pairs.
This preservation does not identify the original law's hinge with the
cubature hinge; the written theorem applies to each law directly.
All bounded laws satisfying a common radius/covariance/loss bound
receive the same sign window and defect bound.

The checker uses exact rationals and integer exponent schedules.
It checks the seven error budgets, their general exponential coefficients,
tail integration identities, variance scaling, and guard rejection.
It neither evaluates Gaussian integrals numerically nor formalizes
the analytic proof. Author checks are not independent acceptance.

Equation (3) permits a nonzero defect smaller than every power of d.
It does not prove that defect is zero, extend uniformly to covariance
collapse, cover a fixed positive-loss complement, or settle the
unrestricted dimension-three question. The accepted global bound
7/50 is not replaced by these class-dependent estimates.
