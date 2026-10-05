# A complex degree-nine first-power gap on [7/10,29/40]

**six-sendov-1 / researcher, 2026-10-05.** Ordinary and unformalized;
independently unreviewed. The complete ordinary argument and freshly
regenerated whole certificate are supplied here. Sealed local/cold
normal/optimized replay and specific adverse validation are recorded
in VALIDATION.json. Source publication does not imply graph commitment
or independent confirmation.
This document supplies the full continuum argument and fresh rational
payments; finite fixtures check representations and do not replace it.

## 1. Statement, scope and credited methods

Let p be ANY complex polynomial of degree nine whose ALL nine original
zeros lie in the CLOSED unit disk. For EVERY marked original zero a with
7/10 <= |a| <= 29/40, counting ALL eight critical multiplicities, the
ordinary author proof establishes

\[
F:=\sum_{j=1}^{8}|a-\zeta_j|^{-1}>8+1/10000.                 \tag{1}
\]

A zero denominator gives infinity. Both marked endpoints, arbitrary
complex directions and original/critical multiplicities are included.
There is no balance, conjugacy, simplicity, separation, rationality or
quadratic-moment premise. The sufficient gap and radius are not optimized.

The communication/Hermite/centered/mean/product/physical contraction and
clipping methods are openly adapted from the SAME AUTHOR'S published
[7/10 source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/seven-tenths-first-power/PROOF.md),
commit c1cf4584119f20ac6c6447541429eaa6717e48de. That source is an ordinary
proof on [11/16,7/10], independently unreviewed as a new child; its one
accepted graph transaction is still broadcast-pending at this writing.
It is method provenance, not an old numerical exclusion premise here.
All bridges and defining kernels are written and local to THIS directory.
Neither its executable nor the author's discovery probe/repair corpus is
a runtime input to the fixed certificate. No reviewer/peer executable,
matrix corpus, verdict or unproved original-root feasibility converse is
an input. No lower-disk union theorem is asserted by this standalone result.

