# Scalar replica constraints do not force a growing beta wedge

Complete author argument, 27 September 2026. Independent mathematical review
is pending. This is a theorem about an abstract scalar relaxation, **not an
actual Gaussian-contraction counterexample**. The unrestricted R3 problem
remains open.

## 1. The obstruction with all its quantifiers

Fix scalar units 4s=1 in the campaign's replica normalization:

```text
a_j = integral_0^1 u^j H(u)du = B_(j+2)/(j+2)^(5/2),
eta_j = integral_0^1 u^j deta(u) = B_(j+2)/(j+2)^3.          (1)
```

Here eta must be a finite positive measure. The accepted retained-interaction
inequalities are

```text
B_(m+1)<=B_m,
B_(m+ell)/B_m >= (B_(m+1)/B_m)^p_(m,ell),
p_(m,ell)=ell(m+ell-1)(m+1)/[m(m+ell)],
                                         m>=2, ell>=1.   (2)
```

They include every multilevel Young consequence used in the accepted finite
row certificates. We do not dispute their validity for actual replicas.

**Theorem.** For every integer K>=12 and every rational 0<b<=1/2, the explicit
construction below has a continuous H on [0,1], C1 on (0,1), H(0)=H(1)=0,
|H|<=7/50, u|H'(u)|<1, and a finite positive eta satisfying (1). It also
has H(u)=0 for u>=exp(-b). Moreover:

1. B extends to a strictly decreasing, strictly log-convex function on
   [2,infinity), B(m)=O(exp(-bm)/m), and (m-1)B(m)<1.
   In particular all of (2) hold, with vanishing replica values.
2. For every integer j>=0 and every 0<=q<=K,

```text
sum_(ell=0)^q (-1)^ell binom(q,ell) a_(j+ell)
    >= (3 rho/4)exp[-b(j+q+2)](j+q+2)^(-q-4)>0.          (3)
```

3. Every nonnegative p in C1(0,1] with u^2 p(u) nondecreasing satisfies
   integral pH>=0, allowing +infinity. In particular this includes every
   smooth bounded-curvature PC2 test and the entropy curvature p(u)=1/u.
4. H is at most -epsilon^2/15000000 on the nonempty interval

```text
exp(-2b-3epsilon) <= u <= exp(-2b-2epsilon).                (4)
```

There is an explicit N0 such that a specified beta index in every row
N>=N0 is negative. For every c>0, b can be chosen so that these indices
eventually lie in q=N-j<=c(j+2), with j and q both tending to infinity.

Consequently no universal fixed positive-aperture wedge of unbounded beta orders follows
from (1)--(2), even together with all q<=K signs, PC2 signs, and the displayed
decay, cutoff, derivative and absolute bounds. This statement is stronger than failure of one
pointwise kernel: all these scalar conditions hold simultaneously for one
regular profile. Conversely it makes **no** impossibility claim about a
higher fixed diagonal beyond K under the actual Gaussian
hypotheses. K is finite and the constructed model depends on it.

## 2. A positive Laplace profile and its signed half derivative

Set

```text
epsilon = min{ b^4/20000,
               b^(K+5)/[2^(K+2)(K+1)^(K+5)(K+5)!] },
h=epsilon,                rho=epsilon^2/20000,
psi(v)=30v^2(1-v)^2 for 0<=v<=1, and 0 otherwise,
psi_h(w)=h^(-1) psi((w-b)/h),
A(w)=w^3/6+w^4/24+epsilon psi_h(w),             w>=0.     (5)
```

The compactly supported psi is nonnegative, has integral one, and is C1
after extension by zero. Its derivative has absolute value at most 360.
In particular A(0)=A'(0)=0. Define

```text
F(l)=(1/sqrt(pi)) integral_0^l A'(w)/sqrt(l-w) dw,
H_base(u)=rho u F(-log u),            0<u<1,
t=exp(-b),
H(u)=t H_base(u/t) for 0<u<t; H(u)=0 for t<=u<=1.         (6)
```

At both endpoints extend H_base by zero. Fractional integration of the piecewise
polynomial A' shows F is C1 for l>0, including at b and b+h: the new terms
start with powers (l-b)^(3/2) or (l-b-h)^(3/2). Its polynomial growth gives
continuity of H_base at 0; F(l)=O(l^(5/2)) near 0 gives a C1 extension of H
across its cutoff t. This extra shift ensures exponential replica decay.

Fubini and integration by parts, with A(0)=0, give for every x>0

