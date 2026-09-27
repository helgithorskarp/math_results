# A uniform eventual Gaussian exclusion for signed radial product laws

Complete author proof; independent correctness review and formalization are
pending. The full dimension-three Gaussian-majorisation question remains open.
This theorem excludes all adverse hinges at sufficiently large variance for
a whole signed-radial class, including diffuse laws and maps preserving some
distances. It makes no assertion at smaller variances and yields no new
Kneser--Poulsen consequence.

## 1. The whole family and its uniform cutoff

Let R>0, let A take values in [0,R], and let U be an independent random unit
vector in R3. The law of U is arbitrary. Let h:R->R be odd and 1-Lipschitz,
and put X=A U and Y=h(A)U. Choose an integer m>=1 and a real 0<epsilon<=1.
Assume

```text
|h(R)| <= (1-epsilon)R,
P(A <= epsilon R/8) >= 2^-m,
P(A >= (1-epsilon/8)R) >= 2^-m.                         (1)
```

These are aggregate radial mass conditions, not atom-mass or angular
regularity conditions. Both endpoint laws may be diffuse. Define

```text
N = ceil(32(m+1)/epsilon),
E = 2m+4N,
eta = (epsilon/48) 2^-E,
s_* = (2112/epsilon) 2^E R^2.                         (2)
```

**Theorem.** For every Gaussian variance s>=s_* and every threshold t>=0,

```text
integral (law(Y)*gamma_s-t)_+ >= integral (law(X)*gamma_s-t)_+.   (3)
```

Thus the entire Gaussian majorisation curve has its favorable sign at every
such variance. The same bound works for all A,U,h satisfying (1). Neither
finite support, a covariance floor, a positive angular density, nor a global
Lipschitz bound below one is required. The constants are deliberately coarse.

**Qualitative corollary.** If 0 and R belong to the support of the law of A,
then every odd scalar contraction h gives eventual full Gaussian
majorisation for X=A U. If |h(R)|=R, h is either the identity or its negative
on [0,R], so all Gaussian hinges are equal at every variance. Otherwise take
epsilon=1-|h(R)|/R>0. Both radial intervals in (1) have positive mass, hence
some finite m satisfies (1), and the theorem applies.

For example, take A uniform on [0,4], any independent angular law U, and
h(r)=r on [0,1], h(r)=2-r on [1,infinity), extended oddly. One can use
epsilon=1/2 and m=4, so N=320 and E=1288. The normalized bound is
s/R^2>=4224*2^1288. This profile fixes the whole unit ball and sends radii
above two to the opposite direction. Its Lipschitz constant is exactly one.
The example illustrates the uniform theorem; its constant is not practical
or optimal, and no separation from every other positive theorem is claimed.

## 2. The existing exchange mechanism

Write sigma for normalized area measure on S2 and define

```text
M_Z(v)=E exp(v.Z),
P_Z(v)=M_Z(v)M_Z(-v),
S_Z(lambda)=integral log M_Z(lambda theta) d sigma(theta),
J(lambda)=S_X(lambda)-S_Y(lambda).                      (4)
```

In particular 2S_Z(lambda)=integral log P_Z(lambda theta) d sigma(theta).
The [earlier signed-radial proof](../gaussian_signed_radial_tail_exclusion/PROOF.md)
establishes the following exchange identity and nonnegative sign. We recall
the argument and obtain a new uniform margin below.

For iid A,B and iid U,V, with the two pairs independent, set

```text
p=(U+V)/2, q=(U-V)/2, D=A-B, F=A+B,
D'=h(A)-h(B), F'=h(A)+h(B).
```

Separate exchanges of A,B and of U,V give

```text
P_X(v)=E cosh(D v.p) cosh(F v.q),                       (5)
```

and the same expression with D',F' gives P_Y. Oddness and the Lipschitz
condition imply |D'|<=|D| and |F'|<=|F|. Each conditional product therefore
decreases; P_X>=P_Y everywhere and J>=0.

The radial map T(ru)=h(r)u is indeed globally nonexpansive. For real a,b and
unit u,v, c=u.v, the squared-distance loss is

```text
(1+c)/2 [(a-b)^2-(h(a)-h(b))^2]
 +(1-c)/2 [(a+b)^2-(h(a)+h(b))^2] >= 0.                 (6)
```

