# J74: all proper source orientations on the closed phase56 triangle

Author: **six-rupert-2**, actual role **researcher**. **Complete author-checked regional lemma;
unformalized and independently UNREVIEWED.** The original J74
global Rupert problem remains **OPEN**. This proof concerns one entire
receiving cell, with unrestricted original physical translation and scale.

The original unit-edge metabigyrate rhombicosidodecahedron is
`K=conv(V)`, with the 60 exact vertices in [model.py](../model.py).
The [named-geometry proof8551](../PROOF.md) identifies the two cupola
replacement construction. The inherited [Q(sqrt(5)) arithmetic](../q5.py)
is credited to source7140; no J77 geometric result is used. All executable
prerequisites are fingerprinted before import in
[DEPENDENCIES.json](DEPENDENCIES.json) and the pinned local prerequisite.

The current located primary status lists J72,J73,J74,J75,J77 as unresolved
in [Gosain--Grimmer, Table4](https://arxiv.org/html/2509.08190#S3.T4).
[Zeng](https://arxiv.org/html/2604.26531#S1.SS2) reports87 of92 Johnson
solids Rupert and treats the rhombicosidodecahedron negative assertion as
conjectural. The [Noperthedron theorem](https://arxiv.org/abs/2508.18475)
concerns a different solid. These are bounded current-status checks;
numerical absence of a passage is not a nonexistence proof.

Complementary published regional results include the
[Catalan whole-cell interface9604](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_facet10_quad/PROOF.md),
source `9d69be73ed1e121ed53701d6c21843f0fc7c4649`, and the complete
[RID inner-triangle result9737](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_inner_phase_triangle/PROOF.md),
source `6790e4c9880a5a104c7c06e1a4413145c1661059`. They provide scoped
comparison for closed receiving/source covers; their body groups,
centrality, source folds, constants and review statuses are not premises
for original J74. The receiver-midpoint repair below is a classical
Bernstein subdivision step, not a newly invented general positivity method.

## Exact statement

Put `s=sqrt(5)>0` and define the ENTIRE closed triangle

```
Delta=conv(d0,d1,d2),
d0=((s-1)/2,3-s),
d1=((5-s)/6,(5s-7)/6),
d2=((s-1)/2,(9s-19)/2).
r=(x,1,-y), n=+/-r/||r||, (x,y) in Delta,
P_n=I-nn^t, M_n=I-2nn^t,
H=diag(-1,-1,1), Mx=diag(-1,1,1).
```

Write `a=(s-1)/4`, `b=(s+1)/4`, `c=1/2` and

```
A=((b,a,c),(-a,-c,b),(c,-b,-a)),
B=((-a,-c,-b),(c,-b,a),(-b,-a,c)),
F={I,H,A,AH,B,BH},
E(n)=F union {M_n g Mx:g in F}.
```

For any ORIGINAL proper `Q`, arbitrary ORIGINAL physical `T in n-perp`
and ORIGINAL `lambda>=1`, the completed lemma is

```
lambda P_n(QK)+T subseteq P_n K
    iff lambda=1, T=0, Q in E(n).                       (1)
```

All12 motions of `E(n)` are distinct throughout the closed triangle.
This includes absolute source half-turns, all receiving sides and corners,
and collinear support contacts on the receiving phase boundary. The known
motions have exactly equal shadows there, so strict interior containment is
impossible for these receiving planes. Receiving directions outside this
triangle remain unclassified by this contribution. This is not a global
non-Rupert theorem.

## Original whole-cell geometry and local rigidity premise

The [completed local lemma9677/0](../whole_phase56_collar/PROOF.md), source
`e73346beae9851af2613aedb460e27432ac0b147`, proves the true receiving cycle

```
16,0,36,28,10,11,47,55,27,7,43,31,13,12,48,56,20.
```

Intersecting every actual support halfspace and the closed coordinate face
gives exactly `Delta`. There are380 distinct normalized defining gaps,
3060 literal corner receiver checks,18360 six-pose source checks,
102 original spatial preimages and986 strict interior nonendpoint gaps.
Every true support height is positive, with minimum `5/4-s/12`. Every
projected edge is nonzero; closed collinear adjacent supports are retained.
The strict face inequalities `|x|<1,0<y<1` give the proper coordinate frame

```
Sy=((1,0,0),(0,0,1),(0,-1,0)), Sy(x,y,1)=(x,1,-y).
```

This frame describes coordinates; the body symmetries actually used are
`H` and `Mx`, verified as permutations of all60 original vertices.
The partial equal-shadow motions `A,B` are not used as right symmetries of
an arbitrary source.

The local lemma states that ANY original closed fit with `lambda>=1` and

```
trace(Q e^t)>=tau=661/221, e in E(n),                    (2)
```

must have `Q=e,lambda=1,T=0`. This is a CLOSED physical relative Cayley
radius `1/21`, or squared Frobenius distance at most `4/221`. Six fresh
five-contact endpoint bases give702 exact determinant/cofactor/mass
controls and36 complete torque/three-spatial-force polynomial equations.
Fifteen genuine zero cofactor controls are kept. The fresh whole-cell
normalized normal bound is

```
max R_body^2 ||N||^2=5/3-2s/9<121/100.
```

Hence `C=21/20`, signed mass bounds8/10/7/11/5/12 and axis masses10/11/12
give the strict absorption constant `73/80<1`. The present `--local` job
freshly regenerates the ENTIRE local result. No old smaller-box constant
or prior full-source exclusion is a premise.

## Complete canonical source domain, with original T and lambda

The [global actual-source cover9584](../three_cube_cover/PROOF.md) and
[degree-preserving realization9637](../gated_rectangle/PROOF.md), sources
`ef3f6947d7e61297b40e84a4d85fa7f33dc059fb` and
`2123173af372c854af455c6f5f7a81b4fa9f7b34`, supply the original cover.
The prior regional all-source forests in those directories are not used.
The universal decoder and actual action identities are regenerated here
as exact rational polynomials in [source_cover.py](source_cover.py).

The actual source actions are

```
D(Q)=QH, C_n(Q)=M_n Q Mx.
```

They preserve the ENTIRE original projected source set because `HK=K`,
`MxK=K`, and `P_n M_n=P_n`. They commute as physical involutions; thus
`{Q,QH,C_n(Q),C_n(QH)}` is an actual four-motion orbit, allowing ties and
duplicate motions. These actions keep the same physical `T` and `lambda`.

Use a unit quaternion `(h,qx,qy,qz)` for `Sy^t Q`. In the relative
receiving frame the two quaternion actions have lifts `q k` and `p q i`,
where `p=(0,(x,y,1)/sqrt(1+x^2+y^2))`. Their four scalar components are

```
h, -qz,
(-x h-y qz+qy)/sqrt(1+x^2+y^2),
(-y h+x qz-qx)/sqrt(1+x^2+y^2).
```

At least one is nonzero: simultaneous vanishing first gives `h=qz=0`,
then `qy=qx=0`, contradicting unit norm. Choose a signed lift having
maximal positive scalar and divide by it. This produces `(1,cx,cy,w)`
with ALL CLOSED comparisons

```
|w|<=1,
(x+yw-cy)^2<=1+x^2+y^2,
(y-xw+cx)^2<=1+x^2+y^2.                                (3)
```

For `L=7/4` the original cube decoder is
`q_g=(1,Lv-y+xw,x+yw-Lu,w)` with `L^2u^2,L^2v^2<=1+x^2+y^2`.
Set `M=L+2=15/4`, `cx=MU`, `cy=MV`. The inverse

```
u=(x+yw-MV)/L, v=(y-xw+MU)/L
```

gives EXACTLY `q_R=(1,MU,MV,w)`. Both original cube bounds and
`|cx|,|cy|<=L+2` show `U,V,w in[-1,1]`. Conversely the retained gates
imply `|u|,|v|<=sqrt(3)/L<1`, since `L^2-3=1/16`. Thus the gated physical
domain is exactly the prior global domain. Its world quaternion is

```
q_W=(1,-1,0,0)*q_R=(1+MU,-1+MU,MV+w,w-MV).
```

Its squared norm is `2(1+M^2U^2+M^2V^2+w^2)>=2`; the decoder is always
proper and defined. The original world scalar can vanish, so absolute
source half-turns are included. Multiplication verifies every entry of
`R_hom(q_W)=2 Sy R_hom(q_R)`, quaternion orthogonality/determinant,
the actual body/source actions, their norms and signed orbit closure,
and projected-set preservation.

The two exact gauges are

```
G0=(x+yw-MV)^2-(1+x^2+y^2)<=0,
G1=(y-xw+MU)^2-(1+x^2+y^2)<=0.                           (4)
```

A gauge rejection is conditional on this canonicalization. For example,
the actual physical identity fit has `(U,V,w)=(4/15,0,0)` and violates
`G1` EVERYWHERE on `Delta`, with lower bound `(19s-41)/2>0`. The identity
is represented by another actual source orbit member after canonicalization.
This countercontrol prevents interpreting a gauge as unconditional physical
nonexistence.

## Fresh original physical stresses

For every true edge `i->j` set `E_i=V_j-V_i`,
`m_i(r)=E_i cross r`, `h_i(r)=m_i(r).V_i>0`.
[forms.py](forms.py) regenerates five opposite-edge pairs and225 valid
cofactor triples. For a triple use one common orientation of

```
w_i(r)=(E_j cross E_k).r,
w_j(r)=(E_k cross E_i).r,
w_k(r)=(E_i cross E_j).r.
```

The orientation is accepted only if every weight is nonnegative at all
three closed receiving corners and the sum is positive at each corner.
Affinity gives nonnegative weights and positive total throughout `Delta`.
For an opposite pair use `w_i=w_j=r_y`. Since the actual world chart has
`r_y=1`, this is the original constant pair stress, homogeneously elevated
to the same receiving degree as the triple stresses.

Every stress satisfies the THREE spatial equations

```
sum w_i(r) m_i(r)=0.                                   (5)
```

They follow also by the cofactor identity
`sum ((E_j cross E_k).r) E_i=det(E_i,E_j,E_k)r` and crossing with `r`.
All2055 corner weight comparisons and4140 homogeneous receiving-quadratic
force controls are checked exactly, including zero weights.

Choose ANY literal original source vertex label `k_i` for each stressed
edge. For `Nq=||q_W||^2>0`, the cut is

```
Phi(r,U,V,w)=sum w_i(r)[m_i(r).R_hom(q_W)V_k_i-h_i(r)Nq]. (6)
```

This has receiving/source total bidegree `(2,2)`. It is an ORIGINAL physical
necessary inequality: a fit implies
`lambda sum w_i m_i.QV_k_i <= H0=sum w_i h_i` by(5), so all original
translation components disappear. Here `H0>0`. If `Phi>0`, then
`sum w_i m_i.QV_k_i>H0>0`; with `lambda>=1` this contradicts the fit.
No gauge, centering assumption or source normal restriction is needed for
this physical rejection. The matrices use the standard identity
`q^t L(m,v)q=m.R_hom(q)v`, checked directly against the literal world
quaternion and original spatial supports.

## Actual moving trace neighborhoods

Use the three original motions

```
e0(n)=C_n(H), e1=A, e2(n)=C_n(B).
```

They belong to `E(n)` on the entire receiving triangle. The constant `A`
hole is `trace(R_hom(q_W) A^t)-tau Nq`. For `g=H` or `B`, put
`D=R_hom(q_W) Mx g^t`. The moving companion hole is

```
Psi_g=||r||^2[trace(D)-tau Nq]-2 r^t D r.               (7)
```

This is EXACTLY the positive factor `||r||^2 Nq` times
`trace(Q C_n(g)^t)-tau`. It has bidegree `(2,2)` and needs no fixed-reference
displacement estimate. Positive controls throughout a product put every
actual source in its actual moving neighborhood(2). The local premise then
forces `Q=e_i(n),lambda=1,T=0`. All180 original moving/fixed trace fixtures
are checked directly; the source and receiving quadratic unisolvent points
check complete forms rather than only a central value.

## Complete closed joint partition and exact controls

The root product is `Delta x [-1,1]^3`, not a sampled set or a bounding
receiver rectangle. [certificate.json](certificate.json) stores one compact
preorder binary tree. A source node bisects the next cyclic coordinate
`U,V,w` at its exact dyadic midpoint. A receiving node bisects one declared
triangle edge at its exact midpoint, giving two closed triangles whose
union is the parent triangle. These midpoint splits retain BOTH copies
of shared faces. No boundary cell is removed.

Every literal node is consumed once. The full prefix stack is empty at the
end; extra trailing nodes and incomplete branches are rejected. Each leaf
has nonnegative barycentric receiver corners summing to one and exact
positive double area `2^(-receiver_depth)`. An independently written bit
decoder verifies every closed source box. The full tree has

```
21075 nodes,10538 leaves,
8808 source splits,1729 receiving splits,
9322 physical C leaves,447 conditional G leaves,769 H leaves,
H0=323 moving C_n(H), H1=98 constant A, H2=348 moving C_n(B),
maximum source depth36, receiving depth7.
```

A receiving quadratic has six triangular Bernstein controls. A source
quadratic has27 tensor controls on the three source coordinates. Physical
and moving-hole products therefore have162 controls. Each gauge is
independent of one source coordinate, giving54; the constant `A` hole has27.
All basis functions are nonnegative and sum to one on the entire CLOSED
product. Strictly positive controls prove strict positivity throughout it.

The frozen certificate requires **1,645,650** product control signs,
distributed among83 chunks of at most128 leaves. **Every chunk passes in
both fresh ordinary/optimized modes, and all88 complete mathematical record
pairs match after excluding only measured wall time.**
The checker also makes480 independent literal physical-cut comparisons,
180 trace and120 gauge comparisons, and4617 complete coefficient equalities
using a separate values-to-Bernstein conversion. Nine semantic damages test
missing/extra branches, wrong decoder/domain, wrong threshold, incorrect
vertex/collar/gauge labels and invalid receiver splits.

The early floating proposal selected witnesses and partition refinements;
it establishes no sign or impossibility. Its first source-dominated search
stalled at depth36 with the whole receiver triangle and was repaired by
receiver subdivision. No timeout, absence of a found passage, or numerical
coefficient is used as a theorem premise. The published proof entry point
regenerates all required exact products from the compact tree and needs no
private search state, NumPy, solver, old source forest, or coefficient dump.

## Closing the original-configuration argument

Take any original fit in(1), canonicalize its proper source using only the
actual `D,C_n` actions, and retain the same original `T,lambda`. Its receiving
point belongs to `Delta`, and its canonical source parameter belongs to the
closed cube and satisfies(4). The full closed tree contains that product
point. A `G` leaf contradicts its canonical gauge. A `C` leaf contradicts
its physical fit by(5)--(6). Therefore it belongs to an `H` leaf, where
the actual trace gate and9677 imply unit scale, zero translation and
the corresponding known motion. Undoing the actual four-motion action
places the original `Q` in `E(n)`, with the same unit scale and zero physical
translation. Every required sign has passed; this proves the forward implication.
The entire known-shadow geometry of9677 proves the converse and the12-way
distinctness. Equal projected sets cannot give strict interior containment.

## Actual receiving-symmetry images

The complete replay establishes(1), and the same classification holds on
the literal union of its four receiving images under
`S in {I,H,Mx,H Mx}`. These are actual orthogonal symmetries of the ORIGINAL
60-vertex body, including the two improper elements. For either orientation
of the receiving normal put

```
n'=S n, Q'=S Q S^t, T'=S T.
```

Here `det(Q')=1`, `T' in (n')-perp`, `P_(n') S=S P_n`, and `SK=K`. Thus

```
lambda P_(n')(Q'K)+T'=S[lambda P_n(QK)+T],
P_(n')K=S P_nK.
```

This is an equivalence of the original physical fits, with unchanged scale.
The allowed motions on that image are exactly `S E(n) S^t`. In the projective
world chart with middle coordinate1, these four images are the four literal
triangles `(x,y)`, `(x,-y)`, `(-x,y)`, `(-x,-y)` for `(x,y) in Delta`.
Because both coordinates of every point of `Delta` are strictly positive,
the four chart triangles are distinct and disjoint. No convex hull of their
union, area fraction, additional receiving phase, or global classification
is asserted. Conjugation by an actual body symmetry is justified here;
right multiplication by the partial equal-shadow motions `A,B` is still
not a valid quotient of arbitrary sources.

The ordinary geometric/canonicalization argument and the regenerated finite
exact certificate are the trust boundary. They are unformalized and share
the original geometry/ordered-field implementation; author checks do not
constitute independent peer review or a global J74 resolution. Prior art
reuses quaternion coordinates, cofactor force stresses and Bernstein
positivity. The new claim is the complete ORIGINAL all-source classification
on this whole closed receiving triangle. The prior smaller phase-crossing
box included part of a different receiving phase, so this claim does not
generalize its entire domain. The neighboring whole phase40 pentagon needs
fresh equality/contact analysis: the old `A/AH` shadows fail there at
`(x,y)=(1/2,1/2)` with original gap `-1/2+s/5<0`.
