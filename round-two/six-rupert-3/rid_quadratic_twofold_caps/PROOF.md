# Quadratic equatorial transport enlarges the RID receiving caps

**six-rupert-3, researcher; 2026-10-01.** Author-checked written geometric
proof with an exact finite-hypothesis checker. Unformalized; independent
review and historical priority are not asserted. The standard
rhombicosidodecahedron's global Rupert property remains unresolved.

## 1. Body, dependencies and conclusions

Let \(\phi=(1+\sqrt5)/2\), let \(V\) be all even coordinate permutations
and independent signs of
\[
 (1,1,\phi^3),\qquad(\phi^2,\phi,2\phi),\qquad(2+\phi,0,\phi^2),
\]
and set \(K=\operatorname{conv}V\). This is the standard **edge-two** RID;
\(K=-K\), with sixty original vertices of squared radius
\(R^2=7+8\phi<20\). For unit \(n\), put
\[
 P_n=I-nn^t,\quad A(n)=\operatorname{Area}(P_nK),\quad A_0=12+28\phi.
\]
Let \(e=(0,0,1)\), and let \(\mathcal T\) be its directed orbit under
the sixty-element proper body rotation group. It has thirty members,
or fifteen unoriented twofold axes. All normal distances below are
Euclidean **unit-normal chord distances**. For an orthonormal-row frame
\(B\) with unit kernel normal \(n\), \(\operatorname{Area}(BK)=A(n)\):
the frame identifies the physical projection plane isometrically with
\(\mathbb R^2\).

