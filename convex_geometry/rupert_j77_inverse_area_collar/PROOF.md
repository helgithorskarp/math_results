# Inverting the physical-area sublevel and reducing a new J77 collar

Author: **six-rupert-2**, role **researcher**, 2026-10-01. Complete
author-checked written intermediate proof, with exact finite hypotheses
checked by the accompanying source. This proof is **unformalized and
independently unreviewed**. Historical priority and sharpness are not
asserted. The global Rupert property of J77 remains **OPEN**. The new
collar below is not proved to exclude passage.

## 1. Original body and results

Let $s=\sqrt5>0$. Let $K=\operatorname{conv}V$ be the original
unit-edge, 55-vertex **paragyrate diminished rhombicosidodecahedron**,
Johnson solid J77, in the [pinned model](../rupert_j77_projection_diameter/model.py).
The 50-vertex antipodal core is denoted $V_c$; all five gyrated originals
are retained. $K$ is asymmetric. All originals have common radius

$$
 r=\sqrt{(11+4s)/4}<9/4,
 \qquad 0\in\operatorname{int}K.
$$

For unit $n$, write $P_n=I-nn^t$ and

$$
 A(n)=\operatorname{Area}(P_nK).
$$

This is physical Euclidean area in the actual projection plane. Set

$$
 e=(1,0,0),\quad a=(0,(1+s)/2,1),\quad c=(s-1)/4,
 \qquad Rv=cv+\frac{1-c}{a\cdot a}(a\cdot v)a+\tfrac12(a\times v).
$$

$R$ is the actual proper order-five body rotation, verified on all
originals by the parent. Let

$$
 \mathcal E=\{\pm R^j e:0\le j<5\},\quad
 A_0=\frac{49+25s}{8},\quad
 A_1^2=\frac{725}{8}+\frac{1621s}{40},\quad
 \rho^2=\frac{169}{32}+\frac{359s}{160}.
$$

All square roots, including $A_1,\rho$, use the positive branch.

**Global inverse-area theorem.** For every unit original source normal
$k$ and every $A_0\le T<A_1$, if $A(k)\le T$, then

$$
 \operatorname{dist}(k,\mathcal E)^2\le
 2\left(1-\frac{A_0T+\rho\sqrt{A_0^2+\rho^2-T^2}}{A_0^2+\rho^2}\right).       \tag{1}
$$

For every $0<\eta\le1/10$, a simpler corollary is

$$
 A(k)\le A_0+\eta\quad\Longrightarrow\quad
 \operatorname{dist}(k,\mathcal E)<\frac{7\eta}{20}.                         \tag{2}
$$

At zero excess, $k\in\mathcal E$. These are global conditional
statements; source nearness is derived. Formula (1) is a necessary bound,
and is not asserted sharp. Formula (2) increases the parent's certified
excess domain from $9/1000$ to $1/10$, and improves its factor
$5/14$ to $7/20$. It uses the same original geometric constants.

Define the closed raw triangle and its normalized receiving patch by

$$
 \begin{split}
 u_0&=(1,-1/450,1/900),\\
 u_1&=(1,-1/300,0),\\
 u_2&=(1,-1/225,1/450),\\
 B&=\operatorname{conv}\{u_0,u_1,u_2\},\qquad
 \mathcal B=\{u/\|u\|:u\in B\}.
 \end{split}                                                             \tag{3}
$$

The vertices are $e+d_0/300,e+d_1/300,e+d_0/150$, where the actual
closed receiving-sector23 rays are $d_0=(0,-2/3,1/3)$, $d_1=(0,-1,0)$.
The source recomputes supports directly, so its use of this label is
descriptive rather than a support premise.

**Closed-collar all-source reduction.** Every $n\in\mathcal B$ obeys

$$
 \frac1{500}<\operatorname{dist}(n,\mathcal E)=\|n-e\|<\frac1{200},
 \qquad
 A(n)^2\le\frac{280834381}{3240080}+\frac{31130667s}{810020}
       <(A_0+13/500)^2.                                                  \tag{4}
$$

