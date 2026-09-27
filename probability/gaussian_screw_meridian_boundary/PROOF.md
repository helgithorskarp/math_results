# A sharp boundary between rigid screws and meridian extensions

Author proof, 27 September 2026. Independent acceptance and historical
priority are pending. Full Gaussian majorisation in R3 remains open.
This is an endpoint classification and strict separation, not another
positive motion schedule or an internal review of earlier constructions.

## 1. The finite endpoint question

Let two labelled finite groups A,B each affinely span R3. Their endpoint
maps are Euclidean isometries F_A,F_B, and the combined labelled matching
is 1-Lipschitz. Assume the **relative** isometry F_A^{-1}F_B is proper.
Compose all targets with F_A^{-1}. Thus, without losing any freedom in
independent endpoint frames, the normalized matching is

    T(a)=a (a in A),            T(b)=Qb+t (b in B),
    Q in SO(3).                                                   (1)

We ask whether this finite matching is a restriction of a 1-Lipschitz map
on a rotationally invariant domain which intertwines rotations about
some source and target lines. The two lines, their origins, orientations
and endpoint frames are unrestricted. The domain must contain the full
rotation orbit of every original site. A global extension to R3 is an
equivalent formulation in the classification below.

Call this an **equivariant completion**. It is the maximal rotational
endpoint class underlying twisted meridian formulas

    (r exp(i theta),z) ->
      (rho(r,z) exp(i(theta+psi(r,z))), zeta(r,z)).              (2)

We impose no uniform phase derivative or strict radial/meridian margin.
The weak radial bound rho<=r follows from contraction applied to opposite
points of the same orbit, so it need not be an additional hypothesis.
Thus exclusion here also excludes every sufficiently regular meridian or
twisted-meridian restriction. An **untwisted** completion has psi=0 in
some fixed endpoint frames. This does not include R6's general anisotropic
affine-slice class, which need not have rotational equivariance.

For Q!=I define the rationally expressible quantities

    P = orthogonal projection onto ker(I-Q),
    v = Pt,             h^2=|v|^2,
    c = (I-Q+P)^(-1)(I-P)t,
    L = c+range(P),     chi = 3-tr(Q)>0,
    r_x^2 = |(I-P)(x-c)|^2,
    ell_ab = 2v.(a-b)-h^2.                                   (3)

Here L is the usual screw axis and v is the axial displacement. The axis
point c is perpendicular to its direction. Since Q is a nonidentity
proper rotation, ker(I-Q) has dimension one and I-Q+P is invertible.
For its rotation angle alpha, `chi=4 sin^2(alpha/2)`; alpha itself is not
needed for the finite decision.

**Theorem 1 (all-frame endpoint classification).**

1. If Q=I, every endpoint-contractive matching (1) has an untwisted
   meridian completion. For t!=0 every possible rotation axis is parallel
   to t; its transverse position is arbitrary.
2. If Q!=I, every equivariant completion must use the **same** input and
   output line L after normalization. A completion exists if and only if
   every cross pair satisfies

       ell_ab >= 0,       ell_ab^2 >= 4 chi r_a^2 r_b^2.        (4)

   Equivalently, `ell_ab>=2 sqrt(chi) r_a r_b`. Whenever (4) holds,
   there is a global equivariant 1-Lipschitz extension to R3.
3. No Q!=I matching has an untwisted meridian completion in any independent
   endpoint frames. In particular, for a nontrivial rotation with zero
   pitch v=0, **no equivariant completion exists at all** under the
   full-dimensional group hypotheses.

This is a necessary-and-sufficient test for the stated extension question,
not a sufficient phase clock. It does not decide Gaussian majorisation
or whether an arbitrary matching admits an R5 contracting motion.

## 2. Preserved full-dimensional groups pin the axes

An infinitesimal rotation about an oriented line has the affine field

    V(x)=u cross (x-c),              |u|=1.                   (5)

Suppose a 1-Lipschitz equivariant map on full source orbits agrees with
an isometry F(x)=Rx+s on a full-dimensional finite group. Let V,W be
the source and target rotation fields. For any two labels x_i,x_j in
that group, rotate only x_i. The squared-distance loss

    g(theta)=|Rot_source(theta)x_i-x_j|^2
             -|Rot_target(theta)F(x_i)-F(x_j)|^2

is nonnegative for positive and negative theta and vanishes at zero.
Therefore g'(0)=0, which is

    (x_i-x_j).(V(x_i)-R^T W(F(x_i)))=0.                     (6)

For a fixed i the differences x_i-x_j span R3. Hence the vector in
parentheses is zero. Both fields are affine; their equality on four
affinely independent sites implies

    W(F(x))=R V(x)                  for every x in R3.       (7)

No differentiability of the unknown extension was assumed: its values
along the prescribed rotation orbits are smooth by equivariance alone.
Nor were unsampled interior sites inserted into the finite input.

