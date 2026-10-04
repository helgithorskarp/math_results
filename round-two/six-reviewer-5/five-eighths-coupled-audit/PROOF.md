# Independent analytic audit of the coupled five-eighths cover

Actual six-reviewer-5 / independent mathematical reviewer, 2026-10-04.
Ordinary proof, unformalized. This document supplies the continuous bridges
licensing the independent exact arithmetic in check_cover.py. The author’s
written proof and defining cover are exposed inputs; no author executable or
expected result is a premise.

## Scope and coordinates

For a complex eight-tuple, put r_j=|q_j|, F=sum r_j, mu=u+iv=mean q_j,
w=v^2, T=sum(r_j-1)^2, Pi=F-8u, E=sum|q_j-1|^2 and S=sum|q_j-mu|^2.
Expansion gives, without restrictions on complex arguments or repeated entries,

\[
 E=T+2Pi=T+2F-16u,\qquad
 S=E-8[(1-u)^2+w]=T+2F-8-8(u^2+w).
\]

In particular Pi,T,S are nonnegative, u<=F/8 and |mu|<=F/8.
The channels are

\[
 J_a=\int_0^1\prod_j[a+(1-a^2)tq_j]dt,\qquad
 O_a=9\int_0^1\prod_j(1-atq_j)dt.
\]

We independently verify the following standalone statement on the CLOSED
interval a in [3/5,5/8], under the PER-a floor r_j>=1/(1+a).
If F<=8 and |J_a|>=1, then F>184/25, E<23/5, u>253/400,
|mu|<=1 and |O_a|>2049/2048. We also verify the dichotomy on the closed
domain F in [184/25,8], E<=23/5, u>=253/400: either
|J_a|<9999/10000 or |O_a|>2049/2048. These are necessary relaxations for
the polynomial application, not a characterization of original-root feasibility.

## Radial interpolation, including negative deviations

For l<=a<=h, l>=1/2, 0<=t<=1, the chord c=l+1-l^2-h obeys

\[
 h+ct-[a+(1-a^2)t]=(1-t)(h-a)+t(a-l)(a+l-1)\ge0.
\]

The weaker chord h+ht follows from the identity with (a-1/2)^2 when
h=5/8. Thus triangle inequality followed by AM-GM yields, if F<=184/25,

\[
 |J_a|\le\int_0^1[5/8+(5/8)(23/25)t]^8dt
 =58643076666481/58982400000000<1.
\]

All nine coefficients of this polynomial integral are retained by the checker.

For real deviations e_j with sum e_j<=0, let T=sum e_j^2 and
d=sqrt(T/56). Each positive e_j<=7d: the other seven sum to at most
-e_j and Cauchy-Schwarz gives T>=8e_j^2/7. This also bounds nonpositive
entries. For B>0,y>=0 and positive B+ye_j and B-yd, take
f(x)=log(B+yx). Its quadratic Hermite interpolant at -d (value and
derivative) and 7d (value) has curvature

