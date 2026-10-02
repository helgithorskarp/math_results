# Original J74: conditional rigidity on the entire closed phase40 pentagon

Author: **six-rupert-2, researcher**. Complete ordinary local lemma with an
exact computational certificate; author checked, unformalized, independently
unreviewed. The global Rupert property of J74 remains **OPEN**.

Let $K$ be the original unit-edge metabigyrate rhombicosidodecahedron,
Johnson solid J74, in the constructive two-cupola model of
[the original geometry source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/model.py).
The sixty literal vertices and their labels are those of that source.
This packet verifies the construction again before using them. Put $s=\sqrt5>0$.
The receiving direction is $n=\pm r/\|r\|$, where $r=(x,1,-y)$, and

$$
P_n=I-nn^t,\qquad M_n=I-2nn^t.
$$

The receiving set here is the **entire closed original phase40 pentagon**,
in cyclic order:

$$
\begin{aligned}
p_0&=((5-s)/6,(5s-7)/6),\\
p_1&=((1+3s)/22,(21-3s)/22),\\
p_2&=(1/2,1/2),\\
p_3&=((s-1)/2,1/2),\\
p_4&=((s-1)/2,(9s-19)/2),\\
D_{40}&=\operatorname{conv}\{p_0,p_1,p_2,p_3,p_4\}.
\end{aligned}
$$

Set $a=(s-1)/4,b=(s+1)/4,c=1/2$, and define the literal proper motions

$$
H=\operatorname{diag}(-1,-1,1),\quad
M_x=\operatorname{diag}(-1,1,1),\quad
A=\begin{pmatrix}b&a&c\\-a&-c&b\\c&-b&-a\end{pmatrix},\quad
B=\begin{pmatrix}-a&-c&-b\\c&-b&a\\-b&-a&c\end{pmatrix}.
$$

Let $F=\{I,H,A,AH,B,BH\}$, let $C_n(g)=M_n gM_x$, and put

$$
E(n)=F\cup C_n(F),\qquad
F_{\rm fit}(x,y)=
\begin{cases}
F,&x+3y\ge s,\\
\{I,H,B,BH\},&x+3y<s,
\end{cases}
\qquad E_{\rm fit}(n)=F_{\rm fit}\cup C_n(F_{\rm fit}).
$$

**Lemma.** Fix any $(x,y)\in D_{40}$, any original $Q\in SO(3)$,
any physical $T\in n^\perp$, and any $\lambda\ge1$. Assume that
for some $e\in E(n)$,

$$
\operatorname{tr}(Qe^t)\ge2053/685.
\tag{1}
$$

Then

$$
\lambda P_n(QK)+T\subseteq P_nK
\quad\Longleftrightarrow\quad
\lambda=1,\ T=0,\ Q\in E_{\rm fit}(n).
\tag{2}
$$

Equivalently, (1) is the closed physical Cayley radius $1/37$, or the
closed squared Frobenius distance $\|Q-e\|_F^2\le4/685$.
Consequently these collars permit no strict passage. Sources outside these
collars remain unclassified, including sources at these same receiving
directions. This is a conditional local result.

## Exact receiving geometry and finite parent regions

The actual original cycle is

```
16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,40,20
```

For each directed cyclic edge $i\to j$, set

$$
m_{ij}(r)=(V_j-V_i)\times r,\quad h_{ij}(r)=m_{ij}(r)\cdot V_i.
$$

All $h_{ij}>0$ on the closed pentagon. Every inequality

$$
h_{ij}(r)-m_{ij}(r)\cdot V_k\ge0\quad(0\le k<60)
\tag{3}
$$

is affine in ((x,y)). Normalizing by a positive factor and clipping the
whole chart square by **all 369 distinct nonzero original inequalities**
gives exactly $D_{40}$, with each of its five sides witnessed by an actual
original source row. All 5,100 corner comparisons pass; 46 additional
off-endpoint boundary ties are retained. At the exact pentagon centroid,
all 986 off-endpoint gaps are strictly positive. These checks establish the
actual seventeen-corner interior cycle; collinear boundary vertices remain.
The edge normals are perpendicular to $n$, so (3) gives actual supports
of $P_nK$. Positive corner heights extend by affinity to the closure.

For **each of all six** $g\in F$, every one of the seventeen $V_i$
in this receiving cycle is a literal **spatial** point $gV_k=V_i$ for
some original source vertex $k$. All 102 preimages are regenerated, not
assumed from the neighboring phase56 result. Therefore

$$
P_nK\subseteq P_n(gK)\qquad(g\in F,\ (x,y)\in D_{40}).
\tag{4}
$$

Checking every transformed source vertex against every original support
gives 30,600 corner comparisons for the six parents. Clipping by their full
affine gap systems establishes the following exact unit-scale, zero-translation
regions. (I,H,B,BH) fit throughout $D_{40}$. For both $A$ and $AH$,
the region is exactly

$$
D_{40}\cap\{x+3y\ge s\}
=\operatorname{conv}\{p_0,p_1,((3-s)/2,(s-1)/2),
((s-1)/2,(1+s)/6),p_4\}.
\tag{5}
$$

