# Original-source rigidity on the entire closed 1/5 Cell8 collar

**six-rupert-1, researcher, 2026-10-01.** Complete author-checked written
intermediate proof with exact finite hypotheses. It is unformalized and
independently unreviewed; historical priority is unasserted. The global
Rupert property of the standard deltoidal hexecontahedron remains **open**.

Let K=conv(V)=-K be the original 62-vertex body in [verify.py](verify.py),
with its existing numbering and scale. Let G be its 60 proper rotations,
P_n=I-nn^t and J_n=2nn^t-I for a unit vector n. The raw chart coordinates are

    s=sqrt(5)>0, M=N9=((3s-5)/6,(s-1)/6,1), m=M/||M||,
    N8=((5-s)/10,(-5+3s)/10,1),
    N10=((3-s)/2,(7-3s)/2,1),
    W=((75-17s)/114,(7+5s)/114,1),
    U=(N6+N11+N10+N8)/4, Z_t=(1-t)W+tU,
    L=conv(N8,W,Z_1/5), B=conv(W,N10,Z_1/5),
    F_1/5=conv(N8,N10,Z_1/5)=L union B.

N_j are the exact original area-fan nodes in [expected_global_area.json](expected_global_area.json).
Cell8 is conv(N6,N11,N10,N8). Physical normals normalize the raw vectors.

**Theorem.** For every receiver n represented by the entire closed F_1/5,
or an actual proper-body or antipodal image, every original Q in SO(3),
every planar translation t and every scale lambda>=1,

    lambda P_n(QK)+t subseteq P_nK
      iff lambda=1, t=0, Q in G union J_nG.                 (1)

The two LEFT cosets are disjoint and contain exactly 120 proper rotations.
Consequently strict passage is excluded on this entire closed collar.
The entire Cell8, its remaining receiving complement and the global
named-solid decision remain **open**. All older receiving exclusions
remain valid. This result strictly enlarges their combined domain.

The [preceding Cell8 collar proof](cell8_collar_proof.md), source
4e2806a83f17c20fe755354a0b9b57f0bfef2e3a, graph8186,
already established B and the first triangle only to parameter1/10.
We prove (1) on the remaining L. W lies strictly on N8--N10, with
W=(1-r)N8+rN10 and r=(17+4s)/57 in (0,1). Thus the two closed triangles
partition F_1/5, including their common edge. No union convexity assumption
is needed beyond this explicit partition.

## 1. Original-source area and the two proper source charts

On L the physical area is A(n)=C8.n, where C8 is the original Cell8 area
vector from [global_area_proof.md](global_area_proof.md), graph7378.
Complete corner, edge and interior maximization gives

    max_L A(n)^2=(16831278421101230+7510892433621670s)/153054749858769,
    T=2964457/200000, a=10739/100000, d=7237/100000.          (2)

The maximum is Z_1/5. The checker verifies all stationary admissions,
T^2 strictly above this maximum, and ||n-m||<d on all normalized corners.
The acute chord cap is a convex cone, so the same strict bound holds
throughout the closed receiving triangle.

The complete [source-critical mechanism](source_extrema_proof.md), graph7918,
is freshly replayed at THIS budget and source chord. It includes all12
closed original fan cells, all unsquared feasibility and radical branches:
214 candidates (40corners,24sphere,20area,80edge,50area/edge),55feasible.
Every feasible cap margin is strict. The unique sharp maximizing direction
has two boundary occurrences, Cell8/edge1 and Cell10/edge2; its chord lies
strictly in (a-1/1000000,a). Thus, for every ORIGINAL unit source k,

    A(k)<=T implies dist(k,Gm)<a.                          (3)

This is a global source theorem, with no assumed source nearness or roll.
The original proper-body/area-fan geometry is inherited and byte-pinned;
the new budget's complete critical strata are freshly computed.

Direction information requires care with proper gauges. The original full
reflection group F has120 elements and its determinant+1 subgroup is G.
Let S be its third-wall reflection, normal (-phi,-phi^2,1), with
phi=(1+s)/2. Then SM=M and S permutes the original62 vertices. The old
folding theorem sends every source to the closed fundamental chamber H
with an f in F. If detf=+1, use the actual RIGHT body gauge h=f. If detf=-1,
use h=fS in G; the gauged source instead lies in SH. Therefore the proper
source charts are **both H and SH**, each with12 closed fan cells. We
never assume an improper source rotation is an admissible proper gauge.
The sharp bound (3) remains valid in both charts because S fixes m.

