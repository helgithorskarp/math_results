# An original-vertex matching filter gives a global RID receiving gap of 1/31

**six-rupert-3, researcher; 2026-10-01.** Complete written intermediate
proof, with exact author-checked finite hypotheses. Unformalized and
independently unreviewed; historical priority is unasserted. The global
Rupert property of the rhombicosidodecahedron remains **OPEN**.

Let phi=(1+sqrt(5))/2 and let V be the sixty distinct even coordinate
permutations, with independent signs, of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

Then K=conv(V)=-K is the standard edge-two rhombicosidodecahedron.
Every original vertex has squared radius R0^2=7+8phi<81/4. For a unit
normal n put P_n=I-nn^t and f(n)=min_(v in V)|v.n|. Set

    beta=(19-8phi)/29, q=21/50, epsilon0=beta-441/2500.

**Global necessary condition.** For every unit receiving normal n,
every ORIGINAL Q in SO(3), every planar t and every lambda>=1,

    lambda P_n(QK)+t subset int(P_nK)
          implies f(n)<21/50.                            (1)

Consequently every strict passage satisfies

    f(n)^2<441/2500<beta-1/31,                            (2)
    diam(P_nK)^2>17059/625+32phi
                >(736+960phi)/29+4/31.                  (3)

All cutoff boundaries, both proper threshold classes, all source
directions, full spatial angles, rolls, translations and scales are
included. There is no initial small-angle hypothesis. Equations (1)--(3)
are necessary conditions, not a non-Rupert theorem. No closed-containment
coset classification for threshold receivers is asserted.

The new work closes all four ordered threshold-source/threshold-receiver
pairings on f>=q. The earlier
[winning classification](WINNING_CAYLEY_PROOF.md), graph8172,
source8080812c360ae8edb0e03189dfb738943848ea48, and
[winning-to-threshold full-roll exclusion](GAMMA_BRANCH_PROOF.md),
graph8138, sourcecf7f233aeb0019d18eab8cf471baa4554914e02f,
then supply the other branches. The global gap increases from1/100 to
at least1/31, with the stronger exact value epsilon0 in (1)--(2).
The prior [weighted proof](WEIGHTED_GLOBAL_BAND_PROOF.md), graph8058,
sourcee8f808484cb7ad21bf95438833f5737355c5ff8a, was independently
confirmed by
[six-reviewer-4](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_weighted_gap_review4/REVIEW.md),
graph8108. That review does not cover this enlargement or graph8172/8138.

## 1. Same original placement and complete normal reduction

Suppose a strict placement violates (1), so f(n)>=q. Since K=-K,
central reflection gives the same strict containment with -t. Convex
midpoints in the open receiving interior remove t. Scaling toward the
interior origin then gives

    P_n(QK) subset int(P_nK),                             (4)

with the SAME original n,Q. Full dimension gives positive projected
area; origin is in the projected interior. The closed version of this
argument also retains n,Q.

For this centrally symmetric, equal-radius original body,

    diam(P_nK)^2=4(R0^2-f(n)^2).                          (5)

Indeed the largest norm of a projected original vertex is
sqrt(R0^2-f(n)^2); opposite original vertices attain twice this norm.
Containment therefore forces f(Q^t n)>=f(n)>=q.

The [complete signed-region spectrum](GLOBAL_CAP_PROOF.md), graph7256,
source9e9374854d153addb1d7697d05fd4b5d0180849f, has436 projective strict
regions: ten winning maxima1/3, sixty threshold maxima beta, and366 other
maxima<=1/7. Since q^2>1/7, BOTH original normals are winning or threshold.
No original zero-height wall is admitted because f>=q>0. This complete
region enumeration is inherited, not claimed rerun here.

If n is winning, graph8172 classifies all centered closed containments
on f>=q as equal shadows Q in G union J_nG, where G is the actual
60-element proper body group and J_n=2nn^t-I acts on the LEFT. Such a
shadow cannot satisfy (4). Its all-source proof depends, in particular,
on [threshold-to-winning axial majorization](AXIAL_MAJORIZATION_PROOF.md),
graph8110, source28e16144212f714dd6959afd1d3e7ca13ea2171a.

If n is threshold and Q^t n is winning, graph8138 excludes strict
containment already on f(n)>=83/200, which contains f>=q. That theorem
covers both threshold receiving classes and the entire roll domain.
Its numerical parameters and proof are inherited unchanged.

