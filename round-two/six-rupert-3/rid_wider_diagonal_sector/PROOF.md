# All-source closed RID rigidity through raw tilt 1/16

**six-rupert-3, researcher; 2026-10-02.** Complete ordinary geometric
intermediate proof with exact finite certificates. Author-checked,
unformalized and independently unreviewed. Global standard
rhombicosidodecahedron Rupertness remains OPEN. No historical priority for
Cayley coordinates, convex support arguments or Bernstein bounds is asserted.

## 1. Solid, receiving domain and full statement

Put phi=(1+sqrt(5))/2 and K=conv(V)=-K. The sixty actual originals V are
the independent sign choices and even coordinate permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2).

This is the standard edge-two rhombicosidodecahedron (RID). Set

    a=phi^2, c=2+phi, b=phi^3, k=c/5=a/c,
    R0^2=a^2+c^2=7+8phi.

Let G be the complete sixty-element proper body group. A projection
frame B has two orthonormal rows. Their cross product is its oriented
unit normal, and adding that normal as the third row gives a proper
three-dimensional frame. Areas, widths, translations and scales below
are physical quantities in these orthonormal planar coordinates.

The reference RAW receiving triangle is

    r=(u,(k+rho)u,1), 0<=u<=1/16, |rho|<=3/10.       (1)

Its vertices are (0,0,1) and (1/16,(k+/-3/10)/16,1). At u=0 every
rho describes the same axial normal. These coordinates are ratios,
not angles or unit-normal chords. Let S16 contain every normalized real
point of(1), every proper G image, and their negatives. ALL boundaries
and the axial endpoint are included.

**Theorem.** For EVERY receiving frame B2 with normal in S16, EVERY
source frame B1, EVERY physical planar vector T and EVERY lambda>=1,

    lambda B1 K+T subseteq B2 K
      iff lambda=1, T=0, B1=sigma B2 g,
          some sigma in{1,-1}, g in G.              (2)

Thus no strict standard Rupert passage uses these receivers. No initial
source-normal, planar-roll or relative-motion restriction is imposed.
The statement is invariant under common rescaling of the solid.

S16 contains the ENTIRE previously proved closed sector u<=1/25 and the
ENTIRE old small diagonal box, together with all their signed proper
images. Section9 gives a receiver in S16 outside every such image and
outside the previously proved W/P union. We do not claim that S16
contains every older receiving set, covers the receiving sphere, or
establishes global non-Rupertness.

