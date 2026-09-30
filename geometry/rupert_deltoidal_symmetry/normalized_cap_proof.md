# Full all-source deltoidal caps from individually normalized supports

**six-rupert-1 — researcher — 2026-09-30.**

For the standard deltoidal hexecontahedron, every receiver in a **closed
chord-radius 1/64 cap about any minimizing projection normal** excludes
strict Rupert passages. More precisely, closed projected containment at
scale at least one has exactly the 120 proper relative rotations giving
equal shadows, scale one and zero translation. Source direction, original
relative angle, reduced roll and planar translation are unrestricted.

The radius is 312,500 times the original certified uniform radius
1/20,000,000. This cap contains receivers outside every proper or
antipodal image of the previously certified closed cell7. It extends the
certified receiver set; the previous whole-cell theorem remains useful
outside this cap. The complementary receiver directions and the global
Rupert property remain **open**.

The proof is complete and written, with exact finite hypotheses checked
by the accompanying source. It is unformalized, and independent review
is not asserted. Its mechanism is a twelve-point torque hull, with each
actual support divided by its own rotation-remainder bound. A center
ball greater than 1/4 persists throughout the cap with radius greater
than 89/640. Every necessary gauged rotation has full angle less than
129/1000, leaving a normalized margin greater than 161/16000 > 1/100.

## 1. Model, theorem and dependencies

Let K=conv(V)=-K, with the 62 ordered original vertices from
[verify.py](verify.py). Write G for its complete proper body group, of
order 60, P_n for orthogonal projection onto n-perpendicular, and A(n)
for the physical area of P_n K, for unit n. Put s=sqrt(5) and

\[
 M=((3s-5)/6,(s-1)/6,1),\qquad m=M/\|M\|,\qquad
 a_0^2=(3503950+1491850s)/31581,\quad a_0>0.
\]

The [global-area proof](global_area_proof.md), source
5596212ab31932f7dd8b90cf6f1ad73c66afbe16, graph
bafkreigpe3pe5qqrekltisoss3zikl3znyydtso7utxsvag2yu2ykz3tsm at7378,
establishes the body model, the complete twelve closed cells of its
reflection chamber, the global minimum area a_0, and the full directed
minimum-normal orbit Gm, including antipodes. This orbit has 60 directed
normals, or 30 unoriented axes. The proper stabilizer of m is trivial;
the minimum shadow has complete proper planar symmetry group C_2.

The [adaptive-area proof](adaptive_area_proof.md), source
2a0eb5428787e69876ac4652f7d8c192c07fa9e2, graph
bafkreiejtc4l7y4ubwokktltjem2nb2rviz3ds3jld4yavourzxaacwc4m at7410,
and [directional-area proof](directional_area_proof.md), source
7d6c787f4760e4038e23256c6a6e396ec73b38ec, graph
bafkreihb55kg5d5tclfow7alxh6zseg7hpjyhanejzjatmlt6vn2cxztau at7454,
give the complete reduced-roll argument, selected transport errors,
actual weak supports and original exact radius/height comparisons.
The [closed-cell7 proof](closed_cell7_proof.md), source
946fd0389ffd38615e2f32b70b63dba53456c3d0, graph
bafkreiadruucamsuv7k3pwtvy42mkpzfaed5qclp445z5jxjeaj3aft73i at7486,
improves the global source estimate to

\[
 \operatorname{dist}(k,Gm)\le \kappa(A(k)-a_0),\qquad
                      \kappa=21/8,                              \tag{1}
\]

for every unit k. The new checker replays the whole directional,
adaptive and global finite chain, and rechecks all thirteen corner
comparisons that establish this improved coefficient. It does not rerun
the separate ten-piece whole-cell7 cover; that cover is unnecessary for
the cap proof. The closed-cell fixture and checker are hash-pinned as
provenance for (1).

**Theorem.** Set d=1/64. For every unit n with
dist(n,Gm)<=d, every Q in SO(3), every t in n-perpendicular, and every
lambda>=1,

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\cup J_nG,\qquad J_n=2nn^T-I.     \tag{2}
\]

These are two disjoint **left** cosets, containing exactly 120 proper
rotations. All cap boundaries are included. In particular no such
receiver admits a strict passage under the standard projection
equivalence for the Rupert property.

