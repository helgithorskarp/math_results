# Original-source rigidity on the entire closed 1/4 Cell8 collar

**six-rupert-1, researcher, 2026-10-01.** Complete author-checked written
intermediate proof with exact finite hypotheses. It is unformalized and
independently unreviewed; historical priority and sharpness are unasserted.
The global Rupert property of the original deltoidal hexecontahedron
remains **open**.

Let $K=\operatorname{conv}V=-K$ be the original 62-vertex body in
[verify.py](verify.py), and $G\subset SO(3)$ its 60 proper body rotations.
For unit $n$, put $P_n=I-nn^t$, $J_n=2nn^t-I$. Retain the exact chart
numbering of [expected_global_area.json](expected_global_area.json):
$$
\begin{gathered}
s=\sqrt5>0,\quad M=N_9=((3s-5)/6,(s-1)/6,1),\quad m=M/\|M\|,\\
N_8=((5-s)/10,(-5+3s)/10,1),\quad N_{10}=((3-s)/2,(7-3s)/2,1),\\
W=((75-17s)/114,(7+5s)/114,1),\quad U=(N_6+N_{11}+N_{10}+N_8)/4,\\
Z_t=(1-t)W+tU,\quad L=\operatorname{conv}(N_8,W,Z_{1/4}),\\
B=\operatorname{conv}(W,N_{10},Z_{1/4}),\quad
F_{1/4}=\operatorname{conv}(N_8,N_{10},Z_{1/4})=L\cup B.
\end{gathered}                                                    \tag{1}
$$

**Theorem.** For every $n=u/\|u\|$, $u\in F_{1/4}$, and every
proper-body or antipodal image of such a receiver, every original
$Q\in SO(3)$, planar translation $t$, and scale $\lambda\ge1$,
$$
\lambda P_n(QK)+t\subseteq P_nK
\quad\Longleftrightarrow\quad
\lambda=1,\quad t=0,\quad Q\in G\cup J_nG.                         \tag{2}
$$
These are two disjoint **left** cosets, exactly 120 proper rotations.
Thus strict passage is excluded on the entire closed quarter collar.
The entire Cell8 and the global named-solid problem remain open.

The [whole one-fifth collar](cell8_fifth_proof.md), source
**08fe6643bf9eedf2f225b69eab0f25dff06f80c0**, graph **8238**, is the direct
parent. Both larger quarter triangles are freshly proved here. In
particular the new second triangle is not inferred from the older one.
Since $W=(1-r)N_8+rN_{10}$, $r=(17+4s)/57\in(0,1)$, (1) is an explicit
closed partition including the common edge. All older receiving exclusions
remain valid, and their combined domain strictly grows.

## 1. Fresh physical area and global original-source bounds

Cell8 is $\operatorname{conv}(N_6,N_{11},N_{10},N_8)$. Its physical
Euclidean projection area is $A(n)=C_8\cdot n$, with the original vector
in [global_area_proof.md](global_area_proof.md), graph7378. Fresh complete
corner, admitted edge-stationary and interior-stationary maximization gives:

| piece | exact maximum $A(n)^2$ | active stratum | strict budget $T$ | source chord $a$ | receiver chord $d$ |
|---|---|---|---|---|---|
| $L$ | $(381962042950+170427163870s)/3469463029$ | $Z_{1/4}$ | $3707533/250000$ | $14141/125000$ | $15227/200000$ |
| $B$ | $(193588974348400+86313658482800s)/1757705199129$ | interior of $N_{10}$--$Z_{1/4}$ | $14830423/1000000$ | $113349/1000000$ | $21027/200000$ |

The second maximum is **not** a corner maximum. All critical admissions
and the strict $T^2$ comparisons are replayed. Acute chord caps are convex
cones, so $\|n-m\|<d$ at the three raw corners implies the same strict
bound on the whole closed receiving triangle.

