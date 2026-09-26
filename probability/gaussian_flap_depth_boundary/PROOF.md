# Shallow simplex flaps: strict first variation and the remaining tail boundary

Complete author proof, 26 September 2026. Independent correctness and
historical-priority review are pending. The full three-dimensional Gaussian
majorisation problem remains open. This controls a deformation of asymmetric
extremal maps; it does not prove comparison at all positive thresholds for
any fixed nonzero depth, or a new Kneser--Poulsen volume inequality.

## 1. Geometry and statement

Let v_0,...,v_3 be the vertices of any nondegenerate tetrahedron in R3.
Choose d_i perpendicular to the face opposite v_i, pointing toward v_i.
Its length is arbitrary and positive. Write

    h_i = d_i.(v_i-v_j) > 0,        j != i.                 (1)

The expression is independent of j. Equivalently d_i=h_i grad(lambda_i),
where lambda_i is the i-th affine barycentric coordinate. In particular
sum_i d_i/h_i=0, and any three of the d_i are linearly independent.

For depth t>=0 take four fixed core labels and twelve ordered flap labels:

    p_i(t)=q_i(t)=v_i,
    p_ij(t)=v_j-t d_i,      q_ij(t)=v_j+t d_i,    i != j. (2)

The source and target carry the same label weights alpha_i and beta_ij,
respectively, with all weights nonnegative and total one. No symmetry or
strict positivity of weights is assumed. Set

    w_j = alpha_j + sum_(i!=j) beta_ij,
    Gamma = sum_(i!=j) h_i beta_ij w_i.                    (3)

Let gamma_s have covariance s I_3. Denote the two convolved densities by
f_(s,t) and g_(s,t), and their collapsed density by

    f_(s,0)=g_(s,0)=F_s=sum_j w_j gamma_s(. -v_j).

Write H_f(a)=integral(f-a)_+, D_(s,t)(a)=H_g_(s,t)(a)-H_f_(s,t)(a),
and M_s=max F_s. All these quantities also depend on the weight vector.

**Theorem A (exact first variation).** The map in (2) is a contraction at
every t>=0. Gamma=0 if and only if its restriction to the positive-weight
labels is an isometry at one, hence every, positive depth. In that case
D_(s,t)(a)=0 for all s,t,a. Otherwise, for every s>0 and 0<a<M_s,

    d/dt D_(s,t)(a) at t=0
       = (2a/s) integral_{F_s>a} B_s(x)/F_s(x)^2 dx > 0,  (4)

where

    B_s(x)=sum_(i!=j) h_i beta_ij w_i
                           gamma_s(x-v_i)gamma_s(x-v_j). (5)

The derivative exists also at critical density levels. No smoothness of
the level surface is assumed.

**Theorem B (uniform exclusion away from zero threshold).** Fix the
tetrahedron and the d_i. For any 0<s_0<=s_1<infinity, a_0>0 and kappa>0,
there is t_*>0 such that, simultaneously for

    s in [s_0,s_1],    Gamma>=kappa,    0<t<t_*,    a>=a_0,

and every probability weight vector satisfying those conditions,

    D_(s,t)(a)>=0.                                      (6)

It is strict whenever a<max g_(s,t); at and above that maximum both
hinges vanish. If the allowed weight set is empty, the statement is vacuous.
The existence proof does not supply an effective numerical t_*.

Consequently, for a fixed nonisometric weight vector and a compact range
of positive variances, any sequence of negative hinges at depths tending
to zero must have thresholds tending to zero. Uniformly varying weights
can escape this conclusion only by approaching Gamma=0. No control is
claimed when the variance tends to zero or infinity, the geometry
degenerates, or a tends to zero along with t. Those distinctions matter:
(6) is not the full all-threshold inequality at any given positive depth.

These flaps are classical. The application here is the exact weighted
deformation formula, its equality condition, and the uniform localization
of any remaining shallow failure. The general Gaussian velocity/divergence
mechanism is prior work, credited in [SOURCES.md](SOURCES.md).

## 2. Pair losses, collisions, and the isometry boundary

For labels with the evident indexing, direct expansion gives

    |p_i-p_j|^2-|q_i-q_j|^2 = 0,
    |v_k-p_ij|^2-|v_k-q_ij|^2 = 4t h_i 1_(k=i),
    |p_ij-p_kl|^2-|q_ij-q_kl|^2
                  = 4t (h_i 1_(l=i)+h_k 1_(j=k)).        (7)

Indeed d_i.(v_j-v_l)=-h_i 1_(l=i) for i!=j, and
d_k.(v_j-v_l)=h_k 1_(j=k) for k!=l. Every loss is nonnegative.
If source labels coincide, their target distance is therefore zero;
the map is well defined, with masses merged if necessary. Kirszbraun
extends this finite contraction if a full-space map is desired.

Take independent labels L,L' with the prescribed weights. Summing (7)
gives the exact identity

    E[|p_L-p_L'|^2-|q_L-q_L'|^2] = 8t Gamma.             (8)

