# Independent geometric review of the rigid-hull comparison theorem

**Accept with high confidence within the stated scope.** This review covers
researcher 1's [all-threshold rigid-hull theorem](../gaussian_contact_rigid_hulls/PROOF.md)
at source commit `23098acb378d85684b32c8913f4bd1f42b3a97dc`: the linear
mean-width margin, the displacement-relative tail lemma, the explicit
neighborhood, and the gluing to all hinges and concentration profiles.
The published [local near-isometry theorem](../gaussian_contact_near_isometries/PROOF.md)
is a credited premise. Its use here agrees with its hypotheses and its
[existing independent review](../gaussian_contact_near_isometries_review2/REVIEW.md).

The result applies to a fixed finite source spanning R3, with fixed
positive weights, an infinitesimally rigid graph of actual hull edges,
and every nonvertex source site strictly inside the hull. At each fixed
variance, all sufficiently close contracted images, after the specified
weighted Procrustes alignment, satisfy every Gaussian hinge comparison.
The general-position corollary has no atom-count cap. The neighborhood
is not uniform over changing weights, colliding sites, degenerating
geometry, or all positive variances.

This is an independent cross-lane agent review, not external human peer
review or a formalization. Researcher 6 did not develop this theorem and
has not read, imported, or executed its author checker or expected record.
The new exact controls below reconstruct the geometry through positive
Gram forms and rational LDL factorizations. No new theorem or map class
is claimed by the reviewer. The unrestricted R3 question remains open.

## 1. The geometric coercivity has the required linear scale

Write the aligned displacement as h_i=y_i-x_i and
delta=max_i |h_i|. Centering and Procrustes alignment give

    sum p_i h_i=0,       sum p_i x_i cross h_i=0.

Endpoint contraction, without a monotone straight path, implies

    s_ij=(x_i-x_j).(h_i-h_j) <= -|h_i-h_j|^2/2 <= 0.

For hull vertices, infinitesimal rigidity says that zero edge strains
give exactly the six rigid velocities. The displayed gauge removes
translations; on rotations its matrix is

    tr(Cov_p(x)) I-Cov_p(x) >= 2 kappa I.

Thus the edge operator is injective on that gauge subspace. Its inverse
norm supplies the author's C_E. This is a norm bound on velocities, not
merely the qualitative assertion that a particular contraction loses
some mean width.

The extension to interior sites is valid and needs the full contraction
cone. Fit a rigid velocity to the hull using uniform hull weights, and
let r_i be the residual on all labels. Hull rigidity gives

    max_(j on hull) |r_j| <= C_H sum_(e on hull)(-s_e) = H.

For an interior site i with B(x_i,rho_i) contained in the hull, choose a
vertex j minimizing the functional r_i.x_j. The ball inclusion gives
rho_i |r_i| <= (x_i-x_j).r_i. The pair-strain inequality then implies

    rho_i |r_i| <= (x_i-x_j).r_j <= 2 R_x H.

Consequently all residuals have norm at most K H, where
K=max(1,max_i 2R_x/rho_i). Returning from the fitted hull gauge to the
weighted gauge on all labels costs at most 2+R_x^2/(2kappa). This is
exactly the stated

    C_E=(2+R_x^2/(2kappa)) K C_H.

One cannot replace this argument by full rank of the hull-edge matrix
on all sites. Our eight-site control exhibits a nonzero gauged velocity
with every hull-edge strain zero: give the central site velocity e_1
and remove the common mean. It has a positive interior-to-hull strain,
so the all-pair contraction cone excludes it. This independently tests
the reason the interior-depth assumption is present.

## 2. The support integral and its remainder have the correct sign

Let W(X)=integral_(S2) max_i theta.x_i d sigma, with sphere area 4pi.
For a hull normal cell C_i, the spherical identity Delta theta=-2theta
gives integral_C_i theta=-(1/2) integral_boundary(C_i) n_out. Across
the arc for edge ij, n_out=(x_j-x_i)/|x_i-x_j|. Summing the two cells
therefore gives

    DW_X[h] = (1/2) sum_(ij in E)
                    (alpha_ij/|x_i-x_j|) s_ij.

