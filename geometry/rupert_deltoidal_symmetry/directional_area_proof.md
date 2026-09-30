# Tangential area reduction and directional transports certify half of a deltoidal receiver cell

**six-rupert-1 — researcher — 2026-09-30.**

For the standard deltoidal hexecontahedron, this proof improves the global
source-normal estimate to

\[
                 \operatorname{dist}(k,Gm)\le {153\over50}(A(k)-a_0).
                                                                    \tag{1}
\]

Selected support errors based on the original vertices' axial heights
then control the **complete** reduced roll interval. Composing the two
minimal normal transports with that roll gives a stronger all-source
receiver criterion. A homogeneous polynomial certificate applies it on
the **entire closed half-cell7 triangle**, including its corners and edges.
This triangle has **100 times** the preceding triangle's unit-z chart
area. One corner's unit normal has chord greater than **1/50** from the
minimizing normal. The full rotation remainder has margin **157/8000**.

For every receiver on this domain, closed projected containment at scale
at least one occurs exactly at scale one, zero translation, and the
120 proper relative rotations in two disjoint **left** cosets giving equal
shadows. All original source directions, full rotations and planar rolls
are allowed. Proper body images and antipodal receivers are included.
The global Rupert property remains **open**.

This is a complete written intermediate proof with exact finite
hypotheses, unformalized and without asserted independent review.
No claim of historical priority is made for the elementary tangent,
transport, quaternion or coefficient-sign arguments. The advance here
is their application with the deltoidal model and complete domain bounds.

## 1. Definitions, dependencies and the quantified receiver criterion

Let $K=\operatorname{conv}(V)=-K$, where $V$ is the ordered list of
62 original vertices in [verify.py](verify.py). The coordinate model,
its central symmetry, the full proper body group $G$ of order 60, and the
complete twelve-cell reflection chamber are the
[global-area proof's](global_area_proof.md) established hypotheses.
Its graph lemma is
bafkreigpe3pe5qqrekltisoss3zikl3znyydtso7utxsvag2yu2ykz3tsm,
source commit 5596212ab31932f7dd8b90cf6f1ad73c66afbe16.

For a unit normal $n$, let $P_n$ be orthogonal projection onto $n^\perp$
and $A(n)$ its physical projection area. Put $s=\sqrt5$ and

\[
 M=((3s-5)/6,(s-1)/6,1),\qquad m=M/\|M\|,\qquad
 a_0^2={3503950+1491850s\over31581}.
\]

The parent proves that $a_0$ is the global minimum and that its full
directed normal orbit is exactly $Gm$, including antipodes.
The [adaptive-area proof](adaptive_area_proof.md), graph
bafkreiejtc4l7y4ubwokktltjem2nb2rviz3ds3jld4yavourzxaacwc4m
at height 7410, source 2a0eb5428787e69876ac4652f7d8c192c07fa9e2,
supplies the thirteen corner area-gap checks, the minimum shadow's
complete proper group $C_2$, both signed roll probes, and persistent
weak contacts on the whole closed cells 4, 7 and 9. These exact
hypotheses and the full global-area computation are replayed here.

For a unit-z ray $u$ in any of these three whole cells define

\[
\begin{split}
 n&=u/\|u\|,& e&=A(n)-a_0,&
 \delta&=\|n-m\|,&a&=(153/50)e,\\
 E_0&=(29/100)(a+\delta)+(23/20)(a^2+\delta^2),\\
 E&=(29/100)a+(141/200)\delta+(23/20)(a^2+\delta^2),\\
 b&=2E,&
 \Theta_\perp&=(101/100)\sqrt{(a+\delta)^2+b^2}.
\end{split}                                                        \tag{2}
\]

Use the four contact triples from the following table. For $(p,q,j)$,
set $f_j=V_q-V_p$, $\mu_j(u)=f_j\times u$,
$T_j(u)=V_j\times\mu_j(u)$ and

\[
          r_i(u)=\min_{\|z\|=1}\max_j z\cdot T_j(u).
\]

| Whole closed cell | Four actual contact triples |
| --- | --- |
| 4 | (59,55,55), (36,20,36), (17,4,4), (17,4,17) |
| 7 | (43,57,43), (57,61,57), (57,61,61), (45,34,34) |
| 9 | (59,55,55), (58,45,58), (45,34,34), (45,34,45) |

**Directional all-source receiver criterion.** Suppose

\[
 \delta\le1/20,\quad a\le1/10,\quad E_0\le1/28,\quad b\le1/10,
 \qquad r_i(u)>{23\over16}\|u\|\Theta_\perp.                          \tag{3}
\]

Then, for every proper rotation $Q$, every planar translation $t$ and
every $\lambda\ge1$,

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\ \cup\ J_nG,\qquad J_n=2nn^T-I.      \tag{4}
\]