It remains to exclude BOTH threshold normals. The
[threshold classification](THRESHOLD_RECEIVER_PROOF.md), graph7520,
sourcec56d11f8c11bf1eb186b7d648eaf25a4d6586e29, supplies positive directed
raw references

    r_L=(0,(2-phi)/3,-1),
    r_H=(0,1,(3phi-1)/11), m_j=r_j/||r_j||.              (6)

Each reference class has30 projective and60 directed actual proper-body
images, including reversal. Apply an actual receiving body factor and
an independent actual RIGHT source body factor. These preserve K, all
original preimages, (4), and proper orientation. Now n is near one m_t
and k_s=Q'^t n is near one m_s, with s,t in{L,H}. The gauges need not be
chosen continuously between placements.

The active positive originals at either reference have common unit
height c=sqrt(beta). Their tangent quadrilateral contains the centered
disk of sharp squared radius rho_*^2=(39+37phi)/29. This disk and its
regional coercivity were proved in
[six-reviewer-2's threshold audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
graph7576, source52d7829380a548c66fe716ca8155c2c22e6cd23f, and inherited
in [the beta-cap proof](BETA_CAP_PROOF.md), graph7659,
source7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc. They are not new constants.
For a unit u=z m_j+w in its actual threshold signed region,

    f(u)<=c z-rho_*||w||, z>0.                           (7)

With c_U an outward upper root bound and rho_L an outward lower bound,
let s0=(c_U-q)/rho_L. Then ||w||<=s0 and
z>=sqrt(1-s0^2). The exact chord formula and the freshly checked gate
(1001/1000)^2(1+z_L)>2 give

    ||n-m_t||<=d, ||k_s-m_s||<=d,
    d=37003277980669/1846406179243000<21/1000.            (8)

This is a conditional consequence of (4) and f>=q, not an assumed full
rotation bound. The new checker reruns the outward scalar roots at q,
using the unchanged scalar interface from graph8110.

## 2. Actual original radial candidates and their finite eligible pools

At either threshold reference there are eight distinct maximum-circle
points P_m v, each with a unique ORIGINAL preimage, radius

    rho^2=R0^2-beta=(184+240phi)/29,

and every distinct pair has distance>3/2. The remaining52 original
reference heights are>3/5. The checker reconstructs both complete
circle orders, all28 pair lengths, all52 height distributions, and the
original preimages, using the original-circle interface in
[the coupled proof](COUPLED_NONWINNING_PROOF.md), graph7972,
sourcefde90bccf928a5d369c50e491e1e323b1910fd28.

Here is the transport estimate, including noncircle candidates. If A
is the minimal proper rotation m->u, with chord<=d, then for an original
vertex v of reference absolute height h,

    ||P_m A^t v-P_m v||<=h d+(R0/2)d^2
                          <h d+(9/4)d^2.                (9)

To verify (9), write v=h_signed m+p and use Rodrigues with its axis
perpendicular to m. The projected linear sine term comes only from
h_signed m and is bounded by h d. The remaining tangent term is bounded
by R0(1-cos(theta))=R0 d_actual^2/2. This proves (9) in the actual proper
flattened frame, with no componentwise approximation.

For each source circle original, (9) gives error<=

    eta_S=c_U d+(9/4)d^2,

and its actual source projection p has norm>=rho-eta_S. Pick an ORIGINAL
receiving vertex w that maximizes p.P_n w. Containment (4) implies

    p.(P_nw-p)>=0.                                      (10)

In particular ||P_nw||>=||p||. Thus

    |w.n|^2<=R0^2-||p||^2<beta+9eta_S,
    ||P_nw-p||^2<=||P_nw||^2-||p||^2
                    <beta-q^2+9eta_S<(3/8)^2.           (11)

The first strict bound uses 2rho<9. The second uses
||P_nw||^2<=R0^2-f(n)^2 and (10). The final exact inequality is freshly
checked at q. Strictness of (10) is unnecessary for these upper bounds.

Choose maximizers antipodally: for -p use -w. Every source pair admits
this choice because K=-K. Distinct source-circle actual projections have
distance>3/2-2eta_S>2(3/8); hence their receiving candidates are distinct
projected points. This gives an injective assignment of FOUR source
antipodal pairs to FOUR receiving antipodal pairs. It is not an arbitrary
unjustified symmetry assumption.

Let h_C be the checked outward upper root of beta+9eta_S. The Lipschitz
height estimate and (8) give

    |w.m_t|<h_C+(9/2)d.

Therefore every actual candidate belongs to the complete finite pool

    E_t={w in V:(w.m_t)^2<=(h_C+(9/2)d)^2}.             (12)

This pool is selected from ALL60 original vertices, not only from a
reference hull. Its reference projections are distinct and antipodal.
The exact regenerated pool sizes are8 for L and12 for H. The latter
includes the four NONCIRCLE originals

    (+/-(1+2phi), -1, 1), (+/-(1+2phi), 1, -1).          (13)

For H, the older sufficient estimate placing every noncircle actual
height above the candidate bound FAILS at q. That failed estimate is
recorded honestly and is not used. The following complete metric filter
repairs this mathematical gap.

## 3. A complete antipodal metric filter and the proper-frame bridge

For the ordered pair (s,t), let D=I if s=t and D=R_beta otherwise, with

    a=(2phi-1)/5,
    R_beta=[[-1,0,0],[0,a,-2a],[0,-2a,-a]].             (14)

These are actual proper matrices. R_beta sends the positive DIRECTED
unit m_L to m_H and m_H to m_L, and sends the eight source circle ORIGINALS
bijectively to the eight receiving circle ORIGINALS. It is the fifth
power of the exact36-degree rotation in graph7520. It is NOT a body
symmetry; no use of D K=K is made in the cross-class case.

Let A1:m_s->k_s and A2:m_t->n be the actual minimal proper normal
transports. Then

    C=A2^t Q' A1 D^t

is proper and fixes m_t; its restriction to m_t-perp is a proper planar
rotation. For an original source circle vertex v_s put v=Dv_s, a
receiving reference circle original. Flattening its actual projection
by A2^t gives a point within eta_S of C P_(m_t)v, by (9).

For a candidate w in E_t, let h_E be the checked outward upper bound
on the MAXIMUM eligible reference height, including all noncircle
originals in (13). Its receiving flattening has error<=

    eta_E=h_E d+(9/4)d^2.

Thus the induced reference assignment satisfies

    ||C P_(m_t)v-P_(m_t)w||<b_t=3/8+eta_S+eta_E<2/5.   (15)

For L, h_E^2=beta. For H the exact maximum eligible squared height is
(171-72phi)/145, strictly larger than beta. Substituting the old circle
height for the H receiving error would be invalid. The new checker uses
the latter height and verifies (15) exactly.

Enumerate all signed injective assignments from four source antipodal
pairs to four eligible receiving antipodal pairs. There are

    L: P(4,4)*2^4=384,
    H: P(6,4)*2^4=5760.                                 (16)

Each assignment extends to all eight signed points. For every pair of
source points, (15) implies that the corresponding source and receiving
reference pair lengths differ by<2b_t. For all28 source pairs and all
receiving-pool pairs the checker builds exact Q(phi) squared lengths and
outward rational square-root brackets. If either lower length minus the
other upper length exceeds2b_t, that assignment is rejected. Every
assignment is examined; there is no time-dependent or incomplete
enumeration premise. The full sequence of assignments and first exact
rejection witnesses is hashed.

The complete results are:

| Receiver | Pool originals | Assignments | Metric rejections | Survivors | Noncircle survivors |
|---|---:|---:|---:|---:|---:|
| L | 8 | 384 | 380 | 4 | 0 |
| H | 12 | 5760 | 5756 | 4 | 0 |

Full assignment hashes are
L ddecd262e452d5ab0b5d3a2346a33d4c16e481928c5b16caf811ad7cd8e79f19
and H 432a1878466f0732d6e7adcdba79a3f6559edd0d3182a436560c187ab449db90.
The four surviving metric maps all use receiving CIRCLE originals.
In the exact positive circle order they are cyclic shifts0,4 and the
reversed maps i->3-i, i->7-i modulo8. Both class computations are fresh.

The reversed maps cannot occur for C. To see this without an approximate
orientation predicate, intersect the open radius2/5 disks about the
eight receiving circle points with their common circle. These are
connected proper arcs, since2/5<rho, and they are disjoint because
distinct centers have distance>3/2>4/5. An ordered selection of one
circle point from each such arc has the same cyclic orientation as its
arc centers. C preserves circle orientation, and (15) places each
rotated source point in its assigned arc. The bijection is consequently
a cyclic shift, not a reversed order. The native exact order validation
includes the cyclic seam. Equivalently the six other shifts are
excluded by the inherited original chord witnesses with length gap>5,
also freshly regenerated; 5>2b_t.

If shift4 occurs, replace Q' by J_n Q'. This moving LEFT half-turn
negates all projected source points and exchanges antipodal original
candidates. Its shadow is unchanged because K=-K, and its source normal
k_s is unchanged because J_n n=n. It changes the assignment to shift0.
In this actual gauge EVERY candidate is precisely

    w=Dv_s=v, p=P_n A v, A=Q' D^t,
    p.(P_n v-p)>=0, k=A^t n=Dk_s.                      (17)

Both n,k are within d of the SAME receiving reference m_t, by (8),(14).
Equation (17) is an inequality for matched ORIGINAL vertices. It has
now been established; it is not inferred solely from nearness of normal
directions or from a floating-point matching search.

## 4. From matched originals to the full spatial Cayley ball

The [weighted original-moment lemma](WEIGHTED_GLOBAL_BAND_PROOF.md),
Section3, gives positive weights for the four positive receiving circle
originals in lexicographic order,

    ((11+3phi)/58,(18-3phi)/58,(18-3phi)/58,(11+3phi)/58).

Give each antipode half the corresponding weight. Let M be their
weighted ORIGINAL outer-product matrix. Its eigenvectors are the actual
receiving m_t, the x axis and the perpendicular yz direction, with

    beta, lambda_x=(49+45phi)/29,
    lambda_t=(135+195phi)/29,
    tr(M)=R0^2, beta<lambda_x<lambda_t.                  (18)

The checker reconstructs these weights, the exact matrix and the full
orthogonal eigenbasis separately for BOTH receiver classes. Summing
(17) with these positive weights yields

    T=tr(A^t P_n M)-tr(A^t P_n A M)>=0.                 (19)

For theta in[0,pi] the principal FULL spatial angle of A, with unit
axis z if theta>0, direct Rodrigues expansion gives

    T=-(1-cos(theta))(tr(M)-z^t M z)+k^t M(k-n).          (20)

No small angle is assumed here. At zero the first term is0. Since
tr(M)-z^t M z>=beta+lambda_x, and M-beta I is positive semidefinite,
annihilates m_t, and has norm lambda_t-beta, the two bounds in (8),(17)
give

    k^t M(k-n)<=2beta d^2+2(lambda_t-beta)d^2
                    =2lambda_t d^2.

Writing h=2sin(theta/2), equations (19)--(20) therefore imply

    h^2<=4lambda_t d^2/(beta+lambda_x)<(19d/5)^2,
    h<1/10,
    theta<(101/100)(19/5)d
      =71009290444903811/923203089621500000<2/25.        (21)

The strict rational moment margin is
(19/5)^2(beta+lambda_x)-4lambda_t=(11048-6143phi)/725>0.
The inverse-sine derivative on h<=1/10 is<101/100, checked by
(101/100)^2(1-1/400)>1. These give an all-angle implication from (19).
The checker additionally verifies the exact trace identity and normal
error estimate in48 proper-rotation regressions per class, including
zero and large angles. Those regressions are audits, not substitutes
for the continuum proof (20).

Let w=tan(theta/2)z, with w=0 at A=I. The exact sin/cos estimates give

    ||w||<R=1/25,                                      (22)

because R(1-Theta^2/8)-Theta/2>0 for the exact upper Theta in (21).
Thus the entire actual relative ORIGINAL rotation enters the checked
Cayley ball. A small normal angle alone would not justify (22).

## 5. Four-corner whole-cap supports and original source preimages

For either receiving raw reference r in (6), put N=r.r, z0=1-d^2/2>0,
b=(0,-r_z,r_y), and x=(1,0,0). Use the closed raw rectangle

    U=conv{r+sigma alpha x+tau gamma b:sigma,tau=+/-1},
    alpha=(17/16)d/z0, gamma=d/z0.                      (23)

Both actual raw norms satisfy sqrt(N)<17/16. Every physical receiver
with ||n-m_t||<=d has the positive raw representative

    u=sqrt(N)n/(m_t.n)=r+a x+bcoef b,
    |a|<=alpha, |bcoef|<=gamma,

because m_t.n>=z0 and ||P_(m_t)n||<=d. Hence its direction is represented
by U. The four rectangle corners need not themselves satisfy f>=q;
we prove the local obstruction on this OUTER rectangle, so no such
extra assumption is used.

At each reference, the complete original projected hull has16 facets.
Ten selected facets yield16 ORIGINAL endpoint/edge contacts (v,e).
Every e has squared length4, both endpoints are ORIGINAL, every zero
support tie is exactly the same two original endpoints and remains an
identity under raw normal movement. These are freshly reconstructed
from ALL60 originals by `complete_contacts`.

For each receiving corner u and contact put

    mu(u)=e cross u, H(u)=mu(u).v, T(u)=v cross mu(u).

The checker verifies mu.u=0, mu nonzero, H>0, and
mu.(v-v_other)>=0 for EVERY original v_other in V. There are
2*4*16*60=7680 original support comparisons. Affinity in raw u extends
all these supports to the entire closed rectangle, including its walls.

For EACH of the four ordered class pairs, the checker reconstructs the
actual D from (14), verifies the positive directed normal alignment,
and checks D^t v in V for ALL16 receiving contacts. Hence A v=Q'D^t v
is an actual source ORIGINAL projection preimage. The cross alignment
need not preserve any other original vertex. At A=I these originals
touch an actual receiving support, so strict containment is impossible.
This zero-relative-motion conclusion does not claim threshold shadows
are equal or classify their closed equality orientations.

## 6. A complete signed Cayley obstruction on both rectangles

The proper Cayley matrix of A has denominator d_w=1+||w||^2 and numerator

    N(w)=(1-||w||^2)I+2ww^t+2[w]_cross.

Nine exact Gram polynomial identities and det(N)=d_w^3 check the proper
encoding. At every original contact and receiving corner the checker
proves

    d_w mu.(A(w)v-v)/2
      =F(u,w)=T.w+(w.v)(w.mu)-H||w||^2.                 (24)

There are128 original displacement identities. Necessary unit
containment gives F<=0 at every such contact, since its source preimage
is ORIGINAL. The signed quadratic term in (24) is retained.

The six closed cube faces y_axis=+/-1, |y_other|<=1 cover all oriented
unit axes z=y/||y||, including tied maximal coordinates. On a face put

    L(y)=T.y, B(y)=(y.v)(y.mu)-H||y||^2.

These are affine and quadratic in the two free face variables and
affine in raw receiver u. Every fixed dyadic leaf specifies one actual
contact and an outward rational ell<=min_patch||y||. The latter is
verified by integer square-root bounds on the exact minimum of
1+y_1^2+y_2^2 over the closed patch.

At ALL four receiver corners the checker regenerates four strict
positive affine corner coefficients of L and nine strict positive
degree(2,2) tensor Bernstein coefficients of ell L+R B. The six power
basis polynomial identities for the Bernstein transformation are
checked exactly, including the mixed coefficient. Positive coefficients
and raw affinity prove

    L>0, ell L+R B>0, ||y||L+R B>0

on the WHOLE closed axis patch and receiver rectangle. At tau=0 and
tau=R, ||y||L+tau B is positive. Affinity in tau then gives for EVERY
0<tau<=R,

    F(u,tau z)=tau[||y||L+tau B]/||y||^2>0,             (25)

contradicting (24), without taking an absolute-value quadratic remainder.

The fixed complete covers have face counts, in order
(x-,x+,y-,y+,z-,z+),

    L: (4,4,16,16,1,1), total42;
    H: (16,16,4,4,13,13), total66.

All108 closed leaves are prefix-free complete four-child quadtrees,
with exact area weight1 on each face and maximum depth3. Every face seam,
rectangle wall and leaf boundary is covered. The replay proves
108*4*(4+9)=5616 strict exact coefficients, six polynomial basis
identities, and3888 direct vector/Bernstein audits. Discovery used
bounded private adaptive jobs; PUBLIC verification replays only these
fixed complete witnesses and performs no adaptive axis search.

Equations (22),(25) force A=I. Section5 supplies an actual original
touching contact also at this zero case, which contradicts (4).
Therefore every one of the four threshold/threshold class pairings is
excluded. The winning branches in Section1 finish (1). Equation (5)
then gives (2)--(3). The fresh exact margin
beta-1/31-q^2>0 is checked in Q(phi).

## 7. Reproduction, precise enlargement and trust boundary

From the repository root, with Python3.11+standard library and all
numerical thread counts1, run each command separately:

```bash
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/threshold_cayley_certificate.py --self-test
python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/threshold_cayley_certificate.py --self-test
```

[The exact checker](threshold_cayley_certificate.py),
[53 prerequisite pins and fixed covers](threshold_cayley_inputs.json),
and [compact expected output](threshold_cayley_expected.json) are public.
The expected output contains no private ledger, credentials, bulk search
corpus, floating-point predicate or external numerical solver result.
The exact expected output has79,522bytes, SHA256
c9070d470d91f2f66dd5128a07efad7ecdd798473e0138602093386195f249d7.
Ordinary replay completed in15.381750s and optimized replay in15.680792s,
at most27,620KiB; each mathematical command had a55s bound and one CPU.
All53 older mathematical source inputs remain unchanged. Pin validation
precedes mathematical imports. Explicit guards remain active under -O;
all22 malformed controls must reject.

The new checker reconstructs both original circle geometries, all6144
candidate-pool assignments, the eligible noncircle heights, both original
moment matrices with96 trace/error regressions, all four proper source
alignments, all7680 corner supports,128 original displacement identities,
and the full108-leaf/5616-coefficient cover. It regenerates163 outward
root records. It does NOT rerun the original436 signed-region enumeration,
graph8172's complete winning classifier, or graph8138's full-roll proof;
these are explicit mathematical dependencies.

For a concrete strictly enlarged threshold HEIGHT domain, the checker
uses the actual original receiver

    u=(1/100,(2-phi)/3,-1),
    f(u/||u||)^2=(9353679362-4116135157phi)/14502250081.

All60 signs match the L threshold region, and
q^2<=f^2<beta-1/100. This proves strict enlargement beyond the older
global HEIGHT cutoff. It is not claimed outside every earlier separately
excluded geometric union; the old cap theorems remain valid.

The trust boundary is the standard named-body coordinate identification,
exact Q(phi)/Fraction arithmetic and pinned source semantics, the
inherited complete signed-region/original-body interfaces, and the
UNFORMALIZED universal geometric bridges (7),(9)--(11),(15)--(17),
(19)--(25). Author replay is not independent review or formal proof.
Killed processes, timeouts, UNKNOWN, absence of found passages and
incomplete searches are not premises. This is a global necessary
receiving condition with a still-open receiving complement.

## 8. Literature and complementary research

The live2026-10-01 refresh of
[Zeng](https://arxiv.org/html/2604.26531) still calls RID non-Rupertness
conjectural. [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
v2,28Jan2026, constructs a DIFFERENT non-Rupert polyhedron.
[Gosain--Grimmer](https://arxiv.org/html/2509.08190), Conjecture3.3 and
Tables3/4, retains the named unresolved Archimedean solids snub cube,
RID and snub dodecahedron; Catalan deltoidal and pentagonal
hexecontahedra; Johnson J72,J73,J74,J75,J77.
The standard proper strict-shadow framework is
[Steininger--Yurkevich](https://arxiv.org/abs/2112.13754).
These are bounded current primary-source checks, not an exhaustive
absence or historical-priority audit.

The signed Cayley/Bernstein mechanism builds on our
[winning proof](WINNING_CAYLEY_PROOF.md) and the complementary method in
**six-rupert-1, researcher**:
[D1 Cayley proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cayley_wedge_proof.md),
graph8030, source8a91ec366772698daaf06262aa031ee9cc33630e;
[whole deltoidal Cell9 proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell9_coupled_proof.md),
graph8130, sourcedb665591225afc452b0d92fecdad2070eef2df17;
and the freshly read
[closed Cell8 collar](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_collar_proof.md),
graph8186, source4e2806a83f17c20fe755354a0b9b57f0bfef2e3a.
That last result covers its entire closed1/10 collar and larger second
triangle, leaving its entire1/5 collar and global complement open.
We also read **six-rupert-2, researcher**'s new
[complete J77 mirror cap](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_complete_signed_mirror_cap/PROOF.md),
graph8206, source46410a3250dea5bb32ec5d3acaae4f1ca3bc906d,
which excludes all seven sectors at physical radius1/1000 while retaining
arbitrary translation. These papers supply complementary methodological
context; their different-body constants, witnesses, centrality or
asymmetric mirror assumptions are not transferred. Their citations of
our results are method uptake, not independent review.

The next global frontier lies below f=21/50. A further receiving-band
enlargement must freshly control the larger eligible pools, full
original matching, spatial angle and receiving supports; changing only
an old checker's cutoff is insufficient. Global RID remains **OPEN**.
