# J74: three closed configuration cubes using only actual body symmetries

Author: **six-rupert-2**, actual role **researcher**. Ordinary intermediate
proof, author checked, unformalized and independently **UNREVIEWED**.
The global Rupert property of the original unit-edge J74 metabigyrate
rhombicosidodecahedron remains **OPEN**. This contribution supplies a complete
configuration reduction and a regional equality-branch corollary. It supplies
neither a passage nor a global exclusion.

The named body is the convex hull `K` of the original 60 vertices in
[model.py](../model.py), using the ordered field in [q5.py](../q5.py).
[The original named-geometry proof](../PROOF.md) establishes the two cupola
replacement construction, including its origin. We use this original body,
not a centrally symmetric substitute. The direct named-source fingerprints
are checked before importing either module; see [DEPENDENCIES.json](DEPENDENCIES.json).
The current primary sources leave J72, J73, J74, J75 and J77 unresolved:
[Gosain--Grimmer, Table 4](https://arxiv.org/html/2509.08190#S3.T4), with related
[Zeng discussion and proper projection definition](https://arxiv.org/html/2604.26531).
The proved [Noperthedron result](https://arxiv.org/abs/2508.18475) concerns a
different body. These are bounded current literature checks, not an exhaustive
novelty certification.

For a unit vector `n`, write `P_n=I-nn^T`, `M_n=I-2nn^T`,
`Mx=diag(-1,1,1)` and `H=diag(-1,-1,1)`. An original configuration has an
arbitrary `Q in SO(3)`, an unrestricted physical `T in n-perp` and its original
scale `lambda>=1`. Its closed fit is

```
lambda P_n(QK)+T subseteq P_n K.                         (1)
```

Strict interior containment is the usual projection formulation of the Rupert
property. The reductions below preserve the entire projected source set, so
apply to closed fits and strict fits alike, with the **same actual T and
lambda**. There is no source-normal, roll, Cayley or translation entry premise.

## The global three-cube statement

Set `L=7/4` and fix these three proper frames, written as matrices:

```
Sx=((0,0,1),(0,1,0),(-1,0,0)),
Sy=((1,0,0),(0,0,1),(0,-1,0)),
Sz=I.
```

They send `e_z` to `e_x,e_y,e_z`, respectively. They are coordinate frames;
no body symmetry is claimed for `Sx` or `Sy`. Their homogeneous quaternion
lifts are `(1,0,1,0)`, `(1,-1,0,0)`, `(1,0,0,0)`.

For each frame `S`, take the **entire closed five-dimensional cube**

```
(x,y,u,v,w) in [-1,1]^5
```

and retain the two closed quadratic gates

```
L^2 u^2 <= 1+x^2+y^2,     L^2 v^2 <= 1+x^2+y^2.           (2)
```

Decode

```
r=(x,y,1),
q_g=(1, L v-y+x w, x+y w-L u, w),
n=+/-S r/sqrt(1+x^2+y^2),
Q_g=S R_hom(q_g)/(q_g.q_g).                              (3)
```

Here `R_hom` is the standard homogeneous quaternion matrix, written explicitly
below. The scalar component of `q_g` is always one, so (3) is everywhere
well-defined, proper and continuous on the closed parameter domain.

**Theorem.** For every original `(n,Q,T,lambda)`, there is at least one
parameter tuple in one of these three closed gated cubes whose decoded
receiving plane is the original plane and whose decoded source satisfies

```
P_n(Q_g K)=P_n(QK).                                     (4)
```

The decoded `Q_g` is one of the four actual source motions

```
Q, QH, M_n Q Mx, M_n QH Mx.                             (5)
```

Consequently, existence of any original closed or strict fit is equivalent
to existence of such a fit among (3), retaining its original unrestricted
`T` and original `lambda`. Conversely every admitted parameter tuple gives
an actual receiver and a proper source, so the reduction introduces no
fictitious geometric configuration. The gates are sufficient to define a
cover; they need not select a unique representative of every orbit.
All receiving face ties, source scalar ties, source half-turns, cube sides
and corners are retained.

The entire ungated outer cube also satisfies

```
q_g.q_g <= 153/8,    (unit-normalized scalar of q_g)^2 >= 8/153.   (6)
```

The first bound is sharp on that outer cube. The radial constant required by
this particular maximal-scalar orbit construction is at least `sqrt(3)`;
`7/4` gives the exact positive squared margin `L^2-3=1/16`.
Neither sharpness assertion claims optimality of all possible coordinate
reductions or of the smaller gated domain in (2).

## Actual body actions and projection equivalence

The checker permutes **all 60 original vertices** under `H` and `Mx`, and
verifies the two cupola construction agrees with exactly that vertex set.
Thus `HK=K` and `MxK=K`. It separately checks `-K != K`: whole-body centrality
is not a premise. Since `H` commutes with `Mx`, the two source actions

```
D(Q)=QH,       C_n(Q)=M_n Q Mx
```

commute and are involutions on rotations. Both are proper: `H` is proper,
and the two reflections in `C_n` have determinant product one. Moreover

```
P_n QH K=P_n QK,
P_n M_n Q Mx K=P_n QK,
```

because `P_n M_n=P_n` and the two right factors act on the entire body.
This proves preservation of the entire source set, not just selected
supports. Translation and scale in (1) therefore stay fixed. Partial
regional equal shadows such as the later matrix `A` are **not** used as
right symmetries of an arbitrary source. The earlier
[regional J74 proof](../full_source_rectangle/PROOF.md) makes this distinction
explicit.

## Quaternion canonicalization with all closed boundaries

Choose any coordinate where `|n_j|` is maximal. Its value is nonzero.
Using the corresponding frame and either orientation of the same normal
line, write `n=+/-S(x,y,1)/sqrt(1+x^2+y^2)` with `|x|,|y|<=1`.
The signs of `n` do not affect either `P_n` or `M_n`. Closed face ties permit
more than one frame; no unique frame choice is needed.

In this relative frame put `n'=S^T n` and let a unit quaternion
`q=(h,x_q,y_q,z_q)` represent `S^T Q`. Use Hamilton units `i,j,k` and the
pure quaternion `p=(0,n')`. The lifts of the two physical actions are

```
D(q)=q k,
C(q)=p q i.
```

Indeed `R(k)=H`, `R(i)=-Mx` and `R(p)=-M_n'`, so the two minus signs cancel.
These linear maps obey

```
D^2=-I,      C^2=I,       CD=-DC,
```

and preserve unit norm. Thus the signed orbit
`+/-{q,Dq,Cq,CDq}` is closed under both actions. It is not assumed to have
eight distinct elements. The scalar components are

```
h,
-z_q,
-n'_x h-n'_y z_q+n'_z y_q,
-n'_y h+n'_x z_q-n'_z x_q.                               (7)
```

At least one is nonzero: if all four vanish, the first two give `h=z_q=0`,
and the last two, using `n'_z!=0`, give `y_q=x_q=0`, contradicting unit norm.
Choose a signed lift whose scalar component is positive and has greatest
absolute value among (7). Divide by that scalar to obtain
`q_c=(1,c_x,c_y,c_z)`. Closure of the signed orbit and maximality give

```
c_z^2 <= 1,
(x+y c_z-c_y)^2 <= 1+x^2+y^2,
(y-x c_z+c_x)^2 <= 1+x^2+y^2.                           (8)
```

Define

```
w=c_z,
u=(x+y w-c_y)/L,
v=(y-x w+c_x)/L.                                       (9)
```

Then `|w|<=1`, and (8) is exactly (2). Since `1+x^2+y^2<=3<L^2`,
we even have `|u|,|v|<=4sqrt(3)/7<1`. Formula (9) has the explicit inverse
`c_x=L v-y+xw`, `c_y=x+yw-Lu`, which is (3). The selected physical rotation
is one of (5); the preceding body argument proves (4). This completes the
global theorem, including original source half-turns. Such a half-turn can
have original scalar zero; (7) replaces it by a finite actual equivalent
source. No half-turn is discarded.

For reference, for any nonzero quaternion `q=(h,a,b,c)` of squared norm `N`,

```
R_hom(q)=((h*h+a*a-b*b-c*c, 2*(a*b-h*c), 2*(a*c+h*b)),
          (2*(a*b+h*c), h*h-a*a+b*b-c*c, 2*(b*c-h*a)),
          (2*(a*c-h*b), 2*(b*c+h*a), h*h-a*a-b*b+c*c)).
```

Direct polynomial multiplication gives `R_hom^T R_hom=N^2 I` and
`det R_hom=N^3`. The checker establishes every scalar coefficient of these
identities and of the two action formulas, independently of the finitely
sampled configurations.

## Norm bound and the sharp radial obstruction for this construction

In (3), the vector quaternion is affine in each one of `x,y,u,v,w`
separately. Its squared norm is therefore a convex quadratic in each variable
separately with the others fixed. Repeatedly maximizing a convex function on
`[-1,1]` reduces its maximum to the 32 corners. Exact evaluation at every
corner gives maximum `153/8`. For example `(x,y,u,v,w)=(1,1,-1,1,1)` has
`q_g=(1,7/4,15/4,1)` and squared norm `153/8`. Since its scalar is one,
unit normalization gives the second bound in (6). This argument deliberately
uses the whole outer cube, not a purported sharper gated maximum.

To see why this orbit construction needs `L>=sqrt(3)`, set `t=sqrt(3)>0`,
use the triple-tie receiver `(1,1,1)/sqrt(3)` in the identity frame and take

```
q_0=(t+1,0,-1,1).
```

It has `R(q_0)e_x=n`. Also, for the raw pure receiver `p_r=(0,1,1,1)`,

```
p_r q_0 i = -t q_0.
```

Thus `C_n(Q_0)=Q_0`. The four physical motions in (5) reduce to `Q_0` and
`Q_0H`. The former has strictly larger absolute scalar component than the
latter because `t+1>1`. Every maximal-scalar choice consequently gives the
same `q_c=q_0/(t+1)` and

```
|x+y c_z-c_y| = 1+2/(t+1)=t.
```

Hence `|u|=sqrt(3)/L`. Choosing another maximal receiving-coordinate frame
does not evade the obstruction: `Q_0e_x=n` makes `C_n(Q_0)=Q_0` in every
frame, and its nonzero scalar lift has `|C(q)_scalar/q_scalar|=1`, so the
raw first gauge numerator has magnitude `||r||=sqrt(3)` at this triple tie.
This is a sharp lower bound for the stated orbit construction.
The symbolic audit verifies the reflection identity and `R(q_0)e_x=n`
modulo `t^2-3`, so no floating `sqrt(3)` evaluation is needed.

## A regional consequence: only three canonical equality branches

This paragraph additionally uses the existing
[complete closed phase-crossing classification](../phase_crossing_box/PROOF.md),
LEMMA9531/0, source commit `2ba89329055167fe838b568349801a2d7ccd39be`.
It is an author-checked, independently unreviewed prerequisite. The global
three-cube theorem above does **not** depend on that classification.

Let `s=sqrt(5)>0`,

```
r_*=((2315-453s)/1798,(2211+205s)/1798,-1),
Omega=r_*+[-1/1000,1/1000]^2 x {0}.
```

The prior result classifies (1) on every point of this entire closed raw box,
both normal orientations, both actual 17-corner support phases and their
whole 16-corner closed seam: the only fits have `lambda=1,T=0` and

```
Q in E(n)=F union M_n F Mx,
F={I,H,A,AH,B,BH},
a=(s-1)/4, b=(s+1)/4, c=1/2,
A=((b,a,c),(-a,-c,b),(c,-b,-a)),
B=((-a,-c,-b),(c,-b,a),(-b,-a,c)).
```

All twelve proper original motions remain valid and distinct before
canonicalization. On this whole box `Sy` is the unique maximal-coordinate
frame, because `Y-X,Y+X,Y-1>0` for every original raw receiver `(X,Y,-1)`.
The three affine inequalities are positive at all four corners: 12 exact
checks imply their positivity everywhere.

The four-action source orbit partitions these twelve motions into the three
orbits anchored at `I,A,B`. The seed unit quaternions are respectively

```
(1,0,0,0),    (c,-b,0,-a),    (a,-c,0,b).
```

Multiply each by the conjugate of the `Sy` lift `(1,-1,0,0)` on the left,
obtaining a homogeneous relative quaternion `(h,x_q,y_q,z_q)` of squared
norm two. Here the unscaled relative raw receiver is `(X,1,Y)`.
Multiplying each normalized scalar score by the common squared raw norm
`R2=X^2+Y^2+1` gives four polynomials

```
S0=R2*h^2,
S1=R2*z_q^2,
S2=(-X*h+Y*y_q-z_q)^2,
S3=(X*z_q-Y*x_q-h)^2.                                  (10)
```

For `I,A,B` the unique winning actions on the **whole closed box** are
respectively **3,0,2**. This is not a center-only comparison: for each seed,
all three winning-minus-losing polynomials are expanded in the tensor
Bernstein basis of degree two in each raw receiver coordinate on
`Omega`. All nine coefficients of each gap are strictly positive in the
ordered field, giving **81 exact positive controls**. The minimum is

```
387673104799/808201000000
  +(709049747/808201000)*sqrt(5) > 0.                    (11)
```

All controls appear in [expected.json](expected.json). For clarity, if a gap
has power coefficients `a_pk` after the affine change from the raw box to
`[0,1]^2`, its Bernstein coefficient `(i,j)` is

```
sum_{p<=i,k<=j} a_pk * binom(i,p)/binom(2,p)
                     * binom(j,k)/binom(2,k).
```

The basis functions are nonnegative and sum to one on the entire closed
square. Strict positivity proves the asserted whole-box ranking, including
the phase seam. The checker additionally compares the polynomial and
Bernstein values at all four literal corners and at the midpoint for each
of the nine gaps: 45 independent exact evaluations.

Therefore the maximal-scalar canonical representatives of every possible
closed fit over `Omega` are precisely

```
M_n H Mx,     A,     M_n B Mx,                           (12)
```

and still have original `lambda=1,T=0`. Each does fit, by the prerequisite
and actual projection equivalence. Formula (12) reduces equality branches
for a future computation in these coordinates; it does not replace the
original twelve physical fits by a three-motion classification in the
original coordinates. In particular `A` is not used to right-fold arbitrary
sources. The corrected identity-orbit winner is action3, not action0.

## Computational boundary and the next use

This construction uses the classical quaternion double cover and finite
symmetry-orbit canonicalization. The related different-body
[RID closed grazing-quadrilateral proof](../../six-rupert-3/rid_closed_grazing_quad/PROOF.md)
uses maximal scalar gauges and a squared pure-receiver lift. Its RID body
centrality, larger group, constants and regional conclusion are not imported.
No general-method priority or independent verification of that proof is
claimed. The new concrete objects here are the actual J74 three closed
parameter cubes, gates, exact bounds and the whole-box three-branch corollary.

The adapted homogeneous source matrix has total receiving/source bidegree
at most `(2,2)`. Substituting it into a generic old receiver-quadratic source
cut can produce bidegree `(4,2)`; the explicit audited example is
`x^2*(q_g.q_g)`. An unoptimized receiver tensor would then have `5*5=25`
controls rather than the old `3*3=9`, with `3^3=27` source controls:
**675 rather than 243 controls per cut**. Thus three global configuration
cubes do not establish fewer proof nodes or faster exclusion. No old source
forest is asserted to transport under this coordinate change. The concrete
next step is to derive and benchmark fresh gated cuts and the three actual
regional equality holes before using the coordinates on an unclassified
receiving corridor.

[check.py](check.py) and [poly.py](poly.py) use exact rational polynomial
arithmetic and the published ordered `Q(sqrt(5))` arithmetic. They audit two
full-body permutations, three proper frames, 60 scalar universal polynomial
identities in 13 groups, the gauge inverse, 32 corner norms, seven scalar
identities for the sharp example modulo `t^2-3`, 36 direct numeric Hamilton
versus expanded-polynomial comparisons, and 96 entire 60-point projected
source fixtures. The fixtures include positive and negative receiving axes,
closed face/scalar ties and all three original half-turn axes. They
illustrate the implementation; the universal theorem rests on the written
argument and full polynomial identities, not sampling. Eight deliberately
damaged semantic controls must reject, including a partial shadow as a body
symmetry, an improper frame and opened receiver/source boundary domains.
The checker also exhibits a fixed identity-frame equatorial configuration
where all four scalar probes vanish; the three-frame choice is essential.

The complete mathematical and damage-control records passed both ordinary
and optimized execution with byte-identical output. Default reproduction
also compares the complete record against frozen expected output. Exact
resources, before-import fingerprints and expected-record hashes are in
[VALIDATION.json](VALIDATION.json); commands are in [README.md](README.md).
No coefficient corpus, private discovery data or network oracle supplies a
proof sign. The inherited named model and ordered-field implementation,
Python rational arithmetic and this compact source remain explicit trust
boundaries. Publication is provenance, not independent acceptance.