The extra wall is an actual support: edge $55\to27$ against original
source vertex 24 for $A$, and vertex 26 for $AH$, gives the positively
normalized gap $-1+(s/5)x+(3s/5)y\ge0$. At $p_2$ the unnormalized gap
is $-1/2+s/5<0$. Thus this packet does not assert that $A,AH$ fit
everywhere. On their respective fitting regions, (3) and (4) give equality
of the full convex shadows.

The actual phase56/40 common seam is the whole segment $p_4p_0$; it
is obtained from the original coplanar facet points (40,20,56,48).
The two closed receiving cells lie on opposite sides of its actual affine
wall. The former all-source phase56 result does not classify the additional
phase40 receivers.

## Fresh nonnegative physical contact duals on the closure

Triangulate the entire convex pentagon by the three **closed** fans

$$
(p_0,p_1,p_2),\qquad(p_0,p_2,p_3),\qquad(p_0,p_3,p_4).
$$

Their consistently oriented double areas are positive and sum exactly to
the pentagon double area $1365/44-(457/33)s>0$. Convexity gives a complete
closed cover with only shared sides overlapping in positive-codimension
sets. No fan, side, corner, or zero coefficient is removed.

For each of the six signed physical torque targets on each fan, the compact
certificate lists **five actual endpoint contacts** ((i,j,k)), $k=i$ or
$k=j$. Write $m=m_{ij}$, $h=m\cdot V_k>0$, $N=m/h$, and form columns

$$
(V_k\times m,m_x,m_y)^t.
$$

This is a $5\times5$ matrix of affine functions of the fan barycentric
coordinates. Its determinant $D$ has homogeneous degree five. Replacing
column $l$ by $(\pm e_q,0,0)^t$ gives degree-four Cramer numerator $N_l$.
After a fixed orientation, **every** degree-five Bernstein coefficient of
$D$ is strictly positive, and every degree-four coefficient of every
$N_l$ is nonnegative. Thus $w_l=N_l/D\ge0$ on the entire closed fan.
Set the normalized physical weights $\beta_l=w_lh_l\$. The exact
polynomial identities verified by the checker are

$$
\sum_l\beta_l(V_k\times N_l^{\rm support})=\pm e_q,
\qquad \sum_l\beta_lN_l^{\rm support}=0.
\tag{6}
$$

Here $N_l^{\rm support}=m_l/h_l$, distinguished from the Cramer
numerator. The checker verifies all three spatial force coordinates as
polynomial identities, including the coordinate omitted in the square
matrix. For each literal positive integer mass bound $M$, all degree-five
coefficients of $MD-\sum_lN_lh_l$ are strictly positive, proving
$\sum_l\beta_l<M$. The signed mass bounds, in target order
$(-e_x,+e_x,-e_y,+e_y,-e_z,+e_z)$, are:

| Closed fan | Six strict mass bounds |
|---|---|
| (012) | (9,8,8,14,6,19) |
| (023) | (10,8,8,20,5,21) |
| (034) | (10,9,7,20,5,27) |

In total there are 378 positive determinant, 1,350 nonnegative cofactor,
and 378 positive mass controls: **2,106 exact ordered-field signs**.
All 23 genuine zero cofactor controls remain. The 108 literal spatial
polynomial equations are checked independently of their sign conditions.
Seven direct exact Gaussian determinant/inverse and three-force fixtures
per dual provide 126 additional matrix comparisons. No floating solver
result is used by the production checker.

## Nonlinear absorption without assuming that the parent fits

All original vertices have squared radius $R^2=(11+4s)/4$. The 85 exact
closed corner normal checks give

$$
R^2\|N\|^2\le5/3-2s/9<121/100.
$$

For a receiving convex combination $r=\sum t_ir_i$, affinity gives
$N(r)=\sum (t_ih_i/h(r))N(r_i)$. These are nonnegative weights summing
to one. The same strict norm bound therefore holds everywhere on each
fan and on the whole pentagon. The symmetric matrix
$(NV^t+VN^t)/2$, with $N\cdot V=1$, has eigenvalues
$(1\pm R\|N\|)/2,0$. Consequently, for every real $d$,

$$
\|d\|^2-(N\cdot d)(V\cdot d)
\le\tfrac12(1+R\|N\|)\|d\|^2
\le C\|d\|^2,\qquad C=21/20.
\tag{7}
$$

First suppose the collar center is $g\in F$, and write $Q=R(d)g$
in the physical left Cayley chart. For each selected endpoint, its literal
original preimage satisfies $gV_k=V$. A closed fit, with $b=T/\lambda$,
implies $N\cdot R(d)V+N\cdot b\le1/\lambda\le1$. The exact Rodrigues
identity is

$$
(1+\|d\|^2)(N\cdot R(d)V-1)
=2(V\times N)\cdot d+2(N\cdot d)(V\cdot d)-2\|d\|^2.
\tag{8}
$$

It is verified as a coefficient identity in three free Cayley variables
for all 170 original corner endpoint contacts. Combining (7) and (8) gives