## 2. Necessary support inequalities for the entire signed roll

Central symmetry sends a supposed translated containment also to its
negative translation. Convex midpoints remove t, then contraction toward
0 removes lambda>=1 as a necessary condition. Hence A(Q^tn)<=A(n)<T.
Choose the proper gauge just described and write k=h^tQ^tn. Let R1 and R2
be the minimal proper transports m->k and m->n. A LEFT J_n factor preserves
the projected original source because P_nJ_n=-P_n and K=-K. Reducing the
roll modulo pi gives, for some epsilon in {0,1},

    Q'=J_n^epsilon Qh=R2 C_alpha R1^t,
    -pi/2<=alpha<=pi/2.                                   (4)

This covers every original source placement, with no initial spatial
angle restriction. Let sigma be the sign of alpha and x=tan(|alpha|/2)
in [0,1]. The original reference shadow P_mK has16 exact facet probes
mu,H, with mu.m=0 and H=max_(v in V)mu.v. For any actual source point p
in K, pull unit containment back through R2 to get

    mu.C_alpha R1^t p <= max_(v in V)mu.R2^t v <= H+B_mu.   (5)

The signed [rank-transport proof](rank_transport_wedge_proof.md), graph7976,
supplies a whole-receiver bound B_mu. Explicitly, put eta>=||mu||,
r_v>=||P_m v|| and chi(u)=mu.u/(||M||||u||). Exact corner ratios enclose
chi(u) between l=min(0,corner ratios) and h=max(0,corner ratios). Then

    B_mu=max(0,max_(v in V, xi in {l,h})
            [-M.v*xi-(H-mu.v)+(d^2/4)(eta*r_v-mu.v)]).      (6)

The signed Rodrigues/rank-one argument proves (6) throughout L. All1984
original vertex/endpoint comparisons are reconstructed, not sampled.
The16 probes and all62 original plus12 checked convex zero-height points
are freshly reconstructed from the pinned original model.

For most roll intervals the same source rank bound suffices. Define
c_s=1-a^2/4, gamma=mu.p, r_p>=||P_mp||, h_p>=|m.p|, and choose the exact
outward lower tau_sigma<=sigma*mu.(m cross p). Necessary containment gives
the concave polynomial

    P(x)=(c_s*gamma-H-E)+2*c_s*tau_sigma*x
                            +(-c_s*gamma-H-E)*x^2 <=0,
    E=eta*h_p*a+(a^2/4)*eta*r_p+B_mu.                       (7)

Strict positivity at both endpoints rejects an entire closed interval.
The fixed certificate supplies the following16 standard intervals:

| sigma | closed x interval | probe | source point |
|---|---|---|---|
| -1 | [1/10,17/80] | 3 | 45 |
| -1 | [17/80,13/40] | 2 | 45 |
| -1 | [13/40,7/16] | 1 | 45 |
| -1 | [7/16,79/160] | 1 | 45 |
| -1 | [79/160,167/320] | 1 | 45 |
| -1 | [167/320,11/20] | 5 | 4 |
| -1 | [11/20,31/40] | 0 | 45 |
| -1 | [31/40,1] | 4 | 65 |
| +1 | [1/10,17/80] | 4 | 45 |
| +1 | [17/80,13/40] | 0 | 62 |
| +1 | [13/40,11/20] | 1 | 57 |
| +1 | [11/20,31/40] | 7 | 45 |
| +1 | [31/40,71/80] | 3 | 57 |
| +1 | [71/80,151/160] | 3 | 62 |
| +1 | [151/160,311/320] | 3 | 62 |
| +1 | [631/640,1] | 4 | 64 |

The positive interval I=[311/320,631/640] is proved differently below.
Its inclusion makes consecutive closed covers of [1/10,1] for both signs.

## 3. Exact source-height transport preserves directional gains

Set L0=||M||, M2=M.M, and write a gauged raw source as q=M+w with M.w=0.
Its normalization is k=q/r, where r=||q|| and c=m.k=L0/r. Formula (3) gives

    c>c0=1-a^2/2>0, ||w||^2<U0=M2*(1/c0^2-1).              (8)

Exact minimal-transport Rodrigues gives

    P_mR1^t p=P_mp-(M.p)/(L0*r)*w-(p.w)/(r*(r+L0))*w.       (9)

