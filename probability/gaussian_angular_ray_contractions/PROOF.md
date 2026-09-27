# Contractions with an angular factor on each ray

Complete author proof, 27 September 2026. Independent correctness and
historical-priority review are pending. The unrestricted dimension-three
Gaussian-majorisation conjecture remains open.

The result covers every nonexpansive positively homogeneous map which
preserves each ray and its orientation. The factor may vary over all
directions. A fractional-linear deformation raises the map into one extra
coordinate; an orthogonal contraction then reaches the required endpoint.
The Gaussian and ball-volume transfers are established results, credited
in [SOURCES.md](SOURCES.md).

## 1. Statement and exact hypothesis

Let n>=2, let K be a nonempty Borel subset of the unit sphere S^(n-1), and write

    C(K) = {r u: r>=0, u in K}.

Let alpha:K->[0,1] and set T(0)=0 and

    T(r u) = r alpha(u) u.                                  (1)

Assume that T is 1-Lipschitz on the **whole cone** C(K). This is equivalent
to the following angular condition, for every u,v in K:

    c(1-a b) <= sqrt((1-a^2)(1-b^2)),
    a=alpha(u), b=alpha(v), c=u.v.                           (2)

**Theorem.** The map (1) has a continuous contracting motion in R^(n+1),
with two analytic pieces for each labelled trajectory and endpoints in
R^n x {0}. In particular:

