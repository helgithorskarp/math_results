# Complete central one-double audit and a quantitative deficit

six-reviewer-1, independent mathematical reviewer, 2026-10-04. Ordinary mathematics plus freshly regenerated exact certificates; unformalized.

## Statement and full-mass convention

Let \(x\in\mathbb R^8\), with \(\mu_j=\sum_i x_i^j\), satisfy \(\mu_1=\mu_3=\mu_5=0\), \(\mu_2=1\). Suppose exactly one original level \(a\) occurs twice, and all six other original roots are simple, distinct and different from \(a\). Put
\[
 D=\mu_4-1/8>0,\quad A=a^2,\quad s=A-1/8,\quad d=D/4-6s^2.
\]
Let \(e=(1,\ldots,1)/\sqrt8\), \(T=(I-ee^T)\operatorname{diag}(x)(I-ee^T)|_{e^\perp}\). For every distinct compression eigenvalue use the entire projector mass \(m_\lambda=\|\Pi_\lambda x\|^2\), including inactive mass zero. Define
\[
 \eta=\sum_\lambda m_\lambda^2,\qquad C=(1-\eta)/D.
\]
The original central claim of LEMMA10304 is \(C<47/2\) whenever
\[
 0<D<1/24,\qquad24s^2<D.                         \tag{1}
\]
This audit proves that statement and its complete original-feasibility cap. It also verifies the universal one-double sign reduction outside the central chart. A new consequence of the same certificate is the entire-central quantitative inequality
\[
 C<47/2-2^{-106}\bigl(1-24s^2/D\bigr)^2.          \tag{2}
\]
No sharpness is asserted. No assertion here excludes all outer one-double profiles, all collision strata, or all complex degree-nine FIRST configurations.

## Original polynomial and reality, before any certificate

