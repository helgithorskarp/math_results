# A two-point proper-roll obstruction excludes threshold-to-winning RID passages at 83/200

**six-rupert-3, researcher; 2026-10-01.** Complete written intermediate
proof with exact author-checked finite hypotheses. This proof is
unformalized and independently unreviewed. Historical priority is
unasserted. The global Rupert property of the rhombicosidodecahedron
remains **OPEN**.

Let phi=(1+sqrt(5))/2, and let V consist of the sixty distinct even
coordinate permutations, with independent signs, of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

Set K=conv(V)=-K, R0^2=7+8phi, P_n=I-nn^t for unit n, and
f(n)=min_(v in V)|v.n|. This is the standard edge-two original body.
Write beta=(19-8phi)/29 and q=83/200. The winning and threshold signed
regions are the original regions in the complete
[normal spectrum](GLOBAL_CAP_PROOF.md), graph7256. Their reference
maxima are respectively1/3 and beta. Both proper threshold classes are
included below; the source body is always the original K.

**Mixed-branch theorem.** Suppose n is in a winning signed region and
f(n)>=83/200. For every ORIGINAL Q in SO(3) such that Q^t n is in a
threshold signed region, every planar t and every lambda>=1,

    lambda P_n(QK)+t is NOT a subset of P_nK.             (1)

Thus even closed containment is impossible on this branch. No initial
spatial-angle restriction, roll restriction, source-nearness assumption
or assumption of zero translation is made. The receiving cutoff is
closed. Since beta-1/28>q^2, this also covers the branch with
f(n)^2>=beta-1/28. This is a branch exclusion, **not a GLOBAL1/28 gap**.
The established global necessary condition remains f(n)<21/50,
with squared-height gap at least1/31, from
[the preceding global proof](THRESHOLD_CAYLEY_PROOF.md), graph8228,
source411ae5ebba4c5c426650c491ed48742ebeff0231.

Equation (1) strictly extends the receiving-height domain of the earlier
[axial-majorization branch](AXIAL_MAJORIZATION_PROOF.md), graph8110,
source28e16144212f714dd6959afd1d3e7ca13ea2171a, whose cutoff is21/50.
Here a simultaneous proper rotation of two matched points supplies the
missing obstruction. The older four-height majorization gates are not
continued below their proved range or used in this proof.

## 1. The original placement forces both normal caps

Assume the closed containment in (1). Central symmetry gives the same
containment with -t. Convex midpoints remove t; contraction toward the
origin removes lambda>=1 as a necessary condition. This yields

    P_n(QK) subseteq P_nK                                 (2)

with the SAME original n,Q. For this antipodal, equal-radius body,

    diam(P_nK)^2=4(R0^2-f(n)^2).

Indeed the maximum projected norm is attained by an original vertex,
and its opposite attains twice that norm as a distance. Applying
diameter monotonicity in (2) proves f(Q^tn)>=f(n)>=q.

The complete spectrum has436 projective strict regions: ten winning,
sixty threshold and366 others with maximum squared height<=1/7.
Since q^2>1/7, a putative containment with this receiving cutoff has
only winning or threshold source directions. We prove the threshold
source branch. The old spectrum is an inherited prerequisite and is
not claimed reenumerated here. Positive f excludes every original
zero-height wall.

Choose independent actual proper receiving and RIGHT source body
gauges. They preserve K, the original preimages, (2), and proper
orientation. In the gauged placement, the receiving reference is

    B=(0,2-phi,1), m_W=B/||B||,

and the source reference is one of

    r_L=(0,(2-phi)/3,-1),
    r_H=(0,1,(3phi-1)/11), m_j=r_j/||r_j||.               (3)

Let Q' be the gauged original rotation and k=Q'^tn. The actual proper
orbits contain20 directed winning references and60 for EACH threshold
class, including reversal. Their140 strict original sign patterns are
distinct. These native orbit/sign counts are freshly checked by the
new source. The low raw vector in (3) is positively collinear with the
first threshold reference in graph7520; it is not an improper fold.

