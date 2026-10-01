# Exact shadow-area spectrum of the pentagonal hexecontahedron

Actual author **six-rupert-1**, role **researcher**, 2026-10-01.
This is an author-checked computer-assisted intermediate result, with a
complete finite reduction and exact arithmetic. It is not proof-assistant
formalized or independently reviewed. The full Rupert problem remains **OPEN**.

## 1. Body, motions and statement

Let \(\phi=(1+\sqrt5)/2\), and let \(x\) be the unique positive root of
\(x^3-2x-\phi=0\). Work first in the normalization \(K=K_{\rm original}/C_{19}\),
where

\[
C_{19}=\frac{\phi}{2}\sqrt{x(x+\phi)+1}.
\]

The named body is the standard pentagonal hexecontahedron in the
[exact named-solid model](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.py),
with the 92 literal vertices and 60 cyclic pentagonal facets in
[model.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_minimum_diameter/model.json).
Its identification with the McCooey coordinates, completeness of those
supporting facets, convex cyclic orders, polar equal edges and proper
body symmetries are the prerequisite lemma **8547**,
`bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi`, source
commit **86ab225fb8becbe66601a5da0b5b017e872e1833**.

For a definition independent of coordinate decimal values, set

\[
u=\phi(3-x^2),\quad r=5-\phi+2\phi x-3x^2,\quad
a=\frac{(14\phi-27)x^2+(10\phi-6)x+32-12\phi}{31},\quad
t=\frac{x^2-2}{\phi}=\frac1x.
\]

Let \(N=(1,0,\phi)\), let \([N]_\times\) denote cross product by \(N\),
and define

\[
G=\frac{\phi-1}{2}I_3+\frac{2-\phi}{2}NN^{\mathsf T}
  +\frac12[N]_\times,\qquad T=\operatorname{diag}(-1,-1,1),
\qquad \mathcal I=\langle G,T\rangle.
\]

This is the proper icosahedral group of order 60. Put

\[
W=\{(1,0,\phi),(-1,0,\phi),(\phi,1,0),(\phi,-1,0),
       (0,\phi,1),(0,\phi,-1)\},
\]

and let \(D\) consist of the eight points \((\pm1,\pm1,\pm1)\) and all
cyclic coordinate permutations of \((0,\pm1/\phi,\pm\phi)\), with signs
independent. Then

\[
K=\operatorname{conv}\big(\mathcal I\cdot(-u,-r,-1)
                     \ \cup\ a(\pm W)\ \cup\ tD\big).
\]

The three disjoint orbits have 60, 12 and 20 vertices. The origin is
strictly inside \(K\). Only the exact named algebraic parameters are used
here; no result is asserted on the earlier four-parameter box, whose
generic faces need not be coplanar pentagons.

For unit \(n\), write \(P_n=I_3-nn^{\mathsf T}\) and
\(A(n)=\operatorname{Area}(P_nK)\). A closed fit means

\[
\lambda P_n(RK)+b\subseteq P_nK,
\qquad R\in SO(3),\quad b\cdot n=0,\quad\lambda>0.
\tag{1}
\]

Strict containment in the receiver interior defines a passage fit.
Let \(\mu(K)\) be the supremum of strict fit scales. All source normals,
in-plane rolls and projected physical translations are allowed; central
symmetry of the body is not assumed. The statements also hold for the
other handed form by reflecting the entire configuration, conjugating
every proper relative motion by the same reflection. Copies remain
same-handed.

Index the literal facets from 0 to 59, and let \(b_i\) be their **outward
area vectors**, not just normal vectors. For a cyclic facet \(F_i\),

\[
b_i=\pm\frac12\sum_{(v,w)\text{ consecutive in }F_i}v\times w,
\qquad b_i\cdot v>0\quad(v\in F_i).
\]

Set

\[
v_*=b_0\times b_{58},\qquad
S_* =\frac12\sum_{i=0}^{59}|b_i\cdot v_*|,\qquad
A_{\min}=\frac{S_*}{\sqrt{v_*\cdot v_*}}.
\tag{2}
\]

At \(v_{38}=b_0\times b_{38}\), set

\[
c_{38}=\frac12\sum_{i\notin\{0,38\}}
       \operatorname{sgn}(b_i\cdot v_{38})b_i,\qquad
g_*=c_{38}+\frac12(b_0-b_{38}).
\tag{3}
\]

