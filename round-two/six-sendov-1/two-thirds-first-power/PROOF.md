# Complex degree-nine first-power inequality on the marked two-thirds disk

Actual author **six-sendov-1**, role **researcher**, 2026-10-04.
Complete ordinary analytic author proof with finite exact rational
sufficient inequalities; **unformalized and independently unreviewed**.
The unrestricted first-power conjecture and optimal marked radius remain
open in this work. The standard REAL Hilbert Banach norm identity is an explicit external
ordinary premise, credited in section5 below. No historical priority is
claimed for that premise, its quartic consequence or classical methods.
Classical communication, interpolation, Newton,
Cauchy–Schwarz, Maclaurin and Bernstein mechanisms are credited.

## 1. Statements and dependence

For a complex eight-tuple put

\[
r_j=|q_j|,\quad F=\sum r_j,\quad
\mu=\tfrac18\sum q_j=u+iv,\quad w=v^2,
\]
\[
T=\sum(r_j-1)^2,\quad E=\sum|q_j-1|^2,\quad
\Pi=F-8u,\quad S=\sum|q_j-\mu|^2.
\]
Define the two communication channels

\[
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt,\qquad
J_a(q)=\int_0^1\prod_j[a+(1-a^2)tq_j]\,dt.
\tag{1}
\]

**Channel lemma.** For every real \(a\in[13/20,2/3]\) and every
complex eight-tuple with \(r_j\ge1/(1+a)\), \(F\le8\), and
\(|J_a(q)|\ge1\),

\[
F>37/5,\quad E<23/5,\quad |\mu|\le1,\quad
u>51/80,\quad |O_a(q)|>10001/10000.
\tag{2}
\]

**Reusable closed dichotomy.** If \(a\in[13/20,2/3]\),
\(r_j\ge1/(1+a)\), \(37/5\le F\le8\), \(E\le23/5\), and
\(u\ge51/80\), then

\[
|J_a(q)|<99999/100000\quad\text{or}\quad
|O_a(q)|>10001/10000.
\tag{3}
\]

This retains both channels and their coupled moments; an energy ceiling
alone is not asserted to imply the origin conclusion. All complex directions
and repeated entries are allowed. No conjugacy, balance, equal-radius,
separation, or second-moment premise is imposed.

**Actual-polynomial theorem.** Every complex polynomial of degree nine
whose **all nine original zeros** lie in the closed unit disk satisfies

\[
\sum_{j=1}^8\frac1{|a-\zeta_j|}>8
\quad\text{at every marked zero }|a|\le2/3,
\tag{4}
\]

counting all eight critical multiplicities. A zero denominator means infinity.
Only the region \(|a|\le13/20\) invokes the author's
[thirteen-twentieths theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/thirteen-twentieths-first-power/PROOF.md),
source **e890a86e7e09756fd5223e221d91be80ba6dcf29**, LEMMA10216/0,
**bafkreif5mj5n5cws35bv7smlnn652pyzkm55z4czrgevjy5pj7qas4z52q**.
The new interval and all analytic bridges below are proved afresh. The
same-author checker architecture is credited and adapted, but the new
source imports no ancestor, scratch, reviewer or external executable.

Independent REVIEW10226/0, source
**d4d07d27e8aed6530597de3c05e15c6101530c5c**, confirms WHOLE10216
relative ONLY10170 and gives an additional first-power margin \(2^{-22}\)
ONLY on CLOSED[5/8,13/20]. That margin, reviewer code and any ancestor
verdict are not inputs to the new interval or a verdict on this extension.
The present new proof is independently unreviewed.

## 2. Exact coupling, affine envelope and scalar mass floor

Direct expansion gives

\[
E=T+2F-16u=T+2\Pi,\qquad
S=E-8[(1-u)^2+w]=T+2F-8-8(u^2+w).
\tag{5}
\]

For \(1/2\le l\le a\le h<1\), set \(c=l+1-l^2-h\). For
\(0\le x\le1\),

\[
h+cx-[a+(1-a^2)x]
=(1-x)(h-a)+x(a-l)(a+l-1)\ge0.
\tag{6}
\]

On the present full interval the exact budgets are

\[
l=13/20,\ h=2/3,\ c=673/1200,\\
b_-=5/9,\ b_+=231/400,\ a_*=10/27.
\tag{7}
\]

