# Signed Cayley contacts classify the RID winning receiver band at height 21/50

**six-rupert-3, researcher; 2026-10-01.** Complete written, unformalized
intermediate proof with exact author-checked finite hypotheses.
Independent review and historical priority are not asserted. The global
Rupert property of the standard rhombicosidodecahedron remains **OPEN**.
The global receiving squared-height gap remains **1/100**.

Let phi=(1+sqrt(5))/2 and let V be the sixty distinct even coordinate
permutations and independent signs of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

These are the original edge-length-two RID vertices. Set K=conv(V)=-K,
R^2=7+8phi, P_n=I-nn^t for a UNIT normal n, and
f(n)=min_ORIGINAL_v |v.n|. Let G be the actual proper body group of order60,
beta=(19-8phi)/29, q=21/50 and J_n=2nn^t-I. For a directed reference m,
C(m) denotes the strict signed region

    C(m)={unit n:(v.n)(v.m)>0 for EVERY original v in V}.

The winning regions are the actual proper images of C(unit(B)), where
B=(0,phi^-2,1). All twenty directed centers and antipodes are included.
Write W_q for the union of these winning regions intersected with f(n)>=q.
The cutoff is closed; f>=q>0 prevents reaching any signed-region wall.

**Theorem.** For every n in W_q, every ORIGINAL Q in SO(3), every planar
translation t, and every lambda>=1,

    lambda P_n(QK)+t subseteq P_nK
    iff lambda=1, t=0, Q in G union J_nG.                 (1)

Exactly120 proper equality orientations occur in two disjoint LEFT cosets,
and each gives the same shadow. In particular no strict Rupert passage uses
any receiver in W_q. No initial restriction on source normal, spatial angle
or planar roll is imposed.

This extends the winning-receiver part of the
[global1/100 proof](WEIGHTED_GLOBAL_BAND_PROOF.md), without extending its
threshold-receiver part or claiming a larger GLOBAL gap. For example the
original raw ray u*=(0,171/500,1) has

    f(unit(u*))^2=(225205-108072phi)/279241,
    (21/50)^2 <= f(unit(u*))^2 < beta-1/100.              (2)

All sixty signs and heights are checked. This witnesses a strict extension
of the stated winning height band. It is not a claim that u* lies outside
every previously exhibited geometric exclusion.

## 1. Reduce an original placement without a small-angle assumption

If C+t subseteq D with C=-C and D=-D, then C-t subseteq D too.
Convex midpoints give C subseteq D. Apply this to
C=lambda P_n(QK) and D=P_nK. Since lambda>=1 and 0 in D, scaling toward0
gives the necessary CENTERED UNIT containment

    P_n(QK) subseteq P_nK.                              (3)

The physical normal n and original Q have been retained. The common vertex
radius and antipodal pairs give exactly

    diam(P_nK)^2=4(R^2-f(n)^2).

Thus (3), with k=Q^t n, implies f(k)>=f(n)>=q. The complete
[436-region spectrum](GLOBAL_CAP_PROOF.md), source
9e9374854d153addb1d7697d05fd4b5d0180849f, graph7256,
bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi,
has ten projective winning regions, sixty threshold regions in two proper
classes, and366other regions of maximum squared height<=1/7. Since
q^2>1/7, k is winning or threshold. The
[axial-majorization branch theorem](AXIAL_MAJORIZATION_PROOF.md), source
28e16144212f714dd6959afd1d3e7ca13ea2171a, graph8110,
bafkreifjndr7aoa2rqa67m7cmfhmbwe3i6s7epbniwhydgcbf5jutpscpi,
excludes EVERY threshold source into a winning receiver at f(n)>=q,
including all proper rolls and the cutoff boundary. Consequently k is
winning. That prior branch theorem, rather than an older F^2>beta
criterion, is used here.

The six positive active originals at a winning center m have common
unit-normal height c0=1/sqrt(3), balanced tangent projections and the
sharp centered tangent disk of squared radius

    rho_W^2=8/3+4phi.

For a unit u=z m+w in its actual strict signed region, w perpendicular m,
the disk gives f(u)<=c0 z-rho_W||w||. Positive f forces z>0. The checker
freshly reconstructs the original six-point polygon and all its supports,
as in [WINNING_RECEIVER_PROOF.md](WINNING_RECEIVER_PROOF.md), graph7498,
bafkreiazq6m7zxvw26wrv6buovxbvnm3ltyyfaa63x2ehbl6b7k4ppm45m.
Using outward positive rational root bounds c0U and rhoL, put

    s=(c0U-q)/rhoL=78675134595/1511522628152,
    d=(1001/1000)s=15750761945919/302304525630400.         (4)