The complete [source-critical mechanism](source_extrema_proof.md),
graph7918, is freshly replayed at each separate budget: all 12 closed
original source fan cells, unsquared cone/area/unit constraints, and both
radical branches. Each run has 214 critical candidates: 40 corners,
24 sphere-stationary, 20 area-stationary, 80 edge-stationary, and
50 area/edge intersections. Exactly 56 are feasible, with every cap margin
strict. The unique farthest direction occurs on Cell8/edge1 and
Cell10/edge2, with chord in $(a-10^{-6},a)$. Thus globally,
$$
A(k)\le T\quad\Longrightarrow\quad
\operatorname{dist}(k,Gm)<a                                      \tag{3}
$$
for every original unit source normal $k$. Source nearness is derived,
with no initial chamber, spatial-angle or roll premise.

The original full reflection group has 120 elements. Let $S$ be the
parent's third-wall reflection, $SM=M$, $\det S=-1$, permuting all
62 originals. Choose $f$ in that full group with $f^tQ^tn\in H$, the
closed fundamental chamber. If $\det f=1$, use the actual right body
factor $h=f$. If $\det f=-1$, use $h=fS\in G$, so
$h^tQ^tn=Sf^tQ^tn\in SH$. Both proper source charts $H,SH$, each with
12 closed fan cells, are included. This explicit transpose convention
gives the actual right gauge; an improper rotation is never used as one.
Since $Sm=m$, the strict chord bound applies in both charts.

## 2. Actual proper frames and full signed roll

Suppose (2)'s containment holds. Central symmetry and convex midpoints
remove translation as a necessary condition; contraction toward zero
removes scale. Hence $P_n(QK)\subseteq P_nK$ and
$A(Q^tn)\le A(n)<T$. Let $R_1,R_2$ be the minimal proper transports
$m\mapsto h^tQ^tn$, $m\mapsto n$. A left $J_n$ preserves the projected
source because $P_nJ_n=-P_n$ and $K=-K$. Therefore some
$\epsilon\in\{0,1\}$ gives the actual factorization
$$
Q'=J_n^\epsilon Qh=R_2C_\alpha R_1^t,\qquad
-\pi/2\le\alpha\le\pi/2.                                         \tag{4}
$$
Put $\sigma=\operatorname{sign}\alpha$,
$x=\tan(|\alpha|/2)\in[0,1]$. Use the 16 exact original reference
probes $(\mu,H_\mu)$, $\mu\cdot M=0$, and the 62 originals plus
12 verified convex source points. Necessary containment implies, for
each actual $p\in K$,
$$
\mu\cdot C_\alpha R_1^tp
\le\max_{v\in V}\mu\cdot R_2^tv\le H_\mu+B_\mu.                    \tag{5}
$$

For each receiving piece the signed
[rank-transport bound](rank_transport_wedge_proof.md), graph7976,
is freshly computed. If $\eta\ge\|\mu\|$, $r_v\ge\|P_mv\|$, and the
parent corner-ratio mechanism encloses $\mu\cdot u/(M\cdot u)$
between $l,h$, then throughout the closed triangle
$$
B_\mu=\max\left(0,\max_{\substack{v\in V\\\xi\in\{l,h\}}}
 [-M\cdot v\,\xi-(H_\mu-\mu\cdot v)
           +(d^2/4)(\eta r_v-\mu\cdot v)]\right).                 \tag{6}
$$
Each case replays all 1984 original vertex/endpoint comparisons.

Set $c_s=1-a^2/4$, $\gamma=\mu\cdot p$, and use the exact outward
lower $\tau_\sigma\le\sigma\mu\cdot(m\times p)$. The parent gives
the necessary concave quadratic
$$
\begin{split}
&(c_s\gamma-H_\mu-E)+2c_s\tau_\sigma x
               +(-c_s\gamma-H_\mu-E)x^2\le0,\\
&E=\eta\,|m\cdot p|_{\rm upper}a
          +(a^2/4)\eta\,\|P_mp\|_{\rm upper}+B_\mu.
\end{split}                                                      \tag{7}
$$
Strict positive endpoint values exclude an entire closed interval.
[expected_cell8_quarter.json](expected_cell8_quarter.json) fixes
15 standard intervals for $L$ and 19 for $B$. They cover both signs
on $[1/10,1]$, except the positive $L$ intervals
$$
I_0=[151/160,311/320],\qquad I_1=[311/320,1].                       \tag{8}
$$
The two intervals in (8) are proved next. The checker verifies consecutive
closed coverage, every endpoint and both signed branches. No height-cover
premise is used on $B$: its 19 standard intervals suffice.

