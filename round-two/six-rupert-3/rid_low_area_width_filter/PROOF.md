# RID area and quadratic width reduce all sources to twofold caps

**six-rupert-3, researcher; 2026-10-01.** Complete written geometric
source-domain reduction with exact finite hypotheses. Author-checked,
unformalized and independently unreviewed; historical priority is not
asserted. The global RID Rupert question remains open. This artifact
does not exclude all passages at its example receiver.

## 1. Definitions and statements

Put \(\phi=(1+\sqrt5)/2\). The original edge-two rhombicosidodecahedron
is \(K=\operatorname{conv}V=-K\), where \(V\) consists of all sixty signed
even coordinate permutations of
\[
(1,1,\phi^3),\qquad(\phi^2,\phi,2\phi),\qquad(2+\phi,0,\phi^2).
\]
The common squared original radius is \(R^2=7+8\phi\). Let \(G\le SO(3)\)
be the sixty-element proper body group. Write
\[
\mathcal T=G(0,0,1),\quad
e=(0,\phi,1)/\sqrt{\phi+2},\quad\mathcal W=Ge,
\quad A_0=12+28\phi,\quad A_1=\sqrt{940+1520\phi},
\quad A_2=\sqrt{960+1536\phi}.
\]
The sets \(\mathcal T\) and \(\mathcal W\) contain respectively thirty
and twelve directed normals, i.e. fifteen twofold and six fivefold axes.
Distances are between **unit normals**, in the Euclidean chord metric.

For unit \(n\), let \(P_n=I-nn^t\),
\(A(n)=\operatorname{Area}(P_nK)\), and
\[
\mu(n)=\min_{\substack{d\perp n\\\|d\|=1}}
\big(h_K(d)+h_K(-d)\big)
=2\min_{\substack{d\perp n\\\|d\|=1}}h_K(d).
\]
This is the physical minimum width of the shadow. It is invariant under
proper planar roll and translation. Under uniform body scaling it scales
linearly, while area scales quadratically.

**Quadratic width lemma.** If
\(d=\operatorname{dist}(n,\mathcal W)\le1/30\), then
\[
\mu(n)^2\ge(20+32\phi)(1-(10/9)d^2).
\tag{1}
\]
At a fivefold axis equality gives \(\mu^2=20+32\phi=4\phi^6\).
The negative change allowed by (1) is quadratic in normal tilt.

**Global source filter.** Suppose \(0<\eta\le1/4\), and the receiving
unit normal \(n_2\) satisfies
\[
A(n_2)\le A_1+\eta,\qquad
\mu(n_2)^2\le(20+32\phi)(1-10\eta^2/729).
\tag{2}
\]
For any orthonormal-row frames \(B_1,B_2\) with oriented unit normals
\(n_1,n_2\), any \(\lambda\ge1\) and physical planar translation \(t\),
\[
\lambda B_1K+t\subseteq B_2K
\quad\Longrightarrow\quad
\operatorname{dist}(n_1,\mathcal T)<1/8.
\tag{3}
\]
There is no source-normal or relative-roll premise. The second polar
source orbit is eliminated by width, leaving only the first orbit.
Equation (3) is a necessary condition; it is not a receiver exclusion.

**Concrete annular reduction.** For
\(n_2=(1,0,12)/\sqrt{145}\), every closed fit as in (3) satisfies
\[
1/17<\operatorname{dist}(n_1,\mathcal T)<1/8.
\tag{4}
\]
The source roll, scale and translation still require further study.
In particular the identical closed fit is present; the checker verifies
that this known equality example lies strictly inside (4).

## 2. Dependencies and finite coverage

