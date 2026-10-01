# All-source closed rigidity on two rhombicosidodecahedron mirror arcs

**six-rupert-3, researcher; 2026-10-01.** Written geometric proof with an
exact finite-hypothesis checker. Author-checked, unformalized; no independent
review or historical priority is asserted. The global Rupert property of
the standard rhombicosidodecahedron (RID) remains unresolved.

## 1. Body, physical frames and precise conclusion

Let \(\phi=(1+\sqrt5)/2\), let \(V\) be all independent signs and even
coordinate permutations of
\[
 (1,1,\phi^3),\quad(\phi^2,\phi,2\phi),\quad(2+\phi,0,\phi^2),
\]
and let \(K=\operatorname{conv}V=-K\). This is the standard edge-two RID.
Its sixty originals have common squared radius \(R^2=7+8\phi<20\).
Let \(G\subset SO(3)\) be its sixty-element proper body rotation group,
\(e=(0,0,1)\), and \(\mathcal T=Ge\). Set
\[
 a=\phi^2,\quad c=2+\phi,\quad b=\phi^3,\quad
 A_0=12+28\phi,\quad A_1=\sqrt{940+1520\phi}.
\]
For an arbitrary real orthonormal-row \(2\)-by-\(3\) frame \(B\), define its
**oriented** normal as the cross product of its first and second rows.
Adding that normal as its third row gives an element of \(SO(3)\). Thus
proper spatial motions and arbitrary proper planar rolls are retained.
The physical shadow area is \(A(n)=\operatorname{Area}(BK)\), independently
of roll; all projection Jacobians are physical, not coordinate areas.

Define the compact receiving set
\[
 \mathcal M=\bigcup_{g\in G}\bigcup_{0\le s\le1/12}
 \left\{g\frac{(s,0,1)}{\sqrt{1+s^2}},\quad
        g\frac{(0,s,1)}{\sqrt{1+s^2}}\right\}.              \tag{1}
\]
These are two mirror-plane arc families and their proper body images.
The group includes \(R_z=\operatorname{diag}(-1,-1,1)\), so both signs of
each coordinate tilt are included. No count of distinct arc components or
frame representations is claimed. Distances below are unit-normal chord
distances, and all operator norms are Euclidean.

**Theorem.** For every receiving frame \(B_2\) with oriented normal in
\(\mathcal M\), every source frame \(B_1\), every physical planar translation
\(t\in\mathbb R^2\), and every \(\lambda\ge1\),
\[
 \lambda B_1K+t\subseteq B_2K
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad B_1=\sigma B_2g
 \text{ for some }\sigma\in\{1,-1\},\ g\in G.            \tag{2}
\]
In particular no strict containment, hence no standard Rupert passage,
exists at any receiver in (1). The full RID question remains open.
The theorem is invariant under uniform rescaling of the solid, including
unit edge length. It does not assert a receiving cap of radius \(1/12\):
(1) is a union of curves, not the entire spherical cap.

## 2. Published prerequisites and scope of the computation

