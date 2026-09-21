# Reconstruction from local Firey translation areas

2026-09-21. Human-readable proof; not a formal proof or a priority claim.

Let C=-C be a compact convex body with interior in R², centered at the
distinguished origin. For x in int C define

    F_C(x) = |(C+x) +_2 (C-x)|,

where |.| is area and h_(K+_2 L)²=h_K²+h_L². The data below are the analytic
germ at x=0, or its Taylor polynomials in fixed coordinates. A directional
measurement [t^d]F_C(tv) means a Taylor coefficient, not the unnormalized
d-th derivative. T_d F denotes the homogeneous degree-d Taylor term.

## Theorem

1. For every v≠0,

       ||v||_C = lim_(m→∞) ((2m-1)|[t^(2m)]F_C(tv)|)^(1/(2m)).       (1)

   Thus the Taylor series of t↦F_C(tv) has radius of convergence exactly
   1/||v||_C, and the local germ determines C. No smoothness is required.

2. From T_(2k)F_C one can form a positive semidefinite (k+1)×(k+1)
   matrix G_k, defined below. For k≥1, G_k is singular if and only if C
   is a polygon with at most 2k facets. If C has exactly 2r facets, then

       rank G_k = min(k+1,r).

3. If C has exactly 2r facets (r≥2), its Taylor jet through order 2r
   determines C among **all** full-dimensional origin-symmetric planar
   convex bodies. An explicit reconstruction uses just T_(2r)F_C and
   T_(2r-2)F_C: a one-dimensional kernel gives the facet directions, and
   positive moment ratios give their distances from the origin.
   The order 2r is sharp for every r≥2: distinct rotations of a regular
   2r-gon have identical jets through order 2r-1.

4. The construction respects invertible linear coordinate changes:

       F_(TC)(Tx) = |det T| F_C(x).                              (2)

   It is an affine-geometric reconstruction of a body whose center is
   designated. It is not a claim of translation invariance with the
   distinguished origin held fixed.

In fact, classical L_p Minkowski uniqueness implies that T_(2r)F_C alone
determines a 2r-facet polygon; Section 6 gives the precise deduction.
The two-term formula is an explicit reconstruction without solving a
Minkowski problem. No claim about stable recovery from noisy measurements
or a minimal number of sampled directions is made.

## 1. The reviewed transform and its moment interpretation

Write h=h_C on the unit circle, and let S_C be the surface area measure.
The previously proved and independently reviewed planar Firey transform
(linked in REFERENCES.md) specializes at p=2 to

    F_C(x) = (1/2) ∫ h(n) [2+2t arctan t] dS_C(n),
    t = x·n / h(n).                                             (3)

This identity already includes nonsmooth bodies. In particular,
∫h dS_C=2|C|. Define the finite positive even measure ν_C by pushing
h(n)dS_C(n) forward under

    n ↦ u(n)=n/h(n) ∈ ∂C°.

Its total mass is 2|C|. This is a measure on the polar boundary, not the
usual surface area measure on the unit circle. For ||x||_C<1 the series
for t arctan t converges uniformly on the relevant n, so

    F_C(x) = 2|C| + Σ_(m≥1) (-1)^(m-1)/(2m-1) M_(2m)(x),
    M_(2m)(x) = ∫ (x·u)^(2m) dν_C(u).                           (4)

Absolute uniform convergence also holds on a sufficiently small complex
coordinate neighborhood of 0. This proves analyticity of the germ and
justifies coefficient extraction. Formula (3), not numerical quadrature,
is the external mathematical dependency of this work.

The integrals in (4) equal ∫(x·n)^(2m)h(n)^(1-2m)dS_C(n).
Up to conventional normalization, these are classical L_(2m) projection
data. Their reinterpretation here as Taylor coefficients does not make
L_p projection bodies or moment inversion new methods.

## 2. The supported polar hull, including nonsmooth bodies

We prove

    conv(supp ν_C) = C°.                                        (5)

Let Z=supp S_C. The map n↦n/h(n) is a homeomorphism from the circle
onto ∂C°, and h is continuous and strictly positive. Consequently
supp ν_C is exactly the image of Z.

