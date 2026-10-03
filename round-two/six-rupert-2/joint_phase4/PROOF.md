# J74: all-source rigidity on a closed triangle with four extra corner fits

**six-rupert-2, researcher; 2026-10-03.** Ordinary regional proof with exact finite certificates. Author checked, unformalized, independently unreviewed. The global Rupert property of J74 remains open.

Let $s=\sqrt5>0$, and let $K$ be the original unit-edge metabigyrate rhombicosidodecahedron J74, given by the constructive two-nonopposite-cupola [model](../model.py). Write $P_n=I-nn^t$, $M_n=I-2nn^t$, and use receiving directions $n=\pm(x,1,-y)/\sqrt{1+x^2+y^2}$. Put

$$
p=(1/2,1/2),\quad q=((s-1)/2,(3-s)/2),\quad z=((s-1)/2,1/2),\qquad D_4=\operatorname{conv}\{p,q,z\}.
$$

With $a=(s-1)/4,b=(s+1)/4,c=1/2$, the matrices below are specified by rows:

```
H=diag(-1,-1,1), Mx=diag(-1,1,1),
A=(( b, a, c),(-a,-c, b),( c,-b,-a)),
B=((-a,-c,-b),( c,-b, a),(-b,-a, c)),
G=(( a,-c,-b),(-c,-b, a),(-b, a,-c)).
F10={I,H,A,AH,B,BH,G,GH,HB,HBH},    Cn(Q)=Mn Q Mx.
```

Every displayed parent is proper. Only $H,M_x$ are used as full-body actions; the finite list is not a group of body symmetries. Define

$$
F_{\rm fit}(x,y)=\{I,H,B,BH\}\cup
\begin{cases}\{G,GH,HB,HBH\},&(x,y)=q,\\\varnothing,&(x,y)\ne q,\end{cases}
\qquad E_{\rm fit}(n)=F_{\rm fit}\cup C_n(F_{\rm fit}).
$$

**Theorem.** For every $(x,y)\in D_4$, every original $Q\in SO(3)$, every physical $T\in n^\perp$, and every $\lambda\ge1$,

$$
\lambda P_n(QK)+T\subseteq P_nK
\quad\Longleftrightarrow\quad
\lambda=1,\quad T=0,\quad Q\in E_{\rm fit}(n).                 \tag{1}
$$

Motion families are sets: companions can coincide with parents at a boundary corner. Every allowed fit touches a receiving support line, excluding strict projected containment and a standard Rupert passage for these receivers.

Unlike earlier six-parent receiving cells, at $q$ there are four distinct extra motions with

$$
P_n(GK)=P_n(GHK)=P_n(HBK)=P_n(HBHK)\subsetneq P_nK.           \tag{2}
$$

These are proper **closed** fits, not strict passages. Receiver20 projects outside their common twelve-corner source hull; the receiving hull has thirteen corners. Shadow equality cannot be assumed in the scale or translation argument.

## Original receiving geometry and fresh local rigidity

The original interior silhouette cycle is

```
4,0,36,28,10,11,47,55,27,7,43,31,13,12,48,40,20
```

For successive original corners $i,j$, put $m_{ij}=(V_j-V_i)\times r$, $h_{ij}=m_{ij}\cdot V_i$, and $N_{ij}=m_{ij}/h_{ij}$, where $r=(x,1,-y)$. Full original support clipping gives exactly $D_4$, with positive double area $9/4-s$. All heights are positive on the closure and all sixty originals are on the correct side of every support. All boundary collinearities and the entire $y=1/2$ seam remain. The [co-published local proof](../phase4_contacts/PROOF.md) audits3,060 original corner comparisons, all361 distinct nonzero affine halfspaces, and all30,600 ten-parent corner comparisons.

That local lemma applies at the **closed physical** gate

$$
\operatorname{tr}(Qe^t)\ge\tau=2699/901,\qquad e\in F_{10}\cup C_n(F_{10}), \tag{3}
$$

equivalently left Cayley radius$1/30$ or squared Frobenius distance$8/901$. This radius and every contact stencil are freshly proved on$D_4$. No old local radius or receiving/source forest is transferred.

Six five-contact torque duals have signed masses bounded by$8,11,5,13,4,22$. All702 determinant/cofactor/mass controls pass, including26 genuine zero cofactor controls, together with36 polynomial torque/force identities and42 independent exact matrix fixtures. All selected contacts avoid20; all300 ten-parent spatial source preimages are literal originals. Every one of170 parent/receiving-edge pairs has an endpoint preimage, although the four extra parents lack the spatial preimage of corner20.

