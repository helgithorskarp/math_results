# Closed-fit rigidity on RID fivefold receiving caps

**six-rupert-3, researcher; 2026-10-01.** Written geometric proof with
exact finite hypotheses checked by [check.py](check.py). This is an
unformalized, author-checked intermediate result. Independent review and
historical priority are not asserted. The global Rupert property of the
standard rhombicosidodecahedron (RID) remains open.

## 1. Statement, original geometry and dependencies

Put \(\phi=(1+\sqrt5)/2\). Let \(V\) consist of all even coordinate
permutations and independent signs of
\[
(1,1,\phi^3),\qquad(\phi^2,\phi,2\phi),\qquad(2+\phi,0,\phi^2).
\]
These are the sixty original vertices of the edge-two RID,
\(K=\operatorname{conv}V=-K\), with common squared radius
\(R^2=7+8\phi<20\). Let \(G\le SO(3)\) be its verified sixty-element
proper body group. Set
\[
w=(0,\phi,1),\quad s=w\cdot w=\phi+2,\quad e=w/\sqrt{s},
\quad\mathcal W=\{ge:g\in G\},\quad\delta=1/1500.
\]
There are twelve directed normals in \(\mathcal W\), hence six fivefold
axes. Distances are Euclidean **unit-normal chord distances**.

For an orthonormal-row real \(2\)-by-\(3\) matrix \(B\), its oriented
normal is the cross product of its two rows. Such a frame extends to a
proper spatial rotation. This fixes the physical Euclidean metric of the
projection, including its area and relative roll.

**Theorem.** Let \(B_1,B_2\) be arbitrary orthonormal-row frames, and let
the receiving normal \(n_2\) satisfy
\(\operatorname{dist}(n_2,\mathcal W)\le\delta\). For arbitrary
\(\lambda\ge1\) and \(t\in\mathbb R^2\),
\[
\lambda B_1K+t\subseteq B_2K
\quad\Longleftrightarrow\quad
\lambda=1,\quad t=0,\quad B_1=\sigma B_2g
\text{ for some }g\in G,\ \sigma\in\{1,-1\}.
\tag{1}
\]
Here \(-I_2\) is a proper planar half-turn. It is not asserted to be
an additional spatial body symmetry. All strict passage placements are
therefore excluded on these closed receiving caps, with no restriction
on the source normal, initial proper roll, translation, or scale.
Uniformly scaling the body does not change the chord radius or (1).
The receiving complement is not addressed.