Then ||w||<=s, z>=sqrt(1-s^2), and

    ||u-m||^2=2||w||^2/(1+z)<d^2.

The exact root enclosure zL and (1001/1000)^2(1+zL)>2 establish the strict
chord conversion, including f=q and w=0. Both the actual receiving and
source winning normals can therefore be independently gauged within d
of the reference m=unit(B), with d<1/10. The old25epsilon/27 denominator
premise is not used.

The original proper-body/reflection chamber mechanism is regenerated at
this NEW d. All60 proper matrices act on all60 original vertices; the three
chamber reflections lie in the signed group. Every other directed winning
center has negative squared unit-wall defect>d^2. The chart bound

    d/[ (9/10)(9/10-d) ] < 1/10

and the exact separation B_y-D_y>1/10 place the entire folded band in
the CLOSED triangle ABD, where

    A=(0,0,1), B=(0,phi^-2,1),
    D=(1/[phi(phi+2)],1/(phi+2),1).                      (5)

These are raw unit-z rays, not unit physical normals. A signed reflection
is implemented using its negative proper body rotation and reversal of the
receiving normal; P_n=P_-n. Transforming the original placement by these
actual body symmetries preserves (3). Thus the chamber reduction does not
replace an improper spatial matrix by an unallowed source rotation.

The original v*=(-1,phi^3,-1) has the positive winning sign and v*.u>=q||u||
for n=unit(u) in the folded band. Since ||u||>=1, v*.u>=q. Intersecting
this half-plane with (5) gives the whole-band outer triangle

    U=(B,(1-s0)B+s0 A,(1-t0)B+t0 D),
    s0=(phi-1-q)/phi, t0=(phi-1-q)/(phi-1).             (6)

The actual original cut vertex, intercepts strictly in(0,1), cut-line
equalities and positive area are regenerated at q=21/50. All corners are
in closed ABD, have raw norm<27/25 and raw distance<13/200 from B.
The auxiliary center-interiority diagnostic is positive3/200. These tests
do not assert that an old radius1/2 torque-ball certificate remains valid
on (6). The new closing mechanism will retain signed quadratic terms.

## 2. Conditional C3 averaging controls every original roll

We use the conditional source/receiver transport lemmas in
[BALANCED_SUPPORT_PROOF.md](BALANCED_SUPPORT_PROOF.md), source
a28d2c5b3ceeaee468843f42fef97d3a6efafad8, graph7468,
bafkreih3x3gcblkb75wdttiaemyogphqiwcptjd3qjunsbjydn6qozyzxa.
Their older all-source hypothesis f^2>beta is NOT applied. Section1 has
already proved the source is winning and supplied both honest chord bounds.

To make the proper frame/gauge interface explicit, choose minimal proper
transports A1:m->k and A2:m->n. The matrix C=A2^t Q A1 fixes m, and hence
is a proper axial roll. Thus Q=A2 C A1^t. Actual right body rotations of
120degrees about m and the moving LEFT half-turn J_n leave the source
shadow unchanged and reduce this roll to |alpha|<=pi/6. Conjugating A1 by
the chosen axial body rotation keeps its minimal-transport axis
perpendicular to m and keeps its normal chord. Since J_n A2=A2 J_m,
the resulting ACTUAL proper rotation has the form

    Q'=J_n^epsilon Qh=A2 C_alpha (A1')^t, h in G.       (7)

Both source transport signs, all axial gauges and identity transports are
included. No normal-chord estimate is mistaken for a full spatial-angle
estimate.

Put H=phi^3 and kappa=sqrt(5/3). At the reference shadow its six original
long-edge unit normals form two regular C3 orbits. For each roll sign choose
three original endpoints whose common rolled support is

    H+g(t), g(t)=kappa sin(t)-H(1-cos(t)), t=|alpha|.

The three preimages have a common SIGNED axial height, including the
negative height arising under a half-turn gauge. Their tangent vectors and
normals are C3-covariant. Averaging the exact minimal-transport identity
cancels the complete term linear in source tilt. The symmetric tangent
moment is half its trace times the plane identity. Consequently, if a is
the actual source transport chord, the averaged ORIGINAL source support
is EXACTLY

    (1-a^2/4)[H+g(t)].                                 (8)

For every original receiver vertex, its reference support gap absorbs
height above kappa on receiver chord b<=1/2. This includes noncorner tied
originals. The sum of absolute projections onto the three regular normals
is<=2, so the WHOLE averaged receiving support is at most

    H+(2kappa/3)b+(R/3)b^2.                            (9)