The area maximum is attained exactly at the direction of $u_2$.
For **every original** $Q\in SO(3)$, arbitrary physical planar
translation $t$, and $\lambda\ge1$, closed containment

$$
 \lambda P_n(QK)+t\subseteq P_nK                                         \tag{5}
$$

necessarily gives $\lambda^2<501/500$ and an actual **right** body
factor $h=R^j$, $0\le j<5$, such that

$$
 \|(Qh)^tn-e\|<91/10000,
 \qquad \operatorname{angle}(Qh)<1/20.                                   \tag{6}
$$

After the minimal proper normal transports, the only surviving planar
family is the proper roll $T(x)$, with

$$
 |x|=|\tan(\phi/2)|<1/60.                                               \tag{7}
$$

The entire opposite directed source branch and all other rolls are
excluded by the fresh finite certificate. These are necessary conditions
on (5), not a classification of containment or a passage exclusion.
They also transport to all $\pm R^j\mathcal B$, by actual body
invariance and reversal of the receiving normal.

The complete patch (3) is disjoint from the following explicitly named
older receiving domains, including all their body/reflection/sign images:
the complete mirror caps of radius $1/1000$, the old diameter-axis
caps of radius $1/40$, and the largest old north and south receiving
triangles specified in Section 5. Throughout this new patch the core
height is below $9/800$, hence its square is below $1/12$; it is also
outside the old winning-region criteria that require height squared
strictly greater than $1/12$. No dominance statement about arbitrary
conditional local small-rotation theorems is intended.

## 2. Exact prerequisites and continuous geometric input

The direct mathematical parent is the
[original physical-area proof](../rupert_j77_projection_area/PROOF.md),
source **cd0088c8aa1e308657b17d759bc5600c7b8b2b34**, graph
**bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au**,
committed at 7801. The second direct source parent is the
[proper-frame and full-roll proof](../rupert_j77_area_axis_roll/PROOF.md),
source **86dcf1e10d0eddbc26fc8343b6df4fcc642d47c6**, graph
**bafkreifknnotrmemmzit7mming6alsh2ddarslrbxdff3qkpoeitbzknmm**,
committed at 7867. All14 direct files and all 21 distinct direct/transitive
files are byte-pinned. The entire old roll checker is replayed, including
its complete area prerequisite; every expected parent byte is compared.
The old $1/1000$ receiving and $9/1000$ source-budget bounds are
not applied outside their domains. Only the exact geometry and the
general proper-frame, support and balance mechanisms are reused.

Here are the geometric inputs established there and replayed here.
For all 52 original outward facet area vectors

$$
 b_F=\tfrac12\sum_{v_i\in\partial F}v_i\times v_{i+1},
 \qquad A(n)=\tfrac12\sum_F|b_F\cdot n|.                                 \tag{8}
$$

The factor $1/2$ in each formula is physical. The facet list is proved
complete by checking all 26235 original triples. The area zonotope
$Z=\sum_F[-b_F/2,b_F/2]$ is full dimensional, has support $A$, and
has 221 projective facet normals or 442 directed polar vertices. Its
minimum facet height is $A_0$, exactly at $\mathcal E$; all other
facet heights are at least $A_1$. Consequently the vertices of
$Z^\circ$ are the ten $m/A_0$, $m\in\mathcal E$, together with
vertices of norm at most $1/A_1$.

At each $m\in\mathcal E$, the nonzero signed generator sum is
$A_0m$. The zero-dot generators form a tangent zonotope of inradius
$\rho$. Absolute value dominates any signed linear term, so for
**all** unit $k=zm+w$, $w\perp m$,

$$
 A(k)\ge A_0z+\rho\|w\|=A_0z+\rho\sqrt{1-z^2}.                          \tag{9}
$$

No source area-fan signs, central symmetry of $K$, diameter hypothesis,
or roll assumption are needed in (9).

## 3. Exact inversion on the whole sublevel domain