For \(b=1-a^2\), we have \(b_-\le b\le b_+\) and
\(ab\ge a_*\). The last bound follows from concavity of
\(a(1-a^2)\) and its endpoint values.

Triangle inequality and AM–GM give
\(|J_a(q)|\le\int_0^1[a+btF/8]^8dt\).
If \(F\le37/5\), use (6) with \(x=tF/8\le1\) and positivity to get

\[
|J_a(q)|\le\int_0^1[2/3+(673/1200)(37/40)t]^8dt
=\frac{249696043309681560348176317427447167201}
{253613523861504000000000000000000000000}<1.
\tag{8}
\]

This proves the mass floor in (2). The checker compares all nine binomial
coefficients and the complete integral with the antiderivative identity.
Every new scalar coefficient and endpoint budget is paid afresh;
the prior13/20 entry is not reused as an interval conclusion.

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

The uniform radius floor \(m=3/5\) follows from the premise. Writing
\(r_j=m+x_j\), \(x_j\ge0\), \(X=\sum x_j\le8(1-m)\), gives

\[
T\le8(1-m)^2-2(1-m)X+X^2
\le56(1-m)^2=224/25=:T_{\max}.
\tag{10}
\]

The final quadratic is convex and its maximum on the whole X interval is
at an endpoint. In particular \(d\le2/5<1\). With
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

The sharper cap for D uses the full per-a radius floor; a uniform3/5
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
on a T cell. Use all72 consecutive CLOSED cells

\[
L=k/8,\quad U=\min((k+1)/8,224/25),\quad k=0,\ldots,71,
\tag{16}
\]

the whole marked interval, \(F_+=8\), and this P. Every exact integral
in (15) is strictly less than1. The whole shell and its shared endpoints
are reconstructed in [verify.py](verify.py). It follows that \(E<23/5\)
under the channel premise. By (5), \(T\ge0\), and (8),

\[
u\ge F/8-E/16>37/40-23/80=51/80,\qquad |\mu|\le F/8\le1.
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

The coefficients in (21) are first derived by that recurrence. Retain
six of them, and replace ONLY the fourth coefficient by \(c_4=3/16\),
as follows. No later Newton coefficient is silently reoptimized.

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
for the quartic estimate is not asserted. All final constants are therefore

\[
(c_2,\ldots,c_8)=
(1/2,151/512,3/16,1497/5120,7/128,363/65536,1/4096).
\tag{21a}
\]

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

because \(a\le2/3,t\le1\). Increasing w to \(W_+\) gives
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

Since \(U_-\ge51/80\), \(s_\beta\le1\), and \(B_a\le2/3\),
we have \(0<73/120\le A_0\le A\le B_a\) and
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

The root box in coordinate order \((a,E,F,u,w)\) is

\[
[13/20,2/3]\times[0,23/5]\times[37/5,8]
\times[51/80,1]\times[0,23/40].
\tag{34}
\]

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

[COVER.json](COVER.json) gives **514 exact internal cuts and515 leaves**,
a complete **1029-node** binary tree of depth at most18. Each cut is the
recorded rational midpoint of one tightened parent axis, strictly inside
the ORIGINAL raw parent. Both children retain the full raw parent in every
other coordinate and are CLOSED with a shared boundary. Their union is
the whole raw parent. Every path/type, midpoint identity, nondegeneracy,
child and reachable node is checked; no tightened complement is omitted.

Every leaf is nonempty at the necessary-enclosure level and is paid by
its defining sufficient inequality, independently of estimate priority:

- **213** scalar-origin leaves have \(D-R>10001/10000\).
- **27** mean-polynomial origin leaves have a whole-u lower bound
  \(>10001/10000\) from sections6a/6b. BOTH energy/joint channels are
  recomputed; all54 are bounded here, with no omitted centered term.
- **57** standard-polar leaves have \(\mathcal J<99999/100000\).
- **218** E/T-polar leaves have \(\max_iV_i<99999/100000\).

The least defining origin lower bound is exactly

\[
\frac{74117852712486533992975193817572860819}{74102076198407683540883865600000000000}>10001/10000.
\tag{37}
\]

All515scalar-origin payments are checked, including polar and mean-polynomial
leaves. The complete finite comparisons comprise3605centered scalar vectors,
347ordinary19-coefficient polar vectors (72entry+275leaf attempts),
2834full E/T19-coefficient vectors and218whole13-entry integral/control
vectors;378full9x10mean coefficient matrices,54whole nine-control vectors
and54whole ten-control vectors. Unsuccessful standard-polar attempts on
the218E/Tleaves are compared but are not falsely called exclusions.
The source uses ONE final3/16quartic amplitude throughout. Displayed extrema
and[EXPECTED.json](EXPECTED.json) summarize defining exact checks;
the fingerprint is computed only after every whole comparison and inequality.

This proves (3). Under the channel premise, (8), (16), and (17) put the
tuple in (34); the polar alternatives contradict \(|J_a(q)|\ge1\),
so (2) follows. No energy-only origin theorem has been substituted.

## 9. Actual original polynomials and every multiplicity

For \(|a|\le13/20\), invoke only the explicitly credited LEMMA10216/0.
For \(13/20<|a|\le2/3\), a marked multiple zero has a critical point
at the same location and gives infinity. Otherwise rotate to real a,
normalize to monic, and write

\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\quad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\quad q_j=(a-\zeta_j)^{-1}.
\]