Apply (7) to the normalized stationary group A. It gives W=V, so the two
oriented rotation fields, and thus their axes, agree. Applying (7) to B
then says the rigid isometry Qx+t commutes with this rotation group. For
proper Q, the identity `Q(u cross x)=(Qu) cross (Qx)` gives

    Qu=u,                 (I-Q)c-t parallel u.              (8)

When Q!=I this forces the unique line (3). When Q=I,t!=0 it forces
u parallel t, with no condition on the transverse axis position. These
are exactly the axes claimed in Theorem1. This argument already allowed
independent endpoint isometries, including reflections: they merely
conjugate the two oriented rotation fields before normalization.

## 3. The sharp orbit inequality and sufficiency

Assume Q!=I and use its forced axis L. Relative to L, write
a=c+u_a+z_a e and b=c+u_b+z_b e, where e is a unit axis vector,
v=h e, and u_a,u_b are perpendicular to e. Equation(1) has transverse
parts u_a and Qu_b and axial parts z_a and z_b+h. After independently
rotating the two source sites about L, their loss is

    ell_ab + 2 u_a . (Q-I) Rot(theta)u_b.                   (9)

Only the relative azimuth theta matters. The amplitude of its second
term is `2 r_a |(Q-I)u_b|=2 sqrt(chi) r_a r_b`. Thus the minimum over
all azimuths is exactly

    ell_ab - 2 sqrt(chi) r_a r_b.                            (10)

Nonnegativity of (10) is precisely (4), with the sign check before
squaring. Within each group the isometry commutes with rotation about L,
so every within-group orbit distance is preserved. Consequently (4)
defines a 1-Lipschitz equivariant map on the union of all these orbits.
If two labels produce the same source orbit point, their target points
coincide by the same distance inequality; the definition is well defined.

For completeness, translate a point of L to the origin and take any
global Kirszbraun extension G of this orbit map. Average

    G_bar(x) = (1/(2pi)) integral_0^(2pi)
                   Rot(-theta) G(Rot(theta)x) dtheta.       (11)

It is 1-Lipschitz by the triangle inequality, agrees with the orbit map,
and is equivariant by change of variable. The integrand is continuous
for each x, and rotations form a compact group. Equivariant Lipschitz
extension is established prior work; a more general theorem is
Cavagnari--Savare--Sodini, Theorem2.13 of arXiv:2305.04678v2.
Neither (11) nor Kirszbraun extension is claimed as new.

If Q=I and t!=0, choose e=t/|t|. Write x=u+ze. Endpoint contraction
for a cross pair is just

    2|t|(z_a-z_b)-|t|^2 >=0.                                (12)

The scalar assignments z_a->z_a and z_b->z_b+|t| therefore form a
well-defined 1-Lipschitz map on the finite set of axial heights. Extend
it to a 1-Lipschitz f on R. Then `(u,z)->(u,f(z))` is a global
untwisted completion about any line parallel to t. The identity case
is immediate.

For Q!=I, an untwisted representation would use the forced line L. Its
fixed transverse identification between endpoint planes must be identity:
the fixed group A has transverse projections spanning a plane. On B it
would then require Qu_b=u_b on all sites, impossible because B also has
full-dimensional affine span. This proves the untwisted assertion. If
v=0, (10) is strictly negative for any cross pair with r_a,r_b>0; such
a pair exists because both groups span R3. This finishes Theorem1.

## 4. Other endpoint freedoms: exact classification

These statements clarify which upstream criteria can remove the screw
case; they do not reprove the Gaussian theorems behind those criteria.

**Norm anchors.** There exist source and target anchors p,q with
`|x-p|=|T(x)-q|` on all labels if and only if Qx+t has a fixed point.
Indeed, the fixed group A makes
`2(q-p).a+|p|^2-|q|^2=0` on a full-dimensional set, so p=q.
The corresponding equality on B then forces `Qp+t=p`, and that
condition is also sufficient. Thus, for Q!=I, anchors exist exactly
when h^2=0 and are precisely the points of L. A nonzero pure translation
has no anchors. This locates the applicability of R8's norm-preserving
theorem6510; nonzero pitch cannot be removed by choosing better anchors.

**Scalar defect.** The upstream criterion asks for unit vectors e,f with

    Delta_ij >= [e.(x_i-x_j)-f.(T(x_i)-T(x_j))]^2.           (13)

Preserved full-dimensional groups force e=f and e=Q^T f. If Q!=I,
e=f is therefore one of the two unit axis directions. Every cross right
side in (13) is h^2. Hence the scalar criterion is equivalent to

    min_(a in A,b in B) Delta_ab >= h^2.                    (14)

For Q=I choose e=f perpendicular to t (any unit e if t=0), and it
always holds. This includes independent endpoint frames; normalization
simply transports the two unit vectors.

**Paired affine rank.** Differences in A span the diagonal three-space.
Modulo this subspace, B contributes range(Q-I) and the translation t.
Thus the affine span of `(x,T(x))` has dimension

    3 + rank[Q-I | t].                                      (15)

