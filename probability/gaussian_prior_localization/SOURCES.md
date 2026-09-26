# Sources, dependencies and trust boundary

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
