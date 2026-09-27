# Radial contractions and Gaussian majorisation

Complete author proof, 27 September 2026. Independent correctness and
priority review are pending. The full dimension-three conjecture remains
open. The norm-displacement lift and both transfer theorems below are
classical inputs; the contribution is their uniform application to the
entire class of direction-preserving radial contractions, including
arbitrary reversals of radial order.

## 1. Statement

Let n>=2 and let rho:[0,infinity)->[0,infinity) be 1-Lipschitz with rho(0)=0.
Define on R^n

    T(0)=0,                 T(r u)=rho(r) u,   |u|=1, r>0.        (1)

In particular 0<=rho(r)<=r. No monotonicity, differentiability, or finite
number of turning points is assumed for rho.

**Theorem.** The map (1) has a continuous contracting motion in R^(n+1),
with analytic trajectories and endpoints in R^n x {0}. Consequently:

1. For every bounded Borel probability measure mu on R^n, every s>0,
   and every h>=0, writing gamma_(n,s) for N(0,s I_n),

       integral (mu*gamma_(n,s)-h)_+
           <= integral ((T#mu)*gamma_(n,s)-h)_+.                 (2)

   All integrals in (2) are over R^n. Thus the source density is majorised
   by the target density. No symmetry of mu, restriction on its angular
   support, or condition on its atom weights is imposed.

2. For all N>=1, all labeled centers x_1,...,x_N in R^n, and all individual
   ball radii a_i>=0,

       vol_n union_i B(Tx_i,a_i) <= vol_n union_i B(x_i,a_i),
       vol_n intersection_i B(Tx_i,a_i)
           >= vol_n intersection_i B(x_i,a_i).                  (3)

In particular (2)--(3) hold in dimension three. The radius profile rho
acts on center locations; it does not change the ball radii a_i.
Translations of the center of (1), separate endpoint Euclidean isometries,
restrictions to arbitrary subsets, and finite compositions preserve the
conclusions. For compositions, concatenate the lifted motions (with any
needed rigid endpoint motion), or apply (2)--(3) successively. The bounded
measure hypothesis is preserved by these Lipschitz maps.

This is exactly the full class of direction-preserving radial 1-Lipschitz
self-maps fixing zero: necessity of the condition on rho follows by testing
two points on one ray and zero. Sufficiency also follows directly from
the distance decomposition in the next section. Signed radial profiles,
or profiles depending on direction, are outside the theorem as stated.

## 2. The motion and its sign

For 0<=t<=1 put

    A_t(r)=(1-t)r+t rho(r),       d(r)=r-rho(r)>=0,
    F_t(r u)=(A_t(r)u, sqrt(t(1-t)) d(r)),     F_t(0)=0.      (4)

Fix radii r,q, abbreviate R=rho(r), Q=rho(q), and write c=u.v in [-1,1].
Expanding the distance gives the exact identity

    |F_t(r u)-F_t(q v)|^2
       =(1-t)(r-q)^2+t(R-Q)^2
           +2 A_t(r) A_t(q)(1-c).                              (5)

Indeed the difference of the extra coordinates contributes
t(1-t)[(r-R)-(q-Q)]^2, which converts the squared difference of A_t(r)
and A_t(q) into the first two terms of (5).

The first part of (5) is nonincreasing because |R-Q|<=|r-q|.
Each A_t is nonnegative and nonincreasing, so its product is also
nonincreasing. Equivalently, the exact derivative is

    (R-Q)^2-(r-q)^2
       -2(1-c)[(r-R)A_t(q)+(q-Q)A_t(r)] <= 0.                 (6)

This proves simultaneous contraction for every pair. If either point is
zero, choose any direction for it; every term containing its radius is
zero, so the same identity applies. Equal radii, unchanged radii,
coincident points, and collapsed target radii also need no division or
strict inequality. At t=0 and t=1 the extra coordinate vanishes, giving
the asserted endpoints.

Set t=sin(theta)^2 for 0<=theta<=pi/2. Then (4) becomes

    ( (cos(theta)^2 r+sin(theta)^2 rho(r))u,
       sin(theta)cos(theta)(r-rho(r)) ).                        (7)

Every labeled trajectory is real analytic through both endpoints, even
if rho is not differentiable in r. Joint continuity follows from the
Lipschitz property of rho and |A_t(r)|<=r at the origin. On a bounded
support the trajectories and their theta derivatives are uniformly
bounded. This is one motion of the entire domain, not a different choice
for each finite collection of atoms.

At t=1, (5) also verifies directly that T is 1-Lipschitz, since
(R-Q)^2<=(r-q)^2 and RQ<=rq.

## 3. Transfer to internal energies and ball volumes

Pad (7) by one zero coordinate to a continuous contraction in R^(n+2).
Apply Aishwarya--Li, Theorem 1.4(i)(a), to the lifted measure. At the two
endpoints, its Gaussian densities are f(x)gamma_(2,s)(z) and
g(x)gamma_(2,s)(z), where f=mu*gamma_(n,s) and g=(T#mu)*gamma_(n,s).
That theorem orders the density values sampled from the two densities.

Let X have density f and let Z independently have density gamma_(2,s).
With C=(2 pi s)^(-1), the variable |Z|^2/(2s) is exponential of mean one,
so for every h>0,

    Pr{ f(X) gamma_(2,s)(Z)>h C }
       =integral f(x)(1-h/f(x))_+ dx
       =integral (f-h)_+ dx.                                   (8)

The same identity holds for g. The sampled-density comparison proves (2).
For h=0 both sides are one. This is the same two-coordinate cancellation
used in the earlier team [scalar-defect proof](../gaussian_majorisation_scalar_defect/PROOF.md),
and is not a new transfer theorem. It gives the usual convex internal-energy
comparisons whenever their integrals are defined, by the hinge criterion
for majorisation.

For any finite list of centers, reverse the analytic motion (7), pad to
R^(n+2), and apply Bezdek--Connelly, Theorem 1, to this expansion. It gives
both inequalities in (3) for positive a_i. Zero radii follow by continuity
as a_i+epsilon decreases to a_i. Repeated source centers can be merged,
retaining the largest radius for the union and the smallest for the
intersection. To remove target collisions if necessary, replace rho(r) by
(1-epsilon)rho(r)+epsilon r. For a fixed finite list, all but finitely many
positive epsilon give distinct targets: different directions cannot collide,
and an equality on one ray is a nonconstant affine equation in epsilon.
Apply the theorem along such a sequence tending to zero and use continuity
of finite ball-union and ball-intersection volumes in their centers. In (7)
distinct source labels are distinct at all interior times: if (5) vanishes
there, both the source radial difference and angular term must vanish.
Thus no interior collision needs a separate smoothness argument.

The external inputs are precisely the sampled-density comparison, the
elementary Gaussian identity (8), and the established ball-volume transfer.
They do not assume the still-open full-dimensional endpoint conjecture.

## 4. Breadth and two model profiles

**Inversion fold.** For any b>0 take

    rho_b(r)=r             for 0<=r<=b,
             b^2/r        for r>=b.                            (9)

Each branch is 1-Lipschitz and they agree at b, so the joined function is
1-Lipschitz. The map fixes the entire ball of radius b and sends every
exterior sphere to an interior sphere with reversed radius order. There
is no restriction on how mass is distributed on those spheres. Formula
(3) applies to arbitrary finite mixtures of interior and exterior centers
and arbitrary, unrelated ball radii.

**Repeated folds.** The function rho(r)=dist(r,2 Z) on [0,infinity) is
nonnegative, 1-Lipschitz, and fixes zero. It repeatedly rises from zero to
one and falls to zero. The same single motion handles any number of these
folds. These two examples illustrate the general profile theorem; neither
is an additional hypothesis on it.

For (9), straight interpolation in the original space does not suffice.
For example r=2 and q=3 on one ray at b=1 have reversed target order, and
their straight-interpolated distance increases near its final endpoint.
The extra coordinate in (4) exactly removes this radial crossing defect.

## 5. Relation to existing sufficient classes

**The lift is classical.** Bezdek--Connelly's Corollary 5 already uses

    ((1-t)x+t y, sqrt(t(1-t)) |x-y|).                          (10)

It treats an expansive partial dilation by one common positive factor;
reversing its direction gives the corresponding contraction class.
For radial inward motion |x-Tx|=r-rho(r), so (4) is exactly (10).
The new deduction claimed here is the uniform sign (5)--(6) for *every*
nonnegative scalar 1-Lipschitz profile, not a new interpolation formula.
The family permits a continuum of distinct dilation factors and reversals
of radial order. It is not asserted to contain every partial-dilation
configuration covered by that corollary.

**An exact finite benchmark.** Set b=1 and take the ten sites

    0,  e_i, (3/2)e_i, 2e_i   (i=1,2,3).                      (11)

Their respective targets are 0, e_i, (2/3)e_i, (1/2)e_i. The paired
vectors (x,Tx) span R^6: for each i the first two nonzero columns on that
axis have determinant 2/3-3/2=-5/6. Displacements span R^3. Thus the
paired-rank-five and two-dimensional-displacement criteria do not apply
directly. There are three distinct radial factors 1,4/9,1/4, so this is
not a single partial common dilation about the displayed center.
Nor is it a uniform contraction: a source separation is 1/2, while a
target separation is sqrt(2).

It also fails the team's scalar-defect condition for every choice of its
two unit vectors e,f. The fixed root 0,e_1,e_2,e_3 forces e=f. For the
pair e_i,(3/2)e_i, the squared-distance drop is 1/4-1/9=5/36. Writing
alpha_i=e.e_i, the defect square is (5/6)^2 alpha_i^2. Therefore that
condition would force alpha_i^2<=1/5 for each i, contradicting |e|=1.
Separate endpoint isometries
are already allowed in that criterion, so they cannot fix this failure.

The full inversion-fold map is not a strong coordinate contraction in any
separate orthonormal input/output coordinates. Such a condition would make
each output coordinate depend only on the corresponding input coordinate.
On the fixed open unit ball the derivative is I; hence the two bases must
agree up to corresponding signs. Outside the ball,

    DT(r u)=r^(-2)(I-2 u u^T).                                (12)

For simultaneous diagonality the unique negative eigendirection u would
have to be one of a fixed list of coordinate axes, for every unit u. This
is impossible when n>=2. This global separation does not assert that the
particular ten-site benchmark fails every rotated strong-coordinate test.

**Team boundary.** The base cap and axial constructions concern fixed
piecewise orthogonal cluster maps; the closed orthocentric flap result is
a finite selector family. Here the map can vary nonlinearly throughout an
open annulus, on all directions and at arbitrarily many radial scales.
It is not one of those displayed maps. We do not exclude factorizations,
limits, rematchings, or indirect deductions using combinations of existing
classes. This is a complementary class theorem, not a classification of
extremal maps, an extension of the closed flap family, or a counterexample
to Gaussian majorisation. Researcher 4's extremal-map and researcher 7's
adversarial frontiers remain separate.

## 6. Correctness, priority, and reproducibility

The proof of the whole class is (5)--(8) and the two cited transfer
theorems. The exact standard-library checker expands the polynomial
identities, verifies the rational benchmark and its rank/defect calculations,
checks boundary profiles, and deliberately rejects false scalar hypotheses.
It does not certify prior-literature completeness, replace the analytic
proof, or constitute independent review.

The full radial-profile application was not found in the targeted primary
sources listed in [SOURCES.md](SOURCES.md). Its priority is provisional.
The formula (10), Gaussian transfer, and Kneser--Poulsen transfer are
explicitly credited. Neither a new general transfer theorem nor a solution
of the unrestricted R^3 problem is claimed.
