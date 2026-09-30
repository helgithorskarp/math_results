# Signed rank-one transport closes a larger deltoidal receiving wedge

**six-rupert-1, researcher, 2026-09-30.** Author-checked written intermediate
proof with exact finite hypotheses; unformalized and independently unreviewed.
Historical priority is not asserted. **The global Rupert property of the
standard deltoidal hexecontahedron remains OPEN.**

Let K=conv(V)=-K be the standard centered 62-vertex solid generated in
[verify.py](verify.py), G its sixty proper body rotations, and
P_n=I-nn^T for a unit normal n. Put s=sqrt(5),

    M=((3s-5)/6,(s-1)/6,1), m=M/||M||,
    N8=((5-s)/10,(-5+3s)/10,1),
    N10=((3-s)/2,(7-3s)/2,1),
    W=((75-17s)/114,(7+5s)/114,1),
    D_t=conv(M,M+t(W-M),M+t(N10-M)),
    J_n=2nn^T-I.

These are raw unit-z chart coordinates; the physical normal is u/||u||.
W=(1-r)N8+rN10, r=(17+4s)/57 in (0,1). All domains below include every
boundary point and every actual proper-body or antipodal image.

**Theorem A (full prospective wedge angle).** If n is the normalization of
any u in D1, Q is any original proper rotation, lambda>=1, t is planar, and

    lambda P_n(QK)+t subseteq P_nK,                         (1)

then there exist an actual RIGHT body gauge h in G and epsilon in {0,1}
such that Q'=J_n^epsilon Qh has principal spatial rotation angle

    theta < 212461/1000000.                                (2)

In the minimal-transport frame below, its entire surviving roll has chord
less than 9859/500000. This is a necessary condition, not a receiving
exclusion on all D1.

**Theorem B (three-quarter receiving rigidity).** If n is the normalization
of any u in the entire closed D_(3/4), then, for every original Q in SO(3),
every planar t and every lambda>=1,

    lambda P_n(QK)+t subseteq P_nK
       iff lambda=1, t=0, Q in G union J_nG.                (3)

The equality set has 120 proper rotations in two disjoint LEFT cosets.
Thus no strict passage uses these receivers. This enlarges the previously
proved entire closed D_(2/3); it is not a global non-Rupert proof.

## Dependencies and scope of the new computation

The sharp source theorem is [source_extrema_proof.md](source_extrema_proof.md),
source **859cb396f54da46cb64786cbd2b72728e8d5f9db**, graph
**bafkreidd34n7ih37dmyvie3myswuj5brtdlyncpusat7tdbkmvco4dqqnm**, actually
committed at 7918. Its complete active-stratum argument proves, for every
unit original source k, with no prior frame or nearness assumption,

    A(k)<=T1=7409521/500000
       implies dist(k,Gm)<a=6571/62500.                    (4)

Here A(k) is the physical projection area in the original vertex scale.
It also proves max_D1 A(n)^2=(119575+53475s)/1089<T1^2. The new checker
hash-pins its source and fixture, replays its complete original-body,
proper-group, full area-fan prerequisite, and replays every field of the
sharp source certificate with its independent radical-sign audit.

The receiving parent is [two_thirds_wedge_proof.md](two_thirds_wedge_proof.md),
source **3276bf5919f10ad27d159578b6c17175cc078485**, graph
**bafkreicl6wlxycuxhyvmpsmj4qf4mz4t3jg5hun3ccsecopv3ytoffigyy**, actually
committed at 7805. It supplies the continuous normalized-torque ball
argument and original contacts. The signed Rodrigues identities and
reference points come from [zero_height_wedge_proof.md](zero_height_wedge_proof.md).
All reused source files are pinned. The new roll and torque inequalities
are reconstructed here; the old two-thirds torque job is not claimed rerun.
No old numerical guard is widened, no source cover is monkeypatched, and
no small-area-excess coercivity theorem is applied outside its scope.

## A signed rank-one inequality improves both transports

For any vectors x,y and unit e,

    (x.y-||x||||y||)/2 <= (x.e)(y.e)
                      <= (x.y+||x||||y||)/2.               (5)

If either vector vanishes this is immediate. Otherwise normalize x,y.
Four times the middle product is
((xhat+yhat).e)^2-((xhat-yhat).e)^2. Drop one nonnegative square and use
Cauchy on the other to prove both bounds. This handles parallel,
antiparallel and zero cases without division by a potentially zero norm.

