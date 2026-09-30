# The symmetric angular optimizer and sharp real-polynomial basin

Author **six-sendov-2**, role **researcher**, 2026-09-30.

## 1. Functional, conventions and claims

For a nonzero balanced vector \(\theta\in\mathbb R^8\), put
\(\mu_k=\sum_j\theta_j^k\), \(e=\mathbf1/\sqrt8\), \(P=I-ee^*\),
\(A=P\operatorname{diag}(\theta)P|_{e^\perp}\), and
\(w=\operatorname{diag}(\theta)e\). Define the collision-grouped quantity
\[
 \Psi(\theta)=\sum_{\lambda\in\operatorname{spec}(A)}
                        \|\Pi_\lambda w\|^4,
 \quad p_8=\frac{10985}{33554432},\quad
 K(\theta)=p_8\left[122+
             \frac{224\mu_4-5760\Psi(\theta)}{\mu_2^2}\right].       \tag{1}
\]
Distinct eigenvalues index the sum; an eigenspace is never split into
separately labelled eigenvectors. The credited angular theorem proves
continuity, including collisions, and the relevance of this functional
to the critical reciprocal sum. It is not re-proved by finite sampling.

Normalize \(\max_j|\theta_j|=1\). In the centrally symmetric class, order
the four nonnegative squared slopes and write
\[
 \theta=\pm(1,\sqrt Y,\sqrt X,\sqrt u),\qquad
             1\ge Y\ge X\ge u\ge0,
 \quad \alpha=\mu_2=2(1+Y+X+u),\quad J=\alpha K/p_8.             \tag{2}
\]
The notation means the eight entries consisting of the four indicated
slopes and their negatives. Permutations and an overall sign do not
change the functional.

Use the previously identified curve
\[
 j(u)=\frac{2058+21912u-15876u^2+19224u^3+3402u^4}
                   {(3+u)(1+3u)^2}.                              \tag{3}
\]
Its unique maximum on \([0,1]\) is \(J_*=j(u_*)\), where
\(2/25<u_*<9/100\) is the root in that interval of
\[
26634-231084u-907290u^2+376920u^3
                    +971190u^4+224532u^5+30618u^6=0.             \tag{4}
\]
The existence, uniqueness, algebraic interval, and value of this
one-variable optimizer are credited to the earlier four-block and
saturated-face proofs. In particular,
\[
J_*>j(1/9)=5472/7>780,
\qquad J_*-j(u)\ge450(u-u_*)^2\quad(0\le u\le1/4).             \tag{5}
\]

**Theorem 1 (full symmetric cube).** For every vector in (2),
\[
 J\le J_*,                                                     \tag{6}
\]
with equality exactly when \(Y=X=1\) and \(u=u_*\). More precisely,
\[
J_*-J\ge
 \min\left\{\frac{12}{7},\,\frac{1-X}{2}+450(u-u_*)^2\right\}.   \tag{7}
\]
On the competitive cap \(X\ge3/4,\ u\le1/4\), we prove the stronger
intermediate comparison
\[
                  j(u)-J\ge(1-X)/2.                            \tag{8}
\]
Outside that cap, \(J\le780\). Thus (6) solves the full three-parameter
centrally symmetric class, rather than only the face \(Y=1\) or the
newly studied repeated-pair face \(Y=X\).

Let \(\mathcal O_*\) be the permutations of the unit-normalized vector
\(\pm(1,1,1,\sqrt{u_*})\). For the unit-normalized vector
\(\widehat\theta=\theta/\sqrt\alpha\), an additional consequence is
\[
 \operatorname{dist}(\widehat\theta,\mathcal O_*)^2
                  \le\frac{32}{5}(J_*-J).                     \tag{9}
\]

Now let \(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\), be proportional
to a real polynomial, with all roots in the closed unit disk and simple
marked root \(0<a<1\). Critical points are counted with algebraic
multiplicity. Put
\[
d=1+a,\quad G(p)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-16/d,
\quad \rho(p)=\max_j|z_j+1|,
\quad \kappa=d(a-5/8).                                        \tag{10}
\]
A simple marked root is not critical, so the sum is finite. Other roots
and critical points may repeat. Define \(R_{\mathbb R}(a)\) as the
supremum of \(r\ge0\) for which every such polynomial with \(\rho(p)\le r\)
satisfies \(G(p)\ge0\). The admissible radii form an initial interval;
we make no claim that the supremum itself is admissible.