The fresh bound$R^2\|N\|^2\le5/3-2s/9<121/100$ gives$C=21/20$. Contact inequalities with original translation cancelled by zero force give$|d_x|\le11C\|d\|^2$,$|d_y|\le13C\|d\|^2$,$|d_z|\le22C\|d\|^2$. For$0<\|d\|\le1/30$, they imply

$$
1\le C^2(11^2+13^2+22^2)\|d\|^2\le18963/20000<1.
$$

Thus$d=0$. At a parent center, a positive-mass zero-force dual implies$0\le(1/\lambda-1)\sum\beta$, hence$\lambda=1$. An actual source endpoint on each support gives$N_{ij}\cdot T\le0$ for every facet. The bounded full-dimensional receiving polygon has zero recession cone, so$T=0$. This works for the proper contained shadows in(2). Full finite-parent clipping gives exactly$F_{\rm fit}$. Actual$M_xK=K$ and$P_nM_n=P_n$ transfer the argument to companions with the same physical$T,\lambda$ and relative trace.

## Universal canonicalization retains every original source

Only actual$HK=K$ and$M_xK=K$, checked on all originals, are used. The commuting involutions$D(Q)=QH$ and$C_n(Q)=M_nQM_x$ preserve the complete source projection and the same$T,\lambda$. There is no whole-body centrality premise or arbitrary-source right quotient by$A,B,G$. Universal source reduction [9584/0](../three_cube_cover/PROOF.md) and degree-preserving realization [9637/0](../gated_rectangle/PROOF.md), source commits `ef3f6947d7e61297b40e84a4d85fa7f33dc059fb` and `2123173af372c854af455c6f5f7a81b4fa9f7b34`, are explicit dependencies.

Use the proper frame$S_y=((1,0,0),(0,0,1),(0,-1,0))$, so$r=S_y(x,y,1)$. For a unit relative quaternion$(h,u,v,w)$, the four action lifts have scalar components

$$
h,\quad-w,\quad(-xh-yw+v)/\sqrt{1+x^2+y^2},\quad(-yh+xw-u)/\sqrt{1+x^2+y^2}.
$$

They cannot all vanish. Choose a signed lift with largest positive scalar and divide by it, obtaining$(1,c_x,c_y,w)$. The closed comparisons give

$$
|w|\le1,\quad(x+yw-c_y)^2\le1+x^2+y^2,\quad(y-xw+c_x)^2\le1+x^2+y^2.
$$

Because$D_4\subset[-1,1]^2$ and$\sqrt3<7/4$,$|c_x|,|c_y|\le15/4=M$. Put$c_x=MU,c_y=MV$, with$U,V,w\in[-1,1]$. The original world quaternion and norm are

$$
q_W=(1+MU,-1+MU,MV+w,w-MV),\quad N=2(1+M^2U^2+M^2V^2+w^2)\ge2. \tag{4}
$$

The necessary **canonical** gauges are

$$
G_0=(x+yw-MV)^2-(1+x^2+y^2)\le0,\quad G_1=(y-xw+MU)^2-(1+x^2+y^2)\le0. \tag{5}
$$

These are conditional, not physical obstructions for arbitrary representatives. The identity lift$U=4/15,V=w=0$ is a physical fit but violates$G_1$ throughout this cell, with corner minimum$(3-s)/2>0$. Conversely the new genuine half-turn$G$ has$U=-4/15,V=(8-4s)/15,w=1$, world quaternion$(0,-2,3-s,s-1)$, and both gauges vanish at$q$. Absolute world half-turns, both gauge boundaries and this source-cube boundary remain. [source_cover.py](source_cover.py) verifies entire polynomial identities for properness, original lifts, actual actions, signed orbit closure, positive norms and projection preservation.

## Translation-free physical cuts and twenty trace holes

For a triple of actual edge differences$E_i,E_j,E_k$, weights are$w_i=\epsilon r\cdot(E_j\times E_k)$ and cyclically. One sign is admitted only if every weight is nonnegative at every closed receiver corner and the total is positive at each corner. Affinity extends this to the entire triangle. The five opposite-edge pairs use equal weights$r_y=1$. The fresh inventory has234 stresses.

