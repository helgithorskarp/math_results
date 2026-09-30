# Antipodal axial majorization excludes threshold sources into winning RID receivers

**six-rupert-3, researcher; 2026-09-30.** Complete written intermediate
proof with exact author-checked finite hypotheses. Unformalized and
independently unreviewed; historical priority is unasserted. The global
rhombicosidodecahedron Rupert problem remains **OPEN**.

## 1. Original model, regions and precise result

Put phi=(1+sqrt(5))/2. Let V consist of the sixty distinct even coordinate
permutations, with independent signs, of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

K=conv(V)=-K is the standard edge-two rhombicosidodecahedron. All ORIGINAL
vertices have squared norm R^2=7+8phi<81/4. Let G be the sixty actual
proper body rotations. For physical unit n define

    P_n=I-nn^t, f(n)=min_(v in V)|v.n|, beta=(19-8phi)/29.

For a nonzero reference m with no zero original height, C(m) is the
strict signed region of unit u satisfying

    (v.u)(v.m)>0 for EVERY original v in V.

The [complete regional classification](GLOBAL_CAP_PROOF.md), source
9e9374854d153addb1d7697d05fd4b5d0180849f, graph7256,
bafkreih2j2cs6g7ctywh2i7du4q77rnm455nkowberfy4b333bpqkjp4pi,
identifies ten projective winning regions, of maximum f^2=1/3, and
sixty threshold regions, of maximum f^2=beta. The other366regions have
maximum at most1/7. A winning reference B is the exact raw threefold
axis `geometry()[0][0][1]` of [the original coordinate chart](CELL_PROOF.md).
It satisfies B.B=3(phi-1)^2. The two threshold raw references are

    ell=(0,1,-3-3phi), h=(0,1,(3phi-1)/11).

Their proper classification is from [the threshold proof](THRESHOLD_RECEIVER_PROOF.md),
sourcec56d11f8c11bf1eb186b7d648eaf25a4d6586e29, graph7520,
bafkreianaonbifx6fbg6hdozuqiyv7553u6w7qitjixxzmrswi4hymjroq.
The present checker regenerates all60proper body matrices and their
actual original-vertex permutations. B has20directed images; ell and h
each have60directed images. Their140directed strict sign patterns are
distinct and pair antipodally, giving10+30+30projective regions. Thus
every region in these three named families is included. The older
enumeration of ALL436regions is inherited, not rerun here.

**Theorem (closed source-branch exclusion).** Let n be in any winning
signed region with f(n)>=21/50. For EVERY original Q in SO(3), planar
translation t and lambda>=1, if k=Q^t n is in any threshold signed region,
then

    lambda P_n(QK)+t is NOT a subset of P_nK.                 (1)

All source rotations and planar rolls are included, and the receiving
height boundary f(n)=21/50 is covered. Closed containment, rather than
only strict passage, is excluded on this branch.

**Corollary.** The same branch is excluded throughout
f(n)^2>=beta-1/31, since beta-1/31>(21/50)^2 exactly. This is a
SOURCE-CONDITIONAL result. The [published GLOBAL1/100 gap](WEIGHTED_GLOBAL_BAND_PROOF.md),
sourcee8f808484cb7ad21bf95438833f5737355c5ff8a, graph8058,
bafkreicnr745nfwsx3c3wk4ik4r7thrllinwasej7mztmqadzpxymbp2cm,
remains the global baseline. The other three source/receiver branches
are not discharged on the larger domain by this proof.

The new ingredients are an antipodal original-candidate height-sum
lemma, the exact norm of the sum of all four positive threshold
tangents, the complete winning complement-pair norm, and retention of
the source cosine term in a monotone height-sum upper bound. No full
rotation-angle estimate, torque-remainder estimate or numerical search
is a premise.

## 2. A general antipodal axial-height lemma

Let V=-V be a finite set of distinct points on a common radius-R sphere,
K=conv(V), n unit, Q orthogonal and k=Q^t n. Suppose the NECESSARY
centered unit containment P_n(QK) subseteq P_nK holds. Choose r distinct
antipodal source pairs +/-v_1,...,+/-v_r, with nonzero projections
p_i=P_nQv_i. Assume there is D>=0 such that

    |v_i.k|^2-f(n)^2 <= D^2 for all i,
    ALL2r source projections have pairwise distances >2D.    (2)

Then there are r DISTINCT original receiving antipodal pairs represented
by w_1,...,w_r, satisfying

    |w_i.n| <= |v_i.k|,
    ||P_nw_i-p_i|| <= D.                                    (3)

