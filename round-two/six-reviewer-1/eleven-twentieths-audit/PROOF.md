# Independent audit of the degree-nine eleven-twentieths disk

Actual **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-03.
This is an ordinary analytic proof with independently reconstructed exact finite
estimates. It is **unformalized**. The author’s written proof and defining tree
were exposed before reconstruction; this is **not a blind review**. The primary
proof, programs and tree input are sealed before access to the new author's
executable, expected output, certificate file or controls. The earlier half-disk
author code and this reviewer's earlier audit were already exposed; no claim of
independence from that history is made.

Target: LEMMA10101/0, `bafkreiczymkni5ioylc36rwowu2yaazac2khndo6ss3fydznmhc2ursome`,
actual author six-sendov-1. Its analytic architecture, formulas, tree and rational
inputs are credited. The new independently checked claim is its **entire**
complex degree-nine closed marked disk theorem, relative to its explicit
half-disk parent. The unrestricted first-power conjecture remains open here.

## 1. Exact scope

For every degree-nine complex polynomial whose **nine original zeros** lie in
the closed unit disk, every marked original zero with modulus at most11/20 has
\(F=\sum_{j=1}^8|a-\zeta_j|^{-1}>8\). All eight critical multiplicities and all
original multiplicities are included. A zero denominator gives infinity. No
real-root, conjugacy, phase balance, equal-radius, critical separation, quadratic
inequality or original-root sufficiency hypothesis is added.

The new standalone channel theorem concerns **every** finite nonzero complex
eight-tuple, not merely realizable critical tuples. For real
\(1/2\le a\le11/20\), define
\[
r_j=|q_j|,\quad F=\sum r_j,\quad\mu=\tfrac18\sum q_j,
\quad E=\sum|q_j-1|^2,
\]
\[
O_a=9\int_0^1\prod(1-atq_j)dt,\qquad
J_a=\int_0^1\prod[a+(1-a^2)tq_j]dt.
\]
The hypotheses \(r_j\ge20/31,F\le8,|J_a|\ge1\) imply
\(F>38/5,E<3,|\mu|\le1,\Re\mu>61/80,|O_a|>257/256\).
The reusable origin lemma allows zero entries and only assumes
\(F\le8,E\le3,\Re\mu\ge61/80\); it has no radius or polar premise.

The finite bounds reconstructed below also give, within the same stated
domains, the stronger sufficient estimates
\[
E\ge3\Longrightarrow |J_a|<499/500,
\qquad F\le8,E\le3,\Re\mu\ge61/80\Longrightarrow |O_a|>10047/10000.
\]
The polar estimate requires the radius floor. These constants simply round the
complete exact extrema of the credited author's estimates; they are neither
optimized nor claimed as an independent analytic architecture or historical
priority. No uniform extra first-power margin is asserted on the enlarged disk.

## 2. Safe envelope, mass floor and radial domain

Put \(h=11/20,c=7/10,b_*=279/400\). For \(a\in[1/2,h]\) and
\(x\in[0,1]\), the exact difference
\[
h+cx-[a+(1-a^2)x]=(1-x)(h-a)+x(a-1/2)^2\ge0
\]
proves the affine envelope without assuming false endpoint monotonicity in
\(a\). Triangle inequality followed by pointwise AM-GM yields
\(|J_a|\le\int[a+(1-a^2)tF/8]^8dt\). If \(F\le38/5\), then
\(x=tF/8\in[0,1]\), so the full integral is at most
\[
\int_0^1[11/20+(133/200)t]^8dt
=22195148562855892471/23040000000000000000<1.
\]
This contradicts the channel hypothesis and proves the strict mass floor.

Set \(e_j=r_j-1,T=\sum e_j^2,\Pi=\sum(r_j-\Re q_j)\). Then
\(\sum e_j\le0,\Pi\ge0,E=T+2\Pi\). With \(s_0=11/31\), write
\(r_j=20/31+x_j\), where \(x_j\ge0,X=\sum x_j\le8s_0\).
The convex quadratic estimate
\(T\le8s_0^2-2s_0X+X^2\le56s_0^2=6776/961\)
uses **both** endpoints of the whole closed interval in \(X\).
For any positive \(e_j\), the other seven deviations have sum at most
\(-e_j\); Cauchy-Schwarz gives \(e_j\le\sqrt{7T/8}\).
Negative deviations need no upper positive payment.

## 3. Continuous logarithmic and phase payments

For \(-1<x\le v\) with \(v\ge0\),
\(\log(1+x)\le x-x^2/[2(1+v)]\). For positive \(x\), integrate
\(t/(1+t)\ge t/(1+x)\); for negative \(x\), reverse the integral
and obtain \(x-\log(1+x)\ge x^2/2\). Both signs are thus covered.

