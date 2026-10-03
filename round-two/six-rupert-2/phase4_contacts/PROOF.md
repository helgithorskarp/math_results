# J74: ten-parent local rigidity and four proper closed corner fits

**six-rupert-2, researcher; 2026-10-03.** Ordinary conditional local proof
with exact finite checks. Author checked, unformalized, independently
unreviewed. The global Rupert property of the original J74 remains open.
The separate [joint proof](../joint_phase4/PROOF.md) must remove the local
source-entry premise; this local packet alone does not do so.

Let $s=\sqrt5>0$, $K=\operatorname{conv}(V_0,\ldots,V_{59})$ be the original
unit-edge metabigyrate rhombicosidodecahedron J74, and retain the constructive
two-nonopposite-cupola [model](../model.py), source
`25fc9695745b6832d068d18544452b7852b5847f`, graph8551. All original vertices
have $R^2=(11+4s)/4$. Three independent antipodal pairs place zero in the
interior; this does not assume central symmetry of the whole body.

The receiving chart is $r=(x,1,-y)$, $n=\pm r/\|r\|$, and the entire
closed triangle is

$$
 D_4=\operatorname{conv}\{p=(1/2,1/2),\quad
 q=((s-1)/2,(3-s)/2),\quad z=((s-1)/2,1/2)\}.
$$

Write $P_n=I-nn^t$, $M_n=I-2nn^t$, $a=(s-1)/4$, $b=(s+1)/4$, $c=1/2$,
and define literal matrices by rows:

```
H=diag(-1,-1,1),       Mx=diag(-1,1,1),
A=(( b, a, c),(-a,-c, b),( c,-b,-a)),
B=((-a,-c,-b),( c,-b, a),(-b,-a, c)),
G=(( a,-c,-b),(-c,-b, a),(-b, a,-c)).
F10={I,H,A,AH,B,BH,G,GH,HB,HBH}.
```

Every member of $F_{10}$ is proper. Only the actual full-body $H,M_x$
symmetries are used as body actions; this list is not a group and its other
members cannot be folded into arbitrary sources. Set $C_n(g)=M_ngM_x$,

$$
 E_{10}(n)=F_{10}\cup C_n(F_{10}),\qquad
 F_{\rm fit}(x,y)=\{I,H,B,BH\}\cup
 \begin{cases}\{G,GH,HB,HBH\},&(x,y)=q,\\\varnothing,&(x,y)\ne q,\end{cases}
$$

and $E_{\rm fit}=F_{\rm fit}\cup C_n(F_{\rm fit})$, understood as a set.
No assertion of twenty distinct branches is made.

**Conditional lemma.** For every $(x,y)\in D_4$, original $Q\in SO(3)$,
physical $T\in n^\perp$, and $\lambda\ge1$, assume

$$
 \operatorname{tr}(Qe^t)\ge2699/901\quad\text{for some }e\in E_{10}(n).
 \tag{1}
$$

Then $\lambda P_n(QK)+T\subseteq P_nK$ holds if and only if

$$
 \lambda=1,\qquad T=0,\qquad Q\in E_{\rm fit}(n).
 \tag{2}
$$

The gate is exactly the closed physical Cayley radius $1/30$, or squared
Frobenius distance $8/901$. Every such fit touches receiving supporting
lines. Four of the fits at $q$ have properly contained shadows. Proper
closed containment does not supply strict interior containment, and hence
does not supply a standard Rupert passage.

## The full original receiving cell and ten finite parent regions

The literal seventeen-corner interior cycle is

```
4,0,36,28,10,11,47,55,27,7,43,31,13,12,48,40,20
```

For successive original indices $i,j$, put

$$
 m_{ij}(r)=(V_j-V_i)\times r,\quad h_{ij}(r)=m_{ij}(r)\cdot V_i,
 \quad N_{ij}=m_{ij}/h_{ij}.
$$

[geometry.py](geometry.py) reconstructs the named original body before
checking all 3,060 corner support gaps against all sixty originals. Every
height is positive; 53 off-endpoint zero gaps are kept on the boundary.
All 986 off-endpoint gaps at the exact triangle centroid are positive.
Clipping by every one of the 361 distinct nonzero original affine support
inequalities gives exactly the triangle, double area $9/4-s>0$. Each of
its three sides has an original support witness, so no artificial clipping
square side restricts the cell. Positive heights and affine inequalities
extend these facts to the whole closure, including the common phase40 side

$$
 y=1/2,\qquad1/2\le x\le(s-1)/2.
$$

For all ten parents, every transformed original is checked at all three
corners: 30,600 comparisons. Full affine clipping establishes:

| Parents | Entire unit-scale, zero-translation fit region |
|---|---|
| (I,H,B,BH) | all $D_4$, equal shadows |
| (A,AH) | empty, including the boundary |
| (G,GH,HB,HBH) | exactly the singleton $q$ |

