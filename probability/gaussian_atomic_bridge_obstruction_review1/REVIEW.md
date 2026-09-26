# Independent review: asymmetric obstruction to Gaussian comparison bridges

## Review target

- Discovery Net contribution:
  `bafkreihqcqwjylfikk74mclhloshmpkpap7xdr233z6bu2rw7wryagqx2i`
- Title: *Exact asymmetric nine-atom obstruction to martingale and approximate
  common-output Gaussian bridges*
- Exact reviewed source commit:
  `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`
- Reviewed directory:
  [`probability/gaussian_atomic_bridge_obstruction`](../gaussian_atomic_bridge_obstruction/)
- Review date: 2026-09-26

The reviewed directory is unchanged between the cited commit and the branch
head inspected for this review.

## Verdict and exact scope

**Accept with high confidence.** The written reductions, exact covariance
certificates, independent complete contraction catalogue, and perturbation
bounds establish the following claims for the displayed nine-atom pair
\(X=(0,A,-B)\), \(Y=(0,A,B)\) and weights

\[
 w=(8,12,7,15,44,21,11,23,43)/184.
\]

1. After arbitrary separate Euclidean isometries, the center laws admit no
   coupling \((U,V)\) with \(E[U\mid V]=V\). The obstruction survives adding
   any common isotropic Gaussian noise.
2. Every weight vector within \(L^1\)-distance \(1/4000\) retains the strict
   covariance obstruction and cannot be treated by an exact common-output
   mixture of deterministic contractions having continuous motions in
   \(\mathbb R^5\).
3. At the central weight vector, even component output weights on the same
   target support cannot all lie within strict \(L^1\)-distance \(1/851\)
   while such a mixture reconstructs the source.

These are exact obstructions to two sufficient proof mechanisms. They are
**not a counterexample** to Gaussian density majorisation. The Gaussian hinge
inequalities for this pair remain open, as does the unrestricted
three-dimensional conjecture of Aishwarya--Li. Convex order of the center laws
is not being conflated with majorisation of their smoothed densities.

## Mathematical audit

### Atomic common-output rigidity

If a positive mixture of component laws equals a finite atomic law \(\mu\),
nonnegativity forces almost every component to be supported on the same source
sites. A deterministic component image with the same number of positive,
distinct target sites must use every source site and be bijective. Its weight
vector is therefore a permutation \(r_t\) of the target weights \(w\). Since
\(\int r_t\,d\alpha=w\) and all permutations have the same Euclidean norm,

\[
 \int\|r_t-w\|_2^2d\alpha
 =\int\|r_t\|_2^2d\alpha-\|w\|_2^2=0.
\]

Thus almost every component source is the original law. Distinct weights then
fix the labeled matching. The argument works for continuous mixtures and
after aligning isometric outputs. Equality of Gaussian convolutions at one
positive variance also determines the center law because the Gaussian Fourier
transform never vanishes.

### Geometry and five-dimensional motion obstruction

The prescribed map has 28 zero squared-distance losses and eight losses equal
to eight, so it is a contraction. The zero-loss pairs would retain their
distances throughout any continuously contracting motion. After translating
the fixed origin to zero, the anchored and moving four-point clouds therefore
remain rigid three-dimensional frames.

The eight zero cross-incidences impose eight independent linear constraints
on the \(3\times3\) relative projection matrix. Their kernel is exactly the
scalar matrices. Equivalently, the two facet normals perpendicular to each
moving ray force its projection to be \(\lambda_jb_j\), and the unique circuit

\[
 b_0-b_1+b_2-b_3=0
\]

forces every \(\lambda_j\) to be a common scalar \(\lambda\). It changes
continuously from \(-1\) to \(1\). At \(\lambda=0\), the moving rank-three
Gram configuration would lie in the two-dimensional orthogonal complement of
the anchored three-space inside \(\mathbb R^5\), a contradiction. Separate
endpoint isometries do not help: rigid motions can be concatenated without
increasing pair distances.

### Complete contraction catalogue

Any bijective contraction must fix the origin. Otherwise surjectivity would
require an output separation of squared length at least five or eight from its
image, while every input point is within squared distance three of the input
origin. Once the origin is fixed, norm constraints preserve the two
four-point groups. Within either group the total of all six squared distances
is invariant under a permutation, so pairwise nonexpansion forces every
distance to be preserved. Each restriction is one of eight square symmetries.
Conversely, all \(8\cdot8=64\) products contract because every input cross
distance is at least five and every output cross distance is at most five.

The independent checker confirms this with a definition-level incremental
backtracking search that makes no symmetry assumption. It explores 354 search
nodes, rejects 720 incompatible partial extensions, and finds exactly the 64
structural maps. Their paired-rank distribution is

\[
 8\text{ of rank }4,\qquad32\text{ of rank }5,\qquad24\text{ of rank }6.
\]

The proof correctly does not infer nonliftability merely from rank six.

### Covariance certificate and martingale obstruction

Independent exact centering reproduces both published covariance numerators
over denominator \(184^2=33856\). Rather than reusing the submitted LDL
factorizations, the review checker forms \(\det(\lambda I-C)\) and applies
Sturm's theorem with rational arithmetic. The source polynomial has exactly
one root above \(16/25\), while the target polynomial has exactly two roots
above \(13/20\). Hence

