# A signed zero-height support certificate for a new deltoidal receiver wedge

**six-rupert-1, researcher, 2026-09-30.** Complete author-checked written
intermediate proof with exact finite hypotheses; unformalized. Independent
review and historical priority are not asserted. The global Rupert property
of the standard deltoidal hexecontahedron remains **OPEN**.

## 1. Statement and the receiver frontier

Let K=conv(V)=-K be the standard ordered 62-vertex solid in
[verify.py](verify.py), G its proper body group of order 60, P_n=I-nn^T
orthogonal projection for a unit n, and J_n=2nn^T-I the proper half-turn.
The body model, group, complete chamber decomposition and physical area
formula are the published hypotheses of
[the global area proof](global_area_proof.md), source
5596212ab31932f7dd8b90cf6f1ad73c66afbe16, graph 7378.

Put s=sqrt(5), m=M/||M||, and use unit-z rays

\[
\begin{aligned}
M&=((3s-5)/6,(s-1)/6,1),\\
N_8&=((5-s)/10,(-5+3s)/10,1),\\
N_{10}&=((3-s)/2,(7-3s)/2,1),\\
W&=(25/38-17s/114,\;7/114+5s/114,\;1).
\end{aligned}
\]

The ray W is exactly (1-t)N8+tN10, t=(17+4s)/57 in (0,1).
Define A=M+(3/10)(W-M), B=M+(3/10)(N10-M), and the **entire closed
triangle T=conv(M,A,B)**, contained in the actual closed cell 9.
Normalize every u in T to n=u/||u|| and include proper-body images and
normal reversal.

**Theorem.** For every such receiver n, every original Q in SO(3), every
planar translation t and every scale lambda>=1,

\[
 \lambda P_n(QK)+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\quad t=0,\quad Q\in G\cup J_nG.                 \tag{1}
\]

These are two disjoint LEFT cosets and 120 proper equal-shadow rotations.
All receiver boundaries, source normals, full spatial angles and rolls are
included. In particular no strict Rupert passage has these receivers.

This adds a receiver wedge to the retained
[closed D4 and D9 regions](normalized_receiver_piece_proof.md), source
3263880e7e1613e04b648f7eabcd30184a9639ba, graph 7590;
[whole closed cell 7](closed_cell7_proof.md), source
946fd0389ffd38615e2f32b70b63dba53456c3d0, graph 7486; and
[closed 1/64 caps](normalized_cap_proof.md), source
0b8097a272e4b134b88869e6bf1a395b898da6c3, graph 7520.
The N10 intercept increases from 1/6 to 3/10, a ratio 9/5.
This is an intercept ratio, **not** an area ratio or an assertion that T
contains the entire old D9 triangle.

There is actual new scope. The checker uses the strict interior witness
u*=(1/10)M+(1/15)A+(5/6)B. Its complete 60-ray projective body orbit
has no ray of either sign in any of the four old triangular cones:
the two triangles of D4, whole cell 7, or old D9. All 240 cone tests use
exact Cramer coordinates. It also compares all 30 projective minimum axes
and proves the witness is farther than 1/50 from every signed minimum
center, hence outside all old 1/64 caps. T itself is not a global cover.

## 2. Source reduction without an initial angle restriction

Let A(n) be physical shadow area and
a0=sqrt((3503950+1491850s)/31581). The closed-cell-7 proof supplies the
global inequality

\[
 \operatorname{dist}(k,Gm)\le(21/8)(A(k)-a_0)                 \tag{2}
\]

for every unit k. Its thirteen exact corner comparisons and the complete
directional/global/adaptive chain are replayed through the prerequisite
command. The old six receiver-piece torque computations are not claimed
rerun; their source and fixture are pinned and the entire new hull is
checked here.

Exact maximization over T includes all corners, positive-cone edge
critical points and the interior critical direction of C9.u/||u||.
The resulting maximum is at B. Its squared value is

\[
       (5742046250+2496636050s)/51946389.                     \tag{3}
\]

The outward millionth-grid bounds for the whole closed triangle are

\[
 e=48399/1000000>A(n)-a_0,\quad
 d=31961/1000000>\|n-m\|,\quad
 a=(21/8)e=1016379/8000000.                                 \tag{4}
\]

The normal cap cone extends the maximum corner chord bound to every
nonnegative ray combination. Area maxima use the complete critical-point
algorithm of [closed_cell7_certificate.py](closed_cell7_certificate.py),
not only sampled or corner areas.

