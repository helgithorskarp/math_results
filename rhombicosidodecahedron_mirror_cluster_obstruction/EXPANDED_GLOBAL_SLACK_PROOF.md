# An expanded torque triangle gives global RID receiving slack 1/450

**six-rupert-3 — researcher — 2026-09-30.**

Complete written, unformalized intermediate proof with exact finite
certificates. Global rhombicosidodecahedron Rupertness remains **OPEN**.
The new theorem is unreviewed; historical priority is not asserted.

## 1. Precise theorem, normalization and inputs

Let phi=(1+sqrt5)/2. Let V be the sixty distinct signed even coordinate
permutations of (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).
This is the edge-two standard rhombicosidodecahedron. Put

  K=conv(V)=-K, R^2=7+8phi, P_n=I-nn^t,
  f(n)=min over actual original v in V of |v.n|,
  beta=(19-8phi)/29.

**Theorem.** For every unit original receiving normal n, every original
proper Q in SO(3), every planar translation t and every lambda>=1,

~~~text
lambda P_n(QK)+t subset int(P_nK)  implies  f(n)^2<beta-1/450.
~~~

Equivalently, every strict passage has receiving diameter squared

  >(736+960phi)/29+2/225.

The equality cutoff, all chart/order/sign walls, full original source
rotations and every planar roll are included. This strengthens the
previous [global numerical 1/1200 theorem](GLOBAL_SLACK_PROOF.md),
source d68a00c27754ac1517aba99197334e5e19fabb8b, graph
bafkreie7fdnz7e7b3wlhu4o4d7dd5rzbzkodpnoplztzxqympafq2llvbq at7703.
It does not exclude the lower-height receiving sphere.

There are two new ingredients. First, an exact full torque certificate on
a larger receiving triangle extends the conditional winning-to-winning
argument to f>909/2000. Second, the source-point injection is certified
with larger transport errors. The nonwinning bound is an explicitly
imported independent result, rather than a claimed new proof here:

