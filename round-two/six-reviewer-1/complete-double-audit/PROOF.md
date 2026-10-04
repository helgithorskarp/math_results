# Complete one-double audit and quantitative middle-band consequences

Actual six-reviewer-1 / independent mathematical reviewer, 2026-10-04.
This is an ordinary unformalized proof with complete exact finite certificates.
Written target proofs, rectangles and minima were exposed; this is not blind.

## Precise domain and dependencies

Let the eight real original entries, including multiplicities, satisfy
\(\mu_1=\mu_3=\mu_5=0,\mu_2=1,D=\mu_4-1/8>0\). Exactly one value
\(a\) occurs twice and the other six are distinct simple values different
from \(a\). Let \(S=P_8\operatorname{diag}(x)P_8\) on \(e_8^\perp\), and
use full spectral projections in \(m_\sigma=\|\Pi_\sigma x\|^2\),
\(\eta=\sum m_\sigma^2\), \(C=(1-\eta)/D\).

The complete conclusion is **\(C<47/2\)**, without a stationarity premise.
The prior all-multiplicity small-D theorem REVIEW10298 supplies this strict
inequality for \(D\le1/625\). The prior central theorem, independently
confirmed in REVIEW10318, supplies it when \(D>24(A-1/8)^2\).
REVIEW10186 supplies the all-value sign implication: zero third moment and
\(C\ge404/23\) force four positive and four negative entries and no zeros.
These three previously confirmed results are credited inputs, not re-audited
parent theorems in this pass. Definitions are the published7432 framework.

The repeated-original contrast has mass zero. The other six eigenvalues are
simple strict gaps, have positive masses summing to one, and give
\(\eta\ge1/6\). Thus \(D>5/141\) implies \(C<47/2\).
In a putative counterexample we therefore have four positive/four negative
originals, \(1/625<D\le5/141\), and may reflect so \(a>0\).
All remaining root and certificate arguments below are proved afresh.

## Original equations and the full spectral polynomial

Put \(A=a^2,s=A-1/8,d=D/4-6s^2,E=3/64-D/8\). Newton's identities and
the double-root equations give, for a real parameter \(u\),

\[
q_0(t)=t^2+(2A-1/2)t+3A^2-A+2E,\quad
k_0(t)=t^2+(A-3/8)t+A^2-3A/8+E,
\]
\[
Q_u(z)=(z+a)^2q_0(z^2)+4u,\quad f_u(z)=(z-a)^2Q_u(z),
\quad H_u(z)=z(z+a)k_0(z^2)+u,\quad f'_u=8(z-a)H_u.
\]

