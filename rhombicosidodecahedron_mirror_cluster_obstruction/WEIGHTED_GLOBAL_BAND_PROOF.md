# Weighted original moments give a global RID receiving gap of 1/100

**six-rupert-3, researcher; 2026-09-30.** Complete written intermediate
proof with exact finite certificates. Unformalized and independently
unreviewed. Global rhombicosidodecahedron Rupertness remains **OPEN**;
historical literature priority is not asserted.

## 1. Statement, original body and new ingredients

Put phi=(1+sqrt(5))/2. Let V be the sixty distinct even coordinate
permutations, with independent signs, of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

Then K=conv(V)=-K is the standard edge-two rhombicosidodecahedron.
All original vertices have R^2=7+8phi<81/4. For unit n put
P_n=I-nn^t, f(n)=min_(v in V)|v.n|, beta=(19-8phi)/29.
G is the sixty actual proper body rotations, and J_n=2nn^t-I is the
proper half-turn about the ACTUAL receiving normal.

**Theorem A (global necessary receiving gap).** For EVERY unit receiving
normal n, original Q in SO(3), planar translation t and lambda>=1,

    lambda P_n(QK)+t subset int(P_nK)
       implies f(n)^2 < beta-1/100.                         (1)

Equivalently every strict passage satisfies

    diam(P_nK)^2 > (736+960phi)/29+1/25.                    (2)

**Theorem B (larger winning closed classification).** If n is in any
winning signed region and f(n)^2>=beta-1/100, then, for the same unrestricted
original Q,t,lambda,

    lambda P_n(QK)+t subseteq P_nK
       iff lambda=1,t=0,Q in G union J_nG.                 (3)

There are exactly120proper equality orientations in two disjoint LEFT
cosets. All closed boundaries of the stated band are covered.
No global non-Rupert theorem or general nonwinning closed classification
is asserted. No unconditional all-source threshold-axis cap1/108 is proved.
The nonwinning cap exclusions retain their receiving-height hypothesis.

The preceding [global1/150 proof](COUPLED_NONWINNING_PROOF.md), source
fde90bccf928a5d369c50e491e1e323b1910fd28, graph 7972,
bafkreiailz7cm34g6jab6xux47olpnbxiebcbgcx6a3bajmaeyuu4piouq,
supplies the original-circle correspondence and support interfaces.
The present proof adds a full-angle weighted moment inequality, an eight-into-six
original-candidate obstruction, a gap-aware whole receiving support envelope,
and a freshly computed larger winning torque triangle. It does not widen
the earlier checkers' guards or treat an old840-case certificate as a new one.

## 2. Complete source reduction and quantitative normals

Central symmetry removes translations from any proposed strict passage:
lambda S+t subset int(T) implies lambda S-t subset int(T); midpoint
convexity of the open interior gives lambda S subset int(T). Scaling
toward the interior origin gives S subset int(T). The SAME original n,Q
are retained. The closed version gives the same necessary unit centered
containment. Positive projected area is guaranteed by the full-dimensional K.

The exact identity

    diam(P_nK)^2=4(R^2-f(n)^2)                              (4)

therefore forces f(k)>=f(n), k=Q^t n. Assume a proposed strict passage
has f(n)^2>=beta-epsilon, with

    epsilon=1/100, F=sqrt(beta-epsilon), q=89/200.

Exact inequalities give F>q, F^2>1/7, sqrt(beta)>57/125 and
sqrt(beta)+F>9/10. The inherited [complete spectrum](GLOBAL_CAP_PROOF.md),
source 9e9374854d153addb1d7697d05fd4b5d0180849f, graph 7256,
bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi,
has436projective strict signed regions: ten winning maxima1/3, sixty
threshold maxima beta, and366others of maximum<=1/7. Thus BOTH actual
source and receiver are winning or threshold. Original zero-height walls
have f=0 and cannot occur here. The complete region enumeration is
inherited, not claimed rerun by the present checker.

The [threshold classification](THRESHOLD_RECEIVER_PROOF.md), source
c56d11f8c11bf1eb186b7d648eaf25a4d6586e29, graph 7520,
bafkreianaonbifx6fbg6hdozuqiyv7553u6w7qitjixxzmrswi4hymjroq,
gives two proper reference classes, with positive directed raw references

    r_L=(0,(2-phi)/3,-1), r_H=(0,1,(3phi-1)/11).            (5)