The [prior RID brightness proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
graph `bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`,
established the minimum area, complete polar spectrum and a receiving
radius \(1/30000\). Its continuum Cauchy and polar method credits
[six-rupert-2's J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md).
The final local argument here is the **general** paired/singleton theorem
in Section 2 of the published
[mirror-cluster proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md).
Those results are dependencies, rather than new claims here. In particular,
we recheck that general theorem at a larger frame radius; we do not change
the earlier specialization's radius or source.

**Theorem.**

1. If \(0<\eta\le1/15\) and \(A(n)\le A_0+\eta\), then
   \(\operatorname{dist}(n,\mathcal T)<\eta/12\).
2. For arbitrary real \(2\)-by-\(3\) orthonormal-row frames \(B_1,B_2\),
   any receiving unit kernel normal \(n_2\) satisfying
   \(\operatorname{dist}(n_2,\mathcal T)\le1/270\), any physical
   \(t\in\mathbb R^2\), and any \(\lambda\ge1\),
   \[
    \lambda B_1K+t\not\subset\operatorname{int}(B_2K).
    \tag{1}
   \]
3. Any strict passage at any receiver normal must have
   \[
    A(n_2)>A_0+2/45.                                      \tag{2}
   \]

There is no source-orientation or residual-roll restriction in (1).
Every original placement obtained using \(SO(3)\) is included, and the
proof retains arbitrary proper planar roll. It gives no classification of
touching closed placements and no conclusion for the receiving complement.
The new chord radius is \(1000/9\) times the preceding one.

For the **unit-edge** RID, areas divide by four, so the minimum is
\(a_0=3+7\phi=(13+7\sqrt5)/2\), statement 1 becomes
\[
 0<\eta\le1/60,\quad A_{\rm unit}(n)\le a_0+\eta
       \ Longrightarrow\ \operatorname{dist}(n,\mathcal T)<\eta/3,
 \tag{3}
\]
and statement 3 becomes \(A_{\rm unit}(n_2)>a_0+1/90\).
The chord radius itself does not depend on the edge normalization.

## 2. Exact tangent upper bound and a local area formula

The dependency reconstructs all 62 original facets, with physical area
vectors in opposite pairs. Let \(C\) be its 31 representatives. Cauchy's
formula, proved there, is
\[
 A(n)=\sum_{c\in C}|c\cdot n|=h_Z(n),\qquad
 Z=\sum_{c\in C}[-c,c].                                  \tag{4}
\]
At \(e\), define
\[
 D=\{c\in C:c\cdot e=0\},\quad Z_0=\sum_{c\in D}[-c,c],
 \qquad E=C\setminus D.
\]
There are six generators in \(D\), twenty-five in \(E\), and the exact
signed sum is
\[
 \sum_{c\in E}\operatorname{sign}(c\cdot e)c=A_0e.          \tag{5}
\]
The new checker enumerates all \(2^6=64\) endpoint sums of \(Z_0\),
and verifies
\[
 M^2:=\max_{x\in Z_0}\|x\|^2=96+128\phi<(35/2)^2.         \tag{6}
\]
The maximum occurs at exactly four endpoint sums,
\((\pm(4+8\phi),\pm4,0)\). To justify completeness, the Minkowski sum
of the six segments is the convex hull of all their endpoint sums, and
convexity of the Euclidean norm bounds every convex combination by their
maximum norm. Thus no face-interior point can exceed the enumerated values.

The checker also verifies the exact sign-stability threshold
\[
 \min_{c\in E}\frac{(c\cdot e)^2}{\|c\|^2}
       =\frac{2-\phi}{4}>1/16.                            \tag{7}
\]
For a unit \(n\) with \(d=\|n-e\|\le1/4\), Cauchy--Schwarz and (7)
give \(|c\cdot(n-e)|<|c\cdot e|\) for every \(c\in E\).
Their signs therefore remain fixed. Write \(n=ze+w\), \(w\perp e\).
Equations (4)--(5) give the exact formula
\[
 A(n)=A_0z+h_{Z_0}(w),\qquad
 z=1-d^2/2,\quad \|w\|=d\sqrt{1-d^2/4}.                 \tag{8}
\]
In particular,
\[
 A(n)-A_0\le M d\sqrt{1-d^2/4}-A_0d^2/2\le M d.         \tag{9}
\]
For \(d>0\), this is strictly below \((35/2)d\); at \(d=0\), the
excess is zero. Symmetry gives (8)--(9) at every \(m\in\mathcal T\).
For unit edge, \(M^2/16=6+8\phi\) and the slope is below \(35/8\).
These constants can be used independently of the passage exclusion.

## 3. Extend the global source area budget

The dependency exhausts all 121 projective facet normals of \(Z\), and
proves that the polar vertices of largest norm are exactly \(m/A_0\),
\(m\in\mathcal T\). Every other polar vertex has norm at most \(1/A_1\),
where \(A_1^2=940+1520\phi\). It also proves the tangent inradius
\(\rho^2=(288+464\phi)/5>14^2\) and the **global** lower bound
\[
 A(zm+w)\ge A_0z+\rho\|w\|,\qquad w\perp m.             \tag{10}
\]
This does not require the signs in (7) to remain fixed.

Let \(A(n)\le T=A_0+\eta\), \(0<\eta\le1/15\). Homogeneity gives
\(n/T\in Z^\circ\). A polar vertex maximizing \(x\mapsto n\cdot x\)
has value at least \(1/T\). The exact bounds
\[
 50<A_0<115/2,\qquad T<58<A_1
\]
exclude every nonminimum vertex from achieving that value. Some
\(m\in\mathcal T\) therefore satisfies
\[
 n\cdot m\ge A_0/T,\quad
 \alpha^2:=\|n-m\|^2\le2(1-A_0/T)<2\eta/50
       \le1/375<1/256.                                  \tag{11}
\]
Thus \(\alpha<1/16\). If \(\alpha=0\), statement 1 holds immediately.
Otherwise, substitute \(z=1-\alpha^2/2\),
\(\|w\|=\alpha\sqrt{1-\alpha^2/4}\) into (10):
\[
 A(n)-A_0\ge
 \alpha\left(\rho\sqrt{1-\alpha^2/4}-A_0\alpha/2\right)
 >\alpha\left(14\frac{999}{1000}-\frac{115}{64}\right)
 >12\alpha.                                             \tag{12}
\]
The positive-root comparison uses
\((999/1000)^2<1-1/1024\). This proves statement 1 globally on the
source sphere and extends the dependency's smaller \(1/20\) budget.

## 4. A shortest rotation has quadratic equatorial drift

This bridge is valid for any body. Let \(n=(x,y,z)\) be a unit normal
with \(z>0\), let \(d=\|n-e\|\), and write \(u=(x,y)\). The proper
shortest rotation taking \(n\) to \(e\) is
\[
 H_n=\begin{pmatrix}
 1-x^2/(1+z)&-xy/(1+z)&-x\\
 -xy/(1+z)&1-y^2/(1+z)&-y\\
 x&y&z
 \end{pmatrix},\qquad C_n=PH_n,
 \quad P(x,y,z)=(x,y).                                   \tag{13}
\]
Direct multiplication using \(x^2+y^2+z^2=1\) proves orthogonality
and \(H_nn=e\). Its determinant is positive by continuity on the upper
hemisphere and equals one at \(e\). It fixes the direction perpendicular
to \(u\) in \(e^\perp\), and acts in the complementary plane as the
rotation of angle \(\arccos z\) carrying \(n\) to \(e\), so it is the
shortest proper rotation. The formula covers \(n=e\) as well.

The usual full-frame estimate is \(\|C_n-P\|_{op}\le d\). On the
original height-zero plane, however, (13) gives
\[
 C_n|_{e^\perp}=I-\frac{u u^t}{1+z},\qquad
 \left\|C_n|_{e^\perp}-I\right\|_{op}
      =\frac{\|u\|^2}{1+z}=1-z=d^2/2.                    \tag{14}
\]
The identity also holds for \(u=0\). Thus every equatorial original
\(q\) obeys
\(\|C_nq-Pq\|\le\|q\|d^2/2\).
This is a quantified algebraic identity, not an inference from sampled
rotations. The checker's four exact transport controls only guard the
implementation of the displayed formula.

## 5. Arbitrary containment forces the proper roll into the local criterion

Set
\[
 \delta=1/270,\quad \eta_*=(35/2)\delta=7/108<1/15,
 \quad u_*:=\eta_*/12=7/1296,\quad h=1/81.                \tag{15}
\]
Suppose a strict placement as in (1) exists. Central symmetry removes
its physical translation: both \(x+t\) and \(x-t\) are in the open
target for each centered source point, hence so is their midpoint.
Contraction toward the interior origin removes \(\lambda\ge1\).
Consequently \(B_1K\subset\operatorname{int}(B_2K)\), and
\[
 A(n_1)<A(n_2)<A_0+\eta_*.
\]
The receiver bound follows from (9), including the zero-chord case.
Statement 1 then places the source within \(u_*\) of some minimum axis.
Independently folding the two frames by proper body symmetries leaves
their projected bodies unchanged and yields
\[
 d_1:=\|n_1-e\|<u_*,\qquad d_2:=\|n_2-e\|\le\delta.     \tag{16}
\]
Their row-cross-product normals are near \(e\). Every orthonormal-row
frame with such a normal is a **proper** planar rotation of (13).
After a common planar rotation, the actual frames can therefore be
written
\[
 B_1=R_\alpha C_{n_1},\qquad B_2=C_{n_2},\qquad
 R_\alpha\in SO(2).                                      \tag{17}
\]
No initial restriction on \(R_\alpha\) has been imposed.

Put \(b=\phi^2\), \(c=2+\phi\). The exact height-zero originals are
\[
 q_+=(b,c,0),\quad q_-=(b,-c,0),\quad -q_+,\quad -q_-.
 \tag{18}
\]
Each has norm \(R\). All other originals have \(|v_z|\ge1\), hence
\(\|Pv\|^2\le R^2-1\). These facts concern all sixty original vertices,
not an assumed silhouette vertex list.

For \(q=q_+\) or \(q_-\), let \(s=B_1q\). Equal original radii give
\[
 \|s\|^2=R^2-(n_1\cdot q)^2\ge R^2(1-d_1^2)>0.
\]
Containment supplies a maximizing target original \(v\) such that
\(s\cdot B_2v\ge\|s\|^2\). Put \(p=Pv\). First use the full-frame
drift \(\|B_2v-p\|\le R d_2\) to obtain
\[
 \|s-p\|^2\le\|p\|^2-\|s\|^2+2R^2d_2.               \tag{19}
\]
For a nonequatorial \(v\), the right side is at most
\(R^2(d_1^2+2d_2)-1\), which is negative because the checker verifies
\[
 (7+8\phi)(u_*^2+2\delta)<1.                            \tag{20}
\]
Thus every chosen maximizing \(v\) is one of (18).

Now apply the stronger drift (14) to that **actual** equatorial target
original: \(\|B_2v-p\|\le R d_2^2/2\). Repeating (19) gives
\[
 \|s-p\|^2\le R^2(d_1^2+d_2^2).
\]
Also (14) on the source original gives
\(\|R_\alpha Pq-s\|\le R d_1^2/2\). Hence
\[
 \|R_\alpha Pq-p\|
 \le R\left(\sqrt{d_1^2+d_2^2}+d_1^2/2\right)
 <R\left(1/150+u_*^2/2\right)<1/20.                     \tag{21}
\]
The exact positive-root gate is \(u_*^2+\delta^2<(1/150)^2\);
the last inequality uses \(R<5\).

For clarity, the proper pair-matching step is retained explicitly.
The two matched target points \(p_+,p_-\) are distinct, since
\(\|Pq_+-Pq_-\|=2c>2\) while twice the matching error is below \(1/10\).
Their squared distance belongs to
\(\{4b^2,4c^2,4R^2\}\). With \(\epsilon=1/20\), its difference
from the original \(4c^2\) is below \(8R\epsilon<2\). The other
levels have gaps \(4(c^2-b^2)>2\) and \(4b^2>2\), so the matched
distance is \(4c^2\). Such pairs have determinant \(\pm2bc\).
The determinant differs from
\(\det(R_\alpha Pq_+,R_\alpha Pq_-)=-2bc\) by less than
\(2R\epsilon<1/2\). Since \(4bc>1/2\), its sign is negative.
Exact enumeration of the four points then leaves only
\[
 (p_+,p_-)=(Pq_+,Pq_-)\quad\hbox{or}\quad(-Pq_+,-Pq_-).
\]
Both matches share one sign \(\sigma\in\{1,-1\}\).

For a proper planar rotation, \(R_\alpha-\sigma I\) has the same
length ratio on all nonzero vectors. The finer estimate in (21) yields
\[
 \|R_\alpha-\sigma I\|_{op}<1/150+u_*^2/2,
\]
\[
 \|\sigma B_1-P\|_{op}
   <u_*+1/150+u_*^2/2
   =\frac{1014697}{83980800}<1/81,
 \qquad \|B_2-P\|_{op}\le1/270<1/81.                    \tag{22}
\]
Central symmetry gives \(\sigma B_1K=B_1K\), and \(\sigma I\)
itself is a proper planar rotation. Equation (22) has derived full-frame
alignment from an arbitrary source and arbitrary proper residual roll.

## 6. Recheck the general local theorem at frame radius 1/81

Use \(a=\phi^3\), \(b=\phi^2\), \(c=2+\phi\), paired heights
\(\pm1\), and singleton height zero. The checker freshly evaluates all
700 original radial support gaps for the twelve selected projected
classes; their minimum remains exactly one. The squared common-radius
and parameter-sign identities of the general paired/singleton theorem
are checked again.

At \(h=1/81\), its support condition holds because
\[
 4R^2h+2R^2h^2<80h+40h^2=6520/6561<1.                    \tag{23}
\]
Its other two conditions are checked with exact positive signs before
squaring:
\[
 1-h^2>(a^2+1)h^2,
\]
\[
 (a^2b^2-c^2)^2(1-h^2)>
       (a^2+1)h^2(c^2-b^2)^2,
 \qquad a^2b^2-c^2>0.
 \tag{24}
\]
Thus the published **general** local theorem applies to (22) and
contradicts the strict containment. This proves statement 2. It does
not assert that an enlarged corollary had already been published.

If a hypothetical passage receiver has \(A(n_2)\le A_0+2/45\),
statement 1 applied to that receiver with \(\eta=2/45\le1/15\)
gives \(\operatorname{dist}(n_2,\mathcal T)<1/270\).
Statement 2 excludes it. This proves statement 3.

## 7. Reproduction, transfer constants and remaining frontier

[check.py](check.py) verifies the hashes in [DEPENDENCIES.json](DEPENDENCIES.json)
before importing the previously published arithmetic and verifier. It
first regenerates every byte of the prior 4452-byte expected record,
including the complete original hull, polar spectrum, proper group and
independent projected-hull area checks. It then freshly reconstructs the
physical facet vectors to check (5)--(7), enumerates all 64 tangent
endpoint sums, checks (11)--(12), (20)--(24), and regenerates
[expected.json](expected.json). The four additional negative controls
must reject an incomplete generator list, rescaled physical area
vectors, a receiving radius outside the certified budget, and frame
radius \(1/80\), whose support bound fails. All guards remain active
under Python -O. Failure of one of these tests is a rejected certificate,
not a nonexistence conclusion at the rejected parameter.

For collaborators, the unit-edge constants are: tangent inradius
\(\rho/4>7/2\); tangent circumradius squared \(6+8\phi\), below
\((35/8)^2\); exact local area formula for chord at most \(1/4\);
global source budget (3); all-source receiving chord \(1/270\); and
global receiving-area gap \(1/90\). At any positive receiver cap radius
\(\delta\le1/4\), (9) gives
\(A_{\rm unit}(n)<a_0+(35/8)\delta\), including its center.
A different body's agreement with a RID receiving shadow alone is
insufficient for transfer: a passage source must independently be proved
to lie in the common-shadow region, with proper motions and translations
retained. No Johnson-solid assertion is made here.

These twofold caps meet the region where an original vertex has zero
axial height. They supplement the earlier global RID receiving-height
cutoff and do not alter it. The global named-solid question is still open
in the primary status literature:
[Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1)
and [Zeng](https://arxiv.org/html/2604.26531). The area/polar mechanism and
general mirror-cluster theorem are credited dependencies; the new pieces
are the exact tangent upper and sign constants, extended budget,
quadratic equatorial roll reduction, and its resulting larger exclusion.
No exhaustive literature-absence or historical-priority claim is made.

The written continuum bridges remain unformalized. Python/Fraction
semantics, the hash-pinned dependency and the checker remain explicit
trust boundaries. The next substantive RID frontier is exclusion away
from the minimum-area axes, using joint area and original-vertex support
constraints rather than further small improvements of this cap constant.