At w=0 both correction terms vanish, so no tilt direction is undefined.
For positive roll put

    z=M cross mu,
    mu_tilde(x)=(1-x^2)mu-2x*z/L0,
    l(c)=c/M2, b(c)=c^2/(M2*(1+c)), h=M.p.

Taking support in (9) gives the EXACT signed source numerator

    (1+x^2)*mu.C_alpha R1^tp
      =gamma(1-x^2)+2*mu.(m cross p)*x
                       -[l(c)h+b(c)(p.w)]*(mu_tilde(x).w). (10)

The last term can be negative, giving a useful increase of support.
In particular, we retain its signed height term rather than replacing
every original vertex with a zero-height convex combination.

Both l,b increase on [c0,1]: b'(c)=c(2+c)/(M2*(1+c)^2)>0. Let their endpoint
midpoints be lbar,bbar and halfwidths el,eb. Take strict rational bounds

    21199/20000<L0<1059951/1000000,
    1/L0 in [IL,IH], IM=(IL+IH)/2, IE=(IH-IL)/2,
    IM=21199010000/22469901249, IE=10000/22469901249.

Use Rw>=sqrt(U0), rp>=||P_mp|| and rz>=||z||, all exact outward millionth
grid bounds. With lo=311/320 and hi=631/640, the loss in (10) is at most

    [lbar*h+bbar*(p.w)]*([(1-x^2)mu-2x*IM*z].w)+Err,
    Err=el*|h|*(1+hi^2)*eta*Rw
        +eb*rp*(1+hi^2)*eta*U0
        +(l(1)*|h|+b(1)*rp*Rw)*2hi*IE*rz*Rw.               (11)

Indeed ||mu_tilde(x)||=(1+x^2)||mu||; replacing l,b by their midpoints
has the first two errors, and replacing1/L0 by IM has scalar error at
most2hi*IE*rz*Rw. The midpoint factors are bounded by their upper endpoints
in the last error. These estimates apply to actual sources satisfying
(8); the enclosing polygons need not themselves lie inside that cap.

## 4. Complete closed source polygons and a fixed roll cover

Use tangent basis B1=(1,0,-M_x), B2=(0,1,-M_y), and w=y1*B1+y2*B2.
The inverse Gram matrix and (8) give the coordinate bounds
|y1|<55061/500000, |y2|<7009/62500. Add16 CLOSED chord half-planes from
the eight tangent directions B1,B2,B1+/-B2,2B1+/-B2,B1+/-2B2:
|v.w|<=upper_sqrt(U0*||v||^2). Their intersection is a20-corner polygon
enclosing every actual source in the cap.

For each original closed fan cell, intersect its inward cone sides
E.(M+w)>=0 and the necessary area half-plane

    Ccell.(M+w)<=T*MH/c0, MH=1059951/1000000.                (12)

Every source in H is retained because its area is Ccell.k<=T and r<L0/c0.
Reflect each COMPLETE enclosure through the actual S to cover SH. It is
unnecessary to assume invariance of the polygonal chord enclosure.

At each fixed tree node apply two further necessary area cuts. The convex
quadratic ||w||^2 has its polygon maximum at a corner. Hence an actual
source in the current polygon has

    r<=upper_sqrt(M2+min(U0,max_polygon_corners||w||^2)).    (13)

Use T times this bound in (12) and repeat once. These are outer cuts;
every actual source remains in the current polygon. Closed clipping
retains zero-dimensional and edge cases. Sourcecells0 and11 are empty
in both copies. Only cells8 and9 need one binary split: bisect the longer
coordinate range at its exact midpoint, keeping BOTH closed halves,
then repeat the two cuts. Ties choose coordinate1. Paths0 and1 mean
respectively the >= and <= halves. The public verifier checks full
prefix-free binary coverage of all24 cell copies, including empty leaves.

For fixed w, the midpoint product in (11) is a quadratic in x with
nonnegative Bernstein basis on I. Its three coefficient vectors are

    v0=(1-lo^2)mu-2lo*IM*z,
    v1=(1-lo*hi)mu-(lo+hi)*IM*z,
    v2=(1-hi^2)mu-2hi*IM*z.                                (14)

Consequently its upper bound over I and a polygon is the maximum over
j=0,1,2 of

    max_polygon [lbar*h+bbar*(p.w)]*(vj.w).                 (15)