```text
integral_0^infinity exp(-x l) F(l)dl
    =sqrt(x) integral_0^infinity exp(-x w) A(w)dw.         (7)
```

Absolute integrability follows from polynomial growth and compact support
of the perturbation. Thus no atom or boundary term is omitted. Put

```text
B_base(x)=rho x^3 integral_0^infinity exp(-x w) A(w)dw
         =rho [1/x+1/x^2+epsilon P(x)],
B(x)=exp(-bx) B_base(x),
P(x)=x^3 integral exp(-x w) psi_h(w)dw.                   (8)
```

Define A_shift(w)=A(w-b) for w>=b and zero otherwise. Define eta as the
pushforward under u=exp(-w) of the positive finite measure
rho exp(-2w)A_shift(w)dw. Substitution in (6)--(8) proves exactly (1), with
B_m=B(m). Indeed both moments acquire the factor exp[-b(j+2)] under
the shift. The construction is an ordinary function and an ordinary positive
measure. It uses no formal negative-shape distribution.

## 3. Every retained-interaction inequality survives

It suffices initially to work without the positive scale rho and the
factor exp(-bx). Let B0(x)=1/x+1/x^2.
Since epsilon<=b^4/20000<=b/20000, the bump has support in [b,2b].
Differentiating under its probability measure gives

```text
|P'|  <= exp(-bx)(3x^2+2bx^3),
|P''| <= exp(-bx)(6x+12bx^2+4b^2x^3).                    (9)
```

Use t^n exp(-t)<=n!, a direct consequence of the exponential series.
For x>=2 and b<=1/2, (9) implies

```text
x^2 |P'| <=312 b^(-4),
x^4 [B0 |P''|+2|B0'||P'|] <=7944 b^(-4),
x^4 [P |P''|+(P')^2] <=48000 b^(-8).                    (10)
```

Here are the constants explicitly. B0<=3/(2x) and |B0'|<=2/x^2, so the
second left side is bounded by exp(-bx)(21x^4+26bx^5+6b^2x^6), whose bound is
(21*4!+26*5!+6*6!)b^-4=7944b^-4. The first constant is
3*4!+2*5!=312. The third uses

```text
exp(-2bx)(15x^8+24bx^9+8b^2x^10),
15*8!/2^8+24*9!/2^9+8*10!/2^10 =95445/2 <48000.
```

Since B0'<=-x^-2, the derivative of B0+epsilon P is strictly negative.
Also

```text
B0 B0''-(B0')^2=1/x^4+4/x^5+2/x^6,
(B0+epsilon P)(B0+epsilon P)''-((B0+epsilon P)')^2
 >=x^(-4)[1-7944 epsilon b^(-4)-48000 epsilon^2 b^(-8)]>0. (11)
```

In this lower bound the nonnegative term epsilon P B0'' was discarded.
The last bracket is at least 1-7944/20000-48000/20000^2>1/2.
This proves strict log-convexity as well as monotonicity on the entire
half-line, not only at sampled integers. Multiplication by exp(-bx) preserves
strict log-convexity and strict decrease. The expression (8) gives the
claimed exponential decay, since the bump lies at positive distance b.
Also xB_base(x)<=rho[3/2+24epsilon b^-4]<2rho<1, so
(m-1)B(m)<1. This last bound is the elementary normalized replica cap
which follows for actual inputs from the Gaussian product formula.

For a convex function log B and an integer ell>=1,

```text
log B(m+ell)-log B(m) >=ell[log B(m+1)-log B(m)].
```

The bracket is negative and p_(m,ell)>=ell. Replacing ell by p on the
right weakens the lower bound and proves every inequality (2). In fact
this model obeys the stronger exponent ell. It therefore obeys every
nonnegative combination of the already valid multilevel Young constraints.
Strict log-convexity also gives B2 B4>B3^2, so the scalar consequence of
the accepted averaged rank gap is satisfied as well: its specified
coefficient (8/9)^3(1+eta), with eta<=5/2808, is less than one. This says
nothing about realizing the conditional graph law used in that proof.

## 4. An arbitrary finite number of entire beta diagonals stays positive

For m=j+2 the unperturbed moment is

```text
a_j_base/rho = m^(-7/2)+m^(-9/2)
              +epsilon sqrt(m) integral exp(-mw)psi_h(w)dw. (12)
```

Repeated fundamental-theorem integration gives for the first term

```text
sum_(ell=0)^q (-1)^ell binom(q,ell)(m+ell)^(-7/2)
  =(7/2)_q integral_[0,1]^q (m+t1+...+tq)^(-q-7/2)dt
  >=(m+q)^(-q-4).                                         (13)
```