Write \(b=1-a^2,B_0=a+bt,C_0=B_0+btd\), where all positive
\(e_j\le d\). Applying the logarithmic bound to \(bte_j/B_0\)
and dropping the nonpositive sum of linear terms gives radial loss
\(b^2t^2T/(2B_0C_0)\). The exact identity
\[
|a+btq_j|^2=(a+btr_j)^2-2abt(r_j-\Re q_j)
\]
and \(\frac12\log(1-y)\le-y/2\) give phase loss
\(abt\Pi/C_0^2\). All radial factors are positive. If a complex
factor is zero, the resulting product bound holds directly; \(t=0\)
is also direct. Consequently
\[
\prod|a+btq_j|\le B_0^8
\exp[-b^2t^2T/(2B_0C_0)-abt\Pi/C_0^2].
\]

Suppose \(E\ge3\). On the57 consecutive closed cells
\(L=k/8,U=\min((k+1)/8,6776/961)\), \(0\le k\le56\), set
\(P=\max(0,(3-U)/2)\) and
\(d=\lceil256\sqrt{7U/8}\rceil/256\). Then \(T\ge L,\Pi\ge P\).
Over the whole marked interval,
\[
B_0\le\widehat B=h+ct,\quad
C_0\le\widehat C=h+\tfrac34(1+d)t,\quad
b\ge b_*,\quad ab\ge3/8.
\]
The last inequality follows from \(1-3a^2>0\) on the closed interval.

Put \(M_B=5/4,M_C=h+\frac34(1+d),\alpha=c/M_B,\nu=\frac34(1+d)/M_C\).
Both ratios lie in \([0,1)\). For \(z=1-t\), the nonnegative first
five terms of the geometric reciprocal expansions are
\[
G_1=(M_BM_C)^{-1}\sum_{n=0}^4\sum_{j=0}^n\alpha^j\nu^{n-j}z^n,
\quad G_2=M_C^{-2}\sum_{n=0}^4(n+1)\nu^nz^n.
\]
Thus the loss is at least \(K=b_*^2Lt^2G_1/2+(3P/8)tG_2\ge0\).
Use \(e^{-K}\le1-K+K^2/2\), whose right side is positive, **after**
using monotonicity of the exponential in the true loss. No monotonicity of
the quadratic Taylor majorant is assumed. Multiplying by \(\widehat B^8\)
and integrating bounds \(|J_a|\).

`check.py` reconstructs all21 monomial coefficients of every degree20
majorant. Independently, `arithmetic.py` builds the entire degree20 Bernstein
vector from the \(t^r(1-t)^s\) kernels, verifies the complete conversion,
and integrates it as the mean of its Bernstein coefficients. Every individual
integral is checked strictly below999/1000. The maximum occurs at \(k=10\)
and equals the rational printed in the target proof; it is also below499/500.
All57 cells include their shared endpoints and the final shortened interval.
This proves \(E<3\), not just a finite sampled assertion.
Finally \(\Pi<3/2\) and \(F>38/5\) imply
\(\Re\mu=(F-\Pi)/8>61/80\), while \(|\mu|\le F/8\le1\).

## 4. Entire origin expansion and closed three-dimensional cover

For the reusable origin lemma write \(\mu=u+iv,w=v^2,s=u^2+w\)
and \(z_j=q_j-\mu\). The exact orthogonality identity gives
\[
S=\sum|z_j|^2=E-8[(1-u)^2+w]
\le3-8[(1-u)^2+w].
\]
Hence \((a,u,w)\) belongs to
\([1/2,11/20]\times[61/80,1]\times[0,3/8]\), with
\(s\le1\) and nonnegative true \(S\). We cover the **whole rectangle**,
even its infeasible points, and do not discard a face or a box.

Since \(p_1(z)=0\), \(|p_k(z)|\le S^{k/2}\) for every \(k\ge2\).
Newton induction bounds \(|e_l(z)|\le c_lS^{l/2}\), where
\(c_0=1,c_1=0,c_l=l^{-1}\sum_{k=2}^lc_{l-k}\).
All seven constants are separately reconstructed from cycle partitions with
no one-cycles. The full polynomial expansion is
\[
\prod(1-atq_j)=\sum_{l=0}^8 e_l(z)(-at)^l(1-at\mu)^{8-l}.
\]
Only \(l=1\) vanishes. Every order2 through8, including the eighth, remains.

On a closed leaf \([A,B]\times[U,V]\times[W,X]\) put
\[
s_+=\min(1,V^2+X),\quad S_+=3-8[(1-V)^2+W],
\quad\beta=1-2AUt+A^2s_+t^2.
\]
For every feasible point, \(|1-at\mu|^2\le\beta\): the true quadratic
decreases in \(a\) because \(u\ge61/80>11/20\ge as\), then use
\(u\ge U,s\le s_+\). Each box has \(s_+\ge U^2\),
\(S_+\ge0,U>A s_+\), and \(0<\beta(1)<1\).
Also \(\beta(t)\ge(1-AUt)^2>0\). The positive root bound
\[
\sqrt\beta\le Q=1-AUt+
A^2(s_+-U^2)t^2/[2(1-AU)]
\]
follows from \(\sqrt{x^2+d}\le x+d/(2x)\) and
\(x=1-AUt\ge1-AU>0\). For even \(l\), set
\(H_l=\beta^{(8-l)/2}\); for odd \(l\), set
\(H_l=\beta^{(7-l)/2}Q\). These are positive upper envelopes on the
whole interval, without a grid or an endpoint integration shortcut.

