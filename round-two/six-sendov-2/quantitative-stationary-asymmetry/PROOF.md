# Explicit stationary asymmetry from original-root separation

Actual **six-sendov-2**, role **researcher**, 2026-10-03. Complete ordinary
author proof, **unformalized and independently unreviewed**. The exact
identities and rational constants have a portable accompanying checker.
Classical polynomial traces, Newton identities, interlacing, root
continuity, coefficient norms and differential estimates retain their credit.

## 1. Domain, functional and claims

Let a1<...<a8 be eight **distinct real original coordinates**, with

\[
 \sum_i a_i=0,\qquad \sum_i a_i^2=1,\qquad
 a_{i+1}-a_i\ge\delta\quad(1\le i\le7),\quad 0<\delta\le1.
\]

Put f=product(z-ai), h=f'/8, and let lambda1<...<lambda7 be the seven
simple real zeros of h. Use the **actual** compression masses and quotient
of [7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [9496](../mass-stationary-chart/PROOF.md):

\[
 m_j=-8f(\lambda_j)/h'(\lambda_j)>0,\quad
 \sum_jm_j=1,\quad \eta=\sum_jm_j^2,\quad
 D=\sum_i a_i^4-1/8,\quad C=(1-\eta)/D.                 \tag{1}
\]

Write
\[
 f(z)=z^8-z^6/2+f_5z^5+f_4z^4+f_3z^3+f_2z^2+f_1z+f_0.
\]
Stationarity
means first-order stationarity of C on the **balanced, fixed-norm
original-root sphere**, equivalently vanishing of all six coefficient
derivatives in directions of degree at most five. This equivalence is
the all-distinct open coefficient chart of9496; it is not inferred from
a simple critical spectrum alone.

**Theorem A (even-chart gradient).** For every reflection-symmetric
profile in this domain, write

\[
 f=z^8-z^6/2+a z^4+b z^2+c.
\]

Then its three full coefficient derivatives, including moving critical
nodes, satisfy

\[
 \max(|C_a|,|C_b|,|C_c|)\ge10^{-18}\delta^{88}.         \tag{2}
\]

There is no centering or stationarity premise in Theorem A.

**Theorem B (stationary asymmetry).** Every stationary profile in the
domain of (1) satisfies

\[
\sigma:=|f_5|+|f_3|+|f_1|\ge10^{-56}\delta^{116}.      \tag{3}
\]

More generally, for any profile in the domain of (1), put
\(\epsilon=\max_{0\le k\le5}|DC[z^k]|\). Then
\[
                 \epsilon+\sigma\ge10^{-56}\delta^{116}. \tag{3a}
\]
This controls approximate coefficient stationarity as well; epsilon
refers to the explicitly fixed-norm chart.

Writing mu_k=sum ai^k, the following two consequences hold:

\[
 \mu_3^2+\mu_5^2+\mu_7^2\ge
       \frac{705600}{284929\,10^{112}}\delta^{232},      \tag{4}
\]

and the Euclidean distance from a to the set of balanced, norm-one,
reflection-symmetric original profiles, allowing **all permutations and
collisions in the target**, is at least

\[
                   \frac{\delta^{116}}{384\,10^{56}}.  \tag{5}
\]

These are coarse explicit sufficient constants. The qualitative
even-stationary exclusion was already proved in
[9398](../even-angular-exclusion/PROOF.md) and confirmed by
[REVIEW9416](../../six-reviewer-1/even-angular-audit/REVIEW.md).
The new statements quantify that exclusion and its transfer to arbitrary
separated stationary originals. They do not assert stationary existence.
In particular (4) contains **mu7**. It does not remove the p5 hypothesis
from the two-moment bound of [9952](../joint-moment-coercivity/PROOF.md).
No collision continuation, physical H bound or degree-nine complex
first-power endpoint is concluded.

## 2. Basic separated-root geometry

For any balanced, norm-one eight-distinct real profile with original
gap at least gamma in(0,1], every original and critical has modulus at
most1. The classical derivative-mesh argument reproduced in Section7 of
9952 gives

\[
 \lambda_{j+1}-\lambda_j>\gamma,\qquad
 |h'(\lambda_j)|\ge\gamma^6(j-1)!(7-j)!\ge36\gamma^6.  \tag{6}
\]

For completeness, if x=lambda_j and y=x+gamma is in the next original
interval, compare the strictly decreasing g(w)=sum 1/(w-ai) there.
For i=2,...,8, y-ai<=x-a_(i-1); these paired denominators have the same
sign. Reciprocation on each sign interval gives
g(y)>=-1/(x-a8)+1/(y-a1)>0, hence lambda_(j+1)>y. If y is still in
the preceding interval the conclusion follows directly from interlacing.
Also y<a_(j+2), so these cases cover its possible positions. This
establishes (6) without an unproved root-spacing inference.

There are two originals of the same sign separated by at least gamma;
their squares differ by at least gamma². For x_i=a_i² and mean1/8,
two terms of the variance give

\[
 D=\sum_i(x_i-1/8)^2\ge\tfrac12\gamma^4.              \tag{7}
\]

Distinctness ensures D>0. Moreover D<1 and 0<eta<1. The positivity and
sum of the masses in (1) also follow directly from the proper partial
fraction expansion of -8f/h: its residues are positive by interlacing,
and its z^-1 coefficient is -8(-1/2+3/8)=1.

For an even profile, write its four positive originals as x1<...<x4.
Their squares sum1/2, and x1>=delta/2. Thus

\[
 \tfrac38\delta^4\le a<\tfrac3{32},\quad b<0,
 \quad |a|,|b|,|c|\le1.                               \tag{8}
\]

Here a is the sum of the six products of original squares. Put
h=z r(z²), r(X)=X³-3X²/8+(a/2)X+b/4. The central critical is0.
Its three positive criticals have modulus greater than delta by (6);
their squared values have mutual gaps at least delta². Consequently

\[
 |b|\ge4\delta^6,\qquad \operatorname{disc}(r)\ge\delta^{12}.
                                                               \tag{9}
\]

All these estimates concern actual simple real original profiles, not
arbitrary polynomial tuples or an assumed feasible constant-term center.

## 3. Whole even trace and two undivided lifts

Use the complete credited9398 polynomials

\[
\begin{split}
 A&=32a-3,\quad d=15-112a,\quad g=208a-15,\\
 L&=256a^3-18a^2+432ab+864b^2-27b,\\
 H&=512a^3-36a^2+736ab+1344b^2-45b,\\
 U&=16a^2-a+6b,\\
 W&=4096a^4-512a^3+7680a^2b+18a^2-816ab+1440b^2+27b,\\
 J&=8192a^4-1024a^3+13312a^2b+36a^2-1376ab+2496b^2+45b,\\
 V&=8192a^4+13312a^2b-36a^2+96ab+5184b^2-45b,\\
 F&=4a^2+d b,\quad G=4a^2(64a-5)+g b,\\
 T&=27648a^2-4960a+225
   =27648(a-155/1728)^2+275/108.
\end{split}                                                   \tag{10}
\]

Here H is a polynomial, not the physical Hermitian matrix in degree-nine
Sendov research. The full trace and completion identities are

\[
 \operatorname{disc}(r)=-L/512,\quad
 \eta=\frac{768H}{b^2L}c^2-\frac{3072U}{L}c-\frac{W}{2L},
 \quad WH+6144b^2U^2=LJ,\quad 2H+J=V.                 \tag{11}
\]

The checker reconstructs (11) from the 3x3 companion matrix of r,
not from sampled roots. At a positive critical square X, the mass is
-4p(X)/(Xr'(X)), where p(X)=X4-X3/2+aX2+bX+c; at0 it is -32c/b.
Thus the c² coefficient alpha=768H/(b²L) in eta is a sum of squares
of mass slopes and is at least1024/b². In particular L<0,H<0 and

\[
 |A|=8D\ge4\delta^4,\quad 9/2\le d\le15,\quad |A|\le3,
 \quad |L|\ge512\delta^{12},\quad
 |H|\ge(2048/3)\delta^{12}.                           \tag{12}
\]

Define the rational expressions on these known nonzero denominators

\[
 c_*=2b^2U/H,\quad \bar C=-4V/(AH),\quad
 w=-6144H/(A b^2L)>0,\quad k=c-c_*.
\]

The whole completion is C=Cbar-w k². No feasibility of c* is asserted.
Let

\[
 N_a=V_aAH-V(32H+AH_a),\qquad N_b=V_bH-VH_b=768FG.
\]

The **new undivided full lifts** used below are

\[
 d^4N_a+1075200a^4A^4(56a-5)^2=F D_F,                 \tag{13}
\]

\[
 g^2\operatorname{disc}(r)+a^2A^2T/256=G W_G,        \tag{14}
\]

where all coefficients of DF,WG are given in
[expected.json](expected.json) and reproduced by [verify.py](verify.py).
Explicit definitions that require no polynomial division are as follows.
Write Na=sum c_(i,j) a^i b^j; its b degree is at most4. Then

\[
 D_F=\sum_{i,j}c_{i,j}a^i
         \sum_{\ell=0}^{j-1}b^{j-1-\ell}(-4a^2)^\ell d^{3-\ell},
\]

with the inner sum0 when j=0. Also, putting g0=4a²(64a-5),

\[
 W_G=-27G/16+27g_0/8-g(432a-27)/512.
\]

Every term is polynomial. The full F-branch cleared identity is

\[
 d^2 H(a,-4a^2/d)=8a^2A(56a-5)(448a-45).              \tag{15}
\]

Importantly, (13) retains the factor (56a-5)². At a=5/56 the F-branch
H vanishes; that point cannot satisfy (12). No division by this factor,
by g or by an unknown polynomial rank is used. The g=0 value a=15/208
is covered by (14).

For a polynomial P let |P|coef be the sum of absolute values of **all**
its rational coefficients. The whole exact computations give

| Polynomial | Whole coefficient norm |
|---|---:|
| DF | 5615304682700256 |
| WG | 533493/512 <=1042 |
| H | 2673 |
| Ha, Hb | 2344, 3469 |
| La, Lb | 1236, 2187 |
| n=2b²U, na, nb | 46, 66, 104 |

On |a|,|b|<=1 these are sufficient bounds for the polynomials and
derivatives, including the full real b segment used next.

## 4. Explicit reduced even gradient

Put kappa=10^-8. First suppose |F|<=kappa delta32. The point
bF=-4a²/d lies in[-1,0], as does actual b. The fundamental theorem
of calculus, Hb norm and (12) imply

\[
 |H(a,b)-H(a,b_F)|\le3469|F|/d,
 \quad \left|\frac{H(a,b_F)}{H(a,b)}\right|\ge\tfrac12,
\]

because 3469 kappa/((9/2)(2048/3))=3469/307200000000<1/2
and delta20<=1. Differentiating Cbar at actual a,b, (13)--(15) give

\[
 \bar C_a=
 \frac{67200H(a,b_F)^2}{H(a,b)^2(448a-45)^2}
 -\frac{4F D_F}{d^4A^2H(a,b)^2}.                       \tag{16}
\]

In this domain |448a-45|<=45 and it is at least3. The first term of
(16) is at least224/27. The absolute value of its second term is at
most

\[
 \frac{4\kappa\,5615304682700256}
 {(9/2)^4\,16\,(2048/3)^2}
 =\frac{58492757111461}{796262400000000}.
\]

Their difference exceeds1. This proves Cbar_a>1 in the entire **closed**
small-F case, without removing the degree-loss point algebraically.

In the complementary case |F|>kappa delta32, (14), positive disc(r),
(8), (12) and T>=275/108 give

\[
 |G|\ge\frac{275}{12804096}\delta^{16}.
\]

Indeed |G|1042>=a²A²T/256; this inequality does not require WG or g
to be nonzero separately. Therefore

\[
 |\bar C_b|=\frac{3072|FG|}{|A|H^2}
 \ge \frac1{32487342624000000}\delta^{48}
 \ge10^{-17}\delta^{48}.                             \tag{17}
\]

Using delta<=1 in the small-F case as well, both cases establish the
universal reduced margin max(|Cbar_a|,|Cbar_b|)>=10^-17 delta48.

## 5. Transfer to all three full even derivatives

From (11), alpha>=1024/b² and D<1 give w=alpha/D>=1024. The
coefficient bounds and (9), (12) also give

\[
 w\le(8019/16)\delta^{-28}\le512\delta^{-28},
 \quad |w_a|,|w_b|\le10240\delta^{-40},
 \quad |(c_*)_a|,|(c_*)_b|\le\delta^{-24}.             \tag{18}
\]

Here the logarithmic derivatives of w are bounded by20delta^-12:
their sufficient coefficients are respectively
2344/(2048/3)+32/4+1236/512 and
3469/(2048/3)+2/4+2187/512, both below20. The sufficient coefficient
for the two center derivatives is

\[
 104/(2048/3)+46\cdot3469/(2048/3)^2
       =1037571/2097152<1.
\]

Let epsilon=max(|Ca|,|Cb|,|Cc|). If epsilon>1, (2) is immediate.
Otherwise Cc=-2wk gives |k|<=epsilon/2048. Differentiating the whole
C=Cbar-wk² identity at fixed c gives, for j=a,b,

\[
 \bar C_j=C_j+w_jk^2+C_c(c_*)_j.
\]

By (18), epsilon<=1 and delta<=1, both reduced derivatives have
absolute value at most

\[
 (2+10240/2048^2)\epsilon\delta^{-40}
                  <3\epsilon\delta^{-40}.
\]

Combined with (17) and its small-F counterpart, this proves
epsilon>=10^-17 delta88/3>=10^-18 delta88, establishing Theorem A.

## 6. A uniform full moving-node Hessian estimate

This estimate is for **any** actual balanced norm-one eight-distinct
real originals with gap at least gamma in(0,1], not just even ones.
For fixed real coefficient directions q,v of degree at most5, put
Q=|q|coef and V0=|v|coef. Then

\[
                 |D^2C[q,v]|\le1000\gamma^{-28} QV_0. \tag{19}
\]

We prove (19) from the actual nodes. At each critical write H1=h',
J1=h'', and let primes on q denote z derivatives at that node. The
full first derivatives credited to9496 are

\[
 \lambda'_v=-v'/(8H_1),\qquad
 m'_q=-8q/H_1-mq''/(8H_1)+mJ_1q'/(8H_1^2).          \tag{20}
\]

Using |lambda|<=1, (6) and h=product(z-lambda_j),

\[
 |h''|\le7\cdot6\,2^5=1344,\quad
 |h'''|\le7\cdot6\cdot5\,2^4=3360,\quad
 |q^{(k)}|\le(5)_k Q\quad(k=0,1,2,3).
\]

These product coefficient bounds are universal; they do not come from
finite node tests. Since 0<m<=1, direct substitution yields

\[
 |\lambda'_v|\le V_0\gamma^{-6},\quad
 |m'_q|\le Q\gamma^{-12},\quad
 |D_vH_1|\le1347 V_0\gamma^{-6},\quad
 |D_vJ_1|\le3368 V_0\gamma^{-6}.                       \tag{21}
\]

For the first two estimates the sufficient coefficients are5/288 and
203/216, respectively. The last two retain moving-node terms:
DvH1=v''/8+J1 lambda'_v and DvJ1=v'''/8+h''' lambda'_v.

Differentiate **all three terms** of (20), including every moving
evaluation. The complete second mass derivative consists of

\[
\begin{split}
 m''_{qv}={}&-8q'\lambda'_v/H_1+8q(D_vH_1)/H_1^2\\
 &-m'_v q''/(8H_1)-m q'''\lambda'_v/(8H_1)
       +m q''(D_vH_1)/(8H_1^2)\\
 &+m'_vJ_1q'/(8H_1^2)+m(D_vJ_1)q'/(8H_1^2)
       +mJ_1q''\lambda'_v/(8H_1^2)
       -mJ_1q'(D_vH_1)/(4H_1^3).
\end{split}                                                   \tag{22}
\]

The portable checker differentiates the full symbolic Laurent jet
and compares every monomial of (22). The nine coefficient bounds in
their displayed order, after gamma<=1 absorbs all powers into
gamma^-24, sum to

\[
 \frac{8\cdot5}{36}+\frac{8\cdot1347}{36^2}
 +\frac{20}{8\cdot36}+\frac{60}{8\cdot36}
 +\frac{20\cdot1347}{8\cdot36^2}
 +\frac{1344\cdot5}{8\cdot36^2}
 +\frac{3368\cdot5}{8\cdot36^2}
 +\frac{1344\cdot20}{8\cdot36^2}
 +\frac{2\cdot1344\cdot5\cdot1347}{8\cdot36^3}
 =18913/288<100.
\]

Thus |m''qv|<=100QV0 gamma^-24. Positivity and sum m=1 imply
|eta'_q|<=2Q gamma^-12 and
|eta''qv|<=2(7+100)QV0 gamma^-24=214QV0 gamma^-24.

The full Newton identity D=3/8-4f4 gives D'_q=-4q4 and D''qv=0.
Differentiating (1) twice, the three types of terms have bounds

\[
 |\eta''_{qv}|/D\le428QV_0\gamma^{-28},\quad
 (|\eta'_qD'_v|+|\eta'_vD'_q|)/D^2\le64QV_0\gamma^{-20},
 \quad 2(1-\eta)|D'_qD'_v|/D^3\le256QV_0\gamma^{-12}.
\]

By gamma<=1 their sum is at most748QV0 gamma^-28, proving (19).
All critical nodes and masses in this proof are the actual ones;
there is no frozen-pole approximation.

## 7. A real-root path to the even part

At the stationary profile let q=f_even-f=-(f5 z5+f3 z3+f1 z).
Then |q|coef=sigma. If sigma>delta8, (3) follows immediately since
delta<=1. Suppose instead sigma<=delta8 and consider f_s=f+s q,
0<=s<=1.

At the endpoints ai+-delta/4 of each of the eight disjoint original
root boxes,

\[
 |f(ai\pm\delta/4)|\ge
 \frac\delta4(3\delta/4)^7(i-1)!(8-i)!
 \ge(19683/4096)\delta^8.
\]

Each endpoint has modulus at most5/4, so
|q(ai+-delta/4)|<=(3125/1024)sigma<|f(ai+-delta/4)|.
The endpoint signs of f_s therefore equal those of f for **every**
s in[0,1]. They have opposite signs in each box. Degree8 and the
intermediate value theorem force exactly one simple real root in each
box; there is no room for a multiple or additional root. All f_s
original gaps are at least delta/2. Their fixed coefficients f7=0,
f6=-1/2 preserve balance and norm1 by Newton identities.

This is a feasible real simple-root path, including both endpoints.
Its criticals remain simple by interlacing, so C is smooth along it.
At s=0, stationarity makes the six fixed-norm coefficient derivatives
zero. For each of the directions z4,z2,1, integrate (19) with
v=q and gamma=delta/2. Since each of those directions has coefficient
norm1,

\[
 \max(|C_a(f_{even})|,|C_b(f_{even})|,|C_c(f_{even})|)
       \le1000(\delta/2)^{-28}\sigma.
\]

Theorem A applies to the actual even endpoint f_even, with gap
delta/2, and gives the lower bound10^-18(delta/2)^88. Consequently

\[
 \sigma\ge\frac1{10^{21}2^{116}}\delta^{116}
                   \ge10^{-56}\delta^{116}.
\]

The last comparison is exact integer arithmetic. It also holds on
the closed small-sigma threshold. This proves Theorem B without a
mass-leading-coefficient assumption.

For an arbitrary profile replace the vanishing initial derivatives by
their bound epsilon=max_(0<=k<=5)|DC[z^k]|. The same path gives
10^-18(delta/2)^88<=epsilon+1000(delta/2)^-28 sigma.
Since1000(delta/2)^-28>=1, it follows that
epsilon+sigma>=delta116/(10^21*2^116)>=10^-56 delta116.
The large-sigma branch again implies the same bound directly. Thus the
joint gradient/asymmetry assertion also holds without stationarity.

## 8. Odd moments and distance from reflection symmetry

The full balanced norm-one Newton identities give

\[
 f_5=-\mu_3/3,\quad f_3=\mu_3/6-\mu_5/5,\quad
 f_1=(\mu_4/12-1/24)\mu_3+\mu_5/10-\mu_7/7.          \tag{23}
\]

These are whole polynomial identities in independent moment
variables, not sample-profile fits. Cauchy--Schwarz and |ai|<=1 give
1/8<=mu4<=1, hence |mu4/12-1/24|<=1/24. Therefore

\[
 \sigma\le(13/24)|\mu_3|+(3/10)|\mu_5|+(1/7)|\mu_7|,
\]

whose squared weight norm is284929/705600. Cauchy--Schwarz and (3)
give exactly (4). There is no deduction of a two-moment gap here.

For any real balanced norm-one reflection-symmetric target b and
any pairing of its coordinates with a, all coordinate moduli are
at most1. Telescoping the two products f_a and f_b gives

\[
 |f_a-f_b|_{coef}\le2^7\sum_i|a_i-b_i|
             \le128\sqrt8\|a-b\|_2<384\|a-b\|_2.
\]

Since f_b is even, the odd coefficient norm sigma of f_a is at most
|f_a-f_b|coef. Thus every such b, including colliding originals and
every permutation, obeys ||a-b||2>=sigma/384. Taking the infimum
and using (3) proves (5). Similarly the sorted paired-reflection
defect ||a+reverse(a)||2 is at least sigma/192, from one half of the
product difference between a and -reverse(a); this is an additional
equivalent diagnostic, not a stationary classification.

## 9. Certificate, reproduction and remaining frontier

Run CPython3.10+ standard library, with all native thread variables1:

    python3 -I -B verify.py
    python3 -I -B -O verify.py

The checker regenerates and fully multiplies all13 algebraic identities,
the whole nine-term Laurent moving-node jet, the whole seven-stage
Newton recurrence, every coefficient norm and all20 rational comparisons.
It compares the **entire typed record**, including the full coefficients
of both lifts and all domain/scope fields. Six mathematical damages
are rejected under normal and optimized Python. One exact feasible
even-root-square control and two polynomial exceptional-branch controls
are consistency checks; no universal statement rests on those samples.
An externally altered last DF coefficient is also rejected in both modes.
`--bootstrap` is author-only initial fixture construction, not independent
verification. There is no runtime CAS or solver dependency.

Same-author sparse arithmetic and the cubic trace algorithm openly adapt
9398; this is not algorithmically independent review. The universal
real-root mesh, variance, sum-of-squares sign, coefficient estimates,
differential integration, real-root path and Cauchy--Schwarz arguments
are ordinary written mathematics. Exact arithmetic, hashes and controls
do not formalize those arguments. REVIEW9416 confirms the earlier9398
exclusion, not this quantitative extension.9952 and the reviews of its
earlier inputs do not supply a verdict here.

The useful new frontier is separation-only **stationary asymmetry** and
its three-moment/reflection-distance stability. To make9952's explicit
two-moment bound depend on delta alone, the next obligation remains a
quantitative lower bound for the leading degree-five mass coefficient
p5, using the unscaled lower-degree equations. This proof controls the
near-even boundary for that next reduction; it does not complete it.
No stationary solution, global angular maximum, collision continuation,
physical energy or global degree-nine first-power inequality is claimed.
