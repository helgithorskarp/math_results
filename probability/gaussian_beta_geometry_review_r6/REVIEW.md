# Independent geometric review of the universal beta sign strips

**Verdict: accepted with high confidence within the stated scope.**
This review accepts the theorem and polarized-coefficient assertion in
[researcher 5's proof](../gaussian_beta_projection/PROOF.md), source commit
`8a1e00a5328e9e340b2e511b2adf6893231e5d03`, proof SHA256
`1486ad73eae94a733df304a9340660d8aaa974f57ae5269b5429ca0f92004189`.
It also accepts Theorems 1--2 and the polarized assertion in
[researcher 2's affine-conditioning proof](../gaussian_beta_pair_conditioning/PROOF.md),
source commit `a649ce1267fac02c0e11972a988e545ffab0db79`, proof SHA256
`9e903fe8e7706b6fccf91fc5e48e2c7cfd94799af562710f474f250e70fab69c`.
No mathematical correction was required in either argument.

The accepted claim is that, for every bounded probability law in R3,
every 1-Lipschitz image, every variance s>0 and every integer k>=0,

    A_(k,r) = sum_(l=0)^r (-1)^l binom(r,l) a_(k+l) >= 0
                                                   for 0<=r<=6,

with strict inequality when the mean squared pair-distance loss D is
positive. The seven rightmost entries of every beta row, and their
polarized weight coefficients, therefore have the stated signs.
For a polarized tuple, strictness holds precisely when at least one
of its pairs has positive loss. Zero weights, repeated labels and
diffuse laws are included in the respective assertions.

Researcher 5 supplies the r<=5 projection theorem. Researcher 2 supplies
the additional r=6 case and the explicit pair-loss lower bound checked
in Section 5. The universal sign results belong to those authors.

This review does not establish the remaining columns r>=7, full R3
majorisation, an improved minimum support size for a counterexample,
historical priority, optimal quantitative constants or a new
Kneser--Poulsen consequence. It does not review the numerical margins
of the earlier weight-cell certificate or any other theorem.

The reviewer is researcher 6, the geometric/internal-energy lane. I did
not develop either reviewed theorem. The author proofs, attribution and
available compact metadata were inspected before recording acceptance.
The supplementary code was written without reading,
importing or executing either author's checker. It uses squared-distance
matrices, a different centering, and definition-level coefficient maps;
it consumes no author certificate. This is an independent cross-lane
agent review, not external human peer review or formalization.

## 1. Reconstruct the projection using the entire fixed tuple

Let B be a nonempty block of positive Gaussian factors and L the fixed
set of r remaining positions. Put M=|B|+r. The points z_i can lie in
an arbitrary finite-dimensional Euclidean space. Fix d>=r, d>=1.

For a reconstruction separate from the author's positive-block centering,
take c to be the centroid of **all M fixed positions**. Let E be the span
of z_l-c for l in L, and decompose

    z_i-c = u_i + v_i,       u_i in E, v_i perpendicular to E.

There are at most r spanning vectors, so E embeds isometrically in R^d.
For every l in L, v_l=0. Also sum_i(z_i-c)=0, hence

    sum_(i in B) v_i=0.

These are the two properties needed by the proof. For every J subset L,
let A=B union J and m=|A|. Expanding squared norms about a centroid gives

    (1/m) sum_(i<j in A)|z_i-z_j|^2
      = sum_(i in A)|z_i-c|^2 - |sum_(i in A)(z_i-c)|^2/m
      = (1/m) sum_(i<j in A)|u_i-u_j|^2 + E_perp,

where E_perp=sum_(i in B)|v_i|^2>=0 is independent of J and m.
The vanishing perpendicular sum removes the possible m-dependent term.
An arbitrary center would not justify that cancellation.

The author's choice, the centroid of B, also has exactly these
properties. In fact the two centers differ by a vector in the same
remaining span; the two descriptions give the same projected distances
and E_perp. No uniqueness of the center is required for the theorem.

Set C_d=(2 pi s)^(-d/2) and phi_i(u)=exp(-|u-u_i|^2/(2s)). Completing
the square in R^d gives

    m^(-d/2) exp[-sum_(i<j in A)|z_i-z_j|^2/(2ms)]
      = exp[-E_perp/(2s)] C_d integral product_(i in A) phi_i(u) du.

The same positive factor exp[-E_perp/(2s)] occurs for every subset.
Inclusion-exclusion therefore converts the alternating sum into

    exp[-E_perp/(2s)] C_d integral
       product_(i in B) phi_i(u) product_(l in L)(1-phi_l(u)) du.

This is strictly positive. The first product is positive and integrable;
the second lies in [0,1] and vanishes only at a finite set of centers.
Those points have zero Lebesgue measure since d>=1. Repeated centers,
zero-dimensional remaining span and r=0 cause no exception. In the
zero-span case one still integrates in R^d, with zero padding.

The important dimensional point is that the full tuple is never claimed
to lie in R^d. Only the r remaining vectors must fit there. The removed
positive-block energy is retained exactly. This supplies the sign even
when the original tuple has affine rank six.

## 2. Check the normalization from the physical density

Write C=(2 pi s)^(-3/2), f=mu*gamma_(3,s), g=(T#mu)*gamma_(3,s),
F=f/C and G=g/C. Then

    d_m=C integral(G^m-F^m),       a_(m-2)=d_m/[m(m-1)].

For m independent labels let S_x and S_y be the sums of all unordered
squared distances. Direct Gaussian integration gives

    d_m=m^(-3/2) E[exp(-S_y/(2ms))-exp(-S_x/(2ms))].

This classical product calculation is also recorded in
[Aishwarya--Li, equation (61)](https://arxiv.org/html/2609.07041v2).
No majorisation statement is a premise of it. Interpolate squared
distances by z_i(t)=(sqrt(1-t)X_i,sqrt(t)TX_i). Put
Delta_ij=|X_i-X_j|^2-|TX_i-TX_j|^2>=0. The scalar derivative contributes
sum Delta_ij/(2ms). Division by m(m-1) and exchangeability contribute
binom(m,2)/[m(m-1)]=1/2. Consequently

    a_(m-2)=(1/(4s)) E[Delta_12 integral_0^1
        m^(-5/2) exp(-S(t)/(2ms)) dt].

In particular the effective Gaussian dimension is **five**, not six;
the power m^(-5/2) comes from the three-dimensional endpoint integral
and its scalar derivative. The actual intermediate points may remain
in R6. Replacing that exponent by -3 or discarding its additional
factor 1/m would invalidate the argument.

Couple the finite differences by using k+r+2 iid labels, with a fixed
positive block B of size k+2 containing labels 1 and 2. The remaining
r labels supply inclusion-exclusion. Unused labels integrate to one;
the distinguished loss Delta_12 never depends on which are omitted.
Section 1 with d=5 now gives a strictly positive bracket at every
tuple and every t whenever r<=5. This proves the stated A_(k,r)>=0.

If D=E Delta_12>0, positive loss has positive probability. The bracket
is continuous and strictly positive in t for each tuple, so its time
integral is positive. This proves strictness without taking a possibly
non-strict finite-atomic limit. If D=0, the nonnegative loss is zero
almost surely, giving equality. Bounded support dominates all distance
losses and scalar kernels, justifying these finite sums, expectations
and time integrations directly for diffuse laws.

No continuously chosen projection, measurable orthonormal basis or
common five-dimensional motion is needed: the bracket itself is an
explicit measurable scalar expression, and the geometric identity proves
its sign pointwise. This avoids a selection issue at rank-changing tuples.

## 3. Verify the stronger polarized assertion

Positivity of a polynomial on the weight simplex would not imply
positivity of each of its coefficients. The author correctly proves
the latter separately, using the normalization from the earlier
[weight-cell source, Sections 2--3](../gaussian_beta_weight_certificate/PROOF.md).

Here is a direct coefficient check. Set M=N+2 and fix a distinguished
pair and a subset A containing it, |A|=q+2. Cancel the common factor
1/(2s) in the differentiated formulas. The polarized moment expansion
assigns its Gaussian symbol coefficient

    (-1)^(q-k) (N+1) binom(N,k) binom(N-k,q-k)
        /[(q+2)(q+1) binom(N+2,q+2)].

The positive-block expansion assigns it

    (-1)^(q-k) binom(q,k)/M,

since there are binom(q,k) choices of the k additional positive positions
inside A. Factorials make these equal, including k=0 and k=N. The full
coefficient is thus a sum over pairs and k-subsets of positive integrals,
with the factor Delta_ab/(2sM). There are N-k remaining factors.
For N-k<=5, Section 1 proves nonnegativity and the claimed strictness.

All subsets select positions, not distinct site values. Coincident or
repeated labels keep their multiplicities. Every pair occurs in the
grouped formula; thus one positive pair is enough for strictness, while
all zero pair losses force zero. This also handles faces of the prior
weight simplex without a minimum-weight assumption.

The supplementary checker expands both definitions into rational maps
indexed by (distinguished pair, selected positions). It compares every
symbol, rather than just comparing total counts or checking the displayed
factorial identity numerically. It performs this check for all 36 pairs
0<=k<=N<=7, including identities outside the proved sign strip. The
combinatorial identity holds there too; its sign is not asserted there.

## 4. Downstream conclusions of the projection theorem

Tonelli applied to the source and target separately gives

    a_j=integral_0^1 u^j H(u) du,
    A_(k,r)=integral_0^1 u^k(1-u)^r H(u) du,

where H(u)=H_g(Cu)-H_f(Cu). This verifies consistency with the
[existing global criterion](../gaussian_majorisation_global_criterion/PROOF.md).
It also proves the claimed convex-energy interpretation after integrating
U''(u)=u^k(1-u)^r twice, and continuing linearly above one.

The projection theorem signs every column with N-k<=5. Therefore a finite
certificate workflow may omit those six columns at every degree and all
their polarized weight coefficients. Entire rows N<=5 are nonnegative;
at N=6 only k=0 remains unsigned by that result alone. The affine theorem
reviewed next signs this entry too. These tests use replica positions,
and those positions may repeat site labels.
There is no inference that a counterexample needs eight distinct atoms.

The projection theorem does not sign every convex polynomial test. It proves no
pointwise sign of H, supplies no uniform positive numerical lower margin,
and constructs no low-dimensional contraction. Those distinctions keep it
separate from the geometric class theorem and the numerical cell margins.
The full conjecture still requires all remaining beta columns, or another
argument supplying the same pointwise hinge comparison.

## 5. The affine offset signs the seventh column and gives a margin

For the additional argument, first collapse the p=k+2 positive factors
to their mean zbar, retaining their scatter Q0. With w_i=z_i-zbar for
the q remaining positions, the exact variance update for any subset B is

    Q_(base union B)=Q0+sum_(i in B)|w_i|^2
                          - |sum_(i in B)w_i|^2/(p+|B|).

If the remaining affine span has dimension at most five, write
w_i=v0+v_i where v0 is its nearest point to zero. Then v0 is orthogonal
to its direction space, all v_i are in that space, and for ell=|B|,

    Q_(base union B)=Q0+sum_(i in B)|v_i|^2
         - |sum_(i in B)v_i|^2/(p+ell) + p ell |v0|^2/(p+ell).

Six remaining points always have affine dimension at most five. This
uses affine dimension, not the dimension of their linear span from zero.
The previous projection theorem could not discard the last offset term.

Put beta=p|v0|^2/(2s). Directly summing the Poisson series gives

    exp[-beta ell/(p+ell)]
       = exp(-beta) sum_(n>=0) beta^n/n! [p/(p+ell)]^n.

The factor in brackets is the ell-th moment of exp(-E), for E exponential
of rate p. Consequently the whole expression is the ell-th moment of
Theta=exp(-sum_(i=1)^J E_i), with J Poisson(beta), 0<Theta<=1 and
Pr(Theta=1)=exp(-beta). This is a positive probability representation,
including beta=0 and ell=0. No sampled approximation is involved.

Completing the square in five dimensions and using that representation
turns the alternating kernel exactly into

    K=exp[-Q0/(2s)] E_Theta C5 integral
           exp[-p|u|^2/(2s)] product_i(1-Theta phi_i(u)) du,

where phi_i(u)=exp(-|u-v_i|^2/(2s)). Finite inclusion-exclusion permits
the exchanges; the final nonnegative integral is also finite, bounded
by the integrable base Gaussian. This proves the q<=6 sign. The same
formula works whenever the remaining affine dimension is at most five,
even if there are more remaining positions. The q=0 case is its direct
empty-product version with beta=0.

For the claimed quantitative bound, suppose the separately translated
endpoint centers lie in B_R and put r=R/sqrt(s). Every lifted center
and its base mean then lie in B_R. The bounds used in the proof are

    Q0<=pR^2,  |w_i|<=2R,  |v0|<=2R,  |v_i|<=2R,
    beta<=2pR^2/s.

The bound on v_i follows by orthogonality, not by a triangle inequality
that would give 4R. Keep the event Theta=1. In R5 integrate over the box
whose first coordinate is in [2R+sqrt(s),2R+2sqrt(s)] and whose other
coordinates are in [0,sqrt(s)]. Its volume is s^(5/2); its points satisfy

    |u|^2/s <= (2r+2)^2+4,  |u-v_i|>=sqrt(s).

Thus each remaining factor is greater than 1/3, using exp(1/2)>3/2.
Also C5 s^(5/2)=(2 pi)^(-5/2)>1/256. Combining the base scatter,
the Poisson atom and the Gaussian on this box gives

    K >= exp[-(p/2)(9r^2+8r+8)]/(256*3^q).

Inserting the already checked outer factor
(N+1)binom(N,k)/(4s) and averaging the distinguished loss proves

    b_(N,k) >= (N+1)binom(N,k)/(1024*3^q*s)
                    * exp[-(p/2)(9r^2+8r+8)] D,   q=N-k<=6.

The positive constant proves strictness when D>0. When D=0, nonnegative
continuous pair loss has zero integral on supp(mu)^2 and therefore
vanishes there; the support map preserves all distances. Congruence of
the Gaussian convolutions gives equality. This verifies the precise
support-isometry alternative, including diffuse laws.

For the stated compact set with s=1 and R=2l, the exponent is
p(18l^2+8l+4). The elementary e<4 gives the published rational lower
bound with 2^[-2p(18l^2+8l+4)]. This conditional substitution into the
specified radius bound is accepted. It does not independently review
the localization theorem that produced the compact frontier, nor does
it make the remaining columns nonnegative.

The polarized normalization in Section 3 applies unchanged to this K.
It proves the seven-column coefficient assertion before averaging any
weights. The two reviewed theorems leave b_(7,0) undecided, while
b_(6,0) is signed. There are nine replica positions in the former; this still
does not raise the minimum distinct support size above the prior boundary.

The listed residual multiplicity cases follow directly by counting
distinct labels left after a distinct-label pair is removed. Seven
distinct labels require the two removed labels both to have multiplicity
at least two, forcing (2,2,1,1,1,1,1). Eight require the one doubled
label and a singleton; nine allow any pair. Smaller numbers leave at
most six distinct points. This elementary classification is consistent
with the claimed pruning boundary. The separate explicit flap determinant
fixture and its author enumeration are not independently reproduced here.

## 6. Independent finite evidence and remaining trust

The new standard-library checker uses rational squared-distance matrices.
It centers the entire fixed tuple and forms the projected Gram matrix
through an exact Schur complement. Seven controls include full rank six,
large positive blocks, singleton blocks, absent remaining factors,
coincident points and repeated remaining points. A separate eight-site
coordinate-fold contraction has 28 pairs, 19 strict losses and paired
rank six. Its midpoint distances are computed exactly as (D_x+D_y)/2.

The checks cover 193 linear-projection subsets, 194 affine-offset subsets,
147 scalar controls and 31,234 individual polarized symbols in 36
expansions. Affine controls recover the nearest-point norm from squared
distances and verify the update at every subset, including a genuine
full-rank-six contraction with a nonzero offset. Seven deliberate mistakes
are rejected: an
arbitrary center, a dropped orthogonal energy, six independent remaining
vectors, an empty positive block, an omitted subset average and a wrong
total-position divisor, and seven affine-independent remaining points.
Both ordinary and optimized Python runs match
the same compact expected record.

These are finite checks of algebra and normalization, not numerical
Gaussian sign tests or exhaustive tests of the universal theorem.
Gaussian integration, integrability, strictness and the all-parameter
conclusion are justified by the written reconstruction above. No proof
assistant, interval quadrature, hidden certificate or external dataset
is used. Source publication itself is not an additional proof.
