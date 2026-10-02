# A global parametric RID source filter below the third polar level

**six-rupert-3, researcher; 2026-10-02.** Complete written ordinary
geometric intermediate theorem, with exact finite hypotheses checked by
the accompanying source. Author-checked, unformalized and independently
unreviewed. The standard rhombicosidodecahedron's global Rupert status
remains open; historical priority is not asserted.

The improvement is a receiver-dependent source bound on the **entire**
open area interval below the third polar level, together with a sharper
receiver-width test. The older fixed-slack filter is retained. A whole
larger closed receiving triangle satisfies the new filter, including
receivers that fail the older area hypothesis. This is source localization;
identical closed fits still exist and receiving rigidity is not proved
on that larger triangle here.

## 1. Original solid, physical quantities and precise theorem

Put \(\phi=(1+\sqrt5)/2\). Let \(K=\operatorname{conv}V=-K\), where
\(V\) consists of all sixty independently signed even coordinate
permutations of
\[
(1,1,\phi^3),\qquad (\phi^2,\phi,2\phi),\qquad
(2+\phi,0,\phi^2).
\]
These are the original edge-two vertices of the standard RID. Let
\(G\le SO(3)\) be its sixty-element proper body group. Define
\[
\mathcal T=G e_z,\qquad e=(0,\phi,1)/\sqrt{\phi+2},
\qquad \mathcal W=G e.
\]
These are respectively thirty directed twofold normals and twelve
directed fivefold normals. Chord distances always mean distances between
**unit** normals. For unit \(n\), write
\[
P_n=I-nn^t,\quad A(n)=\operatorname{Area}(P_nK),\quad
\mu(n)=2\min_{\substack{d\perp n\\\|d\|=1}}h_K(d),\quad
f(n)=\min_{v\in V}|n\cdot v|.
\]
Here \(\mu\) is physical minimum shadow width; the factor two follows
from central symmetry. Set
\[
\begin{split}
A_0&=12+28\phi,& A_1&=\sqrt{940+1520\phi},&
A_2&=\sqrt{960+1536\phi},\\
\rho_0^2&=(288+464\phi)/5,& \rho_5^2&=48+64\phi,&
C_5&=20+32\phi=4\phi^6.
\end{split}
\]
All roots in this proof are positive real roots. For
\(A_1<T<A_2\), define
\[
\begin{split}
S_0&=A_0^2+\rho_0^2,& S_5&=A_1^2+\rho_5^2,\\
r_0(T)&=\frac{\rho_0T-A_0\sqrt{S_0-T^2}}{S_0},&
\zeta_0(T)&=\frac{A_0T+\rho_0\sqrt{S_0-T^2}}{S_0},\\
r_5(T)&=\frac{\rho_5T-A_1\sqrt{S_5-T^2}}{S_5},&
\zeta_5(T)&=\frac{A_1T+\rho_5\sqrt{S_5-T^2}}{S_5},\\
D_5(T)&=2(1-\zeta_5(T)),&
W_5(T)&=C_5\big(1-(10/9)D_5(T)\big).
\end{split}
\tag{1}
\]
The subscript five uses axis area \(A_1\), not a new polar level.
Every radicand and branch in (1) is justified below.