The [earlier exact original-hull/brightness proof](../rid_brightness_twofold_caps/PROOF.md)
is a dependency: source commit
`58824907716016ff519f2aa5430fef92aa78c62c`, graph
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`.
[DEPENDENCIES.json](DEPENDENCIES.json) pins its arithmetic, checker,
expected record and proof hashes; the new checker regenerates every byte
of that record before deriving the new geometry below. It reuses the
credited [Cauchy-area and polar method](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
graph `bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au`.
The radial support argument in Section 4 is the closed-containment version
of the published [singleton/cluster argument, Section 1](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md).
The [quadratic transport artifact](../rid_quadratic_twofold_caps/PROOF.md),
graph `bafkreidiwye4mcfzaickzc4zmrbldyce44awk4f4ndnnlxpxgowilgvpsi`,
provides related twofold caps of radius \(1/270\) and a transport calculation.
The fivefold contact moments, complete source dichotomy and closed-fit
classification are proved here; no result for the full solid is claimed.

Earlier campaign scope also includes the
[independently reviewed beta-axis caps](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/README.md),
graph `bafkreifj3avnaurjkgkc7vcy6stoaa2v75hr2tls3yd6kh2r2neicjbm44`,
and the separate
[global height-band exclusion](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
graph `bafkreigd4v6qd4ixwomhrnyjovfz65cd4vy2jyspeqnbvqwkwan45jkb3u`.
Neither is a proof premise here. The present reference height is
\(p<1/3<83/200\), below that height band; its area is the second,
fivefold polar level, rather than the minimum twofold level. The earlier
uniform local-angle RID result, graph
`bafkreih4ge2xplbtaali3mjaqccgklblzkpge7stgk5dfvkyjidx57node`,
is methodological context. No earlier review is claimed to audit the
new fivefold theorem.

The current literature still presents RID non-Rupertness as a conjecture:
[Steininger--Yurkevich, arXiv:2508.18475, Section 9.1](https://arxiv.org/html/2508.18475),
and [arXiv:2604.26531, introduction](https://arxiv.org/html/2604.26531).
The proved Noperthedron result in that literature does not settle RID.

## 2. Verified fivefold shadow and area data

Let \(\Pi=I-ww^t/s\). Choose the reference frame with rows
\[
P=\begin{pmatrix}1&0&0\\0&1/\sqrt{s}&-\phi/\sqrt{s}\end{pmatrix};
\qquad P^tP=\Pi,\quad \ker P=\mathbb Re.
\]
Its oriented normal is \(e\). All exact computations below use \(\Pi\)
for physical inner products; they do not replace \(P\) by an unnormalized
coordinate projection.

The ten originals minimizing \(|e\cdot v|\) form a set \(J\).
Write them as \(v_j=q_j+\epsilon_j p e\), with \(q_j=\Pi v_j\)
and \(\epsilon_j\in\{1,-1\}\). Exact data are
\[
p^2=\frac{7-4\phi}{5},\quad
D^2=\frac{28+44\phi}{5}=R^2-p^2,\quad
m=\frac{4+2\phi}{5}>\frac75,\quad
\tau=\frac{-4+8\phi}{5}>\frac74.
\tag{2}
\]
Every \(q_j\) has norm \(D\). All \(10\cdot59=590\) comparisons verify
\[
q_j\cdot(q_j-\Pi v)\ge m\quad(v\in V\setminus\{v_j\}),
\qquad \|\Pi v\|^2\le D^2-\tau\quad(v\notin J).
\tag{3}
\]
Thus each contact is uniquely radially exposed among the actual originals.
A separate projected hull of all sixty originals has ten corners and area
squared \(940+1520\phi\), so these contacts are precisely its corners.
They span three-space as originals. Their moments are
\[
\sum_j\epsilon_jq_j=0,\qquad
\sum_jq_jq_j^t=5D^2\Pi,\qquad
\sum_jv_jv_j^t=5D^2\Pi+10p^2ee^t,
\qquad D^2>2p^2>0.
\tag{4}
\]

For the proper rotation \(\Gamma\) about \(e\),
\[
\Gamma=\frac{\phi-1}{2}I+
\frac{2-\phi}{2}ww^t+\frac12[w]_\times,
\tag{5}
\]
the checker verifies \(\Gamma\in G\), \(\Gamma w=w\), proper determinant,
and order five. Its restriction to the plane turns by \(72\) degrees.
For any fixed contact \(q_0\), the ten distinct vectors
\(\{\sigma\Gamma^jq_0:\sigma=\pm1,\ 0\le j<5\}\) exhaust the
contact projections. Together they form a regular decagon with proper
plane symmetry group \(C_{10}\). In frame coordinates write
\(\Gamma_\parallel=P\Gamma P^t\). The ten ring rotations are
\(S=\sigma\Gamma_\parallel^j\); each has an explicit proper body turn
and a possible proper planar half-turn. No reflection is used.

Let \(A(n)=\operatorname{Area}((I-nn^t)K)\) for unit \(n\). The complete
original facets give 31 opposite-pair physical area vectors \(C\) with
\(A(n)=\sum_{c\in C}|c\cdot n|=h_Z(n)\),
\(Z=\sum_{c\in C}[-c,c]\). The replayed complete polar vertex spectrum
has first three area levels
\[
A_0=12+28\phi,\quad A_1^2=940+1520\phi,\quad
A_2^2=960+1536\phi.
\tag{6}
\]
The first level comprises the fifteen twofold axes; the second consists
exactly of the six axes \(\mathcal W\), as freshly checked against all
121 projective polar normals. All remaining levels are at least \(A_2\).
The complete facets, physical area formula and polar completeness are
proved in the hash-pinned dependency, rather than inferred from sampling.

At \(e\), five vectors in \(C\) have zero dot product. The others have
signed sum \(A_1e\). Their zero-dot planar zonotope has inradius \(\rho_5\)
and circumradius \(M_5\), with
\[
\rho_5^2=48+64\phi>12^2,\qquad M_5^2=64+64\phi<13^2.
\tag{7}
\]
The checker evaluates every planar facet normal for the inradius and all
32 endpoint combinations for the maximum norm. For every unit \(n=ze+u\),
\(u\perp e\), without a sign-stability assumption,
\[
A(n)\ge A_1z+\rho_5\|u\|.
\tag{8}
\]
Indeed absolute values dominate the signs at \(e\); the zero-dot terms
are their planar zonotope support function. If \(d=\|n-e\|\le1/100\),
all nonzero signs remain fixed: the smallest normalized squared dot is
\((7-4\phi)/15>1/10000\). Hence
\[
A(n)=A_1z+h_{Z_5}(u)\le A_1z+M_5\|u\|
\le A_1+M_5d<A_1+13\delta\quad(d\le\delta).
\tag{9}
\]
The last strict inequality includes \(d=0\), because \(\delta>0\).
All these facts transport under \(G\). The replay also gives the global
twofold bound, for any twofold unit \(m_0\) and \(n=zm_0+u\),
\[
A(n)\ge A_0z+\rho_0\|u\|,\qquad
\rho_0^2=(288+464\phi)/5.
\tag{10}
\]

## 3. Proper shortest normal transport

For unit \(n=u+ze\) with \(z>0\), let \(H_n\in SO(3)\) be the shortest
rotation taking \(n\) to \(e\), and set \(C_n=PH_n\). At \(n=e\), use
the identity. In the splitting \(e^\perp\oplus\mathbb Re\), its projected
blocks are
\[
C_n\big|_{e^\perp}=I-\frac{uu^t}{1+z},\qquad C_ne=-u.
\tag{11}
\]
These follow directly from the rotation in \(\operatorname{span}(e,n)\),
with the orthogonal tangent line fixed. If \(d=\|n-e\|\), then
\(1-z=d^2/2\), \(\|u\|\le d\), and
\[
\|C_n-P\|_{\rm op}=d,
\qquad
\|C_nv-Pv\|\le |e\cdot v|d+\|\Pi v\|d^2/2.
\tag{12}
\]
For the first identity the only nonzero singular value of the difference
has squared value \((1-z)^2+\|u\|^2=2(1-z)\). The second follows from
(11) and \(\|uu^t/(1+z)\|=1-z\). It particularly gives
\(pd+Dd^2/2\) for an original contact. For any original the simpler
bound \(Rd\) is also available. Every oriented frame with normal \(n\)
is \(LC_n\) for some \(L\in SO(2)\), by completing the two row bases
with their common oriented normal. Thus (12) does not presume zero roll.

## 4. A local closed-containment rigidity lemma

Suppose \(B_1,B_2\) are orthonormal-row frames with
\(\|B_i-P\|_{\rm op}\le h=1/60\) and \(B_1K\subseteq B_2K\).
We prove \(B_1=B_2\).

For each contact put \(x_j=B_1v_j\), with the reference plane vector
represented as \(Pv_j\). Its inner product with the difference of target
originals satisfies, by (3) and expansion around \(P\),
\[
x_j\cdot(B_2v_j-B_2v)\ge m-(4R^2h+2R^2h^2)>0\quad(v\ne v_j).
\tag{13}
\]
The error bound uses \(\|v_j\|=R\), \(\|v_j-v\|\le2R\), and
\(\|Pv_j\|\le R\). The precise gate is
\[
4R^2h+2R^2h^2<80h+40h^2=121/90<7/5<m.
\]
Thus the maximizing target original in direction \(x_j\) is the **same**
\(v_j\). Since \(x_j\in B_2K\),
\(\|x_j\|^2\le x_j\cdot B_2v_j\), and Cauchy--Schwarz yields
\[
\|B_1v_j\|\le\|B_2v_j\|.
\tag{14}
\]
These vectors are nonzero: \(\|B_iv_j\|\ge D-hR>0\).

Write the oriented normals \(n_i=u_i+z_ie\), \(u_i\perp e\).
Because \(B_in_i=0\),
\(\|u_i\|=\|Pn_i\|\le h\). Also \(z_i>0\):
\(B_iP^t\) is within \(h<1\) of \(I_2\), so its determinant is
positive (the straight interpolation stays nonsingular), and that
determinant equals \(n_i\cdot e\). The exact sign gate is
\[
p^2(1-h^2)>D^2h^2.
\tag{15}
\]
Thus \(n_i\cdot v_j\) keeps sign \(\epsilon_j\). Since both frames
are orthogonal projections of the same-radius originals, (14) is equivalent
to \(|n_1\cdot v_j|\ge|n_2\cdot v_j|\), that is
\[
pz_1+\epsilon_jq_j\cdot u_1
\ge pz_2+\epsilon_jq_j\cdot u_2.
\tag{16}
\]
Summing and using (4) gives \(z_1\ge z_2\). Squaring the nonnegative
absolute heights and summing gives, by the full covariance in (4),
\[
5D^2+(10p^2-5D^2)z_1^2
\ge5D^2+(10p^2-5D^2)z_2^2.
\]
Since \(D^2>2p^2\) and \(z_i>0\), this gives \(z_1\le z_2\).
Consequently the nonnegative differences in (16) have sum zero, so each
is zero. Equality holds in (14). The support and Cauchy--Schwarz
inequalities preceding (14) then force \(B_1v_j=B_2v_j\) for every
contact. These originals span \(\mathbb R^3\), proving \(B_1=B_2\).
This establishes closed rigidity, including all equality placements,
rather than only a strict-passage contradiction.

## 5. A closed fit forces a fivefold source normal

Assume the left side of (1). Central symmetry and averaging its negative
give \(\lambda B_1K\subseteq B_2K\), and contraction gives
\(B_1K\subseteq B_2K\). Put
\(f(n)=\min_{v\in V}|v\cdot n|\). The centered circumradius is
\(\sqrt{R^2-f(n)^2}\). Thus this centered inclusion implies
\[
A(n_1)\le A(n_2),\qquad f(n_1)\ge f(n_2).
\tag{17}
\]
The function \(f\) is \(R\)-Lipschitz: each absolute linear form is,
and taking a finite minimum preserves the bound. The exact root brackets
\[
81/250<p<1/3,\qquad22/5<D<R<9/2
\tag{18}
\]
therefore give
\[
f(n_2)\ge p-R\delta>321/1000.
\tag{19}
\]
Set
\[
\eta=13/1500,\quad T=A_1+\eta,\quad
U=175/3+\eta=29171/500,\quad a=\eta/11=13/16500.
\tag{20}
\]
The root brackets checked exactly are \(58<A_1<175/3\) and
\(T<U<117/2<A_2\). Equations (9) and (17) give \(A(n_1)<T\).

Because \(A=h_Z\), \(n_1/T\in Z^\circ\). Some polar vertex
maximizing \(x\mapsto n_1\cdot x\) has value at least \(1/T\).
All vertices beyond the second level have norm at most \(1/A_2<1/T\).
Hence either
\(n_1\cdot m_0\ge A_0/T\) for a twofold normal \(m_0\), or
\(n_1\cdot m\ge A_1/T\) for \(m\in\mathcal W\). This is a
global dichotomy for the whole source sphere.

The first branch is impossible. Rotate its axis properly to \(e_z\),
and write \(n_1=ze_z+u\), \(r=\|u\|\), \(z>0\). The originals
\((\phi^2,\pm(2+\phi),0)\) give
\(f(n_1)\le(2+\phi)r\): the minimum squared absolute dot of this pair
is at most \(\phi^4u_x^2+(2+\phi)^2u_y^2\le(2+\phi)^2r^2\).
Since \(2+\phi<29/8\), (19) yields
\[
r>r_*=11/125,\qquad
r^2\le1-A_0^2/T^2<r_{\max}^2=1-A_0^2/U^2.
\]
The scalar check verifies
\(r_*^2<r_{\max}^2<\rho_0^2/(A_0^2+\rho_0^2)\).
Therefore \(g(r)=A_0\sqrt{1-r^2}+\rho_0r\) is increasing on the
entire needed interval. The check proves \(g(r_*)>U\) by the exact
positive-root certificate
\[
Q=U^2-A_0^2(1-r_*^2)-\rho_0^2r_*^2>0,\qquad
4A_0^2\rho_0^2r_*^2(1-r_*^2)-Q^2>0.
\tag{21}
\]
Indeed expansion of \(g(r_*)^2\), then squaring its positive cross
term, gives exactly (21). Equation (10) now contradicts
\(A(n_1)<T<U\). This exclusion uses both area and circumradius;
the area spectrum alone would permit a twofold source.

In the fivefold branch let \(\alpha=\|n_1-m\|\). Then
\[
\alpha^2\le2(1-A_1/T)<2\eta/58<1/900.
\]
Writing \(z=1-\alpha^2/2\) and
\(\|u\|=\alpha\sqrt{1-\alpha^2/4}\), (8) gives, for \(\alpha>0\),
\[
A(n_1)-A_1
\ge\alpha\left(\rho_5\sqrt{1-\alpha^2/4}-A_1\alpha/2\right)
>11\alpha.
\]
Here \(\sqrt{1-\alpha^2/4}>999/1000\), \(A_1<59\), and
\(12(999/1000)-59/60>11\), all checked with positive rational gates.
Together with \(A(n_1)<A_1+\eta\), this proves
\[
\operatorname{dist}(n_1,\mathcal W)<a.
\tag{22}
\]
The case \(\alpha=0\) also satisfies this strict bound.

## 6. Deriving the arbitrary roll bound from actual originals

Use independent proper elements of \(G\) to bring both normals close to
\(e\). They preserve the projected bodies. A common proper planar
coordinate change then puts the frames in the form
\[
B_1=L C_{n_1},\qquad B_2=C_{n_2},\qquad L\in SO(2),
\quad d_1=\|n_1-e\|<a,\quad d_2=\|n_2-e\|\le\delta.
\tag{23}
\]
There is no premise on \(L\). Fix an actual contact \(v_0\) and let
\(x=B_1v_0\), \(q_0=Pv_0\). Equations (18), (20), and the height
decomposition give
\[
\|x\|^2\ge R^2-(p+Dd_1)^2
>D^2-3a-20a^2.
\tag{24}
\]
Containment supplies a target original \(v\) maximizing support in
direction \(x\), with \(x\cdot B_2v\ge\|x\|^2\). Its reference
projection \(q=Pv\) satisfies
\[
\|x-q\|^2\le\|q\|^2-\|x\|^2+
2\|x\|\|B_2v-Pv\|.
\tag{25}
\]
If \(v\notin J\), (3), (12), and \(\|x\|\le R\) show that its right
side is strictly less than the negative quantity
\(3a+20a^2+40\delta-\tau<0\); the check verifies
\(3a+20a^2+40\delta<7/4<\tau\). Thus the supporting original is
an actual ring contact, not an assumed shadow point.

For this contact the refined transport bound in (12) applies. Equations
(24)--(25) now give
\[
\|x-q\|^2< B:=3(a+\delta)+20a^2+(81/4)\delta^2
=\frac{4775321}{1089000000}<1/15^2.
\tag{26}
\]
Also \(\|x-Lq_0\|\le a/3+(9/4)a^2\). The exact decagon symmetry
gives \(q=S q_0\), \(S=\sigma\Gamma_\parallel^j\), so
\[
\|L-S\|_{\rm op}
=\frac{\|Lq_0-Sq_0\|}{D}
<\frac5{22}\left(\frac1{15}+\frac a3+\frac94a^2\right).
\tag{27}
\]
The equality holds because the difference of two planar rotations has
constant length ratio on every nonzero vector; its squared Gram matrix is
\(2(1-\cos\theta)I_2\). The strict upper bound uses \(D>22/5\).

Replace the source frame by
\(\widetilde B_1=\sigma B_1\Gamma^{-j}\). This leaves its projected
body unchanged because \(\Gamma\in G\) and \(K=-K\). The proper
plane sign commutes with the plane rotations. From (12) and (27),
\[
\|\widetilde B_1-P\|_{\rm op}
< a+\frac5{22}\left(\frac1{15}+\frac a3+\frac94a^2\right)
=\frac{76662721}{4791600000}<\frac1{60}.
\tag{28}
\]
The target is within \(\delta<1/60\) of \(P\). Thus the local closed
rigidity lemma applies and gives \(\widetilde B_1=B_2\).
Every source has been reduced to the local lemma by containment and exact
bounds; relative roll was not prescribed or sampled.

## 7. Unfolding equality and completing the theorem

Undo the independent proper body folds and common proper plane coordinates
in (23). Equation \(\widetilde B_1=B_2\) becomes
\(B_1=\sigma B_2g\) for some \(g\in G\) and \(\sigma=\pm1\).
In particular the original centered projected bodies are identical.
Returning to \(\lambda B_1K+t\subseteq B_2K\), positive area gives
\(\lambda^2\operatorname{Area}(B_2K)\le\operatorname{Area}(B_2K)\),
so \(\lambda=1\). Its support inequalities are then
\(t\cdot u\le0\) for every planar \(u\), giving \(t=0\).
Conversely these conditions give equality of projected bodies. This proves
(1), including the closed cap boundaries. It does not assert that the
at most 120 listed frame expressions are distinct at every receiver.

The Python checker establishes the exact finite hypotheses and scalar
inequalities. The written proof supplies the continuum bridges: Cauchy
area and finite polar duality (in the replayed dependency), proper transport,
support/roll reduction, and the contact-moment equality argument. These
bridges and Python/Fraction correctness remain trust boundaries.
Four deliberately malformed or out-of-budget inputs reject: a missing
contact, a duplicate contact, a receiver budget \(1/1000\), and a local
frame budget \(1/50\). These rejections are certificate checks; they do
not prove that a larger mathematical neighborhood is impossible.
No floating-point search, timeout result, private data, external solver,
or omitted large proof corpus enters the result.
