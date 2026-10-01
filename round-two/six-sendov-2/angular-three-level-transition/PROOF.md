# Sharp three-level angular ratio and a finite attained transition constant

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact rational polynomial certificates;
unformalized, independent review pending. The global constant below is
proved finite and attained, but its numerical value and equality set on
the full sphere remain open.

The [previous asymmetric obstruction](../asymmetric-angular-obstruction/PROOF.md),
source `9b33444a3e8478d3f056b615caf499525cfcd524`, graph8702, disproved
the proposed universal208/9 extension. This work gives the sharp constant
on **all profiles with at most three distinct original slopes**, proves
that its maximizing orbit is strictly stable against every tangent
direction in the full sphere, and establishes a compact global
variational formulation. No reduction of four-or-more-level profiles
to this orbit is asserted. These are original-root angular statements,
not a proof or counterexample of the first-power Tang--Zhang conjecture.

## 1. Statements

Let
\[
\mathcal S=\{\theta\in\mathbb R^8:\sum\theta_j=0,
                         \ \sum\theta_j^2=1\},\quad
e=\mathbf1/\sqrt8,\quad P=I-ee^T,
\]
\[
H=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
w=\operatorname{diag}(\theta)e,\quad
X=\sum\theta_j^4,\quad
\rho_\lambda=8\|\Pi_\lambda w\|^2,\quad
\eta=\sum_{\lambda\ {m distinct}}\rho_\lambda^2.
\]
Use full eigenspace projections, including at collisions. Let
\(\mathcal U\) be the finite orbit of the four-positive/four-negative
equal-magnitude profile. For \(\theta\notin\mathcal U\) set
\[
             C(\theta)=\frac{1-\eta}{X-1/8}.                 \tag{1}
\]

**Theorem 1 (uniform extension and true transition).** The function C
extends continuously to all of \(\mathcal S\), with value16 on
\(\mathcal U\). Its maximum
\[
                  C_*=\max_{\mathcal S}C
\]
is finite and attained away from \(\mathcal U\). Define
\(J_R=RX-\eta\). The uniform orbit is globally maximizing for J_R
exactly when \(R\le-C_*\). For \(R<-C_*\) it is the complete equality
set; at \(R=-C_*\) the equality set is
\(\mathcal U\cup\operatorname{argmax}C\). For
\(-C_*<R<-16\), the uniform orbit is strictly locally maximizing and
globally suboptimal. This interval is nonempty by Theorem2.

**Theorem 2 (complete three-level optimum).** Let alpha be the unique root
in
\[
 I_\alpha=\left[-\frac{853410556973738}{10^{15}},
               -\frac{853410556973736}{10^{15}}\right]
\]
of
\[
 Q(t)=4575t^4+11695t^3+11175t^2+4737t+746.                \tag{2}
\]
Put
\[
 c_3=\frac{8(\alpha-1)^2(5\alpha+3)^2}
 {(15\alpha^2+24\alpha+10)(35\alpha^2+38\alpha+11)}.
\tag{3}
\]
Then on all balanced norm-one profiles with at most three distinct
slopes, including the extended values at uniform,
\[
\boxed{C\le c_3,\qquad
       24.53389668<c_3<24.53389670.}                      \tag{4}
\]
Equality consists exactly of permutations and sign changes of the
normalization of
\[
        u_\alpha=(\alpha,\alpha,\alpha,\alpha,
                         1,1,1,-4\alpha-3).
\tag{5}
\]
In particular \(C_*\ge c_3>49/2\). The number c_3 is the unique root
in the interval (4) of
\[
20667c^4-50108c^3-7974720c^2-103317504c+587202560=0.
\tag{6}
\]
The symbol c_3 denotes the three-level constant, not the older marked
radius \(a_3\) in graph8672.

**Theorem 3 (full-sphere local stability).** Let \(\mathcal O_3\) be the
finite normalized orbit in (5). There are \(\epsilon,b>0\) such that
\[
\boxed{\operatorname{dist}(\theta,\mathcal O_3)<\epsilon
\ \Longrightarrow\
c_3-C(\theta)\ge b\operatorname{dist}(\theta,\mathcal O_3)^2.}
\tag{7}
\]
The neighborhood and coefficient are existential, not computed. This
is local stability in the full six-dimensional balanced sphere,
including directions which split either repeated original block.
It does not prove \(C_*=c_3\).

