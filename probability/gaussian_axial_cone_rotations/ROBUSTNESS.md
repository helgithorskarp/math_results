# Uniform nonlinear robustness of the axial motion

Complete author proof, 26 September 2026; independent mathematical review is
pending. This is a robustness extension of the existing axial result, not a
new cone threshold. It makes two facts explicit:

1. Controlled nonlinear distortions of the entire source and target domains
   preserve a contracting motion after a reserved amount of target scaling.
   The same condition works for every bounded law, every Gaussian variance
   and threshold, and every assignment of individual ball radii.
2. A fixed neighborhood of freely perturbed versions of the existing
   25-point matching has a four-dimensional motion but no three-dimensional
   motion, even after independent endpoint rigid alignments. The neighborhood
   also has paired affine rank six and fails the scalar-defect criterion.

The linear-segment criterion below is the classical firmly nonexpansive
condition. Concatenation, elementary singular-value estimates and the
Gaussian/Kneser--Poulsen transfer theorems are not claimed new. The additional
geometric consequence is a quantitative neighborhood of the axial examples,
with unrestricted weights and radii and without the original exact cone,
plane, or rigid-cluster equalities. The full R3 question remains open.

## 1. A uniform deformation lemma

Let D be a subset of R3 and T:D -> R3 admit a continuous contracting motion
F_t in R^m, m>=3, with F_0(x)=(x,0) and F_1(x)=(T(x),0). Suppose

    S(x)=x+e(x)                  on D,       Lip(e)<=epsilon<1,
    V(y)=lambda*y+g(y)           on T(D),    Lip(g)<=eta,

where lambda>0. Choose a number r satisfying

    0<r<=1-epsilon,       0<=lambda-eta<=lambda+eta<=r.       (R1)

Then S is injective, with inverse Lipschitz constant at most
1/(1-epsilon), and

    T_tilde = V o T o S^(-1) : S(D) -> R3                   (R2)

admits a contracting motion in the same R^m. Its Lipschitz constant is at
most (lambda+eta)/(1-epsilon). The error maps need not be differentiable,
linear, symmetric, or zero at the origin. The map g is defined on the target
points themselves, so it must respect any collisions of T.

**Proof.** A pair of vectors u,v has a linearly interpolated difference
w_t=(1-t)u+tv. Since

    (1/2) d|w_t|^2/dt = v.(v-u) - (1-t)|v-u|^2,

