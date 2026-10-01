# Coupled physical-area budgets close the entire deltoidal receiving cell9

**six-rupert-1, researcher; 2026-10-01.** Author-checked written intermediate
proof with exact finite certificates. Unformalized and independently
unreviewed; historical priority is unasserted. The global Rupert property
of the standard deltoidal hexecontahedron remains **OPEN**.

Let K=conv(V)=-K be the original standard 62-vertex body in
[verify.py](verify.py), in its existing scale and numbering. Let G be its
60 actual proper body rotations, P_n=I-nn^t for unit n, and J_n=2nn^t-I.
Put s=sqrt(5)>0 and use the following **raw unit-z chart**:

    M=((3s-5)/6,(s-1)/6,1),       m=M/||M||,
    N8=((5-s)/10,(-5+3s)/10,1),
    N10=((3-s)/2,(7-3s)/2,1),
    W=((75-17s)/114,(7+5s)/114,1),
    C9=conv(N10,M,N8),
    D1=conv(M,W,N10),             L=conv(M,N8,W).

The physical receiving normal represented by u is n=u/||u||. C9 is the
ENTIRE actual closed area cell with original corner indices [10,9,8] in
[expected_global_area.json](expected_global_area.json), including every
edge, vertex and area-fan seam. This indexing is a source convention,
not a separate modification of the named solid.

**Theorem.** For every receiver represented by C9, or any actual
proper-body or antipodal image of it, every original Q in SO(3), every
planar translation t and every lambda>=1,

    lambda P_n(QK)+t subseteq P_nK
       iff lambda=1, t=0, Q in G union J_nG.                 (1)

There are exactly120proper equality rotations in two disjoint LEFT
cosets. Thus no strict passage uses these receivers. All older cell7,
D4, D9 and 1/64-cap exclusions are retained. No global non-Rupert theorem
or passage is claimed.

**Auxiliary sharp source result.** With A(k)=Area(P_k K) for unit k and
E=Gm, put TL=739431/50000. Then

    A(k)<=TL implies dist(k,E)<85407/1000000=:a,
    85406/1000000 < max_{A(k)<=TL} dist(k,E) < a.             (2)

These are Euclidean chord distances between UNIT normals, with all
original source directions included. No source chart or small angle is
assumed in (2).

## 1. Closed receiver partition and the coupled source budget

Exactly W=(1-r)N8+rN10, r=(17+4s)/57 in (0,1). Drawing M--W in the
closed triangle C9 gives

    C9=D1 union L, D1 intersect L=conv(M,W).                 (3)

The checker verifies the original corners, every weak cell inequality,
this exact edge interpolation, positive triangle orientation and the
sum of the two raw chart areas. The elementary closed-triangle partition
proves the union, including the shared seam. The canonical raw chart
area ratio is

    Area_chart(C9)/Area_chart(D1)=3/2+(3/20)s.                (4)

This is not a spherical area ratio or a ratio of the complete orbit unions.

The inherited [global physical-area proof](global_area_proof.md) gives
A(n)=C_area.n on each original closed area cell, with the fixed vector
C_area recorded for cell9. The new complete maximization on L gives

    max_{u in L} A(u/||u||)^2
       =(4886285+2181775s)/44649 < TL^2.                    (5)

It evaluates all three corners, the stationary direction on each edge's
positive cone and the interior stationary direction. The maximum is
corner W; all three possible edge stationary directions and the interior
stationary direction are outside their admitted cones. These exact signs
and coefficients are in the fixture. TL is the first strict millionth-grid
upper bound on the square root. The normalization in (5) is essential.

The larger D1 retains its different budget T1=7409521/500000 and source
chord a1=6571/62500 from the
[sharp source proof](source_extrema_proof.md) and
[signed rank-one proof](rank_transport_wedge_proof.md), source
cdb89b3e2b7184e8c36978593a393fcb1500535d, graph7976,
bafkreidf5cjwlb6ec43cakymb27yocromqbmbhaqnnwo4zuz3cerhj4mni.
The smaller TL and a in (2) are applied only on L, not on D1 or all C9.
This receiver-dependent pairing is the new global-to-local reduction.

Here is the complete justification of (2). The byte-pinned
[source_extrema_certificate.py](source_extrema_certificate.py) implements
the general critical-stratum mechanism proved in source_extrema_proof.md,
source859cb396f54da46cb64786cbd2b72728e8d5f9db, graph7918,
bafkreidd34n7ih37dmyvie3myswuj5brtdlyncpusat7tdbkmvco4dqqnm.
Its generic certify(T,a) function is freshly run with TL,a. The old
two-budget numerical theorem alone is not substituted for this new run.

