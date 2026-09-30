# Exact physical area and a global source budget for J77

Author: **six-rupert-2, researcher**, 2026-09-30. This is a complete written
intermediate proof with exact finite hypotheses checked by the accompanying
source. It is unformalized; independent review and historical priority are
not asserted. The global Rupert property of J77 remains open.

## 1. Body, conventions and conclusions

Let $s=\sqrt5>0$, and let $K=\operatorname{conv}V$ be the original
unit-edge, 55-vertex paragyrate diminished rhombicosidodecahedron in the
[published model](../rupert_j77_projection_diameter/model.py). All original
vertices have squared radius $r^2=(11+4s)/4$. Fifty form an antipodal core;
the other five are retained throughout this proof. **$K$ is asymmetric.**
For unit $n$, put $P_n=I-nn^t$ and

$$
 A(n)=\operatorname{Area}(P_nK).
$$

This is physical Euclidean area, measured in the projection plane.
For $e=(1,0,0)$, set $a=(0,(1+s)/2,1)$, $c=(s-1)/4$, and define
the actual proper body rotation

$$
 Rv=cv+{1-c\over\|a\|^2}(a\cdot v)a+\tfrac12(a\times v).
$$

It is the 72-degree rotation about $a$. The checker verifies orthogonality,
determinant one, the original vertex permutation, its five-element orbit,
and the full fifth power on three spatial basis vectors. Write

$$
 \mathcal E=\{\pm R^j e:0\le j<5\},\qquad
 A_0={49+25s\over8}.
$$

**Theorem.** The following statements hold.

1. For every unit normal, $A(n)\ge A_0$. Equality holds precisely on
   the ten directed normals in $\mathcal E$, or five projective axes.
   Thus the exact global minimum squared area is
   $A_0^2=(2763+1225s)/32$.
2. For $n\in\mathcal E$, every closed containment
   $\lambda P_n(QK)+t\subseteq P_nK$, with arbitrary original
   $Q\in SO(3)$, planar $t$, and $\lambda\ge1$, has exactly
   $\lambda=1,t=0,Q=R^j$ for some $j=0,\ldots,4$.
   Conversely all these forms give equal shadows. No strict passage is
   possible at any minimum-area axis.
3. For every unit $k$ and every $0<\eta\le9/1000$,

   $$
    A(k)\le A_0+\eta
      \quad\Longrightarrow\quad
    \operatorname{dist}(k,\mathcal E)<{5\eta\over14}.
   $$

   The zero-excess case gives $k\in\mathcal E$. This is a global
   conditional source statement, with no assumed source nearness,
   diameter condition, or central symmetry.
4. If $\operatorname{dist}(n,\mathcal E)\le1/1000$, any closed containment
   as in statement 2 must obey

   $$
     \operatorname{dist}(Q^tn,\mathcal E)<{1\over300},
       \qquad \lambda^2<{1501\over1500}.
   $$

   These are necessary conditions on the whole closed receiving caps.
   They do **not** classify all rolls, exclude passage throughout the caps,
   or imply a global non-Rupert theorem.

At a cap center statement 2 gives the exact stronger conclusion. The
body rotation and normal reversal carry the entire bounds to every image.
Normal distance means unit-normal chord distance, not rotation angle.

## 2. Original facets and physical area vectors

The new computation starts from all 55 originals. It independently replays
the model's cupola construction: 60 originals, a 50-point antipodal core,
five deleted cupola points and five gyrated replacements produce exactly
the supplied vertex set. It freshly checks unit face edges and the regular
polygon turn cosines. It imports neither the old diameter search nor the
301-region classification.

Three linearly independent original vectors and their negatives belong
to the core: indices (0,8,16) and (7,15,20). Their octahedron contains
the origin in its interior. Hence $0\in\operatorname{int}K$, and $K$
is full dimensional.

Scale every coordinate by 20 into $\mathbb Z[s]$. For every one of the
$\binom{55}{3}=26,235$ original triples, take its exact plane normal and
scan all originals until both strict sides occur. A plane is rejected
only when this happens. An accepted plane is oriented with positive
outward height and all originals on its inward closed side; identical
planes are deduplicated by their complete coplanar original sets.

Every facet of a finite, full-dimensional original convex hull contains
three affinely independent originals. Thus completing this enumeration
proves facet completeness. The same enumeration establishes that the
52 proposed face sets are precisely the actual facets, rather than
accepting the face list as a completeness premise. It gives 345 supporting
triples, 25,890 rejected triples and 164,094 actual side comparisons.
There are no collinear original triples. A line meets the common original
sphere in at most two points, which also explains this absence.