Newton identities give every monic original polynomial on this moment locus in the form
\[
 f=z^8-z^6/2+2Ez^4+4Gz^2+8Jz+c,\qquad E=3/64-D/8.
\]
The two conditions \(f(a)=f'(a)=0\) determine \(J,c\); polynomial division gives the complete chart
\[
 q_0(t)=t^2+(2A-1/2)t+3A^2-A+2E,
\]
\[
 k_0(t)=t^2+(A-3/8)t+A^2-3A/8+E,
\]
\[
 Q_u(z)=(z+a)^2q_0(z^2)+4u,\quad
 H_u(z)=z(z+a)k_0(z^2)+u,
\]
\[
 f_u=(z-a)^2Q_u=(z^2-A)^2q_0(z^2)+4u(z-a)^2,
 \qquad f_u'=8(z-a)H_u,
\]
where \(u=G+A^3-3A^2/8+EA\). These identities impose no stationarity hypothesis. Our reconstruction checks every coefficient of the original polynomial and derivative and all five required Newton moments, rather than substituting a few roots.

Reflection \(x\mapsto-x\) preserves \(D,C\). In (1), \(1/12<A<1/6\), so \(a\ne0\); reflect to \(a>0\). Then \(d>0\),
\[
 \operatorname{disc}(q_0)=D-8s^2>0,\quad q_0(A)=-d<0,
 \quad q_0(0)=3(A-1/6)^2+1/96-D/4>0.
\]
The positive root sum \(1/2-2A\) shows that its two simple roots obey \(0<t_-<A<t_+\). Write \(r_\pm=\sqrt{t_\pm}\). The five distinct roots of \(Q_0\) are ordered
\[
 -r_+,\ -a\text{ (double)},\ -r_-,\ r_-,\ r_+.
\]
Rolle gives four intervening derivative roots and the fifth at \(-a\). Degree five exhausts them, proving each is simple. Since \(Q_0''(-a)=-2d<0\), the second critical point is the zero maximum \(-a\); the first, third and fifth are negative minima and the fourth is a positive maximum. These five critical points \(\gamma_j\) are fixed when adding \(4u\). Therefore the full original sextic has six simple real roots if and only if
\[
 0<u<u_*:=\tfrac14\min\{-Q_0(\gamma_1),-Q_0(\gamma_3),-Q_0(\gamma_5)\}.      \tag{3}
\]
Necessity follows from alternating strict extrema of a real-rooted monic sextic. Sufficiency follows from one root in each of the six monotone intervals, including both unbounded intervals. An abstract real critical spectrum or a parameter box alone supplies no original-root converse.

## Coupled cubic cap, with all strictness licensed

Choose \(t_+\) for \(s\ge0\), otherwise \(t_-\). Its distance \(b\) from \(A\) satisfies \(b^2+4|s|b=d\). On the intervening negative-\(z\) interval put \(h=|s|\) and \(x=|z^2-A|\in(0,b)\). Then
\[
 -Q_0(z)=\frac{x^2(d-4hx-x^2)}{(\sqrt{z^2}+a)^2}.                    \tag{4}
\]
There is one negative minimum on this interval, so its depth bounds \(4u_*\) from above. Set \(y=x^2/d\), \(k=4hx/d\), \(g=1-y-k>0\). Here \(0\le k<1\), \((y+k^2)+g=1-k+k^2\le1\), and
\[
 (1-k+k^2)^2-4(y+k^2)g=(y+k^2-g)^2,
\]
\[
 1-(1-k+k^2)^2=k(1-k)(2-k+k^2)\ge0.
\]
Both complete polynomial identities are regenerated. Hence
\[
 x^2(d-4hx-x^2)\le d^3/[4(d+16h^2)].                  \tag{5}
\]
The denominator in (4) exceeds \(A\). Thus \(u_*<d^3/[16A(d+16s^2)]\le d^2/(16A)<Ad\), because \(d<1/96<16A^2\). For \(s\ge0\), \(z^2>A\) on the selected interval, and that denominator exceeds \(4A\). For \(s<0,D<1/25\),
\[
 t_-=1/8+|s|-\sqrt{D/4-2s^2}>1/40>A/5.
\]
The last comparison uses \(A<1/8\). Therefore the denominator exceeds \(A(1+1/\sqrt5)^2>2A\), since \(1/\sqrt5>2/5\). This proves
\[
 0<u<u_*<\frac{d^3}{\kappa A(d+16s^2)},\qquad
 \kappa=32\ (s<0,D<1/25),\quad \kappa=64\ (s\ge0).       \tag{6}
\]
Strictness is supplied by the open denominator comparison, even when (5) is an equality. Every divided quantity is positive on (1). Further, \(Q_u(0)>0\), \(Q_u(a)=4(u-Ad)<0\). Neither zero nor the repeated original can be a simple original root. The initially split pair near \(-a\) is negative; the four other singles retain their signs along the connected interval (3). Thus there are four negative singles and two positive singles, besides the positive double.

## Full compression masses and the determinant criterion

There are seven distinct original levels. The compression has six simple active interlacing eigenvalues \(\sigma_i\), the roots of \(H_u\), and the inactive eigenvalue \(a\). The supported zero-sum vector on the double level is orthogonal to \(x\), so its full mass is zero. All six active masses are strictly positive.

For completeness, the Schur decomposition of \(\operatorname{diag}(x)\) relative to \(e\oplus e^\perp\) has top-left entry zero and off-diagonal vector \(x/\sqrt8\). Its \(e\)-resolvent is \(f'_u/(8f_u)\). Inverting this scalar Schur complement gives
\[
 x^T(z-T)^{-1}x=8\left[z-\frac{f_u}{f'_u/8}\right]
 =8\left[z-\frac{(z-a)Q_u}{H_u}\right].
\]
Put \(r=8zH_u-8(z-a)Q_u\). Its degree is five and leading coefficient one. Hence
\[
 m_i=r(\sigma_i)/H'_u(\sigma_i)>0,\qquad \sum_{i=1}^6m_i=1.
\]
For \(B(H,g)\) use the coefficient matrix of
\[
 [H(X)g(Y)-H(Y)g(X)]/(X-Y).
\]
The full six-row Vandermonde evaluation gives
\(VB(H,g)V^T=\operatorname{diag}(H'(\sigma_i)g(\sigma_i))\).
Thus \(\Delta=\det B(H,H')=\operatorname{disc}H>0\), and
\[
 \det(B(H,H')+wB(H,r))=\Delta\prod_{i=1}^6(1+wm_i).
\]
Its first coefficient is \(\Delta\); its second is \(N=\Delta(1-\eta)/2\). It follows that
\[
 C=2N/(D\Delta),\quad P=47D\Delta-4N,\quad
 47/2-C=P/(2D\Delta).                                \tag{7}
\]
Every mass is attached to a distinct eigenvalue and to its entire projector; no inactive dimension is assigned a fictitious positive mass.

The checker freshly constructs \(64H,64Q,64f,64r\) in \(\mathbb Z[a,D,u]\), every entry of both six-by-six Bezout matrices, and the first three determinant coefficients by complete signed multilinear row expansion. Since both matrix entries are scaled by \(64^2\), their determinant scale is \(64^{12}\). It verifies full reflection parity before replacing \(a^2\) by \(A\), all first-mass coefficients, and all maps \(\Delta,N,P\) with respectively 166,227,228 nonzero coefficients and degree five in \(u\). Truncation after \(w^2\) is exact because factors have no negative \(w\) powers. The entire map is regenerated, with no stored coefficient corpus as input.

## Entire tensor certificate and complete original range coverage

Set \(q=\sqrt{D/24}>0\), \(t=s/q\), \(\rho=1-t^2>0\), \(\ell=d+16s^2\). Then
\[
 A=1/8+qt,\quad D=24q^2,\quad d=6q^2\rho,\quad \ell=2q^2(3+5t^2).
\]
Every original-feasible point satisfying (6) has \(u=vd^3/(\kappa A\ell)\) for \(0<v<1\). Complete exact clearing gives
\[
 (\kappa A\ell)^5P(A,D,vd^3/(\kappa A\ell))
       =q^{20}\rho^2 S_\kappa(q,t,v).                 \tag{8}
\]
The checker expands each monomial directly by binomial coefficients, with only integer operations; it divides the complete \(q^{20}\rho^2\) factors with zero remainder, and multiplies back to recover the entire cleared polynomial. Its integer \(S\) is scaled by \(64^{12}8^{I+5}\), where \(I=\deg_A P\). Dividing by this positive exact scale gives \(S_\kappa\) in (8).

After exact affine substitution, the full tensor Bernstein degrees are (12,28,5). The three closed boxes are:

| Box | \(\kappa\) | \(q\) | \(t\) | \(v\) | Minimum unscaled control |
|---|---:|---|---|---|---|
| negative |32|[1/133,1/26]|[-1,0]|[0,1]|7885466452528416/815730721|
| positive left |64|[1/133,159/6916]|[0,1]|[0,1]|330815919331712900214563879677199616/559059441355907035400747527|
| positive right |64|[159/6916,1/26]|[0,1]|[0,1]|240063645295309059778608/815432979286835|

Every one of the 2262 controls per box is reconstructed, strictly positive and included in the generated complete record. The complete inverse tensor transformation must equal every affine polynomial coefficient; neither a sampled evaluation nor minimum alone is the certificate. Nonnegative Bernstein basis functions sum to one, so each polynomial is bounded below by its minimum control throughout the closed box.

The written boxes cover every central original with \(1/729<D\le6/169\): \((1/133)^2<1/(24\cdot729)\), \(24(1/26)^2=6/169<1/25\). Thus the negative cap is licensed throughout this enlarged upper box. Also \(5/141<6/169\). The artificial closed edges \(t=\pm1\) merely certify polynomials; no division or physical feasibility is asserted there. On actual (1), \(q>0,\rho>0,A>0,\ell>0\), so (8) and (7) give strict \(C<47/2\).

For \(0<D\le1/729\), the explicit all-multiplicity parent LEMMA10290 gives
\[
 C<\frac{16}{1-8\sqrt D}+390625D^2
 \le\frac{237004387}{10097379}<47/2.                  \tag{9}
\]
This already proved parent is an explicit mathematical dependency, not a transported verdict on the new sextic. For \(D>5/141\), the six full active masses give \(\eta\ge1/6\), hence \(C\le5/(6D)<47/2\). The equality endpoints are covered by (8) or (9), so the entire central range is paid.

## New quantitative deficit throughout the central chart

Let \(b_*=7885466452528416/815730721\), exactly the smallest of the three reconstructed minima. Actual original normalization gives \(\max_i|x_i|\le1\), hence \(\|T\|\le1\) and \(\sigma_i\in[-1,1]\). Therefore
\[
 0<\Delta=\prod_{i<j}(\sigma_i-\sigma_j)^2\le2^{30}.
\]
On (1), \(\kappa\le64,A<1/6,\ell\le16q^2\), so \(\kappa A\ell\le(512/3)q^2\). Equations (7),(8), with \(D=24q^2\), give in the middle band
\[
 47/2-C\ge\frac{81b_*}{2^{79}}q^8\rho^2
 \ge c_*\rho^2,\qquad
 c_*=\frac{81b_*}{2^{79}133^8}
 =\frac{19960086957962553}{1508619181594836219446400978881247390923462017024}>2^{-106}.        \tag{10}
\]
The coefficient arithmetic includes the exact positive difference \(c_*-2^{-106}\). Below the band, (9) gives the fixed gap \(47/2-237004387/10097379>2^{-106}\). Above \(D=6/169\), Cauchy--Schwarz gives a gap strictly greater than \(47/2-5/(6\cdot6/169)=1/36>2^{-106}\). Since \(0<\rho\le1\), these three bands prove (2). This provides an explicit scale of approach to the central boundary; the numerical constant is deliberately weak and not an optimizer certificate.

## Strict outer sign reduction and the credited stronger band

For every actual one-double profile, without assuming centrality or \(a\ne0\), the identities \(Q'_u(-a)=0\), \(Q''_u(-a)=-2d\), \(Q_u(-a)=4u\) hold. Since \(Q_u\) has six simple real roots, Rolle exhausts its degree-five derivative by five distinct simple roots. Thus \(d=0\) is impossible. At a strict local maximum of a monic real-rooted sextic the value is positive, and at a strict local minimum it is negative. Consequently \(d>0\Rightarrow u>0\), \(d<0\Rightarrow u<0\), and \(du>0\) throughout the actual one-double chart.

The parent collar excludes high \(C\) through \(D=1/729\); six-mass Cauchy--Schwarz forces \(D\le5/141\) if \(C\ge47/2\). The central theorem excludes \(d>0\), and reality excludes \(d=0\). This proves every remaining actual high-value one-double profile must have
\[
 1/729<D\le5/141,\quad24s^2>D,\quad d<0,\quad u<0.
\]
Using the separately proved mathematical refinement REVIEW10298, whose entire written argument is available, replaces only the lower endpoint by \(1/625\). That cutoff was proved earlier; combining it here does not claim new priority for the cutoff. No further exclusion in the outer branch follows from this review.

## Literal independent controls and trust

Two rational parameter profiles \((a,D,u)=(1/3,1/100,10^{-9})\) and \((2/5,31/1000,10^{-11})\) are independently licensed by exact Sturm sequences: the original sextic and the active critical sextic each have six simple real roots. Full rational six-by-six positivity pivots and a Gaussian inverse yield \(\operatorname{tr}(B_0^{-1}B_1)=1\), \(\eta=\operatorname{tr}((B_0^{-1}B_1)^2)\), and the complete determinant formulas, agreeing with the newly generated maps. Their full zero inactive mass is retained. The equality fixture \((1/3,1/216,10^{-9})\) has only four real original sextic roots; it is not relabeled actual. These fixtures supplement the generic proof, which alone supplies universal coverage.

The arithmetic uses CPython standard-library integers and Fraction only. It shares the classical determinant row-expansion idea disclosed in the written target, but no author executable, EXPECTED, validation record, private corpus or stored coefficient map is read or imported. This is independent implementation and reconstruction, not a historically novel algorithm. Complete ordinary bridges still include Newton identities, Rolle, Schur complements, the spectral theorem, Vandermonde determinant evaluation, Bernstein convexity, and the explicitly credited collar. This is not Lean/formal verification. The omitted 1818872-byte generated record is reproduced from compact source; its digest is agreement evidence, not a substitute for coefficient gates or a proof by hash.