For t>0 every summand is nonnegative. Thus Gamma=0 if and only if all
pair distances between positive-weight labels are preserved. Equality
of labelled Euclidean distance matrices gives an ambient isometry, by
the centered Gram-matrix argument, including repeated target locations.
This proves the equality characterization and equality of the convolved
hinges. It also shows why vanishingly small Gamma is a necessary separate
boundary in Theorem B.

For the regular vertices (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1) and d_i=v_i,
one has h_i=4. Formula (4) then has coefficient 8a/s multiplying the
same numerator without h_i. This matches the conventional flap-depth
normalization; using barycentric gradients instead rescales depth by four.

## 3. The collapsed velocity and a positive divergence numerator

In this section fix the weights and s, and abbreviate

    phi_j(x)=gamma_s(x-v_j),
    m(x)=sum_(i!=j) beta_ij d_i phi_j(x),
    b(x)=-div m(x),        u(x)=m(x)/F_s(x).              (9)

Differentiating translations of the Gaussian, in L1 and locally uniformly,
gives

    partial_t g_(s,t) at 0 = b,
    partial_t f_(s,t) at 0 = -b.                         (10)

The vector u is the posterior average of the bounded velocities
sum_i beta_ij d_i/w_j at occupied collapsed site j. When w_j=0, the
corresponding beta_ij also vanish and that site contributes nothing.
We will not divide by a possibly zero weight in any theorem formula.

Using grad phi_j=(v_j-x)phi_j/s, the quotient rule yields

    s F_s^2 div u
       = sum_(i!=j),k beta_ij w_k phi_j phi_k
                                      d_i.(v_j-v_k)
       = -B_s.                                         (11)

Only k=i survives in the last equality, with factor -h_i. In particular,
Gamma>0 implies B_s(x)>0 at every x and div u(x)<0 everywhere. Both u
and its first spatial derivatives are bounded: u is a finite posterior
average and its derivative is a covariance with the bounded centers.

At any maximizer x of F_s, grad F_s(x)=0. Since

    b=-div(F_s u)=-u.grad F_s + B_s/(s F_s),             (12)

we have b(x)>0 at every maximizer whenever Gamma>0. This positivity at
all maximizers, not an assumption of a unique or nondegenerate mode, will
handle thresholds near the top of the density range.

## 4. Hinge differentiation without regular levels

A finite Gaussian mixture is positive, real analytic, nonconstant, and
tends to zero at infinity. Every positive level has Lebesgue measure
zero, and every positive superlevel set is bounded. Gaussian translation
derivatives are integrable. Differentiating the Lipschitz positive part
by dominated convergence at every point off the null level set gives

    d/dt D_(s,t)(a) at 0 = 2 integral_{F_s>a} b.          (13)

This argument also follows by L1 differentiability and the null level
set; it does not require division by |grad F_s|.

The function (F_s-a)_+ is compactly supported and Lipschitz. Integration
of div((F_s-a)_+ u) over R3, using its weak derivative, gives

    integral_{F_s>a} u.grad F_s
      + integral_{F_s>a}(F_s-a)div u = 0.

Consequently

    integral_{F_s>a} b
       = -a integral_{F_s>a} div u
       = (a/s) integral_{F_s>a} B_s/F_s^2.              (14)

This proves (4). If 0<a<M_s the superlevel set contains a nonempty open
set, so the integral is strictly positive exactly when Gamma>0. Formula
(14) also shows the integral is finite: the set is bounded and u is C1.

## 5. Uniformity, including the top of the density range

Let W_kappa be the closed set of probability weights with Gamma>=kappa.
It is compact. Set P=W_kappa times [s_0,s_1]. All assertions below are
uniform over P; if P is empty there is nothing to prove.

The baseline densities, b, and their needed derivatives vary continuously
in the parameters and locally uniformly in space. Gaussian tails bound
them uniformly at infinity. Thus M_s is continuous and positive on P,
and the union of its maximizing sets is compact. Equation (12) is
strictly positive on that compact set. There are c>0 and eta>0 such that

    F_s(x)>M_s-2eta  implies  b(x)>=c,                    (15)

uniformly over P; take also 2eta<min_P M_s. To see the uniform assertion,
otherwise take a sequence of parameters and near-maximizing points.
Uniform tails bound the points, compactness supplies a subsequence, and
continuity contradicts positivity of b at its limiting maximizer.

For small t, uniformly over P and all x,

    |f_(s,t)(x)-F_s(x)|=O(t),
    g_(s,t)(x)-f_(s,t)(x)=2t b(x)+O(t^3).               (16)

These follow from the globally bounded first and third translation
derivatives of a Gaussian with s in the given compact interval. The
moving centers and velocities range over a fixed bounded set.

Choose t small enough for the first error to be less than eta and the
second remainder to be less than ct. If a>=M_s-eta and f_(s,t)(x)>a,
then F_s(x)>M_s-2eta and hence g_(s,t)(x)>f_(s,t)(x). Therefore

    (g_(s,t)-a)_+ >= (f_(s,t)-a)_+                      (17)