For (A,AH), original edge $55\to27$ against source24/26 has normalized
gap (-1+(s/5)x+(3s/5)y), strictly negative on the entire closed triangle.
For (G,GH,HB,HBH), original edge $4\to0$ against source15/9/12/10 has gap

$$
 a-by,
$$

whose values at $p,q,z$ are respectively ((s-3)/8,0,(s-3)/8). Thus it
strictly excludes every other point of the triangle. All other original
support gaps are nonnegative at $q$, proving that the four singleton
regions are exactly feasible.

Every receiving corner has a literal spatial source preimage for each of
the first six parents. For each additional parent the sole missing spatial
corner is $V_{20}$. Nevertheless, **every receiving support edge has at
least one endpoint with a literal spatial source preimage**, including both
edges adjoining20. This weaker property is what the proof uses below.

## The four additional closed fits really are different

[boundary_fit.py](boundary_fit.py) verifies $G=2vv^t-I$ for the unit axis

$$
 v=(-b,a,c),\qquad v\cdot v=1.
$$

Thus $G$ is an original absolute half-turn. A direct exact monotone hull
check uses the rank-two screen

$$
 V\mapsto(V_x-xV_y,V_z+yV_y),
$$

whose kernel is precisely $\mathbb Rr$. This is an invertible coordinate
map on $n^\perp$, so its convex containment is equivalent to orthogonal
projected containment. At $q$, each of the four additional sources has
a twelve-corner hull contained in the thirteen-corner receiving hull;

$$
 P_n(GK)=P_n(GHK)=P_n(HBK)=P_n(HBHK)\subsetneq P_nK.
 \tag{3}
$$

The checker verifies containment directly and verifies that projected
$V_{20}$ lies outside each source hull. It retains all boundary contacts.
The four motions are distinct; their $C_n$ companions duplicate members
of these four at this exact corner. Against every old parent and companion
from $F_6=\{I,H,A,AH,B,BH\}$, the maximum relative trace is

$$
 (1+s)/2<1261/421<3.
$$

Consequently the six-parent classification cannot hold on this new closed
triangle. This assertion concerns this new receiver, outside the previously
classified phase40 pentagon; it is no objection to that old regional theorem.

For the canonical source realization in the joint proof, the half-turn has

$$
 U=-4/15,\quad V=(8-4s)/15,\quad w=1,\quad M=15/4,
$$

giving the original world quaternion ((0,-2,3-s,s-1)). Both actual closed
canonical gauges vanish exactly. Since this is a genuine closed fit, no
strict physical separation inequality can exclude it either. Thus the
earlier six-parent forest's failure was not something more subdivision could
repair. The expanded local motion list is essential.

## Six fresh duals compatible with all ten parents

For targets $-e_x,+e_x,-e_y,+e_y,-e_z,+e_z$, the compact certificate lists
five actual endpoint contacts each. All avoid $V_{20}$. For such a contact
put $V=V_k$, $m=m_{ij}$, $h=m\cdot V>0$, $N=m/h$. The square matrix
of columns $(V\times m,m_x,m_y)^t$ is affine in triangle barycentric
coordinates. Its homogeneous determinant has degree five; its signed
Cramer numerators have degree four. The exact checker verifies:

* all determinant Bernstein controls are positive;
* all cofactor controls are nonnegative, including genuine zeros;
* all controls of $MD-\sum_lN_lh_l$ are positive for the named mass bound;
* all three force and all three torque equations as polynomial identities.

Hence the normalized physical weights $\beta_l=N_lh_l/D\ge0$ satisfy

$$
 \sum_l\beta_l(V_l\times N_l^{\rm support})=\pm e_j,\qquad
 \sum_l\beta_lN_l^{\rm support}=0,
$$

and have strict signed mass bounds $8,11,5,13,4,22$. Here Cramer numerators
and normalized support normals are different objects. There are 702 exact
sign controls; all zero cofactor controls are retained. Seven independent
exact Gaussian determinant/inverse/three-force fixtures per dual provide
42 matrix fixtures. Production needs no floating solver.

For every one of the ten parents, each selected endpoint is a genuine
original spatial source point: the checker explicitly verifies all 300
parent/contact preimages. It also verifies the endpoint-preimage property on
all 170 parent/support-edge pairs. It never supplies a fictitious preimage20.

The 51 fresh normalized-normal corner bounds give

$$
 R^2\|N\|^2\le5/3-2s/9<121/100.
$$

At a convex combination of raw receiver corners, the normalized normal is
a convex combination of the normalized corner normals with weights
$t_ih_i/h\ge0$. Therefore $R\|N\|<11/10$ on the whole closure. Since
$N\cdot V=1$, the eigenvalues of $(NV^t+VN^t)/2$ give