Let R be the minimal proper rotation from m to
n=cos(theta)m+sin(theta)e, with e perpendicular to m and unit; at theta=0
choose any such e. Put delta=||n-m||, so 1-cos(theta)=delta^2/2. For a
reference facet normal mu perpendicular to m, the exact identity is

    mu.R^T v = gamma_v-(M.v) chi(u)
                      -(delta^2/2)(mu.e)(P_m v.e),         (6)
    gamma_v=mu.v, chi(u)=(mu.u)/(||M||||u||), n=u/||u||.

Take exact rational upper bounds eta>=||mu|| and r_v>=||P_m v||. Using
the LOWER bound in (5) and delta<=d gives

    mu.R^T v <= gamma_v-(M.v)chi(u)
                         +(d^2/4)(eta r_v-gamma_v).        (7)

The last coefficient is nonnegative by Cauchy, so replacing delta^2 by
d^2 is justified. This keeps the useful sign of the quadratic term.

The whole-receiver envelope is exact. For the three raw corners u_i put

    l=min(0,min_i mu.u_i/(M.u_i)),
    h=max(0,max_i mu.u_i/(M.u_i)).                          (8)

All M.u_i>0. On every nonnegative corner combination, mu.u/(M.u) is a
weighted corner average. Multiplication by (M.u)/(||M||||u||) in (0,1]
places chi(u) in [l,h], including all edges and corners. If
H=max_(v in V) mu.v, define

    B_mu=max(0,max_(v in V, xi in {l,h})
       [-(M.v)xi-(H-gamma_v)+(d^2/4)(eta r_v-gamma_v)]).     (9)

Equations (7)--(9) prove max_K mu.R^T v<=H+B_mu. Each of the sixteen
original facets uses all 62 original receiver vertices and both endpoints,
**1984 exact vertex/endpoint comparisons**, rather than receiver sampling.

For the SOURCE tilt R1:m->k, write p_perp=P_m p and |p.m|<=h_p. Exact
Rodrigues gives

    P_m R1^T p=p_perp-sin(theta1)(p.m)e1
                         -(delta1^2/2)(p_perp.e1)e1.      (10)

Let C_alpha be any proper roll about m and gamma_alpha=mu.C_alpha p.
Apply the UPPER bound in (5) to C_alpha^T mu,p_perp and e1. Because
gamma_alpha+eta r_p>=0, delta1<=a and |sin(theta1)|<=delta1 yield

    mu.C_alpha R1^T p >= (1-a^2/4) gamma_alpha
                         -eta h_p a-(a^2/4)eta r_p,        (11)

where r_p>=||p_perp||. Thus the source quadratic term also retains its
sign, even for a source point of nonzero height. Put c=1-a^2/4>0.
All perpendicular norm bounds are outward rational millionth-grid
enclosures, checked by exact squared comparisons in Q(sqrt(5)).

The written algebra proves (5)--(11) for every admitted rotation. Exact
regressions additionally check 100 rank-one inequalities, including zero,
parallel and antiparallel cases; 108 signed receiver and rolled-source
inequalities across two axes, three signed tilts, three signed rolls and
three signed heights; and all 36 ancestor Rodrigues identities. These
regressions detect implementation errors; they are not a sampled proof
of the continuous statement.

## Every original source enters a complete signed roll cover

Centered central symmetry removes translation and scale as NECESSARY
conditions: from lambda*S+t subseteq U obtain lambda*S-t subseteq U,
then average to give lambda*S subseteq U; convexity and 0 in S also give
S subseteq U. Thus (1) implies A(Q^Tn)<=A(n)<T1. Equation (4) supplies
an actual h in G with k=h^TQ^Tn at chord below a from m.

Let R1:m->k and R2:m->n be the minimal proper transports, both with
axes perpendicular to m. Since P_n J_n=-P_n and K=-K, a LEFT J_n
factor preserves the full projected source. Reducing the entire proper
roll modulo pi gives, for some epsilon in {0,1},

    Q'=J_n^epsilon Qh=R2 C_alpha R1^T,
    -pi/2<=alpha<=pi/2.                                   (12)

There is no initial spatial-angle or roll restriction. The new explicit
chord test has the declared scope 0<d<1/4 and tests the positive branch

    M.u>0, (M.u)^2>(1-d^2/2)^2 ||M||^2||u||^2.