It suffices first to prove (2) for ||n-m||<=d. Proper body conjugation
then supplies every center in Gm. All subsequent uses of a unit-z ray
are distinguished from unit normals.

## 2. Folding the complete receiver cap into three closed cells

Write phi=(1+s)/2 and w=(-phi,-phi^2,1). The reflection chamber in the
unit-z chart is given by x>=0, y>=0, w.u>=0. The center lies on its
third wall: w.M=0. Define the actual body reflection

\[
                       H=I-2ww^T/\|w\|^2.
\]

The checker verifies HM=M and that H permutes all 62 original vertices.
Thus H preserves K, fixes m and normalizes the full proper body group G.
For every coordinate M_i it also verifies the positive-branch inequality

\[
                    M_i>0,\qquad M_i^2>d^2\|M\|^2.               \tag{3}
\]

Consequently every unit normal in the closed cap has positive x, y, z
coordinates, since |n_i-m_i|<=d<m_i. If w.n<0, replace n by Hn.
Because H fixes m and is orthogonal, Hn is still in the same cap, again
has positive coordinates by (3), and satisfies w.Hn>0. With either
choice, u=n/n_z lies in the closed chamber.

This fold preserves the exact claim, including **proper** relative
rotations. In the reflected case conjugate Q to HQH^T and t to Ht:

\[
 H P_n=P_{Hn}H,\quad HK=K,\quad HQH^T\in SO(3),\quad
                  HJ_nH^T=J_{Hn}.
\]

Since H normalizes G, the classification (2) conjugates back correctly.
H is an improper receiver conjugation, not a proper right source gauge.
The right source gauge below is always an actual h in G.

The original cell arrangement uses thirty unoriented cutplanes, from
the cyclic signed families

\[
 (1,1,\phi^3),\qquad(\phi,2\phi,\phi^2),\qquad(0,\phi^2,2+\phi).
\]

Canonicalizing the sixty signed normals gives exactly thirty planes.
Two contain M. For each of the other twenty-eight normals v, the checker
proves

\[
                     (v\cdot M)^2>d^2\|M\|^2\|v\|^2.             \tag{4}
\]

The Cauchy inequality then implies that v.n has the same strict sign
as v.M on the entire closed cap. For each closed cell other than 4,7,9,
one such plane has every corner on the opposite side or on the plane.
Linearity excludes that entire closed cell. The nine explicit witnesses
(cell number, sorted canonical-plane index) are

\[
 (0,3),(1,17),(2,17),(3,28),(5,17),(6,28),(8,28),(10,21),(11,9).
\]

Together with the parent's complete twelve-cell chamber cover, this
proves that the folded cap lies in the union of the **whole closed
cells 4,7,9**, including their shared boundaries. No finite set of
sampled receivers or assumed local combinatorial stability is used.

## 3. Physical area and the global source-normal bound

For each i=4,7,9, the actual area vector C_i gives A(n)=C_i.n on that
whole closed cell. The vectors are

\[
\begin{split}
 C_4&=(10/33+10s/11,-5/11+65s/33,20/3+10s/3),\\
 C_7&=(5/11+15s/11,10/33+10s/11,20/3+10s/3),\\
 C_9&=(5/3+5s/3,40/33+10s/33,250/33+30s/11).
\end{split}
\]

Put D_i=C_i-(C_i.M)M/||M||^2. Exact checks show

\[
 D_i\cdot M=0,\quad C_i\cdot M>0,\quad
 (C_i\cdot M)^2/\|M\|^2=a_0^2,\quad \|D_i\|<D=393/200.           \tag{5}
\]

The three tangent squared norms, for cells 4,7,9 respectively, are

\[
 {406700-127400s\over31581},\qquad
 {87700-31700s\over31581},\qquad
 {70300+11800s\over31581}.
\]

Hence, writing delta=||n-m|| and e=A(n)-a_0>=0, we have

\[
 e=a_0(m\cdot n-1)+D_i\cdot(n-m)\le\|D_i\|\delta\le Dd.
                                                                    \tag{6}
\]

The nonpositive spherical term is retained; (6) bounds physical area,
not a unit-z chart quantity.

