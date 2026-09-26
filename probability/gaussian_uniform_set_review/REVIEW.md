# Analytic review of the uniform lattice-set reduction

26 September 2026. Reviewer: analytic/optimal-transport lane, researcher 5.
Reviewed author: measure-localization lane, researcher 3.

**Verdict:** accept Theorem 1 of the pinned source and its rigid-packet
interaction identity (12). No mathematical correction to either is required.
The equivalence includes preservation of the supremal positive defect,
strict contraction between whole cubes, rational thresholds, and integer-square
variances. This does not prove the common sign or provide a counterexample.

Reviewed source:
[PROOF.md](../gaussian_uniform_set_reduction/PROOF.md), commit
`748304ec455b7c233da6931cbfed763105949a36`, SHA256
`be52e51607781f20f641ce1053d1fb452ba0c750ed75d0e5070956a3022203a5`.
The proof is unchanged by this review. [INPUTS.json](INPUTS.json) pins its bytes.

The review is separate from authorship of the reduction. The reviewer authored
the separately cited isometric-reference theorem. The paragraph applying that
theorem to a single cube is **excluded from independent acceptance here**.
Neither Theorem 1 nor (12) uses it. This is an internal team review, not external
human peer review, a priority assessment, or a proof-assistant formalization.
The author's finite checker and fixtures were not replayed as evidence for
the universal argument.

## 1. Precise accepted statement

Let Q=[-1/2,1/2]^3. For a finite list of integer source and target centers
X_i,Y_i, require, for i!=j,

    ||X_i-X_j||_infinity>=2,     ||Y_i-Y_j||_infinity>=2,
    |X_i-X_j|^2-|Y_i-Y_j|^2
       > 2||(X_i-X_j)-(Y_i-Y_j)||_1.                         (R1)

Put E=union_i(X_i+Q), F=union_i(Y_i+Q), with uniform probability densities
1_E/N and 1_F/N. Translate each source cube to its labelled target cube.
These are actual contractions of positive-volume supports, with equimeasurable
initial densities. The full bounded-law R3 Gaussian-majorisation assertion is
equivalent to its restriction to these pairs, variances q^2 for positive
integers q, and positive rational hinge thresholds.

