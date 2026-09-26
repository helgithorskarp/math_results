# Damped cone reflections: a variational motion criterion

Complete author proof, 26 September 2026. Independent review and formal
verification are pending. The full dimension-three Gaussian-majorisation
problem remains open. The positive result concerns a uniform geometric
class at every Gaussian variance and every ball radius.

Identify R3 with C x R. For a compact set P in C containing zero, write

    C(P) = {(z u,z): z >= 0, u in P}.

Convexity and central symmetry are not needed below. For 0 < lambda <= 1,
define the damped reflection on D = C(P) union (-C(Q)) by

    T_lambda(a) = lambda a,       a in C(P),
    T_lambda(-b) = lambda b,      b in C(Q).

The two pieces meet only at zero. All norms and volumes are Euclidean.
The word damped refers to the factor lambda at BOTH endpoint clusters.

## 1. The geometric principle

For a complex number s and a real number xi <= 0, set

    Phi_PQ(s,xi) = max_{u in P,v in Q}
                  [xi |u||v| - Re(s conjugate(u) v)].                 (1)

It is nonnegative because zero belongs to P and Q. It is a support function
of the compact convex hull of
(Re(conjugate(u)v), Im(conjugate(u)v), |u||v|), evaluated in the indicated
direction. The third coordinate must be retained: in general one cannot
replace the product set by its planar convex hull before taking (1).

**Theorem 1.** Suppose a piecewise continuously differentiable path
w:[0,1] -> C excluding zero satisfies

    w(0) = -1,  w(1) = lambda^2,
    x(t) = |w(t)| is nonincreasing,
    L = integral_0^1 Phi_PQ(w'(t),x'(t)) dt <= 2.                    (2)

Then T_lambda has a continuous contracting motion in R4. Consequently:

* For every bounded Borel probability law mu on D, every s > 0, and every
  h > 0, writing f = mu * gamma_(3,s) and
  g = (T_lambda # mu) * gamma_(3,s),

      integral (f-h)_+ <= integral (g-h)_+.                         (3)

  This is full majorisation, with no restriction on weights, atom count,
  or nonatomic mass.
* If the control path w is piecewise real analytic, then for any finite
  labeled centers z_i in D and arbitrary individual radii r_i >= 0,

      vol union_i B(T_lambda(z_i),r_i) <= vol union_i B(z_i,r_i),
      vol intersection_i B(T_lambda(z_i),r_i)
          >= vol intersection_i B(z_i,r_i).                        (4)

  These are three-dimensional volumes. For every compact E in D and every
  r > 0, vol(T_lambda(E)+r B3) <= vol(E+r B3).

A common Euclidean similarity can be applied to the entire construction.
An arbitrary affine change of metric is not part of the assertion.

**Proof of the motion.** Choose a continuous argument theta with
w = x exp(i theta), starting at theta = pi. Its final value is a multiple
of 2 pi. Put rho = sqrt(x). If L > 0, define

    c(t) = -1 + (2/L) integral_0^t Phi_PQ(w',x') dt,
    d(t) = sqrt(1-c(t)^2).                                        (5)

Thus c is nondecreasing from -1 to 1. If L = 0 use any continuously
differentiable nondecreasing c with these endpoints. In R4 use the maps

    G_t(a) = (rho a_perp, a_z, 0),
    F_t(b) = (rho R_theta b_perp, c b_z, d b_z),                    (6)

where the original input -b follows F_t(b). Distances within each cluster
are nonincreasing: their squares are x |Delta_perp|^2 + |Delta_z|^2.

For a = (z_a u,z_a), b = (z_b v,z_b), the cross-distance square is

    D_t = x(z_a^2 |u|^2 + z_b^2 |v|^2)
          + z_a^2 + z_b^2
          - 2 z_a z_b [Re(w conjugate(u)v) + c].                   (7)

For positive z_a,z_b, use x' <= 0 and
z_a^2 |u|^2 + z_b^2 |v|^2 >= 2 z_a z_b |u||v| to obtain

    D_t' <= 2 z_a z_b
             [Phi_PQ(w',x') - c'] <= 0                            (8)

almost everywhere. A zero height represents the origin and is handled
directly by (6). Absolute continuity of (7) proves monotonicity.

The first-stage endpoints are the original configuration and
(lambda a_perp,a_z), (lambda b_perp,b_z), all in the original R3.
Finally multiply the axial coordinate of EVERY point by a common factor
decreasing from 1 to lambda. This is a linear continuous contraction and
gives precisely T_lambda. Thus (6) and this final stage form the required
R4 motion. They also prove that the endpoint map is 1-Lipschitz; no separate
endpoint contraction assumption is hidden in the theorem. A global
1-Lipschitz extension exists by Kirszbraun's theorem.

## 2. A closed formula, optimal for this motion form

Let C_p = {(u,z): z >= 0, |u| <= p z}, with p,q > 0. Define, for 0 <= eta <= 1,

    F(eta) = sqrt(1-eta^2)
             + eta (pi-arccos(eta)) + eta - 1.                    (9)

**Theorem 2.** All conclusions (3)--(4) hold for T_lambda on
C_p union (-C_q) whenever

    pq F(lambda^2) <= 2.                                        (10)

The construction is piecewise analytic after reparametrization. Condition
(10) is necessary and sufficient **within the following motion form**:
the first stage is (6), |w| decreases from 1 to lambda^2, both axial norms
stay equal to their initial values, and the final stage is a common axial
shrink. This is not a necessity claim for arbitrary R4 or R5 motions,
majorisation, or Kneser--Poulsen inequalities.

**Proof.** Write kappa = pq and eta = lambda^2. For disks, phases and
magnitudes can be chosen independently, and |w'| >= |x'|. Thus

    Phi_PQ(w',x') = kappa (|w'| + x'),
    L = kappa [length(w) + eta - 1].                            (11)

The shortest allowed curve from -1 to eta is the tangent from -1 to the
circle of radius eta, followed by the shorter circular arc to eta.
For 0 < eta < 1 its tangent point and length are

    z_* = -eta^2 + i eta sqrt(1-eta^2),
    ell = sqrt(1-eta^2) + eta (pi-arccos eta).                    (12)

The segment's radius decreases from 1 to eta; the arc has constant radius.
Both pieces are analytic. At eta = 1 use the unit semicircle.

Here is a lower-bound proof that covers nonmonotone angular controls and
arbitrary winding numbers. On the universal angular cover of |w| >= eta,
write w = r exp(i theta) and set

    A(r) = sqrt(r^2-eta^2) - eta arccos(eta/r),
    Psi_sigma(r,theta) = A(r) + sigma eta theta,  sigma in {+1,-1}.

The Euclidean gradient has norm one:

    A'(r) = sqrt(r^2-eta^2)/r,
    A'(r)^2 + eta^2/r^2 = 1.                                   (13)

The derivative extends continuously to r = eta. Choose sigma to agree with
the sign of the initial-minus-final angle. That angular difference has
absolute value at least pi. Integrating the unit gradient along any
rectifiable allowed curve proves

    length(w) >= A(1) + pi eta = ell.                           (14)

The tangent and arc attain this bound, proving (10) by Theorem 1.

For necessity within (6), within-cluster monotonicity on the full cones
forces x' <= 0. At any regular time choose |u| = p, |v| = q and phases
maximizing -Re(w' conjugate(u)v), then choose z_a p = z_b q.
Equality holds in the arithmetic--geometric-mean bound in (8).
Consequently every such motion must satisfy

    c' >= kappa (|w'| + x').                                    (15)

Integrating c(1)-c(0)=2 and applying (14) gives (10). For the minimizing
path one can explicitly use c = -1 + 2(s+x-1)/F(eta), where s is arclength
already traversed. For eta > 0 this c is strictly increasing on each
nondegenerate piece. Reparametrizing at c = -1 and c = 1 by a squared
time variable makes sqrt(1-c^2) analytic on the one-sided pieces. The
eta = 1 case is the usual cosine parametrization. This proves the
regularity asserted in the theorem.

The function F is strictly increasing and strictly convex on (0,1):

    F'(eta) = 1 + pi-arccos eta,
    F''(eta) = 1/sqrt(1-eta^2),
    F(0)=0, F(1)=pi.                                           (16)

Hence every finite kappa admits a positive damping range. If kappa <= 2/pi,
lambda = 1 is allowed, recovering the circular part of the earlier
[axial cone theorem](../gaussian_axial_cone_rotations/PROOF.md).
If kappa > 2/pi there is a unique eta_* in (0,1) with
kappa F(eta_*) = 2, and every lambda <= sqrt(eta_*) is allowed.

For comparison, first shrinking transverse coordinates to lambda, applying
that earlier undamped circular theorem, and finally shrinking the axial
coordinate only gives pi kappa lambda^2 <= 2. Strict convexity yields
F(eta) < pi eta for 0 < eta < 1, so (10) strictly improves this particular
composition for every kappa > 2/pi. We do not exclude all other possible
compositions, choices of axis, or linear coordinate changes.
As kappa tends to infinity,

    eta_* ~ 4 / ((pi+2) kappa),                                 (17)

whereas that composition gives 2/(pi kappa). Thus the principle is a
uniform tradeoff for all apertures, not just a change to one angle bound.

For compact centrally symmetric convex P,Q and lambda = 1, choosing the
unit semicircle in (1) recovers one half of the perimeter of the planar
complex-product hull. Thus Theorem 1 also extends the earlier perimeter
mechanism; for noncircular sections it retains their product geometry.

## 3. Majorisation and volume: the external bridges

Pad the R4 motion by one zero coordinate. At its R5 endpoints, Gaussian
convolution gives f(x) gamma_(2,s)(y) and g(x) gamma_(2,s)(y).
[Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
gives stochastic order of these densities sampled from themselves along
a continuous contraction. If Y has density gamma_(2,s), then
gamma_(2,s)(Y) = C exp(-E), where C = (2 pi s)^(-1) and E is mean-one
exponential. Therefore

    P{f(X) gamma_(2,s)(Y) > C h}
       = integral f(x) (1-h/f(x))_+ dx
       = integral (f-h)_+.                                    (18)

This proves (3), using the same two-coordinate cancellation as the team's
[paired-rank result](../gaussian_majorisation_rank_abel/PROOF.md).
No cancellation of a generic product-majorisation inequality is asserted.
The unpadded R4 motion also gives the retained Gamma(1/2) density-value
comparison from the earlier axial source. It is not needed here.

For (4), keep only the finitely many normalized transverse coordinates in
the chosen centers and adjoin zero to each finite set. Their Phi is no
larger than (1). Along a piecewise analytic control w, it is the maximum
of finitely many analytic functions on each compact analytic piece.
Such a maximum has finitely many analytic pieces (identically equal
branches cause no problem). Formula (5) is then piecewise analytic;
at zeros of 1-c^2 a finite even-power reparametrization removes the
one-sided square roots. Constant pieces can be concatenated. The final
linear shrink is analytic too. Padding to R5 and reversing the motion
permits [Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098)
to give both inequalities in (4). Coincident centers and zero radii follow
by continuity. For compact equal-radius neighborhoods, (3) and
Aishwarya--Li, Theorem 1.8(i), apply to a full-support law on E.
These consequences use established theorems; the new input is the motion.

## 4. Proper dual cones and the exact undamped obstruction

Let K be a closed, pointed, full-dimensional convex cone in R3, and K* its
positive dual. The positive theorem applies to the damped map on K* union
(-K) after choosing finite circular envelopes about a common axis.
Such an axis always exists. To see this, choose v in int(K*) and minimize
the Euclidean norm on the compact base B = {b in K: v.b=1}.
If b0 is the minimizer, then b0.b >= |b0|^2 > 0 for all b in B.
Thus b0 belongs to int(K*). Perturbing it slightly toward any point in
int(K) produces e in int(K) intersect int(K*). Normalize e to length one.
Both K and K* make an angle strictly less than pi/2 with e, so both have
finite slopes p,q about that axis. Theorem 2 gives a uniform positive
lambda range, independent of the chosen bounded law or finite centers.

There is a sharp qualitative reason that damping can matter. The undamped
map on a full nonsimplicial proper dual pair does **not** admit a continuous
contracting motion in R5. The following proof extends the mechanism of the
team's [square-cone obstruction](../gaussian_simplicial_cone_reflections/PROOF.md).
Its positive-operator ingredient is classical: see
[Loewy--Schneider, Indecomposable Cones, Theorem 3.3](https://people.math.wisc.edu/hans/loew_s75.pdf).
We reproduce the elementary three-dimensional argument.

Keep the origin among the sites. Distances within either cloud and to the
origin have identical endpoints, so a contracting motion preserves them
throughout. After subtracting the moving origin, the two clouds are given
by continuous linear isometric embeddings G_t,F_t:R3 -> R5, with F_t
acting on the positive argument b of the input -b. Set L_t = G_t^* F_t.
Then L_0=-I, L_1=I, and

    rank(I-L_t^* L_t) <= 2.                                    (19)

Indeed I-L_t^*L_t is the Gram matrix of (I-G_t G_t^*)F_t, whose range is
in the two-dimensional orthogonal complement of G_t(R3).
Cross-distance monotonicity gives

    -a.b <= a.L_t b <= a.b,  a in K*, b in K.                   (20)

Thus I+L_t and I-L_t both map K into itself. For an extreme ray b,
2b=(I+L_t)b+(I-L_t)b forces L_t b to lie on that same line.
A positive affine base of a proper three-dimensional cone has no three
collinear extreme points. Consequently any three distinct extreme rays
are linearly independent. If K is nonsimplicial, take four extreme rays.
The fourth has all three coefficients nonzero in the basis of the first
three; being an eigenvector on all four rays forces L_t to be scalar.
This scalar varies continuously from -1 to 1 and crosses zero, violating
(19). Truncating each cone while retaining every ray gives the same proof.

For a polyhedral cone it suffices to keep its extreme-ray generators,
the extreme-ray generators of its positive dual, and the origin. The
inequalities on these finite generators extend bilinearly to (20).
The usual six-dimensional leapfrog gives the matching upper bound.
Combined with researcher 7's simplicial-cone R5 motion, this classifies
full proper dual pairs: an R5 motion exists exactly in the simplicial case.
This is a motion classification, not a negative Gaussian hinge.

For the self-dual circular cone C_1, the new positive statement is especially
simple: lambda=sqrt(2/3) is allowed for the entire cone pair. In fact,

    F(2/3) < sqrt(5)/3 + pi/2 - 1/3 < 2 - 1/84,                (21)

using arccos(2/3)>pi/4, sqrt(5)<9/4, and pi<22/7.
The undamped full pair has the R5 obstruction just proved. Equation (21)
does not imply any statement about its unscaled Gaussian hinges.

These positive maps are also complementary to researcher 5's
[scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md).
On two open cone pieces, that criterion for T_lambda would require unit
vectors e,f with

    |e-lambda f|^2 <= 1-lambda^2,
    |e+lambda f|^2 <= 1-lambda^2,                               (22)

by considering arbitrary small within-piece differences. Their sum is
impossible for every lambda>0. Independent endpoint rotations are already
included in the independent choices of e,f.

## 5. A rational finite certificate

Let P be the convex hull of the following twelve rational unit vectors,
listed counterclockwise:

    (1,0), (4/5,3/5), (3/5,4/5), (0,1),
    (-3/5,4/5), (-4/5,3/5), (-1,0),
    (-4/5,-3/5), (-3/5,-4/5), (0,-1),
    (3/5,-4/5), (4/5,-3/5).

Its polar Q has the twelve vertices obtained by quarter turns of

    (1,1/3), (5/7,5/7), (1/3,1).

Because P is centrally symmetric, C(Q)*=C(P). Take the 12 height-one
generators A0 of C(P) and B0 of C(Q). Adjoin to A0 the six points
e3 +/- e_i/4, and to B0 the six points 2e3 +/- e_i/4, for i=1,2,3.
Call the resulting 18-point sets A and B. The labeled contraction is

    (0,A,-B) -> (0,(4/5)A,(4/5)B).                             (23)

There are 37 distinct centers at each endpoint. The circular envelopes
have p=1, q=sqrt(10)/3. The following entirely rational bounds prove (10):

    eta = 16/25,
    sqrt(1-eta^2) < 77/100,
    arccos(eta) > 7/8,
    F(eta) < 1303/700,
    kappa = sqrt(10)/3 < 19/18,
    2-kappa F(eta) > 443/12600.                                (24)

For the arccos bound, the alternating Taylor polynomial
1-t^2/2+t^4/24-t^6/720 at t=7/8 is strictly greater than 16/25 and is a
lower bound on cos(t). The upper bound pi<22/7 follows from the positive
integral of x^4(1-x)^4/(1+x^2) on [0,1]. No floating sign is used.

All 666 pairs strictly contract. The paired affine rank is six. For
example, choose the east, north, west generators in A0, and the generators
with transverse coordinates (1,1/3), (1/3,1), (-1,-1/3) in B0.
Their paired six-row determinant has absolute value 16384/1125.
Thus the paired-rank-five criterion, even after separate endpoint rigid
alignments, does not establish (23).

The six added coordinate pairs in each cloud also rule out the scalar-defect
criterion for this FINITE example, including independent endpoint frames.
After dividing each pair by its input length 1/2, its inequalities would be
(e_i-lambda f_i)^2 <= 1-lambda^2 and
(e_i+lambda f_i)^2 <= 1-lambda^2 for all i. Summing requires
2(1+lambda^2) <= 6(1-lambda^2), contradicted by lambda=4/5; the difference
is 28/25. This is an exact obstruction to that certificate, not a claim
about every possible analytic proof.

Removing the factor 4/5 from the output of (23) gives a finite dual-polygon
reflection with the R5 obstruction of Section 4. Conversely (23) itself
has the R4 motion of Theorem 2 and the positive Gaussian and ball-volume
comparisons for every set of weights and every individual-radius vector.
The earlier circular theorem preceded by a uniform transverse squeeze
does not suffice: pi kappa (16/25)>2, since pi>3 and kappa>25/24.
No exclusion of every alternative composition is claimed.

## 6. Verification and remaining question

The main positive input is (7)--(15), a uniform geometric cost principle
with an explicit optimal path in the stated form. The exact finite checker
audits the rational fixture, dual facets and extreme rays, every pairwise
deficit, the rank determinant, the scalar-defect obstruction, and the
rational estimates in (21),(24). It also checks universal polynomial
identities used in the metric and calibration calculations and rejects
specified invalid controls. These checks supplement the written proof;
they are not a formal proof of the analytic theorem or its external bridges.

The undamped nonsimplicial full-dual comparison remains undecided for
Gaussian majorisation and for the associated unrestricted ball-volume
question. A contracting-motion obstruction is not a counterexample to
either one. See [SOURCES.md](SOURCES.md) for the source and team audit.