The checker proves \(g_*=\tau(1,-\phi,-1/\phi)\), \(\tau>0\), so that
\(A_{\max}=\|g_*\|=2\tau\). The exact finite assertions below establish:

1. Globally, \(A_{\min}\le A(n)\le A_{\max}\). Equality on the left
   occurs precisely at the 60 oriented normals
   \(\mathcal I\cdot(v_*/\|v_*\|)\), or 30 projective directions.
   These are generic directions with trivial oriented stabilizer in
   \(\mathcal I\), not rotation axes of the body. Equality on the right
   occurs precisely at the 30 oriented normals
   \(\mathcal I\cdot(1,-\phi,-1/\phi)/2\), the 15 twofold axes.
2. Minimum shadows have exactly 26 strict corners, and maximum shadows
   have exactly 20. A minimum shadow has no nonidentity proper planar
   isometry, even allowing translations.
3. At **every minimum-area receiver**, (1) with \(\lambda\ge1\) holds
   exactly when \(\lambda=1\), \(b=0\) and \(R\in\mathcal I\).
   Thus no strict unit-scale or larger passage uses such a receiver.
4. With \(U=\sqrt{A_{\max}/A_{\min}}\),

   \[
   1\le\mu(K)<U<1.012390033.
   \tag{4}
   \]

   The strict inequality \(\mu<U\) gives a qualitative positive gap
   below the exact ratio; it supplies no numerical value for that gap.

Outward rational enclosures, after undoing \(C_{19}\) normalization,
are

| Quantity | Strict lower bound | Strict upper bound |
|---|---:|---:|
| \(A_{\min}\), normalized | 3.105324990 | 3.105324991 |
| \(A_{\max}\), normalized | 3.182751853 | 3.182751854 |
| \(C_{19}^2A_{\min}\), original coordinates | 13.656085205 | 13.656085206 |
| \(C_{19}^2A_{\max}\), original coordinates | 13.996580274 | 13.996580275 |
| \(U\), independent of normalization | 1.012390032 | 1.012390033 |

The full exact coefficient triples for \(S_*^2\), \(v_*\cdot v_*\)
and \(A_{\max}^2\) are regenerated and compared with `expected.json`.
An entry `[[a0,b0],[a1,b1],[a2,b2]]` denotes
\((a_0+b_0\phi)+(a_1+b_1\phi)x+(a_2+b_2\phi)x^2\).
For example,

\[
A_{\max}^2=\frac{8676-80304\phi
 -(62968+163720\phi)x+(68184+103484\phi)x^2}{961}.
\]

## 2. Brightness zonotope and complete facet cover

For a generic direction, projected front facets tile the shadow and
projected back facets tile it again. Each facet contributes
\(|b_i\cdot n|\). Continuity treats exceptional directions. Thus Cauchy's
projection formula gives

\[
A(n)=\frac12\sum_i|b_i\cdot n|=h_Z(n),\qquad
Z=\sum_i[-b_i/2,b_i/2].
\tag{5}
\]

Here central symmetry belongs to \(Z\), not necessarily to \(K\).
The checker verifies that the area generators span three-space, that
they are distinct, and that they constitute one \(\mathcal I\)-orbit.
Consequently \(Z\) is a full-dimensional centered zonotope invariant
under \(\mathcal I\).

At any nonzero normal \(v\), its exposed face is exactly

\[
F(v)=c(v)+\sum_{i:b_i\cdot v=0}[-b_i/2,b_i/2],\qquad
c(v)=\frac12\sum_{i:b_i\cdot v\ne0}
                   \operatorname{sgn}(b_i\cdot v)b_i.
\tag{6}
\]

The exposed face is a facet precisely when the zero generators span a
plane. Every facet therefore has two independent zero generators, and
their cross product is its normal. Conversely every independent pair
gives a facet, because all zero generators lie in the perpendicular
plane and already span it.

Given any pair \((b_i,b_j)\), a proper body symmetry sends \(b_i\) to
\(b_0\). The other generator becomes one of \(b_1,\ldots,b_{59}\).
An orthogonal proper map sends the pair's cross product to the cross
product of its images. Hence the **59 charts**

\[
v_j=b_0\times b_j,\qquad 1\le j\le59,
\tag{7}
\]

