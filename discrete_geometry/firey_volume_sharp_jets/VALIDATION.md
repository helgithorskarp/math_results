# What the exact checker establishes

All arithmetic in `verify.py` uses Python integers and `fractions.Fraction`.
There are no tolerances, numerical eigensolvers, or external data. The
records' digest covers the coefficient, local-curvature, direct-volume,
reconstruction and cylinder-rank records in deterministic order.

## Analytic normalization through separate identities

The coefficients b_(d,m) are compared with a direct expansion of the two
terms in Phi_d. For a Euclidean ball, its normalized even spherical moments
are (1/2)_m/(d/2)_m. Multiplication by d*b_(d,m) must give binomial(1/2,m),
as independently required by the ellipsoid determinant
|B_d +_2 [-x,x]|/|B_d| = sqrt(1+|x|^2). This checks all d=2,...,20 and
m=1,...,20. It is an exact identity check on that range, not its proof
for arbitrary parameters.

For local curvature, rational positive-definite Q and rational first jets
are generated in dimensions 2,...,8. The Hessian of t is fixed by l=ht
and the spherical linear-function identity. Expanding the second derivatives
of h*sqrt(1+t^2) and taking a determinant is compared with the rank-one
cofactor formula. Pythagorean values of t make all quantities rational.
The contracted identity used in the divergence step is checked separately.
The differential-geometric integration and global approximation are proved
in prose, not established by these local fixtures.

For a distinct, definition-level volume check, take C=[-1,1] x B with any
origin-symmetric (d-1)-body B and an axial segment of half-length t>=0.
The L_2 sum is the union of aC+b[-te_1,te_1] over a,b>=0, a^2+b^2<=1:
this union is convex, and its support is sqrt(h_C^2+t^2 n_1^2).
At transverse gauge s=||y||_B, the top axial coordinate is

    sqrt(1+t^2)                   if s<=1/sqrt(1+t^2),
    s+t*sqrt(1-s^2)               otherwise.

Put f=sqrt(1+t^2), s0=1/f. Direct layer integration, divided by |C|, is

    f*s0^(d-1) + (d-1)(1-s0^d)/d
       + (d-1)t integral_(s0)^1 s^(d-2)sqrt(1-s^2) ds.

For odd d=3,5,...,15 the remaining integral is a finite polynomial in
u0=t/f after u=sqrt(1-s^2). Four Pythagorean t values, including zero,
allow an exact rational comparison with (Phi_d(t)+d-1)/d. This does not
derive the direct volume by reusing the surface-measure formula being tested.

## Reconstructing realizable polytopes

Fixtures are products of exact rational cyclic polygons with boxes in
dimensions 2,...,5, and their nonsingular sheared images, together with
three- and four-dimensional crosspolytopes and their shears. Polygon facets
and pair masses are derived from oriented edges, rather than chosen as
arbitrary moment atoms. For the crosspolytope, normals on the polar cube
have antipodal-pair mass 2/(d-1)!. Affine images transform polar endpoints
by inverse transpose and pair masses by the absolute determinant.

The checker encodes the two homogeneous Taylor terms, decodes their full
moment tensors, constructs the top Gram kernel, and checks a supplied list
of distinct spanning rational lines against that kernel. Dimension and
evaluation-rank checks verify equality with the whole vanishing-polynomial
space, so the written separation lemma proves that the certificate excludes
unlisted real projective zeros. Interpolating products of hyperplanes then
give the radial ratios. Every recovered polar outer product is compared
with its original geometric endpoint, and both full moment tensors are
reconstructed entry by entry. The line representatives are deliberately
rescaled so the cancellation of their arbitrary normalization is tested.

Off-support rational points test the separation construction. Affine
directional-moment identities independently check determinant normalization.
The full data are generated in memory; no opaque moment dataset is shipped.

## Boundary and adversarial checks

Ball Gram forms in dimensions two through four have full rank. For the
three-dimensional circular cylinder, exact circle beta moments plus axis
atoms instead give ranks four and five in degrees two and three. This
checks the explicit nonpolytope with a singular quadratic Gram form.

A four-dimensional parallelotope and its factor-three dilation have
identical fourth terms and different quadratic terms, checking the actual
critical-dimension ambiguity. Finite integer frequency calculations check
the rotational cancellation used in the sharpness construction; its
all-parameter conclusion is the written roots-of-unity proof.

Six malformed or impossible inputs are required to fail: repeated lines,
a zero line, a negated even top moment form, an empty jet, an invalid
dimension and an odd jet degree. Arbitrary one-entry changes are not all
invalid: some represent different positive moment data. The checker does
not certify geometric realizability for every arbitrary input tensor.

## Trust boundary

These are author checks, not independent peer review. Exactness depends on
the readable implementation, Python's rational/integer semantics, runtime,
OS and hardware. The universal theorem relies on the written proof and its
explicit classical analytic inputs. No numerical conditioning or noisy-data
algorithm is tested or promised.