* For every bounded Borel probability mu supported on C(K), every s>0,
  and every h>=0, with gamma_(n,s) the covariance-s I_n Gaussian,

      integral (mu*gamma_(n,s)-h)_+
        <= integral ((T#mu)*gamma_(n,s)-h)_+.                (3)

  Thus full majorisation holds, with arbitrary priors and nonatomic laws.

* For every finite list x_i in C(K) and arbitrary individual radii r_i>=0,

      vol_n union_i B(Tx_i,r_i) <= vol_n union_i B(x_i,r_i),
      vol_n intersection_i B(Tx_i,r_i)
        >= vol_n intersection_i B(x_i,r_i).                 (4)

These statements include n=3. Translations of the common ray origin,
independent endpoint isometries, restrictions, and finite compositions
preserve the conclusions. No symmetry of the input measure is assumed.
The factor alpha acts on the centers, not on the ball radii in (4).

For a finite list of rays, condition (2) itself is the complete checkable
hypothesis. When c<=0 it is automatic; when c>0 it can be checked by
squaring nonnegative sides. Ordinary contraction of just the selected
centers, or of just unit-radius representatives, is a weaker condition
and is not substituted for (2).

To verify the equivalence, the squared-distance loss for r u and q v is

    (1-a^2)r^2+(1-b^2)q^2-2c(1-a b)r q.                   (5)

For nonnegative r,q this quadratic is nonnegative exactly when (2) holds.
If the cross coefficient is nonpositive the assertion is immediate;
otherwise minimize in r/q. This also proves the cases a=1 or b=1 by
taking an unbounded ratio when necessary. Testing against zero gives
0<=alpha<=1, and (2) on the same ray forces its factor to be unique.

## 2. A norm-preserving raise

For 0<=theta<=pi/2 put tau=cos(theta), and define

    A_tau(a) = (a+tau)/(1+a tau),
    B_theta(a) = sqrt(1-a^2) sin(theta)/(1+a tau),
    F_theta(r u) = r (A_tau(alpha(u)) u, B_theta(alpha(u))). (6)

There is no vanishing denominator: 1+a tau>=1. The identity

    (a+tau)^2+(1-a^2)(1-tau^2) = (1+a tau)^2               (7)

shows that |F_theta(r u)|=r. The motion starts at (r u,0) and ends at

    L(r u) = (T(r u), r sqrt(1-alpha(u)^2)).                (8)

For a pair of unit directions, put d=sqrt((1-a^2)(1-b^2)). Their raised
inner product is

    k(tau) = [c(a+tau)(b+tau)+d(1-tau^2)]
              /[(1+a tau)(1+b tau)].                       (9)

Direct differentiation and factorization give

    k'(tau) = [(a+b)(1+tau^2)+2tau(1+a b)]
                [c(1-a b)-d]
              /[(1+a tau)^2(1+b tau)^2].                 (10)

Every factor except the bracket in (2) is nonnegative. Therefore k is
nonincreasing in tau. As theta increases, tau decreases and k increases.
For arbitrary radii the lifted squared distance is

    r^2+q^2-2r q k(cos(theta)),                            (11)

so it is nonincreasing. This is one simultaneous motion of the entire
cone, with no choice depending on an atom list or its weights.

When a<1 one can understand (6) by writing a=tanh z and tau=tanh w:
the first coefficient becomes tanh(z+w). This interpretation motivates
the deformation; formulas (6)--(10) prove it without infinite parameters.
In particular a=1 gives the fixed trajectory (r u,0), and a=0 is allowed.

## 3. Lowering the added coordinate and regularity

After (8), use 0<=t<=1 and the motion

    G_t(r u) = (T(r u),(1-t)r sqrt(1-alpha(u)^2)).           (12)

For a pair, its squared distance is the target squared distance plus

    (1-t)^2 [r sqrt(1-a^2)-q sqrt(1-b^2)]^2,

which is nonincreasing. Its final endpoint is (T(r u),0). Concatenating
(6) and (12) proves the motion theorem.

The original nonexpansiveness gives continuity of alpha on K, since
alpha(u)=|T(u)|. Formulas (6) and (12) are jointly continuous away from
the origin, and their norms are at most r at the origin. Each labelled
trajectory is analytic in theta on the first closed interval and linear
in t on the second. On a bounded support its coordinates and time
derivatives are uniformly bounded, directly from 0<=a<=1 and 1+a tau>=1.
No differentiability of alpha in the direction is required. Possible
coincident intermediate labels do not obstruct the continuous contraction.

## 4. Transfer to Gaussian energies and both ball volumes

Pad the motion by one zero coordinate, obtaining a continuous contraction
in R^(n+2). Aishwarya--Li Theorem 1.4(i)(a) compares density values sampled
from the two endpoint Gaussian convolutions. These endpoint densities
factor as f(x)gamma_(2,s)(z) and g(x)gamma_(2,s)(z), where f and g are the
two n-dimensional convolutions in (3).

If X has density f and Z independently has density gamma_(2,s), then,
with C=(2 pi s)^(-1),

    Pr[f(X)gamma_(2,s)(Z)>h C]
      = integral f(x)(1-h/f(x))_+ dx
      = integral(f-h)_+ dx.                               (13)

Here |Z|^2/(2s) is exponential of mean one. Apply the sampled-density
order and the same identity for g to obtain (3). At h=0 both sides are
one. This is the established two-coordinate cancellation, not a new
internal-energy transfer theorem. The usual convex-energy comparisons
follow from the hinge characterization whenever the integrals are defined.

For a finite list, reverse the piecewise-analytic motion and apply
Bezdek--Connelly Theorem 1 in dimension n+2. It gives both assertions (4).
One can avoid all collisions in applying that theorem: replace alpha by

    alpha_epsilon=(1-epsilon)alpha+epsilon,  0<epsilon<1.

Its map is (1-epsilon)T+epsilon I, hence is nonexpansive and still satisfies
(2). Its positive factors make the target, every first-stage configuration,
and every second-stage configuration injective on distinct source points.
Apply the theorem and let epsilon decrease to zero. Finite union and
intersection volumes of balls are continuous in their centers. Positive
radii can likewise decrease to zero. Repeated source centers are handled
by retaining the largest radius for a union and the smallest for an
intersection. Thus no distinctness or positive-radius hypothesis is hidden.

## 5. Angular freedom and a global three-dimensional example

On the whole sphere, a useful sufficient condition for a locally Lipschitz
alpha is

    0<=alpha<=1,    |grad_S alpha|<=1-alpha^2 a.e.           (14)

For example alpha=tanh z, where z is any nonnegative C^1 function on the
sphere with |grad_S z|<=1. This allows arbitrary smooth angular patterns,
not just a finite number of cones or a common factor.

Here is the differential check behind (14). At a differentiability point,
the derivative of x->alpha(x/|x|)x has the form

    J=alpha I+u (grad_S alpha)^T.

On the span of u and grad_S alpha it is the shear matrix
[[alpha,g],[0,alpha]], g=|grad_S alpha|; on the remaining directions it
is alpha I. For q>=alpha, its norm is at most q precisely when

    g <= q-alpha^2/q,                                     (15)

with the zero case interpreted separately. This follows from the two
principal minors of q^2 I-J^T J. Taking q=1 gives (14). Integrating the
derivative on almost every segment parallel to a fixed direction, then
passing to every segment by continuity, proves global nonexpansiveness.
The map is locally Lipschitz away from zero and has a continuous extension
at zero; a segment through zero can be split there.

A concrete example in R3 is

    alpha(u)=|u_1 u_2 u_3|,
    T(x)=|x_1 x_2 x_3| x/|x|^3 for x!=0, T(0)=0.          (16)

It is in fact 2/3-Lipschitz. To see this, write z_i=u_i^2, so sum z_i=1.
At a point off the coordinate planes,

    alpha^2=z_1 z_2 z_3<=1/27,
    |grad_S alpha|^2=z_1 z_2+z_1 z_3+z_2 z_3
                         -9z_1 z_2 z_3<=1/3.

For q=2/3, the right side of (15) is at least 11/18, whose square exceeds
1/3 by 13/324. Thus the derivative norm is at most 2/3 in every open
orthant. A segment crosses finitely many coordinate planes; if it lies
in one, T is zero on it. Integrating on the remaining pieces, and using
continuity at zero, proves the global Lipschitz bound.

This example shrinks different directions by different factors and
collapses all three coordinate planes. The result applies to every bounded
law on R3 and to arbitrary ball radii, not only to the finite control below.

### What established direct tests do not supply for this example

The map (16) is not one common radius profile about the origin: points of
one sphere have different output norms. Its full-domain claim therefore
is not an instance of the earlier radial-profile formula. No strict
containment of the arbitrary-convex-core class is asserted.

It also fails the earlier scalar-defect condition for every pair of
independent unit axes e,f. Suppose that condition held. At a unit point
u on the kth coordinate plane with its other coordinates nonzero, the
two one-sided derivative limits are

    J_+=h u e_k^T,     J_-=-h u e_k^T,     h>0.

Apply the proposed scalar-defect quadratic to the unit vector e at these
two derivative limits. Put E=e.e_k and F=f.u. The two nonnegative
quantities would be

    1-h^2 E^2-(1-h F E)^2,
    1-h^2 E^2-(1+h F E)^2.

Their sum is -2h^2 E^2(1+F^2), so E=0. Repeating for k=1,2,3 forces
e=0, a contradiction. Rational choices such as u=(0,3/5,4/5) give
h=12/25. This exclusion is a consequence of the positive-class example,
not the main theorem or a counterexample to majorisation.

Nor is (16) a strong coordinatewise contraction after independent rigid
changes of frames. Such a representation would make each output coordinate
depend on just one input linear coordinate. Since T vanishes on three
distinct planes, each such one-variable function would vanish identically:
its input functional is nonconstant on at least one of those planes.
That would make T identically zero, contrary to (16). Translations only
add constants and do not change this argument. No exclusion of arbitrary
compositions of earlier classes is claimed.

For the finite rank control, use zero, e_1,e_2,e_3, and
(1,2,2)/3, (2,1,2)/3, (2,2,1)/3. The last three have alpha=4/27.
The six nonzero paired vectors (x,T(x)) have determinant 320/531441,
so their paired affine rank is six. The checker also includes (2,3,6),
whose factor is 36/343, and audits every pair. This is a calibration
fixture, not an exhaustive proof or an independently reviewed result.

## 6. Scope of the contribution

The uniform principle is the lift (6) and its exact sign (10), which uses
the full ray geometry in (2). It supplies an all-variance Gaussian class
and both arbitrary-radius Kneser--Poulsen inequalities. It does not merely
sign fixed-configuration asymptotics or a selected finite energy degree.

The classical norm-displacement interpolation does not supply this entire
class directly. For two rays with a=0, b=4/5 and c=3/5, condition (2) is
an equality. Choose center radii r=3/5 and q=1. Their source and target
squared distances both equal 16/25, whereas the squared distance at the
midpoint of that classical interpolation is 77/125. Thus it decreases and
then increases. The new motion keeps this pair distance constant. This
two-ray calculation only distinguishes the displayed motions; the theorem
above is uniform in the whole cone and in its number of directions.

The prior nonnegative radial-profile theorem changes radii by one common
function rho(r). The present theorem permits arbitrary admissible angular
factors instead. Composing the two known-positive maps also handles
alpha(u)rho(r)u and rho(alpha(u)r)u, with the same conclusions. That closure
observation invokes the prior radial result; it is not used in the proof
of (1)--(4).

General angular remapping, negative factors, arbitrary radius-and-direction
dependence, and contraction known only at selected radial samples are
outside the stated theorem. The accepted cap/flap/axial/convex-core work
is preserved. No all-method classification, optimal dimension, historical
priority, or resolution of the unrestricted problem is claimed.