Each maximum is attained on the polygon boundary. Along a nonzero
tangent direction perpendicular to P_mp, the first factor is constant
and the product is affine. From an interior point at least one boundary
endpoint has no smaller value. For P_mp=0 choose any tangent direction.
On every polygon edge the product is quadratic; check both endpoints
and its admissible concave stationary point. Segments and singletons
are also handled. A NEGATIVE uniform maximum is retained.

Let U be (15)'s maximum plus Err. Equations (5),(10),(11) give the necessary
concave polynomial, valid on that entire source polygon and closed I,

    (gamma-H-B_mu-U)+2*tau_+*x+(-gamma-H-B_mu)*x^2 <=0.      (16)

Its quadratic coefficient is nonpositive because gamma>=-H and B_mu>=0,
regardless of the sign of U. The fixed28 leaves consist of24 actual
support witnesses and4 empty cells. Both endpoint margins at EVERY
support leaf exceed1/100000 exactly. Thirteen leaves have U<0. The
original-source witnesses are:

| cell | H copy: path -> probe,point | SH copy: path -> probe,point |
|---|---|---|
| 0,11 | empty root | empty root |
| 1 through7 | root -> 3,57 | root -> 3,57 |
| 8 | 1 -> 3,62; 0 -> 4,53 | 1 -> 4,53; 0 -> 3,57 |
| 9 | 1 -> 3,57; 0 -> 4,53 | 1 -> 3,57; 0 -> 4,53 |
| 10 | root -> 3,43 | root -> 3,43 |

Thus (16) rejects all sources in BOTH proper-gauge charts on I.
This closes the entire signed roll cover; every common endpoint is included.

## 5. Surviving small roll, local rigidity and equality

On [0,1/10], use (7) at original zero-height V45, probe3 for negative roll
and probe4 for positive roll. Put q=-P; its leading coefficient is positive,
q(0)>0 and q(1/10)<0. Exact root-sign comparisons at a millionth-grid upper
and its predecessor give small-root uppers6909/250000 and10177/1000000.
The larger root lies beyond1/10. Therefore necessary q(x)>=0 forces
x below these uppers, and the surviving full signed roll has chord

    roll_chord<6909/125000.                                (17)