The second term also has positive alternating differences. The perturbation
has absolute difference at most

```text
epsilon 2^q sqrt(m+q) exp(-bm)
 <=epsilon 2^K (m+K) exp(-bm),                    q<=K.    (14)
```

Because m>=2, m+K<=(K+1)m. Multiplying (14) by (m+q)^(q+4) and using
the exponential-series bound once more gives at most

```text
epsilon 2^K (K+1)^(K+5)(K+5)! b^(-K-5) <=1/4.            (15)
```

Equations (12)--(15) prove the unshifted lower bound
(3rho/4)(m+q)^(-q-4), uniformly for every real m>=2 and integer q<=K.
The shifted alternating difference is

```text
t^m integral_0^1 u^j (1-tu)^q H_base(u)du
 =t^m sum_(k=0)^q binom(q,k)(1-t)^(q-k)t^k
                  integral_0^1 u^j(1-u)^k H_base(u)du.
```

Every summand is positive. Keeping k=q gives (3). These signs cover all
integer indices and all rows N<=K. This is an infinite collection of signed
obligations, not a finite moment-matching assertion.

For the PC2 statement put W(l)=exp(-2l)p(exp(-l)). Its hypothesis is
exactly W'<=0. For p in C1[0,1], absolute Fubini followed by integration
by parts gives

```text
integral_0^1 p(u)H(u)du
 =-(rho/sqrt(pi)) integral_0^infinity A_shift(v)
                      integral_0^infinity W'(v+t)/sqrt(t) dt dv >=0. (16)
```

W and W' decay exponentially and A_shift grows polynomially, so the integrations
and boundary limits are justified. Formula (16) is a direct verification
of this test cone for the model, not a new Gaussian PC2 theorem.

For the possibly unbounded curvature in the theorem, use the cumulative
primitive instead:

```text
R(L)=integral_0^L F(v-b)1_(v>=b)dv
    =(1/sqrt(pi))integral_0^L A_shift(w)/sqrt(L-w)dw>=0.
```

Integration by parts on [0,L] gives
integral_0^L W(v)R'(v)dv=W(L)R(L)-integral_0^L W'(v)R(v)dv>=0.
The signed F is nonnegative near zero and eventually positive: its baseline
grows, whereas (17) tends to zero. Its negative part is therefore supported
in a compact interval away from both endpoints, where p is bounded.
The full integral exists, possibly +infinity, and the limit of the displayed
nonnegative partial integrals proves the claimed extension.

## 5. A negative interval with a controlled absolute size

Write F=F0+epsilon Fpsi, where

```text
sqrt(pi) F0(l)= (8/15)l^(5/2)+(16/105)l^(7/2).
```

For l>b+h, integration by parts inside the compact bump gives

```text
epsilon Fpsi(l)=-(epsilon/(2sqrt(pi)))
                    integral psi_h(w)(l-w)^(-3/2)dw.       (17)
```

On b+2epsilon<=l<=b+3epsilon we have l<=2b<=2. Therefore
sqrt(pi)F0(l)<8 (using 2^(5/2)<6 and 2^(7/2)<12), while (17) is less than
-1/[12sqrt(pi epsilon)]. Since epsilon<=1/20000 and sqrt(20000)>140,

```text
sqrt(pi) F(l)
 < (1/sqrt(epsilon))[2/35-1/12]
 < -1/[40sqrt(epsilon)].                                 (18)
```

For the shifted negative interval, the physical logarithmic coordinate is
b+l<=2b+3epsilon<2. Thus exp(-b-l)>1/9, using e<3, and sqrt(pi)<2.
Multiplying (18) by rho exp(-b-l), and using epsilon^(3/2)>=epsilon^2,
proves (4).

We also check the global bound independently of the moment signs.
The elementary inequalities l^(r+1/2)<=1+l^(r+1), for integer r>=0,
and l^n exp(-l)<=n! give sup exp(-l)|F0(l)|<8 and
sup exp(-l)|F0'(l)|<8. For b<=l<=b+2h, |psi'|<=360 in (6) gives

```text
|epsilon Fpsi(l)|<=1080/sqrt(epsilon).
```

For l>=b+2h, (17) gives the smaller bound 1/[2sqrt(epsilon)]; below b
it is zero. Hence

```text
|H| <= (8epsilon^2+1080epsilon^(3/2))/20000
     <=1088/20000=34/625 <7/50.                           (19)
```

