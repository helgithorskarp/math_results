# An unconditional leading-vector certificate at zero cubic moment

Actual **six-sendov-2**, role **researcher**. Complete ordinary algebraic
lemma with exact rational certificates, author checked, unformalized and
independently unreviewed. The input reductions are explicitly same-author
work. Their existing independent reviews do not review this new lemma.

## 1. Object and quantitative claim

Use the complete five transformed residuals
\(R(q,E,r,x,u)\in\mathbb Q[q,E,r,x,u]^5\) from
[9743](../critical-coefficient-recovery/PROOF.md), source
**9daf6c448bddfe865cc348709f517c95afc65fbb**. They come from
[9550](../degree-five-triangular/PROOF.md), source
**cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4**, by multiplying its five rows
by \((s^2,s,s^2,s,s^2)\) and setting

\[
q=B/s,\qquad x=s^2,\qquad u=st=p_4.
\]

For actual distinct real stationary original-root profiles,
[9695](../nonzero-quartic-mass/PROOF.md) proves this chart legal: \(x>0\),
\(u\ne0\), with the convention
\(s=\operatorname{sign}(u)\sqrt{x}\), \(B=qs\),
\(t=|u|/\sqrt{x}>0\). The signed variable \(u\) is retained.
The scalar \(E\) is the coefficient of \(z^3\) in the critical heptic;
it is different from the physical energy used in the complementary lane.
This scalar \(q\) is also different from first-power reciprocal coordinates.

Set

\[
c=\left(\frac{367}{360},-\frac r3-\frac{13}{96},0,-\frac1{48}\right),
\qquad F_i=R_{i+1}+c_iR_0=\alpha_i E+\beta_i\quad(0\le i<4).
\tag{1}
\]

All four entire \(\alpha_i,\beta_i\) are the pinned, fully regenerated
9743 polynomials. No lower stationary equation is a premise of the
following assertion.

**Theorem.** There are explicitly generated
\(L_0,\ldots,L_3\in\mathbb Q[r,x]\), of respective total degrees
\((4,3,5,4)\), and \(Z\in\mathbb Q[q,r,x,u]\), such that the whole identity

\[
\boxed{\quad\sum_{i=0}^3 L_i(r,x)\alpha_i(q,r,x,u)
       =u\{1+qZ(q,r,x,u)\}.\quad}                         \tag{2}
\]

holds. The full coefficients are reconstructed by [verify.py](verify.py)
and recorded in [expected.json](expected.json). Consequently:

1. For every finite **complex** \(r,x,u\), at \(q=0,u\ne0\),
   \(\alpha\ne0\), without any full stationary-equation or feasibility
   hypothesis. The polynomial assertion includes \(x=0\); this is only
   an algebraic extension, not an actual chart at \(s=0\).
2. For \(M\ge1\), \(|r|,|x|\le M\), \(q=0\),

   \[
   \|\alpha\|_2\ge\frac{|u|}{400000M^5}.                \tag{3}
   \]

   There is no upper bound on \(|u|\) in this assertion.
3. For \(M,U\ge1\), \(|r|,|x|\le M\), \(0<|u|\le U\),

   \[
   |q|\le\frac1{2000000M^5U}
   \quad\Longrightarrow\quad
   \|\alpha\|_2\ge\frac{|u|}{800000M^5}>0.              \tag{4}
   \]

The norms in (3)--(4) are Hermitian complex Euclidean norms. The constants
are explicit convenient bounds, with no optimality claim.

For either domain let \(a_*=|u|/(400000M^5)\) or
\(|u|/(800000M^5)\), respectively, and put

\[
D(M)=\sqrt{1+(367/360)^2+(M/3+13/96)^2+1/2304}.
\]

At fixed \((q,r,x,u)\), **every complex** \(E_1,E_2\) satisfies

\[
\|R(E_1)-R(E_2)\|_2\ge\frac{a_*}{D(M)}|E_1-E_2|,
\qquad
\|\partial_E R(E)\|_2\ge\frac{a_*}{D(M)}\quad\text{for all }E.
\tag{5}
\]

Thus the entire residual curve has an explicit scalar inverse bound on
its image. In particular it has at most one common \(E\), which is simple
in this scalar direction. No common root is needed for (5).

## 2. Leading-only constant-pivot reduction

The whole identities from 9743 are

\[
\alpha_i=\kappa_i u A_i,
\qquad(\kappa_0,\kappa_1,\kappa_2,\kappa_3)
=\left(\frac1{16934400},\frac1{4515840},
       \frac1{9408},\frac1{2257920}\right).
\tag{6}
\]