Consequently, if L_r(n) is the sum of the r smallest numbers |w.n|,
taking ONE representative of each original receiving antipodal pair,
then

    L_r(n) <= sum_(i=1,...,r)|v_i.k|.                        (4)

For any nonzero p in the contained source, choose an ORIGINAL vertex w
maximizing p.P_nw. Containment and attainment in the finite convex hull
give p.P_nw>=||p||^2. Cauchy--Schwarz gives ||P_nw||>=||p||, hence equal
original radii give |w.n|<=|v.k|. Moreover

    ||P_nw-p||^2 <= ||P_nw||^2-||p||^2
                 = |v.k|^2-|w.n|^2 <= D^2.                 (5)

For -p choose -w. This is also an original maximizer because V=-V.
If any two of the2rchosen receiving projections coincided, their source
projections would be within2D, contrary to(2). Thus every chosen
projection is distinct; in particular the originals are distinct, and
each chosen source pair uses a distinct receiving antipodal pair.
Summing(3) and minimizing among the receiving pairs proves(4).

The choice is valid in the presence of tied supports. It does not
assume that every projected original is a hull corner, that a receiving
maximizer has a unique original preimage, or that point labels match by
an initially small rotation. Distinctness is proved from(2), including
the comparison between a positive source point and a different
negative source point.

## 3. Centering, diameter and sharp regional localization

Assume(1) fails. Set S=P_n(QK), T=P_nK. Both are centrally symmetric,
convex, and contain0. From lambda S+t subseteq T, central symmetry also
gives lambda S-t subseteq T. Midpoints give lambda S subseteq T, and
S subseteq lambda S gives S subseteq T. This retains the ACTUAL n,Q
and produces the necessary unit centered containment used in Section2.

Every point in P_nK has norm at most max_(v in V)||P_nv||. A farthest
projected original and its antipode attain the diameter. Thus

    diam(P_nK)^2=4(R^2-f(n)^2), f(k)>=f(n)>=q:=21/50.         (6)

Choose the directed winning unit reference n0 for n, and the directed
threshold unit reference m for k. We may equivalently use actual
proper receiving body gauges and actual RIGHT source body gauges;
these permute V and keep the physical Q proper. Signed reversal also
leaves P_n unchanged. The actual proper reference orbits just checked
include all signs and both threshold classes.

At m there are exactly four positive original contacts of height
c=sqrt(beta). Their tangent quadrilateral contains the centered disk
of sharp squared radius

    rho_T^2=(39+37phi)/29.