The two left cosets in (4) are disjoint and contain exactly 120 proper
rotations. In particular no strict passage is possible at these
receivers. The criterion contains the **entire** preceding adaptive
sufficient domain, not just its explicit triangle; see Section 7.

## 2. A tangential proof of the global source estimate

At each of the thirteen nonminimal chamber corners $u_j$, the preceding
checker verifies, with $D_j=\|u_j-M\|^2$ and $q_j=A(u_j/\|u_j\|)^2$,

\[
 L_j=q_j-a_0^2-D_j/9>0,\qquad L_j^2>4a_0^2D_j/9.                   \tag{5}
\]

These positive-branch tests imply
$A(u_j/\|u_j\|)-a_0>\sqrt{D_j}/3$. At $u_j=M$ both quantities vanish.
Normalization on a unit-z segment is 1-Lipschitz, since its derivative
has norm $1/\|x\|\le1$. Consequently

\[
 \|P_m(u_j/\|u_j\|)\|
 \le\|u_j/\|u_j\|-m\|\le\sqrt{D_j}
 \le3(A(u_j/\|u_j\|)-a_0).                                        \tag{6}
\]

For any point in a whole closed cell, write
$u=\sum_j\lambda_j u_j$, $\lambda_j\ge0$, $\sum_j\lambda_j=1$.
With $n_j=u_j/\|u_j\|$ and
$w_j=\lambda_j\|u_j\|/\|u\|$, one has

\[
 n=\sum_j w_jn_j,\quad \sum_jw_j\ge1,\quad
 e=\sum_jw_j(A(n_j)-a_0)+a_0(\sum_jw_j-1)
       \ge\sum_jw_j(A(n_j)-a_0).                                  \tag{7}
\]

The area identity uses the parent's actual linear area vector on this
whole cell. Tangential projection is linear even though normalization
is not. Equations (6)--(7) give

\[
                          \|P_mn\|\le3e.                          \tag{8}
\]

There is a uniform acute-angle cap on the complete chamber. At its three
corners $x$, the new checker proves

\[
 M\cdot x>0,\qquad
 (M\cdot x)^2>c^2\|M\|^2\|x\|^2,\qquad c=2399/2601.               \tag{9}
\]

Linearity and the norm triangle inequality extend $m\cdot n>c$ to
every normalized point of the closed chamber. For $z=m\cdot n$,

\[
 {\|n-m\|^2\over\|P_mn\|^2}={2\over1+z}
 \le {2\over1+c}=(51/50)^2,                                      \tag{10}
\]

with the $n=m$ case handled directly. Combining (8) and (10) proves
$\|n-m\|\le(153/50)e$. Fold arbitrary normals by actual orthogonal
body symmetries into the chamber. They preserve areas, and the full
minimum orbit is $Gm$, including the antipodes. This proves (1).
In particular the proper source gauge used below always exists.

The previous coefficient 6 arose from normalizing a convex combination
and using a two-term norm estimate. The tangential calculation retains
the exact weighted area excess and avoids that loss. This is a proof
improvement; a failed smaller constant in the earlier checker did not
disprove smaller constants obtained by a different argument.

## 3. Support-specific minimal normal transports

The new checker verifies $\|V_j\|<R=23/10$ for all 62 vertices.
Let $R_*$ be the minimal proper rotation carrying $m$ to a nearby unit
normal, and let its operator chord be $d=\|R_*-I\|$. Its axis is
perpendicular to $m$. In the transport plane choose a unit $v$ perpendicular
to $m$; if its angle is $\beta$ then

\[
 P_m(R_*^T-I)x=
       \bigl[-(x\cdot m)\sin\beta+(x\cdot v)(\cos\beta-1)\bigr]v.
\]

Thus for every original vertex, every transport sign, and every unit
direction in $m^\perp$,

\[
 \|P_m(R_*^T-I)V_j\|
       \le h_jd+(R/2)d^2,\qquad h_j=|V_j\cdot m|.                 \tag{11}
\]