Let $A(k)\le T<A_1$ with $k$ unit. By homogeneity, $k/T\in Z^\circ$.
Maximize $k\cdot p$ over the complete polar vertices. The maximum is
at least $k\cdot(k/T)=1/T$. A nonminimum vertex has value at most
$1/A_1<1/T$, so some **actual** minimum vertex $m/A_0$ satisfies

$$
 z=k\cdot m\ge A_0/T>0.                                                 \tag{10}
$$

Write $D=A_0^2+\rho^2$. The fresh exact identity is

$$
 D-A_1^2=1.                                                            \tag{11}
$$

Thus $T<\sqrt D$, all radicals in (1) are real and positive, and
$z\ge A_0/T>A_0/\sqrt D$. The function

$$
 f(z)=A_0z+\rho\sqrt{1-z^2}
$$

is strictly decreasing on $(A_0/\sqrt D,1]$: for interior $z$,
$f'(z)=A_0-\rho z/\sqrt{1-z^2}<0$, and continuity handles 1.
The descending-branch solution of $f(z)=T$ is

$$
 z_T=\frac{A_0T+\rho\sqrt{D-T^2}}D.                                     \tag{12}
$$

The branch and the unsquared equation can be checked directly. Put
$q=\sqrt{D-T^2}>0$ and $p=(\rho T-A_0q)/D$. Since $T\ge A_0>0$,
squaring the positive quantities gives $\rho T\ge A_0q$; hence
$p\ge0$. Expanding gives $z_T^2+p^2=1$ and
$A_0z_T+\rho p=T$, so $p=\sqrt{1-z_T^2}$ with the required sign.
Moreover $z_T>A_0/\sqrt D$. Indeed this is equivalent to
$\rho q>A_0(\sqrt D-T)$, with both sides positive. Divide its squared
version by $\sqrt D-T>0$. The remaining strict comparison is

$$
 \rho^2(\sqrt D+T)-A_0^2(\sqrt D-T)
 =DT-(A_0^2-\rho^2)\sqrt D
 \ge\sqrt D[A_0\sqrt D-A_0^2+\rho^2]>0,
$$

because $T\ge A_0$ and $\sqrt D>A_0$. Thus (12) has the required
branch, and at $T=A_0$ it gives $z_T=1$.

By (9), $f(z)\le A(k)\le T$. Since both $z,z_T$ lie on this
descending branch, $z\ge z_T$. Finally
$\|k-m\|^2=2(1-z)\le2(1-z_T)$, proving (1).
At $T=A_0$, (10) already gives $z=1$ and $k=m$.

No negative square root or extraneous solution is admitted.

## 4. A larger linear budget by two successive bounds

Suppose $0<\eta\le1/10$ and $A(k)\le A_0+\eta$. The checker proves

$$
 (A_0+1/10)^2<A_1^2,\quad
 A_0>(1-1/128)(A_0+1/10),\quad
 13<A_0<105/8,\quad \rho>16/5.                                         \tag{13}
$$

Apply (10), now with $T=A_0+\eta$. It gives
$\alpha:=\|k-m\|<1/8$. If $\alpha=0$, (2) is immediate.
Otherwise $z=1-\alpha^2/2$ and
$\|w\|=\alpha\sqrt{1-\alpha^2/4}$, so (9) gives

$$
 \eta\ge\alpha\left(\rho\sqrt{1-\alpha^2/4}-A_0\alpha/2\right).           \tag{14}
$$

The first two new rational gates are

$$
 (499/500)^2<1-1/256,\quad
 (16/5)(499/500)-105/128>7/3.
$$

All radical factors are positive, so (14) first yields
$\alpha<3\eta/7\le3/70$. The second pair of exact gates is

$$
 (999/1000)^2<1-(3/70)^2/4,\quad
 (16/5)(999/1000)-(105/8)(3/140)>20/7.
$$

Applying (14) again gives $\alpha<7\eta/20$, proving (2).
The closed maximum excess $1/10$ is included. No continuation of the
parent's smaller source domain is assumed.

## 5. Entire receiving triangle, area maximum and old-domain separation

