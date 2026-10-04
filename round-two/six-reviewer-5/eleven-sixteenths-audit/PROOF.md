# Independent adjacent-annulus proof and larger first-power gap

**six-reviewer-5 / independent mathematical reviewer. Ordinary, unformalized proof.**
The independent exact implementation is [face.py](face.py) and [bridges.py](bridges.py).
The complete exposed author mathematical DATA is [COVER.json](COVER.json), pinned in
[DEPENDENCIES.json](DEPENDENCIES.json). This proof confirms the NEW adjacent theorem
of LEMMA10322 and strengthens its gap; it does not independently reverify the separate
numerical premises of the older-band or lower-disk unions.

For EVERY complex degree-nine polynomial whose nine original zeros lie in the CLOSED
unit disk, and EVERY marked original zero satisfying

\[
27/40\le |a|\le11/16,
\qquad F=\sum_{j=1}^{8}|a-\zeta_j|^{-1}>8+1/8800.
\]

All eight critical multiplicities are counted. Collisions give infinity. There is no
symmetry, conjugacy, balance, separation, simplicity, second-moment or rationality
restriction. The finite computations cover closed faces and ordinary inequalities
cover all continuum parameters. The constants are sufficient, not optimal.

## 1. Actual channels and physical normalization

Rotate so a is positive real and make p monic. A collision is immediate; otherwise
the marked root is simple and every reciprocal q_j=(a-zeta_j)^(-1) is finite/nonzero.
Set r_j=|q_j|, mu=sum(q_j)/8=u+iv, w=v², T=sum(r_j-1)²,
E=sum|q_j-1|², Pi=F-8u and S=sum|q_j-mu|². Direct expansion gives

\[
E=T+2F-16u=T+2\Pi,\quad S=E-8[(1-u)^2+w].
\]

Writing p(z)=(z-a) product(z-z_k) and integrating p'(z)=9 product(z-zeta_j)
from a to0 and a to1/a proves, with ALL factors and multiplicities,

\[
O=9\int_0^1\prod(1-atq_j)dt=\prod z_k\prod q_j,
\quad J=\int_0^1\prod[a+(1-a^2)tq_j]dt
=\prod\frac{1-az_k}{a-z_k}.
\]

For the second substitution p(1/a)=9(1-a²)J/[a⁹ product q_j]; the first gives
O=-p(0) product q_j/a, where p(0)=-a product z_k. Gauss--Lucas and
|1-az_k|²-|a-z_k|²=(1-a²)(1-|z_k|²) imply

\[
r_j\ge1/(1+a),\quad |J|\ge1,\quad |O|\le\prod r_j.
\tag{A}
\]

If finite F<=8, put lambda=F/8 in(0,1] and
p_lambda(z)=lambda⁹p(a+(z-a)/lambda). This preserves degree, leading coefficient,
marked root and every original/critical multiplicity; the derivative is
lambda⁸p'(a+(z-a)/lambda). Original and critical roots become
 a+lambda(z-a). Disk convexity preserves every original root, and reciprocal
moduli become r_j/lambda, of exact mass8. Thus exclusion of actual mass8 also
excludes ALL actual F<=8. No formal critical tuple is asserted realizable.

## 2. Paid mass-eight face

The written target's generic analytic inequalities are audited independently.
Here are the mathematical obligations represented by the fresh exact reader.
For a in[A,B], define bm=1-B², bp=1-A², aa=min(A(1-A²),B(1-B²)),
c=A+1-A²-B. These obey bm<=1-a²<=bp, aa<=a(1-a²), and
 a+(1-a²)t<=B+ct, because the difference equals
(1-t)(B-a)+t(a-A)(a+A-1)>=0. A>=27/40>1/2.

Radial Hermite interpolation of log(B0+y e) at -d (double) and7d, where
sum e<=0, sum e²=56d², gives a majorant because its third derivative is
nonnegative and (e+d)²(e-7d)<=0. Cauchy gives e<=7d. Its linear coefficient
is at least3y/[4(B0-yd)], so its eight-factor product is bounded by
(B0+7yd)(B0-yd)^7 exp[-3y(8-F)/(4(B0-yd))]. All factors remain positive
in the radius range, including the zero-variance and t=0 cases. Comparing
squared complex factors pays the extra phase loss exp[-a(1-a²)t Pi/CD²].
For phi(x)=(1+7x)(1-x)^7, phi'/phi=-56x/[(1+7x)(1-x)]<=0.
This licenses the source's radial endpoint replacement.