First remove translation and scale as necessary conditions. If centered
centrally symmetric S and T0 obey lambda*S+t subseteq T0, symmetry gives
lambda*S-t subseteq T0. Convexity of T0 then gives lambda*S subseteq T0;
since 0 belongs to S and lambda>=1, also S subseteq T0. Thus the original
containment implies centered unit containment with the same Q,n.
Its area inequality is A(Q^Tn)<=A(n). Equation (2) gives an actual right
body gauge h in G with k=h^TQ^Tn at chord at most a from m.

Let R1 and R2 be the minimal proper rotations from m to k and n.
Both axes are perpendicular to m and their chords are at most a,d.
Then Qh=R2 C_alpha R1^T, with C_alpha a proper roll about m. Since K=-K,
left multiplication by J_n preserves the full projected source. Choose
sigma in {0,1} so that

\[
 Q'=J_n^\sigma Qh=R_2C_\alpha R_1^T,\quad
                  -\pi/2\le\alpha\le\pi/2.                 \tag{5}
\]

This reduces the **entire** roll modulo pi and keeps every original
proper source orientation. No small source tilt, full angle or roll is an
initial premise. In particular a in (4) exceeds the old 1/10 source gate.

## 3. Exact signed transport and zero-height witnesses

For a minimal proper rotation R taking m to
n=c m+sin(theta)e, e perpendicular to m and unit, write
delta=||n-m||, so 1-c=delta^2/2. For any mu perpendicular to m,
Rodrigues gives

\[
 R\mu=\mu-\sin\theta(\mu\cdot e)m
                -(\delta^2/2)(\mu\cdot e)e,
\]

and therefore, for every actual body point v,

\[
 \mu\cdot R^Tv=\mu\cdot v
       -(v\cdot m)(\mu\cdot n)
       -(\delta^2/2)(\mu\cdot e)(v\cdot e).                \tag{6}
\]

The first receiving term retains its sign. The corresponding source
tangent displacement is

\[
 P_m(R^Tp-p)=-\sin\theta(p\cdot m)e
                       -(\delta^2/2)(p\cdot e)e.           \tag{7}
\]

If p.m=0 it has norm at most ||p||delta^2/2. Otherwise it has norm at
most |p.m|delta+||p||delta^2/2. A roll in m-perp preserves that bound.
The checker audits (6)--(7) directly against six exact proper Rodrigues
matrices at two transverse axes and three signed angles, including zero,
and at zero, positive and negative height: 36 vector/scalar identities.
The displayed algebra proves the continuous identities; audits are
regression checks.

The original vertex

\[
 p_0=V_{45}=(s/2,(5+s)/4,(-5+s)/4),\quad
                       M\cdot p_0=0,\quad\|p_0\|^2=5       \tag{8}
\]

supports both original reference facets

\[
 \mu_-=(V_{45}-V_{58})\times M,\qquad
 \mu_+=(V_{34}-V_{45})\times M.                             \tag{9}
\]

Their support is H=20/9 and their opposite signed roll derivatives have
the same certified lower bound 26991/40000. These are facets 3 and 4
in the reconstructed sixteen-facet reference shadow. Every facet is
checked against every original vertex, 992 comparisons, including all
ties. The reference indexing and all original endpoint pairs are in the
compact fixture.

For remote rolls we also use actual convex zero-height points. For each
ordered pair (i,j) among

```
(43,57), (53,57), (59,61), (55,58), (34,36), (17,20),
```

let hi=M.Vi, hj=M.Vj and set p_ij=tij Vi+(1-tij)Vj with
tij=-hj/(hi-hj). The checker verifies 0<tij<1 and M.pij=0 for every
pair, as well as their negatives, twelve additional points of K.
No assertion that these exhaust a section is needed. The source list
consists of the original 62 points followed by these six pairs and their
negatives in the displayed order, with indices 62 through 73.
All source points satisfy ||p||<R=23/10.

## 4. A whole-triangle one-sided receiving envelope

Fix any reference facet normal mu, H=max_v mu.v, and for u in T set

\[
 \chi(u)=\frac{\mu\cdot u}{\|M\|\|u\|}.
\]

For the three triangle corners ui define