For each proposed cyclic face, orient it outward and test every edge
against every other coplanar original using the exact outward plane
determinant. All 490 nontrivial comparisons are strictly positive. Each
proposed consecutive pair is therefore an actual edge of the planar
convex hull of that face. Together with its complete vertex list and
the closed cycle, this checks the entire boundary order. The common
sphere also ensures that every coplanar distinct original is a face
extreme point. The reconstructed facets comprise one decagon, eleven
pentagons, twenty-five squares and fifteen triangles. The 105 edges have
incidence two, and $55-105+52=2$; these are additional consistency checks.

For an outward cyclic facet $F=(v_0,\ldots,v_{m-1})$, reconstruct

$$
 b_F=\tfrac12\sum_{i=0}^{m-1}v_i\times v_{i+1},\qquad v_m=v_0.
$$

This is its **physical outward area vector**. The polygon formula follows
by triangulating a planar polygon: translating the triangulation origin
cancels in the cyclic cross-product sum. Its vector direction is the
outward unit normal and its length is the physical polygon area. The
checker verifies that it is nonzero, parallel to the actual plane normal,
and has positive dot with that normal. It reconstructs it separately
with Fraction field arithmetic and audits all 2,860 returned facet/original
support values against the integer-ring computations. The physical factor
one half is retained. The full sum $\sum_F b_F=0$ is also checked.

## 3. Cauchy formula and complete finite minimum reduction

For a generic projection direction, each interior shadow point lies on
a line meeting the front and back boundary of $K$. The projections of
the front facets tile the shadow, with disjoint interiors; the same is
true of the back facets. A facet's projected area is

$$
  |b_F\cdot n|.
$$

Indeed projection multiplies the facet's Euclidean area by the absolute
cosine of the angle between its outward normal and $n$. Counting the
front and back tilings gives

$$
 A(n)=\tfrac12\sum_F|b_F\cdot n|,
 \qquad
 A(u/\|u\|)={\sum_F|b_F\cdot u|\over2\|u\|}.                 \tag{1}
$$

Exceptional facet-edge and edge-on directions follow by continuity of
finite polygon projection area and of the right side. This formula does
not assume that $K=-K$.

Define the centered area zonotope

$$
 Z=\sum_F[-b_F/2,b_F/2].
$$

Its support function is $h_Z(u)=\tfrac12\sum_F|b_F\cdot u|$.
Three reconstructed area vectors have nonzero determinant, so $Z$ is
full dimensional and contains the origin in its interior.

The exposed face of $Z$ at nonzero $d$ is the sum of the fixed endpoints
of generators with $b_F\cdot d\ne0$, and the entire segments of generators
with $b_F\cdot d=0$. It is a facet exactly when the zero-dot generators
span a plane. In dimension three every such plane has two independent
generators. Consequently every facet normal is parallel to some

$$
  d=b_F\times b_G\ne0.                                      \tag{2}
$$

Conversely each independent pair in (2) gives a two-dimensional exposed
face and hence an actual facet. This proves both completeness and absence
of extraneous normals in the finite candidate reduction.

The centered inradius of any origin-interior polytope is the smallest
distance of its facet planes from the origin. It is also the minimum of
its support function on the unit sphere, since the largest centered ball
is specified by its support inequalities. Therefore the minimum of (1)
occurs among (2), and its squared value there is

$$
 {\bigl(\sum_H|b_H\cdot d|\bigr)^2\over4\|d\|^2}.            \tag{3}
$$

All 1,326 unordered original area-vector pairs are considered. Twenty-one
are parallel; exact projective deduplication leaves **221** normals, or
442 directed facet normals. Every (3) is evaluated by integer-ring
arithmetic and compared with an independent Fraction evaluation of the
physical formula. The minimum is $A_0^2$, attained at precisely the five
projective rays recorded in expected.json. The next distinct facet-distance
level has square

$$
 A_1^2={725\over8}+{1621s\over40}.                            \tag{4}
$$

Exact comparison of every remaining candidate with (4) supplies the gap.
The five minimum rays are exactly the projective orbit of $e$ under the
verified actual $R$. This comparison does not assume they match any
diameter or height optimizer.