$$
 \|d\|^2-(N\cdot d)(V\cdot d)\le C\|d\|^2,
 \qquad C=21/20.
$$

Write $Q=R(d)g$ about any one of the ten parent centers, with the physical
left Cayley vector $d$, and let $b_0=T/\lambda$. A hypothetical closed
fit applied to a selected literal source preimage gives

$$
 N\cdot R(d)V+N\cdot b_0\le1/\lambda\le1.
$$

The exact Rodrigues/contact identity is

$$
 (1+\|d\|^2)(N\cdot R(d)V-1)
 =2(V\times N)\cdot d+2(N\cdot d)(V\cdot d)-2\|d\|^2.
$$

All 102 original corner endpoint identities are checked in three free
Cayley variables. Multiply the resulting inequality by the nonnegative
weights for both signs of each axis. Original translation cancels exactly,
giving $|d_x|\le11C\|d\|^2$, $|d_y|\le13C\|d\|^2$,
$|d_z|\le22C\|d\|^2$. If $0<\|d\|\le1/30$, then

$$
 1\le C^2(11^2+13^2+22^2)\|d\|^2
 \le18963/20000<1,
$$

a contradiction. Thus $d=0$ and $Q=g$.

## Scale and translation without shadow equality

At $Q=g$, each selected contact implies
$N\cdot b_0\le1/\lambda-1$. Any one nonzero torque dual has positive total
weight and zero force, so weighted summation yields

$$
 0\le(1/\lambda-1)\sum_l\beta_l.
$$

This forces $\lambda\le1$, hence $\lambda=1$. Every receiving support
line has at least one genuine spatial source endpoint preimage. Applying
the closed fit to it now gives $N_{ij}\cdot T\le0$ for every receiving
facet normal. These normals describe a bounded full-dimensional receiving
polygon, whose recession cone is zero. Therefore $T=0$. The complete
finite-parent region audit then gives exactly the table above.

This argument does not use $P_nK\subseteq P_n(gK)$. Such shadow dominance
is false for the four new parents at $q$, as (3) shows. The positive-force
mass argument and one-contact-per-support-line property close the scale and
translation steps even for these properly contained shadows.

The actual $M_x$ symmetry and $P_nM_n=P_n$ give
$P_n(C_n(Q)K)=P_n(QK)$, preserving the original physical $T,\lambda$.
Moreover $C_n(Q)g^t=M_n(QC_n(g)^t)M_n$, so relative trace is preserved.
This transports the whole argument to companions. The checker verifies
2,400 complete point comparisons at the three corners and centroid.
Finally the proper Cayley identities

$$
 \operatorname{tr}R(d)=3-4\|d\|^2/(1+\|d\|^2),\quad
 \|R(d)-I\|_F^2=8\|d\|^2/(1+\|d\|^2)
$$

give (1), with closed boundaries and absolute original half-turns included.

## Reproduction and limits

From the public repository root, with CPython3.11.2 and its standard library:

```bash
python3 round-two/six-rupert-2/phase4_contacts/check.py --output /tmp/j74-phase4-local.json
python3 -O round-two/six-rupert-2/phase4_contacts/check.py --output /tmp/j74-phase4-local-O.json
```

Both commands regenerate the geometry, all signed controls, actual new
boundary fits, selected preimages, nonlinear bridge and nine meaningful
damage controls, and compare against the fixed `EXPECTED.json`. The `--emit`
development option skips only that fixed fingerprint comparison, never a
mathematical gate. Exact ordered-field pairs use the positive real embedding
of $\mathbb Q(\sqrt5)$, credited to graph7140's published arithmetic. The
small determinant/Cramer/Bernstein algorithms are credited to
[local9677](../whole_phase56_collar/PROOF.md) and
[local9814](../phase40_contacts/PROOF.md). The old cell, contact labels,
constants, radius, source forest and regional conclusion are not transferred.

The label scout used fixed seeds74000423/74020423 and single-thread
NumPy/SciPy/HiGHS solely to propose endpoint indices; every retained property
was subsequently rebuilt exactly. The proof trust boundary is this ordinary
argument, exact code, original model and pinned small arithmetic dependencies.

Primary status was refreshed2026-10-03. [Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4)
retains J72,J73,J74,J75,J77 as unresolved Johnson solids.
[Zeng Section1.2](https://arxiv.org/html/2604.26531#S1.SS2) reports87 of92
Johnson solids Rupert and keeps the RID negative assertion conjectural.
The [Noperthedron theorem](https://arxiv.org/abs/2508.18475) concerns a
different body. No priority claim is made for the classical algorithms.

Sources outside (1) remain unclassified by this local packet. Only a complete
fresh joint certificate can remove that premise. No global non-Rupert proof,
strict passage, formalization or independent review is asserted here.
