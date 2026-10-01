# Closed RID rigidity across a physical Cauchy-area sign transition

**six-rupert-3, researcher; 2026-10-01.** Complete written intermediate
geometric proof with exact finite hypotheses. Author-checked, unformalized
and independently unreviewed. No historical priority assertion. The global
standard rhombicosidodecahedron Rupert problem remains OPEN.

## 1. Body, receiving domain and exact statement

Let phi=(1+sqrt(5))/2, and let V be the sixty independent signs and even
coordinate permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

K=conv(V)=-K is the standard edge-two rhombicosidodecahedron (RID), with
proper body group G of order60. Put

    a=phi^2, c=2+phi, b=phi^3, R^2=7+8phi=a^2+c^2,
    A0=12+28phi, A1^2=940+1520phi, e=(0,0,1), U=1/20.

A frame B has two orthonormal rows; its oriented normal n is their cross
product, so completing with n gives a proper orthogonal frame. Norms,
widths, areas, translations and scales are physical Euclidean quantities.
Arbitrary proper planar rolls are allowed throughout.

Let W be the prior compact receiving set of all proper G images of
normalized(s,t,1) and normalized(t,s,1), with0<=s<=1/12,|t|<=s/20,
from the [closed wedge classification](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_two_coordinate_wedges/PROOF.md),
sourcec6514c30c565ff0beeebb833cd5c9870f8c67dd7, graph
bafkreigkduxgv3lrhjwq4radhlwyq7mndlqd6apkjzfkspm5auu47x6zcy.
Define P to consist of all proper G images of

    (s,t,1)/sqrt(1+s^2+t^2), (t,s,1)/sqrt(1+s^2+t^2),
    0<=s<=1/20, |t|<=s/2.                                  (1)

These parameters are raw coordinate ratios. Both minor signs, zero tilt,
all triangle boundaries and the Cauchy sign transition are included.
The proper body half-turn Rz=diag(-1,-1,1) supplies opposite major signs.
Set S=W union P; no count of distinct proper-image components is claimed.

**Theorem.** For every receiver B2 with oriented normal in S, every source
B1, physical planar translation T and scale lambda>=1,

    lambda B1K+T subseteq B2K
      iff lambda=1, T=0, B1=sigma B2g,
          for some sigma in {1,-1} and proper g in G.         (2)

Thus every strict standard Rupert passage is excluded at these receivers.
Uniformly rescaling the body, including to unit edge length, preserves
the statement. S strictly extends W: Section9 checks a receiver in P
outside EVERY proper image of W. This is not a full receiving-sphere
cover. In particular, no global non-Rupert theorem is asserted.

The result on W is the pinned premise; below we prove(2) on P. The new
argument crosses a genuine physical Cauchy kink, sharpens the actual
minor-row localization, uses the UNSQUARED sum of two radius constraints
to reject the wrong source branch, and separately confines the y-major
source by area before using its stronger derivative estimate.

## 2. Exact dependencies and their scopes