At the winning reference, the six positive active original vertices
have common unit height c_W=sqrt(1/3); their tangent hexagon contains
the centered disk of squared radius rho_W^2=8/3+4phi. At either
threshold reference the four positive active originals have height
c_T=sqrt(beta), and their tangent quadrilateral contains the sharp
centered disk rho_T^2=(39+37phi)/29. The threshold disk and regional
coercivity are established in
[six-reviewer-2's threshold audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md),
graph7576, source52d7829380a548c66fe716ca8155c2c22e6cd23f,
and [the cap proof](BETA_CAP_PROOF.md), graph7659,
source7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc. That earlier audit is
not a review of the present enlargement. The new checker reconstructs
all three active tangent polygons and their complete actual supports.

For a unit u=z m+w, w perpendicular to m, in the actual reference
signed region, positivity of all active heights and their centered
tangent disk gives z>0 and

    f(u)<=c z-rho||w||.                                   (4)

The disk yields a tangent original with dot product<=-rho||w||, and
the signed-region assumption makes its signed height admissible in f.
If f(u)>=q, then ||w||<=s=(c_U-q)/rho_L, using outward rational upper
and lower positive square-root bounds. Thus z>=z_L, where z_L is an
outward lower root of1-s^2. The exact chord identity and the fresh gate
(1001/1000)^2(1+z_L)>2 imply

    ||k-m_j||<=d_T=42008277980669/1846406179243000,
    ||n-m_W||<=d_W=16251261945919/302304525630400.          (5)

These bounds are derived from the original containment, not assumed.
All roots have fixed1e12 rational-grid outward brackets, validated by
exact Q(phi) squared comparisons. Both source classes have the same
bound because their active heights and sharp tangent disks agree.

## 2. Radial support choices retain original receiving candidates

At either threshold reference there are eight maximum-circle points,
each with a unique ORIGINAL preimage, of squared radius

    r_s=R0^2-beta=(184+240phi)/29.

Their28 distinct pair lengths exceed3/2. All60 original projections,
all8 original preimages, all28 comparisons and both classes are
freshly reconstructed. No convex-combination source is substituted.

We use the following original-vertex transport estimate. If A is the
minimal proper rotation m->u with actual chord at most d, and v has
reference absolute height h=|v.m|, then

    ||P_mA^tv-P_mv||<=h d+(9/4)d^2.                     (6)

To prove it, write v=h_signed m+p and use Rodrigues with unit axis
a perpendicular to m. The projected first-order sine term from p
vanishes, since a cross p is parallel to m. The height term has norm
at most h|sin(theta)|<=h d. The remaining tangent term is
(1-cos(theta)) times the component of p perpendicular to a, with
norm at most R0 d^2/2<(9/4)d^2. The identity transport follows by
continuity, or directly. Formula (6) applies to circle AND noncircle
originals. The new checker also evaluates18 actual proper minimal
transports on all60 original vertices, for1080 exact inverse-frame
regressions with both tilt signs and the identity. These regressions
complement the universal Rodrigues argument; they do not replace it.

Set, using the freshly checked outward roots c_TU,c_WU,

    eta_T=c_TU d_T+(9/4)d_T^2,
    eta_W=c_WU d_W+(9/4)d_W^2,
    a=2/5, b=9/20.

For each original source circle vertex its actual projected source
point p=P_nQ'v satisfies ||p||>=sqrt(r_s)-eta_T>0. Choose an ORIGINAL
receiving vertex w maximizing p.P_nw. Necessary containment (2) gives

    p.(P_nw-p)>=0.

Consequently ||P_nw||>=||p||, and

    |w.n|^2<=R0^2-||p||^2<beta+9eta_T,
    ||P_nw-p||^2<=||P_nw||^2-||p||^2
              <beta-q^2+9eta_T<(2/5)^2.                 (7)

The strict upper bounds use2sqrt(r_s)<2R0<9 and eta_T>0. The final
inequality is one of the fresh scalar gates. It does not use the old
four-positive-height sum inequality.

Choose maximizers antipodally: -p is assigned -w. Distinct actual
source circle points are separated by more than3/2-2eta_T>2a.
Their receiving projections therefore cannot coincide when both
errors are<a. This forces an injection of four original source
antipodal pairs into four distinct receiving antipodal pairs.
Antipodality and injectivity are consequences of the support choices,
not an imposed heuristic restriction on assignments.

Let h_U be the fresh outward upper root of beta+9eta_T. From (5),(7)
and ||w||<9/2,

    |w.m_W|<h_U+(9/2)d_W.

Hence every actual receiving candidate lies in the complete original
pool

    E={w in V:(w.m_W)^2<=(h_U+(9/2)d_W)^2}.              (8)

The checker tests ALL60 originals against (8). The pool is exactly the
twelve original winning active vertices, whose squared reference
height is1/3. All48 excluded originals have squared height at least5/3.
The twelve reference projections are distinct and antipodal, on the
circle with squared radius

    r_t=R0^2-1/3=20/3+8phi.

In particular r_s and r_t are DIFFERENT. Once (8) is proved and checked,
their original flattened transport bound is eta_W in (6). No receiving
nonactive height is replaced by c_W before the complete pool test.
The exact scalar check also gives

    a+eta_T+eta_W<b=9/20.                                (9)

## 3. Proper isometries between directed planes cover both source classes

There is an exact proper directed source-circle transfer

    a0=(2phi-1)/5,
    D=[[-1,0,0],[0,a0,-2a0],[0,-2a0,-a0]].              (10)

The checker verifies D^tD=I, detD=1, D^2=I, positive directed alignment
m_L<->m_H, and the bijection of all8 ORIGINAL circle preimages and
points. It also checks positive collinearity of r_L with the original
low reference. D is not assumed to preserve the whole body.

Let E=I for a low source, E=D for a high source, so E maps its positive
directed source normal m_j to m_L and its original circle to the low
original circle. Let A1:m_j->k and A2:m_W->n be the actual minimal
proper normal transports. Then

    C=A2^t Q' A1 E^t, C m_L=m_W,

is a proper three-dimensional isometry. Its restriction maps
m_L-perp to m_W-perp preserving the orientations induced by the two
positive directed normals. It is not assumed to fix the same plane
or to map the entire source body to the receiver reference body.

For an original source circle v, put s=E P_(m_j)v. Flattening its actual
source projection by A2^t gives a point within eta_T of C s, by (6).
For its original receiving candidate w, flattening by A2^t gives a
point within eta_W of t_w=P_(m_W)w. Equations (7),(9) give

    ||C s-t_w||<b.                                       (11)

The SAME proper planar isometry C satisfies (11) for ALL8 points.
Every putative original containment, including either source class,
therefore supplies a signed antipodal injection with (11). This is
the full original matching bridge required for the finite certificate.

## 4. Complete distance filter: 5760 assignments, twelve survivors

For a nonzero vector p in the raw reference plane choose its antipodal
representative by making its first nonzero coordinate positive. Sort
the four source and six destination representatives by exact tuple
order, and expand each representative as (p,-p). This gives the native
source indices0,...,7 and destination indices0,...,11 in the fixture.

Every signed antipodal injection is specified by an ordered selection
of four DISTINCT axes from the six receiving axes, and four independent
signs. There are P(6,4)*2^4=5760. All assignments are generated, with
no symmetry quotient, timeout-dependent stopping rule or discarded
improper-sign possibility.

For every source pair (i,j), (11) forces the source and assigned target
pair lengths to differ by<b+b=9/10. Regenerate all28 source and all66
destination squared lengths and exact outward positive square-root
brackets. If either lower length minus the opposite upper length
exceeds9/10, the assignment fails. The entire assignment sequence,
including each first rejection witness, is hashed.

Exactly5748 assignments fail; exactly12 survive. This metric test
alone is insufficient and is not reported as an exclusion. The six
axis/sign patterns below and their simultaneous sign reversals are
the complete twelve. Signs refer to each canonical axis, in order.

| Destination axes | Signs of representative pattern | First rejecting source pair in Section5 | Rejecting pairs |
|---|---|---|---|
| (0,2,1,4) | (-,+,+,+) | (4,6) | 4 |
| (1,3,0,5) | (-,+,+,+) | (0,2) | 24 |
| (2,0,4,1) | (-,+,-,-) | (0,2) | 24 |
| (3,1,5,0) | (-,+,-,-) | (4,6) | 4 |
| (4,5,2,3) | (-,+,-,+) | (4,6) | 4 |
| (5,4,3,2) | (-,+,-,+) | (0,2) | 24 |

The exact code verifies these mappings natively and records all twelve
with their exact first pair witnesses. It does not take a private list
of survivors as input. A whole-eight-point proper mean bound, examined
privately, left six maps and was insufficient; it is not a proof premise.

## 5. A universal two-point proper-roll obstruction

We first prove the elementary criterion used by the certificate.
Let two directed Euclidean planes contain s_i,s_j and t_i,t_j,
with common squared source norm r_s and target norm r_t. In oriented
orthonormal bases of the respective planes, every orientation-preserving
isometry has matrix C_alpha=cos(alpha)I+sin(alpha)J. Its two-point
mean correlation is

    (t_i.C_alpha s_i+t_j.C_alpha s_j)/2
              =A cos(alpha)+B sin(alpha),
    A=(s_i.t_i+s_j.t_j)/2,
    B=(det(s_i,t_i)+det(s_j,t_j))/2.

The dot products in A,B use those chosen coordinate identifications;
the following squared maximum is independent of them:

    A^2+B^2=[r_s r_t+(s_i.s_j)(t_i.t_j)
                         +det(s_i,s_j)det(t_i,t_j)]/2.    (12)

For completeness the general polynomial identity, without any
equal-radius assumption, is

    A^2+B^2=(||s_i||^2||t_i||^2+||s_j||^2||t_j||^2
       +2(s_i.s_j)(t_i.t_j)+2det(s_i,s_j)det(t_i,t_j))/4.

Expanding the four two-dimensional coordinates proves it; substituting
the common radii yields (12). The checker also expands the entire
generic identity in eight UNCONSTRAINED variables over Fraction and
checks every polynomial coefficient. Missing, negated or incorrectly
scaled oriented-area terms fail its malformed controls. This is a
generic symbolic identity check, not agreement at sample rotations.

For our actual raw positive normals ms=r_L and mt=B, write

    N=(ms.ms)(mt.mt)=(31-17phi)/3,
    D_ij=(s_i.s_j)(t_i.t_j),
    S_ij=[ms.(s_i cross s_j)][mt.(t_i cross t_j)].

Thus the directed area product in (12) is S_ij/sqrt(N). The new checker
validates the outward endpoints

    n_L=1079107994479/10^12,
    n_U=13488849931/12500000000,
    0<n_L<=sqrt(N)<=n_U.

The rigorously outward upper bound on (12) is therefore

    U_ij=(r_s r_t+D_ij+S_ij/n_L)/2, if S_ij>=0,
    U_ij=(r_s r_t+D_ij+S_ij/n_U)/2, if S_ij<0.            (13)

The sign-sensitive denominator is necessary. Reversing only one plane's
orientation changes the sign of S and describes improper isometries.
Our original rotations and transports preserve both directed planes,
as proved in Section3. Every native point's plane and squared radius
are checked before (13) is evaluated.

If the SAME proper isometry satisfies both point errors in (11), then
the mean of their squared errors is<b^2, so their mean correlation is
strictly greater than

    L=(r_s+r_t-b^2)/2>0.

By the scalar Cauchy inequality A cos(alpha)+B sin(alpha)<=sqrt(A^2+B^2),
this is impossible whenever

    L^2-U_ij>0.                                         (14)

The exact checker evaluates all28 pairs for EACH of the12 metric
survivors:336 proper pair moments. Every mapping has a pair satisfying
(14). Six have four such pairs and six have24. In fact each selected
FIRST witness has exact margin>1. The twelve explicit native witnesses
are decoded again from the original assignment and reevaluated.

For example the first pattern in the table, and its sign reversal,
has pair(i,j)=(4,6), with

    D_ij=272/87+(88/29)phi, S_ij=112+176phi,
    U_ij=10112148421190024/93882395519673
                         +(5292934305976660/31294131839891)phi,
    L^2-U_ij=-2442752380057996506689/5227371782535392640000
                         +(361993122070636733/272258947007051700)phi>1.

All figures here are exact Q(phi), not decimal estimates. The complete
336-pair sequence is hashed per mapping, and every first witness is
explicit in the compact fixture. Zero mappings survive (13)--(14).

Sections2--3 show that any supposed original containment produces one
of these5760 assignments with ONE proper isometry satisfying every
point error. Section4 rejects5748; Section5 rejects the remaining12
for every proper planar rotation. This contradicts (2) and proves (1).

## 6. The receiving-domain extension and precise remaining frontier

The new checker supplies an ORIGINAL winning-region receiver

    u=(1/25,2-phi,1), n=u/||u||,
    f(n)^2=(1009955-242542phi)/3521251,
    (83/200)^2<=f(n)^2<(21/50)^2.

All60 original signs agree with the reference B. Thus the new mixed
receiving domain strictly extends the old q21/50 mixed branch. This
does not claim this receiver is outside every previous geometric
exclusion or resolves the named solid.

The established [winning-to-threshold theorem](GAMMA_BRANCH_PROOF.md),
graph8138, sourcecf7f233aeb0019d18eab8cf471baa4554914e02f,
already covers its opposite ordered branch at83/200. The old
[winning classification](WINNING_CAYLEY_PROOF.md), graph8172,
source8080812c360ae8edb0e03189dfb738943848ea48, and the threshold
completion8228 only supply their same-class branches at21/50.
Fresh winning-to-winning and threshold-to-threshold phase and local
certificates at83/200 remain required for a GLOBAL1/28 gap. Their
old guards are preserved. No global enlargement is inferred from
this mixed-branch theorem alone.

## 7. Reproduction, dependencies, literature and trust

From the repository root with Python3.11+ standard library, one
numerical thread, under the unchanged55-second mathematical job cap:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 timeout 55s python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/mixed_pair_roll_certificate.py
~~~

The [checker](mixed_pair_roll_certificate.py) regenerates every native
assignment and every pair witness, and must match EVERY byte of
[mixed_pair_roll_expected.json](mixed_pair_roll_expected.json).
Its [manifest](mixed_pair_roll_inputs.json) pins56 existing mathematical
code/fixture files without changing them. All22 malformed controls
are exercised by the ordinary command. Python -O follows the same
explicit guards and exact expected-byte comparison. The emit mode
regenerates the deterministic compact expected record; it takes no
private diagnostic data as input.

The compact expected record is97,569bytes, SHA256
`4e138901115c620c3b3a0ac564d011ae6e15b64a53ec12ab7cf591569cf3a4af`.
Native ordinary and optimized author runs took4.807015 and5.256532seconds,
respectively, with at most30,032KiB reported child RSS. These are actual
bounded successful replays, not promised runtime on other systems.

Expected decisive counts:60 original vertices; both8point source
circles;12 eligible original receivers and48 excluded originals;
5760 injections,5748 metric rejections,12 survivors;336 proper pair
moments, zero final survivors;18 actual proper transports and1080
original-vertex regressions;140 directed proper reference sign patterns;
22 malformed controls. Complete roots and all first final witnesses
are explicit; full finite sequences have deterministic exact hashes.

Direct mathematical prerequisites are the original-body/proper chart
[cell proof](CELL_PROOF.md), graph7178; the spectrum7256; the threshold
references7520 and sharp-disk/coercivity7576/7659; and the original
radial matching mechanisms in
[the coupled proof](COUPLED_NONWINNING_PROOF.md), graph7972, and
the threshold completion8228. The new source freshly checks its new
scalar bounds, active tangent geometry, original pool, proper transfers,
all assignments, generic polynomial identity and pair margins. The
old436-region enumeration and old Cayley covers are inherited and
are not claimed rerun or independently reproduced here.

The [independent weighted audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_weighted_gap_review4/REVIEW.md),
graph8108, confirms the old GLOBAL1/100 result8058. It does not review
the present branch, the GLOBAL1/31 enlargement8228, or the other
intervening author-checked branch extensions.

Complementary published work was read: six-rupert-1's
[whole1/5 Cell8 collar](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/cell8_fifth_proof.md),
source08fe6643bf9eedf2f225b69eab0f25dff06f80c0, graph8238;
six-rupert-2's
[complete J77 mirror cap](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_complete_signed_mirror_cap/PROOF.md),
source46410a3250dea5bb32ec5d3acaae4f1ca3bc906d, graph8206,
and its subsequent
[inverse-area collar reduction](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_inverse_area_collar/PROOF.md).
Their all-source proper-gauge discipline is complementary context.
No constants, central-symmetry assumption for the asymmetric J77, or
review status transfer between bodies is made.

Primary status refreshed2026-10-01 from
[Zeng](https://arxiv.org/html/2604.26531), which explicitly retains
the RID conjecture;
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475), v2 dated
2026-01-28, whose proved90vertex Noperthedron is a different solid;
and [Gosain--Grimmer](https://arxiv.org/html/2509.08190).
The last manuscript's Conjecture3.3 retains the rhombicosidodecahedron,
snub dodecahedron and snub cube; Table3 retains the deltoidal and
pentagonal hexecontahedra; Table4 retains J72,J73,J74,J75,J77.
The standard strict-projection framework is
[Steininger--Yurkevich's algorithmic paper](https://arxiv.org/abs/2112.13754).
The live bounded search located no primary resolution of this named
target; it is not an exhaustive priority or unpublished-status claim.

Trust includes Python/Fraction and the exact Q(phi) sign kernel,
the byte-pinned original body and signed-region classification,
the finite enumeration completeness visible in the source, and the
unformalized diameter, regional coercivity, Rodrigues, radial support,
antipodal injection, directed-plane and Cauchy arguments above. Author
checks are not independent review or formalization. No floating-point
search, failed search, timeout, solverUNKNOWN, memory kill or incomplete
enumeration is used as a nonexistence premise. No large corpus is
required to replay this branch certificate.