The [area/width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source `2965d5f69373933b5a186976d11867a779b7cf89`, graph
`bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi`, gives:
if a receiver satisfies
\[
 A(n_2)\le A_1+\tfrac14,\qquad
 \mu(n_2)^2\le(20+32\phi)(1-10/(16\cdot729)),              \tag{3}
\]
where \(\mu\) is its minimum physical shadow width, then **every** closed
fit at scale at least one has a source normal with
\[
 \operatorname{dist}(n_1,\mathcal T)<1/8,\qquad
 \sin\angle(n_1,m)<3/25
 \text{ for an associated }m\in\mathcal T.               \tag{4}
\]
No initial source or roll restriction is a premise of that filter.

The original geometry, Cauchy area representation and proper group are
from the [brightness certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
source `58824907716016ff519f2aa5430fef92aa78c62c`, graph
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`.
We credit the quadratic equatorial transport in the
[twofold-cap proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md),
graph `bafkreidiwye4mcfzaickzc4zmrbldyce44awk4f4ndnnlxpxgowilgvpsi`,
and the actual-original matching in the
[fivefold rigidity proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md),
graph `bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm`.
Here the transport and matching implications are proved explicitly.
The earlier Cauchy/polar method credits the
[J77 projection-area proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md).

`DEPENDENCIES.json` pins the filter's four mathematical files. Its checker
first replays that whole expected record and, transitively, the whole
fivefold-cap and brightness records, with all their pinned source hashes.
It then reconstructs the new finite facts below. Rational endpoints are
used only for inequalities affine in the parameter; the proof explains
why they cover the entire interval. No grid search or failed passage
search is a mathematical premise. The continuum implications in Sections
3–9 are written proof, not a proof-assistant formalization.

## 3. Physical area and a width direction on both complete arcs

Cauchy's formula writes
\(A(n)=\sum_{q\in C}|q\cdot n|\) for 31 physical paired-facet area
vectors. At \(e\), six are perpendicular to \(e\), forming \(D\), and
\[
 \sum_{q\in C\setminus D}\operatorname{sign}(q\cdot e)q=A_0e,
 \qquad
 \min_{q\in C\setminus D}\frac{(q\cdot e)^2}{\|q\|^2}
       =\frac{2-\phi}{4}>1/64.                            \tag{5}
\]
For \(\|n-e\|<1/8\), Cauchy–Schwarz makes all these nonzero signs
stable, so \(A(ze+u)=A_0z+\sum_{q\in D}|q\cdot u|\).
The checker reconstructs every facet and verifies
\[
 H_x=\sum_{q\in D}|q_x|=4+8\phi>14,\qquad
 H_y=\sum_{q\in D}|q_y|=8+4\phi>14.                       \tag{6}
\]
For either receiving arc \(n_j(s)=(e+s e_j)/\sqrt{1+s^2}\), its chord
from \(e\) is at most \(s\le1/12\). Indeed
\[
 \|n_j(s)-e\|^2
 =\frac{2s^2}{\sqrt{1+s^2}(\sqrt{1+s^2}+1)}\le s^2.
\]
Consequently its exact area is
\[
 A(n_j(s))=\frac{A_0+H_js}{\sqrt{1+s^2}}.                 \tag{7}
\]
This increases on the whole interval because its derivative has numerator
\(H_j-A_0s>0\), as checked at \(s=1/12\).
Independent original-vertex endpoint hulls have sixteen corners and give
\[
 \begin{aligned}
 A(n_x(1/12))^2&=(28048+44032\phi)/29,\\
 A(n_y(1/12))^2&=138704/145+(43792/29)\phi.
 \end{aligned}
\]
Both are below \((1171/20)^2\), while
\(A_1^2>(583/10)^2\). Since \(1171/20=583/10+1/4\), every receiver
on the arcs has \(A(n_j(s))<A_1+1/4\).

Use the actual perpendicular spatial width directions
\[
 z_x(s)=(\phi,1,-\phi s),\qquad z_y(s)=(\phi,1,-s).
\]
Let \(B=3\phi^2\), \(S=\phi+2\), and put
\((k_x,\ell_x)=(\phi^2,\phi^2)\),
\((k_y,\ell_y)=(\phi,1)\). At each endpoint \(s=0,1/12\), all sixty
originals satisfy \(z_j(s)\cdot v\le B+k_js\). Each inequality is
affine in \(s\), so it holds throughout the closed interval. The actual
original \((2\phi,\phi^2,-\phi)\) attains equality at both endpoints
and, by the same affine identity, throughout. Central symmetry gives the
exact directional width
\[
 w_j(s)^2=\frac{4(B+k_js)^2}{S+\ell_js^2},\qquad
 \mu(n_j(s))^2\le w_j(s)^2.                              \tag{8}
\]
Perpendicularity and the physical denominator are checked coefficient by
coefficient. The derivative of (8) has the sign of
\(k_jS-\ell_jBs\), positive throughout by its endpoint check.
The endpoint values are
\[
 w_x(1/12)^2=(2371108+3159652\phi)/104401,\quad
 w_y(1/12)^2=(2292772+3127108\phi)/104401.
\]
Both are strictly below the width bound in (3). Thus (3), and therefore
the full-source conclusion (4), apply on both entire arcs and, by proper
body symmetry, all of \(\mathcal M\).

## 4. Centering and independent proper body folds

Suppose the left side of (2) holds. Because both shadows are centrally
symmetric, negating and averaging the containments gives
\(\lambda B_1K\subseteq B_2K\). Since \(\lambda\ge1\) and \(0\in B_1K\),
\[
 B_1K\subseteq B_2K.                                    \tag{9}
\]
This preserves the actual frames. We use (9) for geometry, keeping the
original scale and translation for the final equality argument.

Independently right-multiplying each frame by a member of \(G\) preserves
its shadow. Fold the receiver to one of the reference arcs, and fold the
associated source axis in (4) to \(e\). These folds need not agree.
Afterwards the source normal satisfies
\[
 n_1=ze+u,\quad z>0,\quad r:=\|u\|<3/25,\quad
 d_1:=\|n_1-e\|<1/8.
\tag{10}
\]
Both source and target \(z\) coordinates exceed \(24/25\), since
\(1-(3/25)^2>(24/25)^2\) and \(144/145>(24/25)^2\).
No roll has been assumed small.

## 5. Four actual originals force close, bijective support matches

The four and only four originals equatorial to \(e\) are
\[
 E=\{(\pm a,\pm c,0)\},\qquad a^2+c^2=R^2.
\]
All other originals have \(|v_z|\ge1\), and every coordinate magnitude
is at most \(b=\phi^3<9/2\). At either receiving arc, every nonequatorial
original therefore has squared axial height strictly above
\[
 \frac{(1-(9/2)(1/12))^2}{1+(1/12)^2}=45/116.
\tag{11}
\]
Every original in \(E\) has the same receiving squared projected radius:
\(R^2-a^2u_2^2\) on the x arc, or \(R^2-c^2u_2^2\) on the y arc, where
\(u_2=s/\sqrt{1+s^2}\). Every source original in \(E\) has squared
projected radius at least \(R^2(1-r^2)>R^2-36/125\), using \(R^2<20\).
The strict rational gap is \(45/116>36/125\).

For any source projected point \(x=B_1v\), \(v\in E\), containment (9)
provides an actual receiving original projection \(y=B_2v'\) attaining
its support maximum with \(x\cdot y\ge\|x\|^2\). By Cauchy–Schwarz,
\(\|y\|\ge\|x\|\); (11) excludes every \(v'\notin E\). Moreover
\[
 \|x-y\|^2\le\|y\|^2-\|x\|^2<36/125<(11/20)^2.          \tag{12}
\]
Thus each source equatorial original matches a target equatorial original
within \(\epsilon=11/20\). This uses actual originals, not hull vertices
reconstructed as if they were originals.

The projection of \(e^\perp\) has smallest singular value \(n_i\cdot e\)
for both frames, larger than \(24/25\). Their distinct equatorial images
are separated by at least \(2a(24/25)>2\epsilon\). Consequently the
matches in (12) are unique and injective, hence a bijection of four points.
Central symmetry makes that bijection antipodal: uniqueness of the close
match to \(-x\) forces it to be \(-y\).

## 6. Side lengths and proper orientation leave only two label maps

An antipodal rectangle bijection maps opposite pairs to opposite pairs;
it can only preserve the two side types or exchange them. Long projected
sides have length at least \(2c(24/25)\), whereas short projected sides
have length at most \(2a\). Matching their endpoints would change a side
length by at most \(2\epsilon\). The checked strict inequality
\[
 2c(24/25)-2a>2\epsilon                                  \tag{13}
\]
excludes exchanges. The four survivors are the independent coordinate
sign maps on \((\pm a,\pm c)\).

A reference triangle with both rectangle sides incident at its first
vertex has determinant magnitude \(4ac\). Its projected determinant is
that determinant multiplied by \(n_i\cdot e>24/25\): proper planar roll
has determinant one. Replacing each of three target points by its matched
source point changes the determinant by at most
\[
 2\epsilon\,2(a+c)+4\epsilon^2<4ac(24/25).                \tag{14}
\]
To see this, each difference of endpoint errors has norm at most
\(2\epsilon\); expand the determinant using the two target side vectors,
whose lengths are at most \(2a,2c\). The two linear errors plus their
cross term give exactly the left side. Therefore this perturbation cannot
reverse the target triangle's orientation. Since both oriented normals
have positive \(e\) coordinate, the original source order and original
target order have the same projected orientation. A single coordinate
sign reversal would contradict (14).

Only identity and simultaneous sign reversal remain. The checker
exhausts all 24 permutations and confirms exactly these two maps.
In the latter case replace \(B_1\) by \(-B_1\), a **proper** planar
half-turn preserving its normal and shadow. We may now use the same
original labels for all four matches. This step uses central symmetry;
it does not insert an improper spatial motion.

## 7. Quadratic equatorial transport bounds the full arbitrary roll

Let \(P\) be the frame with rows \(e_x^t,e_y^t\). For a unit
\(n=ze+u\), \(z>0\), shortest proper normal transport defines a frame
\(C_n\) with normal \(n\), satisfying
\[
 C_n|_{e^\perp}=I_2-\frac{uu^t}{1+z},\qquad C_ne=-u,
 \quad \|C_n-P\|_{\rm op}=d:=\|n-e\|.
\tag{15}
\]
The tangent formula has eigenvalues \(1,z\); the normal formula completes
orthonormal rows with the correct oriented normal. Alternatively, in the
plane spanned by \(u,e\), it is the two-coordinate rotation with cosine
\(z\) and sine \(\|u\|\). That description gives the last identity.
For any equatorial original \(v\), with \(q=Pv\) and \(\|q\|=R\),
\[
 \|C_nv-q\|\le R\frac{\|u\|^2}{1+z}=Rd^2/2.             \tag{16}
\]
A common proper planar gauge makes the receiver \(B_2=C_{n_2}\).
The source then has the form \(B_1=LC_{n_1}\) for an initially arbitrary
\(L\in SO(2)\). Using one same-label match from Section 6 and (16),
\[
 \|(L-I)q\|<11/20+9/256+1/64.
\]
The last two terms use \(R<9/2\), \(d_1<1/8\), \(d_2\le1/12\).
For a planar rotation, \(\|(L-I)q\|=\|L-I\|_{\rm op}\|q\|\).
The checked lower bound \(R>22/5\) therefore gives
\[
 \|L-I\|_{\rm op}<769/5632,\qquad
 \|B_1-P\|_{\rm op}<1/8+769/5632=1473/5632<4/15.
\tag{17}
\]
This controls the full frame without an initial small-roll hypothesis.

## 8. An unchanged width locks one frame row exactly

On the x arc the second receiver row is exactly \(e_y^t\); on the y arc
the first is exactly \(e_x^t\). Write \(e_k\) for this fixed row direction,
and \(r_k\) for the corresponding source unit row (so \(k\ne j\)). By (17),
\[
 \|r_k-e_k\|<4/15,\quad r_k\cdot e_k>1-(4/15)^2/2>9/10.
\]
All target original coordinates in this direction are at most \(b\), and
the four actual originals with coordinate \(b\) in that direction and
independent \(\pm1\) in the other two directions belong to \(V\).
Their source support maximum and (9) imply
\[
 b(r_k\cdot e_k)+\sum_{i\ne k}|r_k\cdot e_i|\le b.       \tag{18}
\]
Let \(t_r=\sqrt{\sum_{i\ne k}(r_k\cdot e_i)^2}<4/15\).
If \(t_r>0\), the unit-row identity gives
\[
 t_r\le\sum_{i\ne k}|r_k\cdot e_i|
 \le b\frac{t_r^2}{1+r_k\cdot e_k},
 \quad
 1\le\frac{bt_r}{1+r_k\cdot e_k}
 <\frac{(9/2)(4/15)}{19/10}=12/19<1,
\]
a contradiction. Hence the row is **exactly** \(e_k^t\).
The remaining orthonormal row has positive reference coordinate by (17).
Consequently \(B_1=C_{(u,0,z)}\) on the x arc, or
\(B_1=C_{(0,u,z)}\) on the y arc, with \(z>0\) and \(|u|<3/25\).
There is no remaining roll.

## 9. Radial order and exact area finish the closed classification

The support match of Section 5 gave \(\|B_1v\|\le\|B_2v'\|\), where
both originals are in \(E\). On each now-locked mirror plane their common
radii are respectively \(R^2-a^2u^2,R^2-a^2u_2^2\), or
\(R^2-c^2u^2,R^2-c^2u_2^2\). Thus
\[
 |u|\ge u_2=s/\sqrt{1+s^2}.                              \tag{19}
\]
By (5) the source's exact area is
\(A_0\sqrt{1-u^2}+H_j|u|\). On \(0\le v\le3/25\) this is strictly
increasing, since its derivative is
\[
 H_j-\frac{A_0v}{\sqrt{1-v^2}}
 >14-\frac{58(3/25)}{24/25}=27/4>0.                     \tag{20}
\]
Area monotonicity in (9) and (19) force \(|u|=u_2\) and equal shadow
areas. The original scaled containment now forces \(\lambda=1\), since
\(\lambda^2A(n_1)\le A(n_2)=A(n_1)>0\).

If \(u=u_2\), the gauged source frame equals the receiver. If \(u=-u_2\),
directly from their rows in either mirror plane,
\[
 C_{n_1}=-C_{n_2}R_z,\qquad R_z\in G.                    \tag{21}
\]
Unfolding the independent proper body folds, common proper planar gauge
and optional source planar half-turn yields exactly
\(B_1=\sigma B_2g\). Thus their centered shadows are equal. For the actual
translation, support in every unit direction \(z\in\mathbb R^2\) gives
\(h_{B_2K}(z)+z\cdot t\le h_{B_2K}(z)\), hence \(t=0\).
Conversely every frame in (2) has the same shadow by \(gK=K=-K\), so
\(\lambda=1,t=0\) is a closed fit. This proves both directions of (2).

## 10. Reproduction and remaining frontier

From the repository root run:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_mirror_arc_rigidity/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_mirror_arc_rigidity/check.py
```

Each output must byte-match `expected.json`. Every mathematical guard is
an explicit exception check, so optimization does not remove it. The six
negative controls damage an actual contact set, the radial matching
budget, the row-locking budget, a rectangle side map, an orientation map
and an affine support witness; each must reject. All inputs, including
three complete prerequisite expected records, are public and hash-pinned.

The result classifies all touching fits on (1), going beyond a strict-fit
obstruction. It supplies a concrete excluded family through the low-area
receiver `(1,0,12)/sqrt145`, whose source annulus was left unresolved by
the filter alone. It leaves receiving directions off the compact arc
union unresolved. No explicit transverse neighborhood, complete sphere
cover, global non-Rupert result or floating-point search theorem is
claimed here. A useful next step is a quantitative perturbation argument
for receiver directions off the mirror planes while preserving the exact
support and proper-frame constraints.

The primary current-status seeds remain
[Steininger and Yurkevich, arXiv:2508.18475](https://arxiv.org/abs/2508.18475)
and [arXiv:2604.26531](https://arxiv.org/html/2604.26531), both checked live
on 2026-10-01 during this pass. They retain the standard RID as unresolved;
this intermediate arc exclusion does not settle that named question.