Moreover, with H_f(a)=integral(f-a)_+, the supremum of

    max(0,H_(mu*gamma_s)(a)-H_((T#mu)*gamma_s)(a))             (R2)

over this discrete class equals the supremum over all bounded probability
laws, contractions, positive variances and nonnegative thresholds. This is
a supremum statement, not the existence of a uniform-set optimizer for a
given map. Both the law and the map change in the construction.

## 2. The estimates really preserve a hinge gap

For equal-mass probability densities f,g, the pointwise Lipschitz bound for
the positive part alone gives ||f-g||_1. The sharper bound used by the source
is also correct:

    |H_f(a)-H_g(a)|<=TV(f,g)=(1/2)||f-g||_1.                (R3)

To see the factor 1/2, suppose H_f(a)>=H_g(a) and use the maximizing set
{f>a} in the variational expression for H_g. The difference is at most
integral_{f>a}(f-g), which is at most integral(f-g)_+=TV(f,g). Interchange
f and g for the other direction. At a=0 both hinges are one.

For unit e, a directional derivative of gamma_s has L1 norm
sqrt(2/(pi s)). Integrating translations along the segment from x to y gives

    TV(gamma_s(. -x),gamma_s(. -y))
      <= |x-y|/sqrt(2 pi s).                                (R4)

Thus any coupling of two center laws bounds the TV distance of their Gaussian
convolutions by the mean displacement divided by sqrt(2 pi s). Mixtures do
not require a density or a least atom weight. The source and target errors
add in (R2); they cannot be replaced by only one of those errors.

For a change of probability weights from w to w', each endpoint density
changes in TV by at most (1/2)sum_i|w_i-w'_i|. Their combined gap error is
therefore at most sum_i|w_i-w'_i|, as stated in the source. Threshold continuity
at every positive a follows by dominated convergence, with dominating density
f for H_f. A strict gap cannot occur at threshold zero.

## 3. Quantifier order in the finite uniform approximation

Start with a specified positive gap d and any loss tolerance eta>0. A common
spatial scaling makes s=1 without changing the numerical gap: densities scale
by s^(-3/2), and the normalized threshold is a s^(3/2).

Partition the bounded source support into finitely many sets of diameter at
most r. Choose representatives from the actual support and retain their exact
images and cell masses. The coupled source and target displacements are each
at most r, so (R3)--(R4) give total error at most 2r/sqrt(2 pi). Merge duplicate
source sites and remove zero masses. The remaining distinct source sites
have a positive minimum pair separation.

Expand the source centers by 1+epsilon while leaving the targets fixed.
Every pair now has a strict contraction margin. Since there are finitely
many sites in a bounded set, the added Gaussian error tends to zero with
epsilon. Choose it only after choosing the finite approximation. Next a
sufficiently small generic target perturbation makes the target sites
distinct while preserving all strict inequalities. Rational approximation
of both coordinate lists and positive rational approximation of the weights
then preserve the strict inequalities, distinctness and nearly all the gap.
Openness is being used on finite lists, not uniformly over the original law.

Write the new weights n_i/N with positive integers n_i. For each old label
choose n_i distinct rational vectors d_(i,j), and replace it by equally weighted
labels with positions

    x_(i,j)=x_i+tau d_(i,j),
    y_(i,j)=y_i+(tau/2)d_(i,j).                              (R5)

Only now choose a sufficiently small positive rational tau. The list of
offsets is finite even though N may be large. Distances inside one old cluster
shrink by exactly 1/2; strict inequalities between different old clusters
persist by continuity. Both endpoint lists remain injective, with distinct
source labels carrying consistent images. The Gaussian errors tend to zero
by the coupling (R4). Repeating coincident labels without this separation
would not justify the next geometric step.

This gives distinct rational equally weighted points with strict pairwise
contraction. A positive rational threshold b can now be chosen with an
arbitrarily small additional error. Allocate a total budget less than eta/2
among these finitely many operations. Each operation permits any positive
budget after its predecessors are fixed. There is no circular demand for a
single perturbation size working before N or the strict margins are known.

## 4. The whole-cube condition and the second scaling

For two unit cubes with center differences u at the source and v at the
target, an arbitrary offset difference h ranges over [-1,1]^3. The squared
distance loss is affine in h:

    |u+h|^2-|v+h|^2=|u|^2-|v|^2+2(u-v).h.

Its minimum is exactly

    |u|^2-|v|^2-2||u-v||_1.                                (R6)

This is a minimum over the entire product of cubes. It proves the necessary
and sufficient nonstrict condition and the strict version in (R1). Center
contraction alone does not prove contraction of the thickened supports.

For the finite rational pair from Section 3, set
d_ij=|x_i-x_j|^2-|y_i-y_j|^2>0 and
l_ij=||(x_i-x_j)-(y_i-y_j)||_1. Choose an integer q clearing all coordinate
denominators, sufficiently large that

    q d_ij>2l_ij,
    q||x_i-x_j||_infinity>=2,
    q||y_i-y_j||_infinity>=2                               (R7)

for every distinct pair. Such denominator multiples exist because the lists
are finite and both endpoint configurations are injective. With X_i=q x_i
and Y_i=q y_i, the quadratic term in (R6) scales by q^2 whereas the offset
term scales by q. Thus (R7) gives exactly (R1), including strict separation
of the cubes themselves.

Gaussian scaling requires variance q^2 and threshold b/q^3. At those
parameters the point-law hinge difference equals the variance-one difference
at threshold b, with no multiplicative loss. Thickening each atom by an
independent uniform vector in Q costs at most sqrt(3)/2 in center displacement.
Apply (R4) with s=q^2 to **both** endpoint laws. The resulting gap error is

    sqrt(3)/(q sqrt(2 pi))<1/q.                             (R8)

Increasing q through denominator multiples makes this less than the remaining
eta/2 budget and preserves (R7). The final threshold is positive rational
and the variance is an integer square. The two initial densities are exactly
0 or 1/N because both cube unions are disjoint. Translation is a bijection
of their supports and has derivative I in each component interior.

The piecewise map is 1-Lipschitz on the whole union by (R6), including boundary
points and pairs from different components. Kirszbraun's Euclidean extension
theorem gives a full-space 1-Lipschitz map if the formulation requires one.
It gives no volume-preserving full-space extension, and the proof needs none.

## 5. Equivalence and supremum, without a hidden uniform bound

Every constructed cube pair is already an admissible pair for the full
conjecture, so its supremal defect cannot be larger. Conversely, Section 4
preserves any specified positive gap to within arbitrary eta. Taking eta<d
proves equivalence of the zero-defect assertions. Approximating every value
below the unrestricted supremum proves equality of the two suprema.

If the unrestricted supremum is zero, the reverse inequality is automatic.
No optimizer, limit of geometries, or interchange of an infinite family with
a sign statement is needed. The construction gives no bound uniform in the
original gap on N, coordinate denominators, perturbation scale or q. Existing
compact finite-atomic bounds therefore cannot be silently transferred to
these lattice parameters. The normal form also does not preserve an externally
specified atom mass, a fixed support map, or an indecomposable tight mesh.

## 6. The exact interaction statement is accepted; its sign is open

Let h=1_Q*gamma_(q^2), f_i=h(. -X_i)/N and g_i=h(. -Y_i)/N. Define

    I(f_1,...,f_N;a)=H_(sum_i f_i)(a)-sum_i H_(f_i)(a).

Since H_(c h)(a)=c H_h(a/c), translation invariance gives

    sum_i H_(f_i)(a)=sum_i H_(g_i)(a)=H_h(Na).

Consequently H_(sum f_i)(a)-H_(sum g_i)(a)=I(f_i;a)-I(g_i;a) exactly.
There is no omitted conditional comparison gap: every component is a
translate of the same density with the same mass. This validates (12).

The full question is therefore equivalent to nondecrease of this interaction
under every admissible whole-packet contraction. The equality of the individual
hinges does not order the two interactions. Although each interaction is
nonnegative, that is not an ordering between them. Nor does equimeasurability
at time zero imply comparison after Gaussian smoothing. These are precisely
the still-missing signs, rather than consequences of the reduction.

The earlier shifted-grid obstruction groups components into conditional laws
that need not be isometric. It does not contradict the present identical-packet
formulation. Conversely this formulation does not repair that false arbitrary-
packet interaction ordering. This review proves neither sign by changing
quantifiers between the two constructions.

## 7. Exclusions, provenance and attribution

The ancillary single-component reference-set paragraph depends on the reviewer's
own isometric-reference proof and is not granted independent acceptance here.
That proof continues to await an independent review. Source publication and
this review do not change its status. Likewise the reviewed equivalence does
not make the actual mixed source's maximizing set a single-component test.

The source's SOURCES.md labelled the reference theorem as researcher 2's work.
Its source commit identifies researcher 5; the attribution is corrected in
the accompanying metadata edit. This clerical change does not alter the
reviewed PROOF.md, its theorem, or its proof hash.

No numerical Gaussian integration, solver, finite-sign computation, new test
instance or computation-intensive checker is used in this review. The analytic
derivations above are the evidence; [REVIEW_SCOPE.json](REVIEW_SCOPE.json)
records the verdict and exclusions. The standard measure approximation,
Gaussian differentiation, scaling and extension ingredients are explicitly
separated from the unresolved interaction sign in [SOURCES.md](SOURCES.md).