The actual120-element reflection group folds every original direction
into the closed chamber. Its orbit of m is the same as the60-element
proper body orbit, including both signs. The fresh nearest-axis replay
checks all180chamber-corner comparisons against60directed minimum axes.
Thus m is a nearest element of E throughout the chamber. Minimizing
M.k on the entire closed area sublevel in that chamber determines the
global maximum chord to E.

The fresh run covers every one of the12actual closed fan cells. It
generates234unit candidates:40corners,24sphere stationary directions,
22area-circle stationary directions,80edge stationary directions and
68area/edge intersections. Every unit norm and active equality is checked;
every cone sign and the unsquared area inequality is used for feasibility.
There are37feasible candidates. The compactness/critical-stratum argument
of the cited proof is applicable here: projected objective norms on all
actual area circles and edge great circles are nonzero, so no omitted
constant-objective component occurs. Empty circles are rejected by the
radicand sign rather than an approximate square root.

For every feasible candidate f=M.k is positive and

    f^2-||M||^2(1-a^2/2)^2 >0.                              (6)

Both factors compared before squaring are positive, so (6) implies the
strict chord cap. The exact minimum occurs on cell3/edge0 and cell6/edge2.
Their algebraic direction coordinates are proved equal component by
component; these are two closed-cell occurrences of one point. All other
35objective comparisons are strict. The fixture gives that unit direction
and objective as A+B sqrt(D) over Q(sqrt5), with all radical branches
checked. Independent rational enclosures give the chord strictly between
85406/1000000 and85407/1000000. This feasible original direction attains
the global maximum, proving both parts of (2).

## 2. Every original source enters a complete signed phase

Suppose the original closed placement on the left of (1) exists. Because
K=-K, reflected translation gives lambda P_n(QK)-t subseteq P_nK.
Taking midpoints gives centered scaled containment. Since0 belongs to K
andlambda>=1, convexity then gives the necessary UNIT containment

    P_n(QK) subseteq P_nK.                                  (7)

The same n,Q are retained. Positive projected area gives
A(Q^t n)<=A(n). For n from L, (5),(2) therefore supply an actual RIGHT
body gauge h in G such that k=h^tQ^t n has chord<a from m.
The checker also proves, by its three normalized corner comparisons,

    ||n-m||<d=14389/250000                                  (8)

throughout the closed L. The unit cap is a positive convex cone, so the
corner tests extend to every raw convex combination; M.u stays positive.

Let R1:m->k and R2:m->n be the actual minimal proper normal transports.
Their axes are perpendicular to m; zero tilt is allowed. Centrality and
P_nJ_n=-P_n permit a moving LEFT half-turn without changing the source
shadow. For some epsilon in {0,1}, the entire surviving planar roll can
therefore be represented as

    Q'=J_n^epsilon Qh=R2 C_alpha R1^t,
    -pi/2<=alpha<=pi/2.                                    (9)

No initial restriction on the original spatial angle or roll was imposed.

We use the generic signed rank-one transport inequalities of the cited
rank proof, with NEW receiver and source parameters. For reference facet
mu perpendicular to m, support H=max_V mu.v and eta>=||mu||, and an actual
point p in K with h_p>=|p.m| and r_p>=||P_m p||, those inequalities give

    max_V mu.R2^t v <= H+B_mu,
    mu.C_alpha R1^t p >= (1-a^2/4)gamma_alpha
                          -eta h_p a-(a^2/4)eta r_p.       (10)

The rank inequality underlying them is
(x.y-||x||||y||)/2 <= (x.e)(y.e) <= (x.y+||x||||y||)/2
for unit e; it handles zero and parallel vectors without division.
For gamma_v=mu.v, r_v>=||P_m v||, and

    ell=min(0,min_{u_i in L} mu.u_i/(M.u_i)),
    bnd=max(0,max_{u_i in L} mu.u_i/(M.u_i)),

the actual receiving error is

    B_mu=max(0,max_{v in V, xi in {ell,bnd}}
      [-(M.v)xi-(H-gamma_v)+(d^2/4)(eta r_v-gamma_v)]).      (11)

The ratio at any nonnegative raw corner combination is a weighted corner
average. Multiplication by (M.u)/(||M||||u||) in (0,1] keeps it inside
[ell,bnd]. Cauchy makes eta r_v-gamma_v nonnegative, justifying the
quadratic chord upper bound. Thus (11) is a whole actual receiving-body
support envelope, not an assumption about a fixed receiving hull.
All16facets,62original vertices and both endpoints are checked:
1984vertex/endpoint comparisons. The checker freshly reconstructs all
992reference-facet supports and all74actual convex source points from
the original vertices. Every extra point is an explicitly checked convex
zero-height combination, not an invented planar point. All perpendicular
norms, source heights and signed torque bounds are reconstructed with
outward exact rational bounds.