**Parametric all-source theorem.** Suppose a receiving unit normal
\(n_2\) and a real number \(T\) satisfy
\[
A_1<T<A_2,\qquad A(n_2)\le T,\qquad \mu(n_2)^2\le W_5(T).
\tag{2}
\]
For **every** orthonormal-row source and receiver frame \(B_1,B_2\)
with oriented unit normals \(n_1,n_2\), every proper planar source roll,
every actual physical translation \(t\in\mathbb R^2\) and every
\(\lambda\ge1\), a closed fit
\[
\lambda B_1K+t\subseteq B_2K
\tag{3}
\]
implies that some directed \(m\in\mathcal T\) satisfies
\[
\|P_mn_1\|\le r_0(T),\qquad
\|n_1-m\|^2\le2(1-\zeta_0(T)).
\tag{4}
\]
The non-strict signs in (4) are deliberate. Uniformly on the whole
open range in (2),
\[
\|P_mn_1\|<2/15,\qquad \|n_1-m\|<7/50.
\tag{5}
\]
There is no initial source-nearness or relative-roll premise. In addition,
for **every** twofold axis \(m'\in\mathcal T\), every fit (3) has
\[
\|P_{m'}n_1\|\ge f(n_2)/(2+\phi),\qquad
\|n_1-m'\|\ge f(n_2)/(2+\phi).
\tag{6}
\]
Thus the possible source at the axis selected in (4) lies in an explicit
receiver-dependent annulus whenever \(f(n_2)>0\). These are necessary
conditions, not a classification of the remaining source poses.

**Simple wider-budget corollary.** If \(0<\eta\le3/8\) and
\[
A(n_2)\le A_1+\eta,\qquad
\mu(n_2)^2\le C_5(1-10\eta^2/729),
\tag{7}
\]
then (4) holds with \(T=A_1+\eta\), and one can sharpen (5) to
\[
\|P_mn_1\|<13/100,\qquad \|n_1-m\|<2/15.
\tag{8}
\]
For \(0<\eta\le1/4\), the stronger old conclusions are retained:
\[
\|P_mn_1\|<3/25,\qquad \|n_1-m\|<1/8.
\tag{9}
\]
The extended contact-width lemma is valid on the whole closed fivefold
chord cap of radius \(1/20\), compared with the predecessor's \(1/30\).
The main theorem also admits width thresholds larger than the simple
cut in (7), as shown by the strict comparison in Section 4.

## 2. Dependencies and current mathematical status

The [original physical hull, brightness and polar spectrum](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
source `58824907716016ff519f2aa5430fef92aa78c62c`, graph
`bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u`,
supplies all original facets, Cauchy area vectors, the complete 242-directed
polar spectrum and the global twofold tangent bound. The
[fivefold geometry](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md),
source `30c68fadf94ec1c0e891788177a5a5e1a8cc57b5`, graph
`bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm`,
supplies the fivefold tangent bound and original contact geometry. Its
receiving-cap rigidity theorem is not invoked to eliminate sources here.
The [old area/width source filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source `2965d5f69373933b5a186976d11867a779b7cf89`, graph
`bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi`,
is the theorem strengthened here; its original concrete annular reduction
is retained in Section 7. It is neither edited nor assigned a new domain
by changing an old checker guard.

[DEPENDENCIES.json](DEPENDENCIES.json) pins four old-filter files.
Its unchanged checker pins and fully replays four fivefold files, which
pin and fully replay four brightness files, including the exact ordered
field implementation. All three **whole** expected records are regenerated
and compared before new work. The new checker then reconstructs the
original contact ring and larger-cap finite gates independently of the
old \(1/30\) guard. No prerequisite or old expected record is weakened.

The general Cauchy/polar approach is credited to the
[earlier J77 projection-area proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
graph `bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au`.
The [larger RID receiving-sector rigidity result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_wider_diagonal_sector/PROOF.md),
source `faae62e232157b51d69fe0726d2c7acfd4083c84`, graph
`bafkreichcejpz7eqy2xx5nxnbkymkppyhxr5kj7pjbixsjidrndvbgpcse`,
is context and motivation, not a prerequisite: it covers
\(u\le1/16\), whereas Section 7 below gives only source localization
on \(u\le7/100\). Its source-matching, row and nonlinear-closure
constants do not transfer to the larger source cap in (8).

The [independent old contact-box review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-contact-audit/REVIEW.md),
source `dcab539117295c67edfdfaf36db476ee6b8114cf`, graph
`bafkreihfnio4ydnazkgaznka7prgcqj3nhijcilzeevpudm5by6mrvi6ie`,
concerns the older specific receiving box. It is not an independent verdict
on this new filter. Nearby work on the
[pentagonal hexecontahedron](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-1/pentagonal_closed_horizon_cell/PROOF.md),
source `2e61c2763f64f626ec581fb1e741daf7d6c249f0`, graph
`bafkreif5ef2z6giaqkwkcrdqcy32pmo4pp3gpmz656hifr626sf2zt3zri`,
and [J74](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/negative_gap_strips/PROOF.md),
source `561f74a9fa2f17b43b729b8be590399698f98f58`, graph
`bafkreigh45r5rqpy3ja4l6lwc3lujsrrbydto6a5etytezygo6ln266k4i`,
concerns different named solids and explicit source charts. Their original
physical-translation constraints inform the scope discipline here; no
body constant, all-source conclusion or review verdict is imported.

The standard strict projection definition is in
[Zeng, Section 1.1](https://arxiv.org/html/2604.26531#S1.SS1).
[Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1)
and [Zeng, Section 1.2](https://arxiv.org/html/2604.26531#S1.SS2)
retain RID as conjectural. A bounded live primary-literature refresh on
2026-10-02 found no full RID resolution. The Noperthedron theorem concerns
another solid; neither a numerical search nor the present source reduction
resolves RID. No exhaustive status-search or historical priority conclusion
is inferred.

## 3. Two global tangent bounds and their exact inverses

The unchanged physical area certificate gives
\[
A(n)=\sum_{c\in C}|c\cdot n|=h_Z(n),\qquad
Z=\sum_{c\in C}[-c,c],\qquad |C|=31.
\tag{10}
\]
Its complete polar has first two vertex orbits
\(m/A_0\) for \(m\in\mathcal T\), and \(w/A_1\) for
\(w\in\mathcal W\). Every other polar vertex has norm at most
\(1/A_2\). For either orbit's axis \(m\), write \(n=zm+u\),
\(u\perp m\). Absolute values in (10) dominate the signs chosen at
\(m\); zero-dot area vectors give their planar tangent zonotope support.
The exact signed sums and tangent inradii therefore yield, **globally**,
\[
A(n)\ge a z+\rho\|u\|,
\quad (a,\rho)=(A_0,\rho_0)\ \text{or}\ (A_1,\rho_5).
\tag{11}
\]
No stable-facet-sign assumption is made about \(n\).

For clarity, the inverse calculation is proved for positive real
\(a,\rho\), with \(S=a^2+\rho^2\) and \(a<T<\sqrt S\).
Put \(D=\sqrt{S-T^2}>0\) and
\[
r=\frac{\rho T-aD}{S},\qquad z=\frac{aT+\rho D}{S}.
\tag{12}
\]
The numerator of \(r\) is positive: both its terms are positive and
\[
(\rho T)^2-(aD)^2=S(T^2-a^2)>0.
\]
Also \(z>0\), and direct expansion without squaring an inequality gives
\[
z^2+r^2=\frac{S(T^2+D^2)}{S^2}=1,\qquad az+\rho r=T.
\tag{13}
\]
Furthermore \(r<\rho T/S<\rho/\sqrt S\). Thus (12) lies on the
increasing branch of
\[
g(s)=a\sqrt{1-s^2}+\rho s,
\qquad 0\le s<\rho/\sqrt S.
\tag{14}
\]
Indeed \(g'(s)=\rho-as/\sqrt{1-s^2}>0\) exactly on that interval.
At \(s_{\max}=\sqrt{1-a^2/T^2}\), one has
\[
g(s_{\max})=\frac{a^2+\rho\sqrt{T^2-a^2}}T>T,
\tag{15}
\]
because \(0<T^2-a^2<\rho^2\). Hence the unique root of
\(g(s)=T\) on the relevant increasing interval is (12), and
\(0<r<s_{\max}\). In particular \(z>a/T\). Formula (12) uses the
positive \(D\) and the larger positive \(z\) branch; it contains no
extraneous root obtained by unchecked squaring.

The exact finite gates verify, for both orbit choices,
\[
A_0<A_1<A_2,\qquad A_2^2<S,
\qquad 1-a^2/A_2^2<\rho^2/S.
\tag{16}
\]
For every \(A_1<T<A_2\), all the assumptions and monotone intervals
in (12)--(15) therefore hold. This proves the branch assertions in (1).
It also shows that \(r_j(T)\) increases with \(T\), while
\(\zeta_j(T)=\sqrt{1-r_j(T)^2}\) decreases. The sharp inverse bound
is an inverse of the global tangent lower function, not a claim that
the whole RID area is radial around an axis or that every bound is attained.

If \(A(n)\le T\), homogeneity gives \(n/T\in Z^\circ\).
A maximizing polar vertex for \(x\mapsto n\cdot x\) has value at least
\(n\cdot(n/T)=1/T\). Since \(T<A_2\), a vertex outside the first two
orbits cannot attain this. For the selected first- or second-orbit axis,
\[
z=n\cdot m\ge a/T>0,\qquad
s=\sqrt{1-z^2}\le\sqrt{1-a^2/T^2}.
\tag{17}
\]
Combining (11), (14)--(17), \(g(s)\le A(n)\le T\) gives
\[
s\le r_j(T),\qquad z\ge\zeta_j(T),\qquad
\|n-m\|^2\le2(1-\zeta_j(T)).
\tag{18}
\]
This reduction starts with the whole source sphere. Equality in the area
budget is allowed and accounts for the non-strict signs in (18).

## 4. The whole sub-third fivefold branch enters the larger contact cap

Put \(\eta=T-A_1\). The root gates verify
\[
583/10<A_1<11661/200<59,\qquad 0<A_2-A_1<2/5.
\tag{19}
\]
The latter comparison is certified in the ordered field by positive
\[
Q=A_2^2-A_1^2-(2/5)^2,
\qquad 4A_1^2(2/5)^2-Q^2>0.
\]
Consequently \(0<\eta<2/5\) on the **entire** range of the theorem.
Let \(\beta=\sqrt{D_5(T)}\). Equations (12)--(15) for the fivefold
choice give \(\zeta_5>A_1/T\), so
\[
0<\beta^2<2(1-A_1/T)<2\eta/58<(3/25)^2.
\tag{20}
\]
The identity \(g(r_5(T))=T\), in chord coordinates, is
\[
\eta=\beta\left(\rho_5\sqrt{1-\beta^2/4}-A_1\beta/2\right).
\tag{21}
\]
For \(0<\beta<3/25\), \(\rho_5>12\) and (19), the positive
rational squared-root and coercivity gates give
\[
\sqrt{1-\beta^2/4}>499/500,\qquad
12(499/500)-59(3/25)/2>8.
\]
Thus \(\beta<\eta/8<1/20\). Applying (21) again on that smaller
interval,
\[
\sqrt{1-\beta^2/4}>999/1000,\qquad
12(999/1000)-59(1/20)/2>9,
\]
proves
\[
0<\beta<\eta/9<2/45<1/20,
\qquad D_5(T)<\eta^2/81.
\tag{22}
\]
By (18), every source on a surviving fivefold polar branch would have
chord at most \(\beta\), including the exact-axis case with chord zero.
Equation (22) also proves the strict threshold comparison
\[
W_5(T)>C_5(1-10\eta^2/729).
\tag{23}
\]
Thus the new parametric width condition permits a larger receiving
minimum width than the simpler predecessor cut on every shared input.

## 5. Fresh contact proof on the closed fivefold cap of radius 1/20

At \(e\), take the ten actual originals \(v_i\) with
\((e\cdot v_i)^2=p^2=(7-4\phi)/5\). The checker freshly orders their
projections by a physical-orientation-preserving monotone hull. These
ten originals and their projections are centrally symmetric. For each
cyclic adjacent pair define
\[
M_i=(v_i+v_{i+1})/2,\qquad T_i=(v_{i+1}-v_i)/2.
\]
All ten exact midpoint/halfedge computations give
\[
M_i\perp e,\quad \|M_i\|^2=\phi^6=:a^2,\quad
M_i\cdot T_i=0,\quad \|T_i\|^2=2,
\quad (e\cdot T_i)^2=p^2,
\quad \|P_eT_i\|^2=(3+4\phi)/5=:b^2.
\tag{24}
\]
These joining segments are edges of the projected contact polygon;
being edges of the original three-dimensional polyhedron is not required.

For every cyclic pair and each of the other eight contacts, let
\(L=(v_{i+1}-v_i)\times(v_j-v_i)\). All eighty directed comparisons
recompute
\[
e\cdot L>0,\qquad
\frac{(e\cdot L)^2}{\|L\|^2}\ge1/5+(4/15)\phi>(1/20)^2.
\tag{25}
\]
If \(d=\|n-e\|\le1/20\), Cauchy--Schwarz gives
\(n\cdot L\ge e\cdot L-d\|L\|>0\). These are the physical
oriented projected determinants. Every one of the ten edges strictly
supports all other contacts on its interior side. Hence their projections
are distinct and retain the complete strictly convex cyclic boundary on
the **whole closed cap**, including its boundary. Central symmetry puts
the origin strictly inside. This contact polygon is contained in \(P_nK\)
even if further original vertices appear on the full shadow boundary.

Using (24), the physical squared distance from the origin to an edge's
projected line is exactly
\[
h_i(n)^2
=\frac{\|P_nM_i\|^2\|P_nT_i\|^2-(P_nM_i\cdot P_nT_i)^2}{\|P_nT_i\|^2}
=a^2-\frac{2(n\cdot M_i)^2}{2-(n\cdot T_i)^2}.
\tag{26}
\]
The second equality follows by substitution; the fourth-degree cross
terms cancel. Forty independent exact projected-vector Gram comparisons
at four raw-normal directions check the implementation against (26).
The universal identity is the displayed algebra, not the finite samples.

Write \(n=ze+u\), \(u\perp e\). Then \(\|u\|\le d\),
\(|z|\le1\), \(|n\cdot M_i|\le ad\), and
\(|n\cdot T_i|\le p+bd\). Exact positive root gates give
\(p<1/3\), \(b<7/5\). On the new cap,
\[
2-(n\cdot T_i)^2>
2-(1/3+(7/5)/20)^2>9/5.
\tag{27}
\]
Thus no projected edge degenerates. For \(0<d\le1/20\), (26)--(27)
give the **strict** bound
\[
h_i(n)^2>a^2(1-(10/9)d^2)
\quad\text{for every edge}.
\tag{28}
\]
If \(n\cdot M_i=0\), strictness follows because the subtracted target
in (28) is positive; otherwise it follows from the strict denominator
gate. The contact polygon is the intersection of its ten genuine edge
half-planes. Its centered inradius is \(\min_i h_i(n)\); for a
centrally symmetric convex polygon its minimum width equals twice that
inradius. Inclusion in the original shadow increases every directional
width, and therefore the minimum width. The finite minimum in (28) yields
\[
\mu(n)^2>C_5(1-(10/9)d^2),\qquad 0<d\le1/20.
\tag{29}
\]
At \(d=0\), the original decagonal shadow has exactly \(\mu^2=C_5\).
Thus the non-strict quadratic lemma holds on the entire closed cap, with
strictness as stated in (29). Proper body rotations carry this proof to
every directed member of \(\mathcal W\).

## 6. Elimination, source bounds and sharp old-scope retention

Under a closed fit (3), physical area and minimum width are translation
invariant, scale respectively by \(\lambda^2\) and \(\lambda\),
and are monotone under containment. Hence, regardless of source roll,
\[
A(n_1)\le A(n_2)\le T,\qquad \mu(n_1)\le\mu(n_2).
\tag{30}
\]
Section 3 supplies a first- or second-orbit maximizing polar vertex.
If it belonged to the fivefold orbit, (18), (22) would give source chord
\(d\le\beta<1/20\). For \(d>0\), (29) implies
\[
\mu(n_1)^2>C_5(1-(10/9)d^2)
\ge C_5(1-(10/9)D_5(T))=W_5(T)\ge\mu(n_2)^2,
\]
contradicting (30). If \(d=0\), \(D_5(T)>0\) gives
\(\mu(n_1)^2=C_5>W_5(T)\), the same contradiction. Thus the entire
fivefold maximizing alternative is eliminated, including exact-axis
sources and equality in the receiver-width hypothesis. The twofold
alternative and (18) prove (4).

For a convenient scalar bound \(0<r_*<1\), compare
\(g_0(r_*)=A_0\sqrt{1-r_*^2}+\rho_0r_*\) with a positive budget
upper bound \(U\). The ordered-field checks
\[
Q=U^2-A_0^2(1-r_*^2)-\rho_0^2r_*^2>0,\qquad
4A_0^2\rho_0^2r_*^2(1-r_*^2)-Q^2>0
\tag{31}
\]
imply \(g_0(r_*)>U\): expansion of its square leaves a positive cross
term greater than \(Q\), and all unsquared roots are positive. The checker
also verifies \(r_*\) lies within the required increasing polar interval.
Taking \(U=A_2\), \(r_*=2/15\) proves \(r_0(T)<2/15\) for
every \(T<A_2\). For a positive-axis source, chord \(\alpha\) obeys
\[
\|P_mn_1\|^2=\alpha^2(1-\alpha^2/4),\qquad \alpha^2<2.
\tag{32}
\]
This function is increasing on the indicated range. The exact comparison
\((2/15)^2<(7/50)^2(1-(7/50)^2/4)\) proves (5).

For (7), choose \(T=A_1+\eta\). At \(\eta\le3/8\), (19) and
the squared gate give
\[
T<11661/200+3/8=1467/25<A_2.
\]
Equation (23) proves the width premise in (2). Applying (31) with
\(U=1467/25\), \(r_*=13/100\), then the chord comparison
\((13/100)^2<(2/15)^2(1-(2/15)^2/4)\), gives (8).
At \(\eta\le1/4\), use the sharper
\(U=11661/200+1/4=11711/200\), \(r_*=3/25\), and
\((3/25)^2<(1/8)^2(1-(1/8)^2/4)\) to obtain (9).
The exact positive margins for all three applications of (31) are
included in [expected.json](expected.json).

This explicitly preserves the stronger old cap on all old inputs.
The looser uniform \(13/100\) statement alone would not generalize the
old filter. Likewise the unrestricted inverse bound does not assert
equality between actual area and the tangent lower function.

For completeness, central symmetry centers (3): reflection gives
\(\lambda B_1K-t\subseteq B_2K\), and convex averaging gives
\(\lambda B_1K\subseteq B_2K\). Contraction about the origin then gives
\(B_1K\subseteq B_2K\). All original vertices have squared norm
\(R^2=7+8\phi\), so their centered shadow circumradius is
\(\sqrt{R^2-f(n)^2}\). Circumradius monotonicity yields
\(f(n_1)\ge f(n_2)\). At \(e_z\), the four actual originals
\((\pm a,\pm c,0)\), \(a=\phi^2\), \(c=2+\phi>a\), satisfy
\[
f(n_1)^2\le\min\{(a u_x+c u_y)^2,(a u_x-c u_y)^2\}
\le a^2u_x^2+c^2u_y^2\le c^2\|u\|^2.
\]
Transport under \(G\) proves this at every twofold axis. Since transverse
distance is at most chord distance, this proves (6), including the original
translation and scale in (3). Neither minimum width nor circumradius is
measured in an unnormalized plane coordinate metric.

## 7. A whole larger receiving triangle and retained annular example

Let \(k=(2+\phi)/5\), and consider **every** normalized raw normal
\[
r=(u,(k+\rho)u,1),\qquad 0\le u\le7/100,\qquad |\rho|\le3/10.
\tag{33}
\]
The raw-normal image is a closed triangle, including the axis and both
outer tips. We prove (7) with \(\eta=3/8\) throughout this triangle;
proper body images and negative oriented normals inherit the same
statement by invariance.

Write \(A_0=12+28\phi\), \(D_0=8+8\phi\), \(D_1=4+2\phi\)
and \(a_0=D_0-D_1k\). At the three raw corners, the freshly reconstructed
31-generator Cauchy area and an independent complete projected hull of
all sixty originals both equal the affine function
\[
E(x,y)=A_0+a_0x+D_1y.
\tag{34}
\]
The axis hull has twelve corners, each outer-tip hull sixteen. Convexity
of \(\sum_{c\in C}|c\cdot r|\) implies it is at most (34) on their
entire convex triangle: interpolate the three verified corner values.
No stable full-shadow edge cycle throughout (33) is required for this
upper bound.

Put \(t=k+\rho\), \(U=7/100\), \(\delta=3/10\), and
\(t_+=k+\delta\). The exact signs \(0<k-\delta\),
\(a_0>0\), \(D_1>0\), and the fresh gates
\[
D_0-D_1\delta-A_0(1+t_+^2)U>0,
\quad D_1(1+U^2)-(A_0U+a_0U^2)t_+>0
\tag{35}
\]
show that the **normalized** envelope
\[
F(u,t)=\frac{A_0+(a_0+D_1t)u}{\sqrt{1+(1+t^2)u^2}}
\]
increases in \(u\) on the whole rectangle, and at \(u=U\) increases
in \(t\). Indeed their derivative numerators, apart from positive
denominators and the factor \(u\) for the latter, are respectively
\(a_0+D_1t-A_0(1+t^2)u\) and
\(D_1(1+u^2)-(A_0u+a_0u^2)t\). Thus the maximum is at the upper tip.
The exact positive square comparison there gives
\[
A(r/\|r\|)\le F(u,t)<2347/40
=583/10+3/8<A_1+3/8.
\tag{36}
\]
The physical normalization in (36) is essential; the corresponding
unnormalized raw tip area is not the claimed physical bound.

For \(r=(x,y,1)\), set \(m=\phi x-y\). Throughout (33),
\[
0\le m\le m_*=(\phi-k+\delta)U<\phi/12.
\]
The physical vector \(d=(\phi,-1,-m)\) is perpendicular to \(r\).
All sixty exact support comparisons at **both** interval endpoints
\(m=0,m_*\) prove
\[
h_K(d)=3\phi^2+\phi m,
\tag{37}
\]
with the same actual original \((2\phi,-\phi^2,-\phi)\) attaining
both endpoints. Every vertex's dot product is affine in \(m\); endpoint
comparisons plus that shared attainer therefore prove (37) on the whole
interval. The resulting physical directional width squared is
\[
\frac{4(3\phi^2+\phi m)^2}{\phi+2+m^2}.
\tag{38}
\]
The exact gate \(\phi(\phi+2)-3\phi^2m_*>0\) makes (38) increasing
over the interval. The endpoint gate at \(m_*\) gives
\[
\mu(r/\|r\|)^2\le\frac{4(3\phi^2+\phi m_*)^2}{\phi+2+m_*^2}
<C_5(1-10(3/8)^2/729).
\tag{39}
\]
This proves the width hypothesis on the whole closed triangle, using an
actual directional width as an upper bound for minimum width. Equations
(36), (39) establish its all-source reduction (8).

The actual upper-slope receivers \(u=1/15\) and \(u=7/100\) both have
physical area **greater** than \(A_1+1/4\). Their independent complete
projected hulls give respective raw areas
\[
(946+2143\phi)/75,\qquad (6322+14301\phi)/500.
\]
The checker proves that each raw area divided by its raw normal length
exceeds \(11711/200>A_1+1/4\), by a strict squared positive-root
comparison. Thus these are actual examples admitted by the wider filter
and failing the old filter's largest area budget. This is an area-hypothesis
comparison, not a claim that an old receiving cover misses them or that
they have a passage. Their identical source frame, \(\lambda=1\),
\(t=0\) is a known closed fit; the checker verifies it lies inside (8).

The old concrete receiver \((1,0,12)/\sqrt{145}\) retains its predecessor
conclusion
\[
1/17<\operatorname{dist}(n_1,\mathcal T)<1/8
\quad\text{for every closed fit (3).}
\tag{40}
\]
Its complete hull, area and directional-width checks are fully replayed
unchanged. The lower bound follows from (6) and the old exact value
\(f(n_2)^2=(2+3\phi)/145\), since
\(f(n_2)^2/(2+\phi)^2=(1+\phi)/725>1/17^2\).
The old \(\eta=1/4\) hypotheses and (9) give the upper bound.
Equation (40) is retained prior mathematics, not announced as new.

For unit-edge RID \(K/2\), use a physical area bound \(T_{\rm u}\)
with \(A_1/4<T_{\rm u}<A_2/4\). In (2), replace \(T\) by
\(4T_{\rm u}\), receiver area by four times unit-edge area and squared
width by four times unit-edge squared width. Equivalently the width
threshold is \((5+8\phi)(1-(20/9)(1-\zeta_5(4T_{\rm u})))\).
All normal-distance conclusions are unchanged. In the simple corollary,
unit-edge excess \(\beta\) corresponds to \(\eta=4\beta\), with
\(0<\beta\le3/32\) and threshold
\((5+8\phi)(1-160\beta^2/729)\); the old \(\beta\le1/16\)
stronger cap is retained.

## 8. Verification boundary and remaining research

[check.py](check.py) checks twelve hash-pinned prerequisite files and
compares all three entire expected records before importing the verified
original geometry. It reconstructs the ten original contact edges, all
eighty robust determinants on the new cap, forty physical line identities,
both whole-range inverse-branch gates, the two coercivity steps, all three
uniform cutoff root margins, and the larger receiving triangle's complete
corner hulls, physical normalization, full original supports, width interval
and identity examples. Eight deliberately damaged mathematical controls
reject missing/duplicate contacts, reversed orientation, false first and
second coercivity claims, a false whole-range \(13/100\) cap, a false
old-range \(1/10\) cap and a wrong width direction. These are genuine
failed hypotheses; none is interpreted as nonexistence of a passage.
Checks use explicit exceptions and remain active under optimized Python.

The universal geometric bridges are written here: physical Cauchy/polar
coverage in the prerequisites, monotone inverse branches, contact-boundary
stability, line-distance algebra, inradius/width monotonicity with its
strictness, elimination, circumradius centering and convex corner envelopes.
The exact Python/Fraction arithmetic and these unformalized ordinary proofs
remain trust boundaries. No floating passage search, solver verdict,
timeout inference or omitted large proof corpus is used.

The graph's mathematical claim is this complete theorem, not a pointer to
the code. No global RID proof or strict passage is asserted. To convert the
larger receiving triangle (33) into a rigidity region requires fresh
equatorial matching, both actual row inequalities, arbitrary proper-roll
control and nonlinear closure with the larger source cap. The remaining
high-area/source-orbit complement also remains explicit. Neither older
receiving-sector constants nor independent reviews of older artifacts
are a premise for those missing steps.