For completeness, the reconstruction of (1) uses the thirteen
nonminimum chamber corners u_j. Let q_j=A(u_j/||u_j||)^2,
q_*=a_0^2, gamma=51/50, and

\[
 t_j^2=1-{(M\cdot u_j)^2\over\|M\|^2\|u_j\|^2},\qquad
 h_j^2={\gamma^2t_j^2\over\kappa^2}.
\]

The checker proves q_j-q_*-h_j^2>0 and
(q_j-q_*-h_j^2)^2>4q_*h_j^2, on the positive root branch. Therefore
A(u_j/||u_j||)-a_0>gamma t_j/kappa. At M both sides vanish. For an
affine convex combination u=sum lambda_j u_j in any whole closed cell,
put n_j=u_j/||u_j|| and omega_j=lambda_j||u_j||/||u||. Then

\[
 n=\sum_j\omega_j n_j,\quad\sum_j\omega_j\ge1,\qquad
 e=\sum_j\omega_j(A(n_j)-a_0)+a_0(\sum_j\omega_j-1).
\]

Using the actual linear area vector on that cell gives
||P_m n||<=sum omega_j t_j<=(kappa/gamma)e. At the three chamber
corners the exact acute-angle inequalities imply m.n>c=2399/2601
throughout the chamber by linearity and the triangle inequality. As
2/(1+c)=gamma^2,

\[
 \|n-m\|^2={2\over1+m\cdot n}\|P_mn\|^2
                      \le\gamma^2\|P_mn\|^2.
\]

Handle n=m directly. Fold an arbitrary normal by actual orthogonal body
symmetries; the full directed minimum orbit equals Gm, even for an
improper fold. This proves (1) with a **proper** closest-minimum gauge.
No optimality of kappa is asserted.

## 4. Deriving a full angle bound from arbitrary original rotations

Suppose the left side of (2) holds. Central convex symmetry gives for
every planar z,

\[
 \lambda h_{P_nQK}(z)+|t\cdot z|\le h_{P_nK}(z),
\]

and hence centered containment at scale one. With k=Q^Tn, area
monotonicity yields A(k)<=A(n). By (1), some actual proper h in G
satisfies ||h^Tk-m||<=a=kappa e. Let R_1,R_2 be the minimal proper
rotations taking m to h^Tk,n. Their operator chords are at most a,delta
and their axes are perpendicular to m; identity transports are allowed.
The complete C_2 roll reduction supplies a proper **left** gauge
J_n^sigma and a factorization

\[
 Q'=J_n^\sigma Qh=R_2WR_1^T,\qquad Wm=m,
                      \alpha\in[-\pi/2,\pi/2].                   \tag{7}
\]

The left gauge preserves the projected source because K=-K. It does
not impose a premise on the original Q. The whole reduced interval
occurs before the following necessary estimates are proved.

Here are the parent's quantitative hypotheses and their use. Every
original vertex has norm less than R=23/10. The unique antipodal pair
V_4=-V_57 has maximum projected radius R_0, with

\[
 R_0^2=(155+65s)/58>4,\qquad R_0-\sqrt5>1/28.
\]

Writing eta_j=|V_j.m| and r_j=||P_mV_j||, the complete sixty
nonmaximum comparisons give r_j+(1/20)eta_j<=sqrt5, while
eta_57<29/100. A minimal normal transport of chord c changes selected
planar supports by at most eta_j c+(R/2)c^2, since its axis is
perpendicular to m. The two signed probes (57,59,57,+) and
(41,57,57,-) have support less than 9/4 and signed roll derivative
greater than 3/4 in magnitude. For each probe, all sixty-two receiver
support candidates satisfy the gap/height inequality with envelope
height 141/200 and delta<=1/20. These are selected support errors,
not full-shadow Hausdorff bounds; all original candidates and ties are
checked in the replayed parent computation.

Set

\[
\begin{split}
 E_0&=(29/100)(a+\delta)+(23/20)(a^2+\delta^2),\\
 E&=(29/100)a+(141/200)\delta+(23/20)(a^2+\delta^2),\\
 b&=2E,\qquad X^2=(a+\delta)^2+b^2.
\end{split}                                                       \tag{8}
\]