There is no factor-of-two or orientation error. If
beta<=min alpha_ij/(2|x_i-x_j|), then
-DW_X[h]>=beta delta/C_E. An exact axis-box normalization control gives
W/pi equal to the sum of the three side lengths and reproduces this
same factor 1/2. That control does not assert hull-edge rigidity for a cube.

A change of maximizing label at interpolation time t requires a slab
|theta.(x_i-x_j)|<=2t delta. The area of one such slab is bounded by
8pi t delta/nu_0. Summing over N(N-1)/2 pairs, bounding the directional
velocity change by 2delta, and integrating 0<=t<=1 gives

    |W(Y)-W(X)-DW_X[h]| <= 4pi N(N-1) delta^2/nu_0.

This does not require an unchanged normal fan. Under the author's
delta<=beta nu_0/(8pi C_E N(N-1)), the remainder uses at most half of
the linear term. Hence W(X)-W(Y)>=c delta with c=beta/(2C_E).

The use of actual hull edges is essential. The Dehn theorem for a
convex polyhedron with triangular faces supplies their rigidity in the
general-position corollary; its statement is recorded in the introduction
of [Connelly--Gortler](https://pi.math.cornell.edu/~connelly/pdf/10.1137_15M1054833.pdf).
Our four fixtures check the rank condition directly, independently of
that classical input. Qualitative strict mean-width monotonicity under
contractions is already known; see
[Gorbovickis, Theorem 1.5](https://arxiv.org/html/1006.0531v2).
The reviewed argument needs, and proves, the additional linear scale.

## 3. The tail error is proportional to the same displacement

This part uses an arbitrary separated finite straight path z_i(t), with
|z_i(t)|<=M, separation at least nu, and velocities bounded by delta.
Neither contraction nor a low-dimensional contracting motion is assumed.
Set a_R=C_3 exp(-R^2/2), R>=max(2,4M). Each radial level boundary lies
in [R-M,R+M]. Its logarithmic radial derivative is -r+m, |m|<=M,
and is strictly negative there. Thus the boundary is unique and smooth,
even though arbitrary interior density thresholds may be critical.

Writing A for the posterior mean of theta.h_i and B for that of z_i.h_i,
implicit differentiation gives

    r'=(r A-B)/(r-m),
    |r'-A|<=4M delta/R,       |r'|<=2delta.

Discard pair slabs of width
eta=(log(1/p_*)+M^2+log R)/(R-M). Outside them the nonleading kernel
mass divided by the leading mass is at most 1/R. The leading velocity
therefore differs from A by at most 2delta/R. Combining the radial
Jacobian, the slab area, and the coarse bound on the discarded set yields

    |V'/R^2-W'|
      <= (pi delta/R)[40M+8
             +(20N(N-1)/nu)(log(1/p_*)+M^2+log R)].

The exterior-mass estimate retains a cancellation that is indispensable
for this application. At the radial boundary let pi_i be the posterior
weights, put ell=sqrt(r^2+2u), d=ell-r, and
J(u)=sum pi_i exp(d theta.z_i). Then

    Q_theta/a_R = integral_0^infinity exp(-u) ell J(u) du,
    sum pi_i'=0.

In the posterior-derivative term subtract 1 from each exponential before
taking absolute values. Using d<=u/r, M/r<=1/3 and
sum |pi_i'|<=5R delta gives

    |J'| <= exp(Mu/r)
           [5R delta M u/r+2delta M u/r^2+delta u/r].

The derivative of ell is bounded by 2delta. Integrating with
integral exp(-2u/3)du=3/2 and
integral exp(-2u/3)(u+u^2)du=9 proves

    |Q_theta'|/a_R <= delta(45RM+18M+12)
                    <=60R delta(M+1).

These same bounds provide an integrable majorant for differentiation.
Spherical integration costs 4pi. As H=1-Q-a_R V, the final coefficients
are 40M+8+240(M+1)=280M+248, giving precisely

    |(H_1-H_0)/(a_R R^2) - (W_0-W_1)| <= delta E(R),
    E(R)=(pi/R)[280M+248
                 +(20N(N-1)/nu)(log(1/p_*)+M^2+log R)].

The path separation and positive fixed weights are real hypotheses.
This bound cannot be used uniformly through collisions or a vanishing
weight. R4's [relative-tail work](../gaussian_flap_depth_boundary/RELATIVE_TAIL.md)
is correctly credited for the radial differentiation and cancellation
method. The present estimates were checked directly in R1's formulation;
this review does not independently accept R4's full flap theorem.

## 4. The two threshold ranges meet without a limiting interchange

For the aligned endpoint contraction, delta<=1 and delta<=nu_0/4
provide M=R_x+1 and nu=nu_0/2 along the straight path. The source's
R_0 bounds imply

    E(R)<=pi A/R+pi B/sqrt(R)<=c/2,       R>=R_0.

Together with the mean-width margin, this yields

    H_g(a_R)-H_f(a_R)>=(c/2) a_R R^2 delta.

All thresholds in (0,a_0], a_0=C_3 exp(-R_0^2/2), are covered by the
same displacement neighborhood. R_0 depends on the fixed source and
weights, not on the chosen nearby target. There is no exchange of a
small-displacement limit with a small-threshold limit.

For a>=a_0 below the source peak, the actual source top set is contained
in B_(R_0+R_x), so its volume radius is at most R_0+R_x. The q-factor
in the published local theorem is therefore at least

    q_0=exp(-[(R_0+2R_x)^2/2+(R_0+4R_x)^2]).

The restriction delta<=kappa q_0/(16R_x) gives a simultaneous positive
profile gap throughout that finite volume range. Testing the target
hinge at the same volume proves strict hinge comparison. At or above
the source peak, its hinge is zero; strictness persists up to the target
peak whenever that interval is nonempty.

Finally, evaluate hinge/profile duality at the target optimizer's
positive threshold. Strict hinge comparison gives strict concentration
profile comparison at every finite positive volume. The null positive
level sets of a Gaussian mixture justify the optimizer statement.
The isometric equality case and the variance rescaling agree with the
credited local theorem. Ordered profile contacts in this neighborhood
are consequently isometric and have equal bulk heat flux.

## 5. Independent evidence and limits of acceptance

[independent_check.py](independent_check.py) uses rational Gram matrices
for edge strains plus the six gauge equations. A positive LDL factorization
and exact strain-coordinate reconstruction supply C_E for four different
hulls with 4, 5, 6 and 7 vertices. The seven-site moment-curve fixture has
10 triangular facets and 15 edges. Adding its centroid verifies the
interior ball and the separate contraction-cone argument above.

The audit obtains rational lower bounds on covariance, edge separation
and exterior angles; its angle bound uses alpha>=sin(alpha), without
numerical inverse trigonometry. It also constructs conservative integer
tail cutoffs using pi<4 and log(1/p_*)<=1/p_*. It never evaluates an
astronomically small Gaussian threshold. These are independent admissible
constants, not a replay or claimed match of the author's constants.

There are 216 radial scalar corner controls, exact Gamma-integral and
support-normalization checks, and six deliberate rejections: a deleted
tetrahedral edge, each omitted rigid-motion gauge, the cube's actual
edge framework, an equality-only interior-site extension, and a zero
weight passed to the fixed-positive-label interface. The cube and
zero-weight tests do not assert failure of Gaussian comparison.

From the repository root, with CPython 3.11.2 and no third-party packages:

```sh
python3 probability/gaussian_rigid_hull_review_r6/independent_check.py --check
python3 -O probability/gaussian_rigid_hull_review_r6/independent_check.py --check
```

Expected status: `INDEPENDENT_RIGID_HULL_GEOMETRY_REVIEW_PASS`.
The canonical [record](EXPECTED.json) has SHA256
`7c5c65aa55948b0f7fe31bd656015556aa0a3b2311bedd31e36a2d099a9dfc9a`.
[INPUTS.json](INPUTS.json) pins the reviewed statements and dependencies.
Finite algebraic checks supplement the written analytic review; they do
not formalize integration, the classical rigidity theorem, or the
universal conclusion.

No acceptance is extended to a variance-independent neighborhood, a new
Kneser--Poulsen consequence, arbitrary bounded or Gaussian-tailed inputs,
historical priority, optimal constants, or separation from every known
continuous-motion class. The reviewer-owned axial/matrix/H/H2 package
is context, not a premise; this review is not an independent review of
that package. Its positive margin and R1's local result retain their
different geometric hypotheses. R4 retains extremal-map ownership.
