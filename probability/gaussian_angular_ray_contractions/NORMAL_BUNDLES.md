# Direction-dependent contractions of convex normal bundles

Complete author proof, 27 September 2026. Independent correctness and
historical-priority review are pending. The unrestricted R3 Gaussian
majorisation problem remains open.

This extends the [homogeneous angular theorem](PROOF.md) from one origin
to an arbitrary closed convex core. The resulting map need not be
homogeneous about any point: its base point is the metric projection onto
the core. The new class allows different factors in different normal
directions, with all ball radii and all measure weights unrestricted.
The earlier [common normal-profile theorem](../gaussian_radial_contractions/CONVEX_CORES.md)
supplies the geometric distance decomposition used here; it does not allow
this directional variation. Both predecessor sources are credited.

## 1. Exact class and characterization

Let n>=2 and let C be a nonempty closed convex subset of R^n. Write N_C
for its unit outward normal bundle:

    N_C = {(p,u): p in C, |u|=1, u.(z-p)<=0 for every z in C}.

Choose a Borel subfamily E of N_C, and let

    D = C union {p+r u: (p,u) in E, r>0}.                 (1)

In particular E=N_C gives D=R^n. For x outside C its displayed
representation is unique: p=P_C(x), r=dist(x,C), u=(x-p)/r.
The inverse coordinates are continuous outside C, so D is Borel.

Consider maps fixing C and affine on every selected full normal ray:

    T(p+r u)=p+r a(p,u)u,     a(p,u)>=0, r>0;
    T(x)=x for x in C.                                   (2)

**Theorem.** Such a map is nonexpansive on D if and only if all its
factors lie in [0,1] and, for every (p,u),(q,v) in E, writing
a=a(p,u), b=a(q,v), c=u.v,

    c(1-a b)<=sqrt((1-a^2)(1-b^2)).                       (3)

In particular the factor must be the same on parallel normal rays; it
depends only on u wherever that direction occurs in E.