Thus (3) concerns an actual contraction of the original law.

## 3. A positive margin on each bounded parameter interval

Put delta=epsilon/8, let L={A<=delta R}, H={A>=(1-delta)R}, and write
alpha=P(L), beta=P(H). These events are disjoint. On either ordered event
(A,B) in L x H or H x L,

```text
|A-B| >= (1-epsilon/4)R,
|h(A) +/- h(B)| <= (1-3epsilon/4)R.
```

The second bound uses |h(a)|<=a in L and
|h(b)|<=|h(R)|+R-b in H. Also A+B>=|A-B|. Consequently both coefficient
squared losses in (5) are at least

```text
[(1-epsilon/4)^2-(1-3epsilon/4)^2]R^2
 = epsilon(1-epsilon/2)R^2 >= epsilon R^2/2.            (7)
```

If |a'|<=|a| and |b'|<=|b|, the cosh power series and cosh>=1 imply

```text
cosh(a)cosh(b)-cosh(a')cosh(b')
 >= ((a^2-a'^2)+(b^2-b'^2))/2.
```

Retain only the two radial events, of total probability 2alpha beta, in
(5). Since (theta.p)^2+(theta.q)^2=((theta.U)^2+(theta.V)^2)/2, it follows
that

```text
P_X(lambda theta)-P_Y(lambda theta)
 >= alpha beta epsilon R^2 lambda^2 E(theta.U)^2/2.
```

Now P_X(lambda theta)<=exp(2lambda R), and log(P_X/P_Y)>=1-P_Y/P_X.
Integrating, using integral(theta.u)^2 d sigma=1/3, gives the uniform bound

```text
J(lambda) >= alpha beta epsilon z^2 exp(-2z)/12,
z=lambda R.                                            (8)
```

This strictly positive bound alone decays at large z. The next argument
prevents that decay from leaving an uncontrolled threshold range.

## 4. A six-vertex bound from radial clouds

Let ell=E[A|L] and r=E[A|H]. Then

```text
0<=ell<=delta R,    (1-delta)R<=r<=R,
r-ell>=(1-epsilon/4)R.                                (9)
```

For v=(v1,v2) define the scalar-coefficient MGF

```text
G_A(v)=E cosh(A v1-B v2),
G_h(v)=E cosh(h(A)v1-h(B)v2).                           (10)
```

Set

```text
K=conv{(1,0),(0,1),(1,-1),(-1,0),(0,-1),(-1,1)},
V={+/-(r,-ell), +/-(ell,-r), +/-(r,-r)},
w=min(alpha beta,beta^2)/2 >= 2^-(2m+1).
```

Conditional Jensen on L x H, H x L and H x H, followed by the two signs
in cosh, proves separately for each v0 in V that

```text
G_A(v) >= w exp(v.v0).
```

Hence G_A(v)>=w exp(max_(v0 in V) v.v0). The six source vectors contain
the scaled hexagon

```text
(r-ell)K subset conv V.                               (11)
```

For clarity, (r-ell,0) is the convex combination with coefficients
r/(r+ell), ell/(r+ell) of (r,-ell), (-ell,r). Reversing the coefficients
gives (0,r-ell). The diagonal vertex (r-ell,-(r-ell)) lies on the segment
from -(r,-r) to (r,-r). Negation gives the other three vertices.
All denominators are positive by (9). This also treats ell=0.

There is a strict coefficient bound for the whole target radial law. For
0<=a<=b<=R and d=b-a,

```text
|h(b)-h(a)| <= min(d,R-d+|h(R)|)
                 <= (R+|h(R)|)/2 <= (1-epsilon/2)R.
```

The second of the two bounds inside the minimum follows by going from a
to0 and from b toR, in the appropriate order of signs. Since h(0)=0, the
same bound applies to |h(a)|. Therefore every vector
(h(a),-h(b)) belongs to (1-epsilon/2)R K: the three defining strip bounds
are on its first coordinate, second coordinate and their sum. The negative
vector belongs to the same symmetric hexagon. Thus

```text
G_h(v) <= exp((1-epsilon/2)R max_(k in K) v.k).         (12)
```

Let kappa=1-epsilon/4. By (9),

```text
kappa(r-ell) >= kappa^2 R >= (1-epsilon/2)R,
kappa^2-(1-epsilon/2)=epsilon^2/16.
```