All q are finite and nonzero; all original and critical multiplicities
are counted. Integrating p' from a to0 and to1/a gives the classical
communication identities

\[
O_a(q)=\prod_j z_jq_j,\qquad
J_a(q)=\prod_j\frac{1-az_j}{a-z_j}.
\tag{38}
\]

For the first, use \(p(0)=-a\prod z_j\) and
\(p'(a)=9\prod1/q_j\). For the second, divide the integral by
\((1/a-a)p'(a)\); its normalized derivative factors are
\([a+(1-a^2)tq_j]/a\), and use
\(p'(a)=\prod(a-z_j)\). Simplicity of the marked zero ensures
\(a-z_j\ne0\).

Since all original zeros lie in the closed disk,
\(|O_a(q)|\le\prod r_j\) and \(|J_a(q)|\ge1\), the latter because
\(|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0\).
Gauss–Lucas gives \(|\zeta_j|\le1\), so \(r_j\ge1/(1+a)\).
If the first-power sum were at most8, AM–GM would give
\(\prod r_j\le(F/8)^8\le1\). The channel lemma contradicts this with
\(|O_a(q)|>10001/10000>1\). This proves (4), including closed endpoints
and all multiplicities. The relaxed tuple conditions have no asserted
converse to actual all-original disk feasibility.

## 10. Evidence and limits

The new application extends the actual complex marked radius from13/20
to2/3. Its decisive additional estimate keeps the real mean in both the
centered energy polynomial and the ACTUAL norm denominator; all nine/ten
Bernstein controls pay the entire mean interval. The centered fourth
amplitude3/16 uses the explicitly stated published REAL Hilbert Banach
premise, not a finite-check claim of that theorem. Other six amplitudes
and all seven centered orders remain. The full E/T phase dependence and
per-a radial floors are retained, with all new entry constants paid afresh.

The standard-library checker uses unbounded integer/Fraction arithmetic,
exact square-root rounding and full finite polynomial comparisons.
Whole local/cold normal/optimized replays and meaningful semantic, typed
expected-record, cut and source-byte rejections are reported in
[VALIDATION.json](VALIDATION.json). Separate literal Gaussian controls
check full origin products and the quartic variance identities; no actual
all-original-root feasibility is inferred from those controls. SAME-AUTHOR
cross-method checking is not independent review or formalization.

Every continuum/channel/interpolation/Hilbert-space and inequality bridge
above is ordinary and unformalized. There is no solver or floating-point
premise, reviewer executable, omitted defining input or graph-verdict
transport. All defining source and rational cuts are compact/public; the
bulky regenerated coefficient record and exploratory histories remain private.
Earlier time/depth-limited partial trees and their mixed-amplitude records
were followed by one complete final-source replay; no resource limit or
incomplete search was treated as mathematical nonexistence. The unrestricted
first-power endpoint, optimal marked radius, optimal constants and a numeric
uniform first-power margin above8 for the whole marked disk are not claimed.
Historical priority for the analytic mechanisms is not asserted.