Each \(A_i(0,r,x,u)\) is affine in \(u\). Write it as
\(a_i(r,x)u+b_i(r,x)\). Specifically

\[
A_2=(d+7200q)u-K,
\qquad d=31304r+1162x+6165,\qquad K=118272.
\tag{7}
\]

The following three complete integer polynomials are obtained directly
from **leading** rows, in order \(i=0,3,1\):

\[
\begin{aligned}
dA_0(0)-a_0A_2(0)&=62720 f,\\
dA_3(0)-a_3A_2(0)&=87808 g,\\
dA_1(0)-a_1A_2(0)&=62720 j,
\end{aligned}                                                   \tag{8}
\]

where

\[
\begin{aligned}
f={}&-205919616r^2-798759752rx-142966224r
      +697198838x^2-311351805x-26263980,\\
g={}&-7983360r^2+26141800rx-5013360r
      -14207110x^2+8925849x-727650,\\
j={}&-68124672r^3+211172864r^2x-68656896r^2
      -123748352rx^2+162619640rx-22453200r\\
   &\quad+4629408x^3-53825666x^2+31300875x-2349270.
\end{aligned}                                                   \tag{9}
\]

No value of \(d\), an affine slope, \(r\), \(x\), or \(u\) is inverted
in (8). In particular, when \(d=0\), \(A_2(0)=-K\); this branch already
prevents all leading rows from vanishing if \(u\ne0\). The original
lower row \(\beta_2\) and the lower polynomial \(N\) used in the general
9743 stationary-root exclusion are **not used** in (8)--(9).

## 3. A short polynomial unit and its lift

Here is a complete defining recipe for the rational multipliers. Let
\(\mathcal M_d=\{(a,b):0\le a\le d,\ 0\le b\le d-a\}\), ordered by
increasing \(a\) and then increasing \(b\). Seek

\[
H_f f+H_g g+H_j j=1,
\qquad\deg H_f,\deg H_g\le3,\quad\deg H_j\le2.           \tag{10}
\]

Rows of a fixed integer matrix are indexed by \(\mathcal M_5\).
Its 26 columns are the complete coefficient vectors of
\(r^a x^b f\), then \(r^a x^b g\), for \((a,b)\in\mathcal M_3\), and
\(r^a x^b j\), for \((a,b)\in\mathcal M_2\). The right side is the
coefficient vector of 1. Exact rational elimination gives rank 21.
Choose all five free coordinates zero in its unique reduced system.
This defines \(H_f,H_g,H_j\) without any parameter-dependent division.

The checker reconstructs the **whole 21-by-26 matrix**, multiplies all
21 coefficient equations, and separately multiplies the full polynomial
identity (10). The full matrix, solution, and all three polynomials are
in the compact certificate. Therefore the proof does not depend on a
CAS solver's answer or merely on a reported rank or aggregate count.

Define

\[
\begin{aligned}
C_0&=dH_f/62720,& C_3&=dH_g/87808,& C_1&=dH_j/62720,\\
C_2&=-a_0H_f/62720-a_3H_g/87808-a_1H_j/62720,
& L_i&=C_i/\kappa_i.
\end{aligned}                                                   \tag{11}
\]

Equations (8) and (10) give the whole unit
\(\sum C_iA_i(0)=1\). Combining it with (6) gives
\(\sum L_i\alpha_i(0)=u\). All \(L_i\) depend only on \(r,x\).
Now define the polynomial

\[
Z=\frac{\sum L_i\alpha_i(q,r,x,u)-u}{qu}.                \tag{12}
\]

Every \(\alpha_i\) has a factor \(u\), and its specialization at \(q=0\)
gives the last unit. Thus (12) is an exact polynomial quotient by a
known monomial; it is defined even when \(q=0\) or \(u=0\) by that
polynomial. The checker verifies divisibility of **every monomial**,
constructs all 35 coefficients of \(Z\), and multiplies the whole (2).
There are no deleted zero-leading or special-parameter branches.

## 4. Exact height budgets and the tube

The four \(L_i\) have 13, 8, 19, and 12 nonzero coefficients. Write
\(\ell_i\) for the sum of their absolute rational coefficients. The
entire sums, not sampled evaluations, have integer ceilings

\[
(19823,23314,287768,115984),\qquad
\sum_i\ell_i^2<400000^2.                                \tag{13}
\]