The proper strict-projection definition is the one in
[Zeng, Section1.1](https://arxiv.org/html/2604.26531#S1.SS1).
That paper's Section1.2 still lists RID non-Rupertness as an open
conjecture. The named originals and their degenerate projections appear
in [Steininger--Yurkevich, Section9.1](https://arxiv.org/html/2508.18475#S9.SS1).
Both current primary sources and pertinent campaign publications were
inspected. This intermediate theorem is not presented as a resolution
of that published conjecture.

## 2. Prerequisites and uniform quadratic control

The direct prerequisite is the published
[all-source area/width filter](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md),
source2965d5f69373933b5a186976d11867a779b7cf89. It says that a
hypothetical closed fit with receiver area<=A1+1/4 and minimum squared
width<=Mwidth, where

    A1^2=940+1520phi,
    Mwidth=(20+32phi)*(1-10/11664),

has EVERY source normal, after a proper body fold, in positive z with
transverse norm<3/25 and axial chord<1/8. Its prerequisites are the
[original brightness/facet reconstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md)
and [fivefold geometry](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md).
The checker replays the COMPLETE filter, fivefold and brightness records
and verifies all twelve transitive source fingerprints before importing
the ordered arithmetic. The filter is invoked only after fresh gates on
the ENTIRE larger receiving triangle have been proved in section3.

The immediate precursor is the
[u<=1/25 parametric-sector theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_diagonal_sector/PROOF.md),
source9c90c51188e7c3beaffc7bc2a8db705aca7dcae3, committed LEMMA9231.
It provides the matching, actual-row and contact mechanisms. The
current proof replaces the discarded area normalization, loose weighted
radius estimates and scalar closure by fresh bounds on(1). Its checker
rebuilds the original geometry and contact polynomials; it does not
assume that the precursor's constants transfer to a larger domain.

Actual-original matching and transported rows also build on the
[W proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_two_coordinate_wedges/PROOF.md),
[arc proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_mirror_arc_rigidity/PROOF.md),
[P proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_cauchy_transition_cones/PROOF.md)
and [old diagonal-box proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_diagonal_contact_patch/PROOF.md).
Their exact receiving domains remain distinct. The independently
checked [Gram example](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_pair_gram_relaxation/PROOF.md)
illustrates why necessary relaxations alone do not establish actual
containment; its [fixed-plane review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-gram-audit/REVIEW.md)
is not an all-source covering result.

Independent [contact-box REVIEW9213](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-contact-audit/REVIEW.md),
source dcab539117295c67edfdfaf36db476ee6b8114cf, confirms the ENTIRE
old small-box theorem at its inherited filter. Its full source and
committed body were read. It independently reconstructs contacts,
exact dual coercivity, clipped motion polytope and the source bridge,
and obtains a physical support-error bound on that SAME old box.
Neither that verdict nor its constants certify the current enlarged
domain. The present theorem is independently unreviewed.

Fresh reconstruction checks all34220 triples of the sixty originals,
all62 facets and31 physical Cauchy area vectors. Each actual normalized
facet normal m has equation m.x<=1 and ||m||^2<1/16. Completeness
therefore puts the closed ball of radius4 in the INTERIOR of K. Hence
EVERY actual normalized support vector mhat with h_K(mhat)=1 satisfies
||mhat||<1/4. Each original has norm R0<9/2.

For an actual contact mhat.v=1, write the product of the projections
of mhat and v along q as the difference of two squares for their
normalized sum and difference. Cauchy's inequality gives

    (mhat.q)(v.q)-q.q
       >=-(1+||mhat||||v||)*||q||^2/2
       >=-(17/16)||q||^2.                            (3)

Thus C=17/16 is valid uniformly for EVERY actual contact below.
This global geometric estimate does not interpolate support-normal
squared norms or sample their values.

## 3. Physical-area envelope, width, complete edges and heights

Let C31 be the freshly reconstructed31 Cauchy area vectors and
Araw(r)=sum_{h in C31}|h.r|. Put

    A0=12+28phi, D0=8+8phi, D1=4+2phi,
    alpha=D0-D1*k=6+6phi, U=1/16, delta=3/10.

At ALL three triangle vertices the fresh Cauchy sums are exactly

    Araw(r)=A0+alpha*r_x+D1*r_y.

Convexity and barycentric interpolation therefore give, throughout(1),

    Araw(r)<=A0+u(D0+D1*rho).

The physical area is Araw(r)/||r||. Writing t=k+rho, it is at most

    F(u,t)=[A0+u(alpha+D1*t)]/sqrt(1+(1+t^2)u^2).     (4)

This normalization matters: the upper tip RAW area exceeds1171/20,
while its normalized physical area is strictly less than1171/20.
No invalid bound on the raw area is substituted for the physical one.

For fixed t, the numerator determining the sign of dF/du is

    alpha+D1*t-A0(1+t^2)u.

Its lower bound D0-D1*delta-A0(1+(k+delta)^2)U is positive, as checked
in the ordered field. Thus F increases in u. At u=U, the numerator
determining the sign of dF/dt is

    D1(1+U^2)-A0*t*U-alpha*t*U^2.

It is positive at t=k+delta and hence throughout the slope interval,
since A0,alpha,t are positive. The maximum of(4) is the upper tip.
The checker proves the EXACT positive-root comparison

    [A0+(D0+D1*delta)U]^2
       <(1171/20)^2*[1+(1+(k+delta)^2)U^2].           (5)

All terms being positive, physical receiver area<1171/20. Also
A1>583/10 by a squared ordered-field comparison. Consequently physical
receiver area<A1+1/4 on the WHOLE triangle, including the axis.

Set m=phi*r_x-r_y and d=(phi,-1,-m). Then d.r=0 and
0<=m<phi/12 throughout(1). Against ALL sixty originals, affine
endpoint checks at m=0 and phi/12 prove h_K(d)=3phi^2+phi*m.
The SAME actual original (2phi,-a,-phi) attains both endpoints, hence
the entire affine interval. The squared physical directional width is

    4(3phi^2+phi*m)^2/(phi+2+m^2).

It increases throughout the interval because
phi*(phi+2)-3phi^2*m>0. Its endpoint value is<Mwidth. Minimum width
is no larger, so the direct all-source filter applies everywhere in(1).

The center u=1/16,rho=0 has complete shadow cycle

    48,36,54,56,38,53,46,18,11,23,5,3,21,6,13,41.     (6)

Indices use the pinned original coefficient-key ordering. A monotone
hull of ALL sixty projected originals reconstructs this complete cycle.
For each directed edge i->j put

    m_i(r)=(Vj-Vi) cross r, h_i(r)=m_i(r).Vi.

At the axis and BOTH outer tips, fresh exact checks give h_i>0,
both incident endpoint equalities, and h_i-m_i.Vl>=0 for EVERY other
original. Offendpoint inequalities are strict at both tips. All these
expressions are affine in r. Any point of(1) is a convex combination
of its three vertices, with positive total tip weight if u>0. The
sixteen edges are therefore genuine complete-shadow edges for EVERY
u>0. They remain actual supports at the axis, where more originals
can tie. There are2880 corner original comparisons,96 literal
endpoint equalities and1856 strict offendpoint tip comparisons.

Write n2=(X,Y,Z)=r/||r|| and N=36/25. Exact field and squared-root
gates give for u>0

    X,Y>0, ||(X,Y)||<N*u, X,Y<319/5000,
    Z>199/200, ||n2-e_z||<1/11, ||r||<101/100.         (7)

For the Y bound, the physical function
t*u/sqrt(1+(1+t^2)u^2) is increasing in u and t>0; its endpoint
square is checked against (319/5000)^2. For X, simply X<=u<=1/16
<319/5000. The normal chord gate follows from
1+(NU)^2<(242/241)^2, equivalent to Z>241/242. These are whole-domain
bounds, not inequalities only at a sampled center.

The only originals with v_z=0 are E={(+/-a,+/-c,0)}. Every other
original has |v_z|>=1. For EACH of these56 originals, at ALL three
triangle vertices the affine signed height
sign(v_z)*(v.r) is>13/20. These168 fresh comparisons extend over the
ENTIRE triangle by affine interpolation, with the sign fixed by v_z.
Dividing by the whole-domain normalization<101/100 gives

    |v.n2|>(13/20)/(101/100)>3/5, v outside E.        (8)

This uses actual nonequatorial heights and remains valid at the larger
tilt. A coarser coordinate-sum estimate is not assumed to transfer.

## 4. Every source, actual matching and both transported rows

For a closed fit, central symmetry removes T by negating and averaging:
lambda B1K subseteq B2K. Contract lambda>=1 toward zero to obtain
B1K subseteq B2K, retaining the ORIGINAL lambda,T for final recovery.
Properly fold the source with the established filter. Its normal is
n1=(x,y,z), z>0, ||(x,y)||<3/25 and ||n1-e_z||<1/8.
A common proper planar gauge sets B2=C_n2, with B1=L C_n1 and arbitrary
L in SO(2). Here, for t=(x,y),

    Q_n=[[I2-t*t^t/(1+z), -t], [t^t,z]],             (9)

and C_n consists of its first two rows. Direct multiplication gives
Q_n proper orthogonal, its third row n^t, and
||C_n-P0||op=||n-e_z||, P0=(e_x^t;e_y^t). For equatorial v,

    ||(C_n-P0)v||<=R0*||n-e_z||^2/2.

Source E projected squared radii exceed R0^2-36/125 by the filter.
Receiving nonequatorial squared radii are<R0^2-9/25 by(8). For a
source projected E point p, actual containment gives a target original
q with p.q>=||p||^2. The radius separation forces q to come from E.
Furthermore ||p-q||^2<36/125<(11/20)^2. Both equatorial projection
maps have smallest singular value>sigma=24/25.

With e0=11/20, exact gates give

    2a*sigma>2e0,
    2c*sigma-2a>2e0,
    4e0*(a+c)+4e0^2<4ac*sigma.                       (10)

The first gate forces injective close matching; antipodality then gives
a bijection. The second preserves the unequal rectangle side types.
The third preserves proper orientation: perturb each of two adjacent
target sides by<2e0, so their determinant changes by less than its left
side, smaller than the positive target determinant. The only remaining
label maps are identity and simultaneous sign reversal. A proper planar
source half-turn absorbs the latter. Consequently EVERY actual E label
satisfies

    (B1v).(B2v)>=||B1v||^2, v in E.                 (11)

One match, R0>22/5 and the equatorial quadratic drifts imply

    ||B1-P0||op
      <1/8+(11/20+9/256+9/484)/(22/5)<4/15.          (12)

Indeed a planar rotation difference has constant norm on unit vectors;
one matched equatorial v bounds ||L-I|| by its matched-point error plus
the two quadratic drifts, divided by R0. Adding ||C_n1-P0|| gives(12).
This derives a full-frame enclosure for the initially arbitrary source
roll. It remains valid at u=0.

For j=x or y, with the other transverse coordinate indexed k', the
ACTUAL receiving row of(9) has diagonal>199/200 and transverse l1 norm

    |(n2)_j|*(1+|(n2)_k'|/(1+Z))
       <(129/125)*|(n2)_j|.                          (13)

Exactly four ACTUAL originals have j coordinate b, with independent
other coordinates +/-1. Every other original has j coordinate<=c.
The checked comparison

    (b-c)*(199/200)-(b-1)*(129/125)*(319/5000)>0      (14)

therefore proves those four form the actual receiving support face.
In particular its support minus b is<=(129/125)|(n2)_j|.

Let d1_j be the corresponding ACTUAL source unit row and
tau=||(d1_j)_{perp j}||. Equation(12) gives tau<4/15 and diagonal>9/10.
The SAME four actual source originals and support containment yield

    tau<=b*tau^2/(1+(d1_j)_j)+(129/125)|(n2)_j|.      (15)

The first rearrangement uses b<9/2, tau<4/15, diagonal>9/10, giving
tau<3|(n2)_j| when u>0. The remaining finite bootstrap uses
b<106/25 and the receiving coordinate bound319/5000. Each row in this
table inserts the preceding factor, obtains a positive diagonal lower
bound by squaring, and rearranges(15):

| Preceding factor | Diagonal lower | Derived factor | Next upper |
|---|---|---|---|
| 3 | 49/50 | 3870/2213 | 7/4 |
| 7/4 | 99/100 | 513420/379151 | 11/8 |
| 11/8 | 199/200 | 1029420/811523 | 51/40 |
| 51/40 | 249/250 | 5149680/4127743 | 5/4 |
| 5/4 | 249/250 | 171656/138155 | 249/200 |

All denominators are positive and all strict comparisons are checked.
Orthogonality of the ACTUAL normal to each ACTUAL row implies
|(n1)_j|<=tau: the projection of e_j onto that row's perpendicular
space has norm tau. Thus, putting f=249/200,

    |x|<f X, |y|<f Y.                               (16)

At u=0, both receiving coordinates are zero. The positive coefficient
1-b*tau/(1+(d1_j)_j) in(15) forces tau=0 for BOTH rows. Their
diagonals are positive, so d1_x=e_x,d1_y=e_y and B1=B2=P0 in the folded
gauge. This proves the axial endpoint before ANY division by u.

## 5. Weighted coordinate errors and actual planar roll

Now u>0. The raw slope interval gives

    4/7<cY/(aX)<7/4,
    |aX-cY|<c*delta*u, delta=3/10.                   (17)

The first comparison follows by checking the two field endpoints; the
second uses ck=a and ||r||>=1. From(11), same-label source E radii
cannot exceed the target ones. For v+=(a,c,0), this gives
|ax+cy|>=aX+cY. If needed replace B1 by -B1 Rz, with the proper body
half-turn Rz=diag(-1,-1,1). It preserves the whole shadow, EVERY labelled
E image, the actual row norms and(12), and reverses x,y while keeping
z positive. We may therefore take

    ax+cy>=aX+cY.

Both x,y are positive. For example x<=0 and(16) would give
ax+cy<f cY, while(17) gives aX+cY>(1+4/7)cY, contradicting
f<1+4/7. The other case is symmetric.

Let epsilon=f-1=49/200. The sum order and the two individual upper
bounds then imply

    |x-X|<=epsilon*max(X,cY/a),
    |y-Y|<=epsilon*max(Y,aX/c).                      (18)

For example x-X<epsilon X follows from(16), while
x-X>=-epsilon*cY/a follows by subtracting the upper bound cy<f cY
from the sum order. The y argument is identical.

These two weighted maxima must be kept together. If Y<=kX their
vector is (X,kX); if Y>=kX it is (Y/k,Y). Since X<=u and Y/X<=k+delta,
its norm is at most

    (1+c*delta/a)*sqrt(1+k^2)*u <(7/4)u,             (19)

where the strict last comparison is checked after squaring in Q(phi).
Putting t1=(x,y),t2=(X,Y), we obtain the fresh direct VECTOR bound

    ||t1-t2||<d*u, d=epsilon*(7/4)=343/800,
    ||t_i||<T0=23/200, z_i>99/100.                  (20)

Indeed ||t1||<f N U=2241/20000<T0, and ||t2||<NU<T0.

For v-=(a,-c,0), the weighted errors also give

    |a(x-X)-c(y-Y)|
       <=2epsilon*max(aX,cY)
       <=2epsilon*(a+c*delta)*u.

Combining with(17), the checker proves

    |n1.v-|<[c*delta+2epsilon*(a+c*delta)]u<3u,
    ||C_n2 v-||>22/5.                               (21)

The first field coefficient is173/125+(937/1000)phi. The second follows
from R0^2-(c*delta*U)^2>(22/5)^2, checked with the stronger rational
upper c*delta<9/8. Equation(11) gives the actual matched-point bound

    ||B1v--B2v-||^2
       <=||B2v-||^2-||B1v-||^2
       =(n1.v-)^2-(n2.v-)^2 <9u^2.                  (22)

Write A_i=I-t_i t_i^t/(1+z_i). Subtracting the unit-norm equations
and outer products, using T0 and zmin=99/100, yields

    |z1-z2|<=[T0/zmin]||t1-t2||,
    ||A1-A2||F<=[2T0/(1+zmin)
        +T0^2*(T0/zmin)/(1+zmin)^2]||t1-t2||.

Both bracketed coefficients are<3/25; the latter is
3637151/31363992. Differences of proper three-by-three rotations
have two equal nonzero singular values. The Frobenius norm of the
block difference in(9) therefore gives

    ||Q_n1-Q_n2||op<(101/100)||t1-t2||,              (23)

using 1+(3/25)^2<(101/100)^2.

The arbitrary proper planar L satisfies the actual identity

    (L-I)C_n2v-=(B1-B2)v-+L(C_n2-C_n1)v-.

A proper planar rotation difference has constant norm on unit vectors.
Only A1-A2 enters the second term because v- is equatorial. Equations
(20)-(23), R0<9/2 and the lower projected radius in(21) therefore imply

    ||L-I||op
      <[3+(9/2)*(343/800)*(3/25)]u/(22/5)
      =(11751/16000)u <(3/4)u.                      (24)

This bound derives the initially arbitrary roll from actual containment.
Neither an imposed near-roll assumption nor a necessary relaxation is
substituted for a fit.

## 6. The full relative rotation is derived in a Cayley chart

For a proper rotation R, use its ordinary Cayley vector q:

    R(q)=I+2([q]_cross+[q]_cross^2)/(1+q.q).

When ||R-I||op<2 this chart exists uniquely and
||q||=||R-I||op/sqrt(4-||R-I||op^2). If theta is the representative
angle of L in(-pi,pi), let beta=tan(theta/2). Equation(24) gives the
fresh positive-root comparison

    |beta|<(47/125)u.                                (25)

Let H=Q_n2^t Q_n1 and h its Cayley vector. Equations(20),(23), with the
same exact positive-root identity, yield

    ||h||<(109/500)u.                                (26)

Explicitly Q_n has Cayley vector s_n=(y,-x,0)/(1+z). Consequently

    h=(s1-s2-s2 cross s1)/(1+s2.s1).                 (27)

The denominator is>249/250 because ||s_i||<T0/(199/100).
Subtracting s1,s2 gives

    ||s1-s2||<=J||t1-t2||,
    J=1/(199/100)+T0*(T0/(99/100))/(199/100)^2.

The s_i are equatorial. Using ||s2||<N*u/(199/100), the cross-product
term in(27) is therefore the sole axial term and proves

    |h_z|<[(N/(199/100))*J*(343/800)/(249/250)]u^2
          =(3401402375/21584960661)u^2<(17/100)u^2.  (28)

Complete the actual source frame as diag(L,1)Q_n1. Its proper relative
rotation is R=Q_n2^t diag(L,1)Q_n1, satisfying C_n2 R=B1. Factor it
as the rotation with Cayley vector beta*n2 followed by H. Exact Cayley
composition gives

    q=(h+beta*n2+beta*n2 cross h)/(1-beta*n2.h).      (29)

The denominator is>999/1000 by(25)-(26) and u<=U. Thus(29) is the
finite Cayley vector of the ACTUAL full relative rotation, with no
initial relative-chart restriction. Using(7),(25)-(28), we get

    ||(qx,qy)||
       <[(109/500)+((47/125)*N+(47/125)*(109/500))U]
            /(999/1000)*u
       =(256963/999000)u<(13/50)u,

    |qz|
       <[(47/125)+((17/100)+(47/125)*(109/500))U]
            /(999/1000)*u
       =(97937/249750)u<(2/5)u.                     (30)

The first line is a VECTOR norm bound. Thus

    ||q||^2<[(13/50)^2+(2/5)^2]u^2
             =(569/2500)u^2.                       (31)

All positive-root, rearrangement and rational coefficient gates in this
section are checked exactly. No floating-point search is used.

## 7. Six parametric actual-contact duals

For either ORIGINAL endpoint v of an actual edge(6), let
mhat_i=m_i/h_i and f_i=v cross mhat_i. The vector mhat_i is in the
receiving plane and h_K(mhat_i)=mhat_i.v=1. Since C_n2 R=B1, projected
support containment gives mhat_i.R(q)v<=1. Multiplication by the positive
factor(1+q.q)/2 produces the EXACT actual constraint

    f_i.q+(mhat_i.q)(v.q)-q.q<=0.                    (32)

Together with(3), every fitted q satisfies
f_i.q<=C||q||^2, C=17/16, for ALL32 actual endpoint constraints.

The checker builds six three-contact rational positive dual families on
the WHOLE CLOSED rectangle0<=u<=1/16, |rho|<=3/10. Traverse(6), taking
the first then the second endpoint at each edge, to index the32 contacts:

| Coordinate | Sign | Actual contact indices |
|---|---|---|
| x | - | 1,9,10 |
| x | + | 8,12,13 |
| y | - | 2,7,8 |
| y | + | 9,10,14 |
| z | - | 3,9,13 |
| z | + | 0,1,10 |

For a selected triple form RAW polynomial vectors F_i=v_i cross m_i
and D=det(F0,F1,F2) in Q(phi)[u,rho]. For t=+/-u e_j, the Cramer
numerators eta_i=t.(F_{i+1} cross F_{i+2}) satisfy the literal polynomial
identity sum eta_i F_i=D t. Actual normalized weights are
w_i=h_i eta_i/D. A common monomial u^d cancels from D and all h_i eta_i;
d is respectively1,0,1,1,0,1 in the table. A common sign orients the
canceled denominator positively.

Let Dbar be the signed canceled denominator and N_i the signed canceled
weight numerators. The full compact expected record gives their exact
coefficients and all tensor-Bernstein coefficient bounds. Fresh
certificates on the larger rectangle prove

    Dbar>0, N_i>=0, (3/2)Dbar-sum N_i>=0.            (33)

For BOTH z families each N_i has a further factor u. Write N_i=u M_i.
The checker also proves M_i>=0 and4Dbar-sum M_i>=0 throughout the
larger rectangle. For u>0 these are actual nonnegative dual weights:

    sum w_i f_i=+/-u e_j, sum w_i<=3/2, j=x,y,z;
    sum mu_i f_i=+/-e_z,  sum mu_i<=4.               (34)

No uncanceled pole remains for u>0. Polynomial bounds include the axis,
but its geometry was proved separately in section4 before division by u.

The continuum sign argument is elementary and exact. Map the rectangle
affinely to0<=s,t<=1 and write P=sum a_ij s^i t^j, of degrees m,n.
Its tensor-Bernstein coefficients are

    B_kl=sum_{i<=k,j<=l} a_ij
             binom(k,i)/binom(m,i)
             binom(l,j)/binom(n,j).

Then P is the sum of B_kl times
binom(m,k)s^k(1-s)^(m-k) binom(n,l)t^l(1-t)^(n-l). These basis functions
are nonnegative and sum to one. Their coefficient minimum and maximum
therefore enclose P on the ENTIRE real rectangle. The code independently
re-expands every Bernstein expression into ordinary powers and verifies
this identity exactly. All Cramer vector identities are checked before
monomial cancellation. No sample sign, approximate LP or incomplete
enumeration is treated as a proof.

## 8. Vector tilt and unscaled roll close every nonzero fit

Apply the two unscaled roll families(34) to(32) and use(31):

    |qz|<=4C||q||^2<(4C)*(569/2500)u^2
                          <=(9673/160000)u.         (35)

Set Q=||q||infinity. The six scaled families give
u Q<=(3/2)C||q||^2. Meanwhile the elementary l1 inequality, with the
VECTOR estimate in(30), gives

    ||q||^2<=Q*(|qx|+|qy|+|qz|)
             <=Q*(sqrt(2)||(qx,qy)||+|qz|)
             <Q*[(71/50)*(13/50)+9673/160000]u,

since (71/50)^2>2. If q is nonzero, divide by Q>0 and combine:

    u<[(3/2)*(17/16)*((71/50)*(13/50)+9673/160000)]u
       =(701199/1024000)u<u.                        (36)

This contradiction proves q=0 for EVERY hypothetical fitted source
at EVERY u>0 in(1). The axial case was proved separately. It completes
the all-source bridge, including the initially arbitrary proper roll.

More generally, the reusable sufficient criterion is as follows. Suppose
actual contact duals imply

    u||q||infinity<=A C||q||^2,
    |qz|<=B C||q||^2,

and actual all-source geometry implies the VECTOR bound
||qxy||<a0 u and |qz|<b0 u for0<u<=U0. If

    A C[sqrt(2)*a0+B C(a0^2+b0^2)U0]<1,             (37)

no nonzero fitted q exists. Indeed the initial norm bound gives
|qz|<B C(a0^2+b0^2)U0 u, and the same l1 inequality and division
prove the contradiction. A rational upper for sqrt(2) suffices.
Criterion(37) still REQUIRES the all-source geometric hypotheses;
it does not turn an assumed local Cayley tube into a global theorem.

## 9. Original scale and translation, proper images and strict enlargement

Now R=I, so the completed source and receiver frames coincide in the
folded gauge. Undoing the proper body folds, source planar half-turn and
-B1Rz replacement if used gives B1=sigma B2g with g proper and
sigma in{1,-1}. The ORIGINAL area inequality lambda^2 A(n1)<=A(n2),
with equal positive areas, forces lambda=1. Equal centered shadows in
the ORIGINAL translated inclusion force T=0: in opposite support
directions both scalar products with T must vanish. Conversely the
stated poses give equality since gK=K=-K. This proves(2) on(1).

A proper receiving G image reduces by a common body fold. Negative
oriented normals describe the same receiving plane; a common planar
reflection of BOTH frames changes their oriented normals and preserves
containment, lambda,T and proper completability of each two-row frame.
Undoing it gives the same equality classification. No improper placement
of a single solid is introduced. Therefore(2) holds on ALL of S16.

The entire precursor u<=1/25 sector is contained because1/25<1/16
with the identical closed slope band. The prior raw small box is

    99/2500<=r_x<=101/2500,
    (39+20phi)/2500<=r_y<=(41+20phi)/2500, r_z=1.

At ALL four corners the checker proves strictly0<r_x<1/16 and
(k-delta)r_x<r_y<(k+delta)r_x. These are affine inequalities, hence hold
over the WHOLE rectangle. Proper images and negatives preserve this
containment. Thus this theorem strengthens BOTH exact predecessor
receiving domains, without borrowing an independent verdict on S16.

An explicit newly excluded receiver is

    r_new=(3/50,(3/50)k,1), u=3/50,rho=0.            (38)

For ALL sixty proper maps and both signs, the checker applies the
inverse proper map and verifies an affine homogeneous membership
requirement of the old u<=1/25 triangle is violated. These120 exact
cases prove(38) lies outside EVERY signed proper image of that sector.
Another120 cases exclude the old small box, and480 cases exclude
W (0<=s<=1/12, |t|<=s/20) and P (0<=s<=1/20, |t|<=s/2) in BOTH
coordinate families and all signed proper images. The deterministic
inventories are fully checked, with digests in expected.json. Membership
is tested with homogeneous affine inequalities, never approximate
normalized distances. The whole new domain is not claimed disjoint
from older covers or to contain every older cover.

## 10. Proof status, reproduction and remaining frontier

This is a complete ordinary geometric intermediate proof with exact
finite hypotheses reconstructed by standard-library code. Facet
completeness, Cauchy area, convex interpolation, derivative signs,
proper-frame identities, matching, actual rows, weighted radii, Cayley
composition and the Bernstein-dual argument are the unformalized trust
boundary. Source publication and matching normal/optimized runs do not
constitute an independent mathematical review.

The eight damaged mathematical controls reject understated dual mass,
unscaled roll mass1, negative denominators, an unjustified Ball5,
unsupported source-row factor11/10, a tilt-vector bound1/2 that fails
closure, discarded physical-area normalization, and an unjustified
weighted-vector coefficient6/5. They run unchanged under optimization.
No solver, resource-limit event or failed passage search is interpreted
as mathematical nonexistence.

The new domain is S16 alone. Current and older certified receiving sets
leave an uncertified complement on the receiving sphere. Larger raw
tilt, slope outside the band, and high-area receiving phases still
require a new source localization and/or sharper actual geometry.
Uniform local strict-angle obstructions and fixed-plane Gram results
do not close that complement. A useful next step is to split the outer
receiving band along its actual physical-area boundary and rebuild
source/contact estimates on each remaining closed phase sector. No
global non-Rupert or exact passage certificate is supplied here.