**Exact integer benchmark.** The normalization of four copies of -64,
three copies of75, and one31 has
\[
 N=34220,\quad X=\frac{8147713}{58550420},\quad
 \eta=\frac{1585881829}{2429842430},\quad
 C=\frac{27899524}{1137183}>49/2,
\tag{8}
\]
\[
 \eta-1+24(X-1/8)=-\frac{18365743}{2429842430}<0.          \tag{9}
\]
Thus even24 is too small for the universal angular constant. No
stationarity of this rational benchmark is claimed.

## 2. Spectral preliminaries and continuity

These definitions and the collision mechanism were already proved in
[graph7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and independently checked in
[review7496](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).
Here is the part needed for a self-contained variational argument.

The masses rho are nonnegative and sum to1, because
\(8\|w\|^2=1\). Hence \(0\le1-\eta\le6/7\).
For the polynomial \(f(z)=\prod(z-\theta_j)\), the characteristic
polynomial of H is \(g=f'/8\), by the cofactor identity
\[
\det(zI-H)=f(z)e^T(zI-\operatorname{diag}\theta)^{-1}e=f'(z)/8.
\]
If the distinct original levels are \(r_i\) with multiplicities m_i,
g has \(r_i\) as a root of multiplicity \(m_i-1\), and precisely one
simple root in each gap between successive distinct levels. Indeed
\(\sum_i m_i/(z-r_i)\) has strictly negative derivative and goes from
positive infinity to negative infinity in each gap. The eigenspace
at an original level consists of vectors supported on that block
with coordinate sum zero, and is orthogonal to w. In particular
**every repeated compression eigenspace has zero w projection**.

If a sequence of profiles converges, fixed small contours isolate the
limiting compression clusters. A simple limiting eigenspace has a
continuous projection. A repeated limiting cluster has zero total
w-mass; its nonnegative constituent masses sum to a quantity tending
to zero, so the sum of their squares tends to zero as well. This proves
continuity of eta at every profile, without selecting an eigenbasis
inside a repeated eigenspace.

Also
\[
 X-1/8=\sum_j(\theta_j^2-1/8)^2\ge0.                    \tag{10}
\]
Equality in (10) and balance force exactly four signs of each type,
so its zero set is precisely \(\mathcal U\). C is continuous away
from that finite set.

For a balanced unnormalized u, write
\[
 N=\sum u_j^2,\quad S_k=\sum u_j^k,\quad
 \rho_i^u=8\|\Pi_i\operatorname{diag}(u)e\|^2,
 \eta_u=\sum(\rho_i^u)^2,\quad \delta_u=S_4-N^2/8.
\]
Then \(\eta=\eta_u/N^2\), \(X=S_4/N^2\), and
\(C=(N^2-\eta_u)/\delta_u\). The elementary moment identities are
\[
 \sum\rho_i^u=N,\qquad \sum\rho_i^u\lambda_i=S_3,
 \sum\rho_i^u\lambda_i^2=\delta_u.                     \tag{11}
\]
They follow respectively from the norm of w, its H quadratic form,
and \(8\|P\operatorname{diag}(u)w\|^2\).

## 3. The uniform limit16 in every tangent direction

Fix \(s=(1,1,1,1,-1,-1,-1,-1)\). A full local chart near
\(s/\sqrt8\) is
\[
 \theta(v)=\frac{s+v}{\sqrt{8+q}},\qquad
 q=\|v\|^2,\quad \sum v_j=\sum s_jv_j=0.
\tag{12}
\]
Thus each four-coordinate block of v has sum zero. Put
\(H(v)=P\operatorname{diag}(s+v)P|_{e^\perp}\).
At zero its spectrum is -1 (rank3),0 (rank1),1 (rank3); the zero
unit eigenvector is \(\xi_0=s/\sqrt8\). For \(\|v\|<1/4\),
fixed disjoint contours give analytic projections \(\Pi_-,\Pi_0,\Pi_+\)
of these ranks. The operator perturbation has norm at most \(\|v\|\),
so the spectral separation persists uniformly in this ball.

The first differential of the simple zero eigenvector in direction v
is \(-v/\sqrt8\), and its eigenvalue differential is zero. To verify,
\(P\operatorname{diag}(v)s=s\cdot v\) and
\(H(0)v=s\cdot v\); the eigenvector differential equation and
normalization therefore hold, since v is orthogonal to s. Differentiating
\(\Pi_\pm(v)\xi_0(v)=0\) consequently gives
\[
 \Pi_\pm'(0)[v]s=\Pi_\pm(0)v=v_\pm,
 \quad \Pi_\pm(v)(s+v)=2v_\pm+O(\|v\|^2).             \tag{13}
\]
The constants are uniform over all tangent directions. Since
\(\sqrt8 w_u=s+v\), the total normalized masses in these two clusters
are
\[
 T_\pm=\frac{\|\Pi_\pm(v)(s+v)\|^2}{8+q}
             =\frac12\|v_\pm\|^2+O(\|v\|^3).
\]
Their individual squared masses sum to at most \(T_\pm^2=O(q^2)\).
The simple central mass is \(1-T_+-T_-\), exactly. It follows that
\[
             1-\eta=q+O(\|v\|^3).                    \tag{14}
\]
The root moment computation is independently explicit:
\[
 X-1/8=\frac{4q+4\sum s_jv_j^3+\sum v_j^4-q^2/8}{(8+q)^2}
                =q/16+O(\|v\|^3).                   \tag{15}
\]
For v small the denominator in (1) is at least q/32, so (14)--(15)
give \(C(\theta(v))=16+O(\|v\|)\), uniformly. Permutation symmetry
handles every uniform profile. This proves the continuous extension.

Compactness of the sphere then makes C finite and attained. Theorem2
gives a value above49/2, so no maximizer is uniform. For every
nonuniform profile the exact comparison is
\[
     J_R(\theta)-(R/8-1)=(X-1/8)(R+C(\theta)).          \tag{16}
\]
Equation (16) proves all global assertions in Theorem1. Equations
(14)--(15) also give
\[
 J_R(\theta(v))-(R/8-1)=(R+16)q/16+O(\|v\|^3),
\]
so uniform is strictly locally maximizing for every fixed R<-16.

## 4. Complete reduction for at most three original levels

A balanced two-level profile has only one nonzero compression mass,
so eta=1. Its C value is zero unless it is uniform, where the extended
value is16. A nonzero one-level balanced profile is impossible.

For three levels with multiplicities \((m,n,k)\), relabel blocks so
this triple is one of
\[
 (4,3,1),\ (4,2,2),\ (5,2,1),\ (3,3,2),\ (6,1,1).
\]
Normalize the second level to1 when it is nonzero. The other levels
are \(t,-(mt+n)/k\). The case of second level zero is the point at
infinity of this real projective chart and is included below.
If \(a_1,a_2,a_3\) denote these levels, the displayed compression
quadratic after removal of block factors is
\[
 h(z)=\frac18\sum_{i=1}^3 m_i\prod_{j\ne i}(z-a_j)
     =z^2-Tz+B,\qquad T=a_1+a_2+a_3,\quad D=T^2-4B.
\]
For three distinct levels its two roots are simple, real and active.
The first two equations of (11) uniquely determine their weights, giving
\[
 \eta_u=\frac{N^2}{2}+\frac{(2S_3-NT)^2}{2D},\qquad
 C=\frac{N^2D-(2S_3-NT)^2}{2D\delta_u}.                \tag{17}
\]
At coinciding levels (17) extends by the two moments: the displayed h
still has two distinct real roots, one inactive with zero mass. At the
uniform profile the C ratio is removable as shown in Section3.

Expanding moments in (17) gives these **identities for all real t**
after the indicated removable extensions:

| Multiplicities | C(t) | Value at infinity |
|---|---|---|
|4,3,1|\(8(t-1)^2(5t+3)^2/[(15t^2+24t+10)(35t^2+38t+11)]\)|8/21|
|4,2,2|\(8(t-1)^2(3t+1)^2/[(3t^2+4t+2)(9t^2+2t+1)]\)|8/3|
|5,2,1|\(20(t-1)^2(3t+1)^2(5t+3)^2/[(21t^2+22t+6)(1035t^4+1700t^3+1010t^2+260t+27)]\)|100/483|
|3,3,2|\(6(t-1)^2(3t+5)^2(5t+3)^2/[(5t^2+8t+5)(5t^2+14t+13)(13t^2+14t+5)]\)|54/13|
|6,1,1|\(4(t-1)^2(3t+1)^2(7t+1)^2/[(28t^2+18t+3)(721t^4+492t^3+118t^2+12t+1)]\)|63/721|

All displayed denominators are strictly positive. Each quadratic has
positive leading coefficient and negative discriminant. The quartics
in the521 and611 rows are respectively \(2\delta_u\) and
\(2\delta_u/3\). Their multiplicity triples cannot combine into4+4,
so (10) makes delta strictly positive for every t.
For431, \(\delta_u=6(t+1)^2(35t^2+38t+11)\);
for422, \(\delta_u=2(t+1)^2(9t^2+2t+1)\).
At t=-1 the displayed ratios take the removable value16.

## 5. Exact comparison and root certificates

The422 row is at most16 because sixteen times its displayed denominator
minus numerator is
\[
                    24(t+1)^2(15t^2+2t+1)\ge0.
\]
For the other three non431 rows the same differences, after removing
a positive constant factor, are
\[
\begin{split}
P_{521}={}&28605t^6+78010t^5+86975t^4+50620t^3
                           +16251t^2+2762t+201,\\
P_{332}={}&1925t^6+12530t^5+34955t^4+48636t^3
                           +34955t^2+12530t+1925,\\
P_{611}={}&80311t^6+107478t^5+57549t^4+15588t^3
                           +2289t^2+198t+11.
\end{split}
\]
Each has no real root and is positive at zero. The exact Sturm
algorithm in the checker uses p,p', then negative Euclidean remainders,
each rescaled by a positive leading-coefficient magnitude. Its variation
counts at minus infinity and plus infinity are **3,3 for every one of
these three sextics**. Hence all three are strictly positive everywhere.
This is a finite exact algebraic certificate, not a numerical minimum.

For the431 row F(t), direct differentiation gives
\[
 F'(t)=\frac{16(t-1)(5t+3)Q(t)}
              {(15t^2+24t+10)^2(35t^2+38t+11)^2}.       \tag{18}
\]
The Sturm variation counts for Q at minus infinity and plus infinity
are3 and1. Besides alpha in (2), its only real root beta lies in
\[
 I_\beta=[-443370119245/10^{12},-443370119244/10^{12}].
\]
At the two ends of I_alpha the variation counts are3,2; at the ends
of I_beta they are2,1. Exact rational interval evaluation gives (4)
for F(alpha) and \(4<F(\beta)<5\). The other stationary values,
at t=1 and t=-3/5, are zero. The infinity value is8/21. Thus alpha
is the unique global maximizing projective parameter. This proves
the equality classification, and all other multiplicity types stay
below16<c_3.

For (6), put \(n=8(t-1)^2(5t+3)^2\) and
\(d=(15t^2+24t+10)(35t^2+38t+11)\). The polynomial
\(d^4 P(n/d)\), with P the polynomial in (6), has zero remainder
on division by Q. The checker verifies this identity exactly and
the single root of P in (4) by Sturm. This supplies (6) without
depending on a printed computer-algebra resultant.

## 6. Every transverse splitting direction is stable

Work around (5) before normalization. Two simple active compression
roots stay separated from the inactive rank3 and rank2 clusters at
the original levels alpha and1. Drop the squared masses of those two
clusters to define a smooth **upper** bound
\[
 C^+(u)=\frac{N^2-\rho_1(u)^2-\rho_2(u)^2}{\delta_u}\ge C(u).
\tag{19}
\]
The active roots and projections are analytic in all eight coordinates;
delta is positive locally. The dropped cluster masses are O(distance^2),
so \(C^+-C=O(\mathrm{distance}^4)\). On the three-level stratum the
dropped masses vanish exactly and \(C^+=F(t)\).

The tangent space to the balanced normalized sphere decomposes under
the block permutation group \(S_4\times S_3\) into three pairwise
inequivalent real representations: the three-dimensional sum-zero
fourfold block, the two-dimensional sum-zero threefold block, and the
one-dimensional block-constant tangent. An invariant linear form
vanishes on the first two; (18) makes it vanish on the third at alpha.
Thus the full gradient of C^+ is zero. Its invariant Hessian has no
mixed terms between these representations and is scalar on each
sum-zero block. One pair splitting in each block, and the F'' direction,
therefore determine its definiteness.

Here are universal rational splitting certificates. Set
\[
 f=(z-t)^4(z-1)^3(z+4t+3),\quad g=f'/8,
 \quad d=(15t^2+24t+10)(35t^2+38t+11).
\]
Replace two entries of a block at r by r+epsilon,r-epsilon, with
r=t or r=1. Then
\(f_\epsilon=f+\epsilon^2 f_2\),
\(f_2=-f/(z-r)^2\), and \(g_2=f_2'/8\). For a persistent active
root lambda of g,
\[
 \lambda_2=-g_2/g',\quad \rho_0=-8f/g',
\]
\[
 \rho_2=-8f_2/g'+8fg_2'/(g')^2
             +\lambda_2\{-8f'/g'+8fg''/(g')^2\}.        \tag{20}
\]
All expressions are evaluated at lambda. The last derivative is the z
derivative of the rational expression BEFORE reduction modulo h.
Equation (20) follows by implicit differentiation of the simple root
and residue formula. The new near-block eigenvalues have squared
mass contribution O(epsilon^4), so do not enter the quadratic term.
Compute \(\eta_2=\sum 2\rho_0\rho_2\) by polynomial arithmetic
modulo the active quadratic h, and use
\[
 N_\epsilon=N+2\epsilon^2,\quad
 S_{4,\epsilon}=S_4+12r^2\epsilon^2+O(\epsilon^4).
\]
The coefficient of epsilon^2 in C^+ is
\[
\begin{split}
 L_4(t)&=\frac{4A(t)}{3(t+1)d^2},&
 A(t)&=117375t^7+470475t^6+872170t^5+993954t^4\\
 &&&\quad+751299t^3+366599t^2+103380t+12684,\\
 L_3(t)&=\frac{4B(t)}{9(t+1)d^2},&
 B(t)&=496875t^7+1685625t^6+2646100t^5+2726970t^4\\
 &&&\quad+2064611t^3+1074965t^2+326238t+42424.
\end{split}                                                   \tag{21}
\]
The identities hold on the generic distinct-level chart; alpha is
strictly inside it. Normalizing the split profile does not change C,
since the unnormalized ratio is homogeneous of degree zero.
The checker derives (20) in \(\mathbb Q(t)[z]/h\), compares (21) as
rational functions, and proves both signs are negative on I_alpha.
Their approximate values at alpha are -111.9143 and -293.1363; these
decimals are descriptive, with rational interval signs as the certificate.
It also certifies \(Q'(\alpha)<0\). In (18), both linear factors
are negative at alpha, hence \(F''(\alpha)<0\).

All three Hessian blocks of C^+ are therefore negative definite.
Taylor's theorem on the full sphere gives a strict quadratic upper
bound around the orbit. Equation (19) transfers it to C, proving (7).
This smooth-majorant mechanism is credited to the prior
[triple persistence proof](../triple-angular-persistence/PROOF.md),
source `4587f5f3776a0ec8c22d43ec8b264c8b48915218`; the asymmetric
ratio, block decomposition and splitting formulas here are different.

## 7. Exact scope of the code

Run `python3 -B verify.py` or `python3 -B -O verify.py` in this directory.
The pure standard-library checker regenerates all five universal ratio
identities from weighted root moments, projective infinity values,
the stationary derivative, real-root/Sturm counts, rational isolations,
the constant-polynomial divisibility, the all-parameter residue
splitting formulas, a separate2x2 companion trace, the integer benchmark,
and the entire linearized uniform tangent calculation on a basis with
its full quadratic Gram form. It rejects four damaged certificates.
The small `expected.json` is a regression record, not a trusted root list.

The code checks the finite algebraic portion. The separation of spectral
projections, collision continuity, uniform remainders, compactness,
representation decomposition and local-to-orbit Taylor bound are the
written arguments above. No numerical search, solver nonexistence claim,
proof assistant, external certificate or omitted large corpus is used.
The full C_* value, its support reduction/equality classification, an
effective stability neighborhood, and the finite-energy first-power
endpoint remain unresolved.