The [original-hull/brightness certificate](../rid_brightness_twofold_caps/PROOF.md),
source `58824907716016ff519f2aa5430fef92aa78c62c`, graph
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`,
proves the physical Cauchy-area norm and complete 121-axis polar spectrum.
The [fivefold geometry/cap proof](../rid_fivefold_rigidity/PROOF.md),
source `30c68fadf94ec1c0e891788177a5a5e1a8cc57b5`, graph
`bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm`,
proves the exact fivefold contact ring, proper stabilizer and tangent bounds.
Its receiving-cap theorem is not used to assert (3).
[DEPENDENCIES.json](DEPENDENCIES.json) pins four of its source/proof files,
which in turn pin four original-hull files. The checker replays both entire
expected records before making the new checks; no prerequisite is changed.

The general Cauchy/polar mechanism is credited to the
[J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
graph `bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au`.
The [twofold receiving caps and area gap](../rid_quadratic_twofold_caps/PROOF.md),
graph `bafkreidiwye4mcfzaickzc4zmrbldyce44awk4f4ndnnlxpxgowilgvpsi`,
and the separate
[height-band exclusion](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
graph `bafkreigd4v6qd4ixwomhrnyjovfz65cd4vy2jyspeqnbvqwkwan45jkb3u`,
are cited context, not new assertions or proof premises here.
The example below lies outside the specified twofold/fivefold caps and
below that height band. No claim is made that it lies outside every
older published geometric receiving cover.

Both [Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475)
and [arXiv:2604.26531, introduction](https://arxiv.org/html/2604.26531)
retain RID as conjectural. The Noperthedron theorem concerns another solid.
A bounded live status check on 2026-10-01 located no full RID resolution;
no exhaustive literature-search or priority conclusion is inferred.

## 3. Original contact edges retain their boundary on a whole cap

At \(e\), the shadow is the regular decagon formed by ten actual originals
\(v_i=q_i+\epsilon_i p e\), with
\[
p^2=(7-4\phi)/5,\qquad \|q_i\|^2=(28+44\phi)/5.
\]
The checker orders their projections by a physical-orientation-preserving
monotone hull. It does not presume which originals are neighbors. For all
ten cyclic adjacent pairs it verifies, with
\[
M_i=(v_i+v_{i+1})/2,\qquad T_i=(v_{i+1}-v_i)/2,
\]
the identities
\[
M_i\perp e,\quad \|M_i\|^2=\phi^6=:a^2,\quad
M_i\cdot T_i=0,\quad\|T_i\|^2=2,\quad
|e\cdot T_i|^2=p^2,\quad
\|P_eT_i\|^2=(3+4\phi)/5=:b^2.
\tag{5}
\]
These are edges of the projected **contact polygon**. Their joining
segments are in the original body, but they need not be edges of the
original polyhedron.

For every edge \(v_i,v_{i+1}\) and each of the other eight contacts set
\(L=(v_{i+1}-v_i)\times(v_j-v_i)\). All eighty comparisons verify
\[
e\cdot L>0,\qquad
\frac{(e\cdot L)^2}{\|L\|^2}\ge\frac15+\frac4{15}\phi>1/900.
\tag{6}
\]
Thus whenever \(\|n-e\|\le1/30\),
\(n\cdot L\ge e\cdot L-\|n-e\|\|L\|>0\).
These are the oriented physical projected determinants. Every projected
edge strictly supports all other contact points on its interior side.
Consequently the same ten contacts are distinct and retain that complete
strictly convex cyclic boundary on the entire cap, including its boundary.
This polygon is centrally symmetric, with the origin strictly inside.
It is contained in the full original shadow, whether or not additional
originals appear on the latter's boundary.

## 4. Equatorial midpoints give a quadratic width bound

For an orthogonal pair \(M,T\) as in (5), the squared distance from the
origin to the line through \(P_nM\) in direction \(P_nT\) is
\[
h_i(n)^2=
\frac{\|P_nM\|^2\|P_nT\|^2-(P_nM\cdot P_nT)^2}{\|P_nT\|^2}
=a^2-\frac{2(n\cdot M)^2}{2-(n\cdot T)^2}.
\tag{7}
\]
To obtain the second equality, substitute
\(\|P_nM\|^2=a^2-(n\cdot M)^2\),
\(\|P_nT\|^2=2-(n\cdot T)^2\), and
\(P_nM\cdot P_nT=-(n\cdot M)(n\cdot T)\); the fourth-degree cross
terms cancel. Forty additional exact physical Gram comparisons at four
raw-normal directions check (7) against the direct projected vectors.
The universal identity follows from this algebra, not from those samples.

Write \(n=u+ze\), with \(u\perp e\) and
\(d=\|n-e\|\le1/30\). Then \(\|u\|\le d\), \(|z|\le1\), and
\[
|n\cdot M|\le ad,\qquad
|n\cdot T|\le p+b d.
\]
The exact positive root bounds \(p<1/3\), \(b<7/5\) give
\[
2-(n\cdot T)^2>
2-(1/3+(7/5)/30)^2>9/5.
\tag{8}
\]
In particular no projected edge degenerates. Substituting (8) into (7)
yields \(h_i(n)^2\ge a^2(1-(10/9)d^2)\) for every edge.
By (6) this polygon is exactly the intersection of its ten edge
half-planes; its centered inradius is the minimum of these positive
distances. For a centrally symmetric convex body the minimum width is
twice the centered inradius: both equalities follow from the support
function definition. Thus its minimum width squared is at least
\(4a^2(1-(10/9)d^2)\). Inclusion in \(P_nK\) can only increase every
directional width, hence also the minimum. Proper body rotations transport
the same argument to all \(\mathcal W\), proving (1).

## 5. Area and width eliminate the second source orbit

Assume (2) and a closed fit of scale at least one. Physical area and
minimum width are translation invariant, and scale by \(\lambda^2\) and
\(\lambda\) respectively. Monotonicity under containment therefore gives
\[
A(n_1)\le A(n_2)\le T:=A_1+\eta,\qquad
\mu(n_1)\le\mu(n_2).
\tag{9}
\]
The original physical area formula is \(A=h_Z\) on the unit sphere,
where \(Z\) is the complete original facet-area zonotope. The first two
levels of its polar vertices are \(m_0/A_0\), \(m_0\in\mathcal T\),
and \(m/A_1\), \(m\in\mathcal W\). Every other vertex has norm
at most \(1/A_2\). Because \(n_1/T\in Z^\circ\), some maximizing
polar vertex has dot product with \(n_1\) at least \(1/T\).

The exact root brackets are
\(58<A_1<175/3\) and \(U=703/12<A_2\). For the whole interval
\(0<\eta\le1/4\), \(T<U\). Hence the maximizing vertex must belong
to one of the first two orbits. In the fivefold alternative,
\[
z=n_1\cdot m\ge A_1/T,\qquad
\alpha^2:=\|n_1-m\|^2\le2(1-A_1/T)<2\eta/58<1/100.
\tag{10}
\]
The fivefold tangent zonotope has inradius
\(\rho_5^2=48+64\phi>12^2\). Absolute-value domination of the signed
nonzero facet vectors gives the **global** lower bound
\[
A(n_1)\ge A_1(1-\alpha^2/2)+
\rho_5\alpha\sqrt{1-\alpha^2/4}.
\tag{11}
\]
It does not assume stable facet signs at \(n_1\).
For \(0<\alpha<1/10\), since \(A_1<59\),
\[
A(n_1)-A_1
\ge\alpha\big(\rho_5\sqrt{1-\alpha^2/4}-A_1\alpha/2\big)
>\alpha\big(12(399/400)-59/20\big)>9\alpha.
\]
The positive rational square comparison
\((399/400)^2<1-(1/10)^2/4\) justifies the root bound.
Together with (9), including the \(\alpha=0\) case, this proves
\(\alpha<\eta/9\le1/36<1/30\). Equation (1) now gives
\[
\mu(n_1)^2\ge(20+32\phi)(1-(10/9)\alpha^2)
>(20+32\phi)(1-10\eta^2/729)\ge\mu(n_2)^2,
\]
contradicting (9). Every fivefold maximizing branch is eliminated,
including exact-axis sources and the width boundary in (2).

## 6. The surviving twofold source cap

There is therefore \(m_0\in\mathcal T\) with
\(z=n_1\cdot m_0\ge A_0/T>A_0/U>0\). Put
\(r=\sqrt{1-z^2}\). The global twofold tangent bound from the original
certificate is
\[
A(n_1)\ge g(r):=A_0\sqrt{1-r^2}+\rho_0r,\qquad
\rho_0^2=(288+464\phi)/5.
\]
Also \(r^2<r_{\max}^2=1-A_0^2/U^2\). The exact gates verify
\[
(3/25)^2<r_{\max}^2<\rho_0^2/(A_0^2+\rho_0^2).
\]
Thus \(g\) is increasing on the entire relevant interval.
For \(r_*=3/25\), the checker proves \(g(r_*)>U\) by
\[
Q=U^2-A_0^2(1-r_*^2)-\rho_0^2r_*^2>0,\qquad
4A_0^2\rho_0^2r_*^2(1-r_*^2)-Q^2>0.
\tag{12}
\]
Expansion of \(g(r_*)^2\) and squaring its positive cross term give
exactly these sufficient positive-root gates. If \(r\ge r_*\), the
area lower bound contradicts \(A(n_1)\le T<U\). Hence \(r<3/25\).
For the chord \(\alpha_0=\|n_1-m_0\|\),
\(r^2=\alpha_0^2(1-\alpha_0^2/4)\); because \(z>0\) this is
increasing as a function of \(\alpha_0^2\) on its needed range.
The exact comparison
\((3/25)^2<(1/8)^2(1-(1/8)^2/4)\) gives \(\alpha_0<1/8\).
This proves (3). No initial small-normal or small-roll restriction entered.

## 7. Exact receiver and all-source annulus

For \(r_2=(1,0,12)\), the independent original projected hull has
sixteen corners and
\[
A(r_2/\sqrt{145})^2=(28048+44032\phi)/29,\qquad
f(r_2/\sqrt{145})^2=(2+3\phi)/145,
\quad f(n)=\min_{v\in V}|v\cdot n|.
\tag{13}
\]
It has \(A_1^2<A(n_2)^2<A_2^2\). The exact brackets
\(A_1>583/10\), \(A(n_2)<1171/20=583/10+1/4\) prove the area
part of (2) for \(\eta=1/4\). The actual direction
\(z_2=(12\phi,12,-\phi)\) is perpendicular to \(r_2\); evaluating
all sixty original supports gives its physical squared width
\[
W_2^2=\frac{2371108+3159652\phi}{104401}
<(20+32\phi)(1-5/5832).
\tag{14}
\]
The right side is exactly the threshold in (2) at \(\eta=1/4\).
One actual directional width upper-bounds minimum width, so (14)
proves that part of (2); an unnormalized planar metric is never used.

Central symmetry centers any fit \(\lambda B_1K+t\subseteq B_2K\)
by averaging with its negative, then contraction gives \(B_1K\subseteq B_2K\).
The centered circumradius identity \(\max_{v\in V}\|P_nv\|
=\sqrt{R^2-f(n)^2}\) yields \(f(n_1)\ge f(n_2)\).
At a twofold axis properly rotated to \(e_z\), the four actual
equatorial originals \((\pm\phi^2,\pm(2+\phi),0)\) give
\(f(n_1)\le(2+\phi)\|P_{e_z}n_1\|\). For example, the minimum
squared dot of the pair with the two opposite second-coordinate signs
is at most \(\phi^4u_x^2+(2+\phi)^2u_y^2\le(2+\phi)^2\|u\|^2\).
This holds at every \(m_0\in\mathcal T\) by its proper body orbit.
Also \(\|P_{m_0}n_1\|\le\|n_1-m_0\|\). Consequently for **every**
twofold axis,
\[
\|n_1-m_0\|^2\ge\frac{f(n_2)^2}{(2+\phi)^2}
=\frac{1+\phi}{725}>1/17^2.
\]
Combining with (3) proves (4), including translations and scales in the
original placement. Arbitrary proper rolls remain unrestricted.

All checks in (13)--(14) use actual original vertices. The separate
receiving-cap/height comparisons merely locate the example relative to
three specified previous exclusions. They are not a global uncovered-set
classification. The identical source frame at \(n_2\), scale one and
translation zero is an allowed closed fit inside the annulus. Neither
strict passage nor its impossibility is proved for this receiver.

For a unit-edge normalization, replace \(K\) by \(K/2\). With area
budget \(0<\beta\le1/16\), the corresponding criterion is
\(A_{\rm unit}\le A_1/4+\beta\) and
\(\mu_{\rm unit}^2\le(5+8\phi)(1-160\beta^2/729)\).
The source chord conclusions are unchanged.

## 8. Evidence and remaining trust boundary

The checker verifies all eight prerequisite file hashes and regenerates
both complete earlier expected records, then checks the new ten original
contact edges, eighty boundary determinants, forty physical line-distance
identities, every root/area/width gate, original receiver hull and supports,
and the known identity-fit annulus. Six deliberately malformed/out-of-budget
controls reject: missing or duplicate contact, reversed loop, area budget
outside the claimed domain, a false twofold tangent cutoff, and a
nonperpendicular width direction. A rejected budget proves no mathematical
nonexistence there. Guards remain active under optimized Python.

The continuum reductions are supplied by the written proof: polar
completeness and area in the prerequisites, stable projected boundary,
the universal edge-distance identity, inradius/width monotonicity,
source-orbit elimination, positive-root comparisons, and circumradius
centering. These unformalized bridges and exact Python/Fraction arithmetic
remain trust boundaries. No floating passage search, solver verdict,
timeout conclusion, private data or omitted large proof corpus is used.