Apply the perpendicular-axis quaternion composition lemma from the
[signed transport proof](rank_transport_wedge_proof.md) and
[six-rupert-3's composition proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md), graph7414.
For the ACTUAL factors (4), X2=(a+d)^2+roll_chord_upper^2 is
552635181/15625000000. The quaternion-product and derivative gates are
positive with beta=201/200. They give the principal FULL spatial angle

    theta(Q')<94503/500000=0.189006,
    (1/8)*(1-theta_upper^2/8)-theta_upper/2
                    =479021182991/16000000000000>0.        (18)

Thus the actual Cayley vector has norm tan(theta(Q')/2)<1/8. No different
body's motion constants or common-radius hypotheses are transferred.

The [preceding Cell8 proof](cell8_collar_proof.md) gives the local Cayley
mechanism at radius1/8. We FRESHLY reconstruct the original20-corner hull
on L, its cross sum equal to the actual physical C8,40 endpoint contacts
and their20 distinct exact polynomial rows. All7440 original support
comparisons,60 Cayley displacement identities,9 Gram and1 determinant
identities are checked. The new triangle's fixed six-face axis cover has
leaf counts(4,25,7,4,4,4),48 leaves, maximumdepth4. All1872 linear/Bernstein
coefficients are strict, with3600 face and1296 leaf vector/basis audits.
The parent radius27/250 and depth3 guards are unchanged.

For completeness, an endpoint contact (edge,Vj) has torque Tj=Vj cross mu
and height H_j=mu.Vj. A necessary Cayley support difference is
Tj.w+(Vj.w)(mu.w)-H_j||w||^2<=0. On each closed axis patch the fixed
certificate proves its linear term positive and its linear-plus-radius
quadratic combination positive at radius1/8, for all three receiving
corners. Receiver affinity, the Bernstein basis, a certified axis-norm
lower and interpolation in the radial parameter then make this support
difference strictly positive for every0<||w||<=1/8. This contradicts
containment. Hence w=0 and Q'=I.

Undoing the actual RIGHT h and LEFT J_n proves Q in G union J_nG.
These rotations conversely give equal shadows. Positive shadow area
forces lambda=1; bounded-shadow support functions force t=0. The inherited
minimum squared Frobenius distance from J_m to G is (106-36s)/29>8d^2,
and ||J_n-J_m||_F^2<=8||n-m||^2. Thus J_n is not in G throughout L;
the120 equality rotations are distinct. The parent proves the same on B.
Proper-body conjugation and P_(-n)=P_n give all stated images.

The interior witness (N8+W+4Z_1/5)/6 has60 projective proper-body images
outside all12 previous triangular cones, including the entire Cell9 and
both preceding Cell8 pieces, by720 exact Cramer tests with BOTH projective
signs. Its chord exceeds1/50 from all30 projective minimum axes, so it is
also outside the old1/64 caps. This proves strict enlargement of the
combined excluded receiving domain. No spherical area ratio is asserted.

## 6. Reproduction, dependencies and trust

From the repository root, Python3.11+ standard library, one numerical thread,
under the unchanged55-second mathematical job cap:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 timeout 55s python3 -B geometry/rupert_deltoidal_symmetry/cell8_fifth_certificate.py
~~~

The [fixed checker](cell8_fifth_certificate.py) must match EVERY field of
[expected_cell8_fifth.json](expected_cell8_fifth.json),50,755bytes, SHA256
`e61abcdd15e9229362588bcab15e2bb07a93ce1bbc6a3857bbcd3c1594ba21c1`.
Expected output:214 source candidates/55feasible,24 strict source leaves
plus4empty,48axis leaves/1872strict coefficients, fullangle94503/500000,
19malformed-evidence rejections. Python -O is refused before mathematical
imports. The checker includes162 exact signed-height Rodrigues regressions,
18 roll-Bernstein component identities,3 clipping degeneracy cases, and a
negative-gain regression. These complement the written universal algebra.
The entrywise source-polygon/support digest is
`b56b5d17ef40c7576cd705b127d3eba74b8284b0cf576ce5d1e36b1953e4e29d`.

The checker pins28 inherited code/fixture files, including the prior
Cell8 certificate and fixture. The old B proof and its finite certificate
are used as established author-checked prerequisites; its entire job is
not rerun or claimed independently checked here. Whole-Cell9 graph8130,
source db665591225afc452b0d92fecdad2070eef2df17, and Cayley graph8030
remain prerequisite context. The original model, proper group, area fan,
complete source strata, signed receiver bounds and local mechanism retain
their earlier explicitly scoped trust boundaries.

Trust includes Python/Fraction, exact Q(sqrt5)/quadratic-radical kernels,
the byte-pinned original geometry, and the unformalized convexity,
critical-stratum, proper-fold, transport, closed-cover, root, quaternion
and Cayley arguments. Independent rational enclosure audits check all
executed main-phase nonzero field/radical signs; zero radical signs use
exact identities. Imported constructors remain inherited prerequisites.
All28 source entries and all receiver/source-critical fields match the
private discovery entry by entry. This is author checking, not independent
review, algorithmic independence or formalization. No floating sample,
failed passage search, timeout, solverUNKNOWN or partial enumeration is
a premise of the theorem. No large enumeration output is needed.

Complementary work read includes [six-rupert-2's complete J77 mirror cap](../../convex_geometry/rupert_j77_complete_signed_mirror_cap/PROOF.md),
source46410a3250dea5bb32ec5d3acaae4f1ca3bc906d, graph8206, and
[six-rupert-3's RID winning-receiver rigidity](../../rhombicosidodecahedron_mirror_cluster_obstruction/WINNING_CAYLEY_PROOF.md),
source8080812c360ae8edb0e03189dfb738943848ea48, graph8172, plus the preceding
[RID full-roll exclusion](../../rhombicosidodecahedron_mirror_cluster_obstruction/GAMMA_BRANCH_PROOF.md), graph8138.
The subsequent [RID threshold completion](../../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_CAYLEY_PROOF.md),
source411ae5ebba4c5c426650c491ed48742ebeff0231, graph8228, increases its
global strict-passage receiving gap to at least1/31. Its original matching
and local contact methods were read at bounded statement/method scope.
Their body-specific constants and review status are not imported.
The signed-kernel audit, graph7881, provides methodological context;
no separate audit implementation or review status is imported.

Primary status refreshed2026-10-01 from [Gosain--Grimmer](https://arxiv.org/html/2509.08190),
[Zeng](https://arxiv.org/html/2604.26531),
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475), and the
[standard strict-projection framework](https://arxiv.org/abs/2112.13754).
The searched sources retain the deltoidal and pentagonal hexecontahedra
as unresolved Catalan cases. This bounded refresh is not exhaustive
historical-priority evidence. The global deltoidal Rupert problem is open.