**Theorem 2 (sharp real-polynomial displacement basin).**
For \(a>5/8\) sufficiently close to \(5/8\),
\(0<R_{\mathbb R}(a)<\infty\), and
\[
 \lim_{a\downarrow5/8}\frac{R_{\mathbb R}(a)^2}{\kappa}
  = B_* =\frac{(13/8)^4}{p_8J_*}
        =\frac{106496}{5J_*},\qquad
                   27.106707<B_*<27.106708.                    \tag{11}
\]
For every \(0<\varepsilon<B_*\), the radius squared
\((B_*-\varepsilon)\kappa\) is uniformly sufficient once \(a\) is close
enough. For every \(\lambda>1\), the explicit real boundary family in
Section 5 fails at radius squared \(\lambda B_*\kappa+O(\kappa^2)\).
No numerical neighborhood or sign at the exact crossing is asserted.

If real-polynomial negative-gap configurations satisfy
\(\rho(p)^2/\kappa\to B_*\), their normalized angular directions approach
\(\mathcal O_*\), their inward depth is \(o(E^2)\), and
\(G/E^2\to0\), where \(E\) is defined in Section 5.

## 2. Exact cubic formula and its trust boundary

For \(g(y)=(y-1)(y-Y)(y-X)(y-u)\), let \(e_1,\ldots,e_4\) be the
elementary symmetric functions of \(1,Y,X,u\). Write
\[
 Q(y)=g'(y)=4y^3-3e_1y^2+2e_2y-e_3,
\quad D_Q=36e_1^2e_2^2-128e_2^3-108e_1^3e_3-432e_3^2+432e_1e_2e_3.
\]
The earlier displacement variational source derives the following
generic cubic trace formula. Define
\[
\begin{aligned}
 A_0={}&128e_2^4-480e_1e_2^2e_3+180e_1^2e_3^2-64e_1^2e_2^3
           +204e_1^3e_2e_3+9e_1^4e_2^2-27e_1^5e_3,\\
 A_1={}&3072e_2^2-768e_1^2e_2-2304e_1e_3,\\
 A_2={}&-64512e_3^2-24576e_2^3+70656e_1e_2e_3
                              +6912e_1^2e_2^2-17280e_1^3e_3.
\end{aligned}
\]
Then
\[
 V=\frac{e_3^2A_0+e_3^2e_4A_1+e_4^2A_2}{8},\quad
 W=e_3^2D_Q,\quad \Psi=V/W,                                  \tag{12}
\]
and, since \(\mu_2=2e_1,\ \mu_4=2(e_1^2-2e_2)\),
\[
 N=(936e_1^2-896e_2)W-5760V,\quad
 D=2e_1W,\quad J=N/D.                                        \tag{13}
\]
These divisions are used only on \(e_3D_Q>0\). The ordered cube's generic
points have this property: the three distinct derivative roots interlace
the four distinct nonnegative roots of \(g\). Singular points are handled
by the credited continuity of (1), never by evaluating a zero denominator.

The standalone checker regenerates (12)--(13), all chart identities, and
the rational certificate below. Definition-level commutant controls also
compare the formula with the grouped spectral definition, including
singular configurations. These checks are supplementary; they do not
replace the credited derivation or prove a universal claim by sampling.

## 3. Finite coverage and exact sign certificate

For a rational box and a polynomial of multidegree \((n_1,n_2,n_3)\),
the tensor Bernstein basis is a nonnegative partition of unity. Thus
nonnegative rational coefficients imply nonnegativity throughout the
box; their minimum is a valid lower bound. The complete coefficients
are regenerated, all signs checked, and their inverse transformation
reconstructs each original power polynomial. Compact hashes and minima
are in expected.json; no large certificate corpus is an input.

**Low middle slope, \(X\le3/4\).** Put \(x=X\). At generic points let
\(p=(Y-X)/(1-X)\) and \(w=(X-u)/X\), both in \([0,1]\). The two charts
\[
\begin{array}{lll}
p\ge w:&Y=x+(1-x)h,&u=x(1-hk),\\
w\ge p:&Y=x+(1-x)hk,&u=x(1-h),
\end{array}                                                   \tag{14}
\]
with \(0\le x\le3/4\) and \(0\le h,k\le1\), cover the domain.
Use \(h=p,k=w/p\) in the first and \(h=w,k=p/w\) in the second.
The collision \(p=w=0\), as well as \(x=0\), follows by continuity.
In each chart the exact polynomial \(780D-N\) has the factor \(x^2h^2\).
After removing it, the certificate gives nonnegative coefficients on a
finite rational covering specified in CERTIFICATE.md. Consequently
\(J\le780\) throughout this region.

