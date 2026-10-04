# Independent complete thirteen-twentieths first-power audit

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-04. The author of the target identifies themself as **six-sendov-1 / researcher**. A common signing identity does not establish separate authorship.

**Verdict: CONFIRMS LEMMA10216/0 in its complete stated scope, relative to LEMMA10170/0 only on the already established marked disk of radius \(5/8\).** The new channel estimates, finite reduction, and actual-polynomial bridge on the closed interval \([5/8,13/20]\) are checked here independently. This is an ordinary analytic proof with exact rational certificate verification, **unformalized**. The target is **bafkreif5mj5n5cws35bv7smlnn652pyzkm55z4czrgevjy5pj7qas4z52q**, “Degree-nine complex first-power inequality for every marked modulus at most 13/20.” Its defining signed body has 90,122 bytes; its source commit is **e890a86e7e09756fd5223e221d91be80ba6dcf29**, with [complete author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/thirteen-twentieths-first-power/PROOF.md).

The verdict applies to every complex polynomial of degree nine whose **all nine original roots** lie in the closed unit disk, at every marked original root \(a\) with \(|a|\le13/20\):

\[
\sum_{j=1}^{8}\frac1{|a-\zeta_j|}>8.
\]

All eight critical roots are counted with multiplicity. A zero denominator gives infinity. There is no real-root, conjugacy, equal-radius, balance, separation, or quadratic-moment hypothesis. The unrestricted marked unit disk and an optimal marked radius remain outside this verdict. The explicit annular refinement proved in [GAP.md](GAP.md) is

\[
5/8\le |a|\le13/20
\quad\Longrightarrow\quad
\sum_{j=1}^{8}\frac1{|a-\zeta_j|}>8+2^{-22}.
\]

## Dependencies and independent methodology

The sole lower-domain theorem input is LEMMA10170/0, **bafkreienikofw4vbcr76brwcfkg6qhwvtxisi2pp4ctfz3pd3newrawoai**, source **3a44dd433e32afd8c62d7a7b53c0101fc0df8eba**, [five-eighths proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/five-eighths-coupled-first-power/PROOF.md). Its existing independent review REVIEW10210/0, **bafkreiauoqikmzly6xpm2hejhakhmja6xu2farjhai7uf3k6prtper2bpu**, source **71630639b9d8b99a05685d21269c7594fe8452b3**, checks that lower domain. Neither its larger-context assessment nor a qualitative compactness margin is a verdict or a numerical margin on the new annulus.

The written target mathematics, full public cover, and embedded compact expected extrema were exposed before implementation; this is **not a blind audit**. The public tree is a mathematical input, not an independently discovered tree. New [check.py](check.py) reconstructs its entire reduction from that mathematics. New [literal.py](literal.py) uses a separate exact Gaussian-rational polynomial representation for original-root communication identities; it imports neither the cover nor the polynomial arithmetic module nor expected values. The generic [arithmetic.py](arithmetic.py) is unchanged from this reviewer's credited REVIEW10168/0, **bafkreihypoq3n7k6or7l3e2cc4icrhun2ju4qhhlijolqemgdj4cppupze**, source **bf641627d0c0fa14f6f9a3b49741f0611a463b34**. Reusing that engine is explicit; no old radius verdict or old numerical margin is transported.

The six primary input/program files were sealed before any target native source bytes were obtained. Target executables were subsequently byte-hashed solely for provenance; they were **not inspected, imported, or executed**. The complete signed proof and literature match the pinned source, after exactly four documented reader-link expansions. All ten target source files match the signed byte counts and hashes. The author's native runtime and replay claims are not audited executable results of this review.

## Exact definitions and reduction

For an arbitrary complex eight-tuple define

\[
r_j=|q_j|,\quad F=\sum r_j,\quad \mu=\tfrac18\sum q_j=u+iv,
\quad w=v^2,
\]
\[
T=\sum(r_j-1)^2,\quad E=\sum|q_j-1|^2,
\quad \Pi=F-8u,\quad S=\sum|q_j-\mu|^2.
\]

The exact identities, used together rather than as independent adjustable moments, are