The cap is a positive convex cone, so its corner tests extend to the
entire closed triangle. The complete physical-area maximization includes
all corner, edge and interior critical strata. It gives the following
fresh rational enclosures:

| Receiver domain | Source chord a | Receiver chord d | Roll chord upper | Full spatial angle upper |
|---|---|---|---|---|
| entire D1 | 6571/62500 | 21027/200000 | 9859/500000 | 212461/1000000 |
| entire D_(3/4) | 6571/62500 | 3963/50000 | 2441/125000 | 37271/200000 |

For a reference probe mu,H, an actual source point p, sign sigma of
alpha, and x=tan(|alpha|/2) in [0,1], choose the exact outward lower bound
tau_sigma<=sigma mu.(m cross p). Then

    gamma_alpha >= [gamma(1-x^2)+2 tau_sigma x]/(1+x^2),
    gamma=mu.p, E=eta h_p a+(a^2/4)eta r_p+B_mu.

Pull centered unit containment back by R2. Combining (9),(11),(12) gives
the necessary support polynomial

    P_sigma(x)=(c gamma-H-E)+2c tau_sigma x
                              +(-c gamma-H-E)x^2 <=0.     (13)

Because p belongs to K, gamma>=-H, E>=0, and 0<c<1, its quadratic
coefficient is nonpositive. Strict positivity at both endpoints rejects
the ENTIRE closed interval by concavity.

The reference constructor regenerates all sixteen facets of P_mK,
checks all **992** original-vertex supports, and regenerates the 62
original plus twelve checked convex zero-height source points. The
additional points use the original pairs (43,57),(53,57),(59,61),
(55,58),(34,36),(17,20), each with its negative, and exact weights
defined in the signed zero-height parent. Every point actually belongs
to K. Signed torque bounds, source heights and perpendicular norms are
recomputed exactly; no floating source point is an input.

The SAME eighteen fixed witnesses suffice for both receiver domains:

| Closed x interval | sigma=-1 probe,point | sigma=+1 probe,point |
|---|---|---|
| [1/10,109/640] | 3,45 | 4,45 |
| [109/640,181/640] | 3,45 | 4,45 |
| [181/640,13/40] | 4,72 | 3,66 |
| [13/40,167/320] | 6,4 | 1,57 |
| [167/320,343/640] | 5,4 | 2,57 |
| [343/640,11/20] | 4,63 | 3,64 |
| [11/20,221/320] | 4,63 | 3,64 |
| [221/320,577/640] | 4,4 | 3,57 |
| [577/640,1] | 4,65 | 3,62 |

Every one of the 36 endpoint margins per domain is strictly positive.
Nine consecutive closed intervals per sign cover [1/10,1], including
all common endpoints. For x in [0,1/10], use the corresponding probe
3 or 4 with V45, whose reference support is H=20/9, height is zero and
signed torque lower bound is 26991/40000. Put q=-P_sigma. Its leading
coefficient is positive, q(0)>0 and q(1/10)<0. Both domains also check
q(xU)<0 and q(xU-1/1000000)>=0, with xU respectively

    9859/1000000 for D1, 2441/250000 for D_(3/4).

The larger root lies beyond 1/10 and the smaller root lies strictly
below xU. Necessary q(x)>=0 on the surviving branch therefore forces
x<xU, including x=0. Since 2sin(|alpha|/2)<=2x, this proves the roll
chords in the table. No root branch is inferred from an unsquared sign.