the segment contracts exactly when v.(v-u)<=0. For a map F this is
|F(x)-F(y)|^2 <= (F(x)-F(y)).(x-y), the firmly nonexpansive condition;
see [Bauschke--Wang, Definition 2.1 and Fact 2.2](https://cmps-people.ok.ubc.ca/bauschke/Research/c10.pdf).
The direct pairwise identity works on arbitrary subsets, without convexity
or a global extension assumption.

Concatenate three motions, parametrizing each on its own time interval:

    S(x)  --->  r*x  --->  r*T(x)  --->  V(T(x)).            (R3)

The middle motion is r*F_t. For the first segment, put a=x-y and
b=e(x)-e(y). Its endpoint test is

    (ra).(ra-a-b) <= r(r-1+epsilon)|a|^2 <= 0.

For the last segment, put a=T(x)-T(y), b=g(T(x))-g(T(y)). If a=0, then
b=0. Otherwise normalize |a|=1; its endpoint test is

    |lambda*a+b|^2-r*(lambda*a+b).a
       <= lambda^2-r*lambda+eta^2+|2*lambda-r|*eta
        = max_{sign=+/-1} (lambda+sign*eta)
                              *(lambda+sign*eta-r) <= 0.    (R4)

Both scalar factors lambda+/-eta lie in [0,r] by (R1). All pair distances
therefore decrease on every segment of (R3). Continuity and the endpoint
statements follow directly. The inverse bound follows from
|S(x)-S(y)|>=(1-epsilon)|x-y|. The Lipschitz bound in the statement follows
by composition. QED.

An equivalent way to choose the parameters is

    eta<=lambda,       epsilon+eta+lambda<=1,
    lambda+eta<=r<=1-epsilon.

Equality is permitted. This sufficient reserve is not an optimal robustness
constant for arbitrary contracting motions. At lambda=1 it allows only
constant error maps; an undamped nonlinear neighborhood is not asserted.
Only spatial Lipschitz variation costs reserve: translations are free.

If every finite restriction of F_t can be chosen piecewise analytic in
time, the same is true of (R3). Spatial regularity of e and g does not enter:
their values at each fixed label are constant during the affine segments.

## 2. Consequences for the full axial domains

Take D=C(P) union (-C(Q)) and T from [PROOF.md](PROOF.md), under its
product-perimeter condition per W(P,Q)<=4. The deformation lemma gives
an R4 motion for (R2), on the entire distorted domain S(D).

For every bounded Borel probability measure rho on S(D), every s>0 and
every h>=0,

    integral (rho*gamma_(3,s)-h)_+
       <= integral ((T_tilde#rho)*gamma_(3,s)-h)_+.          (R5)

There are no restrictions on atom counts, weights, or the distribution
inside either distorted cone. Pullback by S^(-1) preserves bounded support.
Pad the motion into R5 and apply exactly the density-value sampling argument
in PROOF Section 3. This proves (R5), and hence the full comparison of
convex internal energies whenever defined. The Gaussian remains isotropic
in the original Euclidean metric; no covariance transformation is used.

For every finite set of prescribed labels z_i in S(D), and every choice
of individual radii R_i>=0, the same geometric condition gives

    volume union_i B(T_tilde(z_i),R_i)
       <= volume union_i B(z_i,R_i),
    volume intersection_i B(T_tilde(z_i),R_i)
       >= volume intersection_i B(z_i,R_i).                (R6)

Use the finite piecewise analytic axial restriction in PROOF Section 3,
concatenate the affine pieces, and apply the credited
[Bezdek--Connelly Theorem 1](https://arxiv.org/pdf/math/0108098) in R5.
The condition and motion do not depend on the radii. Compact equal-radius
neighborhoods consequently compare at every radius as well.

For example, on a circular domain with pq<=2/pi, the global maps

    S(x1,x2,z) = (x1+epsilon*sin(z), x2, z),
    V(y1,y2,y3) = (lambda*y1, lambda*y2,
                   lambda*y3+eta*sin(y1))

satisfy the stated Lipschitz bounds. Thus (R5)--(R6) apply whenever (R1)
holds. This illustrates arbitrary nonlinear distortions of whole domains;
it is not a separate theorem for a trigonometric family. The ordinary
sinusoidal derivative bound suffices, and no numerical sine evaluation is
part of the certificate below.

## 3. An explicit neighborhood with all endpoint coordinates free

Use the original 25-point fixture, in the order

    X=(0,A,-B),       Y=(0,A,B),
    A={(p*d,1):d in D12},  B={(q*d,1):d in D12},
    p=3/4, q=4/5,

where D12 is PROOF equation (20). Let

    lambda=19/20,       delta=1/2000.                       (R7)

**Theorem R2.** Independently choose all 50 endpoint positions X'_i,Y'_i
subject only to

    |X'_i-X_i|<=delta,       |Y'_i-lambda*Y_i|<=delta.        (R8)

Then the prescribed map X'_i -> Y'_i is a strict contraction admitting
a piecewise analytic R4 motion. It satisfies every Gaussian hinge, for
every choice of probability weights and every s>0, and both ball-volume
inequalities for every assignment of individual radii. Nevertheless:

- no continuous contracting motion in R3 exists, even after independent
  rigid alignments of the two endpoint configurations;
- the paired affine rank is six;
- no independently aligned scalar-defect unit-vector certificate exists.

The strict interior of (R8) is an open subset of the 150-dimensional space
of labeled endpoint coordinates. The anchor may move; neither cluster must
remain planar or rigid. The constants are uniform over that whole
neighborhood and over all weights, variances, thresholds and ball radii.
They are deliberately conservative, not an optimization claim.

**Positive proof.** Directly checking all 300 reference pairs gives

    min_(i<j) |X_i-X_j|^2 = 9/200 > (1/5)^2,
    min_(i<j) |Y_i-Y_j|^2 = 1/400 = (1/20)^2.               (R9)

Define e(X_i)=X'_i-X_i and g(Y_i)=Y'_i-lambda*Y_i. Then

    Lip(e)<=2*delta/(1/5)=1/200=epsilon,
    Lip(g)<=2*delta/(1/20)=1/50=eta.

Apply Section 1 with r=49/50. The first endpoint test has upper bound
-147/10000 times |X_i-X_j|^2, and the last has upper bound
-97/10000 times |Y_i-Y_j|^2. The distortion reserve is strictly positive.
The whole endpoint map has Lipschitz constant at most

    (lambda+eta)/(1-epsilon)=194/199<1.                     (R10)

The separation bounds also give distinct endpoints: the source minimum
separation is greater than 1/5-2delta, and the target minimum is at least
lambda/20-2delta, both positive. This is a finite restriction of the uniform deformation
lemma. Alternatively, Kirszbraun extends each error map with the same
Lipschitz bound, placing every instance of (R8) inside a distorted full-cone
domain from Section 2. No explicit choice of those extensions is required
for the finite motion. The original axial proof, not a finite Gaussian
calculation, supplies its middle segment.

## 4. A uniform orientation obstruction in three dimensions

Select directions d_0=(1,0), d_4=(-3/5,4/5), d_8=(-3/5,-4/5).
Let M_A and M_B be the matrices whose rows are these three vectors from
A and B, respectively. Their coordinate Gram matrices are

    M_A^T M_A = [[387/400, 0, -3/20],
                 [0, 18/25, 0], [-3/20, 0, 3]],
    M_B^T M_B = [[688/625, 0, -4/25],
                 [0, 512/625, 0], [-4/25, 0, 3]].           (R11)

The elementary diagonal-minus-absolute-off-diagonal bound gives
M_A^T M_A >= (18/25)I and M_B^T M_B >= (512/625)I.
Their row Gram matrices have the same eigenvalues. Both determinants
are positive: 36/25 and 1024/625. Every selected edge, including an edge
to the origin, has reference length at most 8/5. All vectors of each
cloud have common squared length R_C^2=1+p^2 or 1+q^2, at most 41/25;
each selected internal edge has squared length at most 2R_C^2.

Put alpha=2*delta=1/1000 and E=1/250. Changing an endpoint difference
by at most alpha changes its squared norm by at most

    2*(8/5)*alpha+alpha^2=3201/1000000 < E.                 (R12)

The same bound holds about the scaled target difference, since lambda<1.
If an R3 contracting motion existed, each selected squared edge length
d_t^2 would lie between its two perturbed endpoint values. Relative to its
unscaled reference squared length d^2, it would satisfy

    -(1-lambda^2)d^2-E <= d_t^2-d^2 <= E.                  (R13)

At every time subtract the position of the distinguished origin label.
Recover the Gram entry of two anchored vectors by polarization. Equations
(R13) and d_ij^2<=2R_C^2 give

    |(G_C(t)-G_C(0,reference))_ij|
        <= (1-lambda^2)R_C^2 + 3E/2.

Here the reference is the original unperturbed cloud, not the perturbed
time-zero Gram matrix. The same bound includes the diagonal entries.
A 3-by-3 matrix with entry magnitudes at most b has operator norm at most
3b. Hence both Gram matrices would obey the uniform lower bound

    G_C(t) >= [18/25-3*((1-lambda^2)*41/25+3E/2)] I
            = (2223/10000) I > 0.                          (R14)

No anchored triple can become coplanar at any time.

Initially the two oriented determinants have opposite signs, and finally
they have the same sign. These signs persist under all endpoint
perturbations in (R8): a row-matrix error has norm at most 3alpha=3/1000,
whereas (R11) gives reference smallest singular value greater than 4/5,
and scaled target smallest singular value greater than lambda*(4/5)=19/25.
Linear interpolation to each perturbed endpoint stays invertible.

Thus the product of the two oriented determinant signs would change along
the proposed motion. Equation (R14) forbids that. A rigid alignment of an
endpoint multiplies both determinants by the same sign, so their product
does not change; translations cancel at the anchor. The argument therefore
also excludes motions after arbitrary independent endpoint rigid alignments.
Together with Section 3, the minimal ambient motion dimension is exactly
four throughout (R8).

This proof uses small endpoint distance ranges, not exact preservation of
within-cluster distances. It does not extend the separate finite strong-
composition obstruction in COMPOSITIONS.md to this damped neighborhood.

## 5. Two further comparisons persist throughout the neighborhood

### Paired affine rank

The six paired reference rows selected in Section 4 form the matrix

    M = diag(M_A,M_B) [[I,lambda*I],[-I,lambda*I]].

The second factor has smallest singular value sqrt(2)*lambda. Thus M has
smallest singular value greater than 19/25, using (R11). After subtracting
the two perturbed anchor positions, each entry changes by at most alpha.
The 6-by-6 error has norm at most 6alpha=3/500<19/25. The paired matrix
therefore remains invertible, proving paired affine rank six throughout
(R8). Independent rigid alignments preserve that affine rank.

### Scalar-defect certificates

The criterion in the team's [scalar-defect proof](../gaussian_majorisation_scalar_defect/PROOF.md)
requires unit e,f with

    |X'_i-X'_j|^2-|Y'_i-Y'_j|^2
      >= [e.(X'_i-X'_j)-f.(Y'_i-Y'_j)]^2                    (R15)

for all pairs. Independent endpoint frames are already represented by
arbitrary unit e,f. Apply (R15) to the 24 anchor pairs.

Let R_A^2=25/16 and R_B^2=41/25, and set

    D_C=(1-lambda^2)R_C^2+2E.

Each anchor-pair squared-distance deficit is at most D_C by (R12).
Its scalar expression differs from the ideal expression
(e-lambda*f).a, or -(e+lambda*f).b, by at most 2alpha. The inequality
u^2<=(2v^2+2(u-v)^2) consequently bounds the ideal square by
2D_C+8alpha^2.

Averaging all twelve directions gives exactly

    (1/12)sum a*a^T = diag(p^2/2,p^2/2,1),
    (1/12)sum b*b^T = diag(q^2/2,q^2/2,1).

It follows that any certificate (R15) would require

    2(1+lambda^2)
       = |e-lambda*f|^2+|e+lambda*f|^2
       <= (2D_A+8alpha^2)/(p^2/2)
          +(2D_B+8alpha^2)/(q^2/2).

The left side is 761/200 and the right side is 821119/375000; their
difference is 151439/93750>0. This contradiction excludes the criterion
uniformly over every endpoint perturbation in (R8). It does not exclude
all other sufficient criteria or their compositions.

## 6. Scope, provenance and exact audit

The neighborhood theorem proves all hinges at every variance with all
probability weights. Unlike a bounded neighborhood of one positive weight
vector, it permits arbitrary exponential weight contrasts used to recover
individual ball radii. Its ball conclusion also follows directly from
the piecewise analytic motion, as above. This is consistent with the
[geometric-endpoint classification](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md).

The team's [spatial-cloud stability theorem](../gaussian_majorisation_open_stability/PROOF.md)
permits general small clouds on compact positive variance intervals, and
the [paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md)
gives an all-variance constrained neighborhood with restricted weights.
The later [bounded-law interior theorem](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
extends the analytic stability bridge to arbitrary bounded base laws, while
retaining dependence on the chosen laws and a compact positive variance
interval. These results are not premises here. Our whole-domain statement instead assumes
Lipschitz control of the source and target error maps and reserves a target
scaling factor. The finite application has unrestricted small endpoint
perturbations because its reference sites have fixed positive separations.
It does not assert an all-variance theorem for arbitrary nonatomic clouds
around arbitrary finite contractions.

The original axial geometry remains the nonclassical input. The present
extension is a quantitative closure consequence, not a newly discovered
firmly nonexpansive theorem or an exhaustive historical-priority claim.
The original interval pq<=2/pi is unchanged; the new maps have modified,
scaled and possibly nonlinear endpoints. For ball-method comparisons,
prescribed labels are essential. Pairwise distinct radii force a
radius-preserving permutation to be trivial, but other representations
of a ball union are not classified.

Run `python3 robustness_audit.py --check` and its `python3 -O` variant.
The standard-library exact checker reconstructs the reference sites,
checks every reference pair and the two Gram bounds, verifies all rational
perturbation budgets and the scalar contradiction, and checks symbolic
identities for the segment and Gram estimates. Invalid segment and reserve
controls must be rejected. A second enclosure checks positive definiteness
directly at all 64 corners of each tetrahedron's six squared-edge intervals,
using exact leading principal minors. Gram matrices depend affinely on those
six variables, so convexity covers every interior value as well. These 128
checks use a different representation of the orientation bound; they are
still author computation, not independent review.
[EXPECTED_ROBUSTNESS.json](EXPECTED_ROBUSTNESS.json)
is the compact deterministic output.

These finite checks audit the constants used in a universal written proof.
No grid of perturbed configurations, Gaussian quadrature, solver,
floating-point sign, large artifact, or formalization is a premise.
Author computation is not independent mathematical review.
