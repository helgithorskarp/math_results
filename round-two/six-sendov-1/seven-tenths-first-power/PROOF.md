# A complex first-power gap through the marked radius 7/10

**Complete ordinary proof, six-sendov-1 / researcher, 2026-10-04.**
Unformalized and independently unreviewed as a new child. The exact local
certificate checks every explicit closed cover and complete rational
payment. Finite controls test representations; they do not replace the
ordinary continuum arguments or the external REAL Banach theorem.

## 1. Statement, scope and credited methods

Let p be ANY complex polynomial of degree nine whose ALL nine original
zeros lie in the CLOSED unit disk. For EVERY marked original zero a with
11/16 <= |a| <= 7/10, counting ALL eight critical multiplicities, we prove

\[
F:=\sum_{j=1}^{8}|a-\zeta_j|^{-1}>8+1/10000.                 \tag{1}
\]

A zero denominator gives infinity. Both marked endpoints, arbitrary
complex directions and original/critical multiplicities are included.
There is no balance, conjugacy, simplicity, separation, rationality or
quadratic-moment premise. The gap and radius are sufficient, not optimal.

This is a new adjacent-annulus calculation using published generic
methods, not a consequence of the previous annulus's numerical exclusion.
The same author's [LEMMA10322](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/eleven-sixteenths-first-power/PROOF.md),
source d8eb0d1b908151a1ad1a67c92238860f9fbaf3d4, supplies the openly
adapted communication/Hermite/centered/mean/product/physical contraction
and clipping methods. They are fully written here, and all defining
programs and compact covers are LOCAL. No ancestor/private/reviewer
executable, coefficient corpus or numerical verdict is a runtime input.