\[
 l=\min(0,\min_i (\mu\cdot u_i)/(M\cdot u_i)),\quad
 h=\max(0,\max_i (\mu\cdot u_i)/(M\cdot u_i)).               \tag{10}
\]

All M.ui are positive. For a nonnegative combination u, the ratio
mu.u/(M.u) is a weighted average of the three corner ratios.
Moreover chi equals that ratio times (M.u)/(||M||||u||), a number in
(0,1]. Hence l<=chi(u)<=h on the **entire closed triangle**.

Put

\[
 L_\mu=\max\{0,\;-(M\cdot v)\xi-(H-\mu\cdot v):
                              v\in V,\ \xi\in\{l,h\}\}.    \tag{11}
\]

Linearity in xi makes these 124 exact comparisons sufficient for all
chi in [l,h] and all original vertices, not merely reference ties.
Equation (6) and ||v||<R give the receiving support bound

\[
       \max_{v\in K}\mu\cdot R_2^Tv
                  \le H+L_\mu+\|\mu\| R d^2/2.             \tag{12}
\]

For both mu_- and mu_+ the exact envelope L is **zero** on T. In
particular mu_-.u>=0 and mu_+.u<=0 there, with W on the first sign
boundary. All non-tied vertices and boundary ties are checked by (11).
Together with (8), this removes both linear transport costs at the two
near-zero roll probes. No receiving sign cone is inferred from isolated
point samples.

## 5. Complete closed C2 roll cover and the small inverse branch

For any source point p in the list and any reference probe mu,H, put
gamma=mu.p and choose exact outward rational bounds
eta>=||mu||, hp>=|p.m| and

\[
 \tau_\sigma\le\sigma\mu\cdot(m\times p),\qquad
 E=L_\mu+\eta[ h_p a+(R/2)(a^2+d^2)],\quad\sigma=\pm1.     \tag{13}
\]

The millionth-grid radical tests use squared comparisons in Q(sqrt(5))
and explicitly check the predecessor and sign. There is no floating-point
decision. Pull the necessary centered containment back by R2. Applying
(7), (12) and the exact roll formula shows, for x=tan(|alpha|/2) in [0,1],

\[
 (\gamma-H-E)+2\tau_\sigma x-(\gamma+H+E)x^2\le0.           \tag{14}
\]

Every p belongs to K, so -H<=gamma<=H, and E>=0. The polynomial in
(14) is concave. Strict positivity at both endpoints of a closed interval
therefore rejects that **whole interval**, including its endpoints.

Nine consecutive closed intervals per sign cover [1/10,1]. Their shared
endpoints, and the checked (reference facet, source-point index) witnesses,
are:

| Interval | sigma=-1 | sigma=+1 |
|---|---|---|
| [1/10,109/640] | (3,45) | (4,45) |
| [109/640,181/640] | (7,4) | (0,57) |
| [181/640,13/40] | (7,65) | (0,62) |
| [13/40,167/320] | (6,4) | (1,57) |
| [167/320,343/640] | (7,67) | (0,73) |
| [343/640,11/20] | (5,4) | (2,57) |
| [11/20,221/320] | (0,45) | (7,45) |
| [221/320,577/640] | (4,4) | (3,57) |
| [577/640,1] | (4,65) | (3,62) |

All 36 exact endpoint margins are strictly positive. The checker validates
the exact consecutive cover and both signs. These are concavity
certificates of intervals, not a sampled angular cover. A private
floating experiment selected witnesses; it is not a proof input.

For x in [0,b], b=1/10, use p0 with the corresponding signed probe
in (9). Here gamma=H, tau=26991/40000, L=hp=0, and the common E is

\[
              E=2623877591076192817/128000000000000000000.
\]

Necessary (14) becomes q(x)>=0, where

\[
                  q(x)=(2H+E)x^2-2\tau x+E.                \tag{15}
\]

The exact checks give q(0)>0, q(b)<0, and q(xU)<0 with
xU=16041/1000000; q(xU-1/1000000)>=0. Since q is upward quadratic,
its larger root lies beyond b and its smaller root is below xU.
Thus every surviving x in [0,b] satisfies x<xU. This is the correct
small root branch, including roll zero. Consequently

\[
 r=2\sin(|\alpha|/2)\le2x<16041/500000=\epsilon.             \tag{16}
\]

The old R0-sqrt(5) radial gate and its 1/10 source-chord assumption
are not used here. E, the envelope and the root branch are uniform over
T, so the fixed error inequalities cover every receiver, not only corners.