Identity transports are included. This formula supplies selected
support errors; these errors are not asserted to be Hausdorff bounds
for the entire transported shadow.

Let $r_j=\|P_mV_j\|$. Only $j=4,57$ achieve the maximum radius
$R_0$, and they project to antipodes. The parent supplies

\[
 R_0^2=(155+65s)/58>4,\qquad r_j^2\le5\ (j\ne4,57),\qquad
                         R_0-\sqrt5>1/28.                        \tag{12}
\]

The new checks improve (12), jointly using each original radius and height:

\[
             r_j+(1/20)h_j\le\sqrt5\qquad(j\ne4,57),\qquad
                         h_{57}<29/100.                           \tag{13}
\]

No approximate square root is used. With $q=r_j^2$, $H=h_j^2$,
$d_0=1/20$, (13) is checked by the equivalent positive-branch tests

\[
 L=5-q-Hd_0^2\ge0,\qquad L^2\ge4qHd_0^2.                          \tag{14}
\]

All 60 nonmaximum vertices are included, with equality allowed.

There are two signed roll-support probes:

| Edge | Supporting vertex | Roll derivative sign |
| --- | --- | --- |
| (57,59) | 57 | + |
| (41,57) | 57 | − |

For an edge $(p,q)$ let $\widehat\mu=((V_q-V_p)\times M)/
\|(V_q-V_p)\times M\|$ and
$g_j=\widehat\mu\cdot(V_{57}-V_j)\ge0$. Both probes satisfy

\[
 \widehat\mu\cdot V_{57}<9/4,\qquad
 |m\cdot(V_{57}\times\widehat\mu)|>3/4,\qquad
             g_j\ge(1/20)(h_j-\kappa),\quad\kappa=141/200.          \tag{15}
\]

The last inequality is checked for **all 62 original vertices** for each
probe. The four support ties are respectively
$(53,57,59,61)$ and $(41,43,44,57)$; each tie's height is below $\kappa$.
For the exact check put
$G_j^2=g_j^2/d_0^2$, $H_j=h_j^2$ and
$L_j=H_j-\kappa^2-G_j^2$. If $L_j\le0$ the comparison is automatic;
otherwise the checker requires $L_j^2\le4\kappa^2G_j^2$.
These tests are equivalent to $h_j\le\kappa+g_j/d_0$, with all quantities
nonnegative. They handle ties and both branches without unrecorded
square-root assumptions.

For $\delta\le d_0$, (15) and (11) imply the full receiver-support upper
bound **in each of these two selected directions**:

\[
 h_{P_mR_2^TK}(\widehat\mu)
 \le\widehat\mu\cdot V_{57}+\kappa\delta+(R/2)\delta^2.              \tag{16}
\]

Indeed $-g_j+h_j\delta\le\kappa\delta$ for every candidate vertex:
if $h_j\le\kappa$, use $g_j\ge0$; otherwise use
$g_j\ge d_0(h_j-\kappa)\ge\delta(h_j-\kappa)$.
There is no missing candidate in the receiver maximum.

## 4. Deriving the reduced roll from arbitrary source rotations

Start with any closed containment in (4). Central convex symmetry gives,
for every planar unit vector $z$,
$\lambda h_{P_nQK}(z)\le h_{P_nK}(z)-|t\cdot z|$.
It implies centered containment at scale one. Put $k=Q^Tn$.
Area monotonicity and (1) provide an actual proper body rotation $h\in G$
such that

\[
                         \|h^Tk-m\|\le a.                         \tag{17}
\]

Let $R_1,R_2$ be the minimal proper rotations taking $m$ to $h^Tk$ and
$n$. Their chords are at most $a$ and exactly $\delta$. Let $B_0$
be a properly oriented orthonormal frame on $m^\perp$ and
$B_2=B_0R_2^T$. There is a proper planar rotation $U$ with

\[
 B_2Qh=UB_0R_1^T,\qquad
              UP_mR_1^TK\subseteq P_mR_2^TK.                       \tag{18}
\]

The complete minimum-shadow group is $C_2$. Use the proper **left**
gauge $J_n^\sigma Qh$ to reduce the angle of $U$ to
$\alpha\in[-\pi/2,\pi/2]$. This gauge preserves the original projected
source because $K=-K$; it fixes the source cross-product normal.

Write $x=P_mV_{57}$ and probe the necessary containment (18) in
$q=Ux/R_0$. This is a unit direction even for a remote reduced roll.
Equation (11) gives

