# A certificate for the first unsigned beta test on an asymmetric flap region

Author proof with an exhaustive rational interval computation. Independent
mathematical review and formalization are pending. The unrestricted R3
Gaussian-majorisation conjecture remains open.

## 1. Exact region and conclusion

Take the asymmetric orthocentric tetrahedron

    v0=(0,0,1), v1=(2,0,-1), v2=(-1,3,-1), v3=(-1,-1,-1).

Its off-diagonal inner products are -1, and h_i=|v_i|^2+1 are (2,6,12,4).
This is the rational example in researcher 7's
[two-template reduction](../gaussian_flap_tournament_reduction/PROOF.md),
not a new geometric construction. Form sixteen labelled sites:

    x_i=y_i=v_i;      x_ij=v_j-v_i, y_ij=v_j+v_i, i!=j.       (1)

Write D^x,D^y for their squared-distance matrices. The four anchors come
first. For edges (01,02,03,12,13,23), list the low-to-high and high-to-low
flaps consecutively. This differs from the older regular fixture's ordering;
[EXPECTED.json](EXPECTED.json) gives every label and coordinate explicitly.

Now let v'_0,...,v'_3 be any affinely independent tetrahedron with

    v'_i . v'_j = -c < 0 for i!=j,

and construct its sixteen sites x',y' by (1). Allow every variance s>0
for which the following finite, closed metric conditions hold:

    | |x'_i-x'_j|^2/s - D^x_ij | <= 1/100,
    | |y'_i-y'_j|^2/s - D^y_ij | <= 1/100, for every i<j.     (2)

This is a nonempty region, with the displayed fixture and s=1 in its
relative interior. The shape parametrization in the cited reduction is
continuous near (a,b,d)=(1,2,3), so (2) contains an open neighborhood of
that shape and variance, within the orthocentric family. No floating
coordinate or unspecified search tolerance defines the region.