Write $u=e+q\in B$. The first coordinate is1 everywhere, so all
normalization factors are strictly positive. The raw triangle is
nondegenerate. Its squared tangent norm has exact extrema

$$
 1/162000\le\|q\|^2\le1/40500.                                         \tag{15}
$$

For the lower bound, $q_0\cdot(q_i-q_0)\ge0$ at every corner.
Linearity then gives $q_0\cdot(q-q_0)\ge0$ throughout, and expanding
the squared norm proves its minimum at $q_0$. Convexity of squared
norm and all three corner comparisons prove the upper bound at $q_2$.
The physical chord is

$$
 \|u/\|u\|-e\|^2=2\left(1-\frac1{\sqrt{1+\|q\|^2}}\right).
$$

The checker verifies
$(1-1/(2\cdot500^2))^2(1+1/162000)>1$, with positive unsquared
factors. This gives the strict lower chord $1/500$. The physical chord
is smaller than $\|q\|$, and $1/40500<1/200^2$, giving the strict
upper chord. Every other projective mirror axis has
$|e\cdot R^j e|<81/100$. Thus its signed dot product with $n$ is
below $81/100+1/200$, whereas $n\cdot e>1-1/(2\cdot200^2)$.
The nearest signed axis is uniquely $e$, proving the first part of (4).
In particular the whole closed patch is outside the earlier
[complete mirror cap](../rupert_j77_complete_signed_mirror_cap/PROOF.md),
source 46410a3250dea5bb32ec5d3acaae4f1ca3bc906d, graph 8206.

Independently reconstruct all 52 original facets and their area vectors.
For their signs at the strict interior average of $u_0,u_1,u_2$, every
signed facet dot product is nonnegative at every raw corner. By affinity
the same signs hold on the entire closed triangle, including walls.
Consequently (8) yields

$$
 A(u/\|u\|)=\frac{C\cdot u}{\|u\|},\quad
 C=\left(A_0,-\frac{23}8-\frac{57s}{40},\frac34-\frac{3s}5\right),          \tag{16}
$$

with $C\cdot u>0$ throughout. A second calculation reconstructs the
actual 18-corner original shadow at the interior direction, with cyclic
original labels

    24,54,21,7,3,1,22,49,16,29,41,33,0,4,6,23,53,20.

Its physical area vector $\tfrac12\sum_iV_i\times V_{i+1}$ equals
$C$. All18 candidate edges support all 55 originals at all three raw
corners:2970 comparisons. The support covector
$(V_{i+1}-V_i)\times u$ is affine in raw $u$, so these are whole
closed-triangle support tests, rather than sampled normal tests.

To maximize the square of (16), include all three corners, every
feasible edge-stationary point, and every feasible interior-stationary
point. On an edge $u=a+td$, $0\le t\le1$, put
$a_0=C\cdot a,b_0=C\cdot d,N_0=a\cdot a,N_1=a\cdot d,N_2=d\cdot d$.
The positive numerator permits cancellation in the derivative; its zero
is determined by

$$
 (b_0N_0-a_0N_1)+(b_0N_1-a_0N_2)t=0.                                  \tag{17}
$$

If the coefficient of $t$ vanishes, the objective is constant when
the constant coefficient vanishes, and has no interior stationary point
otherwise. For a nonzero coefficient, admit the unique resulting $t$
only when $0<t<1$. In the two-dimensional interior of $u_x=1$, a
stationary point of $(C\cdot u)^2/(u\cdot u)$, with $C\cdot u>0$,
must be $u=C/C_x$. This follows by setting both tangent derivatives
to zero, then taking the dot product with $u$; here $C_x=A_0>0$.
Admit it only when all three exact barycentric coefficients are
nonnegative. Compactness and the derivative classification prove
completeness of this finite maximum list. The actual edge critical
points and the interior point are infeasible; the three corners remain.
Comparison gives exactly the maximum in (4), uniquely at $u_2$.
The final strict budget is checked by the exact field sign of its
difference from $(A_0+13/500)^2$.

For comparison with older domains, define
$f(n)=\min_{v\in V_c}|v\cdot n|$. The actual original core vertex23
has zero x coordinate. Hence everywhere on the new patch,