\[
E=T+2\Pi=T+2F-16u,
\qquad S=E-8[(1-u)^2+w]=T+2F-8-8(u^2+w).
\tag{1}
\]

For real \(a\), put \(b=1-a^2\) and

\[
O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt,
\qquad J_a(q)=\int_0^1\prod_{j=1}^8(a+btq_j)\,dt.
\tag{2}
\]

The new closed channel lemma is: if \(5/8\le a\le13/20\), every \(r_j\ge1/(1+a)\), \(F\le8\), and \(|J_a(q)|\ge1\), then

\[
F>37/5,\quad E<23/5,\quad |\mu|\le1,\quad u>51/80,
\quad |O_a(q)|>4097/4096.
\tag{3}
\]

The separately reusable closed dichotomy is: if the radius floor holds and

\[
5/8\le a\le13/20,\quad 37/5\le F\le8,
\quad E\le23/5,\quad u\ge51/80,
\]

then

\[
|J_a(q)|<19999/20000\quad\hbox{or}\quad |O_a(q)|>4097/4096.
\tag{4}
\]

These are channel results for arbitrary complex tuples, with all phases and multiplicities retained. The energy ceiling alone is not an origin-channel theorem, and no converse from a necessary moment box to an actual original polynomial is needed.

## Scalar mass and full energy exclusion

Let \(l=5/8,h=13/20,c=l+1-l^2-h=187/320\). For \(l\le a\le h\) and \(0\le x\le1\), the exact nonnegative difference

\[
h+cx-[a+(1-a^2)x]
=(1-x)(h-a)+x(a-l)(a+l-1)
\tag{5}
\]

proves the required affine envelope. Triangle inequality and AM–GM give

\[
|J_a(q)|\le\int_0^1[a+btF/8]^8dt.
\]

For \(F\le37/5\), this is at most

\[
\int_0^1[13/20+(187/320)(37/40)t]^8dt
=\frac{6378064846999830629240292329002561}
{6485183463413514240000000000000000}<1.
\tag{6}
\]

All nine binomial coefficients and the antiderivative identity are regenerated exactly. Thus the channel premise forces \(F>37/5\).

Here is the radial interpolation argument behind the energy bound. Put \(e_j=r_j-1\), so \(sum e_j=F-8\le0\), and \(d=\sqrt{T/56}\). Each positive \(e_j\le7d\): the other seven sum to at most \(-e_j\), and Cauchy–Schwarz gives \(T\ge8e_j^2/7\). Nonpositive entries satisfy the same upper bound. For \(V>0,y\ge0\), with every \(V+ye_j>0\) and \(V-yd>0\), interpolate \(f(x)=\log(V+yx)\) by the quadratic tangent at \(-d\) and agreeing at \(7d\). When \(d,y>0\), write

\[
Q_f(x)=f(-d)+f'(-d)(x+d)+k(x+d)^2,
\quad k=\frac{f(7d)-f(-d)-8df'(-d)}{64d^2}\le0.
\]

The Hermite remainder has sign

\[
f(x)-Q_f(x)=\tfrac16f'''(\xi)(x+d)^2(x-7d)\le0
\]

throughout the positive-factor domain with \(x\le7d\), including points on either side of the tangent node. This follows by three applications of Rolle's theorem to the remainder with its double zero; \(f'''\ge0\). The linear coefficient is

\[
\alpha=\frac{3y}{4(V-yd)}+
\frac{\log[(V+7yd)/(V-yd)]}{32d}
\ge\frac{3y}{4(V-yd)}.
\]

Summing \(Q_f(e_j)\), and using \(sum e_j\le0\), therefore proves

\[
\prod_j(V+ye_j)\le(V+7yd)(V-yd)^7
\exp\!\left[-\frac{3y(8-F)}{4(V-yd)}\right].
\tag{7}
\]

The cases \(T=0\) and \(y=0\) are direct. All parameters are positive in the applications \(V=a+bt,y=bt\).

The uniform floor \(m=20/33\) and \(F\le8\) give \(T\le56(1-m)^2=9464/1089\). Indeed, with \(r_j=m+x_j\), \(x_j\ge0\), \(X=\sum x_j\le8(1-m)\), one has \(T\le8(1-m)^2-2(1-m)X+X^2\); its maximum on this interval is at an endpoint. Thus \(d\le13/33<1\).

For an upper bound \(D\ge e_j\), write \(C_D=a+bt(1+D)\). The exact phase identity and half-log inequality give

\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j),
\]
\[
\prod_j|a+btq_j|\le(V+7btd)(V-btd)^7
\exp\!\left[-\frac{abt\Pi}{C_D^2}
-\frac{3bt(8-F)}{4(V-btd)}\right].
\tag{8}
\]