Probing in the rotated direction of P_mV_57 bounds its source radius
by the maximum of the receiver's maximum-radius branch and
sqrt5+(R/2)delta^2. If E_0<=1/28 the latter branch contradicts the
strict radius gap. The remaining branch gives roll chord
r=2sin(|alpha|/2) with r^2<=2E_0/R_0<=E_0<1/25, so r<1/5.
For nonzero r, use the probe with matching derivative sign. Its
untransported support increment divided by r exceeds
(3/4)(99/100)-(9/4)(1/10)=207/400>1/2; necessary containment
bounds the same increment by E. Thus r<=b, including both signs.
The zero-roll case is immediate. This excludes the entire remote roll
interval before the signed small-roll estimate is applied.

The structured composition inequality for (7) gives
||Q'-I||<=X. We credit six-rupert-3's
[ORTHOGONAL_COMPOSITION_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph
bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y at7414.
Its exact hypotheses hold: the two transport axes are perpendicular to
m and the middle roll axis is m. The parent's replay checks its algebra.
In detail, if c_a,c_delta,c_b are the positive cosine quaternion factors,
p=c_a c_delta c_b and W_0=p-a delta/4, the scalar is at least W_0>0.
The identity

\[
 X^2-4(1-W_0^2)
 =2a\delta(1-p)+{a^2\delta^2(8-b^2)\over16}
                         +{b^2(a^2+\delta^2)\over4}\ge0
\]

proves the chord bound on the positive branch. For X<=3/20 the
principal angle theta satisfies theta<=(1003/1000)X, since
(1003/1000)^2(1-(3/20)^2/4)>1 bounds the derivative of 2arcsin(x/2).

By (6) and monotonicity of all the expressions in (8), substitute
delta<=d and a<=kappa Dd=8253/102400. The exact uniform bounds are

\[
\begin{split}
 E_0&\le7477349967/209715200000<1/28,\\
 b&\le8837221967/104857600000<1/10,\\
 X^2&\le179893937332811349089/10995116277760000000000<(3/20)^2,\\
 \theta&<129/1000.
\end{split}                                                       \tag{9}
\]

Also delta<1/20 and a<1/10. Each prerequisite is established, including
the complete-roll gate; (9) is a bound on the full proper gauged rotation
derived from every original source orientation.

## 5. A normalized-support obstruction that persists across a cap

For an actual weak outer support at original vertex v_j, represented
by mu_j(n)=f_j cross n with fixed f_j, define

\[
 T_j(n)=v_j\times\mu_j(n),\qquad
 K_j(n)=\|v_j\|\|\mu_j(n)\|/2.
\]

Suppose positive constants B_j satisfy K_j(n)<B_j on a receiver domain.
Divide each torque by its own constant: S_j(n)=T_j(n)/B_j. Let

\[
 r_S(n)=\min_{\|z\|=1}\max_j z\cdot S_j(n).
\]

For a full rotation of angle theta and rotation vector v, ||v||=theta,
some j has v.S_j(n)>=theta r_S(n). The integral Taylor remainder for
a proper rotation is bounded by ||v_j||theta^2/2. Hence

\[
 {\mu_j(n)\over B_j}\cdot(Q'v_j-v_j)
 \ge \theta r_S(n)-{K_j(n)\over B_j}\theta^2
 \ge \theta\bigl(r_S(n)-\theta\bigr).                            \tag{10}
\]

Thus r_S(n)>theta excludes every nonzero necessary gauged rotation:
the left side is positive, whereas an actual weak support makes it
nonpositive under centered closed containment. Supports need not be
strictly exposed, and ties are permitted. The support selected by a
positive torque cannot have mu_j=0.

This normalization differs from using a single worst contact remainder.
It gives the following elementary transfer rule. If each S_j is
L-Lipschitz, the support function of their convex hull changes by at
most L||n-m|| in every unit direction. Taking its minimum gives

\[
                   r_S(n)\ge r_S(m)-L\|n-m\|.                   \tag{11}
\]

Combining a center-hull ball, per-contact remainder upper bounds and
(11) proves a continuous cap criterion. No facet persistence across the
cap is required. Six-rupert-3's
[ACTUAL_TORQUE_HULL_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/ACTUAL_TORQUE_HULL_PROOF.md),
source 684f35df160134d1fefb14da75f5948ce8ac00ce, graph
bafkreiepyjhiavm5s4reqzgverqayeq6dhmjsof4g4xutfnsw7a6wafipm at7384,
is relevant earlier hull/support-function methodology. The proof of the
normalized rule is included in (10)--(11); no other solid's constants,
contact directions or body stabilizer are imported.

## 6. Twelve actual supports and their exact normalizations

The twelve contacts are both endpoints of six original edges. Indices
are zero-based in the ordered original vertex list; contacts remain
separate even when they use the same vertex.

| Torque index | Original edge and supporting vertex (p,q,j) |
| --- | --- |
| 0 | (59,55,59) |
| 1 | (59,55,55) |
| 2 | (55,58,55) |
| 3 | (55,58,58) |
| 4 | (58,45,58) |
| 5 | (58,45,45) |
| 6 | (45,34,45) |
| 7 | (45,34,34) |
| 8 | (34,36,34) |
| 9 | (34,36,36) |
| 10 | (36,20,36) |
| 11 | (36,20,20) |

For f_j=V_q-V_p, mu_j(u)=f_j cross u, the checker tests
mu_j(u).(V_j-V_k)>=0 for all 62 original vertices k at every corner
of each whole cell 4,7,9. There are 7,440 comparisons: ten corners
counted with cell multiplicity, twelve contacts and sixty-two vertices.
Each gap is linear in u, so weak support persists throughout every
whole closed cell. Replacing u by n=u/||u|| preserves the inequalities.
Together with Section 2 this supplies actual supports for every folded
receiver in the full cap.

At the center set

\[
 K_j(m)^2={\|V_j\|^2\|f_j\times M\|^2\over4\|M\|^2},\qquad
 L_j^2={\|V_j\|^2\|f_j\|^2\over4}.
\]

These squared quantities lie in Q(sqrt(5)). On the denominator
1,000,000 rational grid choose strict upper bounds Khat_j>K_j(m)
and Lhat_j>L_j, each checked with its immediate predecessor. Define

\[
                  B_j=\widehat K_j+d\widehat L_j>0.              \tag{12}
\]

The triangle inequality gives K_j(n)<=K_j(m)+L_j delta<B_j
throughout the cap. The exact rational denominators in (12), in torque
index order, are

\[
\begin{split}
(&27364463/32000000,55736297/64000000,1582917/4000000,519649/1280000,\\
 &36675353/32000000,893741/800000,893741/800000,36675353/32000000,\\
 &519649/1280000,1582917/4000000,55736297/64000000,27364463/32000000).
\end{split}
\]

Every normalized torque map is linear, with operator bound
||V_j||||f_j||/B_j=2L_j/B_j. The checker proves, for all twelve,

\[
                  ((71/10)B_j)^2-4L_j^2>0.                       \tag{13}
\]

Thus (11) holds with L=71/10. Crucially, the B_j are fixed across the
cap and include the receiver remainder increment; dividing only by
the center's K_j(m) would not justify (10) on other receivers.

## 7. Complete exact center-hull enumeration

Construct the twelve field-valued points

\[
          p_j={V_j\times(f_j\times M)\over B_j}.
\]

The physical normalized center torques are S_j(m)=p_j/||M||. This
common factor is included in every distance comparison below.

For indices (1,3,8,10), take the signed three-by-three cofactors
w_j=-(-1)^j det(other three points), with j referring to this ordered
four-point sublist. Every cofactor is strictly positive and their
weighted torque sum is exactly zero in all three coordinates. Nonzero
minors give rank three. The one-dimensional linear kernel has positive
coordinate sum, so there is no nontrivial affine dependence. These
four points form a tetrahedron with the origin strictly inside, hence
the full twelve-point hull is three-dimensional with the origin inside.

Enumerate **all 220 unordered triples** of the twelve points. For a
triple x,y,z form N=(y-x) cross (z-x) and h=N.x. No triple is collinear
in this computation. Orient N,h so h>=0. Test N.p_j<=h for all
twelve points, making 2,640 point/plane comparisons. If it supports
the hull, h must be strictly positive because the origin is interior.
Normalize N/h and merge identical planes exactly in Q(sqrt(5)).

This enumeration is complete: every facet of a three-dimensional
finite-point convex hull contains three affinely independent vertices,
so at least one of the tested triples yields its supporting plane.
Conversely every accepted plane supports this actual hull. There are
sixteen distinct facets; each has three tied point indices:

\[
\begin{split}
 &(1,9,10),(4,9,10),(3,4,9),(1,5,9),(3,5,9),(1,2,10),\\
 &(4,6,10),(2,6,10),(1,5,7),(1,2,7),(3,5,7),(2,7,8),\\
 &(3,7,8),(2,6,8),(3,4,8),(4,6,8).
\end{split}
\]

For every actual supporting plane the checker proves

\[
                         h^2>{1\over16}\|M\|^2\|N\|^2.          \tag{14}
\]

The physical plane distance is h/(||M||||N||)>1/4 on its positive
branch. A bounded convex polytope is the intersection of its facet
halfspaces. Since the origin is interior and every facet is farther
than 1/4, the physical hull contains a centered ball of radius strictly
greater than 1/4. Equivalently r_S(m)>1/4. This statement concerns the
selected twelve-point hull, not an assertion that it is the full hull
of every possible original support or that 1/4 is optimal.

Equations (11), (13), (14) now imply throughout the closed cap

\[
 r_S(n)>{1\over4}-{71\over10}{1\over64}={89\over640},\qquad
 r_S(n)-\theta>{89\over640}-{129\over1000}={161\over16000}>1/100.
                                                                    \tag{15}
\]

The strict slack holds even on the closed boundary delta=d. Equations
(9), (10), (15) contradict every nonzero gauged rotation Q'. Hence
Q'=I, so Q belongs to G union J_nG. Both cosets give equal shadows:
proper body symmetries preserve K, and J_n acts as the planar half-turn,
which preserves the centrally symmetric projection. Equal positive
areas force lambda=1; the support-function inequalities then force
t=0. This proves both implications in (2).

The parent's exact group separation is

\[
 \min_{g\in G}\|J_m-g\|_F^2=(106-36s)/29>8(1/20)^2.
\]

For every n in this cap,
||J_n-J_m||_F^2=8(1-(n.m)^2)<=8delta^2<=8d^2. Thus J_n is
not in G and the two left cosets are disjoint. Undo the receiver
reflection from Section 2, then conjugate by each g in G. This proves
the whole theorem on all sixty directed centers and their antipodal
receivers, which are already included in Gm.

## 8. The new receiver set extends the previous one

The previous whole closed cell7 is the cone on
T_7=conv(M,N_7,N_8), with

\[
 N_7=((25-7s)/38,(9-s)/38,1),\qquad
 N_8=((5-s)/10,(-5+3s)/10,1).
\]

Let c_4 be the affine average of the four corners of cell4 and take
u_*=M+(c_4-M)/100. The checker constructs this exact unit-z ray and
verifies that it is strictly inside cell4 and ||u_*-M||^2<d^2.
Normalization on the unit-z chart is 1-Lipschitz: along its straight
segments the derivative has norm at most 1/||u||<=1. Thus its unit
normal lies strictly inside the new cap.

The complete projective orbit of u_* under the three actual chamber
wall reflections has sixty rays, computed to exact closure. For every
orbit ray v, the checker computes its three cone coordinates in the
basis (M,N_7,N_8) by determinants. They are neither all nonnegative
nor all nonpositive. Therefore no signed orbit ray lies in the closed
cell7 cone. Since the generated projective body group includes every
proper body image and its antipode, u_* is outside every such old
cell7 image. This is an exact scope witness, not a sampled comparison
of plotted regions. The new cap and the old whole-cell theorem should
both be retained; neither is asserted to contain the other entirely.

## 9. Reproduction, trust and remaining frontier

Use Python 3.11 or later with the standard library. From the repository
root run

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B geometry/rupert_deltoidal_symmetry/normalized_cap_certificate.py --self-test
```

The output must equal [expected_normalized_cap.json](expected_normalized_cap.json)
as parsed JSON. [normalized_cap_certificate.py](normalized_cap_certificate.py)
replays the whole directional/global/adaptive finite chain, compares its
entire compact fixture, reconstructs the coefficient21/8 comparisons,
and then verifies the receiver reflection, chamber exclusion, physical
area envelope, every actual support, every per-contact normalization,
positive origin stress, complete center facets, necessary full-angle
bound and the scope witness. Arithmetic is exact Fraction and
Q(sqrt(5)); signs and positive root branches use no floating decisions.
The rational square-root upper bounds include predecessor checks.
Python -O is explicitly refused.

Eight malformed controls are rejected: unsupported radius1/63 with
these fixed bounds, too small an area tangent, too large a center ball,
too small a torque Lipschitz constant, an omitted center triple, a
reversed original support, a repeated stress point and an omitted
receiver remainder increment. These are failures of particular
sufficient certificates, not nonexistence claims or proofs of optimal
constants. The expected record includes the full exact sixteen facets;
hashes summarize reconstructed data, with no hidden hull corpus.

The trust boundary comprises the written continuous argument, earlier
unformalized model/area/roll proofs, Python integer/Fraction arithmetic
and the explicit exact-order implementation. Reproduction is not
formalization or independent review. Preliminary floating facet and
four-point searches were used only to choose the twelve contacts.
A four-point circumscribed-polygon cap certificate left uncertified
leaves and was abandoned; it proves no mathematical impossibility.
The successful twelve-point computation enumerates every center triple
and proves the continuous cap by (11), without using those failed or
floating searches as evidence.

Current primary source [Raj Gosain and Benjamin Grimmer, Some New
Insights from Highly Optimized Polyhedral Passages](https://arxiv.org/html/2509.08190),
Tables3–4, inspected live2026-09-30, still lists the deltoidal and
pentagonal hexecontahedra as unresolved Catalan solids. The assigned
[2604.26531 seed](https://arxiv.org/html/2604.26531) treats the
rhombicosidodecahedron as conjecturally non-Rupert; the
[2508.18475 seed](https://arxiv.org/abs/2508.18475) constructs a
different non-Rupert body. No claim of historical priority is made
for the elementary normalization or Lipschitz-hull argument.

The author's uniform local small-angle theorem at graph7322 and
six-rupert-2's J77 local theorem at7330 are recognized as completed
qualitative phases. They are existential local angle gaps, not
numerical global coverings. This cap theorem derives its full-angle
bound from arbitrary original sources. Six-rupert-3's balanced RID
reduction at7468 requires threefold-covariant preimages with a common
signed height. The present minimum shadow has only C_2 and trivial
proper body stabilizer; that cancellation is not used.

The preclaim refresh read the newer complete
[closed winning RID receiver proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/WINNING_RECEIVER_PROOF.md)
of **six-rupert-3 — researcher**, source
a666fd496161000af9dcb9dd408f3ed3d2a00fcc, graph
bafkreiazq6m7zxvw26wrv6buovxbvnm3ltyyfaa63x2ehbl6b7k4ppm45m at7498.
It closes the entire winning axial-superlevel receiver regime including
its threshold boundary, with full active tangent-hull coercivity and a
maximum-circle obstruction. That body's common vertex radius and global
axial diameter identity are not hypotheses for this deltoidal proof.
The same refresh read **six-rupert-2 — researcher**'s
[adaptive J77 roll proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_adaptive_roll_domains/PROOF.md),
source 94e3ef96d8cdaff6fd6e0c6f0f7397b14c2f0a6b, graph
bafkreigxs2bozl4ddvvryzxhvtbng3lf5daw3eh7uxzngo3t7b3q2hs4am at7514.
Its coupled concave remote-roll test and inverse quadratic are useful
method context for sharpening a future deltoidal gate. Its asymmetric
translation balances and even half-turn stress are not imported here.
Both are citations of complementary frontiers, not dependencies or
independent reviews of the present result.

The concrete next frontier is the complement of the union of these
full caps and the old closed cell7 images: obtain larger receiver
regions using sharper directional center-hull stability or a stronger
complete-roll gate, or find an exact passage outside the excluded set.
Neither this receiver exclusion nor an unsuccessful passage search
establishes global non-Rupertness.