$$
 f(n)\le |V_{23}\cdot n|\le r\|q\|/\|u\|<9/800.                         \tag{18}
$$

Each function $|v\cdot n|$, and hence their finite minimum, is
$r$-Lipschitz. For $D=(0,-1,z)$, $z=(7+s)/2$, the checker directly
finds

$$
 f(D/\|D\|)^2=(65+10s)/596>(3/8)^2.
$$

In every closed chord-radius $1/40$ cap at a body/sign image of this
normal, $f(n)>3/8-(9/4)/40=51/160>9/800$. Thus (18) separates the
whole new patch from all the
[old diameter caps](../rupert_j77_balanced_torque_caps/PROOF.md).
It also fails the prerequisite $f(n)^2>1/12$ of the old winning-region
receiving criteria.

The largest old south and north raw triangles are respectively

$$
 \operatorname{conv}\{D,(0,-13/11,z),(1/10,-25/24,z)\},\qquad
 \operatorname{conv}\{D,(0,-17/20,z),(1/20,-17/20,z)\}.                    \tag{19}
$$

They are the [south triangle](../rupert_j77_zero_height_supports/PROOF.md)
and [north triangle](../rupert_j77_directional_north_triangle/PROOF.md).
For each of their20 $R^j$ and $X R^j$ images, $X=\operatorname{diag}(-1,1,1)$,
solve the three-column system expressing each new raw corner in the old
three rays. All determinants are nonzero. For every old cone there is
one coordinate strictly positive at all new corners and another strictly
negative at all new corners; the complete exact records are in expected.json.
Affinity extends these signs throughout the new triangle. The negative
coordinate excludes the old positive cone and the positive coordinate
excludes its reversed cone. Positive normalizations preserve this
separation. Thus the entire closed patch is outside both signs of all
the old triangles, including seams.

## 6. Area implication and arbitrary proper moving frames

Closed containment (5) gives

$$
 \lambda^2 A(Q^tn)\le A(n)<A_0+13/500.                                  \tag{20}
$$

Physical planar translation does not affect area. Since $A\ge A_0>13$,
$\lambda^2<1+(13/500)/A_0<501/500$. Apply the new global (2) with
$\eta=13/500<1/10$, giving

$$
 \operatorname{dist}(Q^tn,\mathcal E)<91/10000.                           \tag{21}
$$

Choose an actual signed source axis $\epsilon R^j e$ realizing this
bound and set $Q_g=QR^j$. This is a right factor because $R^jK=K$.
Then $k=Q_g^tn$ has $\alpha=\|k-\epsilon e\|<91/10000$.
Let $A_*$ be the minimal proper transport $e\mapsto n$, and $B_*$
the minimal proper transport $\epsilon e\mapsto k$. Define

$$
 F_3=A_*^tQ_gB_*,\qquad F_3e=\epsilon e,
 \qquad F=F_3|_{e^\perp}\in O(2),\quad\det F=\epsilon.                    \tag{22}
$$

These are actual proper three-dimensional source and receiving frames.
All their chords are below $1/100$, so the minimal transports are
unique. Their operator distances from identity are respectively
$\delta=\|n-e\|<1/200$ and $\alpha<91/10000$.

Put $S=P_eK$, $Y=P_eA_*^tK$, and
$X_*=FP_eB_*^tK$. Pair the same original vertices before and after
each proper transport. By the operator bound and convexity,

$$
 d_H(Y,S)\le r\delta,\qquad d_H(X_*,FS)\le r\alpha.                       \tag{23}
$$

Flatten (5), divide by $\lambda\ge1$, and retain its arbitrary
translation. Since $0\in Y$ and $Y$ is convex, $Y/\lambda\subseteq Y$.
Thus a necessary unit containment is $X_*+t'\subseteq Y$. Combining
(23) gives a necessary translated approximate containment

$$
 FS+t'\subseteq S+E B_2,
 \qquad E=\frac94\left(\frac1{200}+\frac{91}{10000}\right)=\frac{1269}{40000}. \tag{24}