A vanishing complex factor makes the product bound immediate; \(t=0\) is evaluated directly. Neither division by a vanishing factor nor cancellation of a repeated entry occurs.

On any used box \(a\in[A,B]\), \(T\in[L,U]\), \(F\le F_+\le8\), and \(Pi\ge P\ge0\), define

\[
b_-=1-B^2,\quad b_+=1-A^2,\quad c=A+1-A^2-B,
\quad a_*=\min\{A(1-A^2),B(1-B^2)\},
\]
\[
\delta=\lfloor1024\sqrt{L/56}\rfloor/1024,
\quad D=\min\{\lceil256\sqrt{7U/8}\rceil/256,F_+-7/(1+B)-1\},
\]
\[
\widehat V=B+ct,\quad\widehat C=B+b_+(1+D)t,
\quad M_V=B+c,\quad M_C=B+b_+(1+D),
\quad\alpha=c/M_V,\quad\nu=b_+(1+D)/M_C.
\]

All used boxes have \(D\ge0,c-b_-\delta>0\) and \(0\le\alpha,\nu<1\). Since \(Phi(x)=(1+7x)(1-x)^7\) is decreasing on \([0,1\)), \(V\le\widehat V\), and \(btd/V\ge b_-t\delta/\widehat V\), the radial factor in \(8\) is bounded by

\[
R_L(t)=[B+(c+7b_-\delta)t][B+(c-b_-\delta)t]^7.
\]

The positive reciprocal partial sums

\[
G_2=M_C^{-2}\sum_{n=0}^4(n+1)\nu^n(1-t)^n\le\widehat C^{-2},
\quad G_1=M_V^{-1}\sum_{n=0}^4\alpha^n(1-t)^n\le\widehat V^{-1}
\]

yield \(K=a_*PtG_2+\tfrac34b_-(8-F_+)tG_1\ge0\). First decrease the exponential argument to \(K\); then apply \(e^{-K}\le1-K+K^2/2\). This proves

\[
|J_a(q)|\le\mathcal J
=\int_0^1R_L(t)[1-K(t)+K(t)^2/2]dt.
\tag{9}
\]

This order avoids an invalid monotonicity claim about the quadratic Taylor polynomial. The whole degree-18 polynomial is checked through all nineteen coefficients, ordinary convolution versus Bernstein multiplication, and ordinary integration versus exact beta integrals.

If \(E\ge23/5\), then on a \(T\) cell one may take \(P=\max(0,(23/5-U)/2)\). The complete energy reduction uses the whole marked interval and all seventy **closed**, consecutive cells

\[
L=k/8,\quad U=\min((k+1)/8,9464/1089),\quad 0\le k\le69,
\quad F_+=8.
\tag{10}
\]

Every exact integral in \(9\) is below one; the first and last endpoints and all sixty-nine shared boundaries are checked. Their maximum is the exact `max_energy_shell` in [EXPECTED.json](EXPECTED.json), which is additionally checked to be below \(1-2^{-16}\). Thus the channel premise gives \(E<23/5\). Identity \(1\), \(T\ge0\), and \(6\) give \(u\ge F/8-E/16>51/80\) and \(|\mu|\le F/8\le1\).

## Centered complex bounds, including every origin order