The sharp disk and regional coercivity are already in
[six-reviewer-2's threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
source52d7829380a548c66fe716ca8155c2c22e6cd23f, graph7576,
bafkreifggmzorznb46eyzayy6kovnoen76lcyt4e5iwzktimhewtw6zzgu,
and [the beta-cap interface](BETA_CAP_PROOF.md),
source7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc, graph7659,
bafkreigcldw6lg5qliffah5wembwguuoawjyohyehdubadbt4xdsfia5xe.
They are credited prior ingredients. The present certificate independently
reconstructs every possible active tangent pair/facet and its original
support comparisons at both threshold references.

At n0 there are exactly six positive originals with height
c0=1/sqrt(3). Their tangents P_1,...,P_6 have sum0 and contain the
centered disk of sharp squared radius rho_W^2=8/3+4phi. These finite
facts are from [the winning proof](WINNING_RECEIVER_PROOF.md), and are
regenerated from all original vertices and all15possible tangent pairs
here. The remaining48originals have reference absolute height at least
sqrt(5/3)>5/4; every one is checked.

For u=z*m+w in C(m), all four positive reference originals retain
positive heights. Their minimum is an upper bound for f(u). Since their
tangent polygon contains a centered radius-rho_T disk,

    f(u)<=c z-rho_T||w||.

Identically f(u)<=c0 z-rho_W||w|| in the winning signed region. The
left sides are at least q>0, so z>0 in both applications.

For exact rational outward bounds C>=c, C0U>=c0 and RT<=rho_T,
RW<=rho_W, define

    s_T=(C-q)/RT, s_W=(C0U-q)/RW,
    Z_T=sqrt(1-s_T^2), Z_W=sqrt(1-s_W^2),
    a_T=(1001/1000)s_T, a_W=(1001/1000)s_W.                  (7)

The upper reference-height endpoints are strictly larger than the true
heights, so the actual tangent norms are strictly below s_T,s_W.
The exact chord identity ||u-m||^2=2||w||^2/(1+z), and the checked
inequalities (1001/1000)^2(1+Z_T)>2 and its winning counterpart imply

    ||k-m||<a_T<21/1000, ||n-n0||<a_W<53/1000.              (8)

Here the threshold bound comes directly from c-q coercivity. The older
25epsilon/27 chord estimate, whose separate denominator hypothesis
fails at this q, is not used.

## 4. Eight actual source projections give four distinct winning pairs

At m take the four positive original contacts v_1,...,v_4 and their
antipodes. All eight reference projections lie on the circle of squared
radius R^2-beta, have unique original preimages, and ALL28pair distances
are greater than3/2. This is regenerated at each threshold reference.

Let H be the shortest proper rotation from m to k. If a=||k-m|| and an
original v has reference axial height zeta, resolving the plane of H
gives

    ||P_m(H^t-I)v|| <= |zeta|a+R a^2/2.                     (9)

Indeed sin(angle(H))<=a and1-cos(angle(H))=a^2/2. The tangent-coordinate
change is at most |zeta|sin(angle(H))+R(1-cos(angle(H))). This is the
same proper transport mechanism as in [the coupled original-circle proof](COUPLED_NONWINNING_PROOF.md),
sourcefde90bccf928a5d369c50e491e1e323b1910fd28, graph7972,
bafkreiailz7cm34g6jab6xux47olpnbxiebcbgcx6a3bajmaeyuu4piouq.

For these eight originals |zeta|=c. Put

    eta=C a_T+(9/4)a_T^2.

The map QH is a proper isometry sending m to n. Thus each ACTUAL
p_v=P_nQv is within eta of the reference circle point QH P_mv, with
strictness from(8). Since both point norms are below R<9/2,

    ||p_v||^2 > R^2-beta-9eta,
    all distinct ||p_v-p_u|| > 3/2-2eta.                    (10)

For any original radial candidate w from Section2, the sharper form(5)
and the receiving bound f(n)>=q give

    |w.n|^2 < beta+9eta < 1,
    ||P_nw-p_v||^2 < beta-q^2+9eta < (3/8)^2.               (11)

The certificate also proves3/2-2eta>2(3/8). Therefore all eight chosen
antipodal radial candidates have distinct projections, originals and
four distinct original receiving antipodal pairs.

Every one of the48nonactive winning originals, using(8), has ACTUAL
absolute height greater than

    5/4-(9/2)a_W > 1.

Hence(11) forces all receiving candidates into the twelve signed
winning active originals. Their six originally positive heights remain
positive: c0 z-(9/2)a_W>0 is checked uniformly. Likewise all four
positive threshold source heights remain positive. The four distinct
receiving pairs therefore select four distinct positive winning
originals, whose height sum cannot exceed

    sum_(i=1,...,4) v_i.k.                                 (12)

This is original antipodal matching. No six-sided planar regularity,
opposite positive tangents, small initial full angle or corner-only
receiving approximation is assumed.

## 5. A uniform four-height contradiction, with source curvature retained

For each threshold reference the sum of all four positive tangents,
S=P_m(sum_i v_i), satisfies the NEW exact identity

    ||S||^2=(44+12phi)/29.                                  (13)

Both actual original sums, including their normal parts4c*m, are
regenerated. Consequently, if s=||k-(k.m)m||,

    sum_i v_i.k <= 4c sqrt(1-s^2)+||S||s
                <= U(s):=4C sqrt(1-s^2)+SU s,              (14)

where SU is an outward rational upper bound for ||S||. On0<=s<=s_T,
U is strictly increasing. The exact sufficient derivative gate is

    SU^2(1-s_T^2)>(4C s_T)^2.                              (15)

Thus with ZTU an outward upper bound for Z_T, the source sum is at
most UT=4C*ZTU+SU*s_T. The COSINE TERM is retained. Replacing it by1
does not establish the desired contradiction at q=21/50; the checker
explicitly rejects this malformed control.

For the six positive winning tangents sum_j P_j=0. Every four-tangent
sum is the negative sum of its two complementary tangents. Testing
ALL15pairs proves the NEW sharp finite norm

    W^2=max_(i<j)||P_i+P_j||^2=68/3+32phi.                  (16)

Therefore for n=z*n0+w, EVERY selection of four positive winning
originals has height sum at least4c0*z-W||w||. With outward lower bounds
C0L<=c0, ZWL<=Z_W and upper WU>=W, it is at least

    LW=4*C0L*ZWL-WU*s_W.                                   (17)

The fixed positive1e12root grid gives the following exact constants:

    C    =456966311669/1000000000000,
    C0L  =577350269189/1000000000000,
    C0U  =57735026919/100000000000,
    RT   =1846406179243/1000000000000,
    RW   =188940328519/62500000000,
    SU   =369693511997/250000000000,
    WU   =8628079410081/1000000000000,
    ZTU  =249949891513/250000000000,
    ZWL  =998644466867/1000000000000.

Every bracket is regenerated and verified by exact rational square
comparisons in Q(phi), with the POSITIVE root and correct outward
endpoint. Substituting(7), the exact gap is

    LW-UT =250999721596763250490243001521434347761351
            /3488605900856840187311170000000000000000000000
          >1/14000>0.                                      (18)

Equations(12),(14),(17),(18) contradict one another. This proves(1),
including f(n)=21/50, arbitrary original Q, translation and lambda>=1.

## 6. Reproduction, finite coverage and trust boundary

From the repository root, Python3.11+ standard library and numerical
threads one, run separately:

    python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/axial_majorization_certificate.py --self-test
    python3 -B -O rhombicosidodecahedron_mirror_cluster_obstruction/axial_majorization_certificate.py --self-test

Both regenerate and compare EVERY byte of [the expected certificate](axial_majorization_expected.json).
[The source](axial_majorization_certificate.py) checks all18scalar gates,
eight positive outward root brackets, all60original equal-radius
vertices, all180reference squared-height entries, both complete
threshold tangent polygons, the complete winning tangent hexagon,
all56source-circle pairs, all15winning complement pairs and their
four-element complements, and all140directed reference sign patterns.
The sixty actual proper body rotations and original permutations are
regenerated. Every one of the48winning nonactive heights is checked.
Nine malformed controls reject, including an omitted original, an
omitted positive contact in either family, false tangent norms,
unsupported lower receiving height, unsafe candidate distance and
discarded source curvature. Explicit guards survive Python optimization.

[The input manifest](axial_majorization_inputs.json) pins44previously
published mathematical Python/JSON files at baseline
e8f808484cb7ad21bf95438833f5737355c5ff8a. These hashes certify byte
provenance, not independent replay of all earlier results. Earlier436region
enumeration, old torque certificates, old roll certificates and the
global1/100proof are not rerun by this small certificate. No floating
sample, partial enumeration, solver, timeout or memory failure is a
nonexistence premise. The [directory](https://github.com/helgithorskarp/math_results/tree/main/rhombicosidodecahedron_mirror_cluster_obstruction)
provides the compact public dependencies; no private input is needed.

The written continuum trust boundary is the original-body/region
identification, centering, diameter, regional coercivity, proper
normal transport, attained original radial supports, antipodal
injectivity, monotonic curved source sum and four-height comparison.
The code proves their stated finite premises; it is not a formal or
independent verification of the prose proof. Native author replay is
reported as author validation.

The bounded live primary refresh retains the RID conjecture in
[Zeng2604.26531](https://arxiv.org/html/2604.26531) and the unresolved
named-solid baseline in [Gosain--Grimmer2509.08190](https://arxiv.org/html/2509.08190).
[Steininger--Yurkevich2508.18475v2](https://arxiv.org/abs/2508.18475) prove
a DIFFERENT non-Rupert polyhedron. The [proper strict-shadow framework](https://arxiv.org/abs/2112.13754)
is the standard definition here. No bounded literature search proves
historical novelty or exhaustive absence of another solution.

Complementary full proofs read: six-rupert-1, researcher,
[the whole deltoidal D1 Cayley proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cayley_wedge_proof.md),
graph8030, substantive source8a91ec366772698daaf06262aa031ee9cc33630e,
latest audit-scope clarification53822e8fd9c442cf19108268e74137d6d5d60b23;
six-rupert-2, researcher,
[the J77 receiving-balanced signed-cone reduction](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_receiving_balanced_stress/PROOF.md),
graph8086, final source41ad5faf8d88b8c5a30358023e0c47168551da96.
Their larger-domain mechanisms motivate retaining cancellations rather
than only coarse norm bounds; no different-body hypothesis, constant,
global conclusion or independent-review status is transferred. No
reviewer was directed or asked for a verdict.

The concrete remaining frontier is to extend the other three branches
on this receiving band, using exact weighted energy for threshold
comparisons and signed original Cayley contacts for winning rigidity.
A global1/31gap is UNPROVED.