$$

$B_2$ denotes the closed planar unit disk. Origin-interiority removes
scale only as a necessary reduction. Asymmetry is retained, and
translation has not been set to zero.

## 7. Fresh complete roll certificate at the new error

The actual minimum-axis shadow $S$ has ten corners, chosen from
originals 24,18,3,1,22,16,0,2,23,17. Recompute all its edges and their
outward unnormalized normals $m_i$, signed heights $H_i>0$, and
550 all-original support comparisons. Positive rational $U_i$ enclose
$\|m_i\|$ by exact squared inequalities.

For selected original projected source points $p_i$ and strictly
positive weights with $\sum_i w_im_i=0$, (24) requires

$$
 \sum_i w_i(m_i\cdot Fp_i-H_i)-E\sum_iw_iU_i\le0.                        \tag{25}
$$

Both components of translation cancel exactly. All weights are
reconstructed from the actual normal pairs/triples and normalized to
sum 1. The certificate uses edge sets $(0,5),(1,5,8),(1,4,7)$.
Each source witness is one of the original55 vertices.

For $x\in[-1,1]$, let

$$
 T(x)=\frac1{1+x^2}\begin{pmatrix}1-x^2&-2x\\2x&1-x^2\end{pmatrix},
 \qquad H=\operatorname{diag}(1,-1).
$$

The four families $T,-T,HT,-HT$, numbered 0,1,2,3, cover all of
$O(2)$, including every closed chart endpoint. In each, multiply (25)
by the positive $1+x^2$; this gives an exact quadratic. The fixed
closed roots and complete terminal midpoint paths are

| Family | Closed root | Terminal paths |
| --- | --- | --- |
|0|[-1,-1/20]|0,1|
|0|[1/20,1]|0,1|
|1|[-1,1]|00,01,100,101,11|
|2|[-1,1]|000,0010,0011,01,10,11|
|3|[-1,1]|00,01,10,11|

Every internal node has both closed children. The reader checks
prefix-free uniqueness, midpoint intervals and complete endpoint
coverage directly from [certificates.json](certificates.json).
There are 19 leaves,33 total nodes, maximum depth4. With the **new**
allowance $E=1269/40000$, all 57 quadratic Bernstein coefficients are
strictly above $1/1000$. The minimum is exactly

$$
 -\frac{10681465727}{524000000000}
 +\frac{10048770249s}{524000000000}>1/1000.                              \tag{26}
$$

On $[a,b]$, the coefficients are $f(a),f(a)+(b-a)f'(a)/2,f(b)$.
The nonnegative quadratic Bernstein basis sums to 1, proving strict
positivity at every point of each closed leaf. Quadratic identities
are additionally checked against the full matrices at three distinct
parameters; those identities do not substitute for the Bernstein
continuum argument. Consequently (25) excludes all determinant-minus-one
rolls and all remote proper rolls. Only family0 with $|x|<1/20$
survives, and (22) necessarily has $\epsilon=+1$.

The old18-leaf witness alone had one failed sufficient margin under
this larger allowance. Replacing that leaf by two freshly checked
closed children gives this complete19-leaf proof. The failed witness
is not mathematical evidence against passage.

For signed small rolls, the actual opposite normal pair 0,5 has weights
$(2/3,1/3)$, contact height $H_0=(11+5s)/6$, and norm budget
$N=769421/375000$. Actual source contacts are 24,16 for positive roll
and 18,0 for negative roll. Their signed torques are respectively
$L_+=8/3+s$ and $L_-=7/3+s$. Put $x=|\tan(\phi/2)|$. Each
necessary near-roll inequality is

$$
 g_\pm(x)=L_\pm x-2H_0x^2-EN(1+x^2)\le0.                               \tag{27}
$$

The fresh checker verifies $g_\pm(1/60)>0$ and $g_\pm(1/20)>0$.
Both quadratics are strictly concave. Hence they are positive on
the whole closed interval $[1/60,1/20]$, contradicting (27) there.
Together with the remote guard, this proves (7).

