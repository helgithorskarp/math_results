# Four independent inward losses on the whole balanced critical-profile sphere

Actual author/reviewer: **six-reviewer-1**, independent mathematical reviewer,
2026-10-03. This is an ordinary, **unformalized** proof. It rederives the
finite identities of LEMMA10036 without importing its executable kernels,
then proves a scoped four-parameter strengthening. The author's written
proof was exposed before these calculations; this audit is **not blind**.

## Quantified statement and constants

Put
\[
\begin{gathered}
c=\cos(\pi/9),\quad d=2c^2-1,\quad y=[3(1+c)]^{-1},\quad x=2/3-y,\\
H=14y,\quad U=-8x,\quad C=8/3+y,\quad
k=-7(1+2c)/18,\quad \rho=(c-5)/3,\quad \ell=k+\rho,\\
\alpha=-527/360+41c/90+13c^2/90,\quad \tau=\ell^2/2,\\
B_*=2311/108+4934c/27-1976c^2/9,\qquad K_1=B_*-\alpha H^2/2 .
\end{gathered}                                                   \tag{1}
\]
For the compact sphere
\[
\mathcal S=\{v\in\mathbb R^8:\textstyle\sum v_j=0,\ \sum v_j^2=H\},
\]
write \(J_3=\sum v_j^3,\ J_4=\sum v_j^4\), and
\[
u_j=(U+\rho H)/8+(\ell J_3/H)v_j-\rho v_j^2,\qquad
K(v)=K_1+\alpha J_4+\tau J_3^2/H.                               \tag{2}
\]
This sphere has intrinsic dimension six and lies in \(\mathbb R^8\).
No distinctness or nonzero-coordinate condition is imposed.

**Strengthened realization theorem.** There are \(\eta_0>0\), a finite
\(L\), and actual monic degree-nine polynomials \(p_{v,\mu,\eta}\), for
**every** \(v\in\mathcal S\), **every**
\(\mu=(\mu_3,\mu_4,\mu_5,\mu_6)\in[1/2,2]^4\), and **every**
\(0<\eta<\eta_0\), such that all nine original roots are simple and
strictly in the unit disk, one is exactly \(a=1-\eta\), and the eight
critical points, counted with multiplicity, satisfy uniformly
\[
\Im\zeta_j/\sqrt\eta=v_j+O(\eta),\qquad
\Re\zeta_j/\eta=u_j+O(\eta).
\]
Label the original branches near
\(\omega_j=\exp(2\pi i j/9)\), \(j=0,\ldots,8\), as \(r_j\). The four
active branches have independently specified **exact** losses
\[
(|r_j|^2-1)/2=-\mu_j\eta^3,\qquad j=3,4,5,6.                  \tag{3}
\]
The first-power critical objective has the common remainder bound
\[
\left|\sum_{j=1}^8 |1-\eta-\zeta_j|^{-1}
             -8-C\eta-K(v)\eta^2\right|\le L\eta^3,             \tag{4}
\]
and, after one common shrinkage, is at most \(8+C\eta+10\eta^2\).
The same proof works for any fixed box \([m,M]^4\), \(0<m\le M<\infty\),
with collar and bounds depending on that box.

Setting all four \(\mu_j=1\) proves the self-contained realization part
of10036. The refinement is independent prescription of the four sixth
order inward losses without changing the fourth order objective.
It supplies no explicit numerical collar or optimum at the next order.

## Derivation from the full critical-point polynomial