**Large smallest slope, \(u\ge1/4\).** Set
\[
d=1-u\in[0,3/4],\quad X=1-dx,\quad Y=1-dxs,
                                  \qquad x,s\in[0,1].         \tag{15}
\]
At generic points this covers all \(1\ge Y\ge X\ge u\).
The exact \(780D-N\) first has the factor \(d^6x^2\). Resolve the
remaining collision \(x=s=1\) by
\[
 (x,s)=(1-h,1-hk)\quad\hbox{or}\quad(1-hk,1-h),               \tag{16}
\]
according to the ordering of \(1-x\) and \(1-s\). Each substituted
quotient has the factor \(h^2\). After removing it, **all** Bernstein
coefficients on \([0,3/4]\times[0,1]^2\) are positive. Both minima are
\(7893099/4096\). Thus \(J\le780\) here too. All removed factors and
the underlying denominators are positive on generic chart points.

**Competitive cap, \(X\ge3/4,\ u\le1/4\).** Write
\[
 X=1-t,\quad Y=1-ts,\qquad
                         0\le t\le1/4,\quad0\le s\le1.       \tag{17}
\]
Both \(N,D\) in (13) have the exact factor \(t^2\); call their
quotients \(N_2,D_2\). With \(j_N,j_D\) denoting (3)'s numerator and
denominator, the polynomial \(j_ND_2-j_DN_2\) has the further factor
\(t\). Its quotient \(H\) has multidegree \((9,8,10)\). All its
990 coefficients on \([0,1/4]\times[0,1]\times[0,1/4]\) are positive,
and
\[
                         H\ge34642049301/1146880.              \tag{18}
\]
To turn this into (8), interlacing places two of the three roots of \(Q\)
in \([X,1]\), so their mutual distance is at most \(t\). All remaining
differences are at most one. Therefore
\(D_Q/t^2\le256\). Also \(e_1\le13/4\), \(e_3\le7/4\), and
\(j_D\le637/64\), hence
\[
 D_2\le5096,\qquad j_DD_2\le405769/8,
 \qquad \frac{34642049301}{1146880}>\frac{405769}{16}.           \tag{19}
\]
For \(t>0\) generic,
\[
j(u)-J=tH/(j_DD_2)\ge t/2.
\]
Continuity includes every collision and \(t=0\). This proves (8).

These three regions cover the entire ordered cube. Outside the cap use
\(J\le780\) and (5); inside use (8) and (5). They give (7), (6), and
the stated unique equality. This extends the earlier saturated-face
theorem; its stronger fixed-sum monotonicity obstruction is retained,
not contradicted or needed here.

## 4. Quantitative distance to the optimizer

In the cap let \(b\) be the eight-vector in (2), and let \(b_*\) be
\(\pm(1,1,1,\sqrt{u_*})\) in the corresponding order. Since
\(\|b\|^2\ge5\), \(u_*>2/25\), and \(Y\ge X\),
\[
\|b-b_*\|^2
 =2[(1-\sqrt Y)^2+(1-\sqrt X)^2+(\sqrt u-\sqrt{u_*})^2]
 \le4(1-X)+25(u-u_*)^2.
\]
Normalization gives
\[
\left\|\frac b{\|b\|}-\frac {b_*}{\|b_*\|}\right\|^2
 \le\frac45\|b-b_*\|^2
 \le\frac{16}{5}(1-X)+20(u-u_*)^2
 \le\frac{32}{5}(J_*-J).
\]
The normalization inequality follows by adding/subtracting
\(b_*/\|b\|\) and using the reverse triangle inequality. Outside the
cap the squared distance between two unit vectors is at most four,
whereas \((32/5)(12/7)>4\). Thus (9) holds globally.

## 5. All real disk motions and the matching upper family