Parametrize n by angle θ. In distributions, h''+h=S_C. On any connected
open arc I=(α,β) of the complement of Z, this gives
h(θ)=a cos θ+b sin θ. The arc cannot have length at least π, since this
solution and its continuous endpoint values are strictly positive. For
α<θ<β, let

    λ = sin(β-θ)/sin(β-α),   μ = sin(θ-α)/sin(β-α).

Both are positive, n(θ)=λ n(α)+μ n(β), and the same linear relation
holds for h. Thus

    n(θ)/h(θ) = [λ h(α)/h(θ)] n(α)/h(α)
                +[μ h(β)/h(θ)] n(β)/h(β),

a convex combination of two points of supp ν_C. The endpoints belong
to Z. Here Z is nonempty because ∫h dS_C=2|C|>0, so every complementary
arc has endpoints. This treats every missing direction. All of ∂C° is
therefore in conv(supp ν_C), and the reverse inclusion is immediate.
Compactness of the support makes this convex hull closed. This proves (5).

This argument is essential: a polygon's surface area measure is supported
at facet normals, so full support on the circle must not be assumed.

## 3. Coefficient growth recovers the gauge

For v≠0, put a=max_(u∈supp ν_C)|v·u|. By (5), symmetry and polarity,
a=h_(C°)(v)=||v||_C>0. For any ε in (0,a), the set
{|v·u|>a-ε} has positive ν_C measure, by the definition of support.
Consequently

    (a-ε)^(2m) ν_C{|v·u|>a-ε} ≤ M_(2m)(v)
                              ≤ a^(2m) ν_C(R²).

Taking 2m-th roots and then ε↓0 gives M_(2m)(v)^(1/(2m))→a.
Equation (4) proves (1). The factor (2m-1) has 2m-th root tending to 1.
All even coefficients have the prescribed alternating sign and positive
magnitude; all odd coefficients vanish. Cauchy--Hadamard therefore gives
radius 1/a. For v=0 the function is constant and the radius is infinite.

This is the radius of the Taylor series in the complex variable t.
It does not assert failure of real analytic continuation at real t=1/a.
Indeed the support identity √[2(h²+(x·n)²)] supplies a natural extension
to all real x as twice the area of C+_2[-x,x]. Only the local germ is used.

Equality of germs now gives equality of gauges in all directions, hence
equality of bodies. Equation (2) follows directly because linear maps
commute with Firey sums and multiply area by |det T|. It also follows from
(1) that rescaling all area data by a fixed positive constant does not
change the reconstructed gauge.

## 4. A finite jet detects facet support

Let L_(2m) be the linear functional on homogeneous polynomials of degree
2m given by integration against ν_C. It is determined by T_(2m)F_C:
if the coefficient of x_1^j x_2^(2m-j) is c_j, then

    L_(2m)(u_1^j u_2^(2m-j))
       = (-1)^(m-1)(2m-1)c_j / binom(2m,j).                     (6)

On the space H_k of homogeneous binary forms of degree k define

    B_k(P,Q)=L_(2k)(PQ)=∫P(u)Q(u)dν_C(u).

In the basis u_1^i u_2^(k-i), 0≤i≤k, its Gram matrix is

    (G_k)_(ij)=L_(2k)(u_1^(i+j)u_2^(2k-i-j)).                  (7)

It is positive semidefinite. If singular, some nonzero homogeneous P
of degree k has ∫P²dν_C=0. Positivity and continuity imply
supp ν_C⊆{P=0}. A nonzero homogeneous binary form has at most k distinct
real projective roots, so this set away from the origin is contained in
at most k lines. Each such line meets ∂C° in exactly two antipodal points.
By (5), C° is their convex hull; C is a polygon with at most 2k facets.

Conversely, if C has 2r facets, ν_C has positive atoms on exactly r
antipodal pairs ±u_j, one pair for each facet-normal line. Evaluation
on these r projective directions has rank min(k+1,r): injectivity for
k<r follows from the root bound, and for k≥r-1 interpolation follows
from the products of all but one vanishing linear factor (multiplying
by a linear form nonzero at all directions if higher degree is needed).
Since every atom has positive weight, G_k has the same rank. This proves
both the detector and the rank formula.

## 5. Explicit reconstruction and sharpness

Suppose C has exactly 2r facets. G_r has a one-dimensional kernel,
spanned by

    P(u)=∏_(j=1)^r ℓ_j(u),                                    (8)

