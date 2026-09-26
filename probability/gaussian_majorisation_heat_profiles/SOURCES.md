# Sources, dependencies, and novelty boundary

The sole problem source is Gautam Aishwarya and Dongbin Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*](https://arxiv.org/html/2609.07041v2), arXiv:2609.07041v2.
The paper was inspected live on 26 September 2026. Its unrestricted
dimension-three majorisation question remains open in this work. Its
continuous-contraction theorem proves the endpoint comparison for our
explicit diagonal motion; that positive comparison is not new here.
The paper itself warns that volume contraction alone does not suffice.

The concentration profile, coarea computation, and use of parabolic
comparison belong to classical symmetrization theory. A primary modern
source spelling out concentration order and the classical parabolic
Talenti framework is Idriss Mazari,
[*A note on the rearrangement of functions in time and on the parabolic
Talenti inequality*](https://arxiv.org/html/2203.05913v1), Sections 1.1--1.3.
Its time-rearrangement obstruction concerns a different forced PDE;
we do not identify that theorem with our finite contraction example.
All identities required here are derived in PROOF.md.

The particular output of this pass is a strict injective six-atom
contraction that reverses the proposed diffusion-coefficient comparison,
with a rationally certified gap at variance one and an analytic reversal
at every fixed variance at least one. It is new to the inspected team
artifacts; no literature-priority claim is made for the underlying
rearrangement identities or for the general need to retain level geometry.

## Team context inspected before choosing the route

- **Researcher 5, fixed-atom reduction:**
  [ANCHOR_REDUCTION.md](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md),
  commit `138993ba3ec2efde720c789a2a3d887c9c417c69`, graph
  `bafkreievpgikszwz2kggan4dnfbbhvtvjohiycou6xuhlsqpxjvvxrhaai`
  (6112). This shows why a neighborhood of a dominant Gaussian atom is
  not enough without control of the arbitrary separated remainder and
  all thresholds. It is context, not a premise of the coefficient calculation.
- **Researcher 6, axial-cone robustness:**
  [ROBUSTNESS.md](../gaussian_axial_cone_rotations/ROBUSTNESS.md), graph
  `bafkreico6twre4tzlewepj3ej7vay764gyeajof4ni25s4jksd3p4sed2y`
  (6104), and the subsequent
  [MATRIX_PATHS.md](../gaussian_axial_cone_rotations/MATRIX_PATHS.md),
  commit `01b707bf3eb19f7bd44b8c45771fffa7b7651b55`, graph
  `bafkreigbbgjyf5dy5wbhowdlqdrsc24ykargcfqfc6xzir4lvktnyxzmry`
  (6118). Those prove positive geometric classes by lifted motions.
  This packet neither enlarges nor reclassifies those classes.
- **Researcher 7, counterexample lane:** the completed bounded search
  report supplies no rigorous hinge counterexample; apparent tiny negative
  quadrature values were not promoted to failures. Its finite positive
  moment audit is not an all-order theorem. The durable positive endpoint is
  [ALL_VARIANCES.md](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md),
  graph `bafkreib4j6gpea55bkfajd73g2tcmfr5bvdhulhaeqjcw5v5guw2miflki`
  (6100). Our negative statement instead has a proved asymptotic and exact
  rational constants, and explicitly concerns a proposed coefficient sign.
- **Researcher 8, ordered weights:**
  [ORDERED_WEIGHTS.md](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md),
  commit `6056a43fd6c806cc2d92243e551528e238e40a23`, graph
  `bafkreihyai4xolryx3kpmntk4velamfjwaywuer6omhwvpttyqvmqexpy4`
  (6114). The finite-orbit correlation proof and its unequal-radius
  consequence do not supply a pointwise sign for the heat coefficient.
- **Earlier instantaneous lift obstruction:**
  [PROOF.md](../gaussian_majorisation_local_lift_obstruction/PROOF.md),
  graph `bafkreifseyjs3jimzu7yvo3lpfd3555dmnf5q6hraqdonaldti3nqjgxqy`
  (5980). That result disproves instantaneous transformed Hankel positivity
  along a six-dimensional spatial lift. The present variable is Gaussian
  variance and the present test is a level-surface product in three-space;
  neither obstruction implies the other calculation.

Researcher 5's
[endpoint coupling criterion](../gaussian_majorisation_global_criterion/PROOF.md)
is complementary. Formula (8) here is a stopped adjoint representation
for an actual heat evolution on a regular rectangle, not a relabelling
of the optimal endpoint density-value coupling. No teammate source is
imported by the exact audit.

The final source refresh added the
[all-prior set-transfer reduction](../gaussian_prior_localization/PROOF.md),
commit `541d4b7de3d73b41444e5350378a8ecc43d914ea`, and the latest
[dependency handoff](../gaussian_majorisation_global_criterion/DEPENDENCIES.md),
commit `713e542a0bd389681a3fb4ee0c0b61a4f272f104`, graph
`bafkreidn73gtnin3ojvmr6hz6hipasfpf6hl7uhhu3szlauiqhwpkvte2q` (6120).
The set-transfer proof also uses the classical concentration/hinge duality;
its minimax and diffuse-optimizer statements are not premises here.
Our new identities concern evolution in Gaussian variance for a fixed
pair, rather than exchange of the quantifier over priors.

The inverse tube-volume rate and explicit tail bounds in Section 2 quantify
the already known Gaussian-to-Kneser--Poulsen implication in the primary
paper and researcher 5's
[geometric limit](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md).
The claimed distinction is their use as singular initial data for the
profile equation, not a new implication or a new positive ball theorem.
Their constants depend on atom count and the minimum weight.

The newest completed reports from researchers 2--4 still concerned the
parked finite-geometry target at the initial refresh; none was used as
a Gaussian premise. Their ongoing work is not being directed by this lane.

## Verification and trust

The analytic proof uses elementary Gaussian differentiation, coarea,
the divergence and implicit-function theorems, isoperimetry, and the
standard stopped Ito formula. Its regular-level hypotheses are explicit.
The exact script uses Python arbitrary-precision integers and Fractions;
alternating-series errors bound exponentials without a numerical library.
It verifies finite constants, not the analytic theorems or an explicit
volume cutoff. There is no claim of an independent peer review or a
proof-assistant formalization.

No full-domain parabolic comparison has been proved, and no new positive
Kneser--Poulsen consequence is obtained. The substantive handoff is the
failure of coefficientwise closure, together with the exact signed
evolution term a different estimate must control.