together with proper symmetry images and normal reversal cover every
facet of \(Z\). This reduction covers all 1,770 unordered pairs; it
does not sample the sphere. Every chart is nondegenerate. The exact
zero sets have size two in 53 charts and size three in six charts.

The checker also constructs the exact 60-element generator-permutation
group. Symmetry images of zero sets give 1,590 planes with two zero
generators and 60 planes with three: 1,650 unoriented planes or 3,300
oriented facets. A zero set identifies a unique plane because it contains
two independent generators; this deduplication cannot merge different
facet planes. The consistency count is \(1590+3\cdot60=1770\).

## 3. Global minimum and complete equality normals

The centered inradius of a full-dimensional polytope is the least
distance of its facet planes from the origin. From (5)--(7), these
distances are

\[
d_j=\frac{S_j}{\sqrt{v_j\cdot v_j}},\qquad
S_j=\frac12\sum_i|b_i\cdot v_j|.
\]

All \(S_j>0\). Comparing squared distances uses only exact field signs:

\[
S_j^2(v_*\cdot v_*)-S_*^2(v_j\cdot v_j)\ge0.
\tag{8}
\]

The checker verifies every comparison, with equality precisely for
\(j=58\). Thus the centered inradius of \(Z\) is (2). Since its ball
of that radius lies in \(Z\), its unit support function is globally
at least this radius, and the chart attaining it gives the claimed
global minimum of (5).

This also proves completeness of the equality directions. If
\(h_Z(n)=A_{\min}\), the ball point \(A_{\min}n\) belongs to both
\(Z\) and a supporting plane, hence is on its boundary. It belongs
to some facet with outward unit normal \(m\) and distance \(d\ge A_{\min}\).
Then

\[
d=m\cdot(A_{\min}n)\le A_{\min}.
\]

Equality forces \(d=A_{\min}\) and \(m=n\). Thus no intervening
normal can minimize the support. Exact symmetry enumeration gives
30 unoriented minimum planes and 60 oriented normals, with the negatives
also in the same proper orbit. Orbit size 60 gives trivial oriented
stabilizer, establishing their generic character.

## 4. Global maximum and complete equality normals

For any compact \(Z\),

\[
\max_{\|n\|=1}h_Z(n)=\max_{z\in Z}\|z\|.
\tag{9}
\]

A convex norm attains a polytope maximum at a vertex. Every vertex is
on a facet. By (6), every vertex of a chart facet belongs to the finite
set

\[
c(v_j)+\frac12\sum_{i:b_i\cdot v_j=0}\epsilon_i b_i,
\qquad \epsilon_i\in\{-1,1\}.
\tag{10}
\]

Indeed the entire facet is the affine image of the corresponding cube,
and the vertices of an image polytope are among images of cube vertices.
There are \(53\cdot4+6\cdot8=260\) images to test. For a three-generator
facet, its eight cube images can include points inside its hexagon;
they are not all asserted to be vertices. Every image still belongs
to \(Z\), and the set contains every needed vertex. Testing them and
their symmetry images is therefore a complete upper and lower bound.

The checker verifies the exact nonnegativity of
\(\|g_*\|^2-\|z\|^2\) for all 260 images. All tied images belong to
the exact proper orbit of \(g_*\); the seed itself occurs at chart 38,
signs \((1,-1)\). This proves (9) equals \(\|g_*\|\).

For completeness, if \(h_Z(n)=\|g_*\|\), a point achieving that
support satisfies \(n\cdot z=\|g_*\|\) and \(\|z\|\le\|g_*\|\),
so \(z=\|g_*\|n\) and \(\|z\|=\|g_*\|\). Such a point must be
a vertex: a proper convex combination of two distinct points on or
inside this sphere has strictly smaller norm. All maximum normals
are therefore the normalized maximum vectors already covered above.
The exact orbit has 30 vectors, including negatives, and its seed
is \(\tau(1,-\phi,-1/\phi)\). The corresponding unit vector is
\((1,-\phi,-1/\phi)/2\), since its squared unnormalized norm is 4.
The oriented stabilizer has order two, so these are body half-turn axes.

## 5. Exact shadow polygons and their proper isometries

The small certificate `polygons.json` gives cyclic **literal vertex
indices**, with no floating coordinates. The minimum normal is \(v_*\),
and the maximum normal is \(q=(1,-\phi,-1/\phi)\). For every consecutive
edge \(e=V_j-V_i\), the checker verifies

