# Independent entry, clipping and product-cap lemmas

Actual **six-reviewer-5 / independent reviewer**, 2026-10-05.
This component supplies the ordinary reductions and all 73 closed
energy-entry cells, clipping/path argument, necessary cover enclosures
and product-cap proof independently paid in pass 69. PROOF.md completes
the separate 139 face inequalities and proves the sufficient gap 1/340.
The mathematical section below is byte-exact from the earlier independent
proof; historical private progress and unpaid-work notes are omitted.

## Completed ordinary reductions

After rotation let \(a\in[2/3,27/40]\), and put
\(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\),
\(F=\sum r_j\), \(u=\operatorname{Re}(\sum q_j/8)\),
\(w=\operatorname{Im}(\sum q_j/8)^2\),
\(E=\sum|q_j-1|^2\), \(T=\sum(r_j-1)^2\).
The two channel polynomials are

\[
J_a(q)=\int_0^1\prod_{j=1}^8(a+(1-a^2)tq_j)\,dt,
\qquad O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt.
\]

For a monic original polynomial, integrating its derivative from a to0
and a to1/a gives respectively
\(O_a(q)=\prod z_k\prod q_j\) and
\(J_a(q)=\prod(1-az_k)/(a-z_k)\), with eight original nonmarked
roots \(z_k\). The marked root is simple when all reciprocals are finite.
Gauss--Lucas supplies \(r_j\ge m_a=1/(1+a)\). The identity
\(|1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)\ge0\) supplies
\(|J_a(q)|\ge1\); original disk containment supplies
\(|O_a(q)|\le P:=\prod r_j\). These are ordinary polynomial and
disk arguments, not assertions about clipped or arbitrary formal tuples.

The published mathematical exclusion \(F\le8\) on the same annulus
from10274 remains an explicit theorem premise. Its committed independent
review10284 is provenance for that premise, not a verdict on10300 or a
numeric/checker input here. This pass did not re-audit that parent proof.

## Complete energy-entry payment at mass eight

For a formal tuple with \(F=8\) and the per-a radius floor, write
\(r_j=m+x_j\), \(m=40/67\), \(x_j\ge0\),
\(\sum x_j=8(1-m)\). Concentrating a fixed nonnegative sum bounds
\(T\le56(1-m)^2=40824/4489\). The checker covers its ENTIRE closed
interval with the73 consecutive cells
\([k/8,\min((k+1)/8,40824/4489)]\), including the last endpoint.

For a cell \([L,U]\), let
\(\delta=\lfloor1024\sqrt{L/56}\rfloor/1024\) and
\(D=\min(\lceil256\sqrt{7U/8}\rceil/256,7-7/(1+27/40))\).
Centering the real radii and Cauchy--Schwarz show both D bounds are
valid for every \(r_j-1\). The quadratic Hermite majorant for
\(\log(B+ye)\), anchored at \(-\sqrt{T/56}\) twice and
\(7\sqrt{T/56}\), is an upper majorant because its third derivative
is nonnegative and \(e\le7\sqrt{T/56}\). Summing it gives the
one-large/seven-small radial product bound at mass8. This argument
requires positive factors, which hold under the checked radius budgets.

The exact affine envelope has \(h=27/40\), \(c=197/360\):

\[
h+cx-[a+(1-a^2)x]=(1-x)(h-a)+x(a-2/3)(a+2/3-1)\ge0.
\]

The decreasing factor \((1+7x)(1-x)^7\) therefore bounds the radial
product by
\(R_L(t)=[h+(c+7b_-\delta)t][h+(c-b_-\delta)t]^7\),
where \(b_-=871/1600\). If \(E\ge23/5\), the identity
\(E=T+2(F-8u)\) supplies the phase floor
\(P_L=\max(0,(23/5-U)/2)\). For
\(\widehat C=h+(5/9)(1+D)t\), a positive truncated reciprocal
series about t=1 lower-bounds \(\widehat C^{-2}\) by G2. Thus the
phase logarithmic loss is at least
\(K(t)=(23517/64000)P_LtG2(t)\ge0\).
The phase argument is decreased BEFORE using
\(e^{-K}\le1-K+K^2/2\); no monotonicity of that Taylor polynomial
is assumed.

Every19-coefficient vector of \(R_L(1-K+K^2/2)\) was independently
computed by convolution and by direct binomial choices. Every integral
also agrees with the unexpanded exact beta-integral basis
\(\int t^i(1-t)^j=i!j!/(i+j+1)!\). ALL73 upper integrals are
STRICTLY below49/50. Hence at mass8,
\(|J_a(q)|\ge49/50\) implies \(E<23/5\), and the exact coupling
\(E=T+16(1-u)\) further implies \(u>57/80\).
No continuum conclusion was inferred from point samples or hashes.

## Completed coupled continuity lemma

Suppose the original channels and radius floor hold and
\(F=8+\Delta\), \(0<\Delta\le\epsilon\). Define

\[
h_j=\frac{\Delta(r_j-m_a)}{8+\Delta-8m_a},\qquad
q'_j=(1-h_j/r_j)q_j.
\]