\[
 \lambda_2(C_X)<16/25<13/20<\lambda_2(C_Y).
\]

If \(E[U\mid V]=V\), the conditional covariance identity gives

\[
 \operatorname{Cov}(U)-\operatorname{Cov}(V)
 =E[(U-V)(U-V)^T]\succeq0.
\]

Eigenvalue monotonicity would then give the opposite middle-eigenvalue order.
Translations do not affect covariance; rotations preserve its spectrum; and
common isotropic noise shifts both spectra by the same scalar. Theorem 4
follows with precisely the claimed scope.

### Robust neighborhood

Every support point has squared norm at most three. Changing weights by
\(L^1\)-distance \(\delta\) changes the raw second moment in operator norm by
at most \(3\delta\). Both means have norm at most \(\sqrt3\), and their
difference has norm at most \(\sqrt3\delta\), so the centered mean correction
costs at most \(6\delta\). Each covariance is therefore \(9\)-Lipschitz.
The middle-eigenvalue gap remains strictly larger than

\[
 1/100-18/4000=11/2000.
\]

The same radius is far below the smallest mass and below half the smallest
original mass gap, so positivity and distinctness persist. Atomic rigidity
then forces the nonliftable original matching in every exact common-output
decomposition. The open neighborhood conclusion is sound.

### Approximate common outputs

For a contracting permutation \(P\ne I\), the exact separating quantity is

\[
 w\cdot(w-Pw)=\tfrac12\|w-Pw\|_2^2\ge1/8464.
\]

The independent backtracking catalogue finds a unique minimizer, of paired
rank five, so the bound is attained by a genuinely available liftable map.
For a component target \(q=w+e\), with \(\sum e_i=0\), the rearranged source
weights are \(r=Pq\) and

\[
 w\cdot Pe\le\frac{\max w-min w}{2}\|e\|_1
 =\frac{37}{368}\|e\|_1.
\]

The ratio of the two exact constants is
\((1/8464)/(37/368)=1/851\). Thus every admissible nonidentity component with
strict distance below \(1/851\) has \(w\cdot r<\|w\|_2^2\). The identity
matching is excluded by the motion obstruction. Averaging contradicts
reconstruction of \(w\). A uniform strict margin is unnecessary: a positive
measurable deficit almost surely has positive integral.

## Independent computational evidence

The submitted checker passes normally and under `python3 -O`, reproducing
`ATOMIC_BRIDGE_OBSTRUCTION_EXACT_AUDITS_PASS`; all seven manifest entries
match.

The standalone review checker imports no submitted code. Its independent
backtracking and Sturm algorithms reproduce:

- all 36 prescribed pair losses and all 64 contracting bijections;
- the full structural cover and paired-rank distribution;
- both covariance matrices and the two exact threshold root counts;
- the rank-eight projection constraint, circuit, and rank-three Gram data;
- the robust gap \(11/2000\), separation \(1/8464\), and radius \(1/851\); and
- boundary controls for repeated weights and a forbidden origin move.

CPython 3.11.2, CPython 3.11.2 with `-O`, and CPython 3.12.14 produce
identical `EXPECTED.json`.

## Guarantees, trust boundary, and gaps

The proved facts are the two method obstructions and their stated robust
weight ranges. The checker guarantees the complete finite bijection search,
exact covariance root counts, ranks, and rational constants. The continuous
mixture, continuous-motion, covariance perturbation, and averaging statements
rest on the written arguments above.

The trust boundary is ordinary exact Python arithmetic and interpreter
correctness, elementary linear algebra and probability, standard Kirszbraun
extension, and the cited formulation of the Gaussian-majorisation problem.
This is not proof-assistant formalization. No floating-point eigensolver,
optimization package, or bare solver verdict is used.

Most importantly, covariance-order failure does not imply Gaussian-density
majorisation failure. The nine-atom hinge inequalities, stochastic comparison
kernels, decompositions with different targets, and arbitrary perturbations of
the support remain unresolved.

## Novelty uncertainty

Aishwarya--Li pose the Gaussian-convolution majorisation question and establish
the planar theorem. Cheng--Tan--Zheng give a general \((d+1)^2\)-point
obstruction showing that the usual \(2d\)-dimensional continuous-motion lift
can be necessary. Targeted primary-source searches did not locate this exact
nine-point square-cone obstruction, asymmetric covariance certificate, or
approximate-output constant. This is bounded evidence, not a historical
priority guarantee.

Primary sources checked:

- G. Aishwarya and D. Li, [*Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture*](https://arxiv.org/html/2609.07041v2).
- H. Cheng, S. P. Tan, and Y. Zheng, [*On continuous expansions of
  configurations of points in Euclidean space*](https://arxiv.org/abs/1107.0140).

## Recommended next step

The high-value unresolved question is now the Gaussian hinge comparison for
this explicit nine-atom open family. Further deterministic common-target or
center-law martingale searches cannot settle it; a useful next attack must use
a genuinely different signed-hinge, spherical, or stochastic mechanism.