\[
\|e\|^2\|v\|^2-(e\cdot v)^2>0,\qquad
 (e\times v)\cdot V_i>0,
\]

and all 92 original support inequalities

\[
(e\times v)\cdot(V_i-V_k)\ge0.
\tag{11}
\]

Each other declared corner has strict inequality. Each successive
turn has \(v\cdot(e_{\rm previous}\times e)>0\).
These are determinant and halfplane statements in the actual projected
plane: \(e\times v\in v^\perp\), and dot products with that probe
are unaffected by orthogonal projection. The edge lengths and turns
are likewise those of the projected edges up to positive normal factors.

Thus the listed cycles are strictly convex, contain all projected
original vertices, and have all listed corners in the original shadow.
They are exactly the full shadows, with respectively **26** and **20**
strict corners. The two cycles require 2,392 and 1,840 support checks;
58 and 40 are exact contact equalities. Additional original vertices
on a minimum-shadow edge are retained: two source facets collapse into
boundary segments. No singleton-support assumption is made on those
segments.

As a consistency check, the projected shoelace area is verified exactly:
the minimum cycle's area vector dotted with \(v_*\) equals \(S_*\);
the maximum cycle's area vector dotted with \(q\) equals \(4\tau\).
Dividing by normal length gives (2) and \(2\tau\).

The minimum shadow's edge from literal vertex **80 to 44** has a length
different from every other one of its 25 edges. The comparison uses
the exact projected squared-length numerator
\(\|e\|^2\|v_*\|^2-(e\cdot v_*)^2\); the common denominator
\(\|v_*\|^2\) is positive. A proper planar isometry preserving this
polygon must send its unique-length edge to itself and preserve its
counterclockwise boundary orientation. It consequently fixes both
ordered endpoints. A proper planar isometry fixing two distinct points
is the identity. This treats translations as well as rotations and
does not presume any central symmetry or centroid position.

The proper body orbits in Sections 3--4 carry these polygon facts to
every extremizing direction.

## 6. All closed minimum-receiver fits

Suppose the receiver is a minimum shadow and (1) holds with
\(\lambda\ge1\). Area comparison gives

\[
\lambda^2 A(R^{\mathsf T}n)\le A(n)=A_{\min}.
\]

Since \(A(R^{\mathsf T}n)\ge A_{\min}>0\), this forces
\(\lambda=1\) and a minimum source normal. Closed containment between
full-dimensional convex polygons of equal area implies equality:
a proper closed convex subset omits a region of positive area.

Fold the receiver by a proper body symmetry to the seed normal
\(n_*=v_*/\|v_*\|\). Every oriented minimum source normal is in the
same proper orbit, including reversals. Choose \(M\in\mathcal I\)
with \(Mn_*=R^{\mathsf T}n_*\). Then \(U_0=RM\) fixes \(n_*\),
and \(U_0K=RK\). Its restriction to \(n_*^\perp\) is a proper
planar rotation. The equality of shadows says

\[
U_0(P_{n_*}K)+b=P_{n_*}K.
\]

Section 5 forces this planar isometry to be the identity, so \(b=0\)
and \(U_0\) fixes the entire plane as well as its normal. Therefore
\(U_0=I_3\) and \(R=M^{-1}\in\mathcal I\).
Undoing the receiver fold preserves this conclusion. Conversely every
proper body symmetry, unit scale and zero projected translation gives
a closed equality fit. This proves statement 3 with arbitrary source,
roll and translation.

## 7. Passage ceiling and strict supremum refinement

Every closed fit satisfies

\[
\lambda^2 A_{\min}\le\lambda^2 A(R^{\mathsf T}n)
                     \le A(n)\le A_{\max}.
\tag{12}
\]

Thus \(\lambda\le U\), and every strict fit has \(\lambda<U\).
Strictness alone would yield only \(\mu\le U\); proving \(\mu<U\)
requires the following compactness and shape argument.

Closed fits with scales in \([1,U]\) form a nonempty compact parameter
set. The normal and relative motion range over compact \(S^2\) and
\(SO(3)\). Since the origin is in the source, its translated projection
\(b\) belongs to the receiver; \(K\) is bounded, so these translations
are uniformly bounded. The condition \(b\cdot n=0\) is closed.
The finite projected hulls vary continuously in Hausdorff distance, so
closed containment persists under parameter limits. The identity unit
fit establishes nonemptiness. Hence a largest closed scale \(\Lambda\)
is attained; (12) shows this is the unrestricted largest closed scale.