\[
 R_0-(29/100)a-(R/2)a^2
 \le \max\{R_0\cos\alpha+(29/100)\delta+(R/2)\delta^2,\
                         \sqrt5+(R/2)\delta^2\}.                  \tag{19}
\]

The second branch uses (13) for **all** nonmaximum original vertices.
It is impossible when $E_0\le1/28$, since (12) is a strict gap.
Hence, for the roll chord $r=2\sin(|\alpha|/2)$,

\[
               r^2\le2E_0/R_0\le E_0<1/25,\qquad r<1/5.           \tag{20}
\]

This excludes the entire remote roll interval. No small-roll assumption
has been made. If $r=0$ there is nothing further to prove.
For $r>0$ select the probe in (15) with the matching derivative sign.
Its untransported support increment divided by $r$ is at least

\[
 (3/4)\cos(\alpha/2)-(9/4)(r/2)
   >(3/4)(99/100)-(9/4)(1/10)=207/400>1/2.                         \tag{21}
\]

The chosen source vertex's transport error is at most
$(29/100)a+(R/2)a^2$, and (16) bounds the receiver maximum.
Necessary containment therefore bounds its support increment by $E$.
Together with (21) this gives

\[
                              r\le2E=b.                           \tag{22}
\]

Both roll signs, all support ties and the zero-error cases have been
accounted for. The constants $E_0,E$ retain their selected-probe meaning.

## 5. The structured full rotation angle and the torque obstruction

In the proper frame of (18), the gauged three-dimensional rotation is

\[
                         Q'=J_n^\sigma Qh=R_2WR_1^T,              \tag{23}
\]

where $W$ fixes $m$ and has chord at most $b$. The axes of $R_2$ and
$R_1^T$ are perpendicular to $m$; the axis of $W$ is $m$.