The complete proper-relative-motion table is:

| Relative motion | Paired rank | Norm anchors | Scalar criterion | Equivariant completion |
| --- | --- | --- | --- | --- |
| Identity | 3 | Every point | Always | Untwisted, any axis |
| Nonzero translation | 4 | None | Always | Untwisted, axis parallel to translation |
| Nonidentity rotation, zero pitch | 5 | Exactly its axis | Always | Impossible |
| Nonidentity rotation, nonzero pitch | 6 | None | Exactly (14) | Exactly (4), unique screw axis |

All rows assume the original labelled endpoint matching is a contraction
and both groups affinely span R3. Improper relative isometries, lower-rank
groups, label permutations and changes of weights are outside this table.

## 5. Strict separation using the two preserved screw controls

### 5.1 The R5-positive screw has no equivariant completion in any frames

Use the eight labels of the existing positive construction6456:

    A={(0,0,3/2),(1,0,3/2),(0,1,3/2),(0,0,5/2)},
    B={(0,0,0),(1,0,0),(0,1,0),(0,0,1)},
    Q(x,y,z)=(-y,x,z),              t=(0,0,1).

That [source proof](../gaussian_tangential_screw_lift/PROOF.md) supplies
an analytic R5 contraction; this pass does not replay or modify it.
Both groups span R3, so Theorem1 forces the z-axis for any putative
equivariant completion. For a=(0,1,3/2), b=(1,0,0),

    ell_ab=2,      r_a^2=r_b^2=1,      chi=2,
    ell_ab^2-4 chi r_a^2 r_b^2 = -4.                        (16)

There is even a rational adverse orbit pair. Rotate a to
`a'=(3/5,-4/5,3/2)` and keep b fixed. Equivariance would require a'
to stay fixed, whereas b maps to (0,1,1). Their squared distances are

    |a'-b|^2=61/20,       |a'-T(b)|^2=77/20.                 (17)

The exact loss is -4/5. No alternative choice of axes or endpoint frames
repairs this, by Section2. Therefore this known R5-positive matching is
outside the entire equivariant meridian endpoint class, including all
untwisted/twisted meridian subclasses on full rotational domains.
It is a strict all-frame separation, stronger than the earlier displayed-
frame helicity observation. It does not exclude anisotropic affine-slice
representations or compositions of geometric classes.

### 5.2 The R5-obstructed screw does have an equivariant completion

The preserved 24-site construction6472 is a restriction of the two surfaces

    a(v)=(v,(1+|v|^2)/2),        b(u)=(u,-|u|^2),
    T(a)=a,                     T(b)=(Ju,1-|u|^2),
    J(x,y)=(-y,x).

Here the forced axis is again the z-axis, with chi=2 and h^2=1. For
every real u,v, not just sampled points,

    ell=|v|^2+2|u|^2,
    ell^2-8|v|^2|u|^2=(|v|^2-2|u|^2)^2>=0.                (18)

Thus it has an equivariant completion, even a global one by (11).
The existing [author obstruction proof6472](../gaussian_two_body_screw_obstruction/PROOF.md)
shows that its prescribed finite matching has no continuous R5
contraction; its minimum possible motion dimension is six. This inherited
motion claim remains a separately identified proof dependency, not a new
verification or independent acceptance of that source.

Together, (16)--(18) and the two existing motion results prove that
equivariant endpoint completion and R5 motion availability are incomparable
on proper two-rigid-group contractions. In particular, arbitrary azimuth
freedom in a meridian formula is not equivalent to the two auxiliary
coordinates needed by the Gaussian motion transfer.

Both controls have nonzero pitch, paired rank six, no norm anchors and
failure of the scalar criterion. These facts identify the surviving
geometric freedom; they do not produce an adverse Gaussian hinge. R1's
accepted spherical theorem already signs their eventual finite-variance
range. No unrestricted all-variance conclusion is asserted here.

## 6. Exact checking and scope

The checker fits the two rigid endpoint maps from four independent anchors,
verifies every labelled endpoint, normalizes the first group, and computes
P,c,v,chi with rational arithmetic. It checks (4), (14), norm-anchor
existence and paired rank. Independently, it reconstructs the sine/cosine
coefficients of each orbit loss and verifies their amplitude identity.
The within-group orbit-derivative equations have rank10 on the two screw
controls; their two-dimensional affine-generator nullspace is reduced to
the unique rotation axis by requiring its infinitesimal field to have no
translation along its own axis.

Only the new endpoint/orbit calculations are run on the preserved controls.
No old R5 motion or no-lift certificate is rerun. Public dependency hashes
pin those proof sources and the compact 24-site fixture. Handwritten
rigidity, the exact minimization over a circle and the classical extension
theorem discharge the universal quantifiers; finite checks are not a
formalization or independent review. Historical priority of this precise
classification and separation is not established by the bounded search.