If \(\Lambda=U\), equality is forced throughout (12). The source
shadow has minimum area, the receiver has maximum area, and the
scaled translated shadows coincide. An invertible planar similarity
preserves strict corner count. Such an equality would identify a
26-corner polygon with a 20-corner polygon, which is impossible.
Therefore \(\Lambda<U\).

Finally \(\mu=\Lambda\). Any strict fit is closed. Conversely, a
source shadow has the origin in its interior. Shrinking any positive
closed source scale slightly about that origin, keeping the same
translation, places it strictly inside its old source polygon and
therefore strictly inside the receiver. Strict scales approach every
closed scale, including \(\Lambda\). Identity fits yield all strict
scales below one, giving \(\mu\ge1\). This proves (4).

This compactness/nonattainment argument is credited to the campaign's
[independent J74 refinement](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/j74-projection-audit/REVIEW.md),
graph review **8635**, actual author **six-reviewer-4**. Its review verdict
concerns J74 and does not audit the present pentagonal result.

## 8. Arithmetic, completeness and limits

All scalar algebra takes place in
\(\mathbb Q(\phi)[x]/(\phi^2-\phi-1,x^3-2x-\phi)\), using exact
`Fraction` coefficients and the positive root embedding. Nonzero signs
are decided by outward rational intervals; exact coefficient zero is
handled first. An interval containing zero for a nonzero expression
raises an error and gives no completed claim. The root is enclosed by
90 rational bisections on \([17/10,18/10]\), where the cubic is strictly
increasing. Positive square roots use integer square-root enclosures;
there are **zero floating-point proof decisions**.

The checker reconstructs all named parameters, 92 vertices, 60 area
vectors, proper matrices and generator permutations. The three imported
small named-model files have fixed SHA256 hashes, reported in
`expected.json`. Their geometry is a cited mathematical prerequisite;
this checker does not claim a new independent audit of that prerequisite.
All new signs, extrema comparisons, orbit equality sets and polygon
support/length gates are replayed completely in both Python modes.
Six damaged polygon witnesses must fail even under `python -O`.
No proof-critical `assert` is used.

Exploratory floating calculations suggested the two extremizer seeds
and the two cycles. Neither their accuracy nor absence of a found
passage is used as proof. Equations (6)--(10) and their complete exact
comparisons replace that exploratory evidence. Interrupted enumeration,
timeout or memory failure establishes no global statement. A private
progress file, if requested, remains explicitly incomplete until all
checks and the expected-record comparison pass.

This result improves the old diameter-based scale ceiling below
1.054495196 to (4). It does not prove a passage above unit scale,
non-Rupertness, any positive receiving cap around the generic area
minima, or a quantified further gap below \(U\). In particular the
two collapsed facet segments require additional care in any later
local contact argument.

## 9. Literature and methodological provenance

Current primary sources checked on 2026-10-01 include
[Fredriksson](https://arxiv.org/html/2210.00601),
[Gosain--Grimmer, Section 3.3 and Table 3](https://arxiv.org/html/2509.08190),
[Zeng, Section 1.2](https://arxiv.org/html/2604.26531), and
[Steininger--Yurkevich](https://arxiv.org/html/2508.18475).
They retain the located unresolved pentagonal hexecontahedron frontier;
search failure for a passage is not a non-Rupert proof.
The literal coordinate source is
[McCooey's table](https://dmccooey.com/polyhedra/LpentagonalHexecontahedron.txt),
already algebraically identified in the prerequisite. No live web
response is a replay input.

Cauchy's projection formula and zonotope/polytope facts are standard.
The campaign's
[J74 brightness computation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/PROOF.md),
graph **8551**, actual author **six-rupert-2**, and
[RID brightness cover](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
graph **8555**, actual author **six-rupert-3**, are credited method precedents.
Their numerical constants, body symmetry assumptions and excluded caps
are not imported into this chiral Catalan. The strict-supremum method
is credited separately in Section 7. Bounded primary and committed-source
searches did not locate these pentagonal constants or equality sets;
no historical priority claim is made.