We use six-rupert-3's structured rotation-composition lemma, published in
[ORTHOGONAL_COMPOSITION_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5,
graph bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y
at height 7414. Its perpendicular-axis hypotheses hold exactly in (23).
The full proof of the elementary lemma is included here for clarity.
No RID coordinates, diameter reduction or receiver constants are imported.

For perpendicular transport axes $x,y$ and signed roll sine $t$,
write the positive-cosine quaternion lifts with chords $d,a,b\le1/10$.
The scalar of their product is

\[
 w=c_dc_bc_a-{ad\over4}
              \{c_b\,x\cdot y+t(x\times m)\cdot y\},\qquad
 c_j=\sqrt{1-j^2/4},\quad |t|=b/2.
\]

The vector $c_bx+t(x\times m)$ is unit, so the braces are at most one.
Put

\[
 P=(1-d^2/4)(1-a^2/4)(1-b^2/4),\quad p=\sqrt P,\quad W_0=p-ad/4.
\]

Then $w\ge W_0>99/100-1/400>0$, and the exact identity

\[
 (a+d)^2+b^2-4(1-W_0^2)
 =2ad(1-p)+{a^2d^2(8-b^2)\over16}+{b^2(a^2+d^2)\over4}\ge0          \tag{24}
\]

gives $\|Q'-I\|\le\sqrt{(a+d)^2+b^2}<1/4$. The checker's polynomial
expansion verifies (24) modulo $p^2=P$; the continuum comparison is
the displayed nonnegative identity and positive quaternion branch.
For a chord below $1/4$, differentiating $2\arcsin(c/2)$ gives angle
at most $(101/100)c$, since $(101/100)^2(63/64)>1$.
Consequently the **full principal proper rotation angle**, derived from
arbitrary original $Q$, is at most $\Theta_\perp$ in (2).

All contact normals in the table are actual weak outer supports on their
whole closed cells. The previous 2,480 original-vertex comparisons are
replayed; linearity in $u$ proves persistence, with no strict exposure
or assumed facet stability. Their edge lengths are less than $5/4$.
For a nonzero gauged angle $\theta$ and rotation vector $v$,
some contact has $v\cdot T_j(u)\ge\theta r_i(u)$.
The integral Taylor remainder for rotation gives

\[
 \mu_j(u)\cdot(Q'V_j-V_j)
 \ge\theta r_i(u)-{23\over16}\|u\|\theta^2.                         \tag{25}
\]

Here $\|V_j\|<23/10$ and $\|\mu_j(u)\|<(5/4)\|u\|$; the bound
$\|Q'V_j-V_j-v\times V_j\|\le\|V_j\|\theta^2/2$ holds for the full
angle. The last condition in (3) makes (25) positive for every nonzero
$\theta$, contradicting centered closed containment. Thus $Q'=I$.
Undoing the actual right body gauge and left half-turn gives
$Q\in G\cup J_nG$. The converse follows from body symmetry and $K=-K$.
Positive equal areas force $\lambda=1$, and equal support functions
force $t=0$.

The parent's exact Frobenius separation

\[
 \min_{g\in G}\|J_m-g\|_F^2=(106-36s)/29>8(1/20)^2
\]

exceeds $\|J_n-J_m\|_F^2=8(1-(n\cdot m)^2)\le8\delta^2$.
Therefore $J_n\notin G$ and the two left cosets contain 120 distinct
proper rotations. Conjugation by $g\in G$ transports the statement to
its receiver image. Replacing $n$ by $-n$ preserves $P_n$ and $J_n$.
This completes the proof of (3)--(4).

## 6. Exact certification of the entire closed half-cell7 triangle

The whole parent cell7 is $\operatorname{conv}(M,N_7,N_8)$, where

\[
 N_7=((25-7s)/38,(9-s)/38,1),\qquad
 N_8=((5-s)/10,(-5+3s)/10,1).
\]

Define

\[
 U_7=(M+N_7)/2,\qquad U_8=(M+N_8)/2,\qquad
                  \mathcal T=\operatorname{conv}(M,U_7,U_8).        \tag{26}
\]

This is a whole **closed** triangle, not three isolated receivers.
Its affine mix is $1/2$, versus the preceding $1/20$; its chart area
is exactly 100 times the old area and one quarter of the whole cell's.

### 6.1 Continuous normal, chart and actual-area bounds

At all three corners, the checker verifies

\[
 \|u-M\|<H=239/10000,\quad \|u\|<L=53/50,\quad
 M\cdot u>0,\quad (M\cdot u)^2>\ell^2\|M\|^2,\quad \ell=21/20.       \tag{27}
\]

Convexity extends the two upper bounds throughout $\mathcal T$.
Linearity extends $M\cdot u>\ell\|M\|$; Cauchy's inequality gives
$\|u\|>\ell$ throughout. Unit-z normalization is 1-Lipschitz, so
$\delta<H<1/20$.

Let $C_7$ be the actual parent area vector and
$D=C_7-(C_7\cdot M)M/\|M\|^2$. The checker verifies
$D\cdot M=0$, $C_7\cdot M/\|M\|=a_0$, and at all three corners

\[
                  D\cdot(u-M)<\ell e_*,\qquad e_*=153/10000.         \tag{28}
\]

The functional in (28) is linear, hence the inequality holds throughout
the triangle. For every such point the **actual** projection area obeys

\[
 0\le e=a_0(m\cdot n-1)+{D\cdot(u-M)\over\|u\|}<e_* .              \tag{29}
\]

This uses the norm lower bound in (27). It does not presume that physical
projection area achieves its maximum at a corner.

The corner $U_7$ has normal chord greater than $1/50$ from $m$.
The exact check is the positive-dot comparison

\[
 (1-1/(2\cdot50^2))^2\|M\|^2\|U_7\|^2>(M\cdot U_7)^2.             \tag{30}
\]

### 6.2 A continuous certificate for the actual torque tetrahedron

Let $u=\lambda_0M+\lambda_1U_7+\lambda_2U_8$,
$\lambda_j\ge0$, $\sum\lambda_j=1$. Each of the four actual torque
columns is linear:

\[
 T_j(u)=\sum_{k=0}^2\lambda_k T_j(u_k),\qquad (u_0,u_1,u_2)=(M,U_7,U_8).
\]

The checker verifies all 744 original-vertex support comparisons at
the three corners, including weak ties; linearity extends them everywhere.
For the four columns it constructs the four homogeneous cubic cofactors

\[
 w_j(\lambda)=-(-1)^j\det(T_k(\lambda):k\ne j).
\]

**All 40 degree-three monomial coefficients are strictly positive.**
The exact polynomial balance $\sum_jw_jT_j=0$ is checked in every
coordinate. For any point of the closed barycentric simplex, each $w_j$
is positive; nonzero triple determinants give rank three. The positive
balance gives a strict convex representation of the origin.
The columns are affinely independent: their one-dimensional linear
dependence space is generated by $w$, whose coefficient sum is positive.
Thus they form a nondegenerate tetrahedron with the origin in its interior
everywhere, including all triangle boundaries.

For its facet opposite column $j$, let $a,b,c$ be the other columns,
$N_j=(b-a)\times(c-a)$ and $H_j=N_j\cdot a$.
Their entries are homogeneous of degrees two and three, respectively.
The checker verifies $H_j=-(-1)^jw_j$ as a polynomial identity, so
$H_j$ and $N_j$ never vanish on the closed simplex. Put $\rho=43/250$.
For each of the four facets form the degree-six homogeneous polynomial

\[
 F_j(\lambda)=H_j(\lambda)^2
       -\rho^2\|N_j(\lambda)\|^2(\lambda_0+\lambda_1+\lambda_2)^2.    \tag{31}
\]

**All 112 degree-six monomial coefficients are strictly positive.**
There are 28 for each facet; none is undecided or omitted. Therefore
$F_j>0$ at every nonzero nonnegative barycentric vector. On the simplex
its sum is one, so (31) proves every facet distance from the origin
is strictly greater than $\rho$. Because interiority and all four
facets have been certified, the actual torque hull contains the
centered ball of radius $\rho$ throughout the whole triangle:

\[
                         r_7(u)>43/250.                           \tag{32}
\]

The finite certificate is reconstructed from exact coordinates; it is
not a list of sampled facet distances. Direct evaluations at the three
corners and barycenter audit the polynomial formulas, but the 40 cubic
and 112 sextic coefficient signs establish the continuous claim.

### 6.3 Phase gates and the full rotation remainder

Using (27)--(29) in the monotone nonnegative expressions (2), set

\[
 a_*=(153/50)(153/10000)=23409/500000,\qquad d_*=239/10000.
\]

The exact rational comparisons give

\[
\begin{split}
 (29/100)(a_*+d_*)+(23/20)(a_*^2+d_*^2)&<1/28,\\
 2\{(29/100)a_*+(141/200)d_*+(23/20)(a_*^2+d_*^2)\}&<17/250,\\
 (101/100)^2\{(a_*+d_*)^2+(17/250)^2\}&<(1/10)^2.
\end{split}                                                       \tag{33}
\]

Both transport chords and the roll chord are below $1/10$.
The full angle satisfies $\Theta_\perp<1/10$. Equations (27), (32)
and (33) give the explicit continuous remainder margin

\[
 r_7(u)-{23\over16}\|u\|\Theta_\perp
 >{43\over250}-{23\over16}{53\over50}{1\over10}
 ={157\over8000}>{1\over60}.                                      \tag{34}
\]

All hypotheses in (3) now hold at every point of $\mathcal T$.
This proves the entire closed receiver result claimed in (26),
with all original source rotations covered by the earlier reduction.

## 7. Relation to preceding bounds and remaining frontier

Let $a_{\rm old}=6e$, $x=a_{\rm old}+\delta$.
The preceding criterion required $(5/2)x\le1/28$, hence $x\le1/70$.
Our $a\le a_{\rm old}$, $\delta\le x<1/20$ and

\[
 E_0\le(29/100)x+(23/20)x^2<1/28,\qquad
 b\le2(141/200+(23/20)x)x<5x\le1/14.
\]

Also $\Theta_\perp\le(101/100)(a+\delta+b)\le(303/50)x$,
the old full-angle bound. The new torque remainder coefficient
$23/16$ is smaller than the old $25/16$. Hence every receiver
satisfying the entire old criterion still satisfies the new one.
The global exact extrema, universal scale bound below 1.014, and old
tiny all-source caps remain valid.

The separate uniform strict small-angle gap, own graph
bafkreifnp5u7bnnjoxqysdxep55lhl6ohvvro6jmagbdw4wacpdae2eryy
at height 7322, source 58ec651cdd077243b556287369b6f56132735f6d,
remains a closed qualitative local phase. It is existential and is
not used as a numerical global covering here. Its counterpart for J77,
six-rupert-2's graph bafkreiar5zgul6vfndfhkjkvg5cpkuewkkipybatfsbeo6iqojlbeqtbci
at height 7330, also does not resolve a global Rupert question.
Neither author claim implies independent review of the present proof.

The exact new geometric frontier is the complementary receiver domain:
the rest of cell7 and the remaining chamber cells after symmetry, together
with the nonlocal rotation range not eliminated there. The actual
tetrahedron certificate suggests that receiver-specific area and torque
bounds on closed pieces could extend this domain. Alternatively an
exact strict passage witness in the complement must include all original
vertices and a positive strict support margin. No passage or global
non-Rupert proof is provided by this local-domain theorem.

## 8. Reproduction, finite evidence and trust

Use Python 3.11+ standard library, one process and one thread:

~~~
python3 -B geometry/rupert_deltoidal_symmetry/directional_area_certificate.py --self-test
~~~

Compare every output field with
[expected_directional_area.json](expected_directional_area.json).
The checker fully replays the global parent and adaptive finite
hypotheses, including the 45,632 whole-cell support comparisons in the
global parent and the 2,480 persistent weak-contact comparisons in
the adaptive parent. It verifies the new three chamber caps, 62 body
radius bounds, 60 joint radial-height bounds, 124 signed-support
gap-height comparisons, 744 patch supports, 40 strictly positive cubic
coefficients, 112 strictly positive degree-six coefficients, exact
polynomial balance/facet/rotation identities and rational phase margins.
The expected output records a canonical coefficient SHA256 and direct
evaluation audits. All proof decisions use ordered $\mathbb Q(\sqrt5)$
and rational arithmetic. Python optimization mode is refused.

Ten malformed controls are rejected: an unsupported normal gate,
source height, receiver height, body radius or chamber cap; an omitted
roll sign; a reversed actual support; an unsupported torque ball;
a larger triangle with unchanged bounds; and a missing triangle corner.
Rejection of an unsupported larger triangle is failure of these fixed
sufficient estimates, not a nonexistence theorem for that triangle.
Private float probes were used only to size candidate constants; no
float, solver transcript, private input, external package, large proof
corpus or sampled cover is a proof premise.

The external trust boundary is the mathematical coordinate model, the
ordered-field implementation, complete exact generation/replay, and
the unformalized weighted-area, proper-frame, selected-support,
quaternion, polynomial-interiority and Taylor arguments written above.
Matching fixture output supplies regression evidence. It does not
substitute for those continuous mathematical bridges or independent review.

## 9. Primary literature and complementary authorship

The latest primary status checked on 2026-09-30 is the deltoidal
entry in [Gosain--Grimmer, arXiv:2509.08190, Table 3](https://arxiv.org/html/2509.08190);
it remains unresolved. The required
[arXiv:2604.26531](https://arxiv.org/html/2604.26531) gives the standard
proper-rotation strict-shadow definition and current context; its
rhombicosidodecahedron non-Rupert statement is a conjecture.
[arXiv:2508.18475](https://arxiv.org/abs/2508.18475) proves a non-Rupert
example for a different explicitly constructed convex body. It does
not solve the deltoidal or RID cases.

The support-height mechanism was prompted by complementary work:
six-rupert-2's [J77 directional-transport proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_directional_receiver_domains/PROOF.md),
graph bafkreihbeoxtt3rmagrfbwqkn47u3oqm6jt55v7ffayh5yqnxt72fo6eym,
source f7cfae81911e86c562b226a04f7966989812f94d;
and six-rupert-3's
[RID directional-transport proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/DIRECTIONAL_TRANSPORT_PROOF.md),
graph bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u,
source 30c9c86753797307cc17b56ffd76aa88d94987df.
The new RID composition lemma at 7414 is explicitly used in Section 5.
The [RID actual-torque-hull proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ACTUAL_TORQUE_HULL_PROOF.md),
graph bafkreiepyjhiavm5s4reqzgverqayeq6dhmjsof4g4xutfnsw7a6wafipm,
source 684f35df160134d1fefb14da75f5948ce8ac00ce, supplies useful methodological
context for certifying an actual hull rather than only moving its center.
Every solid-specific constant, vertex comparison and receiver domain here
is derived anew for the deltoidal hexecontahedron.

The final refresh also read six-rupert-2's
[complete J77 signed-region classification](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_sharp_region_gap/PROOF.md),
source 2def43a003a2a692571ae654c543517b1cb20e6b, graph
bafkreieoes3bbhpwp53w22xek5ky7mrwmhcdxnb37fex5c2gox4zalouua
at height 7438. It uses actual nearest-point certificates for every
signed region of J77's antipodal-core axial function, giving a sharp
regional gap and a larger receiver domain when the actual diameter
hypothesis holds. This is context for possible future source reductions;
its axial function, regional gap and asymmetric translation arguments
are not premises of the present deltoidal theorem.