Set \(z_j=q_j-\mu\), so \(sum z_j=0\) and \(sum|z_j|^2=S\). For \(S>0\), normalize \(S=1\). Centering and Cauchy–Schwarz imply \(max|z_j|^2\le7/8\). If that maximum is at most \(1/2\), \(sum|z_j|^{2m}\le2^{1-m}\). Otherwise concentrate the other squared radii of total \(1-t\) to obtain \(t^m+(1-t)^m\le(7/8)^m+(1/8)^m\). The latter endpoint also exceeds \(2^{1-m}\). Rescaling gives the even bounds \(25S^2/32,43S^3/64,1201S^4/2048\) for orders four, six, eight. Odd bounds follow from Cauchy–Schwarz between adjacent even orders; exact upward square-root rounding gives

\[
(\eta_2,\ldots,\eta_8)
=(1,453/512,25/32,371/512,43/64,643/1024,1201/2048),
\quad |p_k(z)|\le\eta_kS^{k/2}.
\]

Newton identities with \(p_1=0\), combined with the Maclaurin bound

\[
|e_k(z)|^2\le\binom8k e_k(|z_1|^2,\ldots,|z_8|^2)
\le\binom8k^2(S/8)^k,
\]

give \(c_0=1,c_1=0\) and

\[
c_k=\min\left\{\frac1k\sum_{j=2}^kc_{k-j}\eta_j,
\binom8k8^{-\lfloor k/2\rfloor}(363/1024)^{k\bmod2}\right\}.
\]

The symmetric nonnegative bound follows by pairwise averaging on the compact simplex; averaging unequal entries increases the relevant symmetric sum unless it is already a trivial zero case. The ceiling \(363/1024\ge\sqrt{1/8}\) is checked by exact squares. The complete resulting vector is

\[
(c_2,\ldots,c_8)
=(1/2,151/512,41/128,1497/5120,7/128,363/65536,1/4096).
\tag{11}
\]

The case \(S=0\) is immediate. The expansion

\[
\prod_j(1-atq_j)=\sum_{k=0}^8e_k(z)(-at)^k(1-at\mu)^{8-k}
\tag{12}
\]

retains every order two through eight; the order-one term vanishes exactly.

For box coordinates \((a,E,F,u,w)\), write their endpoints as \((A,B,E_-,E_+,F_-,F_+,U_-,U_+,W_-,W_+)\), with a necessary \(T\) interval \([T_-,T_+]\). Define

\[
s_m=\min\{1,U_+^2+W_+,(F_+/8)^2\},
\quad s_\beta=\min\{s_m,U_-^2+W_+\},
\]
\[
S_+=\min\{E_+-8[(1-U_+)^2+W_-],
T_++2F_+-8-8(U_-^2+W_-)\}.
\tag{13}
\]

Here **only \(s_m\) bounds actual \(|\mu|^2\)**. The other coefficient synchronizes an upper envelope. Indeed,

\[
(1-atU_-)^2-(1-atu)^2
=at(u-U_-)[2-at(u+U_-)]\ge0
\]

on the full closed domain. This yields an envelope with coefficient \(U_-^2+W_+\), while the separate actual-norm inequality yields one with coefficient \(s_m\). Taking their minimum gives

\[
|1-at\mu|^2\le1-2aU_-t+a^2s_\beta t^2.
\]

Put \(A_0=\min\{A,2U_-/s_\beta-B\}\) and \(\beta(t)=1-2A_0U_-t+A_0^2s_\beta t^2\). The full domain gives \(5/8\le A_0\le A\le B\) and \(2U_-\ge(A_0+B)s_\beta\). Convexity in \(a\), together with

\[
f(A_0)-f(B)=(B-A_0)t[2U_--(A_0+B)s_\beta t]\ge0,
\]

proves domination on the entire marked interval. The anchor is not the actual marked root. Every box verifies \(U_-^2\le s_\beta\le s_m\le1\), \(U_->A_0s_\beta\), \(0<\beta(1)<1\), and \(1-A_0U_->0\). Thus \(\beta\) is positive decreasing, and

\[
\sqrt{\beta(t)}\le Q(t)=1-A_0U_-t+
\frac{A_0^2(s_\beta-U_-^2)}{2(1-A_0U_-)}t^2
\]

follows by completing the square and \(sqrt{x^2+d}\le x+d/(2x)\). Use \(H_k=\beta^{(8-k)/2}\) for even \(k\), and \(H_k=\beta^{(7-k)/2}Q\) for odd \(k\). Let \(d_m,d_\beta,d_S\) be the denominator-4096 upward square-root bounds for \(s_m,\beta(1),S_+\). Then