[six-reviewer-2's beta-cap review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/REVIEW.md),
source 943fd6675ef2fce4f338ded9756ebb16b0d5ca9a, graph
bafkreifj3avnaurjkgkc7vcy6stoaa2v75hr2tls3yd6kh2r2neicjbm44 at7739,
proves closed all-source beta-axis chord caps1/480 and the nonwinning
necessary condition f^2<beta-1/450. Its complete proof was read.
Its [compact expected output](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/expected.json)
has SHA256
d9814ba3f397cf05387b0727a003e7fe6bf4cf0eedf329077073ef1f8e37168b.
That proof explicitly does not audit the global numerical successor.
The new checker pins its exact bytes and conclusion; it does not rerun
the review's large independent remote-roll computation.

Other inherited results are the complete436-region
[axial spectrum](GLOBAL_CAP_PROOF.md), the
[all-threshold receiver theorem](THRESHOLD_RECEIVER_PROOF.md), the
original [winning torque and folding mechanism](WINNING_RECEIVER_PROOF.md),
the [balanced support identities](BALANCED_SUPPORT_PROOF.md) and the
full continuous cone/transport/injection bridges of GLOBAL_SLACK_PROOF.md.
The new checker fully replays the latter's finite hypotheses, comparing
every field and its complete expected bytes. The old full regional,
local-cap and winning self-tests are not all claimed rerun.

## 2. Reduce arbitrary placements and exhaust source families

For symmetric convex source and receiver shadows, strict translated
containment at t also holds at -t. Convex midpoint centering then removes
t, and scaling toward the interior origin removes lambda>=1.
Centered unit strict containment is therefore necessary with the same n,Q.

The diameter identity is

  diam(P_nK)^2=4(R^2-f(n)^2).

Consequently any containment forces f(k)>=f(n), k=Q^t n.
Assume f(n)^2>=beta-epsilon, where epsilon=1/450, and set q=909/2000.
Exact guards prove

  beta-epsilon>q^2>1/7, and sqrt(beta-epsilon)>9/20.

The full436-region spectrum has10winning maxima1/3,60threshold
maxima beta and366remaining maxima at most1/7. Only winning and
threshold sources can remain. Positive height excludes every original
axial sign boundary. By the independent nonwinning theorem, all remaining
receivers are winning. By the all-threshold theorem, only the band

  beta-epsilon<=f(n)^2<=beta

needs new work. Both endpoint levels may be included during exclusion.

## 3. Complete expanded winning-to-winning torque argument

This section proves a conditional statement beyond this particular band:
if source and receiver are both in winning signed regions and their
actual heights exceed q=909/2000, then strict containment is impossible.
No threshold-source claim is included in that conditional statement.

Let n0=B/||B||, B=(0,phi^-2,1), c0=1/sqrt3.
The complete six positive original active tangents have disk squared
radius8/3+4phi>9. Write a winning normal as n=z*n0+w.
The actual positive active originals and their disk imply

  f(n)<=c0*z-rho6*||w||, rho6>3.

For f>q the right side is positive, so z>0. With c0<289/500,

  ||w||<(289/500-q)/3<1/20,
  z>199/200,
  ||n-n0||<(101/300)(289/500-q)<1/24.

These facts apply separately to the actual source and receiver.
All inequalities are checked with exact field signs or rational squares.
The existing proper-body/reversal chamber folding at chord1/24 places the
receiver in closed ABD. No improper original Q is introduced.

Let v*=(-1,phi^3,-1), an actual original vertex, and

  A=(0,0,1), D=(1/[phi(phi+2)],1/(phi+2),1),
  s=(phi-1-q)/phi, t=(phi-1-q)/(phi-1),
  U=conv(B,(1-s)B+sA,(1-t)B+tD).

In the unit-z chart u=n/n_z, ||u||>=1 and
v*.u>=f(n)||u||>q, by the winning sign of v*. Thus the folded receiver
lies in the whole closed U. The new U strictly contains the old q57/125
cut triangle. Exact corner and convexity checks retain

  ||u||<27/25, ||u-B||<27/500.

The ten persistent actual original endpoint probes (v_j,e_j) have
supports m_j(u)=e_j cross u. All1800 inequalities

  m_j(u_corner).(v_j-v)>=0, for every original v in V

are freshly verified. Linearity extends them over all closed U.
The center torque hull is regenerated and has sharp ball radius phi-1.
Each torque T_j(u)=v_j cross(e_j cross u) changes by at most
2R||u-B||<9(27/500). Since phi-1>3/5, every new hull has an
origin-interior ball greater than3/5-9(27/500)=57/500>0.
This supplies origin-interiority, without inferring it from plane
distances alone.

For all120 possible triples of the ten affine T_j and every one of the
seven nonempty relative faces of the barycentric simplex, the new checker
certifies either an impossible supporting plane by strict opposite gaps,
degeneracy, or a squared supporting-plane distance at least(1/2)^2.
It verifies all840strata:726opposite,114distance,0degenerate and
0unresolved. Whole relative-face coefficient signs include closed edges
and corners. Origin-interiority and the complete possible-facet coverage
therefore give a centered raw torque ball of radius at least1/2
throughout the whole expanded U.

The complete actual homogeneous polynomial coefficient SHA256 is

  11ecb6ff4bd190f5bdd001ffbb8378dfd25fc512500a20097e00b054ddfd63d4.

The coefficient construction is audited directly at all three corners
and a strict interior barycentric point:480 normal/support identities,
4800 gap identities and480 squared-distance identities. All120 compressed
records cover all seven relative faces with no missing stratum.

For arbitrary original proper Q, actual proper C6 body gauges and the
moving receiving half-turn J_n=2nn^t-I reduce the full roll.
The balanced C3 average cancels source tilt for both roll signs and every
tangent. The geometric identities of the parent need winning membership
and chord bounds, rather than f^2>=beta after membership is established.
At d=1/24 their unchanged remote-roll and proper-axis composition give

  E<267/6580<77/1000, full principal angle Theta<47/500.

The new q-dependent phase gates are recomputed; their unchanged bounds
are the parent's bounds, not a clamped numerical angle.
The full actual support displacement at every nonzero gauged angle
has lower coefficient

  1/2-(9/2)(27/25)(47/500)=1079/25000>1/25.

It therefore violates even closed centered unit containment. At zero
the gauged shadows coincide, excluding strictness. The original moving
J_n, all proper body factors, both normal signs and all source/roll
zero branches remain. This proves the conditional winning-to-winning
statement on f>909/2000 and excludes every winning source in the band.

## 4. Entire tangent-circle height gap and actual receiving candidates

The checker replays every original-parent angular, tangent, preimage and
height record and compares the full expected bytes. The continuous
closed-cone argument in GLOBAL_SLACK_PROOF.md Sections4--5 gives:

* All15pair-equality lines give30signed candidates and18actual directed
  rays in a complete cyclic order, with antipodes and strictly positive
  consecutive determinants. Their18closed cones cover the whole plane.
* A full six-rank permutation, valid on both closed endpoint rays of each
  cone, extends linearly to its entire positive cone. The sharp squared
  third-minus-first normalized endpoint gap is(60-12phi)/19>1.
  The triangle inequality extends this lower gap to every tangent.
* All48nonactive original center heights have square at least5/3.
  At receiving chord<1/24 their absolute heights exceed17/16.
  The six active original signs remain positive.

For the band f(n)<=sqrt(beta), the active originals give
R||w||>=c0*z-f(n). With c0>577/1000, z>199/200 and sqrt(beta)<23/50,

  ||w||>22823/900000>1/40.

Thus the third-smallest positive original height is greater than
f(n)+1/40. Only two positive originals and their antipodes, at most
FOUR actual original receiver vertices, can have absolute height at
most f(n)+1/40. All nonactive originals are separated.
This argument is uniform on the entire tangent circle, including
ordering ties; it does not sample individual directions.

## 5. Threshold sources: larger errors still permit eight-into-four

Both threshold tangent quadrilaterals have sharp disk squared radius
(39+37phi)/29>(9/5)^2. With F=sqrt(beta-epsilon), the actual source
normal k satisfies

  ||k-n_*||<(25/27)epsilon=a=1/486.

Both threshold reference shadows have eight unique original circle
preimages, squared axial height beta and radius r_beta=sqrt(R^2-beta)>4.
All56pair distances replay exactly; their common minimum square is
(40+32phi)/29>1.

Let A1 minimally and properly map n_* to k. Choose ANY proper D mapping
n_* to the ACTUAL receiving n, and put W=Q A1 D^t, so W fixes n and
Q=W D A1^t. For every actual source original v_i put

  p_i=P_nQv_i, p_i0=W D P_(n_*)v_i.

The reference points p_i0 form an exactly rolled isometric circle.
The original transport identity gives

  ||p_i-p_i0||<eta=(23/50)a+(9/4)a^2
                 =2509/2624400<1/1000.

This includes the complete proper orientations of both threshold
families and every roll. No receiving reference transport is added.
Original preimages, rather than invented planar contacts, are used.

If all p_i are contained, select an ACTUAL receiving original
q_i=P_n v'_i attaining support in direction p_i/||p_i||. Then
q_i.p_i>=||p_i||^2 and ||q_i||^2<=R^2-beta+epsilon. Hence

  ||p_i-q_i||^2<=||q_i||^2-||p_i||^2
               <L=epsilon+9eta=3157/291600<1/64.

Its original axial height is at most H=sqrt(beta+9eta)<1/2. Since
H+f(n)>9/10, exact guards give

  H-f(n)<(10/9)L=3157/262440<1/40.

Thus only the four actual originals from Section4 can be selected.
Actual source pairs remain separated by more than1-2eta>1/4, while
each ||p_i-q_i||<1/8. Two source points cannot select the same original:
their distance would be less than2/8=1/4. Eight support choices must
inject into at most four originals, a contradiction.

The parent used distance1/10 and pair1/5. Those smaller error gates are
not reused for this expanded cutoff. The new bounds1/8 and1/4 are
fresh exact sufficient bounds. Their larger values affect no vertex
count or proper-frame hypothesis.

## 6. Exhaustion, reproducibility and honest scope

The imported nonwinning1/450 theorem excludes every nonwinning receiver
under the new cutoff. The inherited all-threshold theorem excludes
f^2>=beta. Sections3--5 exclude both surviving source families for
the entire remaining winning band, including its endpoints.
The lower source families and original axial boundaries were excluded
by the complete spectrum. These cases exhaust every orientation.
Centering and scaling prove the theorem, and4epsilon=2/225 gives
the diameter condition.

The new squared-height and diameter gap are8/3times the preceding
global1/1200 gap. The nonwinning review is credited for its1/450 result;
the new work is the complete expanded winning triangle and its global
source/receiver exhaustion. Neither this quantitative gain nor a graph
commitment proves global non-Rupertness.

Reproduce from a complete repository checkout, Python3.11+standard
library, one process with numerical threads one:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/expanded_global_slack_certificate.py --self-test
~~~

Every output byte must match expanded_global_slack_expected.json.
The neighboring published review directory provides its hash-pinned
expected.json; --review-input can instead select those exact public
bytes locally. There is no network fetch inside the proof checker.
Completed normal and publication-copy optimized timing/hash/control
records are in README.md.

The original injection parent is replayed in full, including all15
malformed controls. Seventeen new malformed expanded bounds, cuts,
simplex face lists and review inputs reject in both Python modes.
The full840strata computation is NEW on the enlarged U; the large
independent beta-review computation and old full region/cap/winning
self-tests are explicitly inherited. Every expanded polynomial and
compressed case record is compared with the private exact prototype.
This is regression evidence, not independent mathematical validation.

Trust boundary: original RID coordinates, inspected exact Q(phi) and
Fraction arithmetic, Python semantics, pinned complete published
mathematical prerequisites, and the written centering, folding,
proper-frame, full-roll, facet-completeness, cone and injection bridges.
No proof assistant, solver, floating predicate, sampled continuum,
timeout or incomplete enumeration is used to prove nonexistence.
Resource limits are unchanged; mathematical jobs are sequential.

Complementary [deltoidal source-area sublevel work](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/area_sublevel_wedge_proof.md),
six-rupert-1, researcher, source c89478a5292356423b2f7ecd27563729d2dfd722,
graph7717, gives a wider deltoidal receiver wedge.
[J77 balanced caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_balanced_torque_caps/PROOF.md),
six-rupert-2, researcher, source788a042adb636949eaf06a5825e9f439d47e48de,
graph7647, and the new
[directional north triangle](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_directional_north_triangle/PROOF.md),
source a2c00c148381a36cb840571ca5b82d98e274fc35, graph
bafkreidpe47gmoytfgw2cbqprh3uxoki5drp722hvyx3xguvwmqon2vf3e at7735,
are current context. No different-body constants are transferred.
The orchestrator is the management hub; reviewers select their own work.

Live primary [2604.26531](https://arxiv.org/html/2604.26531) and
[2508.18475](https://arxiv.org/abs/2508.18475) checked2026-09-30
retain RID non-Rupertness as a conjecture and prove non-Rupertness
for a different constructed body. The strict definition follows
[2112.13754](https://arxiv.org/html/2112.13754).
No priority or complete literature-absence claim is asserted.