At F=8, m=16/27 gives T<=56(1-m)²=6776/729. On each of75 closed T-cells
[k/8,min((k+1)/8,6776/729)], if E>=23/5 then
Pi>=(23/5-T)/2. The positive truncated reciprocal series G1,G2 about t=1
are LOWER bounds for their reciprocals. Therefore decrease the exponential
argument first, THEN use exp(-K)<=1-K+K²/2 for K>=0. This avoids assuming
monotonicity of the quadratic. Every entire degree18 polar polynomial is
integrated and is strictly below2199/2200. Consequently |J|>2199/2200
forces E<23/5 and u>57/80, without an origin-gradient premise.

Centering gives max|q_j-mu|²<=7S/8. Concentrating the remaining squared radii
and evaluating t^k+(1-t)^k at7/8 yields the exact absolute even moments
25/32,43/64,1201/2048. Adjacent Cauchy bounds pay the odd moments with rational
UPPER roots. Newton's identities and subset Cauchy/Maclaurin pay all elementary
orders2..8. The REAL quartic e4 on the real zero-sum subspace has norm at most
3/32: e4=p2²/8-p4/4 and S²/8<=p4<=25S²/32. Banach's REAL Hilbert symmetric
multilinear norm identity supplies the same multilinear bound. Rotate the
complex quartic to nonnegative real value and write z=x+iy. Then
P(x)-6L(x,x,y,y)+P(y)<=3(X²+6XY+Y²)/32<=3S²/16,
where X=||x||²,Y=||y||². Thus the complex c4=3/16 is valid without orthogonality.
The external norm identity is an ordinary literature premise, not a finite check.
No higher Newton coefficient is silently recomputed after replacing c4.

Expand ALL elementary orders in
product(1-atq)=sum e_k(q-mu)(-at)^k(1-at mu)^(8-k).
For scalar boxes keep the ACTUAL mean denominator
sm=min(1,U1²+W1,(F1/8)²) separate from the smaller beta-envelope coefficient
sb=min(sm,U0²+W1). The anchor a0=min(A,2U0/sb-B)>0 licenses the whole interval;
when sb=U0²+W1 use decrease in u, and when sb=sm use the independent norm bound.
The positive decreasing beta and the concave square-root bound retain every
centered order. The diagonal reverse-triangle numerator is positive and its
norm denominator uses sm, not sb.

For retained u, both endpoint anchor inequalities imply the whole u interval
by concavity. Keep SE(u)=E1-8[(1-u)²+W0] and
SJ(u)=T1+2F1-8-8(u²+W0) as SEPARATE licensed polynomials. On21 leaves pay
BOTH channels, each with seven complete9x10 coefficient matrices and every
integral. The degree8 lower-bound polynomial and degree9 cleared positive-
denominator polynomial retain all9 and10 Bernstein controls. For joint polar
leaves retain d=sqrt(T/56), Pi>=E0/2-28d², with its whole sign license. Pay
all37 full13x19 matrices,13 integrals and13 Bernstein controls. Full Bernstein
reconstruction and both endpoint identities are checked, not only extrema.

The four ordered necessary-intersection iterations preserve containment by
E=T+2F-16u, Pi>=0, S>=0 and |mu|<=F/8. They never establish a feasibility
converse. Exact F=8 remains unchanged. The actual product bound uses
log x<=x-1-(x-1)²/(2R), valid throughout(0,R] since
Rx f'(x)=(x-1)(R-x) for the difference f. The full per-box radius cap and
variance cap provide R>=1. The reciprocal of all five LOWER exponential terms
bounds the product ABOVE. It is applied only to an actual tuple or used to bound
the formal clipped radial product, never to assume the clipped origin channel.

The exposed final tree is reconstructed recursively with both children CLOSED
at each strict rational cut. All313 nodes are uniquely reachable,156 cuts,
157 leaves, depth13. Every leaf has a nonempty necessary enclosure; every
scalar origin and product calculation is paid. Defining roles are98 scalar
origin,21 retained origin,1 standard polar and37 joint polar. All119 origin
leaves satisfy L>C+1/3100; all38 polar leaves satisfy U<2199/2200. These
strict inequalities contradict(A) for actual mass8. Physical normalization
therefore proves F>8 for every original polynomial in the stated annulus.