Give all sixteen labels arbitrary nonnegative masses summing to one.
Put f=mu*gamma_s, g=(T#mu)*gamma_s, C=(2 pi s)^(-3/2), and use the
established normalized moments and beta tests

    d_m=C^(1-m) integral(g^m-f^m),  a_j=d_(j+2)/[(j+1)(j+2)],
    b_(N,k)=(N+1) binom(N,k) sum_(l=0)^(N-k)
                                      (-1)^l binom(N-k,l) a_(k+l). (3)

**Theorem.** Every law in (1)-(2), at every allowed variance and every
weight vector including all zero-weight faces, satisfies b_(7,0)>=0.
Together with researcher 2's independently reviewed
[seven-column theorem](../gaussian_beta_pair_conditioning/PROOF.md),
this signs the entire row N=7 on this region.

This is a concrete certificate for the first entry beyond that universal
theorem. It is not an eighth universal column, a hinge sign, an all-order
certificate, or a new Kneser--Poulsen case. No conclusion is drawn about
the still-unsigned entries in higher rows or other parameter regions.

After dividing coordinates by sqrt(s) and translating each endpoint's
anchor 0 to zero, (2) gives both radii at most sqrt(19+1/100)<6.
There are sixteen atoms. Thus the theorem signs an actual region of R3's
[original compact frontier K_3](../gaussian_prior_localization/DEFECT_LOCALIZATION.md),
with its whole weight simplex. It also fits the larger allowed atom budget
at k=3 in the [paired-cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md).
No localization error is subtracted to infer this exact sign.

## 2. A stronger certificate on each surviving ten-site selector

For each edge {i,j}, select one directed flap. Include all four anchors.
As in the cited reduction, a selection is a tournament on four vertices;
a sink has no outgoing edge. Exactly 32 of the 64 selectors have no sink.
The calculation below includes **all 32 labelled selectors**. Using only
two representatives at one fixed asymmetric shape would be insufficient.

For any one of these selectors, take arbitrary paired points z_i,t_i in
R3 on its ten labels. Suppose they are an actual contraction and their
squared distances divided by s satisfy the selected part of (2).
They need not themselves form a flap configuration. Give them any ten
probability weights p. Let Q_d(p), d=7,8,9, be the probabilities that nine
independent labels have, respectively, multiplicities

    (2,2,1,1,1,1,1),   (2,1,1,1,1,1,1,1),   (1,1,1,1,1,1,1,1,1).

The exhaustive certificate proves the stronger statement

    b_(7,0) >= Q_7(p)/1000 + Q_8(p)/100 + Q_9(p)/30.        (4)

The right side is an explicit polynomial, with no lower weight bound:

    Q_7 = (9!/4) sum_(|A|=7) (product_(i in A) p_i)
                                      sum_(i<j in A) p_i p_j,
    Q_8 = (9!/2) sum_(|A|=8) (product_(i in A) p_i) sum_(i in A) p_i,
    Q_9 = 9! sum_(|A|=9) product_(i in A) p_i.              (5)

In particular (4) is strict whenever at least seven of these weights are
positive. For smaller supports it still proves nonnegativity. The
contraction hypothesis is essential: an arbitrary matrix inside a metric
box is neither asserted Euclidean nor asserted contractive.

These ten-site regions contain strict rational contractions in their
relative interiors: keep the displayed source and replace each selected
target by (19999/20000)y_i, at s=1. The selected target sites are distinct,
so all 45 pair losses become strictly positive. Their centre squared
distances are at most 24, and their changes are less than 24/10000<1/100.
Thus these are concrete signable finite inputs with an open margin in
the contraction constraints, not only the original equality faces.

## 3. Polarization and analytic removal of the other tuples

Scale to s=1. For a tuple A of m positions put

    S_x(A)=sum_(a<b in A) |x_a-x_b|^2,
    K_m(A)=m^(-3/2) [exp(-S_y(A)/(2m))-exp(-S_x(A)/(2m))]. (6)

The Gaussian product identity gives d_m=E K_m on independent replicas.
Homogenizing (3) to nine replicas gives b_(7,0)=E c(alpha), where

    c(alpha)=(1/9) sum_(A subset [9], |A|>=2) (-1)^|A| K_|A|(alpha_A). (7)

Indeed the multiplier of each m-subset simplifies exactly:

    8 binom(7,m-2)/[m(m-1) binom(9,m)]=1/9.

Subsets select **positions**, so repeated labels retain their binomial
multiplicities. This is the existing
[weight-polarization identity](../gaussian_beta_weight_certificate/PROOF.md)
at the new, first unresolved test, not an assumption about polynomial
coefficients following from positivity on a simplex.

The affine-conditioning proof in the seven-column source supplies a
stronger pruning rule than a bound on the full tuple's paired rank.
Differentiate (6) along interpolated squared distances. For each
distinguished pair a,b the multiplier is its nonnegative distance loss.
The remaining alternating Gaussian kernel is nonnegative whenever the
remaining seven positions have affine span at most five in the paired
interpolation space. Six or fewer distinct labels suffice. A pair of
identical labels has zero distance loss. The proof of this rule is that
source's positive Poisson/Gaussian representation, not a numerical premise.

Consequently, only the three patterns in Section 2 need enclosure. To
check completeness, remove two different labels from a nine-tuple. Seven
different labels can remain only if there were nine distinct labels, or
eight with one doubled label, or seven with two doubled labels. A tripled
label with six singleton labels does not add a case: removal of two equal
labels has zero pair loss; removal of different labels leaves at most six
distinct labels. Every other tuple is therefore nonnegative analytically.

On ten labels there are binom(18,9)=48620 unordered nine-tuples. Exactly

    binom(10,7) binom(7,2)=2520,
    binom(10,8)*8=360,
    binom(10,9)=10

have the three respective exceptional patterns. The other 45730 need no
interval sign calculation. This includes the equality and zero-weight
boundaries without subtracting a uniform absolute error there.

## 4. Exact interval computation

For each subtuple A let r(A) count its pairs of positions with different
labels. The zero diagonal is exact even for repeated labels. If S_x^0,S_y^0
are its integer centre sums, condition (2) gives, with e=r(A)/100,

    E_x in [max(0,S_x^0-e)/(2m), (S_x^0+e)/(2m)],
    E_y in [max(0,S_y^0-e)/(2m), (S_y^0+e)/(2m)].            (8)

Monotonicity of exp(-u), together with the actual contraction, encloses
K_m by m^(-3/2) times

    [max(0, exp(-E_y^upper)-exp(-E_x^lower)),
     max(0, exp(-E_y^lower)-exp(-E_x^upper))].              (9)

[certificate.py](certificate.py) evaluates (9) using the hash-pinned
[rational enclosure module](../gaussian_majorisation_hankel_transport/bounds.py).
Its reduced exponential series, tail estimate, reciprocal and squarings
use outward rational rounding. Square roots use integer square roots.
The kernel intervals are rounded outward to multiples of 10^-24 after
using 34 requested decimal digits internally. Integer interval summation
then evaluates (7) over denominator 9*10^24, reversing interval endpoints
for odd subset sizes. Precision changes enclosure width, never validity.

Every enumerated subtuple's pair-distance exponent is also checked against
the independent centroid formula m sum |z_i|^2-|sum z_i|^2. All 32 selectors
and all their exceptional tuples pass the corresponding strict lower
bound in (4). There are 92480 coefficient occurrences, 47936 distinct
coefficients after overlap between selectors, 171291 distinct subtuples,
and 18694 distinct scalar interval calculations. The complete interval
stream is regenerated and hashed, rather than shipped as a large file.

The exact overall lower minima for the three patterns are respectively

    449996170999398783371 / 300000000000000000000000,
    469723366661194924601 / 37500000000000000000000,
    162019138383563184993907 / 4500000000000000000000000.

They exceed 1/1000, 1/100 and 1/30. The per-selector minima, first minimizers,
counts and stream hash are in [EXPECTED.json](EXPECTED.json). Combining
these bounds with the analytically nonnegative tuples in (7) proves (4).

## 5. Return to all sixteen masses at a fixed target

Write the four anchor masses as alpha_i and the directed flap masses as
beta_ij. Set q_{ij}=beta_ij+beta_ji. A random selector chooses i->j with
probability beta_ij/q_ij when q_ij>0, independently across edges; for q_ij=0
use probability 1/2. Denote its probability by lambda_sigma. The source
law is the lambda-mixture of selector source laws. Every selector has the
**same target law**, because y_ij=y_ji. Its ten weights, up to labelling,
are always p=(alpha_0,...,alpha_3,q_01,...,q_23).

To justify the functional direction explicitly, on [0,1] put

    U(u)=((1-u)^9-1+9u)/72,   U''(u)=(1-u)^7.

Extend U by its tangent line for u>=1. Then U is convex, U(0)=U'(0)=0,
and all evaluated Gaussian densities divided by C lie in [0,1]. Direct
expansion gives

    b_(7,0)=8 C integral [U(g/C)-U(f/C)].                  (10)

The integrals are finite, since U is O(u^2) near zero and f,g are bounded
probability densities. Convexity and the common target therefore give

    b_(7,0)(original) >= sum_sigma lambda_sigma b_(7,0)(selector). (11)

Researcher 7's explicit R5 contracting motion proves all Gaussian hinge
comparisons for each of the 32 selectors with a sink, at every variance
and every weight. It thus signs (10) for these selectors. Applying (4) to
the other 32 proves the theorem, and supplies the explicit stronger bound

    b_(7,0)(original) >= R [Q_7(p)/1000+Q_8(p)/100+Q_9(p)/30], (12)

where R=sum_(sigma without sink) lambda_sigma. For q_e>0 on every edge,

    R=1-sum_(k=0)^3 product_(j!=k) beta_jk/q_jk.

With zero q_e use the stipulated orientation probabilities. The four
sink events are disjoint. In particular the bound in (12) is strictly
positive if R>0 and at least seven of the ten target-site masses are
positive. No converse equality characterization is asserted here.

The original flap map is an actual contraction by the identities in the
cited reduction. The common-target step requires the exact geometry;
it is not asserted for arbitrary perturbations of all sixteen targets
that split their opposite-flap collisions. The standalone ten-site result
(4) does allow general Euclidean contractions within its metric box.

## 6. Dependency and verification boundary

This combines R2's accepted residual pruning, R7's exact selector reduction,
and the existing functional lane's interval polarization method to sign
a previously unsigned compact region. It does not extend R4's
[shallow-flap theorem](../gaussian_flap_depth_boundary/SUPPORT_SIGN.md):
that theorem proves all thresholds at a sufficiently small, parameter-
dependent depth. Here the depth is exactly one and the certificate is one
finite beta row, uniformly in its entire weight simplex. Neither statement
supplies the other's conclusion.

The target and Gaussian product formula are from
[Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The tetrahedral flap construction and the common-target lemma are credited
in R7's source. [INPUTS.json](INPUTS.json) pins the relevant source bytes
and commits. The R2 proof has independent agent acceptance, including the
[functional-lane audit](../gaussian_beta_conditioning_review_r8/REVIEW.md);
the new certificate and R7's full reduction do not acquire independent
acceptance merely from the checks here.

[verify.py](verify.py) independently classifies all 48620 tuple patterns,
checks the multiplicity normalization with exact artificial kernels,
reconstructs the geometry and selector coverage, and re-encloses the
three weakest tuples with an alternating exponential series that does not
use the producer's bounds module. These are author controls. They do not
replace exhaustive producer coverage, external review, or formalization.
The written Gaussian and convexity arguments, the analytic pruning and
sink-motion dependencies, and Python integer/Fraction arithmetic are
explicit trust boundaries. No quadrature, solver, floating sign, mesh in
weights, or hidden dataset is a premise.