The smaller generic centered high-order coefficient caps used in Section5
are PUBLISHED PRIOR ART: [Roos1203.2871, Lemma2.2](https://arxiv.org/html/1203.2871)
and [Han--Niles-Weed2408.09341, Theorem4.3(1)](https://arxiv.org/html/2408.09341).
The ordinary direct contour proof and every normalization are supplied
below. This work does not claim a new generic coefficient theorem.

The independently selected [REVIEW10334](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/eleven-sixteenths-audit/REVIEW.md),
source609df74ccbd0616ef498a11f4bfd75c65a1cf2d2, confirms10322 and
proves a larger1/8800 gap on its SAME[27/40,11/16] annulus. That scoped
verdict is prior context, not independent review of this new child.
The current adjacent proof uses none of the old numerical exclusions.

For the union corollary,10322 supplies gap1/10000 on[27/40,11/16]
and [LEMMA10300](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/mass-eight-coupled-gap/PROOF.md),
sourcee6d2da6d0b3790a7055614206d79d36559ebc8ab, supplies the stronger
1/350 gap on[2/3,27/40]. Their union with(1) gives gap1/10000 on the
CLOSED[2/3,7/10]. These union premises are EXPLICIT dependencies, not
independently reverified ancestors. [LEMMA10240](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/two-thirds-first-power/PROOF.md),
source30db7e5530428c28667f72e229a29acf337833ee, additionally supplies
strictF>8 for|a|<=2/3, giving strictF>8 throughout|a|<=7/10. No uniform
numeric gap is asserted on that WHOLE lower disk. There is no global
first-power theorem, sharp radius, globally optimized gap or actual-root
feasibility converse.

[Tang--Zhang2609.19126, Conjecture1.2](https://arxiv.org/html/2609.19126)
still states the first-power endpoint; its quadratic Theorem1.3 and
Corollary1.4 are not FIRST premises. The communication identities are
classical, appear as Lemma3.1 there and as
[Tao's Lemma6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
All methods/inputs and their ordinary trust boundaries are credited in
[LITERATURE.md](LITERATURE.md). No historical priority for affine
normalization, elementary contour extraction or the scalar variance
inequality is asserted.

Rotate a to positive real a. If p'(a)=0 then F is infinity. Otherwise a
is simple, and all \(q_j=(a-\zeta_j)^{-1}\) are finite and nonzero. Put

\[
r_j=|q_j|,\quad F=\sum r_j,\quad T=\sum(r_j-1)^2,\quad
\mu=\tfrac18\sum q_j=u+iv,\quad w=v^2,\quad
E=\sum|q_j-1|^2,\quad \Pi=F-8u,\quad S=\sum|q_j-\mu|^2.
\]

Set b=1-a² and retain both entire eight-factor channels

\[
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt,\qquad
J_a(q)=\int_0^1\prod_j[a+btq_j]\,dt.
\tag{2}
\]

After making p monic write \(p(z)=(z-a)\prod_{k=1}^8(z-z_k)\).
Its derivative is \(p'(z)=9\prod_j(z-\zeta_j)\), and
\(p'(a)=9/\prod q_j=\prod(a-z_k)\). Integrating from a to0 and
from a to1/a gives

\[
O_a(q)=\prod_{k=1}^8z_k\prod_{j=1}^8q_j,\qquad
J_a(q)=\prod_{k=1}^8\frac{1-az_k}{a-z_k}.
\tag{3}
\]

Indeed z=a(1-t) gives \(O=-p(0)\prod q_j/a\), while
\(p(0)=-a\prod z_k\). The other substitution z=a+bt/a gives
\(p(1/a)=9bJ/[a^9\prod q_j]\). Thus all eight denominator factors,
the factor9 and a^9 are retained. Gauss--Lucas and disk containment imply

\[
r_j\ge1/(1+a),\qquad
|1-az_k|^2-|a-z_k|^2=(1-a^2)(1-|z_k|^2)\ge0,
\quad |J_a(q)|\ge1,\quad |O_a(q)|\le\prod r_j.
\tag{4}
\]

These classical communication channels are credited to Tang--Zhang and
the parent source. No converse to original-root feasibility is needed.
The finite face concerns possibly nonactual formal tuples of mass8;
only the channels in (4) refer to the original disk polynomial. Sections2–9
give sufficient formal-tuple estimates. Section10 verifies a complete
closed four-dimensional face; Section11 pays the full clipping path.


## 1a. Exact physical reduction to mass eight

Suppose the actual reciprocal sum is finite and F<=8. Every reciprocal
is positive in modulus, so 0<F<=8. Set lambda=F/8 in (0,1] and

\[
p_\lambda(z)=\lambda^9p\bigl(a+(z-a)/\lambda\bigr).
\tag{H1}
\]

Its degree is exactly nine and its leading coefficient is unchanged.
Every original zero becomes z_i^lambda=a+lambda(z_i-a), including the
marked zero a. Every critical point becomes
zeta_j^lambda=a+lambda(zeta_j-a), because

\[
p_\lambda'(z)=\lambda^8p'\bigl(a+(z-a)/\lambda\bigr).
\tag{H2}
\]

Affine substitution has nonzero slope; therefore all original and
critical multiplicities are preserved. Disk convexity gives

\[
|z_i^\lambda|\le(1-\lambda)|a|+\lambda|z_i|\le1.
\tag{H3}
\]

If lambda<1 and |a|<1 the last upper bound is strictly less than1.
Critical distances are multiplied by lambda, so every reciprocal is
divided by lambda and the new sum is exactly F/lambda=8. The marked
root is fixed; the same marked interval applies. Hence excluding actual
mass-eight disk polynomials excludes ALL actual F<=8, without a
lower-side derivative loss or a far-deficit parent theorem.

If p'(a)=0 then the reciprocal sum is infinite and (1) is immediate;
that stratum is not normalized by a finite F. Equation(H1) is elementary
affine mathematics, not a converse from a formal critical tuple to
disk-rooted originals. For F>8 the expansion lambda=F/8 generally leaves
the disk; Section11 instead uses a formal floor-preserving clipping.

## 2. Exact coupling and fresh marked budgets

Direct expansion gives

\[
E=T+2F-16u=T+2\Pi,\qquad
S=E-8[(1-u)^2+w]=T+2F-8-8(u^2+w).
\tag{5}
\]

For 1/2<=l<=a<=h<1 and 0<=x<=1, put c=l+1-l^2-h. Then

\[
h+cx-[a+(1-a^2)x]
=(1-x)(h-a)+x(a-l)(a+l-1)\ge0.
\tag{6}
\]

The NEW full-interval budgets, freshly paid, are

\[
l=11/16,\quad h=7/10,\quad c=659/1280,\\
b_-=51/100,\quad b_+=135/256,\quad a_*=357/1000.
\tag{7}
\]

For b=1-a^2, b_-<=b<=b_+ and ab>=a_*; the latter follows from
concavity of a(1-a^2) and its two endpoint values. All face tuples have
EXACT F=8. Thus the inherited convenience condition F>=37/5 is
automatic and no old scalar mass-floor result on another marked interval
is used as an entry premise. The new energy entry is proved below before
any origin derivative estimate.

## 3. Radial Hermite bound, first-power deficit and phase loss

Let real numbers \(e_1,\ldots,e_8\) satisfy \(\sum e_j\le0\),
\(T=\sum e_j^2\), and \(d=\sqrt{T/56}\). For positive \(B\) and
\(y\ge0\), assume every \(B+ye_j>0\) and \(B-yd>0\). Then

\[
\prod_j(B+ye_j)\le(B+7yd)(B-yd)^7
\exp\!\left[-\frac{3y(8-F)}{4(B-yd)}\right]
\tag{9}
\]

when \(e_j=r_j-1\), so \(\sum e_j=F-8\).
Here is the complete classical interpolation argument. Each positive
\(e_j\le\sqrt{7T/8}=7d\): the other seven sum to at most \(-e_j\),
so Cauchy–Schwarz gives \(T\ge e_j^2+e_j^2/7\). Nonpositive entries
also satisfy the upper bound. For \(T>0,y>0\), write

\[
f(x)=\log(B+yx),\quad
Q(x)=f(-d)+f'(-d)(x+d)+k(x+d)^2,
\]
\[
k=\frac{f(7d)-f(-d)-8df'(-d)}{64d^2}\le0.
\]

Since \(f'''\ge0\), quadratic Hermite interpolation gives
\(f(x)-Q(x)=f'''(\xi)(x+d)^2(x-7d)/6\le0\) throughout the
positive-factor domain with \(x\le7d\). At the interpolation nodes
this is equality; away from them, subtract a suitable multiple of
\((x+d)^2(x-7d)\) and apply Rolle's theorem three times, retaining
the derivative zero at \(-d\). This proves the remainder formula.

The linear coefficient of Q is

\[
\alpha=f'(-d)+2kd
=\frac{3y}{4(B-yd)}+
  \frac{\log[(B+7yd)/(B-yd)]}{32d}
\ge\frac{3y}{4(B-yd)}.
\]

Thus
\(\sum f(e_j)\le8Q(0)+kT+\alpha(F-8)\).
The first two terms equal \(f(7d)+7f(-d)\), by evaluating Q on
one \(7d\) and seven \(-d\). Because \(F-8\le0\), the displayed
lower bound on alpha gives (9) after exponentiation. If \(T=0\), then
\(e_j=0,F=8\), and the conclusion is direct. The case \(y=0\) is direct.
Sharpness of the radial moment estimate does not imply actual original-root
feasibility for a tuple attaining it.

The uniform radius floor \(m=10/17\) follows from the premise. Writing
\(r_j=m+x_j\), \(x_j\ge0\), \(X=\sum x_j\le8(1-m)\), gives

\[
T\le8(1-m)^2-2(1-m)X+X^2
\le56(1-m)^2=2744/289=:T_{\max}.
\tag{10}
\]

The final quadratic is convex and its maximum on the whole X interval is
at an endpoint. In particular \(d\le7/17<1\). With
\(B=a+bt,y=bt\), every positive radial factor and \(B-btd\) is positive.

Every \(e_j\) is bounded above both by \(\sqrt{7T/8}\) and by
\(F-7/(1+a)-1\). If \(D\ge0\) bounds them and \(C_D=B+btD\), then

\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j).
\]

Apply \(\tfrac12\log(1-x)\le-x/2\) and (9). A vanishing complex
factor gives the conclusion directly. Otherwise

\[
\prod_j|a+btq_j|\le(B+7btd)(B-btd)^7
\exp\!\left[-\frac{abt\Pi}{C_D^2}
-\frac{3bt(8-F)}{4(B-btd)}\right].
\tag{11}
\]

All factors and multiplicities are retained. The endpoint \(t=0\) follows
by evaluation.

## 4. Standard rational polar estimate and the full energy shell

On a marked box \(a\in[A,B_a]\), put

\[
b_-=1-B_a^2,\quad b_+=1-A^2,\quad
a_*=\min\{A(1-A^2),B_a(1-B_a^2)\},\quad c=A+1-A^2-B_a.
\]

For \(T\in[L,U]\), \(F\le F_+\le8\), \(\Pi\ge P\ge0\), define

\[
\delta=\lfloor1024\sqrt{L/56}\rfloor/1024,\quad
D=\min\{\lceil256\sqrt{7U/8}\rceil/256,
                 F_+-7/(1+B_a)-1\},
\]
\[
\widehat B=B_a+ct,\quad \widehat C=B_a+b_+(1+D)t,
\quad M_B=\widehat B(1),\quad M_C=\widehat C(1),
\]
\[
\nu=b_+(1+D)/M_C,\qquad \alpha=c/M_B.
\tag{12}
\]

The sharper cap for D uses the full per-a radius floor; a uniform10/17
floor is not substituted into its per-box denominator. The checker verifies
\(D\ge0,c-b_-\delta>0\), and both ratios in \([0,1)\).
For \(\phi(x)=(1+7x)(1-x)^7\), its logarithmic derivative on \([0,1)\)
is \(-56x/[(1+7x)(1-x)]\le0\). Therefore the radial factor in (11) is
bounded by

\[
R_L(t)=[B_a+(c+7b_-\delta)t][B_a+(c-b_-\delta)t]^7.
\tag{13}
\]

Indeed \(B\le\widehat B\) and \(btd/B\ge b_-t\delta/\widehat B\);
all factors in this comparison are positive. Positive reciprocal series
about \(t=1\) give

\[
G_2(t)=M_C^{-2}\sum_{n=0}^4(n+1)\nu^n(1-t)^n\le\widehat C(t)^{-2},
\]
\[
G_1(t)=M_B^{-1}\sum_{n=0}^4\alpha^n(1-t)^n\le\widehat B(t)^{-1}.
\tag{14}
\]

Use \(C_D\le\widehat C\), \(B-btd\le B\le\widehat B\), and set
\(K=a_*PtG_2+\tfrac34b_-(8-F_+)tG_1\ge0\).
First decrease the exponential argument in (11) to K; then use
\(e^{-K}\le1-K+K^2/2\). This yields

\[
|J_a(q)|\le\mathcal J=\int_0^1 R_L(t)[1-K(t)+K(t)^2/2]dt.
\tag{15}
\]

No monotonicity of that quadratic in K is invoked. The checker compares
all19 coefficients through degree18 by convolution versus a separate
binomial radial expansion and all kernel terms and ordered pairs. It
integrates coefficientwise and independently in the exact beta-integral basis.

If \(E\ge23/5\), then \(\Pi=(E-T)/2\ge\max(0,(23/5-U)/2)\)
on a T cell. The complete [ENTRY_COVER.json](ENTRY_COVER.json) starts with
ALL76 consecutive CLOSED radial shells

\[
L=k/8,\quad U=\min((k+1)/8,2744/289),\quad k=0,\ldots,75.
\tag{16}
\]

For each shell use \(F_+=8\) and the displayed P. Sixteen of these
initial rectangles, k=21,...,36, are divided ONLY in the marked coordinate
at111/160, into CLOSED[11/16,111/160] and CLOSED[111/160,7/10].
All other shells retain the whole marked interval. Every resulting92
closed rectangle uses its OWN fresh A,B_a endpoint budgets, whole P and
entire polynomial(15); every exact integral is strictly below2199/2200.
The76 initial shells/16 cuts/92 leaves/108 reachable nodes and ALL shared
endpoints are reconstructed in [verify.py](verify.py). An unpaid initial
sufficient bound was repaired by this subdivision; it never certified
mathematical infeasibility. There is no energy-cap change or sampled
entry argument. Thus the premise |J|>2199/2200 forces \(E<23/5\). Since the mass is exactly8, (5) and \(T\ge0\) give

\[
u\ge 1-E/16>57/80>51/80,\qquad |\mu|\le F/8\le1.
\tag{17}
\]

## 5. Sharper centered complex moments and every origin order

Put \(z_j=q_j-\mu\), so \(\sum z_j=0\) and \(\sum|z_j|^2=S\).
For S=0 all following bounds are trivial. Otherwise normalize S=1.
If \(t=\max|z_j|^2\), centering and Cauchy–Schwarz imply
\(t\le7/8\). For m=2,3,4, if \(t\le1/2\), then
\(\sum|z_j|^{2m}\le t^{m-1}\le2^{1-m}\). If \(t\ge1/2\), the
other squared radii sum to \(1-t\); concentrating that sum can only
increase its m-th power sum. Hence
\(\sum|z_j|^{2m}\le t^m+(1-t)^m\), increasing on \([1/2,7/8]\).
The endpoint values also exceed \(2^{1-m}\). Rescaling gives

\[
\sum|z_j|^4\le\tfrac{25}{32}S^2,\quad
\sum|z_j|^6\le\tfrac{43}{64}S^3,\quad
\sum|z_j|^8\le\tfrac{1201}{2048}S^4.
\tag{18}
\]

Odd absolute power sums are bounded by Cauchy–Schwarz between their adjacent
even sums. Thus \(|p_k(z)|\le\eta_k S^{k/2}\) with exact paid coefficients

\[
(\eta_2,\ldots,\eta_8)=
(1,453/512,25/32,371/512,43/64,643/1024,1201/2048).
\tag{19}
\]

Each odd coefficient is the denominator1024 upward rounding of the square
root of the product of its adjacent even coefficients. All endpoint
budgets and root roundings are checked by rational/integer squares.

Also \(|e_k(z)|\le\binom8k(S/8)^{k/2}\): triangle inequality and
Cauchy–Schwarz over subsets give
\(|e_k(z)|^2\le\binom8k e_k(|z_1|^2,\ldots,|z_8|^2)\).
For nonnegative entries with sum S, the latter symmetric sum is at most
\(\binom8k(S/8)^k\). To see this directly, maximize on the compact
simplex. A positive maximum has at least k positive entries; averaging
any unequal pair increases the symmetric sum by
\((x-y)^2e_{k-2}(\text{others})/4>0\). Thus all entries at a maximizer
are equal. The zero and k=1 cases are immediate.

Newton's identities with \(p_1(z)=0\) now give, inductively,

\[
c_0=1,\ c_1=0,\quad
c_k=\min\left\{\frac1k\sum_{j=2}^k c_{k-j}\eta_j,
\binom8k8^{-\lfloor k/2\rfloor}\tau^{k\bmod2}\right\},
\quad \tau=363/1024\ge\sqrt{1/8}.
\tag{20}
\]

Every \(|e_k(z)|\le c_kS^{k/2}\), and all seven exact constants are

\[
(c_2,\ldots,c_8)=
(1/2,151/512,41/128,1497/5120,7/128,363/65536,1/4096).
\tag{21}
\]

The coefficients in (21) are first derived by that recurrence. Retain the second, third and eighth payments, replace the fourth by \(c_4=3/16\),
as follows, and use the separately published contour payments for orders5,6,7 below. No later Newton coefficient is silently reoptimized.

For complex centered z put \(p_k=\sum z_j^k\), \(M_4=\sum|z_j|^4\),
and \(X_j=z_j^2-p_2/8\). Direct expansion and Newton give

\[
\sum X_j^2=p_4-p_2^2/8,\quad
\sum|X_j|^2=M_4-|p_2|^2/8,\quad
e_4=3p_2^2/32-\tfrac14\sum X_j^2.
\]

Consequently \(|e_4|\le M_4/4+|p_2|^2/16\le(33/128)S^2\).
This direct intermediate payment is valid in all complex directions.

For the stronger bound, let H be the REAL Euclidean zero-sum subspace
of \(\mathbb R^8\), and let P be the restriction of e4 to H. For real
z, \(p_2=S\) and \(S^2/8\le p_4\le25S^2/32\), by Cauchy--Schwarz
and (18). Hence

\[
-9S^2/128\le P(z)=S^2/8-p_4/4\le3S^2/32.
\]

Its real unit-ball norm is at most \(M=3/32\), with equality for four
equal positive and four equal negative coordinates. Let L be its
associated real symmetric four-linear form. The ONLY external analytic
premise here is Banach's REAL Hilbert-space identity equating the norm
of L on four unit vectors to the unit-ball norm of P. It is explicitly
stated for both real and complex Hilbert spaces in
[Carando--Rodriguez1810.09373, Introduction equation(2), printed page2](https://arxiv.org/pdf/1810.09373).
We use its REAL case, giving
\(|L(x,x,y,y)|\le M\|x\|^2\|y\|^2\). This published standard identity
is not proved by the finite checker and is not claimed new.

Choose a unit scalar lambda such that \(\lambda^4 e_4(z)\) is
nonnegative real; zero e4 is immediate. Write \(\lambda z=x+iy\), with
\(x,y\in H\), \(X=\|x\|^2\), \(Y=\|y\|^2\), \(X+Y=S\).
The unique complex extension of P is the same elementary symmetric
polynomial on the complex zero-sum subspace. Its full fourth expansion gives

\[
|e_4(z)|=P(x)-6L(x,x,y,y)+P(y)
\le M(X^2+6XY+Y^2)\le2M(X+Y)^2=(3/16)S^2.
\]

The last difference is exactly \(M(X-Y)^2\ge0\). No orthogonality,
equal norms, conjugacy, balance or actual original-root feasibility is
assumed. This deduction is ordinary and unformalized; historical priority
for the quartic estimate is not asserted. All final constants, including the contour payments below, are

\[
(c_2,\ldots,c_8)=
(1/2,151/512,3/16,5/64,1/54,13/4096,1/4096).
\tag{21a}
\]

For completeness the PUBLISHED centered contour estimate is proved here.
Let \(G(w)=\prod_{j=1}^8(1+wz_j)=\sum_{k=0}^8e_k(z)w^k\), where
\(\sum z_j=0\), \(S=\sum|z_j|^2\). If S=0 all positive orders vanish.
For S>0, finite Fourier coefficient extraction on|w|=r gives
\(|e_k|\le r^{-k}\max_\theta|G(re^{i\theta})|\). Squared factor
moduli have mean \(1+r^2S/8\), because the entire linear term vanishes.
Nonnegative AM-GM consequently gives
\(|G|\le(1+r^2S/8)^4\). For1<=k<8, choose
\(r^2S=8k/(8-k)\) and simplify to

\[
|e_k(z)|^2\le
\frac{8^{8-k}}{k^k(8-k)^{8-k}}S^k.
\tag{21b}
\]

This is the n=8 normalized specialization of the credited Roos/
Han--Niles-Weed bound, not a new generic result. For orders5,6,7 its
complete squared constants are512/84375,1/2916,8/823543.
The exact rational upward caps5/64,1/54,13/4096 give(21a).
For k=8, AM-GM on the eight|z_j|^2 gives1/4096 directly.
All rational normalization/cap-square comparisons are paid by the local
origin/core routines. Every order is retained; replacing the quartic or
these contour caps never silently feeds a different Newton recurrence.

The complete expansion is

\[
\prod_j(1-atq_j)=\sum_{k=0}^8 e_k(z)(-at)^k(1-at\mu)^{8-k}.
\tag{22}
\]

The first centered term vanishes; every order2 through8 remains.

## 6. Synchronized real mean and convex endpoint anchor

Consider a closed box with coordinates
\((a,E,F,u,w)\in[A,B_a]\times[E_-,E_+]\times[F_-,F_+]
\times[U_-,U_+]\times[W_-,W_+]\), and necessary T interval \([T_-,T_+]\).
Write

\[
s_{\rm mean}=\min\{1,U_+^2+W_+,(F_+/8)^2\},\qquad
s_\beta=\min\{s_{\rm mean},U_-^2+W_+\},
\]
\[
S_+=\min\{E_+-8[(1-U_+)^2+W_-],
               T_++2F_+-8-8(U_-^2+W_-)\}.
\tag{23}
\]

The first coefficient bounds actual \(|\mu|^2\), and both centered
bounds follow from (5). **The coefficient \(s_\beta\) is only an
envelope parameter; it does not bound actual \(|\mu|^2\).**
This distinction is essential in the diagonal denominator below.

For fixed a,t,w and \(U_-\le u\le1\), the exact difference is

\[
(1-atU_-)^2-(1-atu)^2
=at(u-U_-)[2-at(u+U_-)]\ge0,
\tag{24}
\]

because \(a\le7/10,t\le1\). Increasing w to \(W_+\) gives
\(|1-at\mu|^2\le1-2aU_-t+a^2(U_-^2+W_+)t^2\).
The separate actual norm bound gives the same inequality with coefficient
\(s_{\rm mean}\). Taking the smaller coefficient therefore proves

\[
|1-at\mu|^2\le1-2aU_-t+a^2s_\beta t^2.
\tag{25}
\]

Set

\[
A_0=\min\{A,2U_-/s_\beta-B_a\},\qquad
\beta(t)=1-2A_0U_-t+A_0^2s_\beta t^2.
\tag{26}
\]

Since \(U_-\ge51/80\), \(s_\beta\le1\), and \(B_a\le7/10\),
we have \(0<23/40\le A_0\le A\le B_a\) and
\(2U_-\ge(A_0+B_a)s_\beta\). The quadratic in a in (25) is convex.
Its value at A0 dominates its value at \(B_a\), since their difference is
\((B_a-A_0)t[2U_--(A_0+B_a)s_\beta t]\ge0\).
Thus beta bounds the entire actual a interval, even when \(U_-<B_a\).
The anchor is not the actual marked root; \(B_a\) still pays all remainder
amplitudes and the diagonal denominator.

The checker verifies \(U_-^2\le s_\beta\le s_{\rm mean}\le1\),
\(U_->A_0s_\beta\), \(0<\beta(1)<1\), and \(1-A_0U_->0\).
Hence beta is positive and decreasing. Completing its square and using
\(\sqrt{x^2+d}\le x+d/(2x)\), with \(x\ge1-A_0U_->0,d\ge0\), gives

\[
\sqrt{\beta(t)}\le Q(t)=1-A_0U_-t+
\frac{A_0^2(s_\beta-U_-^2)}{2(1-A_0U_-)}t^2.
\tag{27}
\]

For even k use \(H_k=\beta^{(8-k)/2}\); for odd k use
\(H_k=\beta^{(7-k)/2}Q\). Let \(d_s,d_\beta,d_S\) be denominator4096
square-root ceilings of \(s_{\rm mean},\beta(1),S_+\), respectively.
All nonnegative operands, minimal upward roundings and signs are checked.
The complete centered remainder is bounded by

\[
R=9\sum_{k=2}^8 B_a^k c_k S_+^{\lfloor k/2\rfloor}d_S^{k\bmod2}
                  \int_0^1t^kH_k(t)\,dt.
\tag{28}
\]

Integrating the diagonal in (22) gives
\((1-(1-a\mu)^9)/(a\mu)\), where \(\mu\ne0\) since \(u\ge51/80\).
With its positive numerator bound,

\[
|O_a(q)|\ge D-R,\qquad
D=\frac{1-d_\beta\beta(1)^4}{B_a d_s}.
\tag{29}
\]

The denominator uses the actual norm bound \(s_{\rm mean}\), never
the synchronized coefficient \(s_\beta\). Each of all seven full
remainder coefficient vectors is compared by multiplication versus complete
multinomial counting. Every integral is independently recomputed from
the multinomial choices, and its nonnegative sign is checked. No last
order or favorable complex phase is discarded.

## 6a. Retaining the actual mean in the centered polynomial

Write the box endpoints as \(a\in[A,B]\), \(u\in[L,U]\subset(0,1]\),
\(w\in[W_l,W_h]\). Choose

\[
A_0=\min\{A,2L/(L^2+W_h)-B,2U/(U^2+W_h)-B\}>0.
\]

The checker pays BOTH endpoint inequalities
\(2L\ge(A_0+B)(L^2+W_h)\) and
\(2U\ge(A_0+B)(U^2+W_h)\). Their left-minus-right function of u is
concave, so both endpoints pay the whole interval. Convexity in a and
\(A_0\le A\le a\le B\) then give

\[
|1-at\mu|^2\le\beta(u,t)=1-2A_0ut+A_0^2(u^2+W_h)t^2.
\]

Indeed the value at A0 minus its value at B is
\((B-A_0)t[2u-(A_0+B)(u^2+W_h)t]\ge0\). The positive square
\(1-A_0ut\ge1-A_0U>0\) and completing the square give

\[
\sqrt\beta\le Q(u,t)=1-A_0ut+
\frac{A_0^2W_h}{2(1-A_0U)}t^2.
\]

Select ONE of the polynomial centered-energy envelopes

\[
\overline S_E(u)=E_+-8[(1-u)^2+W_l],\qquad
\overline S_J(u)=T_++2F_+-8-8(u^2+W_l).
\]

The first is increasing for u<=1 and must be nonnegative at L; the
second is decreasing for u>0 and must be nonnegative at U. Each separately
bounds S by (5). Their pointwise minimum is not used as one polynomial.
Let dS be a denominator4096 square-root ceiling of the chosen whole-u
maximum. Keep the distinct actual mean-norm ceiling
\(d_m\ge\sqrt{\min(1,U^2+W_h,(F_+/8)^2)}\).
Let \(d_b\ge\sqrt{\beta(L,1)}\) be its separate ceiling. Since
\(\partial_u\beta(u,1)=-2A_0(1-A_0u)<0\), this is a whole-u
endpoint bound. Require \(1-d_b\beta(L,1)^4>0\).

For even k put \(H_k=\beta^{(8-k)/2}\), and for odd k put
\(H_k=\beta^{(7-k)/2}Q\). Applying ALL seven centered bounds in
(22), not discarding any favorable/unfavorable phase, gives

\[
R(u)=9\sum_{k=2}^8 B^kc_k\overline S(u)^{\lfloor k/2\rfloor}
d_S^{k\bmod2}\int_0^1t^kH_k(u,t)\,dt,
\quad
D(u)=\frac{1-d_b\beta(u,1)^4}{Bd_m},
\quad |O_a(q)|\ge D(u)-R(u).
\]

D-R is a rational polynomial of degree at most8. The same ordinary
Bernstein convexity as (33), with degree8, gives its whole CLOSED-u
lower bound from ALL NINE controls. Each of ALL seven9x10u/t matrices
is compared by repeated convolution versus direct multiplicity enumeration.
Every integral coefficient is independently paid before coalescing raw
monomials; all nine translations and reconstructed controls are compared.

## 6b. Positive linear actual-norm denominator and all ten controls

The numerator \(N(u)=1-d_b\beta(u,1)^4\) is positive throughout.
For u>=L>0, the ACTUAL mean norm obeys

\[
|\mu|\le\sqrt{u^2+W_h}\le u+W_h/(2u)\le u+W_h/(2L).
\]

Put \(d(u)=B[u+W_h/(2L)]>0\). The diagonal integral in (22) is
therefore at least \(N(u)/d(u)\) in modulus. Retain the SAME complete
remainder R(u), and clear the positive denominator:

\[
|O_a(q)|\ge N(u)/d(u)-R(u)=1+P(u)/d(u),
\qquad P(u)=N(u)-d(u)[1+R(u)].
\]

P has degree at most9. Its TEN closed-interval Bernstein controls give
\(p_{\min}\le P(u)\). If \(p_{\min}\ge0\), use
\(1+p_{\min}/d(U)\); if \(p_{\min}<0\), use
\(1+p_{\min}/d(L)\). This sign-dependent division is essential.
Each is a valid whole-u lower bound; the maximum of this bound and
the degree8 bound remains valid, without an unpaid polynomial minimum.

The verifier compares ALL TEN numerator and cleared coefficients,
ALL100 coefficients of d times the complete bivariate remainder,
both integrated representations, and every degree9 translation and
reconstructed Bernstein coefficient. It explicitly pays d(L)>0,
both anchor endpoints and the full energy/root gates. An unavailable
gate is recorded as unavailable and is never a proof of nonexistence.

## 7. Retaining E/T dependence in the polar bound

The extra polar estimate keeps the **actual** \(d=\sqrt{T/56}\) as a
polynomial parameter. Enclose it in the CLOSED rational interval

\[
d_- =\lfloor4096\sqrt{T_-/56}\rfloor/4096,\qquad
d_+ =\lceil4096\sqrt{T_+/56}\rceil/4096.
\tag{30}
\]

Keep D and the reciprocal kernels from (12)–(14), using the box's full
\(T_+\). Now
\(\Pi=(E-T)/2\ge E_-/2-28d^2\).
This estimate is used only when \(E_-/2-28d_+^2\ge0\), and the checker
also verifies \(c-b_-d_+>0\) and every kernel/radial sign. Put

\[
K(t,d)=a_*(E_-/2-28d^2)tG_2(t)
       +\tfrac34b_-(8-F_+)tG_1(t),
\]
\[
R(t,d)=[B_a+(c+7b_-d)t][B_a+(c-b_-d)t]^7.
\tag{31}
\]

The same monotonic phi comparison, with actual d instead of its lower
endpoint, and the nonnegative phase loss give
\(|J_a(q)|\le g(d)=\int_0^1R(t,d)[1-K(t,d)+K(t,d)^2/2]dt\).
Again the exponential is bounded before replacing it by a Taylor polynomial;
no monotonicity of that polynomial is assumed.

The full product has degrees at most18 in t and12 in d. The separated
expansion uses

\[
R(t,d)=\sum_{i=0}^8 h_i b_-^i t^i(B_a+ct)^{8-i}d^i,
\quad
(h_0,\ldots,h_8)=(1,0,-28,112,-210,224,-140,48,-7).
\tag{32}
\]

The first code route expands this and the d-orders0,2,4 of
\(1-K+K^2/2\). A distinct route multiplies eight literal bivariate
linear factors and keeps kernels in the unexpanded \(t^r(1-t)^n\)
basis. It compares the entire13x19 coefficient matrix, all13 ordinary
integrals, and all13 independently evaluated exact beta integrals.

Write \(g(d)=\sum_{j=0}^{12}g_jd^j\), and \(d=d_-+(d_+-d_-)x\).
Its translated coefficients and Bernstein controls are

\[
b_k=\sum_{j=k}^{12}g_j\binom jk d_-^{j-k}(d_+-d_-)^k,\qquad
V_i=\sum_{k=0}^i b_k\frac{\binom ik}{\binom{12}k}.
\tag{33}
\]

Thus \(g(d)=\sum_i V_i\binom{12}i x^i(1-x)^{12-i}\le\max_iV_i\)
on the whole CLOSED interval: the basis is nonnegative and sums to1.
Every coefficient of the Bernstein reconstruction and an independent
translation by repeated linear multiplication is checked. If the maximum
control is below the strict polar target, the entire box is excluded.
This uses the coupling in (5), not independently selectable E and T.

## 8. All necessary intersections and the whole closed cover

The root box uses FOUR coordinate intervals, in order \((a,E,u,w)\):

\[
[11/16,7/10]\times[0,23/5]\times[51/80,1]\times[0,23/40].
\tag{34}
\]

Insert the exact mass interval \([F_-,F_+]=[8,8]\) in each face leaf
before applying the five-coordinate necessary intersections below. No
five-dimensional tree or private projection file is a runtime input.

The w bound follows from \(E\ge8[(1-u)^2+w]\). Enclose necessary tuples
by four ordered iterations, using the current endpoints each time:

\[
U_+\gets\min(U_+,F_+/8),\quad U_-\gets\max(U_-,F_-/8-E_+/16),
\]
\[
F_-\gets\max(F_-,8U_-),\quad F_+\gets\min(F_+,8U_++E_+/2),
\]
\[
E_-\gets\max(E_-,2\max(0,F_--8U_+),8[(1-U_+)^2+W_-]),
\]
\[
W_+\gets\min(W_+,(F_+/8)^2-U_-^2,E_+/8-(1-U_+)^2).
\tag{35}
\]

All are necessary by (5), \(T,S,\Pi\ge0\), and \(|\mu|\le F/8\).
Since \(u\le1\), \((1-u)^2\) is minimized at its upper endpoint.
No convergence or feasibility converse is assumed. Strictly inverted
endpoints certify an empty box; the checker verifies monotonicity of every
enclosing intersection and its complete endpoints.

Afterward use

\[
T_- =\max\{0,E_--2F_++16U_-,(8-F_+)^2/8\},
\]
\[
T_+ =\min\{E_+-2\max(0,F_--8U_+),
                (F_+-7m-1)^2+7(m-1)^2\},\quad m=1/(1+B_a).
\tag{36}
\]

The lower bound uses (5) and Cauchy–Schwarz. For the radius upper bound,
the calculation in (10) at exact total F gives
\((F-7m-1)^2+7(m-1)^2\). Every used box has
\(F_-\ge37/5>7m+1\), checked exactly, so this expression is increasing
and F may be replaced by \(F_+\). The full per-a floor is retained.


## 9. Actual product loss from radial variance

Fix positive radii with sum F<=8, and a common upper bound R>=1 for them.
For 0<x<=R define

f(x)=x-1-(x-1)^2/(2R)-log x.

The exact derivative satisfies
R*x*f'(x)=(x-1)(R-x). It is nonpositive below1 and nonnegative above1,
and f(1)=0. Hence f(x)>=0 on the WHOLE interval(0,R]. Summing this
ordinary scalar inequality yields

log product_j r_j <= F-8-T/(2R),
product_j r_j <= exp(-(8-F)-T/(2R)).

This standard logarithmic/variance estimate is used as a new sufficient
threshold in the degree-nine cover; historical novelty for the scalar
estimate is not claimed.

On a tightened raw box let F in[F_-,F_+], T in[T_-,T_+], a<=a_+.
Set m=1/(1+a_+). The other seven floor bounds give
r_j<=F_+-7m. Also, with radial mean F/8 and radial centered variance
V=T-(F-8)^2/8, zero-sum Cauchy gives
(r_j-F/8)^2<=7V/8. Thus

r_j <= F_+/8 + sqrt((7/8)[T_+-(8-F_+)^2/8]).

The upper endpoint inside the square root is nonnegative on each paid
box. A fresh rational UPPER square root d with denominator4096 is checked
by d^2>=that endpoint. Take

R=max(1,min(F_+-7m,F_+/8+d)),
z=8-F_+ + T_-/(2R)>=0.

The complete positive exponential comparison e^z>=sum_(j=0)^4 z^j/j!
gives the rational upper bound

C_box = 1 / (1+z+z^2/2+z^3/6+z^4/24)
       >= product_j r_j.

The additional inequality product_j r_j >= |O_a(q)| holds for an
ACTUAL original disk polynomial by (4). It is not imposed on the formal
clipped tuple. Section11 instead pays the displacement from that actual
origin inequality before comparing with this clipped product cap.

All five terms, both scalar polynomial/Horner representations, both radius
caps, the root sign/square, and the FULL derivative coefficient identity
are checked. A favorable truncation of an upper expansion is not used:
the displayed finite sum is a LOWER bound on e^z, and its reciprocal is
therefore an UPPER bound on e^(-z). Every comparison has the correct sign.


## 10. Fresh complete closed mass-eight face

For any formal tuple with exact F=8 and r_j>=1/(1+a), the92 CLOSED
energy-entry rectangles in Section4 prove that |J|>2199/2200 forces E<23/5 and
u>57/80. Hence its (a,E,u,w) coordinates belong to the CLOSED root box
in (34). Formal tuples need not be realizable by original disk polynomials.

The compact [COVER.json](COVER.json) has156 strict rational parent cuts,
157 leaves,313 reachable CLOSED nodes, maximum depth13. Provenance is
the author's10322 tree with every marked cut translated by1/80:
\(a_{\rm new}=a_{\rm old}+1/80\), leaving all other axes fixed.
Its defining leaf roles are reselected using fresh payments. The final
explicit tree alone supplies continuum coverage; no ancestor tree or
private transport program is a runtime input.

Every final leaf has a nonempty necessary enclosure and a paid entire
radial product cap. The defining roles are141 retained-mean origin,
15 joint-E/T polar and1 standard polar. BOTH energy/joint whole channels
of ALL141 mean leaves are bounded, each keeping every centered order:
282 channels,1974 full9x10 remainder matrices,282 full10x10 cleared
matrices,282 degree8 and282 degree9 control vectors. All15 joint
13x19 matrices and their13 integrals/controls, and the whole standard
polar vector, are paid. For all141 origin and all16 polar leaves,
respectively,

\[
L_{\rm box}>C_{\rm box}+1/3100,
\qquad U_{\rm box}<1-1/2200.                              \tag{37}
\]

These are strict exact Fraction comparisons. L_box bounds |O| below,
C_box bounds the radial product P=product r_j above, and U_box bounds
|J| above. Both mean-energy polynomials are computed when that channel
is invoked; all coefficients and all degree-eight/nine Bernstein controls
are checked before selecting a lower bound. The E/T coefficient and
Bernstein representations are likewise whole matrices, not extrema-only
hashes. The inequality |O|<=P is licensed only for an ACTUAL original
disk polynomial, never silently assigned to a clipped formal tuple.

For an actual F=8, equations(4) give |J|>=1 and |O|<=P. Energy entry
places it in a final leaf. Either its origin or polar inequality in (37)
contradicts these channels. Thus actual mass-eight polynomials are excluded.
Section1a then proves F>8 for EVERY actual polynomial in the new interval,
including all lower masses. No older F<=8 exclusion is used here.

## 11. New positive gap by coupled clipping

Suppose for contradiction that F=8+Delta with
0<Delta<=epsilon:=1/10000. Put m_a=1/(1+a) and

\[
h_j=\frac{\Delta(r_j-m_a)}{F-8m_a},\qquad
q'_j=(1-h_j/r_j)q_j.
\tag{38}
\]

The denominator is positive, 0<=h_j<=r_j-m_a, sum h_j=Delta,
r'_j>=m_a and sum r'_j=8. Along q(v)=q'+v(q-q'), v in[0,1], every
radius is at least m=10/17, total mass at most S0=8+epsilon, and
sum|q_j-q'_j|=Delta. No intermediate or clipped tuple is assumed actual.

### 11a. Noncircular energy entry

Differentiating one factor of J leaves seven factors with radius sum
at most S0-m. Put sigma=(S0-m)/7. Triangle inequality and seven-factor
AM--GM give, for every slot and path point,

\[
|\partial_{q_k}J_a|
\le b_+\int_0^1t(h+b_+\sigma t)^7dt
=b_+\sum_{i=0}^7\binom7i\frac{h^{7-i}(b_+\sigma)^i}{i+2}<2/3.
\tag{39}
\]

Every term is compared with the independent exact antiderivative.
No energy or origin bound is used. Therefore

\[
|J(q')|\ge1-(2/3)\epsilon=1-1/15000>2199/2200.
\tag{40}
\]

The fresh92-rectangle entry now proves E'<23/5 and u'>57/80 BEFORE the
origin derivative is bounded. Thus q' belongs to the paid face.

### 11b. Coupled whole-path origin derivative

Let R=S0-7m. Every path radius is at most R. The full l1 displacement
and differentiation of squared norms imply

\[
u(v)\ge u_-:=57/80-\epsilon/8,\qquad
E(v)\le E_+:=23/5+2(R+1)\epsilon.
\tag{41}
\]

For x=at, exact expansion in each removed slot gives

\[
\sum_{j\ne k}|1-xq_j|^2
=7-16xu+x^2(E+16u-8)+2x\Re q_k-x^2|q_k|^2
\le8-16xu+x^2(E+16u-8).
\tag{42}
\]

The full last-slot contribution is at most
2x|q_k|-x^2|q_k|^2=1-(1-x|q_k|)^2<=1. Since x<=7/10<1,
the combined coefficient -16x+16x^2 of u is nonpositive. Use E_+ and
u_- in this SYNCHRONIZED expression before replacing marked endpoints;
do not incorrectly use u_- as an upper bound on the separate quadratic
coefficient E+16u-8. The result is

\[
\frac17\sum_{j\ne k}|1-atq_j|^2\le B(t),\qquad
B(t)=\frac{8-16(11/16)u_-t+(7/10)^2(8+2R\epsilon)t^2}{7},
\tag{43}
\]

because E_++16u_--8=8+2R epsilon exactly. The complete fresh rational
quadratic coefficient vector and degree2 Bernstein vector are

\[
(B_0,B_1,B_2)=
(8/7,-626989/560000,47604620119/85000000000),
\]
\[
(V_0,V_1,V_2)=
(8/7,653011/1120000,347056528333/595000000000).
\]

Expanding ALL three Bernstein terms reconstructs ALL three coefficients.
All V_i>0, so B is positive on the closed interval. Since B2>0, convexity
puts its maximum at an endpoint, and B(1)<B(0)=8/7. Thus0<B(t)<=8/7.
Here B'(1)=144434583/297500000000 is POSITIVE; the old decreasing-
quadratic argument is not used. The convex endpoint argument is the paid
replacement. Set c=107/100, with c^2>8/7. Squared-modulus AM-GM yields

\[
\prod_{j\ne k}|1-atq_j|\le B(t)^{7/2}\le cB(t)^3,
\qquad |\partial_{q_k}O_a|
\le9(7/10)c\int_0^1tB(t)^3dt<5/4.
\tag{44}
\]

The ENTIRE seven-coefficient cubic and its weighted integral are freshly
checked by two exact representations, retaining every signed coefficient.
Thus |O(q')-O(q)|<=(5/4)Delta on the entire path.

### 11c. Full product ratio and both contradictions

Write P=product r_j, P'=product r'_j. Since r'_j>=m, sum h_j=Delta,
eight-factor AM--GM gives

\[
P/P'\le\left(1+\frac{\Delta}{8m}\right)^8
\le A:=\left(1+\frac{\epsilon}{8m}\right)^8.
\tag{45}
\]

Since sum r'_j=8, P'<=1. Apply |O(q)|<=P ONLY to the actual original
tuple, and then the paid origin derivative:

\[
|O(q')|\le P'+(A-1)+(5/4)\epsilon,
\qquad (A-1)+(5/4)\epsilon<1/3100.
\tag{46}
\]

Every coefficient of the eighth power and its full value is checked
by binomial and literal-factor representations. On an origin leaf,
L_box>C_box+1/3100>=P'+1/3100 contradicts(46). On a polar leaf,
U_box<1-1/2200 contradicts(40). All shared cut faces and both marked
endpoints are covered. Combining this with Section1a proves(1).

## 12. Exact certificate and ordinary trust boundary

The local fixed tree, full coefficient/control comparisons, exact homothety
controls and both-endpoint channel/gradient fixtures are checked by
[verify.py](verify.py). See [README.md](README.md) for reproduction commands,
[EXPECTED.json](EXPECTED.json) for compact payments/counts and
[VALIDATION.json](VALIDATION.json) for complete validation evidence.

Communication, Gauss--Lucas, Hermite interpolation, centered/mean and
Bernstein arguments, homothety/convexity, clipping differentiation and
the published REAL Hilbert Banach norm identity are ordinary UNFORMALIZED
inputs, written above. Finite exact controls test representations;
they are not Lean formalization, historical priority or peer review.