## 3. Fresh signed-height source covers on both proper charts

The universal signed source-height transport and polygon maximum
argument is proved in [cell8_fifth_proof.md](cell8_fifth_proof.md),
Sections3--4. We apply it at the **new** $L$ budget; no old budget
or fixed certificate is extended beyond its domain. Write a gauged
source $q=M+w$, $M\cdot w=0$, $k=q/\|q\|$, and
$$
c=m\cdot k>c_0=1-a^2/2>0,\quad
\|w\|^2<U_0=M^2(c_0^{-2}-1),\quad M^2=M\cdot M.                    \tag{9}
$$
The exact minimal transport is
$$
P_mR_1^tp=P_mp-\frac{M\cdot p}{\|M\|\|q\|}w
                    -\frac{p\cdot w}{\|q\|(\|q\|+\|M\|)}w.        \tag{10}
$$
For positive roll define $z=M\times\mu$,
$\widetilde\mu=(1-x^2)\mu-2xz/\|M\|$, $h_p=M\cdot p$,
$l(c)=c/M^2$, $b(c)=c^2/[M^2(1+c)]$. Then
$$
(1+x^2)\mu\cdot C_\alpha R_1^tp
=\gamma(1-x^2)+2\mu\cdot(m\times p)x
 -[l(c)h_p+b(c)(p\cdot w)]\,(\widetilde\mu\cdot w).                \tag{11}
$$
The loss is signed. A negative upper loss gives a uniform source-support
increase and is retained.

Let $\bar l,\bar b,e_l,e_b$ be endpoint midpoints and halfwidths on
$[c_0,1]$. Both functions increase there. The unchanged axis length has
$$
21199/20000<\|M\|<1059951/10^6,\quad
I_M=21199010000/22469901249,\quad I_E=10000/22469901249,
\quad |\|M\|^{-1}-I_M|<I_E.
$$
For $I=[lo,hi]$ in (8), take outward exact grid bounds
$R_w\ge\sqrt{U_0}$, $r_p\ge\|P_mp\|$, $r_z\ge\|z\|$.
The loss in (11) is at most
$$
\begin{split}
&[\bar l h_p+\bar b(p\cdot w)]\,([(1-x^2)\mu-2xI_Mz]\cdot w)+Err,\\
Err={}&e_l|h_p|(1+hi^2)\eta R_w+e_b r_p(1+hi^2)\eta U_0\\
&+[l(1)|h_p|+b(1)r_pR_w]\,2hi I_Er_zR_w.                         \tag{12}
\end{split}
$$
Every factor and error is fresh. The error applies to actual sources
satisfying (9); the outer polygon corners need not lie inside that cap.

Use $w=y_1(1,0,-M_x)+y_2(0,1,-M_y)$. The fresh inverse-Gram bounds are
$|y_1|<58031/500000$, $|y_2|<7387/62500$. Sixteen closed Cauchy
half-planes give a 20-corner cap enclosure. Intersect each actual fan
cone and its necessary area cut
$$
C_{cell}\cdot(M+w)\le T(1059951/10^6)/c_0.                        \tag{13}
$$
Reflect the **complete** enclosures by $S$ to cover $SH$; no cap-polygon
reflection invariance is assumed. At each fixed root or child, apply
two tighter necessary area cuts using
$$
\|q\|\le\operatorname{upper\_sqrt}
  (M^2+\min(U_0,\max_{\rm corners}\|w\|^2)).                       \tag{14}
$$
Convexity proves the norm bound and both cuts retain every actual source.
Closed clipping keeps segments and singletons. Fixed trees split the longer
coordinate range at its midpoint, retain both closed halves, and have
depth at most **one**. All 24 fan copies are covered in each interval.

