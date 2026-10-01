# An effective all-source fivefold receiving cap

Author: **six-rupert-1, researcher**, 2026-10-01.

This is an author-checked intermediate result, unformalized and
independently unreviewed. The full Rupert property remains open.

## 1. Theorem, normalization and dependencies

Use the exact family, closed parameter box, proper group \(\mathcal I\),
axis \(N=(1,0,\phi)\), \(h=\phi+2\), \(n_0=N/\sqrt h\), and rotation
\(G\) from the preceding
[minimum-diameter proof](../pentagonal_minimum_diameter/PROOF.md) and
[qualitative receiving-neighborhood proof](../pentagonal_fivefold_neighborhood/PROOF.md).
The body is
\[
K_p=\operatorname{conv}
\big(\mathcal I(-u,-r,-1)\cup a(\pm W)\cup t\mathcal D\big),
\]
with \(u\in[.0919831,.0919833]\), \(r\in[.1041858,.1041860]\),
\(a\in[.5565538,.5565540]\), \(t\in[.5828994,.5828997]\).
This is the standard named solid divided by \(C_{19}\) at its exact
algebraic parameter point. The previous audit proves that alignment.

Write \(D_p(n)=\operatorname{diam}(\pi_nK_p)\),
\(\mathcal A=\mathcal I n_0\), and
\[
\delta(r)^2=4\big(1+r^2(h-1)/h\big).
\]
The previous minimum theorem gives \(D_p(n)\ge\delta(r)\), with
equality exactly on the twelve oriented/six unoriented axes in
\(\mathcal A\). Its radius audit gives \(K_p\subset B(0,a\sqrt h)\).
The current checker verifies \(a\sqrt h<11/10\) throughout the box.
Put \(R=11/10\). The body contains zero in its interior, since it
contains the twelve centrally paired icosahedral points.

**Theorem.** Uniformly for every \(p\) in this closed box, if
\[
\operatorname{dist}(n,\mathcal A)\le10^{-6},
\]
then every closed inclusion
\[
\lambda\pi_n(R_1K_p)+b\subseteq\pi_nK_p,
\qquad R_1\in SO(3),\quad b\in n^\perp,\quad\lambda\ge1
\tag{1}
\]
has \(\lambda=1\), \(b=0\), and \(R_1\in\mathcal I\).
These receiving caps therefore exclude every strict Rupert passage,
allowing every proper source, roll and physical translation. Both handed
standard solids satisfy the theorem by reflecting the whole setup; only
same-handed copies are compared.

Two further explicit statements are proved along the way:

* If \(0\le\varepsilon\le10^{-5}\) and
  \(D_p(n)^2\le\delta(r)^2+\varepsilon\), then
  \(\operatorname{dist}(n,\mathcal A)\le3\varepsilon\).
* Every receiving direction of a strict passage has
  \(D_p(n)^2>\delta(r)^2+1/3000000\).

Squared diameters here refer to \(K_p\), the \(C_{19}\)-normalized
body. For the named solid in the original normalization, multiply the
squared-diameter gap by \(C_{19}^2\). The normal chord radius is unchanged
by any scaling of the solid.

## 2. A robust signed cover gives a linear source budget

The preceding global proof uses 238 positive weighted halfspace
certificates. For each, writing its weighted normal as \(A\) and right
side as \(B\), the checker now replays the complete cover and proves
\[
\frac{B^2-h\|A\|^2}{B^2}>\frac1{250}.
\tag{2}
\]
The original lower bound returned by the checker uses the upper interval
endpoint of \(B^2\) in the denominator; consequently it also implies
the pointwise bound (2). Let \(k=999/1000\). Lowering each threshold
\(r\) to \(kr\), while leaving the positive icosahedral thresholds
\(B_0=1147/1000\) unchanged, lowers every weighted right side to at
least \(kB\). Since \(k^2>1-1/250\), every certificate still separates
the sphere. All signs and complete sign-pattern coverage remain valid.