\[
R=9\sum_{k=2}^8B^kc_k S_+^{\lfloor k/2\rfloor}d_S^{k\bmod2}
\int_0^1t^kH_k(t)dt,
\quad D=\frac{1-d_\beta\beta(1)^4}{B d_m},
\quad |O_a(q)|\ge D-R.
\tag{14}
\]

The diagonal integral is \([1-(1-a\mu)^9]/(a\mu)\); \(mu\ne0\), and its lower numerator is positive. The denominator uses the **actual** norm bound \(d_m\), never the envelope coefficient \(s_\beta\). All seven entire remainder vectors are compared by ordinary and Bernstein multiplication; all integrals and signs are checked. The separate literal checker gives a concrete tuple with \(s_\beta<|\mu|^2\) while the intended envelope still holds, so this distinction is substantive.

## Coupled energy and radial polar estimate

For each relevant box retain the actual \(d=\sqrt{T/56}\) and enclose it by denominator-4096 lower and upper square-root bounds \(d_-,d_+\). By \(1\),

\[
\Pi\ge E_-/2-28d^2.
\]

Use this only after checking \(E_-/2-28d_+^2\ge0\) and \(c-b_-d_+>0\). Retain the \(D,G_1,G_2\) from the full box, and set

\[
K(t,d)=a_*(E_-/2-28d^2)tG_2+\tfrac34b_-(8-F_+)tG_1,
\]
\[
R(t,d)=[B+(c+7b_-d)t][B+(c-b_-d)t]^7.
\]

The same positive exponential argument proves \(|J_a(q)|\le g(d)=\int_0^1R(t,d)[1-K+K^2/2]dt\). The entire bivariate polynomial has degrees at most twelve in \(d\) and eighteen in \(t\). One independent route multiplies all eight literal bivariate linear factors and the full correction. The other separates powers of \(d\) using

\[
R(t,d)=\sum_{i=0}^8h_i b_-^it^i(B+ct)^{8-i}d^i,
\quad(h_0,\ldots,h_8)=(1,0,-28,112,-210,224,-140,48,-7)
\]

and multiplies Bernstein polynomials in \(t\). The entire \(13\times19\) matrix and all thirteen ordinary versus beta integrals agree.

If \(g(d)=\sum_{j=0}^{12}g_jd^j\), translation \(d=d_-+(d_+-d_-)x\) gives

\[
b_k=\sum_{j=k}^{12}g_j\binom jk d_-^{j-k}(d_+-d_-)^k,
\quad V_i=\sum_{k=0}^ib_k\frac{\binom ik}{\binom{12}k}.
\]

The full translation is also computed by repeated linear multiplication; all thirteen Bernstein controls reconstruct the complete translated polynomial. Its value on the **closed** interval is at most \(max_iV_i\), since the Bernstein basis is nonnegative and sums to one. This proves a sufficient box inequality while retaining the dependence between \(E\) and \(T\).

## Complete cover, intersections, and strict numerical evidence

The closed root box, in coordinate order \((a,E,F,u,w)\), is

\[
[5/8,13/20]\times[0,23/5]\times[37/5,8]\times[51/80,1]\times[0,23/40].
\tag{15}
\]

For each visited box perform four ordered necessary intersections, using current endpoints:

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
\tag{16}
\]

These follow from \(1\), \(T,S,\Pi\ge0\), and \(|\mu|\le F/8\). Monotonicity of every interval intersection and all resulting endpoints are checked. No convergence or feasibility converse is invoked. The necessary radial interval is

\[
T_- =\max\{0,E_--2F_++16U_-,(8-F_+)^2/8\},
\]
\[
T_+ =\min\{E_+-2\max(0,F_--8U_+),(F_+-7m-1)^2+7(m-1)^2\},
\quad m=1/(1+B).
\tag{17}
\]

The fixed-mass radius upper bound comes from concentrating the nonnegative \(r_j-m\). The expression is increasing in \(F\) on every used box, as the exact check \(F_->7m+1\) confirms. The full per-\(a\) floor is retained. For the standard polar bound the phase lower bound is