The perpendicular-axis composition argument, already given in the
signed zero-height parent and
[six-rupert-3's general composition proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source **4ccd4e7803077dacfcd993e01caeaaf001dc18d5**, graph 7414, applies
to the ACTUAL proper factors (12). It transfers no RID constants.
For chords a,d,r write

    P=(1-a^2/4)(1-d^2/4)(1-r^2/4), X^2=(a+d)^2+r^2.

Both domains check P>(99/100)^2, 99/100-ad/4>0 and X^2<=1/9. The
quaternion scalar is at least sqrt(P)-ad/4>0. The identity

    X^2-4[1-(sqrt(P)-ad/4)^2]
       =2ad(1-sqrt(P))+a^2d^2(8-r^2)/16+r^2(a^2+d^2)/4 >=0

gives theta<=2asin(X/2). The derivative test beta^2(1-X^2/4)>1 and
the strict outward squared comparison yield theta<Theta as in the
table. The exact parameters are

    D1:     X^2=8920538593/200000000000, beta=503/500;
    D_(3/4):X^2=85958069/2500000000, beta=201/200.

All nonzero quaternion branches and constants are checked afresh.
This proves Theorem A and the small full-angle premise needed below.

## The complete moving torque hull closes D_(3/4)

Retain original contact ids 1 through 10 of the receiving parent:

    (59,55,55),(55,58,55),(55,58,58),(58,45,58),(58,45,45),
    (45,34,45),(45,34,34),(34,36,34),(34,36,36),(36,20,36).

For each edge/end-point triple (a,b,j) put

    mu_j(u)=(Vb-Va) cross u,
    S_j(u)=(Vj cross mu_j(u))/B_j.

All 62 original vertices at each of the three receiving corners give
**1860** exact weak support tests mu_j.(Vj-V)>=0. Linearity extends
these to the whole closed triangle. In the displayed order the positive
fixed B_j are

    113523/125000,505749/1000000,103769/200000,47651/40000,
    580603/500000,580603/500000,47651/40000,103769/200000,
    505749/1000000,113523/125000.

Each strictly exceeds ||Vj||||mu_j||/2 at all three corners, hence
throughout the triangle by norm convexity. There is no missing physical
factor ||u||: both the torque and the remainder use the SAME raw support
normal mu_j(u). The normalized S_j are affine in the chart.

Original contact ids 1,3,8,10 have forty strictly positive cubic cofactor
coefficients and three identically zero quartic vector balances.
Their rank is three. Thus zero is interior to their tetrahedron and
to the selected torque hull everywhere on the closed receiver domain.
Discarding the other two parent contacts weakens the hull; no assertion
that they are redundant is required.

All **120 potential facet triples** are checked on all **seven nonempty
relative simplex faces**, including edges and corners. The base 840
cases comprise 710 strict opposite-gap cases, 122 nonnegative
plane-distance cases and eight unresolved cases. An unresolved base
case is NOT used as proof. Three complete prefix-free midpoint covers
replace the corresponding triples:

| Original contact triple | Selected indices | All nodes | Closed leaves | Maximum depth |
|---|---|---|---|---|
| 3,4,6 | 2,3,5 | 25 | 19 | 4 |
| 5,7,8 | 4,6,7 | 33 | 25 | 4 |
| 6,7,8 | 5,6,7 | 5 | 4 | 1 |

All leaf paths are in [expected_rank_transport_wedge.json](expected_rank_transport_wedge.json).
The checker validates the FULL closed trees: every internal node has
all four children, no ancestor overlaps a leaf, and the leaf chart
areas sum exactly to the parent area. It reconstructs every supplied
patch and every one of its seven relative faces. The certificate does
not trust the adaptive discovery policy or omit an endpoint.

For a potential triple let N be the cross-product normal and H its
signed plane height. An opposite-gap case gives strictly opposite
sides for two selected points, excluding a supporting plane. A
distance case proves by nonnegative homogeneous coefficients

    H^2-rho^2||N||^2(lambda0+lambda1+lambda2)^2>=0,
    rho=37471/200000=Theta+1/1000.                         (14)

A zero normal is treated separately. No terminal degenerate case is
needed. Replacing the three base triples yields **1155 terminal
strata**, 971 opposite and 184 distance, with zero unresolved or
degenerate cases. Every genuine facet of a full-dimensional finite
convex hull has a noncollinear vertex triple. Origin-interiority and
the distance to every possible supporting facet therefore put the
centered closed rho-ball in the selected torque hull at every receiver.

The direct polynomial-to-vector audits check 6240 base identities
and 819 refinement identities. Complete base coefficient and case
hashes are, respectively,

    56f9b45ed3f5cb41cb41ec801d23dde4fdd7201e4d8de868e834f70958e5ed81,
    fafea4bac3cdaa28bebb4b9da2bd1df34a0fa2cbfe71dcdfb7c368cb0a7e34e6.

The refinement coefficient hash is

    dbb99a4674850f67086cc198047edac5d9af0b9dcf8a182260f64cef4a4af7c9.

These audits and hashes check reproducibility; the homogeneous signs
and full closed covers supply the continuous hull proof.

Let a surviving Q' have nonzero principal angle theta and unit axis z.
The centered torque ball supplies a retained j with z.S_j(u)>=rho.
The proper-rotation Taylor remainder has norm at most ||Vj||theta^2/2,
so its signed support displacement, divided by B_j, is at least

    theta rho-theta^2 > theta(rho-Theta)>0.

This contradicts centered necessary receiving containment. Therefore
Q'=I. Undoing (12) gives Q in G union J_nG. Those rotations give
equal projected shadows. Positive area forces lambda=1, and boundedness
then forces t=0. This proves (3).

The cosets are disjoint. The new checker reconstructs all sixty proper
body rotations and finds

    min_(g in G) ||J_m-g||_F^2=(106-36s)/29>8(21027/200000)^2.

For every n in D1, ||J_n-J_m||_F^2<=8||n-m||^2, so J_n is not in G.
There are exactly 120 proper equality orientations. The same conclusions
hold on proper-body images by transporting the containment, and on
antipodal images because P_(-n)=P_n and J_(-n)=J_n.

## Exact enlargement and remaining work

D_(3/4) contains the ENTIRE previous D_(2/3); its raw unit-z chart area
is **81/64** times that of D_(2/3). This is not a spherical area ratio.
The new strict interior receiver has barycentric weights
(1/10,1/15,5/6) in the new triangle and raw coordinates

    u*=((1595-359s)/2280,(4871-2009s)/2280,1).

For all sixty projective body images the checker performs exact Cramer
tests against the seven earlier triangular cones: both D4 triangles,
whole cell7, old D9, D_(2/5), D_(1/2), D_(2/3). All **420** tests
have mixed signs for both normal directions. Thirty exact squared
axis tests place u* at chord greater than 1/50 from every signed
minimum axis, outside the earlier 1/64 caps. Thus the retained
receiving union strictly grows even after all actual symmetry images.

Theorem A is intentionally retained on D1, where the current selected
torque test is INCOMPLETE. That failure proves neither a passage nor
non-Rupertness. Future work can refine the area/source budget by receiver,
use a stronger normalized contact hull or a sharper anisotropic rotation
remainder. The unexcluded global receiver complement remains open.

## Reproduction, literature and trust boundary

Run sequentially from the repository root, Python3.11+ standard library:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B geometry/rupert_deltoidal_symmetry/rank_transport_wedge_certificate.py --prerequisites
python3 -B geometry/rupert_deltoidal_symmetry/rank_transport_wedge_certificate.py --hull
```

Each command compares EVERY expected mathematical field with the compact
fixture. The hull record uses the exact SHA256 of the regenerated D_(3/4)
phase, whose full fields are already in the prerequisite record. Separate
55-second deadlines, one CPU and one process are sufficient; no solver,
CAS transcript or omitted generated corpus is an input. Python -O is
refused before computation. Thirteen malformed controls reject missing
or gapped roll intervals, incomplete or overlapping closed facet covers,
invalid child digits, duplicate/missing contacts, reversed supports, an
obsolete full-D1 receiver chord, a false perpendicular norm, discarded
signed quadratic terms and a false angle derivative factor.

Final separate replays matched every expected field: prerequisites
30.950818 seconds with peak28604 KiB; torque hull26.938770 seconds with
peak27132 KiB. The new prerequisite sign audit checked129942 calls on
12666 distinct field values; the hull audit checked42436 calls on10350
distinct values. Both separated nonzero signs with at most16decimal
digits. The sharp-source radical and original-area checks also replayed
their full pinned expected outputs. These are author checks, not review.

The original vertex model and primary status sources remain
[McCooey's standard coordinates](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt),
[Gosain and Grimmer, status Tables3--4](https://arxiv.org/html/2509.08190),
[Zeng's current conjectural rhombicosidodecahedron frontier](https://arxiv.org/html/2604.26531)
and the different proved
[non-Rupert Nopert example](https://arxiv.org/abs/2508.18475).
The bounded live literature and campaign refresh on 2026-09-30 continues
to list the deltoidal and pentagonal hexecontahedra as unresolved; no
exhaustive historical-priority search is asserted. The RID conjecture
is not a proved non-Rupert statement and no such premise is imported.
This result is an exact intermediate receiving exclusion and signed
transport lemma, not a solution of the named open problem.

The trust boundary comprises the generated standard vertex model,
the pinned original-body/area/group/source proofs, exact Q(sqrt(5)) and
radical arithmetic, the complete finite checks above, and the written
continuous geometric arguments. Independent enclosure audits check sign
implementations. No independent review or proof-assistant formalization
is asserted. A timeout, memory kill, unresolved finite case or absent
floating passage is never treated as mathematical nonexistence.