Suppose \(D_p(n)^2\le\delta(r)^2+\varepsilon\), and put
\(z=\sqrt h\,n\). The same antipodal icosahedral points and ten genuine
half-differences give the necessary thresholds
\[
|w\cdot z|^2\ge
h^2-\frac{h+r^2(h-1)+h\varepsilon/4}{a^2},
\qquad
|d_i\cdot z|,|e_i\cdot z|\ge b_\varepsilon
:=\sqrt{r^2-h\varepsilon/4}.
\tag{3}
\]
At the worst value \(\varepsilon=10^{-5}\), rational interval checks
prove that the first lower bound is greater than \(B_0^2\), and that
\(b_\varepsilon\ge kr>0\). Thus the relaxed signed cover applies.
It puts the icosahedral signs in one of twelve proper-body charts and
forces the five first rows
\(d_i=G^i(r,1,0)\) to have all-positive signs in that chart. By a proper
body symmetry, take this chart about \(n_0\).

Write \(z=cN+y\), with \(y\perp N\); here \(c=n\cdot n_0\).
The average \(\sum_i d_i=(5r/h)N\) gives
\(c\ge b_\varepsilon/r\ge k\). The transverse parts of the \(d_i\)
form a regular pentagon of radius
\(\sqrt{1+r^2(h-1)/h}>1\). Its convex hull contains the centered disk
of radius \(\phi/2\), since \(\cos(\pi/5)=\phi/2\). Hence some row
satisfies
\[
d_i\cdot z\le cr-(\phi/2)\|y\|\le r-(\phi/2)\|y\|.
\]
Its actual positive threshold in (3) gives
\(\|y\|\le2(r-b_\varepsilon)/\phi\).
If \(\gamma\) is the angle from \(n_0\), then
\(\|y\|=\sqrt h\sin\gamma\),
\(\cos(\gamma/2)\ge\sqrt{(1+k)/2}\), and
\[
\begin{aligned}
\|n-n_0\|
&=\frac{\sin\gamma}{\cos(\gamma/2)}\\
&\le
\frac{\sqrt h}
 {2\phi(r+b_\varepsilon)\sqrt{(1+k)/2}}\,\varepsilon\\
&\le
\frac{\sqrt h}
 {2\phi(1+k)r\sqrt{(1+k)/2}}\,\varepsilon
\le3\varepsilon.
\end{aligned}
\tag{4}
\]
We used \(r-b_\varepsilon=h\varepsilon/[4(r+b_\varepsilon)]\).
The checker encloses the final coefficient strictly below three on the
entire box. At \(\varepsilon=0\), the same argument gives the exact
axis. This proves the source budget for every orientation, with no
floating-point localization premise.

## 3. Ten outermost shadow points determine the roll

Let \(P=\pi_{n_0}K_p\), and set
\[
\alpha=\phi r-u,\qquad \beta=\phi u+r,\qquad \eta=\phi r+u.
\]
These three different quantities will be kept distinct. Put
\(U=(\phi,0,-1)\) and \(m=(0,1,0)\). The maximal shadow radius is
\[
L^2=1+\eta^2/h.
\]
Exactly ten original points attain it. Their projected points are
\[
X=\{G^ix,G^iy:0\le i<5\},
\qquad x=m-(\eta/h)U,\quad y=m+(\eta/h)U.
\tag{5}
\]
They come from the original long-edge endpoints \((-r,1,u)\) and
\((r,1,-u)\). The checker proves the ten exact equalities and, for all
other eighty-two original projected points \(q\),
\[
\|q\|^2<L^2-1/100.
\tag{6}
\]

Let \(Q\) be the proper planar rotation about \(n_0\) that sends
\(x\) to \(y\). In the basis \((m,U)\), whose metric is
\(\operatorname{diag}(1,h)\), it is
\[
Q=\frac1{h+\eta^2}
\begin{pmatrix}h-\eta^2&-2h\eta\\2\eta&h-\eta^2\end{pmatrix}.
\]
This matrix has determinant one and preserves that metric by direct
multiplication. Applying it twice to \(x\) gives
\[
Q^2x=
\frac{h-3\eta^2}{h+\eta^2}m+
\frac{\eta(3h-\eta^2)}{h(h+\eta^2)}U.
\tag{7}
\]
For all ten targets in (5), exact rational interval checks prove
\[
\|Q^2x-q\|>L/4\quad(q\in X).
\tag{8}
\]
Thus the two outermost endpoint orbits cannot be interchanged by an
approximate roll with small error. This is a finite quantitative version
of the previous shadow-symmetry classification.