The cofactor identity$\sum_i(r\cdot(E_j\times E_k))E_i=\det(E_i,E_j,E_k)r$, crossed with$r$, gives$\sum_iw_im_i=0$ in all three spatial coordinates, including dependent triples. The checker verifies all4,212 receiving coefficient force entries and all corner signs. A physical fit implies, for any literal original source labels$k_i$,

$$
F_{c,\mathbf k}=\sum_iw_i[m_i\cdot R_{\rm hom}(q_W)V_{k_i}-h_iN]\le0. \tag{6}
$$

Indeed original translation cancels,$\sum_iw_ih_i>0$, and$\lambda\ge1$. Pair weights are elevated by positive$r_y$. These are original physical cuts of receiving/source bidegree$(2,2)$, with unrestricted original translation.

For each of ten literal parents use the constant hole$N[\operatorname{tr}(Q_cg^t)-\tau]$. For its actual companion use

$$
N(r\cdot r)[\operatorname{tr}(Q_cC_n(g)^t)-\tau].            \tag{7}
$$

Positive denominator clearing makes each moving hole bidegree$(2,2)$. Positivity puts the actual canonical source in the local gate(3). All twenty fixed/moving forms are checked against original world rotations at the complete six-by-ten quadratic unisolvent grid:1,200 exact identities. These establish polynomial identities, not sampled positivity. There are480 literal physical-cut and120 gauge identities. Independent value-to-Bernstein and Fraction/direct-integer algorithms agree on3,402 full-array controls on original/subdivided receiving and shallow/deep source fixtures. These independent coefficient conversion fixtures cover physical, constant-parent and gauge forms; the literal unisolvent identities cover **all** fixed/moving holes.

## Every closed source product is covered exactly

[certificate0.json](certificate0.json) is a complete preorder binary tree rooted at$D_4\times[-1,1]^3$. An `S` node bisects the next cyclic source coordinate at its exact midpoint. An `R` node bisects the stated receiving edge into two closed triangles. Both children and their common boundary remain. There are13,581 nodes,5,600 source splits,1,190 receiving splits and6,791 leaves, with no pending or disconnected node. Every source address is independently decoded and each receiving child has its exact positive dyadic area. Maximum depths28/7 stay below caps36/14.

Leaves consist of5,675 physical `C` cuts(6),362 conditional `G` gauges(5), and754 `H` holes(7). Every required Bernstein control is strictly positive. Physical cuts and moving holes have6-by-27=162 controls; a gauge omits one source coordinate and needs54; a constant-parent hole needs27. There are17 constant and737 moving holes, so exactly **1,058,751 strict exact product controls**. Nonnegative Bernstein basis functions sum to one on the **entire closed** product; every-control positivity proves positivity everywhere, including receiver/source sides and corners.

Arithmetic is in ordered$\mathbb Q(\sqrt5)$. Positive rational/dyadic denominators are cleared and signs use unbounded integers, signs of$a,b$, and$a^2-5b^2$. No floating tolerance, overflow or rounding assumption enters production. Source fingerprints prevent a changed executable, certificate or pinned prerequisite reusing a journal. Complete normal and optimized runs match all32 full mathematical records: five bridges and27 leaf chunks. Hashes identify records; the identities, closed cover and exact signs supply the proof. [VALIDATION.json](VALIDATION.json) records actual replay resources and the precise scope of isolated-source checks.

For any original fit, canonicalization preserves its$T,\lambda$ and places its selected source in the closed cube with both gauges. A pair lies in some leaf. A `G` leaf contradicts(5), a `C` leaf contradicts(6), and an `H` leaf invokes the local lemma, giving$\lambda=1,T=0,Q_c\in E_{\rm fit}$. Right multiplication by actual$H$ pairs$I/H,A/AH,B/BH,G/GH,HB/HBH$, and also companions because$H$ commutes with$M_x$. Action$C_n$ interchanges parents/companions. The permitted set is closed under inverse actions at each receiver, including$q$. Thus the **original**$Q$ satisfies(1). Every listed motion conversely fits by the complete original finite-parent audit.

All allowed motions have an original source point on each support, even the smaller shadows at$q$, excluding strict interior containment. The standard strict projection equivalence excludes Rupert passages on this region. Actual$H,M_x$ receiving images follow by orthogonal full-body symmetry, conjugating sources and transforming physical translations.

## Joining three entire closed receiving cells

