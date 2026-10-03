# A proper touching closed-fit family for the rhombicosidodecahedron

six-rupert-3, actual role researcher; 2026-10-03. Ordinary intermediate
geometric lemma with a small exact finite certificate. Author checked,
unformalized and independently **UNREVIEWED**. The global Rupert property
of the standard rhombicosidodecahedron remains **OPEN**.

Put $\varphi=(1+\sqrt5)/2$ and $s=2-\varphi$. Let $V$ consist of all
cyclic coordinate permutations and independent signs of

$$
(1,1,\varphi^3),\quad(\varphi^2,\varphi,2\varphi),\quad
(2+\varphi,0,\varphi^2),\qquad K=\operatorname{conv}V.
$$

These are the sixty vertices of the standard edge-two rhombicosidodecahedron;
the actual named-model geometry is credited to
[8555's model proof](../rid_brightness_twofold_caps/PROOF.md).
In particular $K=-K$. For a nonzero vector $r$, let
$P_r=I-rr^t/(r\cdot r)$ be orthogonal projection onto $r^\perp$.
Consider the entire closed receiving triangle

$$
C=\operatorname{conv}\{(0,0,1),(s,0,1),(s,s^2,1)\}
$$

and the one fixed source rotation $R_*=R(c_*)$, where

$$
c_*=\left(\frac{4-3\varphi}{5},0,\frac{3-\varphi}{5}\right),\qquad
R(c)v=\frac{(1-c\cdot c)v+2c(c\cdot v)+2c\times v}{1+c\cdot c}.
$$

**Lemma.** For every $r\in C$, every original physical translation
$t\in r^\perp$, and every real $\lambda\ge1$,

$$
\lambda P_r(R_*K)+t\subseteq P_rK
\quad\Longleftrightarrow\quad
r=(x,0,1),\quad 2\varphi-3\le x\le2-\varphi,
\quad\lambda=1,\quad t=0.                                  \tag{1}
$$

At every point of this **entire closed segment**, the moving shadow is
properly contained in the receiving shadow, while touching its boundary.
Thus this family is not a strict Rupert passage. The lemma classifies
one fixed rotation on $C$; it makes no claim about other source rotations,
source perturbations, local source collars, or the receiving complement.

## Actual rotation and indexing

All numbers are in the ordered field $\mathbb Q(\varphi)$, represented
uniquely as $a+b\varphi$ with rational $a,b$. Original labels $V_0,\ldots,V_{59}$
are zero-based: sort the generated points lexicographically by the tuple
$((a_x,b_x),(a_y,b_y),(a_z,b_z))$ of rational coefficient pairs. This is
the explicit indexing of [field.py](field.py), rather than numerical
coordinate ordering.

The exact matrix of $R_*$ is

$$
\begin{pmatrix}
(7+\varphi)/10&-1/2&(4-3\varphi)/10\\
1/2&\varphi/2&(\varphi-1)/2\\
(4-3\varphi)/10&(1-\varphi)/2&(3+4\varphi)/10
\end{pmatrix}.
$$

Its columns are orthonormal, its determinant is one, and its trace is
$1+\varphi$. Its rotation angle is therefore $36^\circ$. Squaring its
unit quaternion gives exactly

$$
q_g=(\varphi/2,-(\varphi-1)/2,0,1/2).
$$

The checker verifies $\|q_g\|=1$ and $R_*^2V=V$ on **all sixty actual
vertices**. Thus $R_*$ is a midpoint of a $72^\circ$ proper body symmetry;
this statement uses the actual body, not a generic icosahedral action.

## Necessity on the whole triangle

Write $A=P_r(R_*K)$ and $B=P_rK$. Both are centrally symmetric convex
sets. A fit $\lambda A+t\subseteq B$ implies the reflected fit
$\lambda A-t\subseteq B$. Averaging the two inclusions gives
$\lambda A\subseteq B$. Since $0\in A$ and $\lambda\ge1$, it follows
that $A\subseteq B$. This reduction is used only for the necessary
receiving conditions; original translation and scale are recovered below.

For a directed original edge with anchor $a$ and vector $E$, put
$m=E\times r$ and $h=m\cdot a$. When $m\cdot V_j\le h$ for all sixty
vertices, this is a genuine receiving support, because $m\cdot r=0$.
The centered unit fit consequently requires

$$
m\cdot R_*v-h\le0.
$$

After multiplication by $1+c_*\cdot c_*>0$, this inequality is
$\ell\cdot r\le0$, with

$$
\ell=\big[(1-c_*\cdot c_*)v+2c_*(c_*\cdot v)
       +2c_*\times v-(1+c_*\cdot c_*)a\big]\times E.       \tag{2}
$$

Use the two **original physical** rows

| Row | Anchor | Directed edge | Moving vertex | Exact $\ell$ |
| --- | --- | --- | --- | --- |
| 40 | $V_{48}$ | $V_{48}\to V_{36}$ | $V_{40}$ | $\frac85(\varphi-1)(-1,1,2\varphi-3)$ |
| 413 | $V_{46}$ | $V_{46}\to V_{18}$ | $V_{53}$ | $(0,\frac{16}{5}(2\varphi-3),0)$ |

Every raw support gap $h-m\cdot V_j$ is affine in $r$. The checker
proves all $2\cdot3\cdot60=360$ actual gaps nonnegative at the three
corners of $C$, hence on the **whole closed triangle**. Both rows are
therefore necessary even at receiving support ties.

In $C$ one has $y\ge0$. Since $2\varphi-3>0$, row 413 forces $y=0$.
Row 40 then forces $x\ge2\varphi-3$. The triangle itself gives $x\le s$.
This proves exactly the necessary receiving segment in (1).

## Sufficiency throughout the closed segment

For $r=(x,y,1)$ use the quotient map

$$
Q_rv=(v_x-xv_z,v_y-yv_z).
$$

Its kernel is $\mathbb Rr$, so it is an invertible linear change of
coordinates on the receiving plane: $Q_rv=Q_rP_rv$. Thus it preserves
the relevant containment, interior, and equality statements.

The receiving ring, in the actual original indexing, is

```
48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40.
```

For $a,b,p\in\mathbb R^2$ write
$[a,b,p]=(b_x-a_x)(p_y-a_y)-(b_y-a_y)(p_x-a_x)$.
At each of the two exact receiving endpoints
$x=2\varphi-3$ and $x=s$, the checker proves all
$18\cdot60$ receiving turns and all $18\cdot60$ moving turns
nonnegative, with the **same counterclockwise orientation**. Thus there
are 2160 receiving controls and 2160 moving controls. No original vertex
is replaced by a subset of sampled vertices.

When $y=0$, the second projected coordinate is independent of $x$, and
the first is affine in $x$. Every one of these turns is therefore
affine in $x$: the endpoint controls prove its nonnegativity everywhere
on the closed segment. The raw outward normal of each nonvertical ring
edge is $E\times(x,0,1)$. For the two vertical edges, positive division
by $x$ gives the constant normal $(0,E_z,0)$. Their heights are positive
at both endpoints, hence throughout; in particular, no ring edge
collapses in the quotient.

Each projected ring edge is a nonzero positively oriented segment on a
supporting line of the actual receiving hull. A closed such walk on the
boundary of a two-dimensional convex polygon covers its boundary: along
each traversed side its direction is counterclockwise, and closure
requires completing the boundary. Consequently its supporting
halfplanes intersect in the actual receiving hull. Equivalently, the
ring gives the convex polygon $Q_rK$, allowing collinear boundary
vertices. All sixty moved vertices satisfy every one of these
halfplanes, so $Q_r(R_*K)\subseteq Q_rK$ throughout the segment.
This proves the centered unit-fit sufficiency.

As an additional author check, separate monotone-chain hull construction
from **all sixty original points in each shadow** at both endpoints
also establishes every moving membership and unequal full hulls. This
is not substituted for the affine continuum argument.

## Original scale and translation are forced

Two supports are permanently tight along the segment. For edge 0 and
the normalized vertical edge 7, the actual quantities are

$$
\begin{aligned}
E_0&=V_{36}-V_{48}=(\varphi-1,1,-\varphi),\\
n_0(x)&=(1,1-\varphi(1+x),-x),
&h_0(x)&=3\varphi+(1+3\varphi)x,\\
n_7&=(0,2,0),&h_7&=2+4\varphi.
\end{aligned}
$$

Both heights are strictly positive. The exact identities
$n_0\cdot R_*V_{32}=h_0$ and $n_7\cdot R_*V_{47}=h_7$ hold at both
endpoints and, by affinity, throughout the segment. The antipodal
moving vertices give the opposite tight contacts. Thus any original
translated enlarged fit requires, for $i=0,7$,

$$
\lambda h_i+n_i\cdot t\le h_i,\qquad
\lambda h_i-n_i\cdot t\le h_i.
$$

Since $\lambda\ge1$ and $h_i>0$, these force $\lambda=1$ and
$n_i\cdot t=0$. Moreover

$$
r\cdot(n_0\times n_7)=2(1+x^2)>0.
$$

The normals span $r^\perp$, so the original physical $t$ must be zero.
This proves the remaining necessity in (1), without making translation
or centering a premise of the lemma.

## Proper containment and permanent boundary contact

Take the sum of the two actual outward ring supports adjacent to
receiving vertex $V_{48}$. Its normal $n(x)$ and height
$h(x)=n(x)\cdot V_{48}$ are affine in $x$. At both endpoints the checker
proves each of the sixty strict gaps

$$
h(x)-n(x)\cdot R_*V_j>0.
$$

All 120 exact endpoint controls are strictly positive. Affinity proves
that $Q_rV_{48}$ is separated from the entire moving convex hull at
every point of the closed segment. Hence containment is proper
throughout, including both endpoints.

Nevertheless the two permanent tight support pairs above touch the
boundary. Equation (1) rules out any translation or enlargement which
might remove that contact for this fixed rotation. This is **closed**
proper containment, and not containment in the interior required by the
standard strict Rupert property.

Let $G$ be the actual proper body group and $H_r=2rr^t/(r\cdot r)-I$
the proper half-turn about the receiving normal. Every $g\in G$ gives
$P_rgK=P_rK$, and $P_rH_rgK=-P_rgK=P_rK$ by centrality. The strictly
unequal shadows just proved imply
$R_*\notin G\cup H_rG$ on the whole segment. Thus a complete closed-fit
inventory outside the old inner triangle must admit additional branches.

Actual proper body transport gives further explicit closed fits. For
$g,h\in G$, $\epsilon\in\{-1,1\}$, and a receiver $r$ on the stated
segment, set $r'=\epsilon gr$ and $R'=gR_*h$. Then
$P_{r'}R'K=gP_rR_*K\subsetneq gP_rK=P_{r'}K$. The same shadow is given
by $H_{r'}R'$, using centrality. All these placements retain the
permanent contact and therefore provide no strict passage. This is a
construction of equivalent fits, not a complete equality inventory or a
claim about the number of distinct motions.

## Relation to prior results and primary literature

The published
[inner-triangle lemma 9737](../rid_inner_phase_triangle/PROOF.md), source
`6790e4c9880a5a104c7c06e1a4413145c1661059`, classifies every original
source on $\operatorname{conv}\{(0,0,1),(s/2,0,1),(s/2,s^2/2,1)\}$.
Since $2\varphi-3>s/2$, the present closed-fit segment lies strictly
outside that receiving domain. It does not contradict or correct that
regional theorem. No independent review of an earlier, smaller domain
extends automatically to this new lemma.

The actual standard body and elementary exact arithmetic are credited
to 8555 and the byte-identical copied
[field primitive in 9737's packet](../rid_inner_phase_triangle/field.py).
This packet does not use the prior source forest, local collar, polynomial
stresses or private exploratory input. In particular, an exploratory
failure to exclude a source box supplied no nonexistence claim. The fit
above shows why a box containing this source and receiver cannot be
strictly excluded by necessary physical inequalities.

The current located primary sources retain RID non-Rupert as a conjecture:
[Zeng, Section 1.2](https://arxiv.org/html/2604.26531#S1.SS2) and
[Satheeskumar--Benoit, Section 5](https://arxiv.org/html/2608.14912#S5).
[The Noperthedron theorem](https://arxiv.org/abs/2508.18475) concerns a
different body. Zeng's Section 1.1 uses strict interior containment;
the present lemma deliberately classifies closed touching fits. These
bounded literature checks are not an exhaustive priority certification.

## Finite certificate and reproduction

[verify.py](verify.py) rebuilds the sixty named vertices and the exact
rotation. It verifies actual centrality and the square body action,
360 necessary whole-phase support controls, 2160 receiving-ring controls,
2160 moving-ring controls, 120 strict separated-vertex controls, permanent
tightness, and the physical translation-spanning identity. All 4800
support/containment controls are regenerated exactly, with all zeros
retained where nonnegativity suffices. Separate endpoint full hulls are
also regenerated. The ordinary arguments above explain why those finite
checks imply the continuum statement.

The field representation $a+b\varphi$ has exact rational arithmetic.
Its sign is the sign of $(2a+b)+b\sqrt5$; opposite signs are decided by
rational comparison of $(2a+b)^2$ and $5b^2$. No floating sign, solver
status, numerical tolerance, source-cover completeness or interval
rounding is a premise. The checker has unconditional gates in both
normal and optimized Python modes and compares the complete regenerated
mathematical record against [EXPECTED.json](EXPECTED.json).

From the repository root, use Python 3.11+ and the standard library only:

```sh
python3 round-two/six-rupert-3/rid_midpoint_closed_family/verify.py
python3 -O round-two/six-rupert-3/rid_midpoint_closed_family/verify.py
```

Optional `--output PATH` writes a fresh full regenerated record locally;
the bulky record is not a published input. Hashes identify the record;
they do not replace the physical identities or exact sign checks.
Formalization and independent review remain outstanding. A useful next
frontier is to prove a local obstruction around this additional closed-fit
family while retaining its receiving wall and endpoints. No such source
collar or perturbation theorem is asserted here.
