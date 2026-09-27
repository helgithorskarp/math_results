# Sources, dependencies and trust boundary

## Shift-averaging boundary supplement

[SHIFT_AVERAGING_BOUNDARY.md](SHIFT_AVERAGING_BOUNDARY.md) addresses the
specific proposed inequality that random source-grid shifts make the
target hinge interaction at least the source interaction. The eight-site
family has strict contraction, distinct images and paired affine rank six,
yet the reverse averaged inequality holds for sufficiently small scale.
The primary Aishwarya--Li Theorem 1.4 gives full majorisation for this
family because its straight trajectories contract every pair. This is
a method obstruction on positive examples, not a conjecture counterexample
or a new positive class. No numerical scale cutoff is claimed.

The [uniform localization proof](DEFECT_LOCALIZATION.md), source
`4ed178725774e2fd3bb486f952825f58e52766cc`, is now committed at graph h6134:
`bafkreibn7nmsfuqqf4uo3nl4zvws5jogxzphra2zan4a7kbmdkofatx72u`.
Its original body and all five initial relations were matched exactly.
The theorem used the source interaction as an error and never asserted
the false comparison. The scalar interaction is also used in the
[fixed-atom source](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
h6112; neither that reduction nor the compensation of a fixed atom is
changed here. The new signed test is proved directly by L1 translation
differentiation, a null Gaussian level, the divergence theorem and exact
cube partition probabilities. These standard tools carry no priority claim.

The prepublication refresh includes the following distinct dependencies:

- The [global interface](../gaussian_majorisation_global_criterion/INTERFACES.md),
  source `8b004c6a747883fcf96f895a052a292a62683f5f`, graph h6144,
  composes localization with moments and a new dominant anchor. Its
  additive errors remain valid; the present example does not justify
  dropping them or disprove a sharper inequality retaining conditional gaps.
- The [ordered-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md),
  graph h6140, asks for a flux sign under profile order and contact. A
  reversal of an unconditional quantity away from contact does not refute
  that conditional obligation. Our partition test does not address its sign.
- The [common-set equality faces](../gaussian_majorisation_minimax_faces/PROOF.md),
  source `e53ad777d2aaa0556e646d4db44a2afc7235c7d0`, graph h6142,
  give positive transfer for special source tests and an exact equality
  reserve. They do not establish arbitrary-set transfer, nor rely on the
  shifted-grid interaction comparison.
- The [finite orthogonal-rule obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md),
  graph h6126, concerns a different averaging operation. Our shifts are
  translations of a fixed-axis grid; no claim about averaging grid rotations
  or adaptively choosing partitions follows from our proof.

All seven other researchers' latest completed reports and relevant new
sources were inspected. The finite-certificate, rigid-mesh and geometric
handoffs preserve their stated boundaries. Researcher 7's latest completed
search report supplies no certified negative integrated witness. Incoming
citations of h6134 are not independent acceptance of its analytic proof.
The primary paper was refreshed live on 26 September 2026. The focused
literature/source inspection did not supply this particular grid interaction
test; no exhaustive novelty or priority claim is made.

[interaction_audit.py](interaction_audit.py) uses CPython 3.11+ and only
the standard library. Normal and optimized runs of `--check` produce
report SHA256
`ed59655a2912164a7b1ff2aa40f0e6131778b214ba7fef4667e1d57cd085ed75`.
The exact controls cover all cube cut masks and pair types, conditional
mass/threshold normalization, the split-count probability polynomial, Walsh
rank, straight-motion margins at three rational scales and the strict
rational radical margin. A corrupted expected report is rejected under
optimized Python. These checks do not compute Gaussian hinges or certify
their sign at any specified finite scale. The universal asymptotic and
sufficiently-small-scale conclusion remain a written proof, with independent
review and formalization pending. The earlier proofs and audit source/output
files are byte-preserved.

## Uniform defect localization supplement

[DEFECT_LOCALIZATION.md](DEFECT_LOCALIZATION.md) adds a sign-preserving
restriction to a spatial cell and the quantitative compact frontier
0<=D-D_k<4/k, with at most k^6 atoms and radius 2k at variance one.
It is a complete author proof awaiting independent review. Neither its
finite-dimensional maximum nor the full Gaussian comparison is settled.

The scalar hinge interaction in researcher 5's
[fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
graph h6112, is a useful dependency in discovering the partition argument.
Here it is proved for any finite number of components, with only the
source interaction charged to an error. The global hinge defect agrees
with [the earlier criterion](../gaussian_majorisation_global_criterion/PROOF.md),
graph h6088. The supplement proves all its analytic estimates directly;
it does not require the fixed-atom equivalence as a premise.

The previous [strict rational witness reduction](../gaussian_majorisation_rank_abel/PROOF.md),
graph h5964, provides qualitative finite witnesses. The earlier source-net
estimate in this packet depends on a given support's extent. The new step
is a uniform control of that extent in terms of the gap one is willing to
lose. It does not preserve exact minimizers, fixed atom masses, or a fixed
coordinate denominator. The diffuse-optimizer obstruction, graph h6122,
is therefore unchanged.

The latest [finite orthogonal averaging obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md)
rules out a universal finite averaging extension of the ordered-weight
certificate. Our partition argument neither uses that method nor assigns
a sign to any averaged Gaussian hinge. The [heat-profile analysis](../gaussian_majorisation_heat_profiles/PROOF.md)
and the [stability handoff](../gaussian_majorisation_open_stability/HANDOFF.md)
retain their explicit boundary and signed-threshold obligations. Restricting
to finitely many compact parameter regions does not discharge those signs.
The [axial review portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md)
and the ordered-weight geometric class keep their original scope; no new
Kneser--Poulsen consequence is claimed here.

The prepublication source refresh also inspected researcher 4's
[extremal-map reduction](../gaussian_majorisation_extremal_maps/PROOF.md),
source `c68eb50ea52c9b578e90e89b5954ea4c63a0d89a`, present in the freshly fetched main. It supplies
rigid tetrahedral support enlargements without a mesh-complexity bound.
Our new bound is on the witness before that enlargement. The two reductions
are independent and complementary; neither establishes the remaining sign.
These newer contributions had been published in source while their graph
commitments remained unconfirmed at the inspected index 6123.

The primary Aishwarya--Li source was refreshed live on 26 September 2026
and remains v2. Targeted searches for Gaussian majorisation, partition
localization and support bounds, together with the inspected team sources,
did not supply this quantitative restriction theorem. This is not an
exhaustive novelty assessment. Hinge superadditivity, random grid shifts,
Gaussian derivative estimates and compactness are elementary or standard
ingredients; no priority claim is made for them. Kirszbraun's classical
extension theorem is needed only if one insists that a finite contraction
be defined on all of R3, not for the localization inequalities themselves.

The supplementary standard-library Python checker is
[localization_audit.py](localization_audit.py). Run it with `--check`, also
under `python3 -O`. It checks three finite-cell families at all their
piecewise-linear knots, 36 exact one-coordinate grid crossings, five product
controls, the explicit endpoint-rounding pitfall, and a rational upper bound
on the constant in (2). The finite-cell controls are explicitly not Gaussian
data; one is deliberately negative to show why source overlap cannot be
discarded. [LOCALIZATION_EXPECTED.json](LOCALIZATION_EXPECTED.json) records
the exact output. No enumeration of k^6-site configurations, Gaussian
quadrature, optimization, external numerical library or proof assistant
is used. These checks supplement the universal written proof.
Normal and optimized CPython 3.11.2 produce report SHA256
`0ec4dc938214a44b0c70cc09b05f3cf3245451619c170977cca0556c8aa28c42`.
A damaged expected report is rejected under optimized Python. The original
minimax/sphere checker and its expected output remain unchanged.

## Primary literature

- M. Kirszbraun, *Über die zusammenziehende und Lipschitzsche Transformationen*,
  Fundamenta Mathematicae 22 (1934), 77--108,
  [publisher page](https://impan.pl/en/publishing-house/journals-and-series/fundamenta-mathematicae/all/22/0/93089/uber-die-zusammenziehende-und-lipschitzsche-transformationen).
  The classical Euclidean extension theorem identifies finite contractions
  with restrictions of globally defined contractions without increasing
  their Lipschitz constant. Our restriction and quantization themselves
  retain actual images and do not require a constructive extension.

- Gautam Aishwarya and Dongbin Li, *Gaussian Convolution, Internal Energies,
  and the Kneser--Poulsen Conjecture*,
  [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), 13 September 2026.
  Conjecture 1.1 is the target. The paper proves the full comparison in
  dimensions at most two, the pressure-class comparison in general
  dimensions, and the continuous-contraction and geometric transfer
  theorems. The present note supplies no additional positive sign for an
  arbitrary three-dimensional contraction.
- Maurice Sion, *On general minimax theorems*, Pacific Journal of
  Mathematics 8 (1958), 171--176,
  [publisher PDF](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-s.pdf),
  [DOI](https://doi.org/10.2140/pjm.1958.8.171).
  Theorem 3.4 supplies the separately continuous affine minimax exchange.
  The compact spaces, payoff and extremum attainment are checked explicitly
  in PROOF.md; no finite-dimensional assumption on the selector space is made.
- Boris S. Mityagin, *The Zero Set of a Real Analytic Function*,
  [arXiv:1512.07276](https://arxiv.org/abs/1512.07276).
  The null-level-set fact is used to make every volume-constrained optimum
  of a Gaussian mixture unique. The threshold maximization itself is proved
  directly by inequality (6), the usual superlevel-set or bathtub argument.
- The abstract relationship to statistical experiment comparison is
  classical; see Erik Torgersen,
  [*Comparison of Statistical Experiments*, Chapter 9](https://www.cambridge.org/core/books/comparison-of-statistical-experiments/majorization-and-approximate-majorization/C35D7CF186D95BA5E3F43D7C40E3E6C9).
  This note does not claim priority for minimax/decision-theoretic duality.
  It proves the specific common-set, contact-set and fixed-atom statements
  needed here and an explicit diffuse-optimizer obstruction.

Stone--Weierstrass, weak compactness of probabilities on a compact metric
space, and weak-star compactness of the L-infinity unit ball are standard
functional-analysis inputs. The spherical exponential-kernel injectivity
is proved directly using positive squared polynomial moments, without
importing a spherical-harmonic table or numerical spectral computation.

## Durable team inputs

The following public source was inspected against main at
`208c21bc66bfc4fd7a6801c1d3aadea038f94733`. The graph refresh indexed 6119.
Their stated review boundaries are retained.

- Named problem, graph
  `bafkreifx5vhi7azxuu4chant6r4c7vvgjsypwdoob4ug7ea2nmzctlsrhu`, height 5950.
- Researcher 5's [global criterion](../gaussian_majorisation_global_criterion/PROOF.md),
  graph `bafkreihp3see622wt3h2fxowhnp6cj4jtz5t53dxp5bmerz7aj5tfo2eeq`,
  height 6088. Its per-law endpoint coupling and complete beta/Hankel
  criteria concern the same hinge defect. Equation (9) here supplies the
  all-prior set-transfer version; it is not a competing transport construction.
- Researcher 5's [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
  source `138993ba3ec2efde720c789a2a3d887c9c417c69`, graph
  `bafkreievpgikszwz2kggan4dnfbbhvtvjohiycou6xuhlsqpxjvvxrhaai`, height 6112.
  This supplies the full-question importance of retaining an arbitrary
  rare packet. Our minimax identity holds independently; its use as an
  equivalent localized full-question obligation invokes that reduction.
  The rare-support bound is not uniform across its family.
- The [finite strict rational-witness reduction](../gaussian_majorisation_rank_abel/PROOF.md),
  graph `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`,
  height 5964. The diffuse-optimizer theorem does not contradict its
  finite strict witnesses or lower bounds on paired affine rank.
- Researcher 6's [axial robustness benchmark](../gaussian_axial_cone_rotations/ROBUSTNESS.md),
  source `a63bee4157117a2d2abb2a358119dfd57ebb5a9d`, graph
  `bafkreico6twre4tzlewepj3ej7vay764gyeajof4ni25s4jksd3p4sed2y`, height 6104;
  and the [matrix-path extension](../gaussian_axial_cone_rotations/MATRIX_PATHS.md),
  source `01b707bf3eb19f7bd44b8c45771fffa7b7651b55`, graph
  `bafkreigbbgjyf5dy5wbhowdlqdrsc24ykargcfqfc6xzir4lvktnyxzmry`, height 6118.
  They prove all-law comparisons on specified domains by geometric motions.
  Hence the common-set condition follows there abstractly. Our result neither
  extends their motion domains nor reoptimizes their path thresholds.
- Researcher 8's [ordered-weight theorem](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md),
  source `6056a43fd6c806cc2d92243e551528e238e40a23`, graph
  `bafkreihyai4xolryx3kpmntk4velamfjwaywuer6omhwvpttyqvmqexpy4`, height 6114.
  Its ordered radial laws and geometric consequence are retained. An
  unrestricted probability simplex cannot be substituted for its ordered
  cone when using Theorem 1. This note removes no ordering hypothesis.
- Researcher 7's [all-variance paired-layer theorem](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md),
  source `465f892ad569fe12fb2634395c21bc7025abff41`, graph
  `bafkreib4j6gpea55bkfajd73g2tcmfr5bvdhulhaeqjcw5v5guw2miflki`, height 6100.
  This remains a positive restricted family. Neither method obstructions
  nor finite positive energy searches supply an actual negative hinge.

No teammate result has gained independent mathematical acceptance from
this note. None of the motion/orbit theorems is a premise of the minimax
or sphere proofs. They are cited to identify the all-law quantifier and
avoid treating a new dual formulation as a new positive class.

## Reproduction and limits

CPython 3.11.2, standard library only. Both ordinary and optimized runs of
`verify.py --check` return

```text
GAUSSIAN_PRIOR_LOCALIZATION_EXACT_CONTROLS_PASS 57b2df033feba47c4ced4965e1c7964fa60472511e7186d5bc0fb6b042d8d657
```

The checker compares two exact expressions for 41 hyperbolic coefficients
and two expressions for exponential-kernel tensor coefficients through
degree 16 on two spherical fixtures. Two finite-cell saddle examples
verify signs and contact normalization while showing that purification
would fail in the presence of tied levels. One has negative value; it is
explicitly not Gaussian data or a contraction counterexample.

These finite checks supplement the written proof. They do not establish
the infinite-dimensional minimax theorem, polynomial density, or all-order
convergence by testing finitely many indices. Those steps are proved or
explicitly cited in the text. There are no external datasets, solver
verdicts, floating-point integrals, omitted large certificates or formal
proofs. The remaining trust is the written derivation and standard
functional-analysis facts. The mathematical contribution is an exact
reduction and a limitation of optimizer localization, not a resolution of
the campaign's full objective.


## Effective rational frontier and finite-atomic handoff

[RATIONAL_INTERFACE.md](RATIONAL_INTERFACE.md) supplies an explicit finite
rational producer for the existing compact frontier; [RATIONAL_INPUTS.json](RATIONAL_INPUTS.json)
pins each premise and distinguishes scope comparisons from dependencies.

The base localization is this lane's h6134, source
`4ed178725774e2fd3bb486f952825f58e52766cc`. Its proof bytes and k^6 atom
bound are unchanged. R8's [uniform frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
h6150, source `88bc098a0f98080f8762ddae9b11cc4e63669e95`, supplies the
2^16 k^8 largest power and the bound14/(3k); neither is claimed anew here.
R5's [global criterion](../gaussian_majorisation_global_criterion/PROOF.md),
h6088, source `713e542a0bd389681a3fb4ee0c0b61a4f272f104`, supplies the
beta probability-kernel and replica identities used by both inputs.
The earlier [strict rational-witness proof](../gaussian_majorisation_rank_abel/PROOF.md),
h5964, already uses strictification and rational approximation. The new
step is to control separation first, allowing fixed denominators, a
uniform approximation budget, explicit finite input counts and a stated
moment precision rather than an unspecified sufficiently small perturbation.
No priority is claimed for greedy nets, largest remainders or norm bounds.

The new rounding loss161/(256k) transfers directly to every beta average.
It is added to the existing global error rather than multiplied by
alternating moment coefficients. Arithmetic errors in individual moment
values are different: the note separately bounds that amplification by
(N+1)3^N. This distinction is part of the producer/consumer contract.

For R2, the [degree barrier](../gaussian_certificate_degree_barrier/PROOF.md),
source `e90c31e08a4c1487fde4c43261aa222dcbb9cd16`, concerns the supplied
exact positive-certificate recipe for one pair. The rational frontier
gives an absolute-error global approximation and does not repair or refute
that barrier. For R8, the [common-set stability interface](../gaussian_common_set_stability/INTERFACE.md),
source `07dc648282cc625294828c885b9c0365cdf15851`, can use the new exact
non-point pair-loss floor1/(2048k^18). Reference coefficient bounds and
the source-set error remain separate requirements. That optional consumer
is not a premise of the rationalization or the global approximation.
No sign is silently supplied by positivity of one energy or pair loss.

The standard-library implementation accepts exact rational inputs only,
checks original contractions, merges nearby labels, expands sources,
rounds both endpoints and rounds masses. Its six controls cover tight
rotations, collisions, zero weights, coincident targets and point laws.
The unmerged two-site rounding shortcut produces integer loss-1 and is
rejected; the actual producer merges it. Four malformed inputs are
rejected, also under optimized Python. Five budget rows and91 exact
coefficient-norm controls supplement the all-k inequalities in the proof.
No Gaussian moment, beta value or exhaustive parameter set is evaluated.

CPython3.11.2 normal and optimized runs agree on canonical report SHA256
`22f543a40f8a2a1298ce2ff933bb78422f57528b032db957b5d481725d1d227c`.
The complete universal argument is a written author proof using the cited
localization and moment results. This supplement has no independent
mathematical acceptance or formalization. It changes no prior theorem's
source or constants and yields no new Kneser--Poulsen consequence.

The final source refresh inspected R8's [weight-cell producer](../gaussian_beta_weight_certificate/certificate.py), source `a006501b012a7084676d632df4d73af1fdd92a58`. The integer-center output here decodes directly to its rational `Cell` input at squared-distance radius zero. Its current code has beta degree N=5 fixed and needs at least seven labels. The higher degree in the present global bound is not implemented or certified by that packet. No seven-distinct coefficient enclosure or full-row replay was duplicated in this pass.


## Paired cubature and the smaller atom budget (pass 7)

The new [CUBATURE_FRONTIER.md](CUBATURE_FRONTIER.md) applies established
approximation methods to the two linked marginals of an arbitrary
contraction. It claims the explicit campaign-bound improvement, not
invention of cubature or local Gaussian moment matching.

* Christian Bayer and Josef Teichmann, [The proof of Tchakaloff's
  theorem](https://arxiv.org/abs/math/0502473), in particular Corollary2
  of the [author manuscript](https://people.math.ethz.ch/~jteichma/tchakaloff120405.pdf),
  supplies finite-function cubature on actual input sites. Our compact
  application also follows directly from Caratheodory's convex-hull theorem.
* Yun Ma, Yihong Wu and Pengkun Yang, [On the best approximation by finite
  Gaussian mixtures](https://arxiv.org/html/2404.08913v2), Section3 and
  Section5.4/Proposition5, explicitly develop local moment matching and
  multidimensional approximation. These methods predate this campaign.
  Our Gaussian-kernel tail estimate is rederived in the note with its
  normalization and constants, without importing their rate theorem.
* The original [shifted-cell localization](DEFECT_LOCALIZATION.md), h6134,
  supplies the support-independent large cube and its source-overlap cost.
  The new ingredient at the campaign interface is simultaneous matching
  of source and image coordinate moments with common weights, followed
  by explicit schedules. Matching each marginal on unrelated supports
  would not retain the given contraction.
* R8's [uniform frontier](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md),
  h6150, supplies its radius-only Theorem2 and the same density-power degree.
  The coordinate moments used for cubature are different from this beta
  testing row. R5's [global criterion](../gaussian_majorisation_global_criterion/PROOF.md),
  h6088, supplies the normalized beta/replica identities.
* The [prior rationalization](RATIONAL_INTERFACE.md), h6194, supplies the
  feasible geometric rounding and the arithmetic-error calculation. Its
  atom bound and weight denominator are changed explicitly in the new
  producer; the older code is not retroactively treated as implementing
  the new contract. Only four elementary exact helper functions are reused.
* The current [R8 N=5 consumer](../gaussian_beta_weight_certificate/certificate.py),
  h6190, and [R2 uniform defect bound](../gaussian_uniform_defect_bound/PROOF.md),
  h6186, retain their distinct scope. Neither signs the required full row
  on the newly smaller finite frontier. No numerical improvement on7/50,
  new positive map class, or Kneser--Poulsen consequence is asserted.

[CUBATURE_INPUTS.json](CUBATURE_INPUTS.json) pins all reused source and labels
context separately from premises. The finite exact controls are author
checks only. Universal Caratheodory existence, Gaussian integration, TV
error transfer and the credited localization/beta proofs are unformalized.
Historical priority for the paired application has not been established.

The final source refresh also reads the [centroid-projection proof](../gaussian_beta_projection/PROOF.md)
and the stronger [pair-conditioning proof](../gaussian_beta_pair_conditioning/PROOF.md).
The latter signs all beta indices with N-j<=6, so the first unsigned index
is now b_(7,0). These are optional analytic pruning results, not premises
of the smaller atom bound. The [independent geometric review](../gaussian_beta_geometry_review_r6/REVIEW.md)
accepts both sign strips within their stated scope; it does not review
the localization or cubature theorem.
The [independent second review](../gaussian_uniform_defect_bound_review2/REVIEW.md),
committed at h6204, accepts the separate bound D<=7/50. That review does not
cover the present cubature proof. No teammate computations were replayed.

## Square-root threshold budget (pass 8)

[SQUARE_ROOT_BUDGET.md](SQUARE_ROOT_BUDGET.md) keeps the same compact and
rational configuration families, beta normalization and replica identities.
Its new campaign estimate combines the support-ball superlevel bound from
R8's h6150 with the unit-mass bound u C V(Cu)<=1. This makes H Lipschitz as
a function of sqrt(u), with an explicit constant of order r^(3/2). The
resulting degree is of order k^5 instead of k^8. No unknown sign or optimal
approximation rate is asserted.

The positive kernel used to convert that modulus into the beta estimate is
classical. Syed Abdul Mohiuddine, Tuncer Acar and Mohammed A. Alghamdi,
[Genuine modified Bernstein--Durrmeyer operators](https://link.springer.com/article/10.1186/s13660-018-1693-z),
Journal of Inequalities and Applications 2018, article 104, equations
(2.1)--(2.5), record the genuine operator at the identity coordinate and
its moments, crediting earlier work of Chen and Goodman--Sharma. Weighted
approximation in this setting is established, not invented here. The new
note derives its particular square-root error directly from the variance;
no external approximation theorem or unspecified constant is imported.

The compact atom/rational schema is the previous paired-cubature result,
now committed at h6212. The degree note uses the existing beta identity
from R5's h6088 and the all-degree perturbation/precision estimates from
h6194. It does not alter the prior paired producer or expected record.
[WEIGHTED_INPUTS.json](WEIGHTED_INPUTS.json) pins these concrete inputs and
the previous R8 modulus. The previously deferred cubature contribution was
confirmed with its exact body and all thirteen initial relations before
this new degree handoff.

The [finite checker](weighted_degree.py) evaluates beta square-root moments
by a positive product and separately by exact polynomial density integration.
Whole-interval Bernstein certificates check the kernel risk at finitely many
degrees. Those controls do not prove the all-degree assertion by extrapolation,
evaluate a Gaussian moment, or certify a signed configuration. The universal
geometric, integration and calculus arguments remain a written author proof.

## Direct hinge evaluation and certified defect refinement (pass 9)

[DIRECT_HINGE.md](DIRECT_HINGE.md) connects the accepted paired-cubature
frontier to actual all-threshold defect enclosures. The mathematical tools
are classical trapezoidal Peano kernels, variation of a convex truncation,
Gaussian tail bounds, and maximization of a piecewise-linear function by
sorting its knots. Their needed forms and constants are derived completely
in the note; no novelty or optimal quadrature rate is claimed. This evaluates
the existing hinge itself, rather than adding equivalent energy classes.

The local new estimate is a uniform O(h^2) spatial quadrature error despite
the nonsmooth threshold, independent of atom count and diameter. Exact
fixed-point exponentials and an all-knot sweep then replace literal replica
enumeration when a bounded-error defect value, rather than a symbolic beta
sign, is required. The public integer checker, three refinement controls,
an intentionally noncontracting positive-defect control, and independent
radial Gaussian checks reproduce the stated numerical conclusions.

Only the paired-cubature atom/radius theorem and the existing uniform hinge
rounding estimate are needed to compose this oracle with the unrestricted
frontier. [DIRECT_INPUTS.json](DIRECT_INPUTS.json) pins their source. The
[independent paired-cubature review](../gaussian_paired_cubature_review2/REVIEW.md),
committed at h6218, accepts that dependency. The subsequent
[square-root-budget review](../gaussian_square_root_budget_review2/REVIEW.md)
accepts the previous degree result; neither review covers this new oracle.
The degree result is contextual here, not a premise of the direct estimate.

The primary [Aishwarya--Li source](https://arxiv.org/html/2609.07041v2) was
refreshed live. Its Conjecture1.1 in R3 is still the sole problem source.
The separately accepted [uniform 7/50 bound](../gaussian_uniform_defect_bound/PROOF.md)
is an optional cap on a future complete-cover upper bound. It is not
numerically improved by checking a single configuration.

Current team context was read without replaying unrelated computations:
R2's [peak pruning](../gaussian_beta_peak_pruning/PROOF.md) signs a growing
beta block but proves that a low-index block necessarily remains; R4's
[full orthocentric-flap motion](../gaussian_flap_selector_motion/PROOF.md)
gives a theorem for that broad class with volume consequences, now accepted
by [R7's scoped independent review](../gaussian_flap_selector_review_r7/REVIEW.md);
R6 independently accepts R1's fixed-data local theorem.
None of these inputs is used as if it were an unrestricted sign. The
direct oracle remains applicable to the paired-cubature family with its
unchanged huge configuration count. No complete cover, exact-zero decision
procedure, or new Kneser--Poulsen conclusion is claimed in this packet.

## Threshold-relative sign certificates (pass 10)

[RELATIVE_HINGE.md](RELATIVE_HINGE.md) changes the numerical error scale,
using the equal-mass identity for clipped densities. Classical midpoint
Peano kernels and the positive variation of a concave clip supply a
threshold-proportional bound. The proof derives its constants and handles
critical levels, arbitrary mixing laws, and the finite-cube boundary.
The all-window rational ratio sweep and exact coordinate-table compression
are new implementations; their standard underlying methods are not claimed
as inventions. The exponentials are the existing pass-9 certified routine.

R8 already proved the
[signed endpoint/middle architecture](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
and [low-threshold geometric estimate](../gaussian_majorisation_open_stability/PROOF.md).
Those results were read and retained as dependencies for a possible
all-threshold consumer, rather than reproved as a new bridge. The present
window oracle has an independent, self-contained quadrature proof and does
not assume a positive Gaussian sign or a mean-width margin. Its role on
the paired-cubature spine is evaluation and sign certification of the actual
finite instances, with cost polynomial in the logarithmic threshold radius
at fixed support and fixed relative accuracy.

The control is a classical two-point collapse with a continuous contracting
motion. It is used to test the certificate at tiny thresholds, not offered
as a new class. Source-relative error and target-relative error are combined
in the adverse convention, opposite to the beta profiles. The full sweep
tests every knot. No floating evaluation is a mathematical premise.

The fresh R8 [seven-factor result](../gaussian_seven_factor_kernel/PROOF.md),
source commit f5bbd92be43517c18a6958acf900ddd67bac62f8, proves the universal
strip N-j<=7. The final refresh found R5's
[independent acceptance](../gaussian_seven_factor_review_r5/REVIEW.md),
source c93cddbbe5e3943acead1d964d8de2cce6a419de; its complete scope and
independence statement were read without replaying the computation.
The first general unsigned entry is now b_(8,0). This replaces the earlier
context above but is not a premise of the quadrature theorem. R2's
[endpoint-scatter obstruction](../gaussian_beta_endpoint_scatter_obstruction/PROOF.md)
closes that particular positive-representation method without contradicting
the seven-factor sign. Both were inspected before this pass's target was
selected. The primary [Aishwarya--Li v2 source](https://arxiv.org/html/2609.07041v2)
was checked live; the unrestricted Conjecture1.1 in R3 remains the target.

[RELATIVE_INPUTS.json](RELATIVE_INPUTS.json) pins the exact code and analytic
interfaces consumed. This packet supplies no all-configuration signed cover,
unrestricted theorem, counterexample, or new Kneser--Poulsen consequence.

## Uniform signed rational-frontier endpoints (pass 11)

[SIGNED_ENDPOINTS.md](SIGNED_ENDPOINTS.md) consumes the unchanged strict
pair-loss, radius and weight floors of the accepted paired-cubature rational
frontier. Its contribution is an explicit mean-support margin and a uniform
signed low-threshold cutoff for the whole finite family, followed by a
source-peak endpoint. The constants and executable certificate discharge
previously external endpoint inputs. They do not sign the middle interval.

Mean-width monotonicity is classical. The primary manuscript
[Gorbovickis, Strict Kneser--Poulsen conjecture for large radii](https://arxiv.org/pdf/1006.0531),
Theorem 1.4, states the non-strict comparison and attributes it to Sudakov,
Alexander, Capoyleas and Pach. Its Theorem 1.5 strengthens this to strictness;
we do not need that strengthening. Factoring out a small target homothety
and using the mean support of a diameter segment supplies our quantitative
lower bound. Neither mean-width monotonicity nor the usual Gaussian
interpolation proof included for normalization is claimed as new.

R8's [low-threshold lemma](../gaussian_majorisation_open_stability/PROOF.md),
Section 2, is the analytic sign premise, and its
[finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
already owns the endpoint/middle architecture. The new formulas use that
architecture rather than introducing an equivalent test class. R2's
[peak-pruning proof](../gaussian_beta_peak_pruning/PROOF.md) already uses the
standard Gaussian pair-overlap inequality; its source-only specialization
provides the other endpoint here. All consumed versions are pinned in
[SIGNED_ENDPOINT_INPUTS.json](SIGNED_ENDPOINT_INPUTS.json).

The final team refresh found independent acceptance of the
[absolute direct-hinge oracle](../gaussian_direct_hinge_review_frontier/REVIEW.md),
graph6271, and of the
[effective indecomposable bound](../gaussian_effective_indecomposable_review2/REVIEW.md).
These reviews do not review the present supplement. R8's new
[small-radius defect estimate](../gaussian_majorisation_high_noise_window/SMALL_RADIUS_DEFECT.md)
gives an exponentially decreasing all-threshold error near collapsed support,
uniformly over bounded laws, and is complementary to this strict finite
endpoint sign. It is an author proof awaiting review, not a premise here.

R2's [conditional-kernel obstruction](../gaussian_conditional_kernel_obstruction/PROOF.md),
now graph6267, rules out all-order pointwise conditional positivity on every
rank-six paired geometry. We retain actual endpoint averaging throughout.
The universal strip through seven factors remains independently accepted;
the first general unsigned beta is still b_(8,0). Neither conditional
failure nor the new endpoint signs change that status. The prior
[covariance-free rigidity proof](../gaussian_contraction_covariance_free/PROOF.md)
was inspected and a duplicate small-distance-loss route was set aside.

The primary [Aishwarya--Li v2 source](https://arxiv.org/html/2609.07041v2)
and Gorbovickis's primary manuscript were checked live. A bounded search on
Gaussian low thresholds, mean width, strict contraction and large-radius
Kneser--Poulsen found the classical geometric background and the team's
existing tail theorem. The claimed progress is the effective signed handoff
on the existing rational frontier, not a historical-priority claim about
those mechanisms. No new positive Kneser--Poulsen class is asserted.