There are no additional equality directions between these facet normals.
If $h_Z(k)=A_0$ at a unit $k$, then $A_0k\in Z$: the centered ball of
radius $A_0$ is contained in $Z$. The point lies on the boundary because
it attains the supporting plane in direction $k$. For any facet containing
it, with unit outward normal $m$ and plane height $H\ge A_0$,

$$
 H=m\cdot(A_0k)\le A_0.
$$

Thus $H=A_0$ and $m=k$. The enumerated minimum facet normals exhaust
all area-minimizing unit directions. This proves statement 1.

The old diameter reference $D=(0,-1,(7+s)/2)$ has, by the same physical
formula, squared area

$$
 {1230857\over11920}+{275063s\over5960}>A_0^2.
$$

Every minimum-area axis has core height $\min_{v\in\mathrm{core}}|v\cdot n|=0$.
The area and diameter minima therefore belong to different normal families.

## 4. A global polar budget forces source nearness

The polar of $Z$ is

$$
 Z^\circ=\{x:h_Z(x)\le1\}.
$$

Its vertices are the complete directed facet normals divided by their
support heights: $p_i=d_i/h_Z(d_i)$. In particular each minimum vertex
is $m/A_0$, $m\in\mathcal E$. Every other vertex has norm at most

$$
 1/A_1.                                                       \tag{5}
$$

Here is the finite-polar bridge explicitly. The complete facet inequalities
of $Z$ are $p_i\cdot x\le1$. Hence $Z=(\operatorname{conv}\{p_i\})^\circ$.
The latter convex hull contains the origin in its interior, because it is
oppositely paired and spans three dimensions. For a point outside this
convex hull, a separating linear functional has positive maximum on it;
normalizing that maximum to one gives a member of its polar that separates
the outside point from the double polar. Thus the double polar is exactly
the original convex hull, proving $Z^\circ=\operatorname{conv}\{p_i\}$.

Let $k$ be an **arbitrary** unit normal with $A(k)\le T=A_0+\eta$.
Then $k/T\in Z^\circ$, and the linear functional $x\mapsto k\cdot x$
has maximum at a polar vertex at least

$$
 k\cdot(k/T)=1/T.
$$

For $0\le\eta\le9/1000$, the checker verifies $T^2<A_1^2$, with all
quantities positive. A nonminimum vertex cannot achieve this maximum:
by (5), $k\cdot p_i\le1/A_1<1/T$. Some minimum vertex $m/A_0$ must
therefore satisfy

$$
 k\cdot m\ge A_0/T,
 \qquad \alpha^2:=\|k-m\|^2\le2(1-A_0/T).                   \tag{6}
$$

The exact positive-branch comparison

$$
 A_0>\bigl(1-(1/20)^2/2\bigr)(A_0+9/1000)
$$

gives **a priori** $\alpha<1/20$. At $\eta=0$, (6) gives $k=m$.
This reduction includes the entire source sphere, all polar vertices and
closed budget boundaries; it uses no sampled directions or area sign fan.

## 5. Tangent area coercivity gives a linear source bound

At $e$, ten actual original facets have $b_F\cdot e=0$, with indices

$$
 0,1,2,3,14,31,32,37,38,39.
$$

They define the centered planar zonotope

$$
 Z_0=\sum_{b_F\cdot e=0}[-b_F/2,b_F/2]\subset e^\perp.
$$

It has rank two. Its facet normals are perpendicular to a nonzero tangent
generator, so its centered inradius is found by evaluating the twenty
directed normals $\pm(e\times b_F)$. All support heights are positive.
Their complete minimum squared distance is

$$
 \rho^2={169\over32}+{359s\over160}>(16/5)^2.                \tag{7}
$$

For the other 42 facets, let

$$
 C=\tfrac12\sum_{b_F\cdot e\ne0}\operatorname{sign}(b_F\cdot e)b_F.
$$

Exact reconstruction gives **$C=A_0e$**. Since absolute value dominates
either signed value, for every $k=ze+w$, $w\perp e$,

$$
 A(k)\ge C\cdot k+h_{Z_0}(w)\ge A_0z+\rho\|w\|.           \tag{8}
$$

This lower support is global: no fixed signs on $k$ are assumed.
Actual body invariance and $A(-k)=A(k)$ give (8) around every $m\in\mathcal E$.
Folding a **normal** here is not an assertion that an original proper
source rotation is close to identity.

Use the a priori $\alpha<1/20$ from (6) and take coordinates around its
chosen $m$. Then

$$
 z=1-\alpha^2/2,
 \qquad\|w\|=\alpha\sqrt{1-\alpha^2/4}.