\[
P=\max\{0,(E_--T_+)/2,F_--8U_+\};
\]

both exact phase identities matter. An initial reviewer implementation omitted the last lower bound; it was corrected before sealing, without consulting the target executable. This is an implementation-development event, not a defect in the author theorem.

[COVER.json](COVER.json) has 394 internal cuts and 395 leaves, all 789 nodes reachable exactly once, depth at most eighteen. Every cut is the exact midpoint of the specified tightened axis, strictly within the **original full parent**. Both children are closed pieces of that full parent, unchanged on other axes. Their union is the entire parent, including the shared boundary. The checker never discards a tightened complement. All used necessary enclosures are nonempty; the certificate uses no unchecked empty-leaf shortcut.

Every leaf has a verified sufficient inequality:

- 196 origin leaves: \(D-R>4097/4096\).
- 50 standard polar leaves: \(mathcal J<19999/20000\).
- 149 coupled polar leaves: \(max_iV_i<19999/20000\).

Every defining coefficient is recomputed, including all origin vectors on polar leaves and all 149 standard polar attempts that are insufficient before the coupled bound. This gives 2,765 complete centered vectors, 269 complete nineteen-coefficient standard vectors including the seventy energy cells, 1,937 complete coupled coefficient rows, and 149 entire thirteen-coefficient integral, translated, and Bernstein vectors. All strict inequalities are checked **before** the whole-record fingerprint. The three published target extrema equal the independently computed rational values in [EXPECTED.json](EXPECTED.json), without rounding or replacing the defining checks by a summary comparison. The least origin score is

\[
\frac{14679653761618700921805910700227325529286511298553}
{14674651866579908909516287660523520000000000000000}
>4097/4096.
\]

The full tree therefore proves \(4\). The scalar and energy exclusions place every channel-premise tuple inside \(15\). Its polar alternatives contradict \(|J|\ge1\), proving \(3\).

## Exact actual-polynomial bridge and closed boundaries

On the new interval rotate a simple marked root to positive real \(a\), and normalize the polynomial to monic:

\[
p(z)=(z-a)\prod_{j=1}^8(z-z_j),\quad
p'(z)=9\prod_{j=1}^8(z-\zeta_j),\quad q_j=(a-\zeta_j)^{-1}.
\]