Every map satisfying these equivalent conditions admits a simultaneous
continuous contracting motion in R^(n+1), with two analytic pieces for
each trajectory and endpoints (x,0) and (Tx,0). Therefore, for every
bounded Borel probability mu on D, every s>0 and every h>=0,

    integral (mu*gamma_(n,s)-h)_+
      <= integral ((T#mu)*gamma_(n,s)-h)_+.                (4)

For any finite labeled list x_i in D and arbitrary individual radii R_i>=0,

    vol_n union_i B(Tx_i,R_i) <= vol_n union_i B(x_i,R_i),
    vol_n intersection_i B(Tx_i,R_i)
       >= vol_n intersection_i B(x_i,R_i).                (5)

No atom-count, weight, angular symmetry, variance, boundedness of C, or
regularity of its boundary is required. C may have empty interior or be
unbounded. If C=R^n, the statement reduces to the identity map.

The **whole-ray** condition is essential to the characterization: testing
only a finite set of selected centers can allow additional factors. The
conclusions also survive restrictions, finite compositions and separate
endpoint Euclidean isometries. Taking E=N_C gives a global map for the
named Gaussian-convolution question.

## 2. Necessity: offsets disappear at large normal distance

If T is nonexpansive, comparing p+r u with the fixed point p gives
0<=a(p,u)<=1. Fix two normal rays and any r,s>0. Apply nonexpansiveness
to p+Lr u and q+Ls v, divide the squared-distance loss by L^2, and let
L increase without bound. The limit is

    (1-a^2)r^2+(1-b^2)s^2-2c(1-a b)r s >=0.              (6)

Nonnegativity of this quadratic for all r,s>=0 is exactly (3), as in the
point-core proof. This handles zero coefficients as well. For u=v, (3)
and squaring its nonnegative sides give (a-b)^2<=0; hence a=b.

Thus base-point variation of factors on parallel rays is not an additional
free parameter. The geometry of the core cannot compensate for a violation
of (3) on arbitrarily long rays, though it can do so at a finite sample.

## 3. Lifting the angular motion over the core

For 0<=theta<=pi/2, tau=cos(theta), put

    A_theta(a)=(a+tau)/(1+a tau),
    B_theta(a)=sqrt(1-a^2)sin(theta)/(1+a tau).

For x=p+r u outside C define

    F_theta(x)=(p+r A_theta(a)u, r B_theta(a));            (7)

keep x in C at (x,0). The functions A_theta are nonnegative and
nonincreasing in theta:

    dA_theta(a)/dtheta=-(1-a^2)sin(theta)/(1+a cos(theta))^2.

For y=q+s v put

    d=p-q,    eta=d.u>=0,    zeta=-d.v>=0.                (8)

Both signs follow from the metric-projection inequalities, including
singular boundary points. If one point lies in C, set its r=0 and u=0;
the remaining sign is still valid. Direct expansion gives

    |F_theta(x)-F_theta(y)|^2
      =|d|^2+2r A_theta(a)eta+2s A_theta(b)zeta
         +|(r A_theta(a)u,r B_theta(a))
                     -(s A_theta(b)v,s B_theta(b))|^2.    (9)

The last term is exactly the point-core angular motion, whose distances
are nonincreasing under (3). The other nonconstant terms decrease because
their coefficients eta,zeta are nonnegative. This proves simultaneous
contraction for all selected rays and all points of C. It is the accepted
convex normal-bundle decomposition applied to the new angular motion,
not an assertion that arbitrary nonexpansive maps can be added to P_C.

At theta=pi/2 the point is (Tx,r sqrt(1-a^2)). Follow it by

    G_t(x)=(Tx,(1-t)r sqrt(1-a^2)),   0<=t<=1.             (10)

Every pair distance is the target squared distance plus the nonincreasing
term (1-t)^2[r sqrt(1-a^2)-s sqrt(1-b^2)]^2. Thus (7),(10) form the
claimed motion, and also prove the sufficiency of (3).

The factor is continuous in direction: (6) at r=s=1 proves that the
homogeneous direction map u->a(u)u is nonexpansive, so a(u) is continuous
on the set of directions occurring in E. Together with continuity of P_C,
this proves joint continuity of (7),(10) away from C. At C, both the
normal displacement and the extra coordinate are bounded by r and tend
to zero. On a bounded support, choose z in C; then r<=|x-z| bounds all
time derivatives, and |P_C(x)-z|<=|x-z| bounds the base points.
Each trajectory has two analytic pieces. No smooth normal field is used.

## 4. The two established transfers

Pad by a zero coordinate to R^(n+2). Aishwarya--Li Theorem1.4(i)(a)
compares sampled density values at the two endpoint Gaussian convolutions.
For any density f, X~f and independent Z~gamma_(2,s),

    Pr[f(X)gamma_(2,s)(Z)>h(2pi s)^(-1)]
       =integral(f-h)_+,

because |Z|^2/(2s) is exponential of mean one. This gives (4), including
bounded diffuse input laws. It is the same credited cancellation as in
PROOF.md, not a new pressure or marginalization theorem.

Reverse the piecewise-analytic motion and use Bezdek--Connelly Theorem1
for (5). Collisions can be removed by a_epsilon=(1-epsilon)a+epsilon.
The regularized map is (1-epsilon)T+epsilon I and remains nonexpansive.
Its positive normal factors keep every non-core point outside C with
the same projection and direction. Hence the target and both motion
stages are injective on distinct source labels. Apply the theorem and
let epsilon decrease to zero. Finite ball union and intersection volumes
are continuous in their centers. Zero radii follow by continuity, and
repeated source centers are reduced to the largest radius for unions
and the smallest for intersections.

## 5. Nonseparable radius dependence and a global cube example

For C=B(0,R), R>0, any admissible angular function a(u) gives

    T(r u)=r u                         if r<=R,
           [R+a(u)(r-R)]u              if r>R.             (11)

Its factor relative to the original radius is
a(u)+(1-a(u))R/r outside the ball. This depends jointly on radius and
direction. Thus the extension already gives a nonseparable family of
positive ray maps, while fixing an entire ball. For nonconstant a, it is
neither the original homogeneous map nor a common function of radius.
This does not prove the theorem for every nonseparable radial map.

For a non-spherical global example in R3 take C=[-1,1]^3, let p=P_C(x)
be coordinate clipping to this cube, and v=x-p. Define

    T_C(x)=p+|v1 v2 v3|v/|v|^3   if v!=0,
           x                     if v=0.                 (12)

The point-core factor a(u)=|u1 u2 u3| is admissible by PROOF.md. Thus
(12) is nonexpansive on all R3 and satisfies (4),(5). Unlike the point-core
map, it has Lipschitz constant exactly one, since it fixes a body with
interior. No symmetry of a law on or around the cube is required.

Since a<=1/(3sqrt(3))<1, the fixed-point set of (12) is exactly C.
Every homogeneous ray map about a point has a conical fixed-point set;
it cannot have this bounded fixed body. Even independent endpoint rigid
frames do not represent (12) by such a map: on the open fixed body the
aligned ray map would agree with an affine isometry. An affine map
parallel to its argument on an open set must be a scalar multiple of
the identity with zero translation. The nonnegative ray factor forces
that isometry to be the identity, returning to the conical-fixed-set
contradiction.

Nor can (12) be a common normal-profile map over any closed convex core
D in the original coordinates. For a nonnegative 1-Lipschitz profile
rho with rho(0)=0, r-rho(r) is nondecreasing. Its zero set is an interval
[0,b], possibly infinite, so the map's fixed set is D+bB. To equal the
bounded cube requires D bounded and b finite. A cube cannot equal D+bB
for b>0: on two nonparallel vectors in the positive orthant its support
function is linear, while h_D=h_C-b|.| violates subadditivity. Thus b=0
and D=C. But at the same normal distance the factor in (12) is zero in
direction e1 and 4/27 in direction (1,2,2)/3. No common rho gives both.
No exclusion of arbitrary compositions of previous classes is claimed.

The map also fails the direct scalar-defect test for every independent
unit-axis pair. In the open normal sectors of cube vertices the projection
is constant and its derivative is precisely that of the point-core
angular map. All of that proof's opposite rank-one derivative limits occur
in these sectors (at possibly different vertices). The same sum
-2h^2(e.e_k)^2(1+(f.u)^2) forces all components of e to vanish.
This transfers an existing separation argument, not a negative Gaussian
example or a new classification of arbitrary methods.

## 6. Scope and evidence

The enlargement is over all convex cores and all admissible normal
directions, with an exact characterization of every nonnegative map
affine on each complete normal ray. Arbitrary nonlinear dependence on
normal distance, signed factors, tangential motion and arbitrary endpoint
maps remain outside it. The earlier common-profile class permits radial
order reversal, which is not asserted by (2); these two extensions have
different freedoms. The point-core theorem is an exact special case.

[check_normal_bundles.py](check_normal_bundles.py) checks new rational
projection data and lifted distances using exact quadratic surds, including
singular and unbounded cores and zero/unit factors. It rejects a normal
ray criterion that is satisfied only at a finite sample. The universal
characterization, continuity and transfers are written mathematics.
All seven original angular files are preserved byte-for-byte;
NORMAL_INPUTS.json records their source pins. See NORMAL_SOURCES.md for credit,
the reproducibility boundary and provisional priority status.