## 3. Full clipping path and the larger gap

Let epsilon=1/8800. Suppose F=8+Delta with0<Delta<=epsilon. For m_a=1/(1+a), set
h_j=Delta(r_j-m_a)/(F-8m_a), q'_j=(1-h_j/r_j)q_j. The denominator is positive,
0<=h_j<=r_j-m_a, sum h_j=Delta, sum|q'_j|=8 and every new radius stays above
m_a. Along the straight path q'+v(q-q'), all radii stay above m=16/27 and
mass stays at most S0=8+epsilon. This formal path needs no root-feasibility premise.

With l=27/40,h=11/16,bp=871/1600 and sigma=(S0-m)/7, a removed J-slot has bound

\[
L_J=bp\sum_{i=0}^7\binom7i h^{7-i}(bp\,\sigma)^i/(i+2)<2/3.
\]

Thus |J(q')|>=1-(2/3)epsilon>2199/2200. The ALREADY paid75-shell estimate gives
E'<23/5,u'>57/80 before the O-gradient calculation. Hence q' lies in the paid face.

Set R=S0-7m,u0=57/80-epsilon/8,E0=23/5+2(R+1)epsilon. The l1 displacement
bounds path u below by u0 and path E above by E0. In a removed O-slot,

\[
\sum_{j\ne k}|1-xq_j|^2
\le8-16xu+x^2(E+16u-8),\quad x=at.
\]

The omitted-slot term 2x Re(q_k)-x²|q_k|² is at most1. Combine the coefficient
-16x+16x²<=0 BEFORE applying u0. Since E0+16u0-8=8+2R epsilon, this gives

\[
\tfrac17\sum_{j\ne k}|1-atq_j|^2\le B(t)
=\tfrac17[8-16l u0t+h^2(8+2R\epsilon)t^2].
\]

Fresh exact gates show B(1)>0,B'(1)<0 and positive quadratic coefficient:
0<B(t)<=8/7 on[0,1]. With (107/100)²>8/7, squared AM--GM gives

\[
L_O=9h(107/100)\int_0^1t B(t)^3dt<8/7.
\]

Every seven signed cubic coefficient and weighted integral is recomputed by
sparse algebra and separate literal convolution. This tighter paid gradient
cap replaces the target's5/4. All nine coefficients of
A=(1+epsilon/(8m))^8 are compared by binomial and literal multiplication, and

\[
(A-1)+(8/7)\epsilon<1/3100,
\qquad (2/3)\epsilon<1/2200.
\]

The exact positive origin slack is in [EXPECTED.json](EXPECTED.json), together
with the entire O/J polynomials and product-ratio coefficients. Since P'<=1
and P/P'<=(1+Delta/(8m))^8, the ACTUAL channel |O(q)|<=P and the paid path
imply |O(q')|<=P'+(A-1)+(8/7)epsilon. Each origin leaf demands more than
P'+1/3100, a contradiction; each polar leaf contradicts the paid lower J bound.
Thus F>8+1/8800, including equality of the proposed threshold and both marked endpoints.
The original1/10000 payment is independently recomputed too.

## 4. Dependencies and limits

[Carando--Rodríguez, Introduction equation(2)](https://arxiv.org/pdf/1810.09373)
supplies the REAL Hilbert norm identity. The communication channels appear in
[Tang--Zhang Lemma3.1](https://arxiv.org/html/2609.19126) and
[Tao Lemma6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
The quadratic theorem there does not imply the first-power conclusion.
The proof/certificate methods and the exposed tree belong to the credited author
and antecedents; no historical priority is claimed for these methods.

If the separate10300 theorem F>8+1/350 on[2/3,27/40] is supplied, its union with
this theorem gives F>8+1/8800 on[2/3,11/16]. If10240 is additionally supplied,
strict F>8 holds on the whole lower disk |a|<=11/16. Those are CONDITIONAL union
implications here, not new independent ancestor verdicts. There is no uniform
whole-disk gap, general-degree/global first-power theorem or sharp radius claim.