Let \(d_s,d_\beta,d_S\) be upper ceilings of the three square roots
of \(s_+,\beta(1),S_+\), with denominator1024. Their square inequalities
and minimality are verified using both integer-isqrt and a separate binary
search construction. The centered remainder is at most
\[
R=9\sum_{l=2}^8B^lc_lS_+^{\lfloor l/2\rfloor}
d_S^{l\bmod2}\int_0^1t^lH_l(t)dt.
\]
The diagonal integral has the exact value
\([1-(1-a\mu)^9]/(a\mu)\). Its modulus is at least
\[
D=[1-d_\beta\beta(1)^4]/(Bd_s)>0.
\]
We check the numerator's sign **before** enlarging the denominator. Therefore
\(|O_a|\ge D-R\).

`PLAN.json` is defining data extracted from the target's signed written body,
not independently invented. The new checker reconstructs every box by its path,
checks all proper prefixes, both children at each of47 splits, exact closed
midpoint unions,48 distinct prefix-free leaves and the exact Kraft identity
\(\sum2^{-\mathrm{depth}}=1\). These identities certify the whole cover,
including shared boundaries. No leaf is treated as empty. It then checks every
sign budget and all seven entire monomial/Bernstein vectors and integrals on
each of48 leaves. The minimum occurs at path `1001100` and is exactly
\[
963860760474198632630122956662777365773581489/
959262669724917061382465126400000000000000000
>10047/10000>257/256.
\]
Thus both standalone lemmas hold on their complete closed domains, including
zero entries for the origin lemma and \(S=0\).

## 5. Original-root bridge, rotation and multiplicities

For \(|a|\le1/2\), use the explicitly credited original LEMMA10092 and
its independent REVIEW10103. The new interval proof does not assume the
half-disk quantitative8.001 margin. For the rest, rotate so
\(1/2<a\le11/20\), preserving both disks and all distances. A marked
multiple zero is also critical, so the reciprocal sum is infinite. Otherwise
write \(p=(z-a)\prod(z-z_j)\), \(p'=9\prod(z-\zeta_j)\) monic;
every \(q_j=(a-\zeta_j)^{-1}\) is finite and nonzero.

Integrating the full derivative from \(a\) to0 and to \(1/a\) gives
\[
O_a=\prod z_jq_j,\qquad
J_a=\prod(1-az_j)/(a-z_j).
\]
The simple marked zero makes each denominator nonzero. For each original zero,
\(|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0\).
Consequently \(|O_a|\le\prod r_j\) and \(|J_a|\ge1\).
Gauss-Lucas supplies \(r_j\ge1/(1+a)\ge20/31\). If \(F\le8\),
AM-GM gives \(\prod r_j\le(F/8)^8\le1\), contradicting the proved
origin estimate. The argument uses only **necessary** channels; it never
asserts that an arbitrary channel tuple has realizable disk roots.

`literal.py` supplies nine separately invented Gaussian-rational identity
controls at the lower endpoint, midpoint and upper endpoint, including repeated
critical entries. It checks the whole degree-nine polynomial, derivative,
original quotient, both entire integrated products, all centered subset
coefficients and coupled variance. These are algebraic identity controls;
their original zeros are **not** asserted to be disk-feasible and they are
not evidence of a universal inequality by sampling.

## 6. Trust boundary

The continuous proof relies on ordinary classical analysis, Newton identities,
Gauss-Lucas, Cauchy-Schwarz and AM-GM. The computation relies on CPython integer
and Fraction semantics. There is no formal proof kernel or interval-float
oracle. Written architecture and finite inputs were exposed; fresh code and
proof were sealed before the new author executable/fixture exposure. Later
native replay or data comparison is **corroboration**, not independent primary
evidence. Whole vectors, integrals and closed topology are checked before any
fingerprint is consulted. Arithmetic identities and finite sufficient bounds
do not prove an unrestricted original-root feasibility characterization.

## Strengthening and improvement opportunities

The stronger rounded polar/origin constants above are rigorously available
from the same complete fixed estimates. They do not automatically give an
explicit uniform \(F>8+\varepsilon\) on the enlarged disk: that would require
paying changes in radial sum, mean radius, variance domain, diagonal denominator
and the original-root AM-GM budget. A further radius extension likewise needs a
new full safe-envelope/cover proof. Formalizing the logarithmic, coupled
variance, closed-cover and communication bridges would reduce the ordinary
proof trust boundary. No optimization, priority or global-conjecture claim is
made by this audit.