Put c=1-a^2/4>0. If sigma is the sign of alpha and
x=tan(|alpha|/2) in [0,1], let tau_sigma be the outward lower bound on
sigma mu.(m cross p), gamma=mu.p, and E=eta h_p a+(a^2/4)eta r_p+B_mu.
Pulling (7) back by R2 and using (10) gives the necessary polynomial

    P_sigma(x)=(c gamma-H-E)+2c tau_sigma x
                                      +(-c gamma-H-E)x^2 <=0. (12)

Its quadratic coefficient is negative, since gamma>=-H,E>=0,c<1.
Consequently strictly positive endpoint values reject a whole closed
interval by concavity. The NEW fixed cover has9negative and11positive
intervals. The last old positive interval is split into THREE:

| Closed x interval | sigma=-1 probe,point | sigma=+1 probe,point |
|---|---|---|
| [1/10,109/640] | 7,4 | 0,57 |
| [109/640,181/640] | 7,4 | 0,57 |
| [181/640,13/40] | 4,72 | 0,62 |
| [13/40,167/320] | 6,4 | 1,57 |
| [167/320,343/640] | 0,45 | 0,73 |
| [343/640,11/20] | 0,45 | 0,73 |
| [11/20,221/320] | 0,45 | 7,45 |
| [221/320,577/640] | 4,4 | 3,57 |
| [577/640,1] | 4,65 | use the three rows below |
| [577/640,1217/1280] | covered above | 3,57 |
| [1217/1280,2497/2560] | covered above | 3,62 |
| [2497/2560,1] | covered above | 4,64 |

All40endpoint margins are strict. The generic validator checks each sign,
the exact beginning1/10 andend1, every seam, strict interval order and
actual source/probe indices. The old parent's nine-interval guard is
unchanged. This is a fixed replay, with no adaptive search in the checker.

For x in [0,1/10], use V45 at probes3 and4 for the respective signs.
Its reference height is zero, gamma=H andtau_sigma>0. For q=-P_sigma,
the checker proves q(0)>0,q(1/10)<0 and positive leading coefficient.
The smaller root is below1/10; the larger root is above1/10.
The fresh strict grid upper xu satisfies q(xu)<0 and
q(xu-1/1000000)>=0. Thus necessary q(x)>=0 in this interval forces
x<xu, including the identity roll. Taking the worse sign gives

    2sin(|alpha|/2) < r_roll=23289/500000.                  (13)

This proves the correct small root branch, without guessing a root
from a squared inequality.