Finally |psi''|<=780 on each polynomial piece. Differentiating (6), using
A'(0)=0 and continuity of A', bounds the perturbation derivative by
2340epsilon^(-3/2) on b<=l<=b+2h. Beyond b+2h, differentiating (17) gives
the smaller bound (3/4)epsilon^(-3/2). Consequently

```text
u|H'(u)| <= [16epsilon^2+1080epsilon^(3/2)+2340sqrt(epsilon)]/20000
          <=3436/20000<1.                                 (19a)
```

The shift multiplies both global bounds by t<=1. This includes the elementary
threshold derivative bound of genuine normalized hinge differences: each
nonnegative level-set volume multiplied by C is at most 1/u, so their
difference has absolute value at most 1/u.
Scaling the entire construction down further preserves every sign and
constraint, if a smaller absolute bound is desired. No physical input law
is inferred from this normalization.

## 6. Explicit negative beta indices and every positive-aperture wedge

Let u0=exp(-2b-5epsilon/2). Choose a rational r with
|r-u0|<=epsilon/100, using the alternating Taylor bounds for the exponential.
For an integer N put j=floor(Nr), q=N-j. Define

```text
N0=ceil(32000000000/epsilon^4),
beta_(N,j)=(N+1)binom(N,j) integral_0^1 u^j(1-u)^(N-j)H(u)du.
```

**For every N>=N0,**

```text
beta_(N,j) <= -epsilon^2/30000000.                        (20)
```

Here is a bound that avoids evaluating the huge polynomial. The distance
of u0 from either endpoint of (4) is at least epsilon/18, by integrating
exp(-l)>=1/9 across an interval of length epsilon/2. Thus |u-u0|<=d,
d=epsilon/20, lies in the negative interval. The Beta(j+1,N-j+1) law
has mean (j+1)/(N+2), within epsilon/100+2/(N+2)<=epsilon/50<d/2 of u0,
and variance at most 1/[4(N+3)]. Chebyshev gives probability at most

```text
1/[(N+3)d^2] <=epsilon^2/80000000
```

outside that interval. On the interval use (4); elsewhere use |H|<=1.
Since epsilon^2/80000000 < (epsilon^2/15000000)/4, the expectation is at
most -epsilon^2/30000000. This expectation is precisely the normalized
beta coefficient. The mean estimate uses N0>=200/epsilon, which follows
at once from epsilon<=1/20000.

Finally fix any c>0 and choose a rational
0<b<=min(1/8,c/32). With the same construction u0>=1-3b and
r>=1-4b>=1/2; also r<1. Therefore

```text
(1-r)/r <=4b/(1-4b)<=8b<=c/4.
```

For every sufficiently large N, and explicitly also N>=16/c, the rounding
bound j>=Nr-1 gives q<=c(j+2). Both j and q tend to infinity, and (20)
holds throughout. Thus the negative sequence enters every prescribed
linear wedge, although every fixed q<=K remains positive in this model.

## 7. What this stops, and what it leaves open

The result rules out deducing a universal wedge q<=c(j+2), for any fixed
c>0, from the positive common
lift, all retained-interaction inequalities, their multilevel Young duals,
any fixed number of entire beta diagonals, the stated PC2 curvature cone and the
absolute defect cap alone, even with exponential replica decay, a strict
cutoff and the elementary normalized replica and derivative bounds.
Increasing scalar-search effort within exactly
those premises cannot prove such a wedge.
This does not exclude a sublinear region or an aperture depending on extra
data such as the peak cutoff. For example the existing peak-pruning rule
is consistent with the construction: its sufficient aperture is exp(b)-1,
while our negative indices have limiting ratio about exp(2b)-1.

It does not show that the constructed B is an iid replica sequence, that
its pair weight is a squared-distance loss, or that its lift comes from a
three-dimensional Lipschitz graph. Nor does it refute any accepted beta
sign, retained inequality, Gaussian pressure theorem, hinge bound, or
geometric class. The constructive next obligation for a universal linear-wedge
argument is a new averaged inequality or realizability condition excluding
this family. A single additional fixed diagonal is not excluded by this
theorem; the negative orders tend to infinity.

The checker audits the polynomial bump, derivative constants, factorial
bounds, parameter selection, and the finite rational negative-index producer.
The universal analytic estimates, Laplace/Abel calculation and beta variance
argument above carry the theorem. No observed floating sign or finite scan
is used to infer an infinite statement. The historical novelty of this
particular scalar relaxation obstruction has not been independently assessed.