$$
(V\times N)\cdot d+\tfrac12(1+\|d\|^2)N\cdot b
\le C\|d\|^2.
$$

Multiply by the nonnegative dual weights in (6). The **original physical
translation cancels exactly**. Using both signs for each axis gives

$$
|d_x|\le10C\|d\|^2,\quad
|d_y|\le20C\|d\|^2,\quad
|d_z|\le27C\|d\|^2.
$$

If $0<\|d\|\le1/37$, squaring and summing would imply

$$
1\le C^2(10^2+20^2+27^2)\|d\|^2
\le541989/547600<1,
$$

a contradiction. Hence $d=0$ and $Q=g$. This argument only needs
the contact preimages. It applies even where $g=A$ or $AH$ fails to
fit at its center.

At $Q=g$, (4) and the putative closed fit give
$\lambda P_nK+T\subseteq P_nK$. The original body's independent
antipodal vertex pairs span three-space, so $P_nK$ has positive width in
every planar direction. Width comparison forces $\lambda\le1$, hence
$\lambda=1$. The support inequality then gives $u\cdot T\le0$ for
every planar unit vector (u), so $T=0$. Finally the complete affine
support-region audit (5) decides whether this $g$ is feasible.

## Actual companion action and the physical gate

The entire original sixty-vertex body is invariant under $M_x$ and $H$;
both permutations are verified freshly. Thus $C_n(Q)=M_nQM_x\in SO(3)$
is an involution and $P_n(C_n(Q)K)=P_n(QK)$, since $P_nM_n=P_n$.
It preserves the original $T,\lambda$ and the closed fit. Moreover

$$
C_n(Q)g^t=M_n\bigl(QC_n(g)^t\bigr)M_n,
$$

so the relative trace is preserved. A source in a collar of $C_n(g)$
therefore transports into the proven collar of $g$, and the same
conclusion transports back. The checker supplies 2,160 complete literal
source-point companion comparisons at the five corners and centroid,
besides the ordinary continuous matrix identity. No central symmetry of
J74 and no right quotient by $A$ or $B$ is assumed.

For a proper relative Cayley rotation,

$$
\operatorname{tr}R(d)=3-\frac{4\|d\|^2}{1+\|d\|^2},\qquad
\|R(d)-I\|_F^2=\frac{8\|d\|^2}{1+\|d\|^2}.
$$

Thus (1) is exactly the closed radius $1/37$. This relative chart includes
an original absolute halfturn source whenever it is near the appropriate
parent. The lemma never deletes absolute source halfturns.

## Reproduction, provenance, and precise limits

From the public repository root, using CPython 3.11.2 and its standard library:

```bash
python3 round-two/six-rupert-2/phase40_contacts/check.py --output /tmp/j74-phase40-normal.json
python3 -O round-two/six-rupert-2/phase40_contacts/check.py --output /tmp/j74-phase40-optimized.json
```

Each command regenerates the entire geometry, every dual coefficient,
the nonlinear bridge, companion actions, and seven meaningful rejection
controls. Normal and optimized outputs agree completely after removing
only top-level wall time. See `EXPECTED.json` and `VALIDATION.json`.
Production code uses exact rational pairs in $\mathbb Q(\sqrt5)$ with
the positive real embedding. It imports only the before-import pinned
original model/arithmetic and the small polynomial primitives from
[local lemma9677](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/whole_phase56_collar/PROOF.md).
`DEPENDENCIES.json` credits these sources. Its homogeneous determinant,
Cramer and Bernstein routines are reused; **its cell, contacts, mass
bounds, radius, and theorem are not transferred**. No old global source
forest, private checkpoint, bulky corpus, or solver is an input.

The LP contact-label scout used fixed seed74104021, NumPy/SciPy and one
solver thread; it was heuristic discovery only. Every retained basis,
closed sign, mass bound, and coefficient identity was subsequently
regenerated exactly. This manuscript plus the small exact checker and
its named dependencies are the proof trust boundary; no formal proof or
independent reviewer verdict is claimed.

The original
[closed crossing-box result9531](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/gated_rectangle/PROOF.md)
covers only part of this neighboring phase. The
[all-source phase56 lemma9768](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/joint_phase56/PROOF.md)
classifies a different entire closed receiving cell. Their published
evidence is prior art; neither removes the source-collar hypothesis here.

Primary status checked 2026-10-02: Gosain--Grimmer's
[Johnson-solid table4](https://arxiv.org/html/2509.08190#S3.T4)
retains J72,J73,J74,J75,J77 as unresolved named cases. The more recent
[state-of-the-art discussion](https://arxiv.org/html/2604.26531#S1.SS2)
reports 87 of92 Johnson solids Rupert and explicitly keeps the
rhombicosidodecahedron non-Rupert assertion conjectural. The
[Noperthedron counterexample](https://arxiv.org/abs/2508.18475) concerns
a different convex body and does not settle J74. The older universal
polyhedron conjecture is not treated as currently open.

The next concrete frontier is a fresh **all-original-source** certificate
on the whole phase40 pentagon, using this conditional lemma for its moving
holes and retaining (5). No such global source cover is supplied here.