The three roll-Bernstein coefficient vectors are
$$
v_0=(1-lo^2)\mu-2lo I_Mz,\quad
v_1=(1-lo\,hi)\mu-(lo+hi)I_Mz,\quad
v_2=(1-hi^2)\mu-2hi I_Mz.                                        \tag{15}
$$
For each $j$, maximize
$[\bar l h_p+\bar b(p\cdot w)]\,(v_j\cdot w)$ exactly on the polygon.
Along a nonzero tangent direction perpendicular to $P_mp$, its first
factor is constant and the product is affine; some boundary endpoint
is no smaller than any interior point. If $P_mp=0$, choose any tangent
direction. On each edge check both endpoints and its admitted concave
quadratic stationary point, retaining negative maxima and degeneracies.
Nonnegative Bernstein weights give a uniform upper loss $U$, including
(12). Equations (5),(11) then require the concave polynomial
$$
(\gamma-H_\mu-B_\mu-U)+2\tau_+x
                       +(-\gamma-H_\mu-B_\mu)x^2\le0.             \tag{16}
$$
Its quadratic coefficient is nonpositive regardless of the sign of $U$,
since $\gamma\ge-H_\mu$. The fixed covers give:

| interval | closed source leaves | empty | strict support leaves | negative uniform losses |
|---|---|---|---|---|
| $I_0$ | 26 | 4 | 22 | 11 |
| $I_1$ | 28 | 4 | 24 | 13 |

Both endpoint margins at **every** strict leaf exceed $1/100000$.
Witnesses are originals or previously verified convex points in $K$.
All prefix-free trees, both source charts, polygon corners and support
values are replayed. This closes both intervals (8), including their
common endpoint, and hence the complete signed remote-roll cover on $L$.

## 4. Spatial-angle gates, original contacts and equality

On $[0,1/10]$, use (7) at original zero-height $V_{45}$: probe3 for
negative roll, probe4 for positive roll. For $q=-P$ the leading
coefficient is positive, $q(0)>0$, $q(1/10)<0$, and the larger root
is beyond $1/10$. Exact signs at the first outward millionth and its
predecessor give:

| piece | negative/positive small-root uppers | roll chord upper | $\beta$ | full spatial angle upper $\theta$ | $R(1-\theta^2/8)-\theta/2$, $R=1/8$ |
|---|---|---|---|---|---|
| $L$ | $14483/500000,\ 5671/500000$ | $14483/250000$ | $201/200$ | $198921/1000000$ | $1594958435759/64000000000000>0$ |
| $B$ | $8089/500000,\ 5747/500000$ | $8089/250000$ | $1007/1000$ | $222413/1000000$ | $833316457431/64000000000000>0$ |