For the ACTUAL proper factors in (9), the perpendicular-axis composition
lemma from the rank proof and
[the general RID composition proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph7414,
bafkreigmk5cetignwl2kdcdsks5mbnwajuamd4znhr5iorjgol7wzmf26y,
uses no different-body constant. Put

    P=(1-a^2/4)(1-d^2/4)(1-r_roll^2/4),
    X^2=(a+d)^2+r_roll^2=22607929453/1000000000000.

Fresh checks give P>(99/100)^2,99/100-ad/4>0,X^2<=1/9 and
beta^2(1-X^2/4)>1 for beta=1003/1000. The positive quaternion scalar
branch gives theta<=2asin(X/2)<beta X. A strict outward comparison gives

    theta(Q') < 150811/1000000 on ENTIRE L.                (14)

On ENTIRE D1 the inherited exact necessary phase gives
theta(Q')<212461/1000000. The checker freshly reconstructs and matches
every field of that D1 phase, using its original parameters and guards.
It does not rerun its older torque ball. By the closed partition (3),
EVERY original placement on C9 therefore has an actual gauge as in (9)
with principal full spatial angle

    theta(Q')<Theta=212461/1000000.                        (15)

This is the missing all-source premise for the whole-cell local
obstruction. The two pieces may choose different gauges; an existence
statement for each receiver needs no agreement across their common seam.

## 3. Exact original Cayley contacts on the entire cell

For the principal axis z of Q', set w=tan(theta/2)z, with w=0 at identity.
The angle is below pi. From sin(x)<=x andcos(x)>=1-x^2/2>0,

    ||w||<R=27/250,
    R(1-Theta^2/8)-Theta/2=2320228733933/2000000000000000>0. (16)

The stronger L gate is64574913141533/2000000000000000>0.
Both are checked rationally; no floating tangent is a proof input.

Use the12original contacts (a,b,j) from
[normalized_cap_certificate.py](normalized_cap_certificate.py), j=a or b,
and define for raw receiver u

    mu_j(u)=(V_b-V_a) cross u, h_j(u)=mu_j(u).V_j,
    T_j(u)=V_j cross mu_j(u).

At EACH of the THREE full original C9 corners, all62original support
comparisons are checked, for2232total. The supports are weak where other
vertices tie; h_j and||mu_j||^2 are strict positive. Mu_j is perpendicular
to u. Linear dependence on raw u proves these exact supports throughout
the entire closed cell, including the area walls. In particular the
necessary centered containment gives

    F_j(u,w)=T_j(u).w+(w.V_j)(w.mu_j(u))-h_j(u)||w||^2 <=0. (17)

The checker proves generic polynomial orthogonality and determinant1
for the Cayley matrix

    Q(w)v=[(1-||w||^2)v+2w(w.v)+2w cross v]/(1+||w||^2),

and all36corner/contact identities
2F_j=(1+||w||^2)mu_j.(Q(w)V_j-V_j). These prove the original support
encoding, with the positive denominator and proper orientation explicit.
The signed quadratic is retained.

## 4. A fixed45-patch certificate rejects every nonzero reduced rotation

The generic signed-axis/Bernstein mechanism is proved in
[the D1 Cayley proof](cayley_wedge_proof.md), substantive source
8a91ec366772698daaf06262aa031ee9cc33630e, graph8030,
bafkreigpymzju5i3ofpeac3tnysyhem7qh5qbfebtkrwabajv6cvau3xk4.
Here its finite hypotheses are NEW and reconstructed on the full C9.
The old57D1patches are neither widened nor treated as a whole-cell proof.
No imported module constant or old guard is altered.

For w=tau z,0<tau<=R, choose a maximal-absolute coordinate of unit z.
Write z=y/||y|| with that coordinate of y equal to sigma=+1 or-1 and
the other two coordinates x,t in [-1,1]. The six CLOSED cube faces cover
every axis, sign, tie and seam. For a chosen original contact put

    L_j(u,y)=T_j(u).y,
    B_j(u,y)=(y.V_j)(y.mu_j(u))-h_j(u)||y||^2.

On a fixed dyadic square, the exact integer square-root calculation
supplies ell>=1 with

    ell^2<=1+min_{square}x^2+min_{square}t^2<(ell+1/1000000)^2.

Thus||y||>=ell. The certificate checks at all three full receiving
corners the four affine corner coefficients of L_j and the nine tensor
degree(2,2)Bernstein coefficients of ell L_j+R B_j. ALL are strict
positive. The six monomials of the Bernstein conversion are independently
reconstructed as polynomial identities, including the mixed coefficient.
Both expressions are affine in raw u, so positivity extends over the
ENTIRE closed receiving triangle as well as each entire closed axis box.

At tau=0,||y||L_j>0; at tau=R,
||y||L_j+R B_j>=ell L_j+R B_j>0. Affinity in tau proves positivity for
every0<=tau<=R, regardless of the sign of B_j. Consequently

    F_j(u,tau z)=tau[||y||L_j+tau B_j]/||y||^2>0,          (18)

contradicting (17) for every nonzero w.

The new fixed cover's six leaf counts, in axis/sign order
(0,-),(0,+),(1,-),(1,+),(2,-),(2,+), are

    7,7,13,7,7,4; total45closed leaves, maximum depth3.

All12original contacts are reconstructed; the selected leaf witnesses
use original IDs1through10. For every square the validator checks a
unique prefix-free complete four-child tree and exact area weight1,
including all closed subdivision seams. The new strict coefficient count
is45*3*(4+9)=1755. Every coefficient is regenerated and hashed. There are
2160direct face polynomial audits and1215leaf vector/Bernstein audits;
these implementation regressions complement the exact basis identities
and the continuous proof, rather than replacing them with point samples.
The discovered private45-patch cover is replayed FIXED in the public
checker. Its full entry-level coefficient hashes match the private replay.

## 5. Equality, proper-body images and strict enlargement

Equation(18)forces w=0 andQ'=I. Undoing the actual right body factor and
moving LEFT half-turn gives Q in G union J_nG. Conversely every such
rotation gives P_n(QK)=P_nK, because G preserves K andK=-K. Positive
projected area forces lambda=1 in (1); support functions of a bounded
convex shadow then force t=0 from its translated containment.

The checker freshly constructs all60body rotations, proves their Gram
and determinant identities and3720original vertex permutation checks.
At m the minimum squared Frobenius distance from J_m to G is exactly

    (106-36s)/29 >8(21027/200000)^2.

All THREE full C9corners have normalized chord below21027/200000 from m,
and the same positive cap cone covers their closed combinations. Since
||J_n-J_m||_F^2=8[1-(n.m)^2]<=8||n-m||^2, J_n is never a member of G
anywhere on C9. The two LEFT cosets are therefore disjoint and have120
members. Conjugating by actual proper body rotations preserves every
claim; P_{-n}=P_n handles antipodal receivers. This proves (1).

The new interior raw ray is

    u*=(43/114-(37/855)s, -367/855+(461/1710)s,1)
       =(1/10)M+(5/6)N8+(1/15)W.

All three barycentric weights are positive. Its60projective proper-body
images are tested against the NINE prior closed triangular cones,
including the entire old D1:540exact Cramer-coordinate tests, treating
both projective signs, give no membership. It has chord>1/50 from all30
projective minimum axes, hence lies outside the old1/64caps. The finite
orbit tests include all old body/antipodal images. Thus the stated
excluded union strictly grows; this is not just a reparameterization of
an earlier domain. All prior independent receiving regions remain valid.

## 6. Reproduction, dependencies and status

From the repository root, Python3.11+ standard library, run with numerical
threads1 and an unchanged55-second cap:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell9_coupled_certificate.py
~~~

Every mathematical field must match
[expected_cell9_coupled.json](expected_cell9_coupled.json),48,434bytes,
SHA2562dd4297158e3af60b37613569527cb401f2452a3c71ef056b6e6cb16841a2f4c.
The checker uses20fixed roll intervals and45fixed axis patches; it has no
adaptive proof search. It rejects20malformed controls, including a missing
global source cell, a false smaller source cap, missing/gapped signed roll
coverage, malformed axis covers and an incorrect Bernstein mixed term.
Optimized Python is explicitly refused BEFORE mathematical imports,
because inherited exact guards require assertions.

All24imported source/fixture files are byte-pinned. The global physical-area
fan and its original named-solid proof are inherited; the NEW234source
critical strata, new20-interval phase, full-cell original supports,
45-patch coefficients, group permutations, equality separation and new
receiving witness are freshly reconstructed. The whole D1necessary phase
is freshly matched; its old local torque enumeration is not rerun.
Every exact field sign in the MAIN verification phase has an independent
rational sqrt(5) enclosure. The signs used by radical and cross-radical
comparisons receive independent rational enclosures or exact zero-branch
identity checks.
Imported byte-pinned constructors belong to inherited prerequisites and
are outside the main-phase audit counter.

Trust remains in the original coordinate/solid identification, inspected
Python/Fraction/Q(sqrt5)and radical semantics, hash-pinned prerequisites,
finite certificate replay and the written unformalized continuum bridges
above. Author validation is not independent review or formalization.
No float, failed search, timeout, UNKNOWN or incomplete enumeration
supplies a mathematical nonexistence premise.

Complementary sources read in full: six-rupert-2,researcher,
[J77 receiving-balanced signed tangent frontier](../../convex_geometry/rupert_j77_receiving_balanced_stress/PROOF.md),
final source41ad5faf8d88b8c5a30358023e0c47168551da96, graph8086,
bafkreifpv2hgmtdfdcgdh3v5d2txmkzj5illszcj2asrq7xgtn2cxc4y5q;
and six-rupert-3,researcher,
[RID original weighted moments and global gap1/100](../../rhombicosidodecahedron_mirror_cluster_obstruction/WEIGHTED_GLOBAL_BAND_PROOF.md),
sourcee8f808484cb7ad21bf95438833f5737355c5ff8a, graph8058,
bafkreicnr745nfwsx3c3wk4ik4r7thrllinwasej7mztmqadzpxymbp2cm.
They are methodological context, not different-body theorem premises.
Neither the J77 mirror companion nor RID constants are imported. Their
global named problems also remain open. No reviewer was directed or asked
for a verdict; the orchestrator remains the management hub.

Current primary status was refreshed live at the start of this pass:
[Gosain--Grimmer Tables2/3/4](https://arxiv.org/html/2509.08190) retain the
deltoidal and pentagonal hexecontahedra among the unresolved named cases;
[Zeng2604.26531](https://arxiv.org/html/2604.26531) retains the RID
non-Rupert conjecture;
[Steininger--Yurkevich2508.18475](https://arxiv.org/abs/2508.18475) prove a
different Noperthedron non-Rupert. The
[standard strict proper-shadow framework](https://arxiv.org/abs/2112.13754)
is retained. A bounded literature search is not exhaustive absence or
priority evidence. The remaining deltoidal receiving complement needs a
new all-source reduction or construction; its global decision is open.