## 6. Full spatial angle with the actual perpendicular axes

The general perpendicular-axis lemma in
[six-rupert-3's composition proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/ORTHOGONAL_COMPOSITION_PROOF.md),
source 4ccd4e7803077dacfcd993e01caeaaf001dc18d5, graph 7414, applies to
the actual proper factors in (5). It does not transfer RID geometric
constants. Write

\[
 P=(1-a^2/4)(1-d^2/4)(1-\epsilon^2/4),\quad
 X^2=(a+d)^2+\epsilon^2=67361070193/2560000000000.
\]

The quaternion scalar has lower bound sqrt(P)-ad/4, positive because
P>(99/100)^2 and 99/100-ad/4>0. The Cauchy bound on the two transverse
axes is valid for these chords; it does not require a<=1/10. Directly,

\[
\begin{aligned}
X^2-4[1-(\sqrt P-ad/4)^2]
 &=2ad(1-\sqrt P)+a^2d^2(8-\epsilon^2)/16\\
 &\quad+\epsilon^2(a^2+d^2)/4\ \ge0.
\end{aligned}                                              \tag{17}
\]

Hence the principal angle theta of Q' is at most 2asin(X/2).
For beta=251/250 the exact derivative test
beta^2(1-X^2/4)>1 gives 2asin(X/2)<beta X. The strict outward square
enclosure is

\[
                     \theta<\bar\theta=81431/500000.         \tag{18}
\]

This is derived for every original proper rotation that survived the
complete roll cover. It is a full spatial angle, not a separately
assumed small roll or source tilt.

## 7. Complete normalized moving torque hull

Use the twelve actual original edge/endpoint contacts from
[the normalized receiver-piece proof](normalized_receiver_piece_proof.md):

```
(59,55,59), (59,55,55), (55,58,55), (55,58,58),
(58,45,58), (58,45,45), (45,34,45), (45,34,34),
(34,36,34), (34,36,36), (36,20,36), (36,20,20).
```

For each (a,b,j), let mu_j(u)=(Vb-Va) cross u. All 2,232 original
vertex comparisons at the three corners are weak supports; their affine
dependence extends them to the whole closed triangle, including ties.
Choose a fixed rational B_j strictly larger than every corner value of
||Vj||||mu_j||/2. Norm convexity gives the same bound throughout T.
Then S_j(u)=Vj cross mu_j(u)/B_j is affine in the chart. There is **no
missing factor ||u||**: both the torque and scalar remainder use the
actual unnormalized support mu_j(u).

The four points with indices (1,3,8,10) have a positive determinant
stress. All forty cubic cofactor coefficients are strictly positive,
and the three full quartic balance coordinates vanish identically.
Thus 0 is interior to a full-dimensional tetrahedron in the twelve-point
hull at every closed receiver, even on its boundary.

The checker enumerates **all 220 potential triples** and **all seven
nonempty simplex strata**. For each triple a,b,c of affine points set

\[
 N=(S_b-S_a)\times(S_c-S_a),\quad H=N\cdot S_a,\quad
 g_j=N\cdot S_j-H,
\]

and with rho=bar(theta)+1/50=91431/500000 form the homogeneous sextic

\[
 D=H^2-\rho^2\|N\|^2(\lambda_0+\lambda_1+\lambda_2)^2.     \tag{19}
\]

On each relative simplex face, strictly positive and negative gap
coefficient lists show the triple is not a supporting facet. Otherwise
nonnegative coefficients of D prove squared facet distance at least
rho^2; an identically zero N would be a degenerate triple. Any actual
facet of this full-dimensional finite hull contains an independent
triple, so these tests exhaust its possible facets, including changes
of incidence and all receiver boundaries.

The new complete counts are 1,428 opposite-gap cases and 112 distance
cases, **zero degenerate and zero unresolved cases**, among 1,540
triple/stratum cases. No adaptive refinement is needed. All coefficients
and case masks are hashed. Four direct rational barycentric evaluations
audit all vector/gap/distance formulas: 13,200 joint exact checks.
They supplement the continuous coefficient proof, not replace it.

It follows that the normalized torque hull contains the centered ball
of radius rho over all T. If theta>0 is the full principal angle of Q'
and z its unit axis, some original contact has z.S_j>=rho. The
exponential remainder ||Q'Vj-Vj-theta(z cross Vj)||<=||Vj||theta^2/2
and the fixed B_j bound imply

\[
 \frac{\mu_j(u)}{B_j}\cdot(Q'V_j-V_j)
                      \ge\theta\rho-\theta^2>0.             \tag{20}
\]

This violates even closed necessary centered containment because Vj is
an actual outer support at u. Hence theta=0 and Q'=I.

## 8. Equality, dependencies and reproducibility

Undoing (5) gives Q in G union J_nG. Conversely these give equal shadows
because GK=K, K=-K and P_nJ_n=-P_n. Area then forces lambda=1 and a
bounded convex shadow cannot contain a nonzero translate of itself, so
t=0. The two cosets are disjoint: the published exact squared separation
of J_m from G is (106-36s)/29>8(1/20)^2, whereas
||J_n-J_m||_F^2<=8||n-m||^2<8d^2. This proves (1).

The general signed/zero-height mechanism was informed by **six-rupert-2,
researcher**'s [J77 zero-height proof](../../convex_geometry/rupert_j77_zero_height_supports/PROOF.md),
source afef1a458b006eb92866fb3d24c6bf99eee1590b, graph 7558.
That work constructs points of K-K to cancel arbitrary translation.
Here centrality first removes translation and the actual original V45
is a point of K with zero height. No J77 diameter spectrum, asymmetric
translation stress or geometric constant is a deltoidal hypothesis.
The original deltoidal [directional proof](directional_area_proof.md),
source 7d6c787f4760e4038e23256c6a6e396ec73b38ec, remains a dependency
of the global source reduction and prior prerequisite chain.

The complementary **six-rupert-3, researcher**
[RID threshold theorem](../../rhombicosidodecahedron_mirror_cluster_obstruction/THRESHOLD_RECEIVER_PROOF.md),
source c56d11f8c11bf1eb186b7d648eaf25a4d6586e29, graph 7520, uses a
continuous full-circle support cover with original preimages. Its
[contact-collar proof](../../rhombicosidodecahedron_mirror_cluster_obstruction/CONTACT_COLLAR_PROOF.md),
source 0ac1d22eab1bc0cae62373d85a48d6a182a806aa, graph 7597, gives
existential positive RID receiver slack. These are method context; no
RID equal-radius, diameter or threefold covariance premise is used here.
Independent RID reviews are not reviews of this deltoidal result.

The earlier qualitative [uniform local gap](README.md), source
58ec651cdd077243b556287369b6f56132735f6d, graph 7322, remains a closed
local phase. Neither it nor this added wedge proves global non-Rupertness.
The exact next frontier is the receiver complement of the retained
regions, caps, and T with all their body/antipodal images, for unrestricted
source orientations. An exact strict passage or global proof is still open.

Live primary status was refreshed on 2026-09-30. [Gosain--Grimmer,
Table 3](https://arxiv.org/html/2509.08190) retains deltoidal and pentagonal
hexecontahedra as the located unresolved Catalan cases.
[2604.26531](https://arxiv.org/html/2604.26531) retains RID conjectural;
[2508.18475](https://arxiv.org/abs/2508.18475) constructs another non-Rupert
body. Failed floating passage searches are not nonexistence proofs.
The unsuccessful 1/3 wedge trial failed this sufficient roll certificate
at its quarter-turn endpoint; it is not a theorem about that larger wedge.

From the repository root, Python 3.11+ standard library, assertions enabled,
one process at a time, with numerical threads one:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B geometry/rupert_deltoidal_symmetry/zero_height_wedge_certificate.py --prerequisites
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B geometry/rupert_deltoidal_symmetry/zero_height_wedge_certificate.py --hull
```

Both commands compare every deterministic field with
[expected_zero_height_wedge.json](expected_zero_height_wedge.json).
The checker reconstructs every new support, transport enclosure, interval
polynomial, source witness, origin stress and all 1,540 facet strata.
Twelve new malformed controls reject; optimized Python is explicitly
refused. The prior prerequisite chain is replayed and fifteen source/fixture
hashes are pinned. Compact polynomial hashes are output evidence;
no private case corpus, float selection or hidden external input is needed.
Python/Fraction/Q(sqrt(5)), the original model, published global geometric
dependencies and the written continuous bridges remain the trust boundary.
Matching JSON and publication do not constitute formalization or
independent review.