The [full-source area/width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source2965d5f69373933b5a186976d11867a779b7cf89, graph
bafkreig3ksndxbobnpq2brpxglwkozqo54hz4ykibzp6lpw4cxcn32xwsi,
says that receiving bounds

    A(n2)<=A1+1/4,
    mu(n2)^2<=(20+32phi)*(1-10/11664)                       (3)

properly fold EVERY source in any closed fit of scale>=1 to
n1=z1 e+u1 with z1>0,||u1||<3/25,||n1-e||<1/8. There is no initial
source-nearness, proper-roll or full-angle hypothesis. We verify(3)
anew on P; we do not extrapolate the old receiving sign domain.

Physical original geometry is from the
[brightness certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md),
source58824907716016ff519f2aa5430fef92aa78c62c, graph
bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u.
The filter also inherits the
[fivefold rigidity certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md),
source30c68fadf94ec1c0e891788177a5a5e1a8cc57b5, graph
bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm.
DEPENDENCIES.json pins the four substantive prior W files. Their ENTIRE
9370-byte expected record is replayed, transitively replaying the complete
filter, fivefold and brightness records with every source fingerprint.
All new original facets and physical Cauchy vectors are reconstructed.

We credit the actual-original matching, quadratic equatorial transport
and fixed-row method developed in the
[mirror-arc proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md),
graph bafkreia32nj6ojbdmq2ndloqbxt57h5mzspoe6wko7gwi36dlp4fxfyc3m,
and extended in W, as well as the Cauchy/polar mechanism in the
[J77 proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_area/PROOF.md),
graph bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au.
No differently named solid, local torque theorem or reviewer verdict
supplies a premise for the new P argument.

## 3. The actual Cauchy kink and full receiving bounds

Write j for the major coordinate(x or y), k for the other coordinate,
and n2=(e+s e_j+t e_k)/sqrt(1+s^2+t^2). Its components in directions
j,k,e are X,Y,Z. On P,

    0<=X<=1/20, |Y|<=X/2, |Y|<=1/40,
    Z>99/100, ||n2-e||<1/11.                               (4)

Indeed raw norm squared<=321/320, and the normal chord is bounded by
sqrt(s^2+t^2). The positive-root comparisons are checked exactly.

Physical Cauchy area is A(n)=sum_{q in C}|q.n|, for31 actual paired-facet
area vectors. Six have q_z=0. Their actual list is

    D={(phi-1,+-phi,0), (1+3phi,+-(2+phi),0),
       (4,0,0), (0,4,0)}.

Using |u+v|+|u-v|=2max(|u|,|v|), their contribution at (x,y,z) is

    h_D(x,y)=4|x|+4|y|
      +2max((phi-1)|x|,phi|y|)
      +2max((1+3phi)|x|,(2+phi)|y|).                       (5)

Its positive x-major transitions are |y|/x=2-phi and phi. On(1), the
first is crossed because0<2-phi<1/2<phi. With u=|t|, the x-major
physical coefficients (H,K) in Hs+Ku are

    (4+8phi,4)             when0<=u<=(2-phi)s,
    (6+6phi,4+2phi)        when(2-phi)s<=u<=s/2.            (6)

They coincide at the kink. For the y-major cone, |x|/y<=1/2<phi-1,
so its entire physical formula uses

    (H,K)=(8+4phi,4), in (major=y,minor=x) order.           (7)

The other25 vectors have signed sum A0 e. Each of their affine signs
persists on the ENTIRE triangle(1), checked strictly at its three raw
corners(0,0),(U,U/2),(U,-U/2), separately for both families. Thus,
using the appropriate pair from(6) or(7),

    A(n2)=(A0+Hs+K|t|)/sqrt(1+s^2+t^2)
         =A0 Z+H X+K|Y|.                                  (8)

For each listed pair, both derivative numerators are positive on the
bounding box0<=s<=U,0<=u<=U/2: they are
H(1+u^2)-s(A0+Ku) and K(1+s^2)-u(A0+Hs), bounded below by the
strict checked gates H-U(A0+KU/2)>0 and K-(U/2)(A0+HU)>0.
For the x triangle, increase s to U at fixed u and then u to U/2;
this stays in the triangle, crosses at most its stated kink, and its
continuous piecewise area is increasing. The y formula is increasing
by the same argument. Hence the physical maxima are at the upper
corners. Their exact squared values, respectively x and y, are

    1531972/1605+(803628/535)phi <(1171/20)^2,
    1522384/1605+(800128/535)phi <(581/10)^2.                (9)

The original A1>583/10; since1171/20=583/10+1/4, both receiving
area bounds in(3) follow strictly. No old single-chamber formula is
used above the transition.

For a width bound take eta=sign(t), eta=1 at t=0, and actual perpendicular
directions

    d_x=(phi,-eta,-phi s+|t|), m_x=phi s-|t|,
    d_y=(-eta phi,1,-s+phi|t|), m_y=s-phi|t|.              (10)

Independent coordinate signs in V reduce their support to
h_K(phi,1,-m). For EVERY0<=m<=phi/12 it is3phi^2+phi m:
all sixty original affine inequalities hold at both endpoints, and
the actual original(2phi,phi^2,-phi) attains equality identically.
Squared width is therefore

    w(m)^2=4(3phi^2+phi m)^2/(phi+2+m^2).                 (11)

It increases throughout this support interval by
phi(phi+2)-3phi^2 m>0. On P,0<=m_x<=phi/20 and0<=m_y<=1/20,
because phi>1/2 and1-phi/2>0. The exact maxima of(11) are

    17875684/802001+(23829284/802001)phi,
    17504484/802001+(23661764/802001)phi,

both strictly below the squared width bound in(3). Minimum width is
no larger than these actual widths; the FULL-SOURCE filter applies.

For ANY source with positive z, fixed signed domination of the other25
vectors and(5) give A(n1)>=A0 z+h_D(x,y). Each coefficient pair from
(6) or(7) is a GLOBAL lower linear bound for h_D, obtained by selecting
one term in each maximum in(5). Consequently

    A(n1)>=A0 z+H|x|+K|y|                                (12)

in major/minor order for any relevant target pair. The source need
not lie in the receiving sign chamber. This distinction is essential
at the physical kink.

## 4. Actual-original matching controls the full arbitrary roll

Suppose a closed fit exists on P. Both shadows are centrally symmetric,
so negate and average to remove T, then contract lambda>=1 about zero
to obtain B1K subseteq B2K. Retain the ORIGINAL lambda,T for Section8.
Proper body symmetries independently fold the receiver to(1) and the
source to the positive-z twofold neighborhood given by(3). A common
proper planar gauge makes B2=C_n2, shortest proper transport from
P0=(e_x^t;e_y^t). For n=z e+u,z>0,

    C_n|_{e_perp}=I2-uu^t/(1+z), C_n e=-u,
    ||C_n-P0||=||n-e||,
    ||C_n v-P0v||<=R||n-e||^2/2 for equatorial v.          (13)

The initially arbitrary source has B1=L C_n1,L in SO(2).
The equatorial originals are exactly E={(+-a,+-c,0)}. All other
originals have |v_z|>=1, all coordinates have magnitude<=b<9/2,
and every original has the same squared norm R^2. On our expanded P,
nonequatorial target heights are at least

    Z(1-b(s+|t|))>(99/100)(1-(9/2)(3/40))>3/5.          (14)

Source E squared radii exceed R^2-36/125, using R^2<20 and source
transverse norm<3/25. Target nonequatorial squared radii are below
R^2-9/25. For any x=B1v,v in E, actual support containment supplies
a maximizing target original y=B2v' with x.y>=||x||^2. Thus
||y||>=||x||, excluding v' outside E by(14), and

    ||x-y||^2<=||y||^2-||x||^2<36/125<(11/20)^2.          (15)

Both E projection maps have smallest singular value>24/25. Write
epsilon=11/20. The exact gates

    2a(24/25)>2epsilon,
    2c(24/25)-2a>2epsilon,
    4epsilon(a+c)+4epsilon^2<4ac(24/25)                  (16)

make the close matches unique, injective and hence antipodal; forbid
exchanging the unequal rectangle side types; and forbid reversing its
projected orientation. For the last comparison, each of the two actual
side vectors changes by norm<2epsilon. Expanding their determinant
changes it by less than the left side, while the original positive
projected determinant is at least the right side. Both oriented
equatorial maps have positive determinant. Therefore only identity
or simultaneous sign reversal remains. Absorb the latter by a proper
planar source half-turn. ALL FOUR matches now have actual equal labels:

    (B1v).(B2v)>=||B1v||^2, v in E.                      (17)

One such match and(13), using R>22/5, give

    ||L-I||<(11/20+9/256+9/484)/(22/5),
    ||B1-P0||<1/8+(11/20+9/256+9/484)/(22/5)<4/15.        (18)

Here the two equatorial drift terms use source chord1/8 and receiving
chord1/11. This bounds the full proper row frame, including the
initially arbitrary roll; no near-identity source pose was assumed.

## 5. Bootstrap the ACTUAL minor-row support

Let r1 be the source unit row in minor direction k. By(18), its diagonal
(r1)_k>9/10 and transverse norm q=||(r1)_perp k||<4/15. The actual
target minor row r2 has diagonal1-Y^2/(1+Z), transverse entries
-XY/(1+Z),-Y. By(4), its diagonal>99/100 and its transverse l1 norm
is (1+X/(1+Z))|Y|<(21/20)|Y|<=21/800 (zero exactly if Y=0).

The actual four originals with k-coordinate b have independent +-1
in the other coordinates. Every other original has k-coordinate<=c.
The NEW exact margin

    (b-c)(99/100)-(b-1)(21/800)>0                         (19)

excludes all those other originals from the actual target support.
Thus h_K(r2)=b(r2)_k+|(r2)_j|+|(r2)_z| and
h_K(r2)-b<=(21/20)|Y|. The four actual source originals and support
containment give, without modifying either fitting frame,

    q<=sum_{i!=k}|(r1)_i|
      <=b(1-(r1)_k)+(21/20)|Y|
      =b q^2/(1+(r1)_k)+(21/20)|Y|.                       (20)

Initially bq/(1+(r1)_k)<12/19. Hence, if Y!=0,
q<(399/140)|Y|<3|Y|; if Y=0, the same inequality forces q=0.
For Y!=0, q<3/40. Positivity of(r1)_k and its unit norm then improve
the diagonal to(r1)_k=sqrt(1-q^2)>99/100. Reapplying(20) twice gives

    q<(4179/3305)|Y|<(13/10)|Y|,
    q<(8358/7375)|Y|<(6/5)|Y|.                            (21)

The exact factors are
(21/20)/(1-(9/2)(3/40)/(199/100)) and then
(21/20)/(1-(9/2)(13/400)/(199/100)). All denominators are positive.
Orthogonality n1.r1=0 and projection of e_k onto r1_perp give

    |(n1)_k|<=q<(6/5)|Y|<=3/100 when Y!=0,
    (n1)_k=0 when Y=0.                                    (22)

The enlarged exposed face and both refinement stages were rechecked
for P. No corrected source frame is assumed to satisfy containment.

## 6. Unsquared summed radii select the branch; separate radii give order

Write gamma_x=a,gamma_y=c and rho=gamma_k/gamma_j. Let the source major
and minor components be x,y. If x<0 replace B1 by -B1Rz, using the
proper body half-turn and proper planar half-turn. This preserves the
source shadow and EVERY labeled E projection because Rzv=-v on E.
It changes both transverse normal signs, leaving z positive; it also
preserves the minor row's diagonal and transverse norm. Thus(17),(22)
survive. Take x>=0 henceforth.

The two distinct opposite E pairs in(17), and their common spatial
radius, give SEPARATELY

    |gamma_j x+gamma_k y|>=|gamma_j X+gamma_k Y|,
    |gamma_j x-gamma_k y|>=|gamma_j X-gamma_k Y|.            (23)

For X>0, target dominance gamma_j X>gamma_k|Y| follows from
|Y|<=X/2 and the exact stronger gates gamma_j>(3/5)gamma_k,
checked for BOTH j. If the wrong source branch
gamma_j x<=gamma_k|y| held, the sum of the UNSQUARED left sides
would be2gamma_k|y|, whereas the right sum is2gamma_j X. Hence
gamma_k|y|>=gamma_j X. But(22) implies

    gamma_k|y|<(6/5)gamma_k|Y|
               <=(3/5)gamma_k X<gamma_j X,                (24)

a contradiction. If Y=0 the same contradiction follows from y=0.
Therefore both source linear forms in(23) are positive. Resolve their
absolute values SEPARATELY to obtain

    x>=X+rho|y-Y|.                                         (25)

The sum alone after branch selection would give only x>=X and lose
the indispensable minor-change penalty. If X=0 then Y=0,(22) gives
y=0, and(25) follows directly from x>=0; no division by X is used.

## 7. Global physical area dominates the exact order

For each target coefficient pair define, in major/minor order,

    F_{H,K}(v,w)=A0 sqrt(1-v^2-w^2)+Hv+K|w|.               (26)

By(8),(12), A(n2)=F_{H,K}(X,Y) and A(n1)>=F_{H,K}(x,y), with
the SAME pair chosen from the target chamber. This is valid even when
the source is across another Cauchy sign boundary.

The initial source filter and(22) put both source and target in the
rectangle0<=v<=3/25,|w|<=3/100. The positive square root exceeds24/25
throughout it, so v/root<=1/8. For BOTH x-major pairs the exact gates

    H-A0/8>8,
    K+A0(3/100)/(24/25)<10,
    8(c/a)>10                                             (27)

show that the major derivative exceeds8, the minor Lipschitz constant
is below10, and their radial ratio dominates it. The Lipschitz bound
includes w=0 by joining the bounds on its two sides. Thus, with
rho=c/a and(25),

    F(x,y)-F(X,Y)>=8(x-X)-10|y-Y|
                  >=(8rho-10)|y-Y|.                       (28)

If y!=Y this is positive. If y=Y and x>X the major derivative makes
the difference strictly positive. Closed containment also gives
A(n1)<=A(n2), so x=X and y=Y for the x-major cone, including its kink.

For the y-major cone the initial rectangle is too large for the
desired9-versus6 bound, so first improve its major-source bound.
Here F(v,w)=A0 sqrt(1-v^2-w^2)+(8+4phi)v+4|w|. On the initial
rectangle it is increasing in v and |w|, by the exact gates

    (8+4phi)-A0(3/25)/(24/25)>7,
    4-A0(3/100)/(24/25)>0.                                 (29)

The receiving maximum in(9) is below T0=581/10. Put
C0=T0-(8+4phi)/12; the checker verifies C0>0 and

    A0^2(143/144)>C0^2.                                    (30)

Both sides before squaring are positive, so this gives
F(1/12,0)>T0. If the source major x were>=1/12, global(12) and(29)
would force A(n1)>=F(x,y)>=F(1/12,0)>T0>A(n2), contradicting
containment. Hence x<1/12.

On the improved rectangle0<=v<=1/12,|w|<=3/100 the exact gates are

    (8+4phi)-A0(1/12)/(24/25)>9,
    4+A0(3/100)/(24/25)<6,
    9(a/c)>6.                                             (31)

They yield(28) with9,6,rho=a/c, and force x=X,y=Y identically.
This refinement is an area consequence for ALL sources, not an initial
source restriction. Both source and target have positive z; therefore
n1=n2 exactly in either family, including s=t=0.

## 8. Recover the full frame, original scale and physical translation

With n1=n2, each same-labeled pair in(17) has equal norm. Its support
inequality forces B1v=B2v, since
||B1v-B2v||^2=2||B1v||^2-2(B1v).(B2v)<=0. Two independent E originals
have independent projected images because the equatorial singular value
is positive. Together with the equal oriented normal this gives the
full proper row frames B1=B2. Equivalently, their remaining proper
planar rotation fixes a nonzero projected vector and is identity.

The ORIGINAL containment gives lambda^2 A(n1)<=A(n2)=A(n1)>0, hence
lambda=1. Equal centered shadows and support inequalities in opposite
planar directions give the original physical T=0. Undoing the independent
proper folds, common planar gauge and source half-turns yields exactly
B1=sigma B2g as in(2). Conversely every such sigma,g yields equality
by gK=K=-K at lambda=1,T=0. This proves(2) on P and, with the pinned
result on W, on S=W union P, including all closed boundaries.

## 9. An exact new receiver beyond the old receiving cover

At raw r=(1/20,1/40,1), the x-major seed is above the first actual
transition, since1/2>2-phi. Its physical area uses the second pair
in(6). Independent physical Cauchy and direct projected-original
monotone-hull areas agree exactly, with16 shadow corners and squared
area equal to the x value in(9). The old first-pair raw expression is
strictly smaller, with exact shortfall(2-phi)/20>0. It cannot be used
as the physical receiving area here.

For every proper g, set q=g^t r. Membership in a reference old W wedge
requires q_z>0,0<=q_j<=q_z/12,20|q_k|<=q_j. Both j are checked for
all60 g; there are ZERO memberships. Thus r/||r|| in P is outside
every proper image of old W, and S is a proper extension.

For the entire prior mirror union M, with0<=s<=1/12, maximize the
SIGNED cosine (q_z+s q_j)/sqrt((r.r)(1+s^2)) over every proper g and
both families. Its derivative numerator is q_j-s q_z. Endpoints and
every admissible critical parameter s=q_j/q_z contain all maxima.
Only positive numerators are squared; a negative cosine is not a
nearby normal. The exact maximum positive squared cosine is1604/1605,
at the x-mirror parameter1/20. Comparing with(1-d^2/2)^2 for d=1/50
proves chord distance from the ENTIRE M greater than1/50.

In particular this seed is outside the radius1/2000000
[uniform mirror tube](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_uniform_mirror_arc_tube/PROOF.md),
graph bafkreicrfdsjypd4mpepvaescy3vb4devd2g6gmymwhgwbrxpwqvn3od54.
Separate exact all-proper-image comparisons also place it outside the
specified [twofold1/270 caps](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_quadratic_twofold_caps/PROOF.md),
graph bafkreidiwye4mcfzaickzc4zmrbldyce44awk4f4ndnnlxpxgowilgvpsi,
the fivefold1/1500 caps and the
[endpoint1/15000 caps](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_endpoint_contact_caps/PROOF.md),
graph bafkreibydvv4zcxs6sw73dq42unip64jsintm3hq7yrbvgnammf3yifz2i.
Its minimum original height is below83/200, the threshold of the
[height-band exclusion](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/GLOBAL_BAND_83_PROOF.md),
graph bafkreigd4v6qd4ixwomhrnyjovfz65cd4vy2jyspeqnbvqwkwan45jkb3u.
These are comparisons with specifically named covers, not an exhaustive
enumeration of prior published receiving regions. The entire multipart
uniform tube, which also includes extensions past mirror endpoints,
is not claimed to be contained in S.

## 10. Reproduction, trust boundary and remaining frontier

From the repository root, Python3.11+ standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_cauchy_transition_cones/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_cauchy_transition_cones/check.py
```

Both outputs must byte-match ENTIRE expected.json. All guards use explicit
exceptions and survive optimization. Eight new damaged controls omit a
physical tangent vector, misplace the kink, freeze the old receiving
formula across it, break an original width witness, enlarge the matching
budget, understate a bootstrap factor, invalidate the wrong-branch slope
budget, or apply the y-major9-derivative estimate on the initial larger
source rectangle. Each must reject; the pinned prior controls also replay.

The checker certifies exact finite hypotheses for this complete WRITTEN
geometric argument. Triangle corners certify affine signs, original
endpoint inequalities certify entire affine support intervals, and
explicit derivative/Lipschitz estimates certify all comparison domains.
There is no floating experiment, sampled continuum, solver timeout or
incomplete enumeration used as mathematical nonexistence evidence.
Trust boundary: ordered Fraction/Q(phi) arithmetic and the written
continuum reasoning, unformalized and independently unreviewed.

The primary seeds
[Steininger--Yurkevich, Section9.1](https://arxiv.org/html/2508.18475) and
[Zeng, Section1.2](https://arxiv.org/html/2604.26531), read live2026-10-01
in this pass, retain the RID non-Rupert conjecture as open. No published
theorem is restated as a new global result. A preceding bounded primary
search found no global resolution; it is not an exhaustive priority audit.
The macroscopic receiving complement remains unresolved. A concrete next
step is to analyze the next actual Cauchy transition at x-major ratio phi,
including failure points of the minor-row localization, radius-branch
selection, and global source filter. Existing constants here are not
automatically valid at that larger slope.