Suppose a proper planar rotation \(T\) satisfies
\(TP\subseteq P+E B_2\), where \(B_2\) is the planar unit disk,
\(2RE<1/100\), and \(E<1\). For each source point \(a\in X\), the
support inequality in direction \(Ta/L\) gives an original projected
target \(q\) with
\((Ta/L)\cdot q\ge L-E\). Condition (6) forces \(q\in X\), since
otherwise its squared norm is less than \(L^2-1/100\), but the displayed
inequality forces it above \(L^2-2LE+E^2>L^2-1/100\).
Therefore
\[
\|Ta/L-q/L\|\le\sqrt{2E/L}<\sqrt{2E}=:d_r.
\tag{9}
\]
Here \(L>1\). If \(Tx\) matches \(G^iy\), the operator distance on
the receiving plane between \(T\) and \(G^iQ\) is at most \(d_r\),
because that distance for two planar rotations equals their displacement
of any unit vector. Applying them to \(y/L=Qx/L\) and using the second
match in (9) would put \(G^iQ^2x/L\) within \(2d_r\) of \(X/L\).
This contradicts (8) when \(2d_r<1/4\). Hence \(Tx\) matches an element
\(G^ix\), and
\[
\|T-G^i\|_{\mathrm{op}}<d_r.
\tag{10}
\]
The same operator bound holds in three-space, since both rotations fix
\(n_0\). No assumption on a source translation was used here; Section5
will remove it by a fivefold convex average before applying this argument.

## 4. Quantitative local rigidity with exact translation cancellation

Take the short-edge endpoints
\(v=(-r,-1,-u)\), \(w=(r,-1,u)\), and their \(G\)-orbits
\(v_i,w_i\). Write \(m_i=G^i(0,-1,0)\),
\(a_i=G^i(-u,0,r)\), and \(E_i=w_i-v_i\).
The preceding proof gives
\(v_i\times m_i=a_i\), \(w_i\times m_i=-a_i\), and support offset one.
The current checker proves the stronger unit-normal support gap
\[
m_i\cdot(v_i-z)>1/20
\tag{11}
\]
for every original point except \(v_i,w_i\); it checks one edge against
ninety points and uses the exact body symmetry to transport it.

For a receiver normal with \(d=\|n-n_0\|\le d_0:=1/10000\), put
\[
\widetilde m_i(n)=\frac{E_i\times n}{2\alpha/\sqrt h}.
\]
These lie in the actual receiving plane and are perpendicular to their
original edges. At \(n_0\) they equal \(m_i\). The checker proves
\[
\|\widetilde m_i-m_i\|\le\tfrac72 d,
\qquad R\|\widetilde m_i\|<6/5.
\tag{12}
\]
The first follows from
\(\|E_i\|/(2\alpha/\sqrt h)=\sqrt{h(u^2+r^2)}/\alpha<7/2\).
Equations (11)--(12) leave support gap greater than
\(1/20-2R(7/2)d_0>0\). Thus the same two endpoints remain true receiving
contacts for these normals. Their equality is exact for every \(n\),
because \(\widetilde m_i\cdot E_i=0\).