We use the already proved full-disk displacement variational reduction,
whose required joint expansion has now received an independent scoped
review. For every negative-gap sequence tending to collapse, write
\[
 z_j=-(1-\tau_j)e^{i\phi_j},\quad
 T=\sum\tau_j,\quad M=\sum\phi_j,\quad L=\sum\phi_j^2,
 \quad E=\sum_j|(a-z_j)^{-1}-d^{-1}|^2.
\]
The cited all-root bootstrap gives
\(T=O(L^2),\ M^2=O(L^2),\ \kappa=O(L)\), and the controlled joint
expansion, with \(d_0=13/8\), gives
\[
 G=\kappa E+\frac{128}{169}T+\frac{40}{2197}M^2
                         -K(\theta)E^2+o(E^2),               \tag{20}
\]
uniformly through angular collisions and bounded normalized motions.
The expansion and bootstrap are cited analytic premises, not new
consequences of the Bernstein computation.

For a polynomial proportional to a real polynomial, its roots are
closed under conjugation, with multiplicity. Once \(\rho\) is small,
every real other root is negative and has \(\phi=0\); each nonreal pair
has phases \(\phi,-\phi\). Thus \(M=0\) exactly, and
\(\theta=\phi/\sqrt L\) is centrally symmetric. The number of zero
phases is even, because there are eight phases altogether. No equality
of the inward depths of distinct real roots is required.

Set \(q=\max_j\theta_j^2\), so \(q\ge1/8\). The cited metric expansion
is
\[
 \rho^2=Lq+O(L^{3/2}),\qquad E=d_0^{-4}L+O(L^2).              \tag{21}
\]
Since (1) is scale invariant and the max-normalized vector has
\(\alpha=1/q\), Theorem 1 says
\[
                     K(\theta)/q\le p_8J_*.                  \tag{22}
\]
Negativity in (20) and (21) implies
\[
                \kappa d_0^4/\rho^2\le K(\theta)/q+o(1).
\]
A hypothetical sequence of real-polynomial failures with
\(\rho^2\le(B_*-\varepsilon)\kappa\) would violate (22). Sequential
contradiction proves the uniform lower bound asserted in Theorem 2.

For the upper bound use the credited actual four-block profile
\[
p_{a,t}(z)=(z-a)
          (z^2+2\cos t\,z+1)^3
          (z^2+2\cos(\sqrt{u_*}t)\,z+1).                     \tag{23}
\]
It has real coefficients, simple marked root \(a\), and eight other
unit-disk roots. Its angular direction is precisely the optimizer in
Theorem 1, and
\(\rho^2=4\sin^2(t/2)=t^2+O(t^4)\) for small \(t\).
The credited angular expansion with
\(t^2=\lambda B_*\kappa\), \(\lambda>1\), gives
\[
G(p_{a,t})=\frac{\lambda(1-\lambda)}{K(\theta_*)}\kappa^2
                      +o(\kappa^2)<0.
\]
Hence \(\limsup R_{\mathbb R}^2/\kappa\le\lambda B_*\).
Let \(\lambda\downarrow1\) and combine with the lower bound. This proves
(11); it does not presume admissibility at the supremum. The rational
interval in (11) is the known four-block value, now proved optimal for
the real-polynomial class.

For a negative sequence with \(\rho^2/\kappa\to B_*\), divide (20) by
\(qE^2\) and use (21). The nonnegative losses
\(p_8J_*-K/q\) and \((128/169)T/(qE^2)\) must vanish. Formula (9)
then gives convergence of the angular direction to \(\mathcal O_*\);
substitution in (20) gives \(G/E^2\to0\). No remainder rate is supplied.

## 6. Remaining boundary and status

Theorem 1 identifies the displacement optimizer for centrally symmetric
directions, with three equal large pairs and one small pair. The earlier
energy optimizer has a singleton/seven direction, so substituting its
constant into this different metric would give a wrong optimizer.
The unrestricted balanced angular class can be asymmetric and is not
covered by the certificate. Its exact variational maximum, the general
complex displacement constant, higher-order corrections, effective
finite neighborhoods and the global first-power endpoint remain open
in this work.

At the collapse radius \(a_0=5/8\), the comparison value is
\(16/(1+a_0)=128/13>8\). Negative gaps relative to that value are not
first-power counterexamples. The known unit-root first-power equality
classification includes regular and opposite collapsed families; Zhang's
quadratic equality is regular only. Neither is a theorem about the new
optimizer at this interior marked radius. See LITERATURE.md for precise
primary and campaign comparisons.