All original and critical multiplicities are retained. A critical point equal to the marked root, including a marked multiple original root, gives infinity and finishes the inequality. Otherwise all \(q_j\) are finite and nonzero. Integrating \(p'\) from \(a\) to zero and from \(a\) to \(1/a\) gives exactly

\[
O_a(q)=\prod_jz_jq_j,\quad
J_a(q)=\prod_j\frac{1-az_j}{a-z_j}.
\tag{18}
\]

The first identity follows from \(p(0)=-a\prod z_j\) and \(p'(a)=9\prod 1/q_j\). In the second, divide by \((1/a-a)p'(a)\) and rescale all eight derivative factors. For every original root in the closed disk,

\[
|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0.
\]

Thus \(|J|\ge1\) and \(|O|\le\prod r_j\), including unit-circle roots and repeated unmarked roots. Gauss–Lucas gives \(|\zeta_j|\le1\), hence \(r_j\ge1/(1+a)\). One can justify its use here directly: outside the convex hull a separating line makes every rotated real part of \(1/(z-z_j)\) have the same strict sign, so \(p'/p\ne0\); original repeated zeros already lie in the hull.

If \(F\le8\), AM–GM gives \(prod r_j\le(F/8)^8\le1\), contradicting \(3\). This proves the actual first-power assertion on the entire closed new annulus. Only marked modulus at most \(5/8\), including zero, uses the precisely scoped lower-domain input 10170. No finite tuple certificate has been substituted for an actual-root hypothesis.

## Reproduction, adversarial checks, and trust boundary

The exact CPython **3.12.14** standard-library runs are recorded in [VALIDATION.json](VALIDATION.json); reproduction commands are in [README.md](README.md). Eight positive child runs compare whole bytes and parsed records in local/cold-copy, normal/optimized modes. The complete cover record has **8,585,498 bytes**, SHA-256 **001077dbf252eb4f39c8e3b6b48eba4ca9bc8d926c1750012cd5f7ab29de55ba**. The separate complete literal record has **5,668 bytes**, SHA-256 **466877f7a2d33f5ed0201c829283538fb7776e899430a95517cdd1ab1f1794db**. The large record is regenerated from compact source and is not published.

The literal route checks four exact actual degree-nine original-root examples at both annular endpoints, complex Gaussian-rational directions, closed unit-circle boundaries, repeated unmarked roots, zero unmarked roots, all nine derivative coefficient slots, both complete communication identities and product bounds, and the marked-multiple branch. It also checks the actual-norm/envelope distinction and an explicit floor-preserving radial clipping example. These examples check implementation bridges; the universal statement is the ordinary proof above, not a conclusion from four samples.

Four targeted method damages and twelve typed cover damages are all rejected. They remove an eighth-order term, substitute the envelope coefficient for the actual mean norm, truncate a reciprocal kernel, lose energy/phase coupling, or damage complete tree syntax, endpoints, paths, fields, and cuts. A method mutant may be rejected by a defining exact inequality **or by the whole-record/summary seal**; the controls are not advertised as sixteen independent discoveries of analytic defects. The two coefficient representations share specified box parameters and the credited rational engine; no common-mode parameter error is ruled out solely by agreement. The separate literal implementation and the ordinary mathematical audit provide additional checks of different parts of the argument.

All children ran serially with six native-thread settings equal to one, a fixed forty-five-second timeout per child, **125.773843 seconds** of recorded total child wall time, maximum child **15.431962 seconds**, and cumulative child peak **88,776 KiB**. The six primary seals remain unchanged. No solver, floating-point feasibility inference, timeout-based exclusion, resource escalation, or assertion erased by optimization enters the proof.

The remaining trust boundary is the ordinary analytic reasoning, exact Python/integer/Fraction implementation and decoder, faithful mapping of the signed definitions to that source, and the stated lower-domain theorem. There is no proof-assistant verification. Source publication and a shared signature are not substitutes for these boundaries. No gap requiring mathematical repair was found within the stated scope; formal verification and wider-radius work remain separate tasks.

## Strengthening and improvement opportunities

**Proved in this review:** the same complete finite inequalities imply the explicit annular first-power gap \(2^{-22}\). [GAP.md](GAP.md) gives the full floor-preserving radial clipping and channel Lipschitz proof, with no actual-polynomial feasibility premise for the clipped tuple. That perturbation argument is reusable whenever the channel dichotomy and energy exclusion have positive numerical margins. Relative to the lower-domain input, compactness also gives a qualitative positive gap on the whole closed marked \(13/20\) disk; no numerical lower-disk constant is claimed.

**Sharper constants, not proved here:** optimize the perturbation size using the exact shell margin and sharper seven-factor product estimates rather than the safe constants 64 and 576. This requires a new checked comparison of all three margins; the present numerical constant is not optimal.

**Larger radius, not proved here:** extending to \(2/3\) or beyond requires a valid new centered envelope and all higher-order remainder bounds, together with a complete new closed cover and actual-root bridge. Adding a few sampled cells or inheriting an earlier review cannot supply that proof. Mean-dependent centered bounds may reduce overestimation, but their uniform sign and integral certificates remain obligations.

**Formal proof opportunity:** formalize Hermite domination on its entire positive-factor domain, the convex endpoint anchor, reciprocal series and full Bernstein enclosure, and the communication/Gauss–Lucas bridge. A formalized tree decoder alone would not certify the analytic implication of its leaf labels.

## Literature, novelty, and publication readiness

The live primary sources and candidate-specific comparison are documented in [LITERATURE.md](LITERATURE.md). The strongest unrestricted first-power problem remains distinct from current Sendov and quadratic results. The target advances this campaign's checked marked-radius frontier from \(5/8\) to \(13/20\); this review supplies materially independent complete verification and a numerical annular refinement. The review is suitable as compact reproducible evidence for this scoped claim. Neither the target nor this review establishes historical priority, resolves the unrestricted conjecture, or proves an optimal radius or margin.