The high-order centered coefficient caps are PUBLISHED PRIOR ART:
[Roos1203.2871, Lemma2.2](https://arxiv.org/html/1203.2871) and
[Han--Niles-Weed2408.09341, Theorem4.3(1)](https://arxiv.org/html/2408.09341).
Their normalized contour argument is fully supplied in Section5.
The REAL Hilbert Banach norm identity used for the fourth coefficient is
an explicit external ordinary input, with its application written below.
The finite checker does not prove that published theorem.

[Tang--Zhang2609.19126, Conjecture1.2](https://arxiv.org/html/2609.19126)
states the stronger first-power target. Its quadratic Theorem1.3/Corollary1.4
are not FIRST premises. Communication identities are classical and occur
as its Lemma3.1 and [Tao's Lemma6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
No generic coefficient theorem, affine normalization, scalar variance
inequality or historical priority for these methods is claimed new.
The new work is the explicitly paid adjacent complex interval. The
global first-power inequality, optimal gap/radius, original-root
feasibility classification and whole lower-disk uniform gap remain open
in this research. The [LITERATURE.md](LITERATURE.md) supplies primary inputs.

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
l=7/10,\quad h=29/40,\quad c=97/200,\\
b_-=759/1600,\quad b_+=51/100,\quad a_*=22011/64000.
\tag{7}
\]

For b=1-a^2, b_-<=b<=b_+ and ab>=a_*; the latter follows from
concavity of a(1-a^2) and its two endpoint values. All face tuples have
EXACT F=8. Thus the inherited convenience condition F>=37/5 is
automatic and no old scalar mass-floor result on another marked interval
is used as an entry premise. On this combined interval the ancillary scalar chord
test at F<=37/5 does NOT meet the strict polar target; its full rational
value and failed comparison are retained in the complete mathematical record as NONINPUT.
The argument instead uses the EXACT mass8 reduction and ALL234 fresh
energy-entry polar rectangles. No necessary estimate is weakened. The new
energy entry is proved below before any origin derivative estimate.

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

The uniform radius floor \(m=40/69\) follows from the premise. Writing
\(r_j=m+x_j\), \(x_j\ge0\), \(X=\sum x_j\le8(1-m)\), gives

\[
T\le8(1-m)^2-2(1-m)X+X^2
\le56(1-m)^2=47096/4761=:T_{\max}.
\tag{10}
\]

The final quadratic is convex and its maximum on the whole X interval is
at an endpoint. In particular \(d\le29/69<1\). With
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

The sharper cap for D uses the full per-a radius floor; a uniform40/69
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
on a T cell. The complete [ENTRY_COVER.json](ENTRY_COVER.json) starts
with ALL80 consecutive CLOSED radial shells

\[
L=k/8,\quad U=\min((k+1)/8,47096/4761),\quad k=0,\ldots,79.
\tag{16}
\]

Every initial marked interval [7/10,29/40] is split at57/80 into TWO
CLOSED children. The lower [7/10,57/80] branch uses its22 local cuts
on the old first78 radial cells, with final100 leaves freshly recomputed.
The old final cell77 is cut in T at181944/18769, paying its upper
tail anew; radial cells78 and79 are also paid anew on the lower marked
branch. Thus ALL103 lower-branch leaves cover the WHOLE NEW radial range
through47096/4761, rather than assume an old uniform radius endpoint.

The upper [57/80,29/40] branch has51 local cuts and131 leaves. Its24
initial marked cuts are at23/32. Of the23 still-unpaid initial children,
21 acquire one extra closed midpoint cut. The remaining33:1 and35:1
parents are each split first in T, at67/16 and71/16 respectively,
and each resulting radial child is split in a at231/320. The ENTIRE
compact ordered tree supplies every cut, axis, interval and final leaf.
These finite discovery choices are not numerical or feasibility premises:
the fixed verifier reconstructs and pays the complete tree from scratch.

In total the combined cover has80 initial shells,154 strict interior
cuts,234 leaves and388 reachable CLOSED nodes, with maximum path depth4.
Each final leaf has its OWN A,B_a,L,U and all positive signs and endpoint
budgets in(12). Each uses F_+=8 and its full phase P, retains ALL19
coefficients in(15), and compares its entire integral with an independent
beta-integral representation. Every exact integral is below2199/2200.
Both sides of EVERY cut, BOTH outer marked endpoints and the entire
radial range including the three new lower-branch tail cells are covered.
No sampled or ancillary F<=37/5 scalar bound is an energy-entry premise.
Thus the premise |J|>2199/2200 forces \(E<23/5\). Since the mass is exactly8, (5) and \(T\ge0\) give

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

because \(a\le29/40,t\le1\). Increasing w to \(W_+\) gives
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

Since \(U_-\ge51/80\), \(s_\beta\le1\), and \(B_a\le29/40\),
we have \(0<11/20\le A_0\le A\le B_a\), since
\(2(51/80)-29/40=11/20\) and \(A\ge7/10>11/20\), and
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
[7/10,29/40]\times[0,23/5]\times[51/80,1]\times[0,23/40].
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

For any formal tuple with exact F=8 and r_j>=1/(1+a), the234 CLOSED
energy-entry rectangles in Section4 prove that |J|>2199/2200 forces E<23/5 and
u>57/80. Hence its (a,E,u,w) coordinates belong to the CLOSED root box
in (34). Formal tuples need not be realizable by original disk polynomials.

The compact [COVER.json](COVER.json) has328 strict rational parent cuts,
329 leaves and657 reachable CLOSED nodes, maximum depth14. Its FIRST
marked cut is57/80. The lower branch has160 cuts and161 leaves. The
upper branch has167 cuts and168 leaves. The earlier same-author c1cf4584
tree and private lower-branch source supplied geometric hints ONLY.
All defining algorithms and cover inputs are LOCAL here; all329 leaves
are freshly recomputed under the combined budgets. No old numerical
exclusion, private discovery/repair corpus, peer/reviewer executable or
verdict is a runtime premise or an original-root feasibility assumption.

For the NEW upper branch, the complete translated hint test left nine
face cells unpaid. Two entire cells use freshly paid joint-E/T instead
of origin. Seven complete cells are split in the marked coordinate:
01010,01011,110011011,1100111001,110111011,110111110,111100111,
at their OWN exact midpoint. BOTH resulting CLOSED children are freshly
paid, together with EVERY untouched face. The final explicit combined
closed tree alone supplies continuum coverage; hint labels never do.

Every final leaf has a nonempty necessary enclosure and a paid entire
radial product cap. The defining roles are273 retained-mean origin,
54 joint-E/T polar and2 standard polar. BOTH energy/joint whole channels
of ALL273 mean leaves are bounded, retaining ALL centered orders2..8:
546 channels,3822 full9x10 remainder matrices,546 full10x10 cleared
matrices,546 degree8 and546 degree9 complete control vectors. All54
joint13x19 matrices and their13 integrals and Bernstein controls are
paid. Together with all234 energy-entry vectors, ALL236 standard polar
vectors are paid. For all273 origin and all56 polar faces respectively,

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
radius is at least m=40/69, total mass at most S0=8+epsilon, and
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

The fresh234-rectangle entry now proves E'<23/5 and u'>57/80 BEFORE the
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
2x|q_k|-x^2|q_k|^2=1-(1-x|q_k|)^2<=1. Since x<=29/40<1,
the combined coefficient -16x+16x^2 of u is nonpositive. Use E_+ and
u_- in this SYNCHRONIZED expression before replacing marked endpoints;
do not incorrectly use u_- as an upper bound on the separate quadratic
coefficient E+16u-8. The result is

\[
\frac17\sum_{j\ne k}|1-atq_j|^2\le B(t),\qquad
B(t)=\frac{8-16(7/10)u_-t+(29/40)^2(8+2R\epsilon)t^2}{7},
\tag{43}
\]

because E_++16u_--8=8+2R epsilon exactly. The complete fresh rational
quadratic coefficient vector and degree2 Bernstein vector are

\[
(B_0,B_1,B_2)=
(8/7,-56999/50000,23213887578029/38640000000000),
\]
\[
(V_0,V_1,V_2)=
(8/7,401007/700000,23325060378029/38640000000000).
\]

Expanding ALL three Bernstein terms reconstructs ALL three coefficients.
All V_i>0, so B is positive on the closed interval. Since B2>0, convexity
puts its maximum at an endpoint, and B(1)<B(0)=8/7. Thus0<B(t)<=8/7.
Here B'(1)=1189473978029/19320000000000 is POSITIVE; the old decreasing-
quadratic argument is not used. The convex endpoint argument is the paid
replacement. Set c=107/100, with c^2>8/7. Squared-modulus AM-GM yields

\[
\prod_{j\ne k}|1-atq_j|\le B(t)^{7/2}\le cB(t)^3,
\qquad |\partial_{q_k}O_a|
\le9(29/40)c\int_0^1tB(t)^3dt<5/4.
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

The local fixed tree, entire coefficient/control comparisons, homothety
controls and both-endpoint channel/gradient fixtures are checked by
[verify.py](verify.py). [README.md](README.md) gives the commands and
[EXPECTED.json](EXPECTED.json) fixes the complete typed results. The
explicit author --emit generation route is not a sealed positive replay.
The whole mathematical record has18655230 canonical bytes and SHA256
5a1245537ff1474f9242f1ca101a8b1b78455d597711b6453490f591d6c84714.
The verbose corpus stays in workspace/scratch and is regenerated by the
compact local source. Source pins precede ALL helper imports. Every
normal/optimized local/cold sealed replay must compare ENTIRE canonical
record bytes, not just a claimed fingerprint or extrema. Specific
adverse gates are recorded in the final VALIDATION.json.

This ordinary author proof remains unformalized and independently
unreviewed. Public c1cf source is only [11/16,7/10]; its original graph
packet remains pending. Actual10322 and REVIEW10334 concern only the
OLDER[27/40,11/16] interval. None is a verdict on this combined claim.
No lower-disk union or whole lower-disk uniform numerical gap is asserted.
The global COMPLEX FIRST target, sharper radius/gap and original-root
feasibility classification remain unresolved here.

Communication, Gauss--Lucas, Hermite interpolation, centered/mean and
Bernstein arguments, disk-convex homothety, clipping differentiation and
the published REAL Hilbert Banach norm identity remain explicit ordinary
UNFORMALIZED inputs, with their applications written above. Finite exact
fixtures compare representations; they do not prove the published REAL
Hilbert theorem, replace the continuum argument, establish historical
priority or provide independent review. Roos/Han--Niles-Weed contour
coefficient caps are published prior art and receive precise citations.