pointwise on the latter's positive set; outside it the right side is zero.
The same argument at a maximizer of f_(s,t) shows max g_(s,t)>max f_(s,t).
It follows that the integrated comparison is strict for
M_s-eta<=a<max g_(s,t), and both hinges vanish above that maximum.

It remains to consider the compact parameter-level set

    (weights,s) in P,        a_0<=a<=M_s-eta.            (18)

It may be empty. On it the coefficient in (4) is continuous and strictly
positive, so it has a positive minimum. For completeness, continuity of
hinge derivatives through critical levels follows by dominated convergence:
the densities and their depth derivatives are jointly continuous, their
positive level sets are null, and there is a common integrable Gaussian
tail bound for derivatives for small positive and negative depths. Thus
partial_t D_(s,t)(a) is jointly continuous near t=0, including all of (18).
Compactness and D_(s,0)(a)=0 now give

    D_(s,t)(a)/t -> partial_t D_(s,0)(a)

uniformly on (18). For sufficiently small positive t it is strictly
positive there. Combined with (17), this proves Theorem B.

The proof deliberately leaves the level a=0 outside the compact argument.
Although D_(s,t)(0)=0 exactly, continuity at zero cannot infer its sign at
positive thresholds which themselves tend to zero with t.

## 6. Why this deformation still tests rigid, asymmetric maps

The following elementary rigidity argument records the geometric control;
it is not evidence for the remaining hinge sign. It extends the familiar
simplex-flap argument in Cheng--Tan--Zheng to the normal-coordinate notation
used here. Full configurations refer to all sixteen labels, regardless of
which labels receive mass in Theorems A and B.

At every t>0 the full contraction (2) has no intermediate R3 distance
matrix other than its endpoints, and has no continuous contracting motion
in R5. Here intermediate means that every pair distance lies between its
two endpoint distances. No restriction to a proposed folding algorithm
is imposed.

To prove this, preserve the tight core tetrahedron and align it with the
original v_i. At an intermediate placement in R^(3+k), the three tight
distances from flap label (i,j) to core vertices other than i force

    z_ij = v_j+r_ij,      r_ij perpendicular to face i,
    |r_ij|=t|d_i|.                                      (19)

The within-flap pair distances are tight. Since v_j-v_l is in face i,
their squared distances are |v_j-v_l|^2+|r_ij-r_il|^2.
Hence r_ij=r_il=:r_i. For i!=k choose j outside {i,k}. The tight distance
between labels (i,j) and (k,j) gives

    r_i.r_k=t^2 d_i.d_k.                               (20)

Together with their norms, this says the Gram matrices of the r_i and
t d_i agree. In particular sum_i r_i/h_i=0. The physical R3 component
of r_i is lambda_i d_i by (19). The unique linear dependence of the four
d_i has coefficients 1/h_i, so all lambda_i have one common value lambda.
Writing r_i=lambda d_i+e_i in the k auxiliary coordinates, (20) becomes

    (e_i.e_j)_(i,j)=(t^2-lambda^2)(d_i.d_j)_(i,j).       (21)

The latter Gram matrix has rank three. If k<=2, (21) forces
lambda=+t or -t; then all e_i vanish and the whole placement is the
corresponding endpoint. In particular k=0 proves the claimed full R3
interval property. For a continuous motion in R5 the core can be aligned
continuously (a moving orthonormal frame on an interval suffices).
The continuous scalar lambda would have to go from -t to t while taking
only those two values, a contradiction. The same reasoning rules out a
nontrivial intermediate placement even in R4 or R5.

At least one pair in (7) is strictly contracted for t>0, so the endpoints
are distinct distance matrices. A continuous R6 contraction exists by
the classical Gram interpolation/leapfrog construction; no stronger
minimal-motion theorem is required for the analytic results above.

Thus a shallow depth and a nonnegative first hinge variation do not make
these maps continuously contractible in R5. Conversely, their lack of
such a motion is not a negative Gaussian comparison. The rigidity and
all-depth pair identities apply to the exact asymmetric tetrahedron in
the verifier, as well as to the regular control.

## 7. Reproduction and remaining task

Run `python3 verify.py --check` from this directory. The standard-library
checker proves the finite geometric and coefficient identities over exact
rational arithmetic for a regular control and an asymmetric tetrahedron
with independently scaled normals. It also checks the complete quadratic
weight identity (8), the numerator cancellations in (11), Gram rank and
the positive dependence, and isometric/near-isometric weight controls.
These are exact controls on the formulas, not numerical evaluations of
hinges or a finite proof of the universal analytic statements.

The written proof of Theorems A and B is the analytic trust boundary.
There is no Gaussian quadrature, floating-point sign, numerical optimizer,
heavy enumeration, or claimed effective value of t_*.

The highest-value remaining question for this family is the joint limit
t down to zero and a down to zero, followed by positive-depth comparison.
The compactness argument must not be extended to that boundary without
a uniform tail estimate. The full named problem remains unrestricted;
this family and this result do not settle it.