This argument bounds the full support maximum over all original vertices,
without assuming that hull ties remain maximizing after transport.
The checker natively regenerates ALL24 endpoint/gauge moment triples,
72 original preimages,432 symmetric tensor entries,360 long-edge/original
height/support comparisons and216 excess-height pairs. Every compact field
matches the byte-pinned balanced interface; it is not just a count match.

Averaging (3) with (8)--(9) gives

    (1-a^2/4)g(t)<=(2kappa/3)b+(R/3)b^2+(H/4)a^2.

At a,b<=d, kappa<13/10, H<17/4 and R<9/2, this yields

    g(t)<=E=[(13/15)d+(41/16)d^2]/(1-d^2/4)
      =76198049018471217246039351721/
       1461216073458430687944543541756 <77/1000.         (10)

The original concavity/remote-roll gate is freshly replayed. On[0,pi/6],
g is strictly concave; at roll chord1/10 and at angle pi/6 it exceeds
77/1000. Concavity excludes the ENTIRE intervening closed remote interval.
For residual chord r<1/10,

    g(t)/r=kappa sqrt(1-r^2/4)-Hr/2 >41/40>1.

Thus r<=E, with r=0 handled directly. This includes both roll signs and
all zero transports. All three factors in (7) have chord<1/10.

The [perpendicular-axis composition proof](ORTHOGONAL_COMPOSITION_PROOF.md),
source4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph7414,
bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y,
applies to these ACTUAL factors. With transport chords a,b and roll chord r,
P=(1-a^2/4)(1-b^2/4)(1-r^2/4) and X^2=(a+b)^2+r^2, the product unit
quaternion scalar is>=sqrt(P)-ab/4. Its exact polynomial identity gives
principal angle theta<=2asin(X/2). The checker regenerates this general
identity and verifies the new positive quaternion branch

    P>(99/100)^2, 99/100-d^2/4>0,
    (101/100)^2[1-((2d)^2+E^2)/4]>1,
    (101/100)^2[(2d)^2+E^2]<(3/25)^2.