\[
 k=[f(7d)-f(-d)-8df'(-d)]/(64d^2)\le0.
\]

The remainder has the sign of (x+d)^2(x-7d), because f''' >=0.
The usual Rolle argument works also for x<-d: its compact interval is
inside the positive-factor domain. Therefore f(x)<=Q(x) for every
relevant x. Write Q(x)=Q(0)+alpha x+k x^2. Direct substitution gives

\[
 alpha=3y/[4(B-yd)]
 +\log[(B+7yd)/(B-yd)]/(32d)\ge3y/[4(B-yd)].
\]

Sum the majorant using k<=0 and sum e_j<=0. The equality configuration
(7d,-d,...,-d) evaluates its constant and squared-moment contribution.
For e_j=r_j-1 this proves

\[
 \prod(B+ye_j)\le(B+7yd)(B-yd)^7
 \exp[-3y(8-F)/(4(B-yd))].
\]

The sign in the exponential matters: multiplying a negative sum by a
lower bound on alpha gives an upper bound. When T=0, F=8 and all e_j=0;
when y=0 the product equality is immediate. No feasibility of the sharp
real moment configuration as a disk-rooted polynomial is needed.

The per-a floor implies the uniform m=8/13. Writing r_j=m+x_j,
X=sum x_j in [0,8(1-m)] and using sum x_j^2<=X^2 proves
T<=56(1-m)^2=1400/169. In particular d<=5/13. With
B=a+(1-a^2)t and y=(1-a^2)t, all radial factors and B-yd stay positive.

The identity

\[
 |a+(1-a^2)tq_j|^2=(a+(1-a^2)tr_j)^2
 -2a(1-a^2)t(r_j-\Re q_j)
\]

and log(1-x)/2<=-x/2 pay a further loss. If a complex factor vanishes,
the product is zero and needs no logarithm. At t=0 the bound is direct.
For any upper bound D>=e_j, the resulting product is bounded by

\[
 (B+7yd)(B-yd)^7
 \exp[-a(1-a^2)tPi/(a+(1-a^2)t(1+D))^2
       -3(1-a^2)t(8-F)/(4(B-yd))].
\]

## Rational polar integrals

On a CLOSED box a in [A,H], T in [L,U], F<=F_+<=8, Pi>=P>=0, set

\[
 b_-=1-H^2,\quad b_+=1-A^2,\quad
 a_*=\min(A(1-A^2),H(1-H^2)),\quad c=A+1-A^2-H,
\]
\[
 delta=\lfloor1024\sqrt{L/56}\rfloor/1024,\quad
 D=\min(\lceil256\sqrt{7U/8}\rceil/256,F_+-7/(1+H)-1).
\]

The second cap uses the actual per-box floor, not just 8/13. Concavity of
a(1-a^2) licenses a_*. The checker establishes D>=0 and c-b_-delta>0.
Writing the radial product as B^8 phi(yd/B), with
phi(x)=(1+7x)(1-x)^7, its decreasing logarithmic derivative on [0,1)
licenses

\[
 R_L(t)=[H+(c+7b_-delta)t][H+(c-b_-delta)t]^7.
\]

Put M_C=H+b_+(1+D), nu=b_+(1+D)/M_C, M_B=H+c and alpha=c/M_B.
All denominator and ratio signs are checked. Positive reciprocal series
about t=1 give a lower bound on the total exponential loss:

\[
 K(t)=t\sum_{n=0}^4 k_n(1-t)^n,
\quad k_n=a_*P(n+1)nu^n/M_C^2
       +(3/4)b_-(8-F_+)alpha^n/M_B.
\]

Thus |J_a|<=integral R_L(t)[1-K(t)+K(t)^2/2]dt. First lower the
exponential argument to the nonnegative K, then use exp(-K)<=1-K+K^2/2.
There is no claim that this quadratic is decreasing on the entire half-line.

The independent code computes the entire degree-18 vector in two ways:
ordinary convolution and binomial kernel expansion with all ordered
kernel pairs. It also integrates independently using
integral t^i(1-t)^j=i!j!/(i+j+1)!. Every square-root ceiling/floor is
checked against exact integer squares in its specified direction.

For E>=23/5, Pi>=(23/5-U)/2 on each T cell. All 67 consecutive
CLOSED cells [k/8,min((k+1)/8,1400/169)], k=0,...,66, give a polar
bound <9999/10000. Therefore E<23/5 under |J_a|>=1.
The coupled identity and the strict F floor give
u>=F/8-E/16>253/400>5/8. No omitted shell or endpoint is involved.

## Centered orders and diagonal lower bound

For z_j=q_j-mu, sum z_j=0 and sum |z_j|^2=S. Cauchy-Schwarz gives
|z_j|^2<=7S/8, hence |p_k(z)|<=(7/8)^((k-2)/2)S^(k/2).
For elementary symmetric functions, triangle and Cauchy-Schwarz over
all subsets followed by Maclaurin give
|e_l(z)|<=binomial(8,l)(S/8)^(l/2). The latter nonnegative symmetric
bound follows by averaging unequal coordinates on the compact simplex;
its maximizing point has all eight coordinates equal. Zero S and l=1
are separate immediate cases.

With rational square-root caps rho=479/512 and tau=363/1024,
Newton's identities (p_1=0) and Maclaurin allow the minimum of the two
recursive coefficients. The independent exact minima for l=2,...,8 are

\[
 (1/2,479/1536,11/32,2541/8192,7/128,363/65536,1/4096).
\]

The full product expansion is
sum_l e_l(z)(-at)^l(1-at mu)^(8-l); only its zero first centered term
vanishes. All remaining seven orders are paid.

On a necessary CLOSED box in (a,E,F,u,w), after the intersections below,
bound s=|mu|^2 by
s_+=min(1,U_+^2+W_+,(F_+/8)^2), and S by

\[
 S_+=\min(E_+-8[(1-U_+)^2+W_-],
 T_++2F_+-8-8(U_-^2+W_-)).
\]

For all retained boxes the code verifies S_+>=0, s_+>=U_-^2,
U_->A s_+, 0<beta(1)<1, 1-AU_->0, where
beta(t)=1-2AU_-t+A^2s_+t^2. Decreasing the actual a to A increases
|1-at mu|^2 because u>a s; then lower u and raise s to get beta.
The positive decreasing beta has

\[
 \sqrt{beta(t)}\le Q(t)=1-AU_-t
 +A^2(s_+-U_-^2)t^2/[2(1-AU_-)].
\]

This follows from sqrt(x^2+d)<=x+d/(2x) with x>=1-AU_->0.
For each even l use H_l=beta^((8-l)/2); for odd l use
H_l=beta^((7-l)/2)Q. Ceiling square roots d_s,d_beta,d_S at denominator
1024 pay the odd powers. The complete remainder is

\[
 R=9\sum_{l=2}^8 H^l c_l S_+^{\lfloor l/2\rfloor}
 d_S^{l\bmod2}\int_0^1t^lH_l(t)dt.
\]

Direct integration of the diagonal is [1-(1-a mu)^9]/(a mu).
Here mu is nonzero. Triangle inequality and the paid endpoint/denominator
bounds give |O_a|>=D-R with D=(1-d_beta beta(1)^4)/(H d_s).
All signs are checked. Every full centered vector is compared with a
multinomial expansion; every integral is independently recomputed before
applying its weight. This is not a truncation at second or third order.

## Necessary intersections and coverage

The exposed root is exactly
[3/5,5/8] x [0,23/5] x [184/25,8] x [253/400,1] x [0,23/40].
The w bound follows from E>=8[(1-u)^2+w]. The input tree first bisects
raw CLOSED boxes at exact midpoints. Both children include the midpoint.
At each leaf the checker performs four ordered necessary intersections:

\[
 U_+\gets\min(U_+,F_+/8),\quad
 U_-\gets\max(U_-,F_-/8-E_+/16),
\]
\[
 F_-\gets\max(F_-,8U_-),\quad
 F_+\gets\min(F_+,8U_++E_+/2),
\]
\[
 E_-\gets\max(E_-,2\max(0,F_--8U_+),8[(1-U_+)^2+W_-]),
\]
\[
 W_+\gets\min(W_+,(F_+/8)^2-U_-^2,E_+/8-(1-U_+)^2).
\]

Each update follows from the identities and Pi,T,S>=0, using u<=1.
A strictly reversed endpoint proves emptiness; failed estimates do not.
No convergence assumption is needed. After intersection the radial bounds are

\[
 T_- =\max(0,E_--2F_++16U_-,(8-F_+)^2/8),
\]
\[
 T_+=\min(E_+-2\max(0,F_--8U_+),
 (F_+-7m-1)^2+7(m-1)^2),\quad m=1/(1+H).
\]

For the upper bound maximize squared radial mass with fixed sum F and
floor m; concentrating the excess gives the displayed quadratic. Its
derivative is positive for F>=7m+1. Every used nonempty box satisfies
F_->7m+1, checked exactly. The last lower bound is Cauchy-Schwarz.

All 491 splits, 492 leaves and 983 reachable nodes are checked, including
types, binary paths, depth<=18 and equality of the entire reachable/input
sets. Sixteen leaves have a strict necessary contradiction. At each of the
476 others every centered order is checked. The 230 origin leaves have
D-R>2049/2048, and the 246 polar leaves have bound <9999/10000.
The 67 energy cells and 246 polar leaves total 313 full vectors; all
476*7=3332 centered vectors are checked. Thus every necessary point is
covered and yields the claimed dichotomy. Under |J_a|>=1, only the origin
alternative remains.

## Passage to actual original polynomials

For 3/5<|a|<=5/8, a multiple marked original zero is also a critical
zero, so the reciprocal sum is infinite. Otherwise rotate the entire
polynomial to make a positive real and normalize it to be monic. Write
p(z)=(z-a)product(z-z_j), p'(z)=9product(z-zeta_j), with all multiplicities.
Simplicity makes q_j=1/(a-zeta_j) finite and nonzero. Integrating p' from
a to 0 and from a to 1/a gives exactly

\[
 O_a=\prod z_jq_j,\qquad J_a=\prod(1-az_j)/(a-z_j).
\]

The closed original disk implies |O_a|<=product r_j and |J_a|>=1,
because |1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)>=0. Gauss-Lucas gives
the essential r_j>=1/(1+a). If F<=8, AM-GM gives product r_j<=1,
contradicting the independently checked origin lower bound. Thus F>8.
For |a|<=3/5 we explicitly use the credited parent10131/index1, whose
complete confirming review10168 is read. We do not re-audit that lower
region or transport its quantitative annular constant to 5/8.

The separate Gaussian-rational controls evaluate all coefficients of six
original polynomials, all eight derivative degrees, both communications,
the marked-multiple branch and a unit rotation. They are algebraic controls,
not finite testing as a replacement for these universal bridges. A separate
rational complex tuple checks all exact moment identities without claiming
original-root feasibility.

## Qualitative uniform gap, proved consequence

Relative to the verified strict theorem and its lower-region dependency,
there exists eta>0 such that EVERY such original polynomial and EVERY
|a|<=5/8 has F>8+eta, with infinite terms understood as above.

To prove this, take the compact set of labeled tuples
(a,z_1,...,z_8,zeta_1,...,zeta_8), each original and critical coordinate in
the closed unit disk, |a|<=5/8, satisfying the full polynomial coefficient
identity

\[
 [(z-a)\prod(z-z_j)]'=9\prod(z-zeta_j).
\]

Coefficient equality is a closed condition, and Gauss-Lucas ensures every
actual polynomial has such a tuple. The extended function sum 1/|a-zeta_j|
is lower semicontinuous, including its infinite values at collisions.
It attains a finite minimum M: the nonempty set includes p=z(z-1)^8,
a=0, whose critical roots are seven copies of 1 and one 1/9, so F=16.
At its finite minimizer the strict theorem gives M>8. Taking
eta=(M-8)/2 proves the assertion. This compactness argument gives neither
a numerical eta nor its optimal value; it does not enlarge the marked disk.