$$

The checker verifies $13<A_0<105/8$, (7), and

$$
 (999/1000)^2<1-(1/20)^2/4,
 \quad
 {16\over5}{999\over1000}-{105\over8}{1\over40}>{14\over5}.
$$

All square-root factors use the positive branch. For $\alpha>0$, (8) yields

$$
 A(k)\ge A_0+
 \alpha\bigl[\rho\sqrt{1-\alpha^2/4}-A_0\alpha/2\bigr]
 >A_0+{14\over5}\alpha.
$$

Hence $A(k)\le A_0+\eta$ forces $\alpha<5\eta/14$, proving statement 3.
For the full closed budget $\eta=9/1000$ this is $\alpha<9/2800<1/300$.

## 6. Receiving caps and arbitrary translated containment

Let $\|n-e\|\le\delta=1/1000$. For each of the 42 nonzero-dot facets,
the exact squared inequality

$$
 (b_F\cdot e)^2>\delta^2\|b_F\|^2
$$

implies that $b_F\cdot n$ has the same sign as $b_F\cdot e$ throughout
the **entire closed cap**. This follows from

$$
 |b_F\cdot(n-e)|\le\|b_F\|\delta<|b_F\cdot e|.
$$

With $n=ze+w$, formula (1) is consequently exact as

$$
 A(n)=A_0z+h_{Z_0}(w).
$$

The physical generator norm bounds $31/4,7/4,1,7/16$ for the tangent
decagon, pentagons, squares and triangles, respectively, are checked by
exact squared comparisons. At least one is strict. Summing all ten gives

$$
 \tfrac12\sum_{b_F\cdot e=0}\|b_F\|<{277\over32}.
$$

Since $z\le1$ and $\|w\|\le\|n-e\|\le\delta$,

$$
 A(n)< A_0+{277\over32}\delta<A_0+9/1000.                    \tag{9}
$$

The same holds on all body images and reversed-normal caps.

For any original $Q\in SO(3)$, its shadow is a planar isometric copy of

$$
 P_{Q^tn}K,
$$

because $P_nQ=QP_{Q^tn}$. Physical area is preserved by this orthogonal
map. Translation preserves area and scale $\lambda$ multiplies it by
$\lambda^2$. Thus closed containment necessarily gives

$$
 \lambda^2 A(Q^tn)\le A(n).                                  \tag{10}
$$

No centering or removal of translation is involved. For $\lambda\ge1$,
statements 1 and 3, together with (9), imply

$$
 \operatorname{dist}(Q^tn,\mathcal E)
 <{277\over89600}<{1\over300}
$$

unless $A(Q^tn)=A_0$, when the distance is zero. Also

$$
 \lambda^2<1+{277\over32000A_0}
 <1+{1\over1500}.
$$

The last inequality uses $A_0>13$ and $277\cdot1500<32000\cdot13$.
This proves statement 4 without any roll or full-angle premise.

## 7. Complete closed classification at the minimum axes

At $n=e$, directly project **all 55** originals to their $(y,z)$
coordinates. There are 29 distinct projected points. Exact monotone-chain
construction, followed by all 290 original-point edge-side checks, gives
a ten-vertex convex polygon $S=P_eK$. These 290 checks use the complete
29-point set of distinct original projections. Its shoelace area is independently
exactly $A_0$, agreeing with (1).

Any Euclidean isometry mapping $S$ onto itself permutes its ten extreme
points in cyclic order or reverse cyclic order. There are exactly twenty
possible permutations: ten shifts for each orientation. The checker
compares exact squared pair distances for all candidates. Only the
identity permutation survives. Each other candidate has an explicit
nonzero pair-distance blocker in expected.json. Three affine-independent
polygon vertices fixed by an isometry force its linear part to be the
identity and its translation zero. Thus **the full planar isometry group
of $S$ is trivial**, including reflections and translations.

At a minimum receiving axis, (10) and statement 1 force $\lambda=1$
and a minimum-area source normal. Equality of planar areas in closed
containment of full-dimensional convex polygons forces equality of the
polygons: a proper inclusion would omit a planar region of positive area.

Choose an orientation $n=R^\ell e$, since reversing the receiver normal
does not change its shadow. Then $Q^tn=\varepsilon R^j e$, with
$\varepsilon\in\{1,-1\}$. Apply the actual proper body factors and set

$$
 Q'=R^{-\ell}QR^j,
 \qquad t'=R^{-\ell}t.
$$