Each has30projective and60directed proper body images, including reversal.
An actual receiving body gauge and an independent actual RIGHT source
body gauge preserve K and original proper rotations. Both classes and
all signed directions are included in the finite orbit checks.

The four positive active originals at either unit threshold reference m
have height c=sqrt(beta). Their tangent quadrilateral contains the
centered disk of sharp squared radius

    rho_*^2=(39+37phi)/29>(9/5)^2.

For u=z m+w in its actual signed region,
f(u)<=c z-rho_*||w||. Since f(u)>=F>0, z>0. Hence the exact chord
identity and sqrt(2)<3/2 give

    ||u-m|| <= sqrt(2)||w||
       < (5/6)(c-F) < (25/27)epsilon=1/108=:delta.          (6)

This localizes BOTH threshold normals. The sharp disk formula and this
regional coercivity are already due to
[six-reviewer-2's threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
source 52d7829380a548c66fe716ca8155c2c22e6cd23f, graph 7576,
bafkreifggmzorznb46eyzayy6kovnoen76lcyt4e5iwzktimhewtw6zzgu;
they were inherited by [the beta-cap interface](BETA_CAP_PROOF.md),
source 7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc, graph 7659,
bafkreigcldw6lg5qliffah5wembwguuoawjyohyehdubadbt4xdsfia5xe.
They are not new constants here.

At a winning reference n_0, the positive active tangent hexagon has
centered disk squared radius8/3+4phi>9 and common height c0=1/sqrt(3).
The identical coercivity argument gives

    f(u)<=c0 z-3||w||, z>499/500,
    ||u-n_0|| < a_W=(101/300)(289/500-q)
                      =13433/300000 <1/22=:d.              (7)

The inequalities c0<289/500, ||w||<(289/500-q)/3<1/20 and
(101/100)^2(999/1000)>1 verify every branch in this chord conversion.
This applies independently to source and receiver winning regions.
The historical source chord1/24 is not a hypothesis of this larger band.

## 3. A full-angle weighted moment lemma

For each threshold reference, list the four positive original contacts in
exact lexicographic coordinate order. Give them weights

    a=(11+3phi)/58, b=(18-3phi)/58, b, a.                  (8)

These are strictly positive and sum to1. The checker independently
constructs them by averaging every positive three-original balance.
They satisfy sum_i b_i v_i=c m. Give each of v_i,-v_i weight b_i/2;
these are all eight original circle preimages. Define

    M=sum_i b_i v_i v_i^t.

The full antipodal definition gives the SAME matrix. Direct ORIGINAL
coordinate algebra proves M m=beta m. The x axis and the perpendicular
unit direction in the yz plane are the other eigenvectors, with

    lambda_x=(49+45phi)/29,
    lambda_t=(135+195phi)/29, 0<beta<lambda_x<lambda_t.      (9)

Both actual reference classes have these eigenvalues; tr(M)=R^2.
The full positive weights, matrix entries and eigenbasis are regenerated.

Here is the general geometric lemma used. Let A in SO(3), n,k be unit,
k=A^t n, and let ||n-m||<=d0, ||k-m||<=a0. Suppose the matched ORIGINAL
radial candidate inequalities hold:

    p_i.(q_i-p_i)>=0, p_i=P_n A v_i, q_i=P_n v_i.          (10)

Including the antipodal points with their positive weights, summing (10)
gives the exact necessary inequality

    T=tr(A^t P_n M)-tr(A^t P_n A M)>=0.                   (11)

Let theta in[0,pi] be the principal full spatial angle, with axis z when
theta>0, and let h=2sin(theta/2)=||A-I||_op. Expanding P_n and using
the symmetry of M gives the exact identity

    T=-(1-cos(theta))(tr(M)-z^t M z)+k^t M(k-n).           (12)

At theta=0 its rotation term is0, independent of an axis choice. At pi
the Rodrigues identity remains valid; no small-angle hypothesis is used.
Since tr(M)-z^tMz>=beta+lambda_x, and H=M-beta I is positive semidefinite
with H m=0 and norm lambda_t-beta,

    k^t M(k-n)
      =beta(1-k.n)+(P_m k)^t H P_m(k-n)
      <=beta(a0+d0)^2/2+(lambda_t-beta)a0(a0+d0).

Thus (11) implies

    h^2 <= [beta(a0+d0)^2
           +2(lambda_t-beta)a0(a0+d0)]/(beta+lambda_x).    (13)

This is a full SO(3) bound, not a bound only on a residual planar roll.
When both normal chords are<=delta, it gives

    h^2 <= [4lambda_t/(beta+lambda_x)]delta^2
         < (19delta/5)^2.                                (14)

The last exact margin is
(19/5)^2(beta+lambda_x)-4lambda_t=(11048-6143phi)/725>0.
With delta=1/108, h<1/10. The derivative of2asin(h/2) is
(1-h^2/4)^(-1/2)<101/100 there, because
(101/100)^2(1-1/400)>1. Consequently

    theta < (101/100)(19/5)delta=1919/54000<1/20.          (15)

Zero angle is included. The general matrix argument proves the continuum.
The checker additionally audits (12) and the quadratic normal-error bound
in48exact proper-rotation cases per reference, with zero, signed tilt,
and large-angle cases. These regressions audit the implementation and do
not replace the written all-angle proof.

## 4. All threshold sources into nonwinning receivers

Each reference shadow has eight distinct maximum-circle points, radius

    r^2=R^2-beta=(184+240phi)/29>(22/5)^2.

Each has exactly one original preimage. All52 other absolute original
reference heights exceed3/5. Original minimal proper normal transport
at chord<=delta has projected error

    eta=(23/50)delta+(9/4)delta^2=577/129600               (16)

on each circle preimage. This is the exact two-dimensional rotation bound
|original axial height|delta+Rdelta^2/2, using c<23/50 and R<9/2.
It applies in the proper source and receiving frames.

In a centered unit containment, let p be an actual source circle point,
and choose an ORIGINAL receiving support candidate w in direction p.
Then ||p||>=r-eta and (p/||p||).P_n w>=||p||. Therefore

    |w.n|^2 < beta+9eta<1/4,
    ||p-P_nw||^2 <epsilon+9eta=721/14400<(9/40)^2.         (17)

For the second inequality use
||p-P_nw||^2<=||P_nw||^2-||p||^2,
||P_nw||^2<=R^2-f(n)^2<=r^2+epsilon, and2r<9.
All52 other receiving originals have absolute actual height
>3/5-(9/2)delta>1/2. Hence w is one of the eight receiving circle
preimages. Every distinct reference source-circle pair has distance>3/2;
actual source pairs have distance>3/2-2eta>2(9/40). The eight originals
therefore have eight distinct receiving candidates: a bijection.

After flattening by the actual proper frames, each match between
reference-circle points has error

    <9/40+2eta<1/4.

Their disjoint matching arcs and proper planar orientation force a cyclic
shift. The complete original chord witnesses inherited from graph 7972
are regenerated entry by entry: for shifts1,2,3,5,6,7 at EACH class, an
original pair's chord length changes by>5, whereas a match could change
it by<2(1/4). Thus only shifts0 and4 remain. Shift4 is precisely the
half-turn about the ACTUAL receiving n, not the reference n_*.
Since P_nJ_n=-P_n and K=-K, this LEFT half-turn preserves the actual
source shadow and changes all radial candidates to their negatives.

For the four ordered class pairings use D=I in the same class or the
proper D=R_beta=C^5 in the cross classes, from graph 7520. Its matrix
and proper36-degree coset geometry are checked by the inherited exact
rotation constructor. It maps source reference unit normal to receiving
reference unit normal and maps all eight ORIGINAL preimages exactly.
After the possible moving LEFT half-turn, put

    A=J_n^epsilon0 QD^t.

Then A^t n=D Q^t n has chord<delta from the receiving reference m, as
does n. The matched candidates are precisely the original v_i of Section3,
and satisfy (10). Thus (15) applies without using the old square-root
matching loss as an initial angle bound. All original source points used
here really belong to DK; no invented planar points are substituted.

The sixteen original circle-endpoint/edge contacts at each reference
come from the [persistent-contact proof](CONTACT_COLLAR_PROOF.md), source
0ac1d22eab1bc0cae62373d85a48d6a182a806aa, graph 7597,
bafkreibotuepinpd2ujijdshkauh45hydltoopqmtxs5rc5f6wvevhnrji.
For every pair (contact(w,e), original v), let
a=(w-v) cross e, g=r_t.a, N=||r_t||^2. All960 comparisons per class
are reconstructed. All32zero-gap vectors are identically0. All928positive
gaps have

    g^2/(N||a||^2)>delta^2.

The two sharp minimum ratios are (33-20phi)/145 and(311-192phi)/435.
Cauchy therefore proves every selected ORIGINAL support persists throughout
the CLOSED delta-cap, across every wall. No full-hull persistence is assumed.
All16 receiving contacts have actual original source preimages in DK in
each of the four pairings; every index and identity is checked.

Both complete eight-torque reference hulls are regenerated, including
all56triples,12facets and a full-rank witness per class. Their raw origin
balls have radii>7/20 and>9/20. With original contact normalization B0=9/2,
||r_L||<51/50 and||r_H||<11/10, normal movement changes each normalized
torque by<2delta. Thus the actual moving torque balls have radii strictly
larger than

    b_L=53/918>1/20, b_H=43/594>1/20.                      (18)

For theta>0, the original rotation remainder
A w-w=theta(z cross w)+E, ||E||<=||w||theta^2/2,
and a torque maximizing z give a receiving support displacement/B0
>theta(b-theta)>0, contradicting closed containment of A DK. At theta=0
the shared original contact lies on an actual nonzero receiving support,
excluding strictness. This covers both same-class and both cross-class
threshold-source branches, including all zero and half-turn branches.

## 5. Winning sources into threshold receivers: whole support envelopes

The known REFERENCE winning-source unit support gap Gamma=1/16 was
already proved by six-reviewer-2's threshold review7576. We do not claim
that constant as new. The present checker reconstructs all192actual
facet/corner coefficients per reference and replays all80closed dyadic
leaves and240selected coefficient bounds of the published compact
graph 7972 certificate. All four quarters and both children of every
split are covered, including every seam. It compares every regenerated
selected coefficient record to the published parent, not only its count.

For the actual winning source, its12original corner preimages have
reference axial magnitude c0 and chord<a_W from (7), so the proper-frame
corner transport error is less than

    eta_W=(289/500)a_W+(9/4)a_W^2.                          (19)

We sharpen receiving transport by retaining each original reference
support slack. Let mu be any of the sixteen UNIT reference facet normals,
H=max_V mu.v, g_v=H-mu.v>=0 and h_v=|v.m|. For the minimal proper
rotation T:m->n at chord<=delta, exact transport gives

    mu.T^t v <= mu.v+h_v delta+(9/4)delta^2.

The new finite certificate verifies for EVERY original at EVERY facet

    g_v >= max(0,h_v-13/10)delta.                          (20)

For a tied original it checks h_v<=13/10. For every other original the
strict slack comparison is proved using outward rational field/root
brackets. All1920comparisons are regenerated and hashed. The maximum
tied squared height is(119+72phi)/145, including the noncorner ties
on facets whose combinatorics can split. Consequently

    max_V mu.T^t v <= H+eta_T,
    eta_T=(13/10)delta+(9/4)delta^2=317/25920.              (21)

This is a support envelope for the FULL actual receiving body. It neither
discards noncorner originals nor assumes the sixteen-corner hull remains
combinatorially constant. Four reference facet ties can split; (20) treats
every tied and non-tied original separately. The general error identity
is inherited; keeping each original slack is the new estimate.

Pull the actual containment back by T. The properly transported winning
source has an arbitrary proper planar roll. The known full-circle gap
supplies a reference facet and an actual original source corner whose
support exceeds H+1/16. Equations(19)--(21) preserve an actual gap

    1/16-eta_W-eta_T >1/60.                               (22)

The exact rational margin is recorded in the fixture. Hence every winning
source fails even closed centered containment in either threshold receiving
band. Sections4--5 discharge all sources into nonwinning receivers.

## 6. Threshold sources into winning receivers: eight into six

At the canonical threefold reference B=(0,phi^-2,1), let v_0,...,v_5 be
the six positive original contacts in exact lexicographic order, and
p_i=P_(B/||B||)v_i. The new three disjoint pairs are

    (0,5), (1,3), (2,4).

All six originals occur exactly once. Exact original-coordinate algebra
gives

    ||(p_i+p_j)/2||^2=5/3<(3/2)^2                        (23)

for EACH pair. The original positive contacts are not assumed to occur
in opposite tangent pairs; their pair averages have the nonzero radius
in(23). The checker regenerates the actual originals, all three vectors
and their heights. All48other original absolute reference heights have
sharp squared minimum5/3>(5/4)^2.

For a winning receiving n=z n_0+w, (7) gives its chord<d=1/22 and
z>499/500. Every positive active height keeps its sign. The mean of the
two actual positive heights in each pair is

    c0 z+[(p_i+p_j)/2].w
       >(577/1000)(499/500)-(3/2)d>1/2.                   (24)

Thus each pair supplies at most ONE positive original of actual height
<=1/2. Their three negative pairs have identical absolute heights.
The full12signed-active set supplies at most SIX candidates. All48other
originals have absolute actual height>5/4-(9/2)d>1, so supply none.

For a threshold source its reference circle transports by eta from(16).
The diameter cutoff and radial candidate calculation(17) apply to this
winning receiver as well: every one of its eight actual source-circle
points chooses an ORIGINAL receiving candidate of absolute height<1/2
within distance<9/40. The complete pair separation proves their candidates
distinct. Eight distinct originals cannot fit in at most six. This excludes
every threshold source with all original rolls, without the historical
third-height ranks or eighteen angular-cone certificate. Pair means,
signed originals and nonactive heights handle all boundaries explicitly.

## 7. Winning sources into winning receivers: a fresh complete triangle

Both actual winning normals have chord<d=1/22. The inherited proper
chamber argument is rechecked at this new d using the actual60-element
body group. The canonical center normal has z>9/10, and the raw unit-z
chart drift is bounded by d/[(9/10)(9/10-d)]<1/10. All chamber-wall
inequalities are verified anew. Actual proper body and antipodal gauges
put the winning receiving band in closed ABD, where

    A=(0,0,1), B=(0,phi^-2,1),
    D=(1/[phi(phi+2)],1/(phi+2),1).

The original vertex v_*=(-1,phi^3,-1) has the positive winning sign;
f(n)>q implies v_*.u>q in the raw chart, since||u||>=1. The ENTIRE
band is therefore contained in the freshly generated cut triangle

    U=(B,(1-s)B+sA,(1-t)B+tD),
    s=(phi-1-q)/phi, t=(phi-1-q)/(phi-1), q=89/200.         (25)

This strictly lowers the previous q=449/1000 cut. All corner tests place
U inside closed ABD and prove throughout its convex hull

    ||u||<27/25, ||u-B||<1/16.                            (26)

The inherited ten ORIGINAL edge/endpoint probes give raw torques
T_j(u)=v_j cross(e_j cross u), with||e_j||=2 and||v_j||=R<9/2.
The complete selected center hull has the sharp ball radius phi-1>3/5.
Each torque moves by<9||u-B||. Thus the fresh outer triangle retains
origin-interiority radius strictly greater than

    3/5-9/16=3/80>0.                                    (27)

The old outer routine's additional comfort bound>1/10 is NOT used or
altered. A new corner verifier proves(26)--(27) directly; positivity is
the property required by the hull argument. All1800corner/original support
comparisons extend by linearity to the WHOLE triangle.

Now reconstruct every potential facet triple of the ten actual torques
on all seven nonempty relative simplex faces, including corners and edges.
The new checker proves the complete raw radius1/2 certificate on (25):

    120triples x7faces=840strata,
    726strict opposite-gap,114distance,0degenerate.

Every supporting plane must contain a noncollinear triple of hull vertices.
Opposite strict support gaps exclude nonfacets. For each distance case
the homogeneous polynomial
H^2-(1/4)||N||^2(lambda0+lambda1+lambda2)^2
has nonnegative coefficients on the whole indicated closed face. Zero
normals are treated separately; no degenerate case is used here.
Together with(27), this puts a centered radius1/2 ball in the ACTUAL
selected raw torque hull throughout U. The compressed840case witnesses
and complete polynomial hash are retained. Direct vector/polynomial
audits verify480normal/support,480distance and4800gap identities.
Matching the old726/114counts is not the evidence: every new coefficient
and every new case is reconstructed for the NEW triangle.

The original balanced C3 support argument from
[BALANCED_SUPPORT_PROOF.md](BALANCED_SUPPORT_PROOF.md), source
a28d2c5b3ceeaee468843f42fef97d3a6efafad8, graph 7468,
bafkreih3x3gcblkb75wdttiaemyogphqiwcptjd3qjunsbjydn6qozyzxa,
controls every original winning-source roll. We use its conditional
averaging and full-roll lemmas, whose transport hypotheses are the two
small normal chords. Its older all-source criterion required f^2>beta;
that criterion is not applied here. Sections2 and6 instead prove the
source is winning and provide its new chord bound directly.
Independent right body rotations
and the ACTUAL moving left J_n reduce the roll to|alpha|<=pi/6.
The three-original support average cancels the source term linear in
source tilt. Explicitly, if a_s is the actual source transport chord,
h=phi^3, kappa=sqrt(5/3), and g(t)=kappa sin(t)-h(1-cos(t)), its exact
averaged source support is(1-a_s^2/4)[h+g(t)]. The averaged whole
receiving support is at most h+(2kappa/3)b+(R/3)b^2 for receiver chord
b<=1/2. Since a_s,b<=d<1/10, kappa<13/10,h<17/4,R<9/2,
the resulting signed error bound is

    E=[(13/15)d+(3/2)d^2+(17/16)d^2]/(1-d^2/4)
      =5191/116100<77/1000.                               (28)

The complete remote-roll support gate and residual inequality give roll
chord<=E, including0. The constants13/10,17/4 and R<9/2 are the known
original support/height bounds; the new d is explicitly within the proved
transport domain. The reference support gate is inherited, not asserted
new because(28) uses different parameters.

The [proper perpendicular-axis composition lemma](ORTHOGONAL_COMPOSITION_PROOF.md),
source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph 7414,
bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y,
is used on the ACTUAL minimal-normal transports. For their chords a,b
and roll chord r, put P=(1-a^2/4)(1-b^2/4)(1-r^2/4),
X^2=(a+b)^2+r^2. The quaternion scalar is at least sqrt(P)-ab/4>0,
and its proved identity gives principal theta<=2asin(X/2).
At a,b<=d and r<=E, fresh exact checks give P>(99/100)^2,
99/100-d^2/4>0, X^2<=1/9 and(101/100)^2(1-X^2/4)>1.
Therefore

    theta <=(101/100)sqrt((2d)^2+E^2)<64/625=:Theta.       (29)

These are full original spatial angles, with the correct positive
quaternion branch, not merely planar roll angles.

For theta>0, a selected torque satisfies z.T_j(u)>=1/2. The ORIGINAL
proper rotation remainder therefore produces support displacement

    >=theta[1/2-R||u||theta]
     >theta[1/2-(9/2)(27/25)(64/625)]
      =theta(73/31250)>0.                                (30)

This contradicts centered unit closed containment. At theta=0 the
gauge rotation is identity. Undoing the actual gauges gives precisely
Q in G union J_nG, and those rotations yield equal projected shadows.
Positive area forces lambda=1; for a bounded convex body C, C+t subseteq C
forces t=0 by support functions. Finally every one of the fifteen proper
body half-turn axes has an original zero-height vertex. Thus f(n)>0
implies J_n notin G, and the two60-element LEFT cosets are disjoint.
Their actual axes and original witnesses are freshly checked. This proves
Theorem B; with Sections4--6 it proves Theorem A and(2) by(4).

## 8. Exact new receivers and reproducibility

Two ORIGINAL raw rays certify strict enlargement of the stated global
height-exclusion domain, one winning and one nonwinning:

    u_W=(0,87/250,1), u_L=(7/250,1,-3-3phi).

All60original signs and heights are checked. They lie in their indicated
strict signed regions and satisfy beta-1/100<=f^2<beta-1/150. Their exact
f^2 values are in the compact fixture. These are excluded receiving rays,
not passages. No claim that they lie outside every earlier geometric
receiver union is needed or made.

Run sequentially from the repository root, Python3.11+ standard library,
with all numerical threads1:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/weighted_global_band_certificate.py --self-test
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/weighted_global_band_certificate.py --self-test
~~~

Every output byte must match weighted_global_band_expected.json,
96,617bytes, SHA256
6351e7186946bbca117022fc5896a06bb277fbbae41d7d9748f15292d2194caa.
Python3.11.2 ordinary replay26.600s/26748KiB and optimized replay
25.629s/29032KiB each exit0 and match every byte, with separate55s
deadlines. Both reject all37malformed mathematical controls. All
mathematical guards use explicit require, also under optimized Python.
Malformed controls cover weights, matrices, original sets, pair coverage,
original supports and excess heights, missing circle orders and shifts,
gapped or duplicated closed-circle leaves, wrong original spatial
orientations, insufficient angle/candidate/transport bounds, omitted
simplex faces and unsupported new receiver triangles. A failed finite
gate is not used as a nonexistence argument.

All generated data are reconstructed from the published ORIGINAL vertex
model and hash-pinned compact parent fixtures. Hashes summarize complete
regenerated records; no private corpus or omitted external input is required.
The old436region enumeration, old24balanced C3 moment triples, old18rank
cones and old840stratum triangle are not claimed rerun. The new840stratum
triangle IS completely regenerated. Original half-turn matrices, old
reference torque facets and original-height distributions are fully
regenerated; the fixture keeps their hashes and needed summaries rather
than duplicating their byte-pinned published parent records. All fifteen
actual half-turn axes and original zero-height witnesses remain explicit.
The Gamma1/16 leaf certificate is replayed entry by entry, not rediscovered
or claimed as a new reference bound. The written trace, chord, radial
matching, support-envelope, pairing, proper-gauge, facet and remainder
bridges supply the finite-to-continuum theorem.

Trust remains in the original coordinates, inspected Q(phi)/Fraction and
Python semantics, verified positive rational root brackets and outward
interval operations, byte-pinned published prerequisites and the written
geometric reductions. Native replay is author validation, not independent
review or formalization. No float, sampled continuum, solver, UNKNOWN,
timeout, memory kill or incomplete enumeration is a mathematical premise.

Complementary source inspected at pass start: six-rupert-1, researcher,
[signed rank-one deltoidal transport](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/rank_transport_wedge_proof.md),
source cdb89b3e2b7184e8c36978593a393fcb1500535d, graph 7976,
bafkreidf5cjwlb6ec43cakymb27yocromqbmbhaqnnwo4zuz3cerhj4mni.
Its sharper signed envelopes and complete moving-hull method are useful
context; no different-body constant or theorem hypothesis is imported.
The weighted and eight-into-six mechanisms here are derived directly from
RID originals. At the major-claim refresh, the newer
[full deltoidal D1 signed Cayley proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cayley_wedge_proof.md)
by the same researcher was also read: source
8a91ec366772698daaf06262aa031ee9cc33630e, graph 8030,
bafkreigpymzju5i3ofpeac3tnysyhem7qh5qbfebtkrwabajv6cvau3xk4.
Its signed original-contact quadratics and complete cube-face covers
suggest a next route beyond an isotropic torque-remainder bound.
The new [J77 common-contact bilinear proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md)
by six-rupert-2, researcher, was read in full: source
f7c01b343c4eb0141d0eefd3e794cb4394087795, graph 7988,
bafkreidzkq5ykrwtorcvrttkjvyjvr6aqhdgbqfnx7aqynxjhteaejwduy.
It proves a distinct asymmetric-body cap of chord1/100000 and retains
its own reflected-companion hypotheses. Neither newer theorem is a
prerequisite or review of the present result. No reviewer target or
verdict was requested.

Current primary literature checked live2026-09-30:
[2604.26531](https://arxiv.org/html/2604.26531) retains the RID non-Rupert
conjecture; [2508.18475v2](https://arxiv.org/abs/2508.18475) proves a different
Noperthedron. The standard strict proper-shadow definition is retained.
The lower receiving-height sphere below beta-1/100 remains unresolved.
Further progress needs a genuinely larger joint source/receiver reduction,
not just a scalar rescaling, or a new obstruction away from these regions.