where ℓ_j is a linear form vanishing on the line R u_j. Factoring P
recovers these r distinct real lines, with no coordinate chart excluded.

Choose an arbitrary nonzero representative v_j on each line, and set
Q_j=∏_(i≠j)ℓ_i. Choose any linear form A_j with A_j(v_j)=1. Write the
unknown polar vertices as ±α_j v_j with α_j>0. By homogeneity and the
vanishing of Q_j on every other line,

    α_j² = L_(2r)(A_j² Q_j²) / L_(2r-2)(Q_j²).                 (9)

The denominator is strictly positive. The common positive weight of the
antipodal pair and the factor α_j^(2r-2)Q_j(v_j)² cancel in the ratio.
The reconstructed body is

    C = {x : |x·(α_j v_j)|≤1 for every j}.                     (10)

To check uniqueness against an arbitrary competitor D, matching 2r-jets
gives the same matrix G_r and hence the same kernel polynomial. Positivity
forces supp ν_D onto these same r lines. Rank r forces all r to occur.
The polar boundary meets a line only at its two radial endpoints, so
formula (9), using the same two moment functionals, gives exactly the
same endpoints for D. Equation (5) then gives D=C. No prior assumption
that D is polygonal or has a bounded number of facets is needed.

For sharpness, let C be a regular 2r-gon centered at 0. Its ν_C consists
of 2r equally weighted atoms with a common radius and angles
θ_0+jπ/r. Restrict a homogeneous polynomial of degree d<2r to that
circle. Its angular Fourier frequencies have absolute value at most d.
Summing over the 2r equally spaced angles kills every nonconstant
frequency, so the sum is independent of θ_0. Every rotation of C has
the same area and the same moments of all even degrees below 2r.
Odd Taylor terms are zero. A rotation through an angle not in (π/r)Z
gives a different polygon with the same (2r-1)-jet. This proves the
sharp uniform derivative order for every r, not only an example at r=2.
The roots-of-unity mechanism is classical; see the related surface-tensor
sharpness argument in Kousholt's Theorem 3.2.

## 6. The highest homogeneous term alone: an attributed corollary

For p=2r>2, write dS_p(C,n)=h_C(n)^(1-p)dS_C(n), the classical
L_p surface area measure. Its p-th moments are M_p. Suppose a body D
has the same T_p as the 2r-facet polygon C. The kernel argument above
also applies directly on the unit circle with measure S_p(D): its
support must be the same r pairs ±n_j as for C. The nonnegative
polynomials Q_j² A_j² of degree 2r, with A_j(n_j)=1, isolate the
mass of each antipodal pair. Thus S_p(C)=S_p(D).

Classical L_p Minkowski uniqueness for p>1, p≠2 in dimension two now
implies C=D. For completeness, the L_p mixed-area inequality reads

    V_p(C,D) ≥ |C|^((2-p)/2)|D|^(p/2),

with equality only for dilates (in the origin-containing formulation).
If the two S_p measures coincide, V_p(C,D)=|D| and V_p(D,C)=|C|.
For p>2 the two inequalities force both opposite area inequalities,
so the areas are equal and equality holds. The dilation is therefore
one. This is an application of established L_p Minkowski uniqueness,
not a new uniqueness theorem for L_p measures or the cosine transform.
The restrictions to a 2r-facet input and p=2r matter: fixed even-p
projection data do not determine arbitrary smooth bodies.

## 7. Validation and scope

The proof is geometric and analytic. The exact standard-library checker
builds rational centrally symmetric polygons from vertices, derives their
jets, then reconstructs them from those jets alone. Its decoder is not
given facet normals, facet counts, atoms, or the original polygon. It
finds the first singular Gram matrix, factors its rational projective
kernel, applies (9), and independently intersects the recovered
halfplanes. It also checks affine covariance, a rotated-square lower-jet
ambiguity, singular/degenerate chart handling, and smooth ellipse moment
data obtained independently from the determinant formula.

These finite checks validate the formulas and implementation; they do
not replace the all-body proof, the support-hull lemma, or the imported
Firey transform and classical L_p uniqueness. The decoder's rational-root
routine is for rational polygon fixtures, not an algorithm promised for
arbitrary real noisy data. No numerical conditioning, noise stability,
higher-dimensional analogue, nonsymmetric analogue, or classification
of all bodies determined by finite jets is asserted.