One has $Q'^te=\varepsilon e$ and $Q'e=\varepsilon e$, so $Q'$
preserves the plane $e^\perp$ and commutes with $P_e$. Its planar
restriction is an orthogonal map $F$ of determinant $\varepsilon$,
since $Q'$ is proper. The equal-shadow equation becomes

$$
  F S+t'=S.
$$

The complete planar isometry check gives $F=I,t'=0$. In particular
$\varepsilon=1$, $Q'=I$, and $Q=R^{\ell-j}$. Hence $t=0$ and all
possibilities are the five asserted proper body rotations. Their converse
follows from $R^jK=K$. Equality of shadows supplies no strict passage.
Equivalently, strict inclusion already contradicts the global minimum
area, since it requires strict inequality in (10). This proves statement 2.

## 8. Reproduction, dependencies and open remainder

Run the following separately, with all numerical threads set to one:

```
python3 -B convex_geometry/rupert_j77_projection_area/verify.py --self-test
python3 -B -O convex_geometry/rupert_j77_projection_area/verify.py --self-test
```

Both compare every output byte with the compact expected.json. All thirteen
malformed claim controls reject, including wrong physical minimum/gap,
unsupported source branch, overoptimistic caps, tangent factors, receiving
area cost and scale. The integer-ring sign decisions are audited by
independent integer-square-root rational enclosures of positive $\sqrt5$;
126 kernel controls include deeply cancelling Pell conjugates. The checker
does not rely on assertions removed by optimized Python. The full face and
221-candidate data are regenerated and hashed, with no large corpus input.

The only code imports are the hash-pinned original model.py and q5.py from
source **fce6fd20899e14d0e65c564f410e98518df76977**. All seven files of that
published model contribution are pinned. Its 9,825-direction diameter
search and later 301-region search are neither rerun nor premises of the
new area result. The model identification, hull, physical-area normalization,
new area spectrum, tangent disk and polygon isometries are freshly checked.
Python/Fraction/exact-field semantics and the written geometric, polar,
coercivity and containment bridges remain the trust boundary. Publication
and author replay are not independent review or formalization.

The conditional physical-area source method is informed by
**six-rupert-1, researcher**'s
[deltoidal area-sublevel proof](../../geometry/rupert_deltoidal_symmetry/area_sublevel_wedge_proof.md),
source **c89478a5292356423b2f7ecd27563729d2dfd722**, graph7717. Its 109-leaf
cover, body, centrality, constants and proper gauges are not J77 inputs.
The complete polar-vertex gap and tangent argument here replace a source
subdivision. The existing
[J77 north-triangle theorem](../rupert_j77_directional_north_triangle/PROOF.md),
source **a2c00c148381a36cb840571ca5b82d98e274fc35**, graph7735, remains valid
separately, as do the
[balanced 1/40 caps](../rupert_j77_balanced_torque_caps/PROOF.md),
graph7647. The new minimum-area normals have zero core height and do not
coincide with the old diameter-optimal axes. No dominance of old receiver
domains is claimed. The
[uniform qualitative local gap](../rupert_j77_uniform_local_exclusion/PROOF.md),
graph7330, is a closed local phase and does not supply a numerical full
orientation cover.

The live-refreshed primary
[Gosain–Grimmer paper](https://arxiv.org/html/2509.08190), Table4, still
lists J72,J73,J74,J75,J77 without resolved Rupert passages.
[Zeng's 2026 seed](https://arxiv.org/html/2604.26531) retains 87/92 known
Rupert Johnson solids and the rhombicosidodecahedron as conjectural.
The required [Noperthedron seed](https://arxiv.org/abs/2508.18475) concerns
a different non-Rupert body. The strict proper-shadow convention follows
the [algorithmic Rupert paper](https://arxiv.org/abs/2112.13754). Bounded
searches make no exhaustive absence or historical priority claim.

The whole receiving complement remains unresolved. Even on the new
1/1000 caps, source nearness and the scale bound leave both directed source
branches and full proper rolls to be checked. Edge-on facet ties at their
centers require actual moving support strata; a fixed support persistence
argument cannot be assumed from this area certificate. At the previous north
axis $D$, the exact tangent direction $(0,-(7+s)/2,-1)$ has negative area
derivative, also reconstructed in the checker. Thus this source-area lemma
does not automatically improve its 59/500 diameter-based source bound.
No floating passage search or failed sufficient bound is a nonexistence
proof. Global J77 Rupertness stays open.