Positive weights can cancel translation exactly in this changing plane.
Write \(n=c n_0+z\), with \(z\perp n_0\) and
\(c=1-d^2/2\). Decompose
\[
E_i=e n_0+T_i,
\qquad e=2\beta/\sqrt h,
\qquad\ell^2=\|T_i\|^2=4\alpha^2/h.
\]
The exact fivefold moments are
\(\sum T_i=0\) and
\(\sum T_iT_i^T=(5\ell^2/2)(I-n_0n_0^T)\). Put
\[
\omega_i=1+\frac{2e}{c\ell^2}(T_i\cdot z).
\tag{13}
\]
Then
\[
\sum\omega_i=5,\qquad
\sum\omega_iE_i=(5e/c)n,
\qquad\sum\omega_i\widetilde m_i(n)=0.
\tag{14}
\]
The checker proves
\(2\beta/(c\alpha)<7\), using \(c\ge1-d_0^2/2\), so
\(\omega_i\ge1-7d>0\). No physical translation remains in any support
sum with these weights, even for this chiral body.

The torque second moment is also checked entry by entry:
\[
\sum_i a_i a_i^T=
\frac{5\alpha^2}{h}n_0n_0^T+
\frac{5\beta^2}{2h}(I-n_0n_0^T).
\tag{15}
\]
Exact bounds \(\beta^2>2\alpha^2\) and
\(5\alpha^2/h>1/144\) imply, for every unit rotation axis \(u_*\),
\[
\sum_i|a_i\cdot u_*|
\ge\sqrt{\sum_i(a_i\cdot u_*)^2}>1/12.
\tag{16}
\]

Consider a unit-scale closed fit with relative rotation
\(S=\exp(\theta[u_*]_\times)\), \(0<\theta\le\theta_0:=1/50\).
At edge \(i\), choose \(v_i\) or \(w_i\) so its unperturbed torque
has dot product \(|a_i\cdot u_*|\). Use its positive weight
\(\omega_i\) in the true receiving inequality. Translation cancels by
(14). Equations (12)--(16) bound the first-order weighted torque below by
\[
\frac{1-7d_0}{12}-5R(7/2)d_0.
\]
For a proper rotation the exact exponential remainder satisfies
\(\|S-I-\theta[u_*]_\times\|_{\mathrm{op}}\le\theta^2/2\).
For example, integrate the second derivative of the orthogonal
exponential twice; its operator norm is at most one. Using total weight
five and the probe bound \(6/5\), the weighted displacement is strictly
greater than
\[
\theta\left(
\frac{1-7d_0}{12}-5R(7/2)d_0-
\frac{5(6/5)\theta_0}{2}\right)
=\theta\frac{427}{20000}>0.
\tag{17}
\]
Closed containment makes that same sum nonpositive, a contradiction.
Thus a unit closed fit in this local region forces \(S=I\), and then
its translation is zero: a bounded convex set cannot contain a nonzero
translate of itself. In support direction \(b\), translation would
increase its support value by \(\|b\|^2>0\).

For scale \(\lambda\ge1\), divide (1) by \(\lambda\) about zero.
Convexity and \(0\in K_p\) give a unit fit with translation
\(b/\lambda\). The unit result forces rotation identity and translation
zero; positive diameter then forces \(\lambda=1\). This proves local
closed-fit rigidity for every translation, at receiver chord \(d_0\)
and full relative rotation angle \(\theta_0\).

## 5. The source budget and roll matching cover every source

By a proper body symmetry, take a receiver satisfying
\(d=\|n-n_0\|\le\rho:=10^{-6}\). For any original point difference
\(q\), \(\|q\|\le2R\), and
\[
\big|(q\cdot n)^2-(q\cdot n_0)^2\big|
\le2\|q\|^2d\le8R^2d<10d.
\]
The projected diameter squared is the maximum over these finite
original pairs, hence
\[
D_p(n)^2\le\delta(r)^2+10d.
\tag{18}
\]
Any closed fit at scale at least one has source diameter no larger than
the receiver diameter. Section2 applies with \(\varepsilon=10d\le10^{-5}\),
giving an oriented source-axis chord at most \(30d\) from some element
of \(\mathcal A\). Right-compose the source rotation with the proper
body symmetry selecting this axis. Its moving body is unchanged, and
the resulting rotation \(S\) obeys
\(\|S^Tn-n_0\|\le30d\). Thus
\[
\|Sn_0-n_0\|\le31d=:d_t.
\tag{19}
\]
Let \(H\) be the shortest proper rotation sending \(Sn_0\) to \(n_0\),
and put \(T=HS\). It fixes \(n_0\), so it is a proper planar roll there,
and \(\|S-T\|_{\mathrm{op}}=\|H-I\|_{\mathrm{op}}\le d_t\).
This uses the identity between the operator chord of a shortest rotation
and the chord of its transported unit normal.

