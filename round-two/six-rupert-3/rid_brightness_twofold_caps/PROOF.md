# RID brightness and all-source twofold receiving caps

**six-rupert-3, researcher; 2026-10-01.** Written geometric proof with exact
finite hypotheses checked by the accompanying source. Unformalized and
author-checked; independent review and historical priority are not asserted.
The global Rupert property of the standard rhombicosidodecahedron remains open.

## 1. Original body and precise conclusions

Put \(\phi=(1+\sqrt5)/2\), and let \(V\) consist of all even coordinate
permutations and independent signs of
\[
(1,1,\phi^3),\qquad (\phi^2,\phi,2\phi),\qquad (2+\phi,0,\phi^2).
\]
These are the sixty original vertices of the **edge-two** RID,
\(K=\operatorname{conv}V=-K\). Every vertex has squared radius
\(R^2=7+8\phi<20\). For a unit vector \(n\), let
\[
 P_n=I-nn^t,\qquad A(n)=\operatorname{Area}(P_nK),
 \qquad A_0=12+28\phi.
\]
Let \(G\) be the sixty-element proper body rotation group generated and
verified in field.py, and set
\[
 e=(0,0,1),\qquad \mathcal T=\{ge:g\in G\},\qquad
 \delta=1/30000.
\]
Thus \(\mathcal T\) consists of thirty directed unit normals, or fifteen
unoriented twofold axes. Distance below is Euclidean **unit-normal chord
distance**, rather than the angle of an original spatial rotation.

**Theorem.**

1. For every unit normal, \(A(n)\ge A_0\), with equality exactly when
   \(n\in\mathcal T\).
2. For every unit \(n\) and \(0<\eta\le1/20\),
   \[
   A(n)\le A_0+\eta
    \quad\Longrightarrow\quad
   \operatorname{dist}(n,\mathcal T)<\eta/12.
   \tag{1}
   \]
   The zero-excess case gives \(n\in\mathcal T\).
3. Let \(B_1,B_2\) be arbitrary real \(2\)-by-\(3\) matrices with
   orthonormal rows, let \(n_2\) be a unit kernel normal of \(B_2\), and
   suppose \(\operatorname{dist}(n_2,\mathcal T)\le\delta\). For every
   \(t\in\mathbb R^2\) and \(\lambda\ge1\),
   \[
    \lambda B_1K+t\not\subset\operatorname{int}(B_2K).
   \tag{2}
   \]
   There is no source-normal, relative-roll, or initial full-rotation
   restriction in this statement.

Statement 3 includes all proper original placements
\(\lambda P_n(QK)+t\), \(Q\in SO(3)\), viewed in an orthonormal frame of
the receiving plane. It excludes strict passages on the entire **closed**
receiving caps. It makes no classification of touching closed placements
and no assertion about the receiving complement.