Set \(t=\sqrt\eta\), use four **real** controls \(G,\sigma,M,b\), and define
the entire untruncated critical tuple and polynomial by
\[
\zeta_j=itv_j+t^2(u_j+\sigma v_j)+it^3(G+bv_j)+t^4M,\qquad
p(z)=9\int_{1-t^2}^z\prod_{j=1}^8(w-\zeta_j)\,dw .             \tag{5}
\]
This is monic degree nine, \(p'=9\prod(w-\zeta_j)\), and the anchor is an
exact original root. Critical collisions do not affect these identities.

Direct coordinate summation gives \(\sum u=U\), \(\sum vu=kJ_3\), and
\[
\begin{aligned}
U_2(\sigma)&=8x^2+\rho^2(J_4-H^2/8)+(k^2-\rho^2)J_3^2/H
                      +2\sigma kJ_3+\sigma^2H,\\
J_{21}(\sigma)&=-xH-\rho(J_4-H^2/8)+\ell J_3^2/H+\sigma J_3,\\
D&=U_2(\sigma)-2bH .
\end{aligned}
\]
The power sums through degree four are
\[
\begin{aligned}
P_1&=Ut^2+8iGt^3+8Mt^4,\\
P_2&=-Ht^2+2i(kJ_3+\sigma H)t^3+Dt^4+O(t^5),\\
P_3&=-iJ_3t^3-3J_{21}(\sigma)t^4+O(t^5),\qquad
P_4=J_4t^4+O(t^5).
\end{aligned}
\]
Applying \(n e_n=\sum_{q=1}^n(-1)^{q-1}e_{n-q}P_q\), integrating the
resulting derivative and expanding the actual anchor \(1-t^2\), gives
the **entire** polynomial map
\[
p=z^9-1+t^2g_2+t^3g_3+t^4g_4+O(t^5),                         \tag{6}
\]
\[
\begin{aligned}
g_2&=9+9x(z^8-1)+9y(z^7-1),\\
g_3&=i[-9G(z^8-1)-(9/7)(kJ_3+\sigma H)(z^7-1)
                                      +(J_3/2)(z^6-1)],\\
g_4&=-36-9U+9H/2-9M(z^8-1)+(9/14)(U^2-D)(z^7-1)\\
&\quad+[-3UH/4+3J_{21}(\sigma)/2](z^6-1)
                           +[9H^2/40-9J_4/20](z^5-1).
\end{aligned}                                                   \tag{7}
\]
Our coordinate-power summation and Newton integral in [jets.py](jets.py)
compare every retained coefficient with (7). An independent literal
eight-factor route in [literal_controls.py](literal_controls.py) checks
four profiles with zeros, repeated coordinates, balanced conjugate and
asymmetric configurations. These finite checks corroborate the algebra;
the uniform existence proof below uses the full polynomial (5).

## All nine original roots and both normal Jacobian blocks

For bounded parameters, (5) tends uniformly in coefficient norm to
\(z^9-1\). Choose nine fixed disjoint disks around its simple roots.
On their boundaries \(z^9-1\) has a positive minimum modulus.
Uniform coefficient continuity on the compact parameter tube makes the
perturbation smaller than this minimum. Rouché's theorem gives exactly
one root, counted with multiplicity, in each disk. Each root is simple,
the nine roots exhaust the degree, and local implicit root branches
give real analytic dependence with uniform derivative bounds on a
smaller compact tube. The branch at \(\omega_0=1\) is exactly \(1-t^2\).

Writing \(r_j=\omega_j+t^2L_j+t^3T_j+t^4Z_j+O(t^5)\), polynomial residual
cancellation gives
\[
\begin{aligned}
L_j&=-g_2(\omega_j)/(9\omega_j^8),\qquad
T_j=-g_3(\omega_j)/(9\omega_j^8),\\
Z_j&=-[g_4(\omega_j)+g_2'(\omega_j)L_j
                          +36\omega_j^7L_j^2]/(9\omega_j^8).
\end{aligned}                                                   \tag{8}
\]
Let \(n_j=(|r_j|^2-1)/2\), \(\theta_j=2\pi j/9\). Direct evaluation of
**every** branch gives
\[
\begin{aligned}
[t^2]n_j&=-2y(\cos\theta_j+1/2)(\cos\theta_j+c),\\
[t^3]n_j&=G\sin\theta_j+(kJ_3+\sigma H)\sin2\theta_j/7
                                      -J_3\sin3\theta_j/18 .
\end{aligned}                                                   \tag{9}
\]
The coefficient at \(t^4\) is
\(\Re(\overline{\omega_j}Z_j)+|L_j|^2/2\); **both** the nonlinear term
in (8) and this modulus curvature are retained.

Only branches3,4,5,6 have zero quadratic normal. For the other five,
the relevant cosines are \(1,d,2d^2-1,2d^2-1,d\), all positive.
Their quadratic normals are strictly negative. The marked one is \(-1\).
Set \(G_0=kJ_3/7,\ \sigma_0=0\). For branch3,
\(\sin2\theta_3=-\sin\theta_3\) and \(\sin3\theta_3=0\).
For branch4,
\(\sin2\theta_4=-2c\sin\theta_4\),
\(\sin3\theta_4=(4c^2-1)\sin\theta_4\).
These identities make all four active cubic normals zero.

For \(j=3,4\), set \(A_j=1-\cos\theta_j\), \(B_j=1-\cos2\theta_j\);
\((A_3,B_3)=(3/2,3/2)\), \((A_4,B_4)=(1+c,1-d)\).
With \(U_{20}=U_2(0)\), \(J_{210}=J_{21}(0)\), put
\[
\begin{aligned}
\mathcal T_j={}&4+U-H/2+B_jU^2/14\\
&+(1-\cos6\theta_j)(-UH/12+J_{210}/6)\\
&+(1-\cos5\theta_j)(H^2/40-J_4/20)+\mathcal C_j,\\
\mathcal C_j={}&-(7x^2/2+6xyq_j+5y^2q_j^2/2)s_j,\\
(q_3,s_3)&=(-1,3/4),\qquad(q_4,s_4)=(-2c,1-c^2),\\
R_j&=\mathcal T_j-B_jU_{20}/14 .
\end{aligned}                                                   \tag{10}
\]
At \(\sigma=0\) the fourth normal is
\[
[t^4]n_j=R_j-A_jM+(HB_j/7)b .                                \tag{11}
\]
The same fourth coefficient holds at the reflected branch.
The two-row matrix in (11) has determinant \(D_E=3H(c+d)/14>0\).
Thus
\[
M_0=H(B_3R_4-B_4R_3)/(7D_E),\qquad
b_0=(A_3R_4-A_4R_3)/D_E                                    \tag{12}
\]
cancel all four fourth normals. These are bounded polynomial functions
of \(J_4,J_3^2\), with no coordinate-gap or \(J_3\) divisor.

For the full polynomial at fixed real controls,
\(p(-t,z)=\overline{p(t,\bar z)}\); uniqueness of each root branch gives
\(n_{9-j}(-t)=n_j(t)\). Therefore
\[
E_j=(n_j+n_{9-j})/(2t^4),\qquad
O_j=(n_j-n_{9-j})/(2t^3),\quad j=3,4                         \tag{13}
\]
extend analytically and evenly through \(t=0\).
Divisibility holds for all nearby controls on \(\mathcal S\):
constant/linear normals vanish, active quadratic normals vanish, and
cubic normals are opposite. No assumption that the controls have
already been closed is used.

At \((G_0,0,M_0,b_0)\), \(O_3,O_4,E_3,E_4\) vanish. With rows in that
order and columns \(G,\sigma,M,b\), the upper-right block is zero.
The odd block has rows \((\sin\theta_j,H\sin2\theta_j/7)\), determinant
\[
D_O=(H/7)\sin\theta_3\sin\theta_4(1-2c)\ne0 ,
\]
and the even block is (11), determinant \(D_E\).
The lower-left block can depend on the profile and is retained.
The complete Jacobian is invertible for every profile; its inverses
have a common bound by continuity and compactness.

## Uniform closing with four independent positive losses

For \(j=3,4\) impose
\[
E_j=-\frac{\mu_j+\mu_{9-j}}2t^2,\qquad
O_j=-\frac{\mu_j-\mu_{9-j}}2t^3.                             \tag{14}
\]
Adding and subtracting in (13) gives **exactly**
\(n_j=-\mu_jt^6\) and \(n_{9-j}=-\mu_{9-j}t^6\).
In particular the odd equation needs \(t^3\), not \(t^2\).

Here is a uniform implicit-function argument with the quantifiers
explicit. The starting graph \(P_0(v)=(G_0,0,M_0,b_0)\) is compact.
Let \(A(v)\) be the Jacobian of the four left sides at this graph,
and \(Q\) a bound on \(\|A(v)^{-1}\|\).
Use local real analytic charts of the sphere (its two constraint
gradients are independent). Uniform continuity of the control
derivatives on a compact neighborhood supplies a common
\(\varepsilon>0\) and time interval on which
\(\|I-A(v)^{-1}D_P f\|\le1/2\).
For \(f\) equal to left minus right sides of (14),
\(\|f(t,v,P_0(v),\mu)\|=O(t^2)\), uniformly on the sphere and loss box.
Shrink the time interval so \(Q\|f(t,v,P_0,\mu)\|\le\varepsilon/2\).
Then \(P\mapsto P-A(v)^{-1}f(t,v,P,\mu)\) contracts the common closed
\(\varepsilon\)-ball around \(P_0(v)\) into itself. It has one solution
in that ball, for **every** profile and loss vector.
The local real analytic implicit-function theorem identifies this
solution as analytic; uniqueness identifies solutions across chart
overlaps. The same contraction estimate gives uniformly
\[
G=G_0+O(t^2),\quad \sigma=O(t^2),\quad
M=M_0+O(t^2),\quad b=b_0+O(t^2).                            \tag{15}
\]
Unlike the symmetric specialization, these closed controls need not
be even in \(t\). This proof never requires that parity.

All four active normals are strictly negative by (3), uniformly over
the positive loss box. Each other normal has its strictly negative,
profile-independent quadratic coefficient plus a uniform \(O(t^3)\).
On one smaller common interval these five are also negative.
The already disjoint simple branches exhaust all nine roots. This
establishes original-root feasibility, including all collision profiles.
Formula (5) and bounded controls give the two critical asymptotics.

## Objective, remainder, exact profile maximum and inherited lower bound

For **fixed real controls**, (5) has imaginary odd and real even powers
of \(t\) at each critical coordinate. Its individual squared critical
distances, and hence their reciprocal square roots, are even analytic.
At \(t=0\) all distances equal one; on a common parameter tube they
are at least \(1/2\). Direct binomial expansion and coordinate summation
give the complete first-power formula
\[
F=8+Ct^2+
[8M-bH+8+2U+U_2(\sigma)-3H/2
                      -3J_{21}(\sigma)/2+3J_4/8]t^4+O(t^6). \tag{16}
\]
The coefficient of \(t^2\) is independent of **all** controls.
Compactness gives a common \(O(t^6)\) bound before closing.
Substitution of (15) changes the fourth coefficient by \(O(t^2)\);
therefore it changes (16) by \(O(t^6)\), even for unequal loss vectors.
No evenness of the closed family is inferred.

For \(w_4=(c+d)^{-1}\), \(w_3=(2/3)(7-(1-d)w_4)\),
\(\sum w_jA_j=8\), \(\sum w_jB_j=7\). Multiplying (11) at its zero by
these weights gives
\[
8M_0+(U_{20}-2b_0H)/2=\sum_{j=3,4}w_j\mathcal T_j .
\]
Substitution in (16) simplifies identically to \(K(v)\) in (2).
Our whole-map coefficient comparison, rather than sampled values,
checks this simplification. Thus (4) follows.

For completeness, Lagrange multipliers at the extrema of \(J_3\) on
the compact balanced sphere give \(3v_j^2=a+bv_j\). At most two
coordinate values occur; one value is impossible since \(H>0\).
If their multiplicities are \(r,8-r\), \(1\le r\le7\), balance and norm
give
\[
J_3^2/H^3=(8-2r)^2/[8r(8-r)] .
\]
The seven values are \(9/14,1/6,1/30,0,1/30,1/6,9/14\).
Hence \(J_3^2/H\le9H^2/14\), with equality exactly at permutations
and sign reversals of \(\sqrt{H/56}(7,-1,\ldots,-1)\).
This skewness argument is classical.
Also
\[
D(v)=J_4-H^2/8-J_3^2/H
     =\sum_j(v_j^2-H/8-(J_3/H)v_j)^2\ge0 .
\]
Let \(K_{\max}=K_1+(43\alpha/56+9\tau/14)H^2\). The exact identity is
\[
K_{\max}-K(v)
 =(\alpha+\tau)(9H^2/14-J_3^2/H)-\alpha D(v).
\]
Exact rational interval evaluation proves \(\alpha<0\),
\(\alpha+\tau>0\), and \(9<K_{\max}<10\).
Equality therefore holds precisely at the stated1+7 profiles;
their \(D(v)\) is zero. Shrinking the common collar to make
\(L\eta<10-K_{\max}\) proves the common budget.
This maximum is over the least attainable cost per profile, not all
disk-root polynomials or optimal finite-collar budgets.

The **lower-rate/profile optimality** part of10036 separately adopts
the arbitrary-competitor rate reduction of8619, independently reviewed
in8684. Its domain is every actual degree-nine closed-disk-root sequence
\(\eta_n\downarrow0\) with \(F\le8+C\eta_n+D_0\eta_n^2\) for one finite
\(D_0\). That result gives bounded real corrections, the limiting
constraints \(\sum u=U,\ v\cdot u=kJ_3\), excludes negative-infinite
normalized-surplus escape, and gives the fourth-order lower expression
\[
K(v)+\tfrac12\|u-(U+\rho H)\mathbf1/8-(\ell J_3/H)v+\rho v^2\|^2 .
\]
For a fixed limiting ordered imaginary profile \(v\), every subsequence
realizing the liminf has a further convergent real-correction subsequence.
The square is nonnegative and moments are continuous, so the liminf
is at least \(K(v)\). The constructed family attains it by (4).
This is the sole inherited analytic dependency; it is not supplied by
the finite jet checker. Its concentration, local energy and conditional
Schwarz–Pick inputs retain8619/8684's earlier explicit premises.

## Exact evidence and trust boundary

[field.py](field.py) implements a new standard-library rational field
\(\mathbb Q[Z]/(Z^{12}-Z^6+1)\), \(Z=e^{\pi i/18}\),
with \(i=Z^9,\ \omega=Z^4,\ c=(Z^2+Z^{34})/2\).
This cyclotomic polynomial is irreducible over \(\mathbb Q\);
the designated embedding is faithful. Conjugation sends \(Z\) to \(Z^{-1}\).
[poly.py](poly.py) tracks the six independent formal moment/control
variables. Whole coefficients are compared, with explicit exceptions
that remain active under optimized Python.
[intervals.py](intervals.py) brackets the unique root \(c>1/2\) of
\(8c^3-6c-1=0\) using 60 prescribed rational bisections of
\([939/1000,940/1000]\); exact closed interval operations verify signs.
The triple-angle identity and \(\cos(\pi/9)>1/2\) identify the embedding.
No floating-point sign, solver or sampled root enters the proof.

The finite program verifies fourth jets, root residuals, both curvatures,
both Jacobian blocks, complete objective/cost/defect maps and all seven
skewness counts. Literal profile checks use a fresh quadratic algebra
with the positive real radical, direct full eight-factor multiplication,
and sequential residual root solving. They are corroborating controls,
not a numerical realization certificate at positive \(\eta\).
Damaged mathematical identities are rejected before fixture comparison.
The universal all-root analytic continuation, desingularization,
uniform contraction, Taylor bounds, skewness extremum argument and
inherited sequence-rate theorem remain ordinary written mathematics.
No proof-assistant kernel or explicit numerical \(\eta_0\) is delivered.