## 8. Full proper rotation and remaining frontier

The surviving $F_3$ fixes $e$ properly, with principal angle
$2\arctan|x|$. Since $Q_g=A_*F_3B_*^t$, the principal-angle
triangle inequality gives

$$
 \operatorname{angle}(Q_g)\le2\arcsin(\delta/2)
   +2\arcsin(\alpha/2)+2\arctan|x|.
$$

For chords below $1/100$, $\beta=1001/1000$ encloses the derivative
of $2\arcsin(q/2)$, because
$\beta^2(1-1/40000)>1$. Integrating and using $\arctan x\le x$
yields the freshly verified bound

$$
 \operatorname{angle}(Q_g)<\frac{1001}{1000}\frac{141}{10000}+\frac1{30}
       <\frac1{20}.                                                     \tag{28}
$$

This proves (6). For a receiving image $\pm R^\ell n$, reverse its
normal if necessary, conjugate the original proper placement by
$R^\ell$, apply the result, and conjugate back. The source right factor
remains in the actual $C_5$, and principal angle is invariant under
conjugation. Translation remains arbitrary in the proper image plane.

The next mathematical question is closed-containment rigidity on this
new patch using actual receiving contacts, signed motions and the
same-shadow companion. The present $1/20$ full-angle bound is a
proved entry condition; the older $15\delta$ statement is not assumed
on this patch. The continuous original-contact argument, persistent
receiving support strata, both reflected inequalities, their common
body gauge, and a positive directed inverse still need a new proof.
An exact passage certificate would also settle a useful part of the
assigned frontier. No absence-of-search inference is made.

## 9. Verification, trust boundary and literature

Reproduce using Python3.11+ and only its standard library:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B convex_geometry/rupert_j77_inverse_area_collar/verify.py --self-test
```

Repeat with `python3 -B -O` to check optimized execution. Explicit
exceptions guard every proof obligation; Python assertions are not used.
Both commands must match every byte of the compact expected.json.
Thirteen malformed new certificates are rejected, including incomplete
directed branches, missing closed children, false contacts, nonoriginal
sources and underestimated norms. The complete parent's controls also
run. Every registered $\mathbb Q(\sqrt5)$ sign, including parents, is
audited independently by rational enclosures for positive $\sqrt5$.

The trust boundary is the pinned original coordinate/cupola model,
the written Cauchy/polar/monotone-root/finite-maximum/moving-frame/
Hausdorff/translation-balance/Bernstein/concavity/angle bridges,
and Python exact integer/Fraction semantics. The continuous proof is
not formalized. No solver, float, sampled continuum, timeout, private
ledger, or omitted large corpus certifies a mathematical exclusion.
The old full diameter-region enumeration is not claimed rerun.

For the family/status context, the current primary sources consulted are
[the 2026 Rupert-family paper](https://arxiv.org/html/2604.26531) and
[the 2025 table containing the unresolved J77 entry](https://arxiv.org/html/2509.08190).
The assigned other seed, [the Noperthedron paper](https://arxiv.org/abs/2508.18475),
concerns a different non-Rupert polyhedron. This source does not transfer
that result to J77 or treat the rhombicosidodecahedron conjecture as a
proved non-Rupert result. The general physical-area strategy in
**six-rupert-1, researcher**'s
[Cell8 collar proof](../../geometry/rupert_deltoidal_symmetry/cell8_collar_proof.md),
source 4e2806a83f17c20fe755354a0b9b57f0bfef2e3a, graph 8186, is useful
context; its centrality and constants do not transfer to this body.
The subsequent
[complete one-fifth Cell8 collar](../../geometry/rupert_deltoidal_symmetry/cell8_fifth_proof.md),
source **08fe6643bf9eedf2f225b69eab0f25dff06f80c0**, graph **8238**,
was read during the preclaim refresh. Its fresh original-source budgets
and closed receiving partition reinforce the same methodological point;
its source charts, translation removal and numerical constants are not
used as J77 hypotheses.
No independent review or historical priority claim is inferred from
these citations.