The perpendicular-axis quaternion bridge in the
[rank-transport proof](rank_transport_wedge_proof.md) and
[six-rupert-3's composition proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
graph7414, applies to the **actual** factors (4). Each
$X^2=(a+d)^2+\text{roll}^2\le1/9$, its product gate exceeds
$(99/100)^2$, $99/100-ad/4>0$, and $\beta^2(1-X^2/4)>1$.
These give the displayed full principal angle and strict actual Cayley
norm $\tan(\theta(Q')/2)<1/8$. No other body's motion constants are used.

Freshly reconstruct the original 20-corner shadow on each triangle.
Its cross sum is $C_8$; 40 endpoint contacts reduce to 20 distinct
polynomial rows. Each case checks 7440 original support comparisons,
60 Cayley displacement identities, nine Gram identities and a determinant
identity. The six signed cube-face covers have leaf counts
$$
L:(4,25,7,4,4,4),\qquad B:(4,13,4,7,4,4):
$$
84 leaves and 3276 strict linear/Bernstein coefficients. Maximum depth
is four on $L$, three on $B$; inherited guards are unchanged.

The local mechanism in [cell8_collar_proof.md](cell8_collar_proof.md),
graph8186, applies with these **fresh** contacts and covers at radius
$1/8$. For an original endpoint $v$ and receiving support covector $\mu$,
necessary Cayley containment requires
$$
(v\times\mu)\cdot w+(v\cdot w)(\mu\cdot w)
                         -(\mu\cdot v)\|w\|^2\le0.                \tag{17}
$$
The positive linear and radius-adjusted quadratic Bernstein bounds,
certified axis-norm lower, receiver affinity and radial interpolation
make some contact strictly positive for every $0<\|w\|\le1/8$,
contradicting containment. Thus the actual Cayley vector is zero and
$Q'=I$. Undoing the right $h$ and left $J_n$ gives the left cosets in
(2). Conversely they give equal shadows; positive shadow area forces
$\lambda=1$, and bounded-shadow support functions force $t=0$.

The inherited exact minimum squared Frobenius distance of $J_m$ from
$G$ is $(106-36s)/29>8\max(d_L,d_B)^2$. Since
$\|J_n-J_m\|_F^2\le8\|n-m\|^2$, $J_n\notin G$ on both triangles,
so all 120 equality rotations are distinct. Proper-body conjugation
and $P_{-n}=P_n$ give every stated image.

The interior witness $(N_8+W+9Z_{1/4})/11$ has 60 projective body images
outside all 13 older triangular cones, including the complete one-fifth
collar and Cell9, by 780 exact Cramer tests with both projective signs.
Its chord from every one of the 30 projective minimum axes exceeds
$1/50>1/64$, also excluding the old caps. Thus the combined excluded
receiving domain strictly grows; no spherical area ratio is asserted.

## 5. Reproduction, dependencies and trust

From the repository root, Python3.11+ and its standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell8_quarter_certificate.py
~~~

The [fixed checker](cell8_quarter_certificate.py) must match **every**
field of [expected_cell8_quarter.json](expected_cell8_quarter.json),
88719 bytes, SHA256
401920a61c7a32a3145400955ecd7dd49c11dc251977f86a8d7e7aa1cacc6268.
Expected: 214 candidates and 56 feasible in each case, 84 axis leaves,
3276 strict coefficients, both displayed angles, and 26 malformed-evidence
rejections. Python -O is refused before mathematical imports. All
54 new polygon/support records and both source-critical, physical-area
and receiver fields match private discovery exactly.

Thirty inherited code/fixture files are byte-pinned, including the
whole fifth-collar source and fixture. Its older result is an author-checked
prerequisite, not independently rerun here. Every new budget, original
receiving contact, source tree and roll cover is freshly reconstructed.
Executed main-phase field signs have independent rational enclosure audits;
radical zero signs use exact identities. Imported constructors retain their
inherited trust scope. The signed-height identity has 162 exact Rodrigues
regressions, with 36 fresh roll-Bernstein component identities and inherited
clipping/negative-gain controls. These supplement the written universal
algebra and are not formalization.

Trust includes Python/Fraction, exact field/radical kernels, pinned
original geometry, and the written convexity, critical-stratum,
proper-gauge, transport, closed-cover, root, quaternion and Cayley bridges.
No floating sample, failed search, resource kill, timeout, solver UNKNOWN,
or incomplete enumeration is a proof premise.

Complementary work read includes
[six-rupert-2's J77 inverse-area collar reduction](../../convex_geometry/rupert_j77_inverse_area_collar/PROOF.md),
substantive source 00fdeef9b4bab9d70b0f8077ace529d676346caa,
reader-link repair 6345acdb4574fe0100230e6c04235892f4cfb13d, graph8248.
It derives all-original-source conditions without claiming passage exclusion
on its collar. Also read
[six-rupert-3's RID receiving-gap proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CAYLEY_PROOF.md),
source 411ae5ebba4c5c426650c491ed48742ebeff0231, graph8228,
with necessary strict-passage condition $f(n)<21/50$ and receiving gap
at least $1/31$; the
[complete J77 mirror cap](../../convex_geometry/rupert_j77_complete_signed_mirror_cap/PROOF.md),
graph8206; and the
[RID winning receiver theorem](../../rhombicosidodecahedron_mirror_cluster_obstruction/WINNING_CAYLEY_PROOF.md),
graph8172. Their body-specific constants, translation arguments and review
statuses are not transferred to the deltoidal body.

Primary status refreshed2026-10-01:
[Gosain--Grimmer](https://arxiv.org/html/2509.08190),
[Zeng](https://arxiv.org/html/2604.26531),
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475), and the
[standard strict-projection framework](https://arxiv.org/abs/2112.13754).
The located primary tables retain the deltoidal and pentagonal
hexecontahedra as unresolved Catalan cases. The rhombicosidodecahedron
non-Rupert statement is a conjecture; the Noperthedron theorem concerns
another body. This bounded refresh is not exhaustive historical-priority
evidence. The global deltoidal Rupert problem remains open.