The general Cauchy-area, polar, and tangent-coercivity method is credited to
[six-rupert-2's published J77 proof, Sections 3--5](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
graph `bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au`.
That method is reused, not claimed as new. The RID facet geometry, complete
spectrum, source constants, original proper-roll reduction, and all-source
twofold cap exclusion here are fresh specializations. The final local
criterion is the already published
[paired/singleton mirror-cluster corollary](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md),
whose frame premise is derived below from arbitrary containment.

## 2. Complete original facets and the physical area norm

The checker enumerates all \(\binom{60}{3}=34220\) original triples,
using exact integer pairs for \(\mathbb Z[\phi]\). No triple is collinear;
this also follows because a line meets the common sphere in at most two
points. A triple whose plane passes through the origin cannot be a supporting
facet: the antipodal spanning original set puts the origin inside \(K\).
Every other plane is oriented with positive outward height, and the checker
rejects it if any original is outside. A facet of a full-dimensional finite
convex hull contains an independent triple, so this exhausts the hull facets.
There are 260 supporting triples and exactly 62 facets: twenty triangles,
thirty squares, and twelve pentagons.

Every complete coplanar original set is given a cyclic boundary order.
Every directed cycle edge is tested against every other coplanar original
by a strictly positive plane determinant. These gates verify the full
convex boundary, including orientation. For each outward facet cycle,
\[
 c_F=\frac12\sum_j v_j\times v_{j+1}
 \tag{3}
\]
is its **physical area vector**, not a normalized face normal. Polygon
triangulation proves (3); its length is the Euclidean facet area. The
checker verifies direction, exact squared areas \(3,16,15+20\phi\), and
all 3720 original support values independently in Fraction field arithmetic.
The area vectors occur in opposite pairs; select one representative of each
pair to give a list \(C\) of 31 vectors.

For a generic direction, the projected front facets tile the shadow with
disjoint interiors, as do the back facets. A facet contributes projected
area \(|c_F\cdot n|\), by the cosine rule for orthogonal projection.
Counting both tilings and then using continuity at nongeneric directions
gives Cauchy's formula
\[
 A(n)=\frac12\sum_F|c_F\cdot n|
     =\sum_{c\in C}|c\cdot n|.
 \tag{4}
\]
Thus \(A\) is the support function of the full-dimensional centered
zonotope \(Z=\sum_{c\in C}[-c,c]\), restricted to unit vectors.
The checker verifies that the generators span three dimensions.

For an independent definition-level check, it constructs the convex hull
of the sixty projected originals with a two-dimensional monotone-chain
algorithm at **every one** of the 121 candidate axes below and at three
other exact directions. The shoelace area, with its physical coordinate
Jacobian retained, agrees with (4) in all 124 cases. No numerical hull
library, floating tolerance, or presumed shadow vertex list is used.

## 3. Finite polar spectrum and all equality directions

The exposed face of \(Z\) at a nonzero \(r\) fixes the endpoint of every
generator with \(c\cdot r\ne0\), and retains the whole segment for every
generator with \(c\cdot r=0\). Its dimension is the rank of the latter
generators. Hence it is a facet exactly when those generators span a plane.
In three dimensions this plane contains two independent generators. Thus
the complete projective facet-normal list is
\[
 r=c\times d\ne0,\qquad c,d\in C,
 \tag{5}
\]
after exact projective deduplication. Conversely any independent pair in
(5) yields a two-dimensional exposed face, so no candidate is extraneous.
All 465 pairs are considered; they give exactly 121 projective normals,
or 242 directed facets and polar vertices.

The centered inradius of \(Z\) is the smallest of its facet-plane heights,
and is also the minimum of its support function on the unit sphere. At
the raw normal \(r\), the squared height is
\[
 \frac{\big(\sum_{c\in C}|c\cdot r|\big)^2}{r\cdot r}.
 \tag{6}
\]
Every value in (6) is checked exactly. The complete distinct spectrum is:

| squared facet-plane height | projective axes |
| --- | ---: |
| \(928+1456\phi=A_0^2\) | 15 |
| \(940+1520\phi=A_1^2\) | 6 |
| \(960+1536\phi\) | 10 |
| \((4848+7744\phi)/5\) | 30 |
| \(986+1584\phi\) | 30 |
| \(2960/3+1584\phi\) | 30 |

These levels are strictly ordered. The fifteen minimum rays are checked
against exactly the projective orbit of \(e\) under \(G\). The group
closure, orthogonality, proper determinants, and preservation of **all**
originals are freshly verified; its directed orbit has size thirty.

There are no extra equality directions between the enumerated normals.
If \(A(n)=A_0\) for a unit \(n\), the centered ball of radius \(A_0\)
is contained in \(Z\), and \(A_0n\) is on its boundary. For any facet
containing that point, with unit outward normal \(m\) and height
\(H\ge A_0\),
\[
 H=m\cdot(A_0n)\le A_0.
\]
Thus \(H=A_0\) and \(m=n\). The complete minimum facet list therefore
exhausts all equality normals. This proves statement 1.

## 4. Global source localization from the polar

The polar \(Z^\circ\) is the convex hull of the 242 directed vertices
\[
 \frac r{\sum_{c\in C}|c\cdot r|}.
\]
This is the standard finite-polytope duality: the complete facet
inequalities of \(Z\) are exactly the polar inequalities of this convex
hull, and separation proves the double-polar identity. Every minimum
vertex is \(m/A_0\) for \(m\in\mathcal T\); every other vertex has
norm at most \(1/A_1\).

Let \(n\) be arbitrary unit, with \(A(n)\le T=A_0+\eta\) and
\(0\le\eta\le1/20\). Homogeneity gives \(n/T\in Z^\circ\).
A maximizing polar vertex for the linear functional \(x\mapsto n\cdot x\)
has value at least \(n\cdot(n/T)=1/T\).
The exact scalar checks give
\[
 50<A_0<115/2,\qquad T<58<A_1.
\]
A nonminimum vertex cannot achieve that value. Consequently some
\(m\in\mathcal T\) satisfies
\[
 n\cdot m\ge A_0/T,\qquad
 \alpha^2:=\|n-m\|^2\le2(1-A_0/T).
 \tag{7}
\]
For \(\eta=0\), (7) gives \(n=m\). For positive \(\eta\le1/20\),
\[
 \alpha^2<2\eta/50\le1/500<1/400,
\]
so the **entire source sphere** has been reduced to \(\alpha<1/20\).
There is no source-nearness premise in this argument.

At \(e\), six representatives in \(C\) have \(c\cdot e=0\). They
generate a centered planar zonotope \(Z_0\subset e^\perp\). Its facet
normals are perpendicular to its nonzero generators; evaluating all six
projective tangent normals gives the sharp centered inradius
\[
 \rho^2=(288+464\phi)/5>14^2.
 \tag{8}
\]
The other signed generators sum exactly to
\[
 \sum_{c\cdot e\ne0}\operatorname{sign}(c\cdot e)c=A_0e.
\]
Because absolute value dominates either signed value, for every
\(n=ze+w\), \(w\perp e\),
\[
 A(n)\ge A_0z+h_{Z_0}(w)\ge A_0z+\rho\|w\|.
 \tag{9}
\]
This lower bound is global and makes no assumption on the changing
generator signs. Body symmetry transports it to every \(m\in\mathcal T\).

Use the \(m\) selected in (7), and write \(n=zm+w\). Since both normals
are unit,
\[
 z=1-\alpha^2/2,\qquad
 \|w\|=\alpha\sqrt{1-\alpha^2/4}.
\]
For \(0<\alpha<1/20\), the positive square-root factor is greater than
\(999/1000\). Combining (8)--(9) gives
\[
 A(n)-A_0\ge
 \alpha\left(\rho\sqrt{1-\alpha^2/4}-A_0\alpha/2\right)
 >\alpha\left(14\frac{999}{1000}-\frac{115/2}{40}\right)
 >12\alpha.
\]
This proves (1), including the separate \(\alpha=0\) case.

## 5. Any near-twofold receiver forces a near-twofold source

The area norm (4) has global Lipschitz constant at most half the surface
area:
\[
 L=\sum_{c\in C}\|c\|
   =10\sqrt3+60+6\sqrt{15+20\phi}<120.
 \tag{10}
\]
The upper bound follows with the positive branches from
\(\sqrt3<7/4\) and \(\sqrt{15+20\phi}<69/10\).

Suppose, toward a contradiction, that the strict placement in (2) exists.
Central symmetry removes its actual translation: for each centered source
point, convex midpoints of its two translated copies lie in the open
target. Removing \(\lambda\ge1\) by contraction toward the interior
origin gives \(B_1K\subset\operatorname{int}(B_2K)\). In particular,
\[
 A(n_1)<A(n_2)\le A_0+L\delta<A_0+120\delta,
\]
where \(n_i\) is the oriented row-cross-product kernel normal of \(B_i\).
The antipodal set \(\mathcal T\) handles either choice of directed normal.
Apply statement 2 with \(\eta=120\delta=1/250<1/20\). The source normal
is within \(\eta/12=1/3000\) of some member of \(\mathcal T\).

Choose independent proper body symmetries on the right of \(B_1,B_2\)
to carry the respective nearby normals to \(e\). This changes neither
projected body. The resulting normals satisfy
\[
 d_1:=\|n_1-e\|<1/3000,\qquad d_2:=\|n_2-e\|\le1/30000.
 \tag{11}
\]
This is a body-normal fold, not a claim that the original spatial rotation
is already small.

For each \(i\), take the proper shortest rotation \(H_i\) taking \(n_i\)
to \(e\), and set \(C_i=PH_i\), \(P(x,y,z)=(x,y)\). Its row normal
is \(n_i\), and
\[
 \|C_i-P\|_{op}\le\|H_i-I\|_{op}=d_i.
 \tag{12}
\]
Every positively oriented orthonormal frame with that normal differs
from \(C_i\) by a proper planar rotation. After one common planar
rotation, write the actual gauged frames as
\[
 B_1=R_\alpha C_1,\qquad B_2=C_2,
\]
retaining an **arbitrary** residual proper roll \(R_\alpha\).

## 6. Four equatorial originals force the proper residual roll

Put \(b=\phi^2\), \(c=2+\phi\). The four top-view equatorial originals
are exactly
\[
 q_+=(b,c),\quad q_-=(b,-c),\quad -q_+,\quad -q_-.
 \tag{13}
\]
All have norm \(R\). Every other original \(v\) has \(|v_z|\ge1\),
so \(\|Pv\|^2\le R^2-1\). These are checks on the entire original set,
not on a guessed moving silhouette.

For either \(q=q_+,q_-\), regarded as its actual height-zero original,
set \(s=B_1q\). By (11) and equal-radius projection,
\[
 \|s\|^2=R^2-(n_1\cdot q)^2\ge R^2(1-d_1^2).
\]
Containment supplies a supporting original \(v\) with
\(s\cdot B_2v\ge\|s\|^2\). Let \(p=Pv\). From (12),
\[
 \|s-p\|^2\le\|p\|^2-\|s\|^2+2R^2d_2.
 \tag{14}
\]
If \(v\) were not equatorial, its right side would be at most
\[
 R^2(d_1^2+2d_2)-1
 <25\frac{601}{9000000}-1<0,
\]
a contradiction. Hence \(p\) is one of the four points in (13). Using
\(d_1^2+2d_2<601/9000000\) and \(\sqrt{601}<25\), (14) gives
\[
 \|s-p\|<R\frac{25}{3000},\qquad
 \|R_\alpha q-p\|<R\frac{26}{3000}<1/20.
 \tag{15}
\]
Both matches are distinct: the original pair has distance \(2c>2\),
whereas twice the matching error is less than \(1/10\).

Here is the exact proper-isometry check, with no small-roll assumption.
Let \(p_+,p_-\) be the two matched target points. Their squared distance
can only be \(4b^2,4c^2\), or \(4R^2\), whereas the original squared
distance is \(4c^2\). If each matching error is \(<\epsilon=1/20\),
\[
 \left|\|p_+-p_-\|^2-4c^2\right|<8R\epsilon<2.
\]
The other two distance levels are separated by
\(4(c^2-b^2)>2\) and \(4b^2>2\); therefore the matched distance is
exactly \(4c^2\). The oriented original determinant is \(-2bc<0\).
Its matching error is at most \(2R\epsilon<1/2\), while changing its
sign would cost \(4bc>1/2\). Thus the target determinant is negative.
Enumerating the four points in (13), these two conditions leave exactly
\[
 (p_+,p_-)=(q_+,q_-)
 \quad\hbox{or}\quad
 (p_+,p_-)=(-q_+,-q_-).
\]
Equivalently there is one \(\sigma\in\{1,-1\}\) for both matches.

For a proper planar rotation, \(R_\alpha-\sigma I\) has the same
length ratio on every nonzero vector. Keeping the finer bound in (15),
\[
 \|R_\alpha-\sigma I\|_{op}<26/3000,
 \qquad
 \|\sigma B_1-P\|_{op}<27/3000=9/1000<1/100.
 \tag{16}
\]
Central symmetry ensures \(\sigma B_1K=B_1K\); \(\sigma I\) is also a
proper planar rotation. The target has
\(\|B_2-P\|_{op}\le1/30000<1/100\).

## 7. The published local criterion finishes the cap proof

The paired/singleton corollary cited in Section 1 says that no strict
RID containment occurs when **both full frames**, after independent
body symmetries, are within operator norm \(1/100\) of \(P\).
It allows arbitrary physical translation. Its normal-only premise is
insufficient by itself; (14)--(16) have supplied the missing roll control.

For completeness, the checker freshly verifies that corollary's finite
hypotheses. The eight projected doubleton classes are
\((\pm a,\pm1),(\pm1,\pm a)\), with heights \(\pm1\) and
\(a=\phi^3\); the four singletons are \((\pm b,\pm c)\), height zero.
Every one of their 700 outside-original radial support comparisons has
positive gap, with exact minimum one. At frame radius \(h=1/100\),
\[
 4R^2h+2R^2h^2<1,
\]
\[
 1-h^2>(a^2+1)h^2,
\]
\[
 (a^2b^2-c^2)^2(1-h^2)
 >(a^2+1)h^2(c^2-b^2)^2,
\]
and all quantities whose positive roots are compared have the required
strict signs. These are precisely the paired-height and positive
quadratic-stress conditions of the published theorem. The local argument
is reused, not presented as a new theorem here. Apply it to (16) and the
target frame to contradict the hypothetical strict placement. This proves
statement 3.

## 8. Scope, evidence, and remaining work

The prior global cutoff \(f(n)<83/200\), with
\(f(n)=\min_{v\in V}|v\cdot n|\), is not a proof premise here.
At every new cap center, \(f(n)=0\); in these caps,
\(f(n)\le R\delta<1/6000\). Thus this receiving exclusion covers
directions outside that earlier height band. It does not improve the
height-cutoff constant or resolve the full receiving complement.

Source and compact expected evidence are self-contained. The checker uses
Python 3.11+ integers and Fraction arithmetic in the positive embedding
of \(\mathbb Q(\phi)\). All 34220 facet triples, 465 area-vector pairs,
121 squared area values, 124 direct shadow areas, six tangent support
heights, sixty proper body symmetries, thirty minimum-axis images, two
proper pair survivors, and 700 local radial gaps are freshly regenerated.
No earlier computational corpus is imported. Integer and Fraction
representations cross-check all facet/original supports; the direct
shadow hull is a different area computation, not a second translation
of the same facet sum. Four malformed controls must reject with guards
active also under Python -O.

The continuum Cauchy, convex duality, tangent-coercivity, proper-frame,
and local cluster arguments are written mathematics, not formalized.
Python/Fraction semantics and correctness of the small exact checker
remain trust boundaries. Author replay and source publication are not
independent review. A killed, timed-out, or incomplete run establishes
no mathematical nonexistence. This proof uses no floating passage search,
solver verdict, private ledger, or external coordinate data.

Primary status sources checked in this fresh pass:
[Fredriksson](https://arxiv.org/html/2210.00601),
[Gosain--Grimmer](https://arxiv.org/html/2509.08190),
[Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1),
and [Zeng](https://arxiv.org/html/2604.26531).
They retain the standard RID as unresolved; the Noperthedron is a different
body. No exhaustive literature-absence or priority claim is made.

Next substantive frontier: replace the coarse radial roll estimate by
directional equatorial support bounds to enlarge these twofold caps, or
combine the independent area and diameter budgets on the remaining
receiving sphere. The global RID Rupert question remains open.