Combining (11)--(12) with the source Jensen bound proves

```text
G_h(v) <= w^-1 G_A(kappa v).                           (13)
```

This is a uniform exponential envelope with a finite mass penalty. It is
not a claim of a dilated martingale coupling or pointwise contraction of
every individual source coefficient.

For independent U,V, P_X(t)=E G_A(t.U,t.V), and analogously for Y. Integrate
(13) in U,V. Convexity of log P_X, with P_X(0)=1, yields

```text
P_Y(t) <= w^-1 P_X(kappa t) <= w^-1 P_X(t)^kappa,
J(lambda) >= (epsilon/4)S_X(lambda) - (1/2)log(1/w).    (14)
```

## 5. A uniform large-parameter lower bound

Let M_A denote the scalar MGF. Jensen for log, first over U, gives

```text
2S_X(lambda) >= E_U integral
 log[M_A(lambda theta.U)M_A(-lambda theta.U)] d sigma(theta).
```

The two ordered radial cloud events, and conditional Jensen, give
M_A(a)M_A(-a)>=2alpha beta cosh((r-ell)a). Use
log cosh(x)>=|x|-log2 and integral|theta.u| d sigma=1/2. Then

```text
S_X(lambda) >= lambda(r-ell)/4 + (1/2)log(alpha beta)
             >= 3z/16-m.                              (15)
```

Here r-ell>=3R/4, alpha beta>=2^-2m, and log2<1. Equations (14)--(15) imply

```text
J(lambda) >= 3epsilon z/64 - epsilon m/4 - m - 1/2.
```

At z>=N>=32(m+1)/epsilon the right side is at least
1+(1/2-epsilon/4)m>=1. This controls every larger parameter, with no
angular mesh, support-cardinality bound or individual atom mass.

For 1/2<=z<=N, (8), alpha beta>=2^-2m, and e<4 give

```text
J(lambda) >= epsilon 2^-2m exp(-2N)/48
             >= epsilon 2^-(2m+4N)/48 = eta.            (16)
```

Since eta<1, both ranges imply J(lambda)>=eta for every lambda>=1/(2R).

## 6. Passage to all actual Gaussian thresholds

The [accepted eventual endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
with its [independent review](../gaussian_majorisation_eventual_endpoint_review2/README.md),
states: for a contraction whose source and target lie in radius-R balls,
a uniform J(lambda)>=eta>0 on lambda>=1/(2R) signs all Gaussian hinges at
s>=R^2 max(8,44/eta). Here |X|,|Y|<=R and T(0)=0. The bound (16) therefore
gives (3), because 44/eta=(2112/epsilon)2^E>8.

The endpoint's Gaussian integration and threshold overlap are imported,
not reproved or independently reviewed in this contribution. Sections2--5
establish its uniform hypothesis for the new class. Positive spherical
tests alone were insufficient; the new cloud envelope supplies the missing
nondecaying margin and a common cutoff for the whole family.

## 7. Search consequence and limitations

The earlier signed-radial result excluded one spherical-tail falsifier.
Under (1), every actual Gaussian hinge is now excluded as a counterexample
at every variance above (2). Arbitrary diffuse radial mass between the two
clouds, arbitrary angular laws and sign-changing profiles are included.
For origin-supported radial laws the qualitative eventual conclusion has
no quantitative cloud assumption beyond positivity of those masses.

At publication refresh, R1's new universal spherical comparison supplied
an author proof of eventual Gaussian comparison for every finite contraction
and every uniformly strict bounded contraction. It explicitly leaves the
general diffuse case at Lipschitz constant one open. The added scope here
is the uniform diffuse signed-radial family, including preserved distances.
The finite checker example is only a control. None of the new R1 theorem
is used as a premise of this proof.

The remaining lower-variance question is unsigned. Radius--direction
dependence is also outside the proof. No assertion excludes all other
possible applications of existing positive theorems to particular laws.
No new ball-volume consequence follows from a variance restriction.
The accepted finite-atomic low-noise work is separate and is not reopened.

The source checker verifies exact polynomial identities, barycentres,
schedule arithmetic and finite controls, using only rational arithmetic.
It does not replace the universal Jensen, independence, spherical-integration
and Gaussian-endpoint arguments. This is an author proof, not formalization
or independent review; historical priority remains unestablished.
