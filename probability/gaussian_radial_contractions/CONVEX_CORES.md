# Convex normal bundles: a geometric extension of the radial theorem

Complete author proof, 27 September 2026. Independent correctness and priority
review are pending. This extends [the radial theorem](PROOF.md) from a single
center to every nonempty closed convex core. The original radial source is
preserved. The unrestricted dimension-three question remains open.

## 1. The full convex-core class

Let n>=2 and let C be a nonempty closed convex subset of R^n. It need not
be bounded, have interior, or have a smooth boundary. Let P_C denote its
Euclidean metric projection. For x outside C write

    p=P_C(x),       r=dist(x,C),       u=(x-p)/r.

Let rho:[0,infinity)->[0,infinity) be 1-Lipschitz with rho(0)=0. Define

    T(x)=p+rho(r)u  for x outside C,     T(x)=x  for x in C.       (1)

Thus the same scalar profile acts on every outward normal ray. It can
reverse distance order arbitrarily often, and it need not be differentiable.
It does not vary independently with the base point or normal direction.

**Theorem.** The map (1) is 1-Lipschitz and has an explicit continuous
contracting motion in R^(n+1), with analytic labeled trajectories and
endpoints in the original R^n. Consequently:

* For every bounded Borel probability law mu on R^n, every s>0, and every
  h>=0, with gamma_(n,s)=N(0,sI_n),

      integral (mu*gamma_(n,s)-h)_+
          <= integral ((T#mu)*gamma_(n,s)-h)_+.                  (2)

  These are n-dimensional integrals. There is no symmetry, atom-count,
  weight, or angular-support hypothesis on mu.
* For every finite labeled set of centers x_i and arbitrary individual
  radii a_i>=0,

      vol_n union_i B(Tx_i,a_i) <= vol_n union_i B(x_i,a_i),
      vol_n intersection_i B(Tx_i,a_i)
          >= vol_n intersection_i B(x_i,a_i).                  (3)

In particular both assertions hold in dimension three. Restrictions,
Euclidean isometries, and finite compositions retain the consequences.
The two classical transfer theorems are identified in Section 4.

The singleton case C={c} is exactly the previous radial result about c.
Allowing arbitrary C is a global geometric enlargement, not a restriction
to another arrangement of finitely many radial centers.

## 2. Projection inequalities, including singular cores

The elementary projection characterization is

    (x-p).(z-p)<=0 for all z in C,       p=P_C(x).              (4)

For necessity, differentiate |x-(p+t(z-p))|^2 at t=0 from the right.
For sufficiency, expand |x-z|^2 and use (4). Existence follows by restricting
the distance minimization to a sufficiently large closed ball; uniqueness
follows from strict convexity of the squared norm along segments. Adding
(4) for two projection pairs also gives

    |P_C(x)-P_C(y)|^2 <= (P_C(x)-P_C(y)).(x-y),

so P_C is 1-Lipschitz. These are standard projection facts, recalled to
make the geometric signs and continuity requirements explicit.

For another point y=q+s v outside C, put

    alpha=(p-q).u,       beta=-(p-q).v,       c=u.v.

Taking z=q or z=p in (4) gives

    alpha>=0,       beta>=0,       -1<=c<=1.                  (5)

If x is in C, use p=x, r=0, u=0; similarly for y. Then the corresponding
alpha or beta is zero, the other inequality in (5) remains valid, and the
formulas below still hold since rho(0)=0. C=R^n gives the identity map.

Also P_C(p+b u)=p for every b>=0 when u is an outward normal at p, by
(4). Thus all nonnegative positions on one normal ray have the same
projection, including the images under (1). No choice among multiple
nearest points or a smooth unit normal field is involved.

## 3. Exact distance identity and contracting motion

Put R=rho(r), S=rho(s), and, for 0<=t<=1,

    A_t(r)=(1-t)r+tR,       A_t(s)=(1-t)s+tS.

The inequalities 0<=R<=r and 0<=S<=s follow from rho's assumptions.
Define on the entire domain

    F_t(x)=(p+A_t(r)u, sqrt(t(1-t))(r-R)).                     (6)

For x in C this is (x,0). With the notation above, direct expansion gives

    |F_t(x)-F_t(y)|^2
      =|p-q|^2+2A_t(r)alpha+2A_t(s)beta
         +(1-t)(r-s)^2+t(R-S)^2
         +2A_t(r)A_t(s)(1-c).                                 (7)

The last three terms are the earlier radial identity. The first term is
constant, and the two additional linear terms are nonincreasing by (5).
Every remaining part is nonincreasing for the same explicit reason:
|R-S|<=|r-s|, each A_t is nonnegative and nonincreasing, and 1-c>=0.
Equivalently the exact derivative is

    -2(r-R)alpha-2(s-S)beta+(R-S)^2-(r-s)^2
      -2(1-c)[(r-R)A_t(s)+(s-S)A_t(r)] <= 0.                 (8)

This proves simultaneous contraction for every pair of points, without
restricting their projection points or normal directions. It also proves
the endpoint map T is 1-Lipschitz. All equalities and zero-distance cases
are retained; no ratio between two distances is used in the sign argument.

Use t=sin(theta)^2, 0<=theta<=pi/2. The resulting coordinates are

    (p+(cos(theta)^2 r+sin(theta)^2 R)u,
                        sin(theta)cos(theta)(r-R)).           (9)

They are real analytic in theta. Away from C, continuity in x follows
from continuity of P_C and of rho. At C, the normal component has norm
at most r, and the extra component at most r/2, so both tend to zero.
This proves joint continuity. If the original support is bounded, choosing
any fixed z in C bounds r by |x-z|; (9) and its theta derivative are then
uniformly bounded. Unboundedness or a singular boundary of C creates no
regularity gap in the Gaussian application.

The formula (6) is exactly the classical norm-displacement lift

    ((1-t)x+tT(x), sqrt(t(1-t))|x-T(x)|),

because |x-T(x)|=r-R. It was already used by Bezdek--Connelly in their
Corollary 5. The new step is the convex normal-bundle decomposition (7)
and its uniform sign; we do not claim a new general interpolation formula.

## 4. Gaussian and ball-volume transfer

Pad (9) by one zero coordinate. This gives a continuous contraction in
R^(n+2). Aishwarya--Li, Theorem 1.4(i)(a), orders density values sampled
from the two endpoint Gaussian convolutions in that dimension. Write their
densities as f(x)gamma_(2,s)(z) and g(x)gamma_(2,s)(z), where f and g are
the two n-dimensional densities in (2). If X has density f and Z is an
independent N(0,sI_2), then, for c_s=(2 pi s)^(-1),

    Pr{f(X)gamma_(2,s)(Z)>h c_s}=integral(f-h)_+.               (10)

Indeed |Z|^2/(2s) is exponential of mean one, and conditioning on X gives
f(x)(1-h/f(x))_+. The same identity for g proves (2); at h=0 both sides
equal one. This is the established two-Gaussian-coordinate cancellation,
not a new theorem about marginalizing arbitrary majorisation relations.

For (3), reverse the finite analytic motion (9), pad to R^(n+2), and apply
Bezdek--Connelly, Theorem 1. This yields the comparisons for positive ball
radii and distinct endpoint centers. Repeated source centers can be merged
using the largest radius for the union and smallest for the intersection.
If needed, replace rho by rho_epsilon=(1-epsilon)rho+epsilon r: projection
points are still preserved, so targets with different bases cannot collide;
on one base, distinct directions cannot collide for epsilon>0; and equality
on one ray excludes only one epsilon for a given pair. Thus generic positive
epsilon avoids all target collisions in a finite list. Monotonicity then
keeps the perturbed centers distinct throughout the motion. Along such a sequence
decreasing to zero, continuity of finite ball volumes gives the conclusion.
Zero ball radii follow by a further decreasing-radius limit. The original
Gaussian comparison does not require this finite-configuration perturbation.

The external premises are the two named published transfer results. The
projection geometry and all formulas needed to apply them are proved above.

## 5. New geometric application: reflecting a whole convex collar

Fix a>0 and let K=C+aB be the outer parallel set of C, where B is the
closed Euclidean unit ball. Define the scalar profile

    rho_a(r)=r       for 0<=r<=a,
             2a-r  for a<=r<=2a,
             0     for r>=2a.                                (11)

It is nonnegative, 1-Lipschitz and fixes zero. The resulting global map fixes
K. On its entire outer collar (K+aB) minus K it is

                         T(x)=2P_K(x)-x.                     (12)

To see this, if x=p+r u with r>a, the unique nearest point in K is p+a u.
That point is in K and at distance r-a from x; no nearer point is possible
because dist(.,C) is 1-Lipschitz. Substitution in (12) gives
p+(2a-r)u when r<=2a. Also K+aB=C+2aB. This proves the assertion throughout
the collar, including its two boundary levels. Beyond C+2aB the global
map (11) equals P_C.

**Collar corollary.** For every nonempty closed convex C, every a>0, and
every bounded law or finite list of centers in C+2aB, the reflected
projection 2P_(C+aB)-I satisfies (2) and both inequalities (3).
Ball radii are arbitrary and need not be related to a. Convex cores may
be polytopes with any number of faces, lower-dimensional convex sets, or
bodies with curved boundary. Every normal direction acts simultaneously;
there is no disjoint-cap, normal-hemisphere, finite-center-count or curvature
smoothness condition.

Another global example fixes C+aB and uses rho(r)=a^2/r for r>a, so
all exterior points return into the parallel set along their normal rays.
It is a nonexpansive retraction with all the same Gaussian and ball-volume
consequences. Repeated folds rho(r)=dist(r,2a Z) are also permitted.

This enlarges the single-center package materially. For example let C be
the line segment [-1,1]e_1 and use the last inversion profile with a=1.
The displacement lines at x=-(1/2)e_1+2e_2 and y=(1/2)e_1+2e_2 are distinct
parallel lines. A nontrivial radial map about one point would require that
point to lie on both. Thus this global example is not radial about any
single center. Its rounded core is a capsule rather than a ball.

## 6. Boundary, attribution, and verification

The claim is for a common nonnegative 1-Lipschitz normal-distance profile
and a closed convex core. Signed profiles, direction-dependent profiles,
nonconvex cores, and unrestricted reflected projections onto arbitrary
convex bodies are not asserted. In particular (12) has the precise
parallel-body and collar hypotheses just proved. No new general
Kneser--Poulsen transfer theorem is claimed.

The point-core radial result is a cited special case, with its proof and
checker preserved unchanged. The accepted cap, flap and axial/matrix
packages are not modified. We make no claim excluding all compositions
or rematchings from known positive classes. R4 retains general extremal-map
classification and R7 retains adversarial searches.

[check_convex_core.py](check_convex_core.py) checks the new polynomial
identity and derivative exactly, and tests the full lifted coordinates
and collar formula on rational cube, segment, singleton, halfspace and whole-space
examples. It includes corner normals, different projection points, zero
normal lengths, reversals and collapsed targets. A false normal sign and
a changed identity must be rejected. These are author algebra controls;
the universal convex-core argument remains the written proof.

Primary sources and the provisional priority boundary are in
[SOURCES.md](SOURCES.md). The old lift, projection facts and transfers are
credited. The claimed advance is their convex-normal sign principle and
the whole-collar Gaussian/Kneser--Poulsen consequence, not a priority claim
based on the absence of search hits.