Since their total degrees are at most 5, for \(M\ge1\) and
\(|r|,|x|\le M\), \(\|L(r,x)\|_2\le400000M^5\).
The entire coefficient absolute sum of \(Z\) has ceiling 514082,
hence is less than \(10^6\). Every monomial of \(Z\) has \(q\) exponent
at most 1, combined \((r,x)\) degree at most 5, and \(u\) exponent at
most 1. Thus, for \(|q|\le1\), \(|r|,|x|\le M\), \(|u|\le U\),
with \(M,U\ge1\),

\[
|Z|\le10^6 M^5 U.                                      \tag{14}
\]

For the width in (4), which is itself less than 1, \(|qZ|\le1/2\).
Apply the complex triangle inequality and Cauchy--Schwarz to (2):

\[
|u|/2\le|u(1+qZ)|
       \le\|L\|_2\|\alpha\|_2\le400000M^5\|\alpha\|_2.
\]

This proves (4). At \(q=0\), use \(|u|\) in place of \(|u|/2\) to
prove (3). No complex positivity of \(\sum\alpha_i^2\) is asserted.

For (5), let \(T_c=[c\mid I_4]\), the four-by-five map in (1).
For arbitrary complex \(c\), \(T_cT_c^*=I_4+cc^*\), hence
\(\|T_c\|=\sqrt{1+\|c\|_2^2}\le D(M)\).
The full cancellation (1) gives, for every pair of complex parameters,

\[
T_c\{R(E_1)-R(E_2)\}=\alpha(E_1-E_2),
\qquad T_c\partial_E R(E)=\alpha.
\]

The operator norm bound proves both statements. This scalar estimate
does not prove independence of an additional parameter derivative.

## 5. Real recovery and original-root interpretation

On the real part of (3) or (4), \(S=\sum\alpha_i^2>0\) is automatic.
With \(T=\sum\alpha_i\beta_i\), \(U_\beta=\sum\beta_i^2\) and
\(R_0=2u^2E^2+\ell_0E+c_0\), the **complete** remaining conditions for
the five scalar rows to have a common real \(E\) are still

\[
SU_\beta-T^2=0,\qquad
2u^2T^2-\ell_0TS+c_0S^2=0,\qquad E=-T/S.                \tag{15}
\]

This is the credited 9743 predicate, independently confirmed in
[9781](../../six-reviewer-1/coefficient-recovery-audit/REVIEW.md), source
**68bf078a7be12dd34ee684b76e0f8e80c2a72c61**. Both cleared equations
remain required. The defined candidate \(-T/S\) does not itself certify
a common root. Outside the stated tube, \(S>0\) remains an independent
condition; this lemma makes no unrestricted-\(q\) assertion.

Original-root interpretation also retains \(x>0,u\ne0\), the signed
chart, all seven simple real critical roots and strict mass positivity,
with the complete [9496](../mass-stationary-chart/PROOF.md) and
[7432](../constant-term-angular-reduction/PROOF.md) reduction. In the
balanced eight-original-root normalization the critical heptic is
\(h=z^7-3z^5/8+Bz^4+Ez^3+\cdots\), and Newton identities give
\(\sum a_i^3=-24B/5\). Thus \(q=0\) in the legal chart is precisely
zero original cubic moment. This does not assume a symmetric root set.

This proves a useful coefficient-regularity and stability frontier around
that slice, not existence or classification of stationary profiles,
collision limits, full Jacobian rank, a sharp basin constant, or the
complex first-power inequality. No historical priority is claimed for
the classical module-unit or coefficient-height method.

## 6. Evidence boundary

The standard-library checker byte-pins both 9743 source files and
regenerates its complete typed record and all pinned parents. It then
regenerates every (8)--(14) polynomial and constant system and compares
the whole typed certificate. It checks the signed negative-\(u\),
\(d=0,x=0\) algebraic branch and the necessary exclusion \(u=0\).
Deliberate changes to a trailing matrix solution, polynomial unit,
original module multiplier and full defect are rejected by exact
coefficient identities. No optimization-sensitive assertions are used.

Separate same-author discovery used exact SymPy 1.14.0 arithmetic,
first through resultants and a longer unit, then through the smaller
coefficient system. The final certificate reconstructs the shorter unit
using Python rational elimination and multiplies every coefficient; it
does not import discovery data or require SymPy. Matching these different
arithmetic routes is author validation, not an independent review.
The ordinary polynomial, norm and original-root interpretation arguments
remain outside a proof assistant.
