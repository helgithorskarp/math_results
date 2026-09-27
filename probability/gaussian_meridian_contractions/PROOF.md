# Azimuth-preserving contractions: a meridian lift in two extra dimensions

Complete author proof, 27 September 2026. Independent mathematical review,
formalization and historical priority remain pending. The unrestricted
three-dimensional Gaussian-majorisation question remains open.

## 1. The entire meridian class

Let n>=2, let E be a nonempty Borel subset of [0,infinity) x R, and let

    S:E -> [0,infinity) x R,      S(r,z)=(rho(r,z),zeta(r,z))

satisfy, for every p=(r,z), q=(s,w) in E,

    |S(p)-S(q)| <= |p-q|,          0 <= rho(r,z) <= r.       (1)

Use the standard Euclidean metric in this two-dimensional meridian plane.
Define the rotational domain and its azimuth-preserving map by

    D={ (r u,z): (r,z) in E, u in S^(n-2) },
    T(r u,z)=(rho(r,z)u,zeta(r,z)).                           (2)

At r=0 the value does not depend on u, because rho=0. In dimension three,
u is the azimuth on the circle around the distinguished axis. Both rho
and zeta may depend on both r and z. No order, differentiability, homogeneity,
or convexity assumption on S or E is imposed.

**Theorem.** The map (2) has one simultaneous contracting motion in
R^(n+2), with analytic trajectories and endpoints in R^n x {0,0}.
Consequently, writing gamma_(n,s) for the covariance-s I_n Gaussian:

* For every bounded Borel probability measure mu concentrated on D, every
  variance s>0 and every h>=0,

      integral (mu*gamma_(n,s)-h)_+
        <= integral ((T#mu)*gamma_(n,s)-h)_+.                (3)

  Thus full Gaussian majorisation, and every defined convex internal-energy
  comparison with energy density U(0)=0, hold for this class.

* For every finite list of centers x_i in D and arbitrary individual ball
  radii a_i>=0,

      vol_n union_i B(Tx_i,a_i) <= vol_n union_i B(x_i,a_i),
      vol_n intersection_i B(Tx_i,a_i)
        >= vol_n intersection_i B(x_i,a_i).                 (4)

The probability law, its atom weights and its support need not have any
rotational symmetry. The centers need not include full circles or orbits.
Only the map admits the rotational extension (2). The a_i in (4) are
independent of the cylindrical coordinates r_i of the centers.

The hypotheses in (1) are exactly those for a nonnegative azimuth-preserving
map (2) to be 1-Lipschitz on the **full** rotational domain D. Indeed,
same-azimuth pairs give the meridian contraction, and opposite points on
one circle give rho<=r. Conversely, for c=u.v,

    |(r u,z)-(s v,w)|^2=|p-q|^2+2rs(1-c),                  (5)

and the target has the analogous expression with S(p),S(q),rho_p rho_q.
Both summands decrease under (1). Contractivity on just an arbitrarily
selected list of azimuths is weaker; it is not substituted for (1).

The theorem is invariant under common Euclidean similarities and independent
endpoint isometries. Restrictions and finite compositions inherit (3)-(4).
Signed transverse factors and changes of azimuth are outside the theorem.

## 2. The motion and universal sign

For 0<=t<=1 put

    A_t(p)=(1-t)r+t rho_p,     B_t(p)=(1-t)z+t zeta_p,
    F_t(r u,z)=( A_t(p)u, B_t(p),
                 sqrt(t(1-t))(r-rho_p),
                 sqrt(t(1-t))(z-zeta_p) ).                  (6)

There are n-1 transverse coordinates, one axial coordinate and exactly two
auxiliary coordinates. The meridian displacement (r-rho,z-zeta) supplies
the auxiliary vector; it does not retain the azimuth u.

Direct expansion gives, simultaneously for every pair,

    |F_t(r u,z)-F_t(s v,w)|^2
      =(1-t)|p-q|^2+t|S(p)-S(q)|^2
         +2 A_t(p) A_t(q)(1-u.v).                           (7)

To see this without any sampled calculation, first set u.v=1. The first,
axial and two auxiliary coordinates are exactly the classical planar
leapfrog, whose squared distance is the first two terms of (7). For general
u,v the change in the transverse squared distance is exactly the last term.
Equivalently, expand the two auxiliary squares to cancel the quadratic
interpolation defects of both meridian coordinates.

The first two terms of (7) are nonincreasing by (1). Each A_t is
nonnegative and nonincreasing, so their product is nonincreasing too.
More explicitly, its derivative is

    |S(p)-S(q)|^2-|p-q|^2
     -2(1-u.v)[(r-rho_p)A_t(q)+(s-rho_q)A_t(p)] <=0.        (8)

No sign is required of z-zeta. This is what allows coupled axial motion
and reversals of meridian order. Formula (8) proves the entire class,
not only the finite benchmark below.

Set t=sin(theta)^2, 0<=theta<=pi/2. The square root in (6) is then
sin(theta)cos(theta), so every labeled trajectory is analytic through both
endpoints, even if S is merely Lipschitz. At the axis, |A_t(p)u|<=r tends
to zero, and the remaining coordinates are continuous functions of (r,z).
Thus the motion is jointly continuous. All coordinates and time derivatives
are uniformly bounded on every bounded part of D: S is Lipschitz and has
one fixed finite reference value.

Distinct source points cannot collide at 0<=t<1. If their meridian points
differ, the first term in (7) is positive. If the meridian points agree,
distinct physical points have r>0 and u!=v, while A_t>=(1-t)r>0.
At t=1 target collisions are permitted.

## 3. Credited Gaussian and ball-volume transfers

Apply Aishwarya--Li, arXiv:2609.07041v2, Theorem 1.4(i)(a), to (6) in
R^(n+2). It orders the values of the two endpoint densities when sampled
from their own distributions. At the endpoints those densities are
f(x) gamma_(2,s)(y) and g(x) gamma_(2,s)(y), with f and g the densities
in (3). If X has density f and Z independently has density gamma_(2,s),
then gamma_(2,s)(Z)/(2pi s)^(-1) is Uniform[0,1]. Therefore

    Pr{ f(X) gamma_(2,s)(Z)>h(2pi s)^(-1) }
       =integral f(x)(1-h/f(x))_+ dx
       =integral(f-h)_+ dx.                                 (9)

The same identity for g proves (3); h=0 follows from equal mass. This
is the existing two-coordinate cancellation, explicitly anticipated by
Aishwarya--Li after Theorem 1.5, not a new transfer theorem. It applies
directly to bounded diffuse laws, without atom approximation.

Reverse the analytic motion and apply Bezdek--Connelly, Theorem 1, to
obtain (4) in dimension n. If a distinct-center formulation is desired,
replace S by S_epsilon=(1-epsilon)S+epsilon I. This is still a contraction,
with epsilon r<=rho_epsilon<=r. For finitely many distinct meridian points,
only finitely many epsilon values can cause target coincidences, since
each difference is affine in epsilon and is nonzero at epsilon=1.
Distinct azimuths at one positive radius cannot coincide for epsilon>0.
Apply the theorem along a sequence avoiding the exceptional values and
let epsilon tend to zero. Repeated source centers can be merged, retaining
the largest ball for a union and the smallest for an intersection. Zero
ball radii follow by continuity. These operations impose no common radius.

The new geometric input is (6)-(8) for the whole meridian class. The
leapfrog, the Gaussian comparison and the n+2-dimensional ball transfer
are classical or cited inputs. Historical priority for this application
has not been established by an exhaustive literature search.

## 4. Breadth: tangential and genuinely coupled maps

**Arbitrary latitude profiles, including reversals.** Fix 0<b<=pi/2 and
any 1-Lipschitz phi:[0,b]->[0,b] with phi(0)=0 and phi>=0. In a meridian
write p=R(sin(theta),cos(theta)), R>=0. Define

    S(p)=R(sin(phi(theta)),cos(phi(theta))).                 (10)

One has phi(theta)<=theta, so the transverse radius decreases. For two
meridian points, the distance is

    (R-Q)^2+2RQ[1-cos(theta-eta)].

The absolute angle difference is at most pi/2 and contracts under phi;
hence S satisfies (1). The theorem therefore permits arbitrary folding
of latitude on a hemisphere while preserving distance to the origin and
azimuth. It does not require phi to be monotone. For instance, if 0<2a<=b,
the three continuous branches theta, 2a-theta, theta-2a on [0,a],
[a,2a], [2a,b] form a permitted profile. This is a breadth example of
the same meridian theorem, not a separate sufficient theorem.

**A global, nonhomogeneous two-variable map.** On the whole meridian
half-plane take

    rho(r,z)=r(2+sin z)/(4(1+r)),
    zeta(r,z)=(sin r+|z|)/4.                                (11)

Then 0<=rho<=3r/4. Away from z=0 the absolute derivative bounds for
(rho_r,rho_z,zeta_r,zeta_z) are respectively 3/4,1/4,1/4,1/4.
Their squared sum is 3/4, so integration on line segments gives
Lip(S)<=sqrt(3)/2<1; the same bound holds across z=0 by continuity and
piecewise integration. Thus (11) is included on all R^n. The two meridian
coordinates are coupled and nonlinear. The fixed set of the resulting T
is {0}, but points with z=0 generally acquire a nonzero axial coordinate.
Consequently this displayed global map is not a convex-normal map of
our earlier form in these coordinates: a nonempty fixed convex core would
have to be {0}, whose normal maps preserve rays. This comparison does
not exclude other representations after independent endpoint frames or
compositions of older classes.

The theorem also recovers ordinary radial profiles about the origin:
S(p)=q(|p|)p/|p| with q>=0, q(0)=0 and Lip(q)<=1. Their meridian map
is a contraction and rho<=r. Their sharper one-extra-coordinate proof is
preserved. Direction-dependent normal maps without axial symmetry are not
subsumed; the classes overlap rather than contain one another.

## 5. Seven exact labels beyond the direct rank and scalar criteria

For a rational benchmark, use the meridian sector z>=0, 0<=r<=4z/3 and

    S(r,z)=(r,z)                         if r<=z/2,
           ((-3r+4z)/5,(4r+3z)/5)        if r>=z/2.         (12)

This is the restriction of a planar fold across r=z/2, hence is
1-Lipschitz. It has 0<=rho<=r on the sector. Its rotational extension
preserves every norm, fixes an open circular cone and folds its exterior
meridian region into that cone. The seven labels are

    0, (0,0,1), (1,0,2), (0,1,2),
       (1,0,1), (-1,0,1), (0,1,1).                         (13)

The first four stay fixed. The final three become

    (1/5,0,7/5), (-1/5,0,7/5), (0,1/5,7/5).              (14)

The six nonzero paired vectors (x,Tx) have rank six, and the displacement
vectors span R3; exact determinants are recorded in EXPECTED.json. Thus
neither the paired-affine-rank-five criterion nor the direct two-dimensional
displacement criterion applies. Seven exceeds the classical n+3 point
count in dimension three. No small-number theorem proves the whole class. This benchmark alone is
not a historical-novelty certificate.

The scalar-defect criterion asks for unit vectors e,f with

    |x-x'|^2-|Tx-Tx'|^2 >= |e.(x-x')-f.(Tx-Tx')|^2.

Every pair with the fixed origin has zero loss here, forcing e.x=f.Tx on
all six nonzero labels. Rank six forces e=f=0, a contradiction. This
exclusion already permits independent endpoint orthogonal frames and
translations (pair differences remove translations). The norm-preserving
rank obstruction is credited to the earlier scalar-defect packet.

The full map (12) is also not one strong coordinate contraction in any
independent input/output orthonormal frames. Coordinatewise contraction
on an open set forces each output coordinate to depend only on its
corresponding input coordinate. On the fixed open cone the derivative
is I, so those two frames agree up to coordinate signs. At an exterior
point (r u,z), the meridian derivative is reflection with unique negative
eigendirection (2u,-1)/sqrt(5); the azimuth eigenvalue is rho/r in (0,1).
These negative eigendirections vary continuously with u and cannot all
be among three fixed coordinate axes. This proves the assertion for the
full map, not an all-frame finite test of the seven labels. Finite chains
of strong contractions, or combinations of other known classes, are not
excluded.

The conical fold (12) can itself be expressed using signed normal
reflection about a convex cone. Its role here is a transparent certificate
against the direct rank/scalar tests, not a claim that one further
normal-ray case is the new result. The theorem concerns arbitrary
coupled meridian contractions such as (11), and (10) with general profiles.

## 6. Scope, dependencies and reproducibility

The finite check verifies the universal polynomial identity (7), its
derivative (8), exact finite families including axes and collisions, the
rank-six benchmark, and deliberately false controls. Checks use integers
and Fraction; they remain active under Python -O. They do not replace the
continuum proof, certify historical priority, numerically integrate a
Gaussian, or prove minimality of the ambient dimension.

This is a constructive geometric class. It neither classifies extremal
maps (researcher 4's lane) nor supplies a Gaussian counterexample
(researcher 7's lane). The reviewed angular/normal and axial/matrix packets
are preserved. There is no premise imported from the team's newer moment,
small-loss, covariance-collapse or contact results. The remaining obstacle
is to handle maps that do not admit (1)-(2), in particular arbitrary changes
of azimuth; the full shared question remains open.