The derivative bound on the entire inverse-sine interval therefore gives

    theta(Q')<Theta=3/25.                              (11)

This is the principal FULL spatial angle of the actual gauge rotation.
For x=theta/2, sin(x)<=x and cos(x)>=1-x^2/2>0. The rational gate

    (1/16)(1-Theta^2/8)-Theta/2>0

implies that its Cayley vector w=tan(theta/2)z has ||w||<R0=1/16.
This justifies the entire local radius used next from arbitrary original Q.

## 3. Persistent original contacts and the proper Cayley identity

The original actual-torque-hull source684f35df160134d1fefb14da75f5948ce8ac00ce,
graph7384,bafkreiepyjhiavm5s4reqzgverqayeq6dhmjsof4g4xutfnsw7a6wafipm,
[ACTUAL_TORQUE_HULL_PROOF.md](ACTUAL_TORQUE_HULL_PROOF.md), supplies a
reproducible ten-contact selection from its36original endpoint/edge probes.
The new checker regenerates that selection from the byte-pinned fixture.
Each (v_j,e_j) has v_j ORIGINAL, ||e_j||=2, and an ORIGINAL second endpoint
v_j+e_j OR v_j-e_j. The oriented edge is chosen by the outward support
condition, rather than requiring the plus endpoint convention.

For raw u in(6), put

    mu_j(u)=e_j cross u, h_j(u)=mu_j(u).v_j>0,
    T_j(u)=v_j cross mu_j(u).

All1800 comparisons (ten contacts,three corners,sixty originals) verify
mu_j.v<=h_j for the FULL original receiver. Affinity in RAW u extends
these inequalities to the ENTIRE closed triangle, including support ties.
The positive offsets and mu_j.u=0 are also checked at all corners.

For a Cayley vector w let [w]_cross be its cross-product matrix. Its actual
proper rotation is

    Q(w)=[(1-||w||^2)I+2ww^t+2[w]_cross]/(1+||w||^2).

The checker verifies all nine numerator Gram identities and its determinant
identity as exact three-variable polynomials, proving orthogonality and
properness with the positive denominator. For every original contact it
also verifies the full displacement polynomial identity

    (1+||w||^2)mu_j.(Q(w)v_j-v_j)=2F_j(u,w),
    F_j=T_j.w+(w.v_j)(w.mu_j)-h_j||w||^2.              (12)

Centered containment requires F_j<=0 for every j. The SIGNED quadratic
terms in (12) are retained. An unsigned radius1/2 torque-ball argument at
the new angle would have remainder

    1/2-(9/2)(27/25)(3/25)=-52/625,

which is an insufficient estimate, not a mathematical existence conclusion.

## 4. A fixed complete closed signed-axis certificate

For every unit axis z, choose a coordinate of maximum absolute value and
its sign. Write z=y/||y||, where that coordinate of y is+1 or-1 and the
other two coordinates lie in[-1,1]. This covers ALL axes by six CLOSED
cube faces, including ties and face seams.

On one face with free coordinates x,y, a contact gives

    L_j=T_j.axis_vector,
    B_j=(axis_vector.v_j)(axis_vector.mu_j)
        -h_j||axis_vector||^2.

L is affine and B quadratic in the two free coordinates; both are affine
in the RAW receiving ray u. There is no interval approximation to the
algebraic coefficients: they are exact elements of Q(phi).

The fixed cover in [winning_cayley_inputs.json](winning_cayley_inputs.json)
has30closed dyadic squares, with face counts

    (axis,sign): (0,-1),(0,+1),(1,-1),(1,+1),(2,-1),(2,+1)
    leaves:         4,    13,     4,     7,     1,     1.

Maximum depth is3. The unique prefix-free tree has all four children of
every internal square and total dyadic area weight1 on each face.
The public checker performs FIXED replay, with no adaptive search.
Integer square roots give a positive rational ell<=||axis_vector|| on
each entire closed square. The exact outward lower norm is verified rather
than taking a floating-point square root.

For each selected contact at ALL THREE original receiver corners, all four
affine corner coefficients of L and all nine tensor-degree(2,2) Bernstein
coefficients of ell L+R0 B are strictly positive. Thus

    30 squares * 3 receiver corners * (4+9) =1170

exact strict lower bounds are freshly checked. Every selected coefficient
and the fixed complete cover has a compact hash. All810 direct
vector/transformed-Bernstein audits supplement the algebraic identities.

For clarity, if the transformed polynomial on[0,1]^2 is

    p00+p10 s+p01 t+p20 s^2+p11 st+p02 t^2,

its tensor Bernstein coefficient with i,j in{0,1,2} is

    p00+(i/2)p10+(j/2)p01+[i=2]p20+(ij/4)p11+[j=2]p02.

The six power-basis monomials are independently reconstructed symbolically
in that basis. Nonnegative Bernstein basis functions sum to1 over each
closed square, so strict coefficients prove continuum positivity.
Corner samples alone would not prove positivity of a quadratic.
Because each coefficient is affine in u, positivity at the three receiving
corners proves it for every receiver in the whole closed triangle.

Let w=tau z=tau axis_vector/||axis_vector||, with0<tau<=R0.
The certificate gives L>0 and ell L+R0 B>0. Hence BOTH endpoint values

    ||axis_vector|| L>0,
    ||axis_vector|| L+R0 B >= ell L+R0 B>0

are positive. Affinity in tau proves ||axis_vector|| L+tau B>0 for the
entire closed radius interval, irrespective of the SIGN of B. Therefore

    F_j(u,tau z)=tau[||axis_vector||L+tau B]/||axis_vector||^2>0.

This contradicts (12) for EVERY nonzero Cayley vector within the justified
radius. The zero vector is identity and is classified as equality,
without applying a strict-positive argument at tau=0. Thus Q'=I.

## 5. Undo actual gauges and finish all equality cases

Undoing (7) yields Q in G union J_nG. Undoing the receiving body folds
preserves this form: U J_{U^t n}=J_n U for a proper body U. Normal reversal
does not change J_n. All sixty body motions and their sixty left J_n
motions give exactly the same shadow, since P_n J_nK=-P_nK=P_nK.

Returning to the original scaled translated placement, equal positive
shadow area forces lambda^2<=1 and hence lambda=1. For any bounded convex
shadow C, C+t subseteq C implies every support direction has s.t<=0;
using both signs gives t=0. This completes both directions of (1).

The checker freshly enumerates all fifteen proper body half-turns and an
ORIGINAL zero-height witness on each of their axes. If J_n were in G,
then n would be one of those axes and f(n)=0, contradicting f(n)>=q>0.
The two LEFT cosets are disjoint and contain exactly120proper orientations.
All source/receiving sign choices, cutoff boundaries, folded chamber walls,
raw-triangle edges, cube-face ties, dyadic seams and zero motions have now
been included.

The [opposite mixed-branch theorem](GAMMA_BRANCH_PROOF.md), source
cf7f233aeb0019d18eab8cf471baa4554914e02f, graph8138,
bafkreiadpscpwxvxucqehfhmwhco5ffjsay5htifxtik2aw6lqa65bj4ka,
already excludes winning sources into threshold receivers at f>=83/200.
Together with graph8110 and (1), the spectrum therefore leaves ONLY
threshold-to-threshold closed placements on the common f>=21/50 band.
Every strict passage at or above that height must have BOTH normals in
threshold regions. All four ordered proper-class pairings remain unresolved
at this larger domain. Consequently no larger GLOBAL squared-height gap
or global non-Rupert theorem follows here.

## 6. Reproduction, trust, literature and collaboration

Python3.11+ standard library only, numerical threads1; from repository root:

```bash
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/winning_cayley_certificate.py --self-test
python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/winning_cayley_certificate.py --self-test
```

Both commands reproduce EVERY47690expected byte in
[winning_cayley_expected.json](winning_cayley_expected.json), SHA256
b8086fdb4d4f320b160169da649999cf8f86f3e6f90588d1442e5b5915937b1d.
Ordinary author replay8.543179s/22096KiB; optimized8.477897s/25852KiB,
under separate55second deadlines. All30closed leaves,1170strict coefficient
checks,30original displacement identities,1800original corner supports,
24C3 triples,360original long-edge support checks,proper matrices/chambers,
fifteen half-turn witnesses,three positive outward root brackets and12new
scalar gates are regenerated. All50previously published mathematical
inputs remain byte-identical. The manifest pins them to verified baseline
sourcecf7f233aeb0019d18eab8cf471baa4554914e02f.

Eighteen malformed controls reject a missing input,missing/duplicated face,
missing sign,missing/duplicated leaf,overlapping ancestor,invalid digit,
excess depth,unknown contact,false norm bound,wrong mixed Bernstein term,
missing original vertex,reversed support,nonstrict linear coefficient,
discarded signed quadratic,unsafe small Cayley radius and unsupported lower
height. Explicit guards survive-O. The old436region enumeration and the
prior full axial-majorization proof are dependencies, NOT claimed rerun.
This author replay is not independent review or formal verification.

Trust boundary: original named-solid coordinates; byte-pinned exact field
and code semantics; positive root branches; complete finite cover and all
original support/moment/gauge identities; cited spectrum and mixed-branch
interfaces; and the written unformalized centering,diameter,coercivity,
proper-frame,C3 averaging,composition,Bernstein,Cayley and equality bridges.
No solver status,absence of a passage,timeout,memory kill,incomplete search
or floating-point experiment is a mathematical exclusion premise.

Bounded live primary checks on2026-10-01 retain the explicit RID conjecture
in [2604.26531](https://arxiv.org/html/2604.26531) and the unresolved named
baseline in [Gosain--Grimmer](https://arxiv.org/html/2509.08190).
[2508.18475v2](https://arxiv.org/abs/2508.18475) proves a DIFFERENT
non-Rupert Noperthedron; it does not solve RID. The standard proper strict
projection formulation is [2112.13754](https://arxiv.org/abs/2112.13754).
These bounded checks are not exhaustive priority evidence.

Read [six-reviewer-4's independent global1/100 audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_weighted_gap_review4/REVIEW.md),
graph8108/source0e8708ef1b27633bcdf0f89b717d93b949c68490. It confirms graph8058,
sourcee8f808484cb7ad21bf95438833f5737355c5ff8a; it does NOT review this new
q21/50 theorem or the newer branch lemmas. No reviewer verdict was requested.

The signed closed-cube-face method was informed by
[six-rupert-1's full D1 certificate](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cayley_wedge_proof.md),
graph8030/source8a91ec366772698daaf06262aa031ee9cc33630e, and
[whole deltoidal Cell9 proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell9_coupled_proof.md),
graph8130/sourcedb665591225afc452b0d92fecdad2070eef2df17. Their full proofs,
committed bodies and generic exact coefficient code were read. The six
power-to-Bernstein identities and signed endpoint bridge are reused as
elementary mathematics, with fresh ORIGINAL RID contacts,radius,triangle
and complete30leaf cover. No deltoidal body constants or57/45patch witnesses
are transferred.

Also read [six-rupert-2's J77 signed sectors](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_signed_mirror_sectors/PROOF.md),
graph8136/source843712820fd1ee1496cc82228794a8d7fe4f0fa3. That asymmetric
body needs translated contact moments and retained negative parts; its
constants,centering assumptions and equality motions do not enter (1).
The named global questions remain open. Collaboration uses published sources
and durable checkpoints with the orchestrator as management hub.

The concrete next frontier is all four threshold-to-threshold pairings on
f>=21/50. Retain the SAME-axis weighted energy and the actual matched-original
premise before estimating a directional Cayley remainder. Finish that branch
before claiming any larger GLOBAL gap. No expensive job remains active.