The denominator exceeds \(\Delta\), since its difference is
\(8(1-m_a)>0\). Thus \(0\le h_j\le r_j-m_a\),
\(\sum h_j=\Delta\), \(\sum|q'_j|=8\), and
\(|q'_j|\ge m_a\). Along the radial path
\(q(v)=q'+v(q-q')\), each radius stays above \(m=40/67\), total
radius stays below \(S_0=8+\epsilon\), and total path displacement
is exactly \(\Delta\). Intermediate tuples need not arise from a
disk polynomial. Complex differentiation applies because both channels
are entire multilinear polynomials in the eight complex coordinates.

Removing one slot leaves seven radii summing to at most \(S_0-m\).
Triangle inequality followed by seven-factor AM--GM gives the uniform
slot-gradient bound

\[
L_J(\epsilon)=\frac59\int_0^1t\left[\frac{27}{40}
+\frac59\frac{S_0-m}{7}t\right]^7dt.
\]

All eight coefficients and the integral agree with a separate endpoint
antiderivative. For \(\epsilon=1/350\),

\[
L_J=\frac{27781636576488695471440375009838692706627}
{47721041299281141974204149751414784000000}<7/12.
\]

Consequently \(|J(q')|\ge1-L_J\epsilon>1-1/600>49/50\).
The completed energy-entry gate gives \(E'<23/5,u'>57/80\) BEFORE
either is used to estimate the origin derivative. This ordering is
noncircular.

Let \(R=S_0-7m\). Differentiating E along the entire path bounds its
absolute derivative by \(2(R+1)\Delta\), without choosing its sign.
The real mean changes by at most \(\Delta/8\). Thus uniformly
\(E(v)\le E_+=23/5+2(R+1)\epsilon\) and
\(u(v)\ge u_-=57/80-\epsilon/8>0\).
For x=at the ENTIRE removed-slot identity is especially transparent as

\[
\sum_{j\ne k}|1-xq_j|^2
=8-16xu+x^2(E+16u-8)-|1-xq_k|^2.
\]

Discard only the nonpositive final square. Since x<1, the coefficient
of u is nonpositive. Use the uniform E and u bounds and then the marked
endpoints. The compensated coefficient is exactly
\(E_++16u_--8=8+2R\epsilon>0\). This gives the average-square bound

\[
B(t)=\tfrac17[8-16(2/3)u_-t+(27/40)^2(8+2R\epsilon)t^2].
\]

Its quadratic coefficient is positive, \(B'(1)<0\), and \(B(1)>0\).
Therefore B is positive and decreasing on ALL[0,1], at most8/7.
With c=107/100, \(c^2>8/7\), and squared-modulus AM--GM gives
\(\prod_{j\ne k}|1-atq_j|\le cB(t)^3\). The ENTIRE signed cubic
agrees by convolution and direct multinomial enumeration, and its full
weighted integral gives

\[
L_O=9(27/40)c\int_0^1tB(t)^3dt
=\frac{3462092984820154424398922887241609907}
{3107039206948096000000000000000000000}<6/5.
\]

Write \(P'=\prod|q'_j|\le1\). Eight-factor AM--GM, retaining every
factor, gives \(P/P'\le A=(1+\epsilon/(8m))^8\). The original
origin-channel upper bound, integrated path-gradient estimate and
\(P'\le1\) therefore give

\[
|O(q')|\le P'+(A-1)+(6/5)\epsilon,
\qquad (A-1)+(6/5)\epsilon
=\frac{203631080250785146637137538224254964641}
{24759631762948096000000000000000000000000}<1/100.
\]

These completed estimates would contradict the target's origin/polar
face bounds IF all those bounds are independently established. They do
not establish those remaining bounds by themselves.

## Closed cover and necessary enclosures

The exact defining COVER.json was compared against the pinned source
and complete Git object before mathematical input. A separate closed-tree
recursion checks canonical rational text, axes as integers (rejecting
bool), strict interior cuts, both common CLOSED cut faces, unchanged
other coordinates, unique reachability and exact root. It reaches277
nodes,138 internal splits and139 leaves, maximum depth13. There are79
scalar-origin,9 retained-mean-origin,2 standard-polar and49 joint-polar
roles. These labels declare intended payments; they do not verify them.

All139 leaves have independently computed four ordered necessary
intersections, exact T intervals and radial-product upper caps. Each
intersection only shrinks the enclosing endpoints according to the
coupling identities and \(|\mu|\le1\); none is a feasibility converse.
The product cap uses the exact scalar derivative identity
\(Rx f'(x)=(x-1)(R-x)\) for
\(f(x)=x-1-(x-1)^2/(2R)-\log x\), R>=1. It follows that
\(\prod r_j\le e^{-T/(2R)}\) at mass8. The five-term LOWER bound
on \(e^{T/(2R)}\), then its reciprocal, gives the rational UPPER
product cap. Both complete five-term representations agree.

The entry component concludes here; PROOF.md proves its complementary face.