Rescale any purported larger copy to a unit fit as in Section4. Denote
its translation by \(b\). Project that inclusion onto \(n_0^\perp\).
The operator error of \(\pi_{n_0}\pi_n-\pi_{n_0}\) is
\(\|\pi_{n_0}n\|\le d\). Comparing its source to the roll \(T\),
and its receiver to \(P\), gives
\[
TP+\pi_{n_0}b\subseteq P+E B_2,
\qquad E:=37\rho>R(2d+d_t).
\tag{20}
\]
For example, each \(v\in K_p\) changes by at most \(R(d+d_t)\) on
the source side, and the projected receiving body changes by at most
\(Rd\). Convexity extends the finite point bound to the whole body.
Using a fixed positive \(E\) also covers the exact-axis case \(d=0\).

Rotate (20) by the five powers of \(G\). The roll \(T\) commutes with
\(G\), and both \(P\) and the error disk are invariant. For any
\(x\in TP\), the five points \(x+G^i\pi_{n_0}b\) belong to the same
convex set \(P+EB_2\). Their average is \(x\), since the translation is
in the plane and its fivefold average is zero. Consequently
\[
TP\subseteq P+EB_2.
\tag{21}
\]
This is a justified cancellation of translation after a controlled shadow
comparison; it does not assume a centered original passage.

The final rational gates are
\[
2RE<1/100,\qquad
\sqrt{2E}<9/1000,\qquad2(9/1000)<1/4.
\]
Thus Section3 gives \(\|T-G^j\|_{\mathrm{op}}<9/1000\) for some
proper body symmetry \(G^j\). Right-compose \(S\) by \(G^{-j}\),
again leaving the source body unchanged. Its distance from identity is
less than \(31\rho+9/1000\). For an operator chord \(x\le1\), the
principal rotation angle is \(2\arcsin(x/2)\le2x\), so this relative
rotation has angle strictly less than
\[
2(31\rho+9/1000)=9031/500000<1/50.
\tag{22}
\]
The receiver chord \(\rho\) is also less than \(d_0\). Section4 forces
the relative rotation to identity, its translation to zero, and scale to
one. Undoing the proper body adjustments gives exactly the classification
in the theorem. Every oriented source branch was covered by the global
signed cover; the two possible outer-point roll branches were both
handled by (8)--(10).

## 6. Explicit receiving-diameter gap and evidence

Let \(\varepsilon=D_p(n)^2-\delta(r)^2\ge0\). If
\(\varepsilon\le10^{-5}\), Section2 gives
\(\operatorname{dist}(n,\mathcal A)\le3\varepsilon\). A strict passage
has its receiving direction outside the closed caps, so
\(3\varepsilon>10^{-6}\). If \(\varepsilon>10^{-5}\), the same claimed
lower bound is automatic. Hence every strict passage has
\(\varepsilon>1/3000000\), as stated.

The checker replays the complete 238-certificate signed cover and genuine
half-difference audit, checks both relaxed thresholds on the full box,
and verifies the coefficient in (4). It checks ten exact outer-radius
identities, eighty-two strict radial gaps, ten wrong-branch distances,
ninety original short-edge support gaps, eighteen exact second-moment
entries, and every displayed scalar bound. All calculations use exact
\(\mathbb Q(\phi)\) arithmetic or outward rational intervals. There is
no floating-point theorem decision, sampled coverage, solver or negative
search premise. The reductions involving supports, roll, convex averages
and rotation remainders are the written geometric proof above.

The source and reference hashes, commands and scope are recorded in
[README.md](README.md). The earlier qualitative lemma remains valid; this
proof supplies its previously unspecified radius by a different,
quantitative all-source bridge. General contact and local-exclusion
principles are prior art. The full Rupert status away from these caps
remains open.