Conversely these equations impose the stated four moment constraints.
The full coefficient checks regenerate these identities and moments.
Actual feasibility requires six distinct real roots of \(Q_u\) and
\(Q_u(a)=4(u-Ad)\ne0\). Rolle then supplies the six distinct gap roots
of \(H_u\), all different from \(a\). Critical-root reality alone is
insufficient; our exact negative control has six simple real H roots but
only four real Q roots. The case \(d=0\) is impossible, since
\(Q'_u(-a)=0\) and \(Q''_u(-a)=-2d\), whereas the derivative of a
six-simple-real-root polynomial has five simple real roots.

For balance and normalization, the compressed resolvent obeys
\[
\langle x,(zI-S)^{-1}x\rangle
=8z-64f_u(z)/f'_u(z)=r(z)/H_u(z),
\quad r=8zH_u-8(z-a)Q_u.
\]
Indeed, with \(\alpha=\tfrac18\sum(z-x_j)^{-1}=f'_u/(8f_u)\),
the Schur complement gives \(8(z-1/\alpha)\). This derivation retains
the original entries and the inactive contrast. The polynomial r has
degree five and leading coefficient one, and its six residues are exactly
the full active masses \(-8(\sigma-a)Q_u(\sigma)/H'_u(\sigma)\).

Define the symmetric Bezout matrix by
\[
\frac{H_u(X)g(Y)-H_u(Y)g(X)}{X-Y}
=\sum_{i,j=0}^{5}B(H_u,g)_{ij}X^iY^j.
\]
Evaluation on the six distinct roots diagonalizes it by a Vandermonde
congruence, with diagonal entries \(H'_u(\sigma)g(\sigma)\). Hence
\[
\det B(H_u,H'_u+w r)=\Delta\prod_{i=1}^6(1+wm_i),
\quad\Delta=\operatorname{disc}(H_u)>0.
\]
If N is the coefficient of \(w^2\), then
\[
N=\Delta(1-\eta)/2,\quad C=2N/(D\Delta),\quad
P=47D\Delta-4N=2D\Delta(47/2-C).
\]
The independent sparse row-subset determinant reconstructs every
coefficient through w-degree two; higher w-degrees cannot change them.
There is no truncation in A,D,u. Entire parity, the coefficient-of-w
identity, and all166/227/228 nonzero terms of Delta/N/P are checked.
Working with64 times H and r multiplies these three polynomials by
\(64^{12}\), which is explicitly divided out in every reported minimum.
The Bezout identity itself is credited prior10136.

## Original-root fibre, including the real-q0 boundary

In the remaining outer case \(d<0\), set \(h=|s|\) and
\(B=1/4-A\). Since \(Q'_u=2(z+a)T_4(z)\),
\[
T_4(z)=3z^4+2az^3-4Bz^2-2aBz+B^2+2h^2-D/4.
\]
Actual Q supplies four distinct real T4 roots, disjoint from -a.
For completeness, the freshly derived leading Hermite minors for monic
T4/3 are
\[
4,\quad(9-56s)/6,\quad
(-504Ds+81D+3136s^3-392s^2-34s+2)/162,\quad F/46656,
\]
where
\[
\begin{split}
F={}&-6912D^3+173376D^2s^2-2736D^2s+117D^2
-1455104Ds^4+30464Ds^3+3888Ds^2-752Ds+32D\\
&+4214784s^6-150528s^5-20160s^4+4224s^3-192s^2.
\end{split}
\]
All four positive minors are equivalent to four distinct real roots.
The forward direction uses the evaluation Gram matrix. Conversely positive
definiteness excludes multiplicity; a conjugate nonreal pair admits a real
degree-at-most-three interpolation polynomial with values i,-i at that pair
and zero at the remaining roots, producing the negative square sum -2.
This contradicts positive definiteness. Sylvester's criterion finishes.

Sort the five fixed derivative roots as \(\gamma_1<\cdots<\gamma_5\).
The monic sextic's minima have indices1,3,5, maxima2,4. Precisely
\[
Q_u\text{ has six distinct real roots}\quad\Longleftrightarrow\quad L<u<U,
\]
\[
L=\max_{i=2,4}[-Q_0(\gamma_i)/4],\qquad
U=\min_{i=1,3,5}[-Q_0(\gamma_i)/4].
\]
Necessity follows from alternating strict critical heights; sufficiency
follows from one crossing in each of the six monotone intervals, including
the two tails. Original separation adds \(u\ne Ad\). Since -a is a
strict minimum with \(Q_0(-a)=0\), feasibility gives \(u<0\).

Suppose \(D\ge8s^2\). Then \(D<24s^2\) and
\(h\le\sqrt{D/8}<3/40\). The two roots of q0 are positive because
\(s+\tfrac12\sqrt{D-8s^2}\le\sqrt{3D/8}<1/8\). They lie on the
same side of A. Write \(H=-d>0\), so \(H\le4h^2\), and let
\(\beta=2h-\sqrt{4h^2-H}\le2h\). In the negative gap adjacent to -a
and the nearer negative q0-root, Q0 has exactly one strict maximum. The
degree-five derivative count proves this also when q0 has a double root:
three distinct double Q0 roots then give three minima and two Rolle maxima.

At this maximum, with \(x=|z^2-A|\in(0,\beta)\),
\[
Q_0=\frac{x^2(H-4hx+x^2)}{(\sqrt{z^2}+a)^2}.
\]
Put \(k=4hx/H\in(0,2)\), \(y=x^2/H\le k^2/4\).
The complete polynomial identities
\[
k^2(2-k)^2-4k^2(1-k+y)=k^2(k^2-4y)\ge0,
\quad1-k^2(2-k)^2=(k-1)^2(1+2k-k^2)\ge0
\]
give numerator at most \(H^3/(64h^2)\). The denominator is strictly
greater than4A if s<0, and9A/4 if s>0; in the latter case the nearest
q0-root squared is at least1/8-h>A/4 since h<3/40. Alternating critical
heights therefore yield
\[
0<-u< H^3/(\kappa Ah^2),\qquad
\kappa=1024\ (s<0),\quad576\ (s>0).
\]
Let \(q=\sqrt{D/24},t=s/q\). Here \(1<|t|\le\sqrt3\), and
\[
A=1/8+qt,\quad D=24q^2,\quad
u=-216v q^4(t^2-1)^3/(\kappa At^2),\quad0<v<1.
\]
Exact full expansion and exact division reconstruct
\[
(\kappa At^2)^5P=q^{10}(t^2-1)^2S_\kappa(q,t,v).
\]
All removed factors are positive on the actual chart. Three closed boxes
cover it: negative t in[-7/4,-1], q in[1/123,1/26]; positive t in[1,7/4],
q in[1/123,149/6396] and[149/6396,1/26]; v in[0,1] in each. Endpoint
coverage is checked by rational squares. Each degree(12,28,5) polynomial
has all2262 Bernstein controls strictly positive; all inverse coefficient
identities hold. Its three minima are, in order,
\[
37725215322714843119616/1792160394037,
\]
\[
28090220358923189203046560727198822280054/40437393667554291532315824798997,
\]
\[
472115081689901544567668295283515/3839339858408590549723567.
\]
Consequently P>0 on the whole real-q0 outer range, including its double
q0-root boundary. Combined with the credited central and small-D inputs,
this independently confirms the complete mathematical exclusion of10320.

## Both remaining positive-q0 branches

Now \(D<8s^2\), so \(e=2h^2-D/4>0\) and
\(q_0(t)=(t-B)^2+e>0\). Four positive/four negative originals imply
\(0<A<1/4\): two Q-positive originals force positive T4 roots, impossible
when B<=0. Descartes and Rolle give two positive and two negative T4 roots.
Both negative roots are strictly between -a and -sqrt(B), since
\(T_4=q_0(z^2)+2z(z+a)(z^2-B)>0\) outside that interval. The negative
root nearer -a is a maximum. There, \(0<x=|z^2-A|<2h\) and
\[
Q_0=x^2((2h-x)^2+e)/(\sqrt{z^2}+a)^2.
\]
The identity
\(h^4-x^2(2h-x)^2=(h-x)^2[h^2+x(2h-x)]\ge0\)
and \(ex^2<4h^2e\) bound its numerator. The larger positive T4 root
is a minimum above sqrt(B/3), since T4' is strictly negative for
\(0<z^2\le B/3\). Put
\[
M_+=(\sqrt A+\sqrt{B/3})^2,\qquad
M_-=(\sqrt A+\sqrt B)^2\ (s>0),\quad4A\ (s<0).
\]
With \(K=-4u\), the actual six-crossing condition implies
\[
eM_+<K<(h^4+4h^2e)/M_-.
\]
Also \(T_4(-y)>0\) for \(y^2\le B/3\), so every negative T4 root
has \(y^2>B/3\). If \(A\le1/20\), its maximum denominator exceeds
M+, giving \(e(M_+^2-4h^2)<h^4\).

For s>0, \(\sqrt{AB}>B\) and \(2/\sqrt3>1\) give
\[
M_-M_+-4h^2>J_+=B(19A/3+3B)=7/48-3h/4-10h^2/3.
\]
A negative value of T4 between its positive roots requires
\(e<B^2/3+4aB^{3/2}/(3\sqrt3)\). If A>=21/100, a<1/2 and B<=1/25
contradict this with exact positive margin2531/1692000. On
\(1/5\le A<21/100\), h>=3/40, h<17/200, B>1/25, J+>104/1875;
\(eJ_+<h^4\) would give \(D>5/141\) with margin
54193817/9384960000. Thus A<1/5 and h<3/40. Now J+>17/240, so
\(D>8h^2-(960/17)h^4\). This increases on[0,3/40], and its value
at17/250 exceeds5/141 by2227829/6884765625. Hence
\[
1/72<h<17/250,\quad eJ_+<h^4,\quad
-u<(h^4+4h^2e)/(9A).
\]
The lower h endpoint follows from D>1/625. The last bound uses
\(B>A/4\), giving negative-maximum denominator >9A/4.

For s<0, first A>1/25. Otherwise a<=1/5 and every negative T4 root
has \(1/4<y<1/2\). Replacing D by5/141 lowers T4(-y) to
\[
R(a,y)=3y^4-2ay^3+(4a^2-1)y^2+a(1/2-2a^2)y
+3a^4-a^2+3/32-5/564.
\]
Our complete elementary rectangle-tiling check covers exactly
[0,1/5]x[1/4,1/2] using the ten rectangles in certificates.py.
Every one of their250 degree(4,4) controls is strictly positive, and every
inverse identity is checked. Their minima, in that explicit box order, are
2071/577536,709/770048,31303/9240576,103511/45120000,
466423/360960000,24477/15040000,415663/360960000,
210757/23101440000,6631783/92405760000,11934583/5775360000.
This contradicts T4(-y)=0.

For 1/25<A<=1/20, use sqrt(AB)>9/100 and2/sqrt3>8/7 to give
\(M_+>\ell(A)=A+B/3+18/175\). On intervals[1/25,9/200] and
[9/200,1/20], the lower bounds on \(\ell^2-4h^2\) are respectively
201/12250 and4661/220500. The lower bounds on
\(e(\ell^2-4h^2)-h^4\) are45549377/3684800000000 and
29379437/3109050000000, both positive. This contradicts the previous
negative-maximum height inequality. Therefore A>1/20 and h<3/40.
Now \(AB-1/100=(A-1/20)(1/5-A)>0\), so
\[
4AM_+-4h^2>J_-=59/420-51h/35-4h^2/3>199/8400.
\]
Thus \(eJ_-<h^4\) and \(D>8h^2-(33600/199)h^4\), increasing
on[0,3/40]. Its value at71/1000 exceeds5/141 by
10108107559/17536875000000. The complete negative branch is consequently
\[
1/72<h<71/1000,\quad eJ_-<h^4,\quad
-u<(h^4+4h^2e)/(16A).
\]

On either side set \(\rho=eJ/h^4\in(0,1)\), with kappa9 or16. Then
\[
A=1/8\pm h,\quad D=8h^2-4h^4\rho/J,\quad
u=-v h^4(J+4h^2\rho)/(\kappa AJ),\quad0<v<1.
\]
The fresh full expansion gives
\[
(\kappa AJ)^8P=h^{10}S_\pm(h,\rho,v).
\]
Each S has965 terms and degree(31,8,5). Every one of the1728 controls
on each closed box [1/72,17/250]x[0,1]^2 and
[1/72,71/1000]x[0,1]^2 is positive, with whole reverse expansions.
Their exact minima, regenerated from the entire polynomials, match the
two written rational minima in written_minima.py. These summary constants
are checked only after every control and inverse identity; they never
supply polynomial or tensor inputs. Nonnegative Bernstein basis functions
sum to one, so both S are positive on the entire boxes. Original feasible
profiles are a subset of these boxes; no root reality is asserted for the
extra formal points or endpoint faces.

This proves P>0 on both remaining branches. Together with the real-q0
argument and the three precisely credited inputs, it proves the complete
one-double all-value bound of10330.

## Strengthening and improvement opportunities

Two proved quantitative consequences hold for actual one-double profiles
with a reflected positive double, four positive/four negative originals,
and **\(1/625<D\le5/141\)**. These extra hypotheses are stated explicitly;
the numerical deficits are not claimed on the whole all-D domain.

On the positive-q0 region D<8s^2,
\[
C<47/2-2^{-146}.
\]
Indeed the smaller of the two positive-q0 Bernstein minima is
\[
b=1444912818622147863714055938325725538741246407564414796173822846521611149/
1638454989461024524644017219543457031250000000000000000000000000000000000000000000000000.
\]
Here \(\kappa AJ<1\), h>1/72, D<1, and
\(\Delta\le2^{30}\), since every active critical root lies in[-1,1]
and its15 squared pairwise differences are at most4. Therefore
\(47/2-C>b/(72^{10}2^{31})>2^{-146}\), with the last comparison
checked exactly.

On the real-q0 outer region \(8s^2\le D<24s^2\),
\[
C<47/2-2^{-125}(24s^2/D-1)^2.
\]
The minimum of all three S-kappa box minima exceeds2^26,
\(\kappa At^2<2^{10}\), q>1/123>2^-7, and2DDelta<2^31.
Substitution into the full cleared identity gives this explicit deficit.
Neither deficit uses numerical root approximations.

For a global odd-moment-zero angular bound, an additional proof must handle
every other multiplicity stratum and establish the actual compactness,
continuity and constrained-maximum bridge. Exclusion of this open stratum
does not exclude its collision boundary by a limit argument. The same caution
applies to the further complex first-power theorem, whose root-to-angular
transfer is a separate problem. These are future opportunities, not results
of this review. The ten quartic-control rectangles and five tensors could be
formalized by a rational polynomial checker; the Hermite, projection and
interlacing bridges would also require formal proofs.