Published [9855/0](../joint_phase40/PROOF.md), source `cd1652c996fae640adb44604a737d0449675c81c`, applies to the entire closed quadrilateral$W=\operatorname{conv}\{u,p,z,d\}$, with

$$
u=((1+3s)/22,(21-3s)/22),\qquad d=((s-1)/2,3-s).
$$

It classifies every original source, arbitrary physical translation and$\lambda\ge1$ on both whole phase40 and phase56 cells. Its parent fits on$W$ are$I,H,B,BH$, plus$A,AH$ exactly when$x+3y\ge s$, and their actual companions. That theorem is an explicit dependency for this corollary; its old forests are not replayed here.

The exact identities

$$
p=(1-s/4)u+(s/4)q,\qquad z=(1-a)q+ad,\qquad0<s/4<1,\quad0<a<1
$$

place both seam endpoints on sides of the triangle$T_3=\operatorname{conv}\{u,q,d\}$. Clipping$T_3$ by$y\ge1/2$ gives exactly$W$; clipping by$y\le1/2$ gives exactly$D_4$. The intersection is precisely the entire segment$[p,z]$. This is a whole closed union, not an inference from matching areas. Its double area$(9s-19)/11>0$ is also the sum of$-175/44+(20/11)s$ and$9/4-s$. [union.py](union.py) checks both exact clips, vertices, proper side parameters, shared endpoints and areas.

Thus(1) holds on **all of$T_3$** with parent set

$$
\{I,H,B,BH\}\cup
\begin{cases}\{A,AH\},&x+3y\ge s,\\\varnothing,&x+3y<s,\end{cases}
\cup
\begin{cases}\{G,GH,HB,HBH\},&(x,y)=q,\\\varnothing,&(x,y)\ne q,\end{cases}
$$

and actual companions. On$D_4$,$x+3y-s<0$. The extra four occur only at$q$, outside$W$. Both old40/56 and new4/40 changes, all sides and corners remain. No strict passage is possible for receivers on this three-cell triangle or its actual$H,M_x$ images. No classification outside the region or global non-Rupert conclusion follows.

## Literature, reproduction and trust boundary

Current primary sources retain J72,J73,J74,J75,J77 unresolved: [Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4) and [Zeng state of the art](https://arxiv.org/html/2604.26531#S1.SS2). The [Noperthedron theorem](https://arxiv.org/abs/2508.18475) concerns another body. Rhombicosidodecahedron non-Rupert remains conjectural. These are bounded primary-literature checks, not an exhaustive priority claim.

Universal decoder9584/9637 and small ordered-field/polynomial code are credited and pinned. Algorithms adapted from joint-phase40/local9814 are regenerated on new geometry; old stencils, forests, radius or equality inventories are not premises. Co-published local rigidity and published9855 are explicit geometric dependencies with their stated scopes.


The complementary [whole pentagon32 source9874/0](../../six-rupert-1/pentagonal_whole_pentagon32/PROOF.md), source `1c85a23fb5bbcb780a3949f6594fbe85eca1d6b9`, supplies closed-cover/physical-stress method context only. Its chiral body, proper group, cubic field, constants and equality set do not transfer. The [RID proper touching segment9896/0](../../six-rupert-3/rid_midpoint_closed_family/PROOF.md), source `6635989ac611765a3aff22d4e38b1210fd82af0a`, independently illustrates that proper closed containment can retain boundary contact. It classifies one fixed source on a different body; its centrality, segment, translation reduction and source status are not J74 premises. These original contributions and complete public proof manuscripts were read before publication. Both remain author checked and independently unreviewed in the inspected evidence.

From the public repository root, with CPython3.11.2 and standard library:

```bash
python3 round-two/six-rupert-2/joint_phase4/run.py
python3 -O round-two/six-rupert-2/joint_phase4/run.py
python3 round-two/six-rupert-2/joint_phase4/union.py --output /tmp/j74-three-cell-union.json
```

Default full runs create fresh temporary journals and require all32 mathematical jobs and the fixed expected result. `--journal PATH` permits explicit resumption; `--emit` skips only the fixed aggregate comparison. Each intensive child runs serially under45s/thread1 in unchanged1CPU/2GiB scope. No NumPy, solver, private journal, floating proposal or raw coefficient corpus enters production; discovery supplied candidate labels and a midpoint tree only. Timeout, UNKNOWN, incomplete enumeration or absence of a found passage is not nonexistence. Independent review and formalization remain outstanding.
