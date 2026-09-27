# A precise map of the positive geometric classes

27 September 2026. Author consolidation and elementary comparison proofs.
Independent acceptance of a source theorem does not constitute independent
review of this document. This document makes no historical-priority claim
and does not settle unrestricted Gaussian majorisation in R3.

## 1. Common conclusion, different hypotheses

Write gamma_s for the centered Gaussian density of covariance s I3. The
positive source theorems in the table provide, for every bounded Borel law mu
on their respective domains, every s>0, and every a>=0,

    integral (mu*gamma_s-a)_+
        <= integral ((T#mu)*gamma_s-a)_+.                         (1)

They also give, for every finite labeled selection of centers x_i in that
domain and every list of individual radii r_i>=0,

    volume union_i B(Tx_i,r_i) <= volume union_i B(x_i,r_i),
    volume intersection_i B(Tx_i,r_i)
        >= volume intersection_i B(x_i,r_i).                     (2)

Equivalently, (1) gives all defined convex internal-energy comparisons with
U(0)=0. The ball radii in (2) are independent of normal distances or cylindrical
radii. No symmetry assumption on mu or the selected centers is present.

All ambient dimensions below are sufficient dimensions actually constructed,
not assertions of optimality. Reviews and source hashes are pinned in
[SOURCES.json](SOURCES.json); the status snapshot is graph6525.

| Source and graph | Geometric freedom and exact domain obligation | Constructed ambient space in R3; correctness status |
|---|---|---|
| [Common normal profile](../gaussian_radial_contractions/CONVEX_CORES.md), 6331 | Arbitrary closed convex core; one nonnegative 1-Lipschitz profile of normal distance fixing zero; all outward rays | R4; accepted by [6343](../gaussian_convex_core_review_frontier/REVIEW.md) |
| [Directional normal factor](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md), 6418 | Arbitrary closed convex core and selected complete outward rays; nonnegative factor constant on each ray; exact angular pair criterion | R4; accepted by [6424](../gaussian_directional_normal_bundle_review2/REVIEW.md) |
| [Meridian contraction](../gaussian_meridian_contractions/PROOF.md), 6468 | Arbitrary Borel meridian domain, full rotational orbits; arbitrary planar 1-Lipschitz map with target radius between zero and source radius | R5; accepted by [6474](../gaussian_meridian_contractions_review2/REVIEW.md) |
| [Twisted meridian](../gaussian_twisted_meridian_contractions/PROOF.md), 6488 | Full rotational orbits; meridian coupling and spatially varying real phase subject to the displayed pair certificate or uniform budget | R5; accepted by [6496](../gaussian_twisted_meridian_contractions_review2/REVIEW.md) and [6498](../gaussian_twisted_meridian_review/REVIEW.md) |
| [Cylindrical twist](../gaussian_cylindrical_twist_contractions/PROOF.md), R4's 6492 | Full solid disk cylinder; constant transverse scale, arbitrary Lipschitz height-dependent rotation and axial fold; exact endpoint budget | R4; author proof, no independent acceptance located |
| [Affine slices](../gaussian_affine_slice_contractions/PROOF.md), 6514 | Full convex prism; arbitrary Lipschitz planar matrices and translations depending on height, and axial output depending on height alone; endpoint nonexpansiveness | R5; accepted by [6518](../gaussian_affine_slice_contractions_review/REVIEW.md) |
| [Positive rigid screw](../gaussian_tangential_screw_lift/PROOF.md), R4's 6456 | Stationary and moving regions with two cross-pair inequalities; moved region undergoes a proper rigid screw | R5; author proof, no independent acceptance located |

The [axial/matrix-path package](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md)
is preserved as a separate previously assembled portfolio. No blanket
containment of it, or of the cap/flap classes, is inferred from this table.

## 2. Normal distance and normal direction: overlap and closure

Fix a nonempty closed convex C in R3. Let E be a nonempty Borel selection of
its unit outward normal pairs (p,u), and set

    D = C union {p+r u : (p,u) in E, r>0}.

For x outside C this representation is unique, with p=P_C(x). The two
accepted normal families, with this same core and domain, have the forms

    N_rho(p+r u) = p+rho(r)u,
    D_a(p+r u)   = p+r a(u)u,                                  (3)

and fix C. Here rho:[0,infinity)->[0,infinity) is 1-Lipschitz with rho(0)=0.
For D_a the factors satisfy 0<=a(u)<=1 and, for every selected pair u,v,

    (u.v)(1-a(u)a(v))
        <= sqrt((1-a(u)^2)(1-a(v)^2)).                         (4)

The source proves that (4) exactly characterizes nonexpansiveness on complete
rays, and forces parallel rays to share a factor regardless of their base
points. We use that result rather than reinterpret finite tests as (4).

**Proposition 1: exact direct overlap.** If the maps in (3) agree on D, then
there is one a0 in [0,1] such that rho(r)=a0 r for all r>=0 and a(u)=a0
for every selected direction. Conversely these conditions give equality.

**Proof.** Choose one selected ray and compare the values at every r>0.
Uniqueness of its representation gives rho(r)=r a(u). Thus rho is linear
with this fixed slope. Comparing every other ray gives the same slope there.
The value at zero and the interval [0,1] follow from the profile hypotheses.
A common constant factor satisfies (4), since u.v<=1. This proves both
directions. The nonempty-ray and complete-ray assumptions are essential to
this conclusion. It asserts neither equality of different-core representations
nor a statement about maps known only on a finite list. QED.

**Proposition 2: existing composition closure.** Every finite composition of
the maps in (3), all with this same C and D and individually satisfying their
stated hypotheses, preserves each selected normal ray and fixes C. Its profile
on a ray is the corresponding scalar composition, for example

    F_u(r)=rho_k(a_k(u) rho_(k-1)(a_(k-1)(u) ... rho_1(a_1(u)r)...)),
    T(p+r u)=p+F_u(r)u.                                      (5)

It has a simultaneous continuous contracting motion in R4, with finitely
many analytic trajectory pieces, and satisfies (1)-(2).

**Proof.** Each generator sends a nonnegative normal distance to another
nonnegative distance on the same complete ray. All positive distances have
the same projection p. If an image reaches distance zero, all remaining
generators fix p; (5) still gives zero. Thus intermediate images stay in D,
and induction proves (5). Each generator already has its cited R4 motion
starting and ending in the physical R3. Apply the next motion to the previous
endpoint labels and concatenate in the same R4. Every pair distance remains
nonincreasing; the auxiliary coordinate is zero at each join, so the number
of auxiliary coordinates does not accumulate. There are finitely many pieces.

Alternatively, the endpoint consequences follow without any regularity
discussion: intermediate pushforwards are bounded laws, so (1) chains at the
same s and a; (2) chains on the same labeled radii. QED.

This already supplies many profiles depending jointly on r and u. Their
existence is a deduction from accepted generators, not a new normal-family
headline. Proposition 1 does not imply disjointness of the classes generated
by compositions. Equation (5) does not characterize every nonexpansive
direction-and-distance profile. With different domains, each successive image
must belong to the next domain before composition can be used.

More generally, any finite composition of source maps with compatible domains
inherits (1)-(2). When each source construction returns to physical R3 from
R4 or R5, their motions concatenate in R5. This statement does not classify
which arbitrary contractions admit such a factorization.

## 3. Exactly when normal geometry has meridian symmetry

Fix the z-axis, write x=(r u,z) with r>=0 and u in S1, and let Q denote any
rotation about that axis. All statements in this section use this same axis
and the same coordinates at both endpoints.

**Projection fact.** If a nonempty closed convex C is invariant under every Q,
then for x=(r u,z),

    P_C(x)=(s(r,z)u,t(r,z)),       0<=s(r,z)<=r.               (6)

Indeed, uniqueness of the metric projection gives P_C(Qx)=Q P_C(x). At a
fixed height the rotational orbit of any point of C has its filled disk
in C by convexity. A closest point with positive transverse radius must
align its transverse direction with u, since rotating it into that direction
minimizes the distance to x. If its radius exceeded r, shortening it to r
within that disk would strictly reduce distance. At r=0, uniqueness and
rotation invariance force the projection onto the axis. These facts prove (6),
including unbounded, lower-dimensional, and nonsmooth C.

**Proposition 3: inclusion and guarded converse.** Suppose a global
nonexpansive map fixes C and has the normal form

    T(x)=P_C(x)+alpha(x)(x-P_C(x)),  0<=alpha(x)<=1  (x outside C).
                                                                    (7)

If C is rotation invariant and alpha(Qx)=alpha(x), then T is a meridian
map about the chosen axis: T(r u,z)=(rho(r,z)u,zeta(r,z)), with
0<=rho<=r and the meridian map (r,z)->(rho,zeta) 1-Lipschitz. Conversely,
if **Fix(T)=C**, membership in that meridian class is equivalent to these
two rotation-invariance conditions on C and alpha.

**Proof.** For the forward direction use (6). The transverse output radius is

    rho=(1-alpha)s+alpha r,

which lies in [0,r]. Both this radius and the output height are independent
of u. Restricting the given nonexpansiveness to one fixed azimuth proves
the two-dimensional meridian Lipschitz bound. At r=0 there is no azimuth
ambiguity. Thus all hypotheses of source6468 hold on the full half-plane.

For the converse, every such meridian map commutes with Q. Therefore its
fixed-point set is rotation invariant. Under Fix(T)=C this proves invariance
of C and hence of its projection. For x outside C the scalar in (7) is unique:

    alpha(x) = ((T(x)-P_C(x)).(x-P_C(x)))/|x-P_C(x)|^2.

Equivariance of T and P_C and preservation of inner products give
alpha(Qx)=alpha(x). This proves the equivalence. QED.

In particular every common normal profile over a rotation-invariant core is
already a meridian map: alpha=rho(dist(x,C))/dist(x,C). So is every global
admissible directional normal map over such a core when a(Qu)=a(u), and every finite
composition of these rotation-invariant normal generators. These are class
inclusions, without imposing rotational symmetry on the input law.

The fixed-set guard is substantive. For a common profile it holds when
rho(d)<d for every d>0; for a directional map it holds when a(u)<1 for every
outward direction. Without it, the identity map can be written over any core
by taking alpha=1, even when that core has no rotational symmetry. Hence
meridian representability alone cannot recover the originally chosen core.

No converse for arbitrary independent endpoint frames is asserted. Nor does
this section say that every meridian map has any normal representation:
meridian maps can couple radius to axial height and reverse axial order.

## 4. Exact affine-slice intersections on a full cylinder

Fix R>0, a nondegenerate interval I, and the full cylinder

    D_R={ (u,z): u in R2, |u|<=R, z in I }.

Consider an affine-slice map with Lipschitz coefficients

    T(u,z)=(A(z)u+b(z),h(z)).                                (8)

Write J=[[0,-1],[1,0]] and Q_theta=cos(theta)I2+sin(theta)J. Rotation
equivariance means T(Q_theta u,z)=(Q_theta T_perp(u,z),T_z(u,z)) for all
theta and every point of this full cylinder.

**Proposition 4: exact equivariant part.** Map (8) is rotation equivariant
if and only if

    b(z)=0,     A(z)=a(z)I2+c(z)J.                            (9)

It is azimuth preserving with a nonnegative target radius if and only if,
in addition, c(z)=0 and a(z)>=0. Thus among nonexpansive maps (8), the
intersection with the untwisted meridian class in these coordinates is exactly

    T(u,z)=(a(z)u,h(z)),      0<=a(z)<=1.                     (10)

**Proof.** At u=0, equivariance forces b to be fixed by every planar rotation,
so b=0. Since the disk has interior, equivariance then gives A Q_theta=Q_theta A
as a matrix identity. Commutation with J is necessary, and direct multiplication
of a general two-by-two matrix shows it is equivalent to (9). Conversely (9)
commutes with every Q_theta. Applying A to (r,0), with r>0, shows that preserving
its nonnegative ray forces c=0 and a>=0; these conditions also suffice for
every other ray. Nonexpansiveness bounds ||A||=a by one. A nonexpansive map
of form (10) has the required meridian Lipschitz bound by fixing an azimuth,
and the reverse implication is the source6468 distance decomposition. QED.

In complex notation (9) is multiplication by w(z)=a(z)+i c(z). The precise
endpoint contraction test in this equivariant part can be written without
a phase choice. At almost every common differentiability height, if |w|<1,
it is

    h'^2 + R^2 |w'|^2/(1-|w|^2) <= 1.                       (11)

Together with |w(z)|<=1 at every height, the singular alternative when
|w|=1 is

    w'=0,       |h'|<=1.                                    (12)

These conditions are necessary and sufficient for (8)-(9) to be nonexpansive
on the full cylinder. To verify them, let d=A'u. The local deficit matrix is

    [[I2-A^T A, -A^T d],
     [-d^T A,   1-h'^2-|d|^2]].                             (13)

For (9), A^T A=A A^T=|w|^2 I2 and |d|=|w'||u|. If |w|<1, its Schur
complement is 1-h'^2-|d|^2/(1-|w|^2); maximizing |u| over the disk gives
(11). If |w|=1, positivity with a zero upper-left block forces A^T d=0.
Since A is invertible, d=0 for every u, equivalently w'=0; the remaining
condition is (12). Conversely these conditions make (13) positive
semidefinite. Integrate the derivative bound along each segment in the convex
cylinder. On nonhorizontal segments exceptional heights have parameter
measure zero; horizontal segments use |w|<=1. This proves the global statement.
Boundary heights follow by continuity, and no division by zero is used.

Where a Lipschitz real phase representation w=beta exp(i theta) is available,

    |w'|^2=beta'^2+beta^2 theta'^2.                          (14)

For constant beta in (0,1), (11) is exactly R4's cylindrical budget6492.
For general w it is the rotation-equivariant portion of accepted affine-slice6514,
which already supplies the R5 conclusion. Thus (11) is a
classification of an existing theorem's hypotheses, not a new twist theorem.
The R4 construction in6492 retains its sharper ambient bound. The complex
formulation remains meaningful at w=0 without inventing a phase there.

The affine-slice theorem also permits anisotropic, noncommuting, singular,
or orientation-reversing matrices and nonzero b(z), which generally break this
equivariance. Conversely, a meridian map whose output height depends
nontrivially on the radius cannot have form (8) on the same cylinder in the
displayed coordinates. These assertions concern direct representations.
They are not exclusions after arbitrary endpoint frames or compositions.

The reviewed twisted-meridian packet6488 permits nonlinear dependence of both
meridian outputs on radius and height. Its **uniform** theorem requires strict
constants Lip(S)<=g<1 and rho<=q r with 0<q<1, and its stated phase budget;
zero phase by itself does not remove those hypotheses. Its separate pairwise
certificate does recover every untwisted meridian contraction at constant
phase. Neither that uniform budget nor a single interpolation clock is the
endpoint characterization for every equivariant contraction. No further clock
is introduced here.

## 5. What a rigid screw means, and what the comparisons do not show

The positive screw6456 fixes one full-dimensional region and applies a proper
rigid screw to another disjoint region. Its reusable hypotheses are the two
cross-pair inequalities in its Section2. Within each region all distances are
preserved. This differs from the extension on every intervening slice of a
convex solid cylinder required in6492 or6514. The word "screw" alone establishes
no inclusion between these domains or theorems.

R4's positive source also proves that its displacement has nonzero helicity
on the moved region, excluding a direct convex-normal representation in its
displayed frame. That is the credited scope of that comparison; it does not
exclude arbitrary independent endpoint frames or compositions. We do not
extend or reclassify that obstruction here.

R4's [24-site two-body screw obstruction6472](../gaussian_two_body_screw_obstruction/PROOF.md)
has no continuous contracting motion in R5. It rules out a universal R5
motion theorem for finite endpoint-contractive screw matchings. It refutes
neither (1) nor (2), and does not satisfy the whole-prism premise merely
because some endpoint pairs contract. R4's newer
[rigid-block certificate6516](../gaussian_rigid_block_certificate/PROOF.md)
provides a different sufficient finite certificate; it is context, not a
premise of Propositions1-4. Sharp extremal motion and obstruction remain
separate from this positive-class consolidation.

The refresh also found R7's
[composition obstruction6524](../gaussian_screw_primitive_obstruction/PROOF.md).
Its author theorem uses R4's same24-site construction and excludes even endpoint
limits of finite chains mixing arbitrary R5-motion steps with anchored
norm-preserving steps, allowing independent frames and any finite factor count.
Here anchored norm preservation means |x_i-a|=|y_i-b| for some anchors a,b;
it is R8's [6510](../gaussian_norm_preserving_majorisation/PROOF.md), accepted
by [6522](../gaussian_norm_preserving_majorisation_review2/REVIEW.md), and is
different from preserving outward normal rays. The obstruction's topology is
that of labeled endpoint distance matrices; its neighborhood radius is not
effective. Its separate exact law statement requires positive distinct atom
weights. The new obstruction itself is not independently accepted at the
recorded snapshot. It gives a precise credited boundary to using portfolio
composition as a complete route, without supplying an adverse Gaussian hinge.
No additional obstruction classification is attempted here.

For applying the portfolio, record the domain before testing its formulas:
complete outward rays for the directional characterization, full orbits for
the meridian characterization, a full convex prism for the slice theorem,
or the specified rigid-region cross inequalities for the screw construction.
Finite restrictions inherit a valid extension's consequences. Finite pairwise
contractivity alone proves none of these extension hypotheses.

## 6. Historical and logical accounting

The primary antecedents remain credited in their original packets:

- [Bezdek--Connelly, math/0108098v1](https://arxiv.org/pdf/math/0108098v1),
  Lemma1 and Theorem1, supply the classical lifting framework and the
  n+2-dimensional motion-to-ball transfer. Section2 attributes its general
  leapfrog formula to Alexander1985, formula(8). Corollary5 already uses
  a scalar norm-displacement lift for partial dilations.
- [Aishwarya--Li, 2609.07041v2](https://arxiv.org/html/2609.07041v2),
  Theorem1.4(i)(a) and the discussion following Theorem1.5, supply the
  sampled-density comparison and explicitly identify the sufficiency of
  at most two auxiliary Gaussian dimensions for full majorisation.
- [Bezdek--Naszodi, 1701.05074v4](https://arxiv.org/pdf/1701.05074v4),
  Sections1.1-1.2, distinguish uniform and strong coordinate contractions.
  Failure of a single fixed-coordinate representation does not prove failure
  of compositions or of other geometric mechanisms.

The earlier [seven-source priority comparison](../gaussian_angular_ray_contractions/PRIORITY.md)
and its [source record](../gaussian_angular_ray_contractions/PRIORITY_SOURCES.json)
remain the historical assessment for the normal package. The direct primary
text of Alexander1985 was not available in that assessment; the attribution
above is via Bezdek--Connelly. No exhaustive priority or composition-classification
claim is made by this note. Repeating a failed access or keyword search would
not change that boundary.

Propositions1-4 distinguish useful parameter freedoms without treating their
combinations as new discoveries. They clarify when old conclusions already
apply and prevent an apparent new family from being counted twice. Correctness
acceptance, extension breadth, sufficient ambient dimension, and historical
novelty are four separate questions. The current source record answers only
the first three to the scopes expressly stated above.
